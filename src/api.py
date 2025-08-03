from fastapi import FastAPI
from src.database.database import load_all_tenders

app = FastAPI()

@app.get("/tenders")
def get_tenders():
    return load_all_tenders()
