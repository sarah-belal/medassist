import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('medassist-products')

products = [
    {"category": "pain_relief", "product_id": "pr1", "name": "Advil Ibuprofen 200mg", "active_ingredient": "Ibuprofen", "how_it_helps": "Reduces inflammation and blocks pain signals", "price": "$8.99", "url": "https://www.amazon.com/dp/B005UQLJEO"},
    {"category": "pain_relief", "product_id": "pr2", "name": "Tylenol Extra Strength 500mg", "active_ingredient": "Acetaminophen", "how_it_helps": "Blocks pain signals in the brain without anti-inflammatory effects", "price": "$9.49", "url": "https://www.amazon.com/dp/B0014DKPOU"},
    {"category": "pain_relief", "product_id": "pr3", "name": "Aleve Naproxen 220mg", "active_ingredient": "Naproxen sodium", "how_it_helps": "Long-lasting anti-inflammatory that reduces pain for up to 12 hours", "price": "$10.99", "url": "https://www.amazon.com/dp/B001G7QRA8"},
    {"category": "allergy", "product_id": "al1", "name": "Zyrtec 24HR 10mg", "active_ingredient": "Cetirizine HCl", "how_it_helps": "Blocks histamine receptors to reduce allergic reactions and itching", "price": "$14.99", "url": "https://www.amazon.com/dp/B001JQLNK4"},
    {"category": "allergy", "product_id": "al2", "name": "Claritin 24HR 10mg", "active_ingredient": "Loratadine", "how_it_helps": "Non-drowsy antihistamine that relieves allergy symptoms", "price": "$13.99", "url": "https://www.amazon.com/dp/B0012FPLMU"},
    {"category": "allergy", "product_id": "al3", "name": "Benadryl 25mg", "active_ingredient": "Diphenhydramine HCl", "how_it_helps": "Fast-acting antihistamine for severe allergic reactions and itching", "price": "$7.49", "url": "https://www.amazon.com/dp/B0011DMUAO"},
    {"category": "skin_rash", "product_id": "sr1", "name": "Cortizone-10 Maximum Strength", "active_ingredient": "Hydrocortisone 1%", "how_it_helps": "Reduces inflammation and itching by suppressing immune response in skin", "price": "$7.99", "url": "https://www.amazon.com/dp/B001G7QU4O"},
    {"category": "skin_rash", "product_id": "sr2", "name": "Calamine Lotion", "active_ingredient": "Zinc oxide and ferric oxide", "how_it_helps": "Provides cooling relief and helps dry out weeping skin while reducing itching", "price": "$5.99", "url": "https://www.amazon.com/dp/B001G7QHWU"},
    {"category": "skin_rash", "product_id": "sr3", "name": "Aquaphor Healing Ointment", "active_ingredient": "Petrolatum 41%", "how_it_helps": "Creates protective barrier to lock in moisture and promote skin healing", "price": "$11.99", "url": "https://www.amazon.com/dp/B006IB5T4W"},
    {"category": "cold_flu", "product_id": "cf1", "name": "DayQuil Severe Cold & Flu", "active_ingredient": "Acetaminophen, Dextromethorphan, Guaifenesin, Phenylephrine", "how_it_helps": "Multi-symptom relief for headache, fever, cough, congestion, and sore throat", "price": "$12.99", "url": "https://www.amazon.com/dp/B0051BHLZU"},
    {"category": "cold_flu", "product_id": "cf2", "name": "Mucinex DM 12HR", "active_ingredient": "Guaifenesin and Dextromethorphan", "how_it_helps": "Thins and loosens mucus while suppressing cough for 12 hours", "price": "$15.99", "url": "https://www.amazon.com/dp/B001G7QNGE"},
    {"category": "cold_flu", "product_id": "cf3", "name": "Chloraseptic Sore Throat Spray", "active_ingredient": "Phenol 1.4%", "how_it_helps": "Numbs sore throat on contact for fast pain relief", "price": "$6.49", "url": "https://www.amazon.com/dp/B001G7QTOG"},
    {"category": "digestive", "product_id": "dg1", "name": "Pepto-Bismol Original", "active_ingredient": "Bismuth subsalicylate", "how_it_helps": "Coats stomach lining and reduces inflammation to relieve nausea and diarrhea", "price": "$7.99", "url": "https://www.amazon.com/dp/B001G7QUOU"},
    {"category": "digestive", "product_id": "dg2", "name": "Tums Ultra Strength 1000", "active_ingredient": "Calcium carbonate 1000mg", "how_it_helps": "Neutralizes excess stomach acid for fast heartburn and indigestion relief", "price": "$6.49", "url": "https://www.amazon.com/dp/B001G7QVOE"},
    {"category": "digestive", "product_id": "dg3", "name": "Imodium A-D", "active_ingredient": "Loperamide HCl 2mg", "how_it_helps": "Slows intestinal movement to reduce diarrhea symptoms", "price": "$8.99", "url": "https://www.amazon.com/dp/B001G7QW8E"},
    {"category": "supplement_immune", "product_id": "si1", "name": "Nature Made Vitamin C 1000mg", "active_ingredient": "Ascorbic acid", "how_it_helps": "Supports immune cell function and acts as an antioxidant", "price": "$9.99", "url": "https://www.amazon.com/dp/B00008I8NI"},
    {"category": "supplement_immune", "product_id": "si2", "name": "Zicam Zinc Cold Remedy", "active_ingredient": "Zincum gluconicum", "how_it_helps": "May reduce duration and severity of cold symptoms when taken early", "price": "$11.99", "url": "https://www.amazon.com/dp/B0012FPLMU"},
    {"category": "supplement_immune", "product_id": "si3", "name": "Sambucol Black Elderberry", "active_ingredient": "Elderberry extract", "how_it_helps": "Rich in antioxidants and vitamins that may boost immune response", "price": "$14.99", "url": "https://www.amazon.com/dp/B000FNJ4MK"},
    {"category": "supplement_skin", "product_id": "ss1", "name": "Nature Made Vitamin E 400 IU", "active_ingredient": "dl-Alpha tocopheryl acetate", "how_it_helps": "Antioxidant that supports skin cell repair and reduces inflammation", "price": "$8.49", "url": "https://www.amazon.com/dp/B00008I8NU"},
    {"category": "supplement_skin", "product_id": "ss2", "name": "Sports Research Omega-3 Fish Oil", "active_ingredient": "EPA and DHA omega-3 fatty acids", "how_it_helps": "Reduces inflammatory response in skin and supports overall skin health", "price": "$21.99", "url": "https://www.amazon.com/dp/B00T0C9XRY"},
    {"category": "supplement_pain", "product_id": "sp1", "name": "Doctor's Best Magnesium Glycinate", "active_ingredient": "Magnesium glycinate", "how_it_helps": "Relaxes muscles and blood vessels, may reduce headache frequency", "price": "$12.99", "url": "https://www.amazon.com/dp/B000BD0RT0"},
    {"category": "supplement_pain", "product_id": "sp2", "name": "Nature's Way Feverfew", "active_ingredient": "Parthenolide", "how_it_helps": "Traditional herb that may help prevent headaches and reduce inflammation", "price": "$8.49", "url": "https://www.amazon.com/dp/B00014FZPS"},
    {"category": "supplement_digestive", "product_id": "sd1", "name": "Culturelle Daily Probiotic", "active_ingredient": "Lactobacillus rhamnosus GG", "how_it_helps": "Restores healthy gut bacteria balance and supports digestive health", "price": "$17.99", "url": "https://www.amazon.com/dp/B000FKDB2I"},
    {"category": "supplement_digestive", "product_id": "sd2", "name": "Heather's Tummy Fiber", "active_ingredient": "Organic acacia senegal fiber", "how_it_helps": "Gentle prebiotic fiber that regulates digestion without bloating", "price": "$13.99", "url": "https://www.amazon.com/dp/B0013OW2KS"},
]

for product in products:
    table.put_item(Item=product)
    print(f"Added: {product['name']}")

print(f"\nDone! Loaded {len(products)} products.")
