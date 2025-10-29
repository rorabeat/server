from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class KeywordRequest(BaseModel):
    keyword: str

class KeywordData(BaseModel):
    keyword: str
    search_volume_pc: int
    search_volume_mobile: int
    competition: str

@app.post("/doNaverKeywordResearch")
def research_keyword(req: KeywordRequest):
    # 실제 데이터는 네이버 검색광고 API 등에서 가져와야 함
    return {
        "results": [
            {
                "keyword": req.keyword,
                "search_volume_pc": 3000,
                "search_volume_mobile": 9000,
                "competition": "중"
            }
        ]
    }

# .well-known 디렉토리를 정적(static) 파일로 서빙
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
