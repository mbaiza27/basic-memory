"""Knowledge graph management tools for Basic Memory MCP server."""

from loguru import logger

from basic_memory.mcp.server import mcp
from basic_memory.mcp.tools.utils import call_get, call_post
from basic_memory.schemas.base import PathId
from basic_memory.schemas.request import (
    CreateEntityRequest,
    CreateRelationsRequest,
    AddObservationsRequest,
    GetEntitiesRequest,
)
from basic_memory.schemas.delete import (
    DeleteEntitiesRequest,
    DeleteObservationsRequest,
    DeleteRelationsRequest,
)
from basic_memory.schemas.response import EntityListResponse, EntityResponse, DeleteEntitiesResponse
from basic_memory.mcp.async_client import client


@mcp.tool(
    description="Create new entities in the knowledge graph with names, types, and observations",
)
async def create_entities(request: CreateEntityRequest) -> EntityListResponse:
    """Create new entities in the knowledge graph."""
    logger.info(f"Creating {len(request.entities)} entities")
    url = "/knowledge/entities"
    response = await call_post(client, url, json=request.model_dump())
    return EntityListResponse.model_validate(response.json())


@mcp.tool(
    description="Create typed relationships between existing entities",
)
async def create_relations(request: CreateRelationsRequest) -> EntityListResponse:
    """Create relations between existing entities."""
    logger.info(f"Creating {len(request.relations)} relations")
    url = "/knowledge/relations"
    response = await call_post(client, url, json=request.model_dump())
    return EntityListResponse.model_validate(response.json())


@mcp.tool(
    description="Get complete information about a specific entity including observations and relations",
)
async def get_entity(permalink: PathId) -> EntityResponse:
    """Get a specific entity info by its permalink.

    Args:
        permalink: Path identifier for the entity
    """
    url = f"/knowledge/entities/{permalink}"
    response = await call_get(client, url)
    return EntityResponse.model_validate(response.json())


@mcp.tool(
    description="Load multiple entities by their permalinks in a single request",
)
async def get_entities(request: GetEntitiesRequest) -> EntityListResponse:
    """Load multiple entities by their permalinks.

    Args:
        request: OpenNodesRequest containing list of permalinks to load

    Returns:
        EntityListResponse containing complete details for each requested entity
    """
    url = "/knowledge/entities"
    response = await call_get(
        client, url, params=[("permalink", permalink) for permalink in request.permalinks]
    )
    return EntityListResponse.model_validate(response.json())


@mcp.tool(
    description="Add categorized observations to an existing entity",
)
async def add_observations(request: AddObservationsRequest) -> EntityResponse:
    """Add observations to an existing entity."""
    logger.info(f"Adding {len(request.observations)} observations to {request.permalink}")
    url = "/knowledge/observations"
    response = await call_post(client,url, json=request.model_dump())
    return EntityResponse.model_validate(response.json())


@mcp.tool(
    description="Delete specific observations from an entity while preserving other content",
)
async def delete_observations(request: DeleteObservationsRequest) -> EntityResponse:
    """Delete specific observations from an entity."""
    url = "/knowledge/observations/delete"
    response = await call_post(client,url, json=request.model_dump())
    return EntityResponse.model_validate(response.json())


@mcp.tool(
    description="Delete relationships between entities while preserving the entities themselves",
)
async def delete_relations(request: DeleteRelationsRequest) -> EntityListResponse:
    """Delete relations between entities."""
    url = "/knowledge/relations/delete"
    response = await call_post(client,url, json=request.model_dump())
    return EntityListResponse.model_validate(response.json())


@mcp.tool(
    description="Permanently delete entities and all related content (observations and relations)",
)
async def delete_entities(request: DeleteEntitiesRequest) -> DeleteEntitiesResponse:
    """Delete entities from the knowledge graph."""
    url = "/knowledge/entities/delete"
    response = await call_post(client,url, json=request.model_dump())
    return DeleteEntitiesResponse.model_validate(response.json())
