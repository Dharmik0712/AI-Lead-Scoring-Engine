import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

tier_1 = ['Mumbai', 'Delhi', 'Bangalore']
tier_2 = ['Pune', 'Ahmedabad', 'Chandigarh']
tier_3 = ['Indore', 'Rajkot', 'Nagpur']
cities = tier_1 + tier_2 + tier_3

def generate_lead():
    city = random.choice(cities)
    return {
        "lead_id": fake.uuid4(),
        "name": fake.name(),
        "age": random.randint(21, 60),
        "city": city,
        "city_tier": (
            1 if city in tier_1 else
            2 if city in tier_2 else 3
        ),
        "occupation": random.choice(["Salaried", "Self-Employed", "Student", "Freelancer", "Unemployed"]),
        "income_bracket": random.choice(["<5L", "5-10L", "10-20L", "20L+"]),
        "education_level": random.choice(["Undergrad", "Graduate", "Postgrad", "PhD"]),
        "num_site_visits": random.randint(0, 15),
        "avg_time_on_page": round(random.uniform(5, 150), 2),
        "form_filled": random.choice([0, 1]),
        "whatsapp_reply_count": random.randint(0, 5),
        "clicked_ad": random.choice([0, 1]),
        "bounced": random.choice([0, 1]),
        "referral_source": random.choice(["Paid Ad", "SEO", "Referral", "Email", "Organic"]),
        "ip_geolocation_verified": random.choice([0, 1]),
        "device_type": random.choice(["Mobile", "Desktop", "Tablet"]),
        "campaign_id": random.choice(["CAMP001", "CAMP002", "CAMP003"]),
        "crm_segment_tag": random.choice(["A", "B", "C"]),
        "linkedin_profile_exists": random.choice([0, 1]),
        "news_sentiment_about_company": round(random.uniform(-1, 1), 2),
        "company_size": random.choice(["<50", "50-200", "200-1000", "1000+"]),
        "industry_type": random.choice(["Tech", "Real Estate", "Finance", "Education", "Healthcare"]),
        "lead_created_at": fake.date_time_between(start_date='-30d', end_date='now'),
        "intent_score": round(random.uniform(0, 1), 2)
    }

data = [generate_lead() for _ in range(1000)]
df = pd.DataFrame(data)
df.to_csv("leads.csv", index=False)

print("✅ leads.csv generated with 1000 rows.")