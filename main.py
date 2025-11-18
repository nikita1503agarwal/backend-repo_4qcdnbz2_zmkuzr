import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Facility, Report, EducationalArticle, PickupRequest, ContactMessage, Organization

app = FastAPI(title="Sampurna API", description="Waste management & sorting platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IdResponse(BaseModel):
    id: str


@app.get("/")
def root():
    return {"name": "Sampurna", "status": "ok", "message": "Sampurna API is running"}


@app.get("/test")
def test_database():
    """Test endpoint to check database connectivity"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "❌ Unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Public content endpoints
@app.get("/api/articles", response_model=List[EducationalArticle])
def list_articles(limit: int = 20):
    docs = get_documents("educationalarticle", {}, limit)
    # Map _id to string and ensure fields present
    result: List[EducationalArticle] = []
    for d in docs:
        d.pop("_id", None)
        result.append(EducationalArticle(**d))
    return result


@app.get("/api/facilities", response_model=List[Facility])
def list_facilities(limit: int = 100):
    docs = get_documents("facility", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return [Facility(**d) for d in docs]


# Submission endpoints
@app.post("/api/pickups", response_model=IdResponse)
def create_pickup(req: PickupRequest):
    inserted_id = create_document("pickuprequest", req)
    return {"id": inserted_id}


@app.post("/api/contact", response_model=IdResponse)
def submit_contact(msg: ContactMessage):
    inserted_id = create_document("contactmessage", msg)
    return {"id": inserted_id}


@app.post("/api/partners", response_model=IdResponse)
def submit_partner(org: Organization):
    inserted_id = create_document("organization", org)
    return {"id": inserted_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
