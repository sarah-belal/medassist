import json
import os
import time
import boto3
import anthropic

client = anthropic.Anthropic()
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')
sns = boto3.client('sns', region_name='us-east-2')
table = dynamodb.Table('medassist-products')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-2:516217483779:medassist-alerts'

system_prompt = """
You are a medical assistant. When a user asks about a health problem, you must respond only in JSON in this exact format:
{
    "condition": "name of the likely condition",
    "explanation": "plain language explanation",
    "severity": "mild, moderate, or see_doctor",
    "categories": ["category1", "category2"],
    "supplement_categories": ["supplement_category1", "supplement_category2"],
    "when_to_see_doctor": "describe warning signs",
    "disclaimer": "a standard medical disclaimer"
}

For categories and supplement_categories, use ONLY from this list:
OTC categories: pain_relief, allergy, skin_rash, cold_flu, digestive
Supplement categories: supplement_immune, supplement_skin, supplement_pain, supplement_digestive

Pick the 1-2 most relevant categories for the condition.

rules:
never recommend prescription medication.
If the symptoms sound serious, set severity to see_doctor.
IMPORTANT: Return ONLY raw JSON. No markdown code blocks or backticks."""

def send_metrics(condition, severity, duration_ms):
    try:
        cloudwatch.put_metric_data(
            Namespace='MedAssist',
            MetricData=[
                {
                    'MetricName': 'QueryCount',
                    'Value': 1,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'ResponseTime',
                    'Value': duration_ms,
                    'Unit': 'Milliseconds'
                },
                {
                    'MetricName': 'SeverityCount',
                    'Dimensions': [{'Name': 'Severity', 'Value': severity}],
                    'Value': 1,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'ConditionCount',
                    'Dimensions': [{'Name': 'Condition', 'Value': condition[:50]}],
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
    except Exception as e:
        print(f"Metrics error: {str(e)}")

def send_notification(question, condition, severity):
    try:
        message = f"""New MedAssist Query!

Symptom: {question}
Condition: {condition}
Severity: {severity}
"""
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"MedAssist - {condition} ({severity})",
            Message=message
        )
    except Exception as e:
        print(f"SNS error: {str(e)}")

def get_products_from_db(categories):
    products = []
    for category in categories:
        try:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('category').eq(category)
            )
            products.extend(response.get('Items', []))
        except Exception as e:
            print(f"Error querying category {category}: {str(e)}")
    return products

def get_health_response(question):
    start_time = time.time()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    result_text = response.content[0].text
    result_text = result_text.strip()
    if result_text.startswith("```"):
        result_text = result_text.split("\n", 1)[1]
    if result_text.endswith("```"):
        result_text = result_text.rsplit("```", 1)[0]
    result_text = result_text.strip()
    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse response", "raw": result_text}

    duration_ms = (time.time() - start_time) * 1000

    send_metrics(
        result.get("condition", "unknown"),
        result.get("severity", "unknown"),
        duration_ms
    )

    send_notification(
        question,
        result.get("condition", "unknown"),
        result.get("severity", "unknown")
    )

    otc_products = get_products_from_db(result.get("categories", []))
    supplements = get_products_from_db(result.get("supplement_categories", []))

    result["otc_products"] = otc_products
    result["supplements"] = supplements

    return result

def lambda_handler(event, context):
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    try:
        body = json.loads(event["body"])
        question = body["question"]

        if not question:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "No question provided"})
            }

        result = get_health_response(question)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }