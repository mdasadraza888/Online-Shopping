from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class ProductVariantRequest(BaseModel):
    product_id: int
    size: str
    color: str
    sku: str
    stock: int = Field(ge=0)

class ProductVariantUpdate(BaseModel):
    size: str | None = None
    color: str | None = None
    sku: str | None = None
    stock: int | None = Field(default=None, ge=0)

class ProductVariantResponse(BaseModel):
    id: int
    product_id: int
    size: str
    color: str
    stock: int

    model_config = ConfigDict(from_attributes=True)

class ProductRequest(BaseModel):
    name: str
    slug: str
    description: str
    price: Decimal = Field(gt=0)
    category_id: int

class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    category_id: int | None = None
    
class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: Decimal
    category_id: int

    model_config = ConfigDict(from_attributes=True)