from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
from model_utils import predict
from llm_reranker import rerank_leads
import httpx
import asyncio
app = FastAPI()

r = redis.Redis(host="localhost", port=6379, db=0)

class LeadData(BaseModel):
    age: int
    city: str
    city_tier: int
    occupation: str
    income_bracket: str
    education_level: str
    num_site_visits: int
    avg_time_on_page: float
    form_filled: int
    whatsapp_reply_count: int
    clicked_ad: int
    bounced: int
    referral_source: str
    ip_geolocation_verified: int
    device_type: str
    campaign_id: str
    crm_segment_tag: str
    linkedin_profile_exists: int
    news_sentiment_about_company: float
    company_size: str
    industry_type: str

@app.post("/score")
async def score_lead(lead: LeadData):
    lead_dict = lead.dict()
    lead_key = json.dumps(lead_dict, sort_keys=True)
    
    cached = r.get(lead_key)
    if cached:
        return {
            "intent_score": float(cached),
            "cached": True
        }

    score = predict(lead_dict)
    r.set(lead_key, float(score), ex=3600)
    asyncio.create_task(push_to_crm(lead_dict, score))
    return {
        "intent_score": float(score),  
        "cached": False
    }

async def push_to_crm(lead: dict, score: float):
    crm_data = {
        "lead_id": lead.get("lead_id", "N/A"),
        "intent_score": score,
        "action": "Store to CRM"
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post("http://example.com/webhook", json=crm_data)
            # response = await client.post("https://webhook.site/your-url", json=crm_data)
            # print("✅ Pushed to CRM:", response.status_code)
    except:
        pass
    # except Exception as e:
    #     print("❌ CRM push failed:", e)

@app.post("/rerank")
def rerank(data: dict):
    leads = data.get("leads", [])
    query = data.get("target_intent", "")
    
    if not leads or not query:
        raise HTTPException(status_code=400, detail="Missing leads or target_intent")
    
    return rerank_leads(leads, query)