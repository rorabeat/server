import os
import time
import hmac
import hashlib
import base64
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# ✅ 환경변수 로드 (.env 파일에서 API 키 읽기)
load_dotenv()

app = FastAPI()

class KeywordRequest(BaseModel):
    keyword: str

@app.post("/doNaverKeywordResearch")
def research_keyword(req: KeywordRequest):
    # ✅ 네이버 SearchAd API 기본 설정
    API_BASE = "https://api.searchad.naver.com"
    uri = "/keywordstool"
    method = "GET"

    # ✅ 환경 변수에서 인증 정보 읽기
    api_key = os.getenv("NAVER_API_KEY")
    secret_key = os.getenv("NAVER_SECRET_KEY")
    customer_id = os.getenv("NAVER_CUSTOMER_ID")

    if not (api_key and secret_key and customer_id):
        return {"error": "환경 변수(API 키)가 설정되지 않았습니다."}

    # ✅ HMAC 서명 생성
    timestamp = str(round(time.time() * 1000))
    signature = base64.b64encode(
        hmac.new(
            secret_key.encode('utf-8'),
            bytes(f"{timestamp}.{method}.{uri}", 'utf-8'),
            hashlib.sha256
        ).digest()
    )

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": api_key,
        "X-Customer": customer_id,
        "X-Signature": signature,
    }

    params = {
        "hintKeywords": req.keyword,
        "showDetail": 1
    }

    try:
        response = requests.get(API_BASE + uri, headers=headers, params=params, timeout=10)
        data = response.json()
    except Exception as e:
        return {"error": f"API 요청 실패: {str(e)}"}

    # ✅ 결과 반환 (네이버 응답 그대로 전달)
    return {"results": data.get("keywordList", data)}

# ✅ .well-known 폴더 정적 서빙
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/.well-known",
    StaticFiles(directory=os.path.join(BASE_DIR, ".well-known")),
    name="well-known"
)
