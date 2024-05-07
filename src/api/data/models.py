from enum import Enum
from typing import List, Optional

from beanie import Document
from core.models.shoes import SneakerView
from fastapi_users_db_beanie import BeanieBaseUser
from fastapi_users_db_beanie.access_token import BeanieBaseAccessToken
from pydantic import BaseModel


class User(BeanieBaseUser, Document):
    favorites: List[str] = []
    size: Optional[int] = None


class AccessToken(BeanieBaseAccessToken, Document):
    pass


class PaginatedSneakersResponse(BaseModel):
    total: int
    page: int
    pageSize: int
    nextPage: str | None
    previousPage: str | None
    items: List[SneakerView]


class SortKey(str, Enum):
    BRAND = "brand"
    SKU = "sku"
    NAME = "name"
    COLORWAY = "colorway"
    AUDIENCE = "audience"
    RELEASE_DATE = "releaseDate"
    PRICE = "price"


class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
