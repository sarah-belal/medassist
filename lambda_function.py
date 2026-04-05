import json
import os
import anthropic

client = anthropic.Anthropic()

system_prompt = """
You are a medical assistant. When a user asks about a health problem they are facing, you must respond only in JSON in this exact format:
{
    "condition": "name of the likely condition",
    "explanation": "plain language explanation",
    "severity": "mild, moderate, or see_doctor",
    "otc_products": ["product 1", "product 2", "product 3 is optional"],
    "supplements": ["supplement 1", "supplement 2"],
    "when_to_see_doctor": "describe warning signs",
    "disclaimer": "a standard medical disclaimer"
}
rules:
Recommend products that are the most suitable for their condition.
promote the use of natural supplements, especially if it is deemed useful in the scenario.
never recommend prescription medication.
If the symptoms sound serious, recommend the user to seek help from a medical doctor."""

def get_health_response(question):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    result_text = response.content[0].text
    try:
        result = json.loads(result_text)
        return result
    except json.JSONDecodeError:
        return {"error": "Failed to parse response", "raw": result_text}

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
