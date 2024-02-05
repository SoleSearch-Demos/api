from typing import Annotated

from fastapi import APIRouter, Query

from src.data.instance import DEFAULT_LIMIT, DEFAULT_OFFSET
from src.data.models import Audience, SortKey, SortOrder
from src.data.queries import find_sneaker_by_id, find_sneakers

router = APIRouter(
    prefix="/sneakers",
)


@router.get("/")
async def get_sneakers(
    brand: str | None = None,
    sku: str | None = None,
    name: str | None = None,
    colorway: str | None = None,
    audience: Audience | None = None,
    releaseDate: str | None = None,
    released: bool | None = None,
    sort: SortKey = SortKey.RELEASE_DATE,
    sortOrder: SortOrder = SortOrder.DESCENDING,
    offset: Annotated[int, Query(gte=DEFAULT_OFFSET)] = DEFAULT_OFFSET,
    limit: Annotated[int, Query(gte=1, lte=100)] = DEFAULT_LIMIT,
):
    return await find_sneakers(
        brand=brand,
        sku=sku,
        name=name,
        colorway=colorway,
        audience=audience,
        release_date=releaseDate,
        released=released,
        sort_by=sort,
        sort_order=sortOrder,
        offset=offset,
        limit=limit,
    )


@router.get("/{product_id}")
async def get_sneaker_by_id(product_id: str):
    return await find_sneaker_by_id(product_id)


@router.get("/{product_id}/prices")
async def get_sneaker_pricing(product_id: str):
    return {"Error": "Not implemented yet"}


@router.get("/{product_id}/prices/{size}")
async def get_sneaker_size_pricing(product_id: str, size: str):
    return {"Error": "Not implemented yet"}