from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from utils.http_client import AsyncClient

class FilterValue(BaseModel):
    """Represents a single filter option with its count.

    Attributes:
        name: The display name of the filter value
        count: Number of items matching this filter value
        id: Optional unique identifier for the filter value
    """
    name: str
    count: int
    id: Optional[str] = None

class FilterGroup(BaseModel):
    """A group of related filter values with total count.

    Attributes:
        total: Total number of items in this filter group
        values: List of individual filter values and their counts
    """
    total: int
    values: List[FilterValue]

class AvailableFilters(BaseModel):
    """Contains all available filter options for inventory search.

    Attributes:
        total_items: Total number of items matching the current filters
        merchants: Filter group for available merchants
        vendors: Filter group for available vendors
        departments: Filter group for available departments
        product_groups: Filter group for available product groups
        product_types: Filter group for available product types
    """
    total_items: int = Field(alias="totalItems")
    merchants: FilterGroup
    vendors: FilterGroup
    departments: FilterGroup
    product_groups: FilterGroup = Field(alias="productGroups")
    product_types: FilterGroup = Field(alias="productTypes")

class InventoryItem(BaseModel):
    """Represents a single inventory item with its details.

    Attributes:
        merchant_id: Unique identifier of the merchant
        variant_id: Unique identifier of the product variant
        product_name: Name of the product
        quantity: Available quantity in stock
        supplier_model_number: Optional supplier's model number
        ean: Optional list of EAN codes
        size: Optional size information
        price: Optional price information
        product_description: Optional product description
        vendor: Optional vendor name
        product_type: Optional list of product types
        product_group: Optional list of product groups
        department: Optional list of departments
        image_url: Optional URL to product image
        created: Optional creation timestamp
        updated: Optional last update timestamp
    """
    merchant_id: str = Field(alias="merchantId")
    variant_id: str = Field(alias="variantId")
    product_name: str = Field(alias="productName")
    quantity: int
    supplier_model_number: Optional[str] = Field(None, alias="supplierModelNumber")
    ean: Optional[List[str]] = None
    size: Optional[str] = None
    price: Optional[str] = None
    product_description: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[List[str]] = Field(None, alias="productType")
    product_group: Optional[List[str]] = Field(None, alias="productGroup")
    department: Optional[List[str]] = None
    image_url: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

class PaginatedInventoryResponse(BaseModel):
    """Response model for paginated inventory search results.

    Attributes:
        items: List of inventory items for the current page
        total_items: Total number of items matching the search criteria
        current_page: Current page number
        total_pages: Total number of available pages
    """
    items: List[InventoryItem]
    total_items: int = Field(alias="totalItems")
    current_page: int = Field(alias="currentPage")
    total_pages: int = Field(alias="totalPages")

class FootwayClient:
    """Client for interacting with the Footway API.

    Provides methods to search inventory and retrieve available filters.

    Args:
        api_key: Authentication key for the Footway API
        base_url: Optional base URL for the API (defaults to production URL)
    """
    def __init__(self, api_key: str, base_url: str = "https://api.footwayplus.com"):
        self.base_url = base_url
        self.headers = {"X-API-KEY": api_key}
        self.client = AsyncClient(headers=self.headers)

    async def close(self):
        await self.client.aclose()

    def _build_array_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Convert array parameters to multi-format query parameters.
        
        Args:
            params: Dictionary of parameter names and their values

        Returns:
            Dictionary with array parameters formatted for the API
        """
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
        """Get available filter options for inventory search.
        
        Args:
            merchant_id: Optional list of merchant IDs to filter by
            vendor: Optional list of vendor names to filter by
            department: Optional list of departments to filter by
            product_group: Optional list of product groups to filter by
            product_type: Optional list of product types to filter by

        Returns:
            AvailableFilters object containing all available filter options

        Raises:
            HTTPError: If the API request fails
        """
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
        return AvailableFilters.model_validate(response.json())

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
        """Search inventory items with various filters.
        
        Args:
            merchant_id: Optional list of merchant IDs to filter by
            product_name: Optional product name to search for
            vendor: Optional list of vendor names to filter by
            department: Optional list of departments to filter by
            product_group: Optional list of product groups to filter by
            product_type: Optional list of product types to filter by
            variant_ids: Optional list of specific variant IDs to retrieve
            search_text: Optional general search text
            page: Page number for pagination (default: 1)
            page_size: Number of items per page (default: 20)
            sort_by: Optional field to sort results by
            sort_direction: Sort direction, either "asc" or "desc" (default: "asc")

        Returns:
            PaginatedInventoryResponse containing the search results

        Raises:
            HTTPError: If the API request fails
        """
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
        return PaginatedInventoryResponse.model_validate(response.json())
