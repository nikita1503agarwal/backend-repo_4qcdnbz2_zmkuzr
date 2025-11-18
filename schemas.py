"""
Database Schemas for Sampurna (Waste Management Platform)

Each Pydantic model corresponds to a MongoDB collection (collection name is the lowercase of the class name).
These schemas are used for request validation and IDE hints. Documents are stored using the helpers
in database.py which also attach created_at/updated_at.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date


class Facility(BaseModel):
    name: str = Field(..., description="Facility name")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    province: Optional[str] = Field(None, description="Province/State")
    postal_code: Optional[str] = Field(None, description="Postal/ZIP code")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
    accepted_waste_types: List[str] = Field(default_factory=list, description="Accepted waste categories")
    contact_phone: Optional[str] = Field(None, description="Facility phone number")
    contact_email: Optional[EmailStr] = Field(None, description="Facility email")


class Report(BaseModel):
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    waste_diverted_tons: float = Field(..., ge=0, description="Total waste diverted in tons")
    recycling_rate: float = Field(..., ge=0, le=100, description="Recycling rate in percent")
    emissions_avoided_tons_co2e: float = Field(..., ge=0, description="Estimated CO2e avoided in tons")


class EducationalArticle(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    tags: List[str] = Field(default_factory=list)
    cover_image_url: Optional[str] = None


class PickupRequest(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: str
    city: Optional[str] = None
    waste_type: str = Field(..., description="e.g., recyclable, organic, e-waste, bulky")
    preferred_date: Optional[date] = None
    notes: Optional[str] = None


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class Organization(BaseModel):
    name: str
    website: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
