# IT Support Chatbot Production Advanced

## Create environment
```bash
pip install -r requirements.txt
```

## Train model
```bash
python scripts/train_intent_model.py
```

## Ingest knowledge
```bash
python scripts/ingest_knowledge.py
```

## Run FastAPI
```bash
uvicorn app.main:app --reload
```

## Run Streamlit
```bash
streamlit run frontend/streamlit_app.py
```

## API docs
Open: http://127.0.0.1:8000/docs
