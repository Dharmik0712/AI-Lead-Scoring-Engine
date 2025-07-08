# 🚀 AI Lead Scoring Engine — Cleardeals Assignment

An end-to-end AI-powered real-time **Lead Scoring System** designed to help brokers prioritize high-intent leads by predicting an **intent score** using machine learning and semantic reranking.

---

## 📌 Problem Statement

> Brokers spend too much time on low-intent leads.
> Goal: Predict high-intent leads and improve conversion efficiency.

This solution delivers real-time **intent scores** via API using:

* A trained **Gradient Boosted Tree** (XGBoost) model
* Optional **LLM re-ranking** using MiniLM embeddings
* **Redis** for fast caching
* **FastAPI** to expose a scoring endpoint
* Async simulation of **CRM push integration**

---

## 🧰 Tech Stack

| Component       | Technology                    |
| --------------- | ----------------------------- |
| ML Model        | XGBoost                       |
| API Server      | FastAPI + Uvicorn             |
| Re-Ranker (LLM) | SentenceTransformers (MiniLM) |
| Cache           | Redis                         |
| Async Requests  | httpx                         |
| Dataset         | Synthetic (1000 leads)        |

---

## ⚙️ Features

* `/score` → Accepts lead info, returns predicted intent score in **<300ms**
* Redis caching for repeated leads
* `/rerank` → Reranks top leads using **semantic relevance**
* Async CRM push simulation
* Handles edge cases and missing fields gracefully

---

## 📁 Project Structure

```
cdt/
├── app.py                 # FastAPI server
├── model_utils.py         # Model loading & prediction
├── llm_reranker.py        # LLM-based lead reranking
├── train_model.py         # Training script (XGBoost)
├── generate_fake_leads.py # Creates 1000-lead dataset
├── leads.csv              # Simulated dataset
├── lead_score_model.pkl   # Trained XGBoost model
├── feature_columns.json   # Feature order mapping
├── requirements.txt
├── .env                   # Optional Redis config
└── README.md
```

---

## 🚀 Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Redis

```bash
redis-server
```

### 3. Run the API

```bash
uvicorn app:app --reload
```

### 4. Access API Docs

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Endpoints

### `/score` — POST

Predicts intent score in real-time. Accepts lead data.

### `/rerank` — POST

Accepts list of top leads + a `target_intent` string. Returns re-ranked leads by semantic similarity using MiniLM.

---

## 🧠 How It Works

* `XGBoost` model scores leads from tabular features
* Optional LLM (MiniLM) computes semantic similarity for top leads
* Redis caches past results
* Async CRM webhook simulated with `httpx`

---

## 🔐 Compliance

* No PII is stored or exposed
* All sensitive fields are excluded from scoring pipeline
* Designed to be **DPDP-ready**

---

## ✍️ Author

**Dharmik Sompura**
📧 Email: \[[your\_dharmiksompura1212@gmail.com](mailto:your_dharmiksompura1212@gmail.com)]

🔗 GitHub: \[[https://github.com/Dharmik0712](https://github.com/Dharmik0712)]

🔗 LinkedIn: \[[https://www.linkedin.com/in/dharmik-sompura/](https://linkedin.com/in/dharmik-sompura)]


