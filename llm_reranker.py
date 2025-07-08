import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer, util

xgb_model = joblib.load("lead_score_model.pkl")
df = pd.read_csv("leads.csv")

df["text_blob"] = df[["occupation", "industry_type", "campaign_id", "crm_segment_tag"]].astype(str).agg(" ".join, axis=1)

X = df.drop(columns=["lead_id", "name", "lead_created_at", "intent_score", "text_blob"], errors="ignore")
X = pd.get_dummies(X)
X.columns = [col.replace('[', '').replace(']', '').replace('<', '').replace('>', '').replace(' ', '_') for col in X.columns]

feature_cols = pd.read_csv("feature_columns.csv", header=None)[0].tolist()
for col in feature_cols:
    if col not in X.columns:
        X[col] = 0
X = X[feature_cols]

df["xgb_score"] = xgb_model.predict(X)

top_leads = df.sort_values(by="xgb_score", ascending=False).head(10).copy()

embedder = SentenceTransformer('all-MiniLM-L6-v2')  

def rerank_leads(leads: list, target_intent: str):
    intent_embedding = embedder.encode(target_intent.lower(), convert_to_tensor=True)

    for lead in leads:
        blob = " ".join([
            str(lead.get("occupation", "")),
            str(lead.get("industry_type", "")),
            str(lead.get("campaign_id", "")),
            str(lead.get("crm_segment_tag", "")),
            str(lead.get("campaign_notes", "")),
            str(lead.get("user_message", ""))
        ]).lower()
        
        lead["similarity"] = util.cos_sim(
            embedder.encode(blob, convert_to_tensor=True),
            intent_embedding
        ).item()
    
    return sorted(leads, key=lambda x: x["similarity"], reverse=True)

target_intent = "Looking for mutual fund buyers from tech industry"

intent_embedding = embedder.encode(target_intent, convert_to_tensor=True)
top_leads["embedding"] = top_leads["text_blob"].apply(lambda x: embedder.encode(x, convert_to_tensor=True))
top_leads["similarity"] = top_leads["embedding"].apply(lambda emb: util.cos_sim(emb, intent_embedding).item())

final_reranked = top_leads.sort_values(by="similarity", ascending=False).drop(columns=["embedding"])

print("✅ Top leads after LLM re-ranking:\n")
print(final_reranked[["name", "occupation", "industry_type", "xgb_score", "similarity"]])