from datetime import UTC, datetime

from bson import ObjectId

from data.instance import ASCENDING, DESCENDING, config, sneakers
from data.models import Audience, SortKey, SortOrder


def find_sneaker_by_id(id: str = ""):
    if not id:
        raise ValueError("The supplied productId cannot be null")
    return sneakers.find_one({"_id": ObjectId(id)})


def find_sneaker_by_sku(sku: str = "", brand=None):
    if not sku:
        raise ValueError("The supplied SKU cannot be null")
    query = {"sku": sku}
    if brand:
        query["brand"] = brand
    return sneakers.find_one(query)


def find_sneakers(
    brand: str = None,
    sku: str = None,
    name: str = None,
    colorway: str = None,
    audience: Audience = None,
    release_date: str = None,
    released: bool = None,
    sort_by: SortKey = SortKey.RELEASE_DATE,
    sort_order: SortOrder = SortOrder.DESCENDING,
    offset: int = config.DEFAULT_OFFSET,
    limit: int = config.DEFAULT_LIMIT,
):
    query = {
        field: value
        for field, value in {
            "brand": brand,
            "sku": sku,
            "name": name,
            "colorway": colorway,
            "audience": audience,
        }.items()
        if value is not None
    }

    if released is not None:
        if released is True:
            query["releaseDate"]["$lte"] = datetime.now(UTC)
        else:
            query["releaseDate"]["$gt"] = datetime.now(UTC)
    elif release_date:
        if ":" in release_date:
            inequality_operator = release_date.split(":")[0]
            if inequality_operator in ["lt", "lte", "gt", "gte"]:
                query["releaseDate"][f"${inequality_operator}"] = datetime.strptime(
                    release_date.split(":")[1], "%Y-%m-%d"
                )
        else:
            query["releaseDate"] = datetime.strptime(release_date, "%Y-%m-%d")

    sneakers.find().sort(
        sort_by, ASCENDING if sort_order == SortOrder.ASCENDING else DESCENDING
    ).skip(offset).limit(limit)