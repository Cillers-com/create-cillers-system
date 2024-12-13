from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..utils.http_client import AsyncClient

@dataclass
class FilterValue:
    name: str
    count: int
    id: Optional[str] = None

@dataclass
class FilterGroup:
    total: int
    values: List[FilterValue]

@dataclass
class AvailableFilters:
    total_items: int
    merchants: FilterGroup
    vendors: FilterGroup
    departments: FilterGroup
    product_groups: FilterGroup
    product_types: FilterGroup

@dataclass
class InventoryItem:
    merchant_id: str
    variant_id: str
    product_name: str
    quantity: int
    supplier_model_number: Optional[str] = None
    ean: Optional[List[str]] = None
    size: Optional[str] = None
    price: Optional[str] = None
    product_description: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[List[str]] = None
    product_group: Optional[List[str]] = None
    department: Optional[List[str]] = None
    image_url: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

@dataclass
class PaginatedInventoryResponse:
    items: List[InventoryItem]
    total_items: int
    current_page: int
    total_pages: int

class FootwayClient:
    def __init__(self, api_key: str, base_url: str = "https://api.footwayplus.com"):
        self.base_url = base_url
        self.headers = {"X-API-KEY": api_key}
        self.client = AsyncClient(headers=self.headers)

    async def close(self):
        await self.client.aclose()

    def _build_array_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert array parameters to multi-format query parameters."""
        result = {}
        for key, value in params.items():
            if isinstance(value, list):
                for i, item in enumerate(value):
                    result[f"{key}"] = item
            elif value is not None:
                result[key] = value
        return result

    async def get_available_filters(
        self,
        merchant_id: Optional[List[str]] = None,
        vendor: Optional[List[str]] = None,
        department: Optional[List[str]] = None,
        product_group: Optional[List[str]] = None,
        product_type: Optional[List[str]] = None,
    ) -> AvailableFilters:
        """Get available filter options for inventory search."""
        params = self._build_array_params({
            "merchantId": merchant_id,
            "vendor": vendor,
            "department": department,
            "productGroup": product_group,
            "productType": product_type,
        })

        response = await self.client.get(
            f"{self.base_url}/v1/inventory/availableFilters",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        return AvailableFilters(
            total_items=data["totalItems"],
            merchants=FilterGroup(**data["merchants"]),
            vendors=FilterGroup(**data["vendors"]),
            departments=FilterGroup(**data["departments"]),
            product_groups=FilterGroup(**data["productGroups"]),
            product_types=FilterGroup(**data["productTypes"])
        )

    async def search_inventory(
        self,
        merchant_id: Optional[List[str]] = None,
        product_name: Optional[str] = None,
        vendor: Optional[List[str]] = None,
        department: Optional[List[str]] = None,
        product_group: Optional[List[str]] = None,
        product_type: Optional[List[str]] = None,
        variant_ids: Optional[List[str]] = None,
        search_text: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: Optional[str] = None,
        sort_direction: str = "asc",
    ) -> PaginatedInventoryResponse:
        """Search inventory items with various filters."""
        params = self._build_array_params({
            "merchantId": merchant_id,
            "productName": product_name,
            "vendor": vendor,
            "department": department,
            "productGroup": product_group,
            "productType": product_type,
            "variantIds": variant_ids,
            "searchText": search_text,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortDirection": sort_direction,
        })

        response = await self.client.get(
            f"{self.base_url}/v1/inventory/search",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        items = [InventoryItem(
            merchant_id=item["merchantId"],
            variant_id=item["variantId"],
            product_name=item["productName"],
            quantity=item["quantity"],
            supplier_model_number=item.get("supplierModelNumber"),
            ean=item.get("ean"),
            size=item.get("size"),
            price=item.get("price"),
            product_description=item.get("product_description"),
            vendor=item.get("vendor"),
            product_type=item.get("productType"),
            product_group=item.get("productGroup"),
            department=item.get("department"),
            image_url=item.get("image_url"),
            created=datetime.fromisoformat(item["created"]) if item.get("created") else None,
            updated=datetime.fromisoformat(item["updated"]) if item.get("updated") else None,
        ) for item in data["items"]]

        return PaginatedInventoryResponse(
            items=items,
            total_items=data["totalItems"],
            current_page=data["currentPage"],
            total_pages=data["totalPages"]
        )
