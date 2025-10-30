import os
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

class KeywordRequest(BaseModel):
    keyword: str

@app.post("/doNaverKeywordResearch")
def research_keyword(req: KeywordRequest):
    client_id = "jfukBkhOOaE9gihs00Qr"
    client_secret = "3askZuE5jE"
    url = "https://api.searchad.naver.com/keywordstool"

    headers = {
        "X-API-KEY": client_secret,
        "X-API-AD-ACCOUNT-ID": client_id
    }
    params = {
        "hintKeywords": req.keyword,
        "showDetail": 1
    }

    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    return {"results": data.get("keywordList", [])}

# ✅ .well-known 디렉토리를 정적(static) 파일로 서빙
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/.well-known",
    StaticFiles(directory=os.path.join(BASE_DIR, ".well-known")),
    name="well-known"
)
