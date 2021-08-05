import json
from enum import Enum
from typing import Any, Dict, NewType, Optional, Tuple

from fastapi.params import Query
from sqlalchemy.orm.query import Query as SQLQuery


class SortOrders(str, Enum):
    ASC = "asc"
    DESC = "desc"


def parse_pagination(
    page: Optional[int] = 1, num_results_per_page: Optional[int] = Query(50, lt=100)
) -> Tuple[int, int]:
    offset = (page - 1) * num_results_per_page

    return offset, num_results_per_page


def parse_filters(filters: Optional[str] = Query(None, max_length=100)) -> Dict[str, str]:
    return json.loads(filters)


def parse_sorting(
    sort_by: Optional[str] = Query(None, max_length=100),
    sort_order: Optional[NewType('SortOrders', SortOrders)] = SortOrders.ASC
) -> Tuple[str, SortOrders]:
    return sort_by, sort_order


def process_filters(
    sqlalchemy_query: SQLQuery, model: Any, filters: Dict[str, str]
) -> SQLQuery:
    for key, value in filters.items():
        sqlalchemy_query = sqlalchemy_query.filter(getattr(model, key) == value)

    return sqlalchemy_query


def process_sorting(
    sqlalchemy_query: SQLQuery, model: Any, sort_by: str, sort_order: SortOrders
) -> SQLQuery:
    sort_attr = getattr(model, sort_by)

    if sort_order == SortOrders.ASC:
        sqlalchemy_query = sqlalchemy_query.order_by(sort_attr)
    else:
        sqlalchemy_query = sqlalchemy_query.order_by(sort_attr.desc())

    return sqlalchemy_query
