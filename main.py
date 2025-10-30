import requests
from fastapi import FastAPI
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

    # 응답 데이터를 파싱해서 반환
    return {"results": data.get("keywordList", [])}
