"""Tests for discussion context MCP tool."""

import pytest
from basic_memory.mcp.tools.discussion import get_discussion_context
from basic_memory.schemas.memory import GraphContext

@pytest.mark.asyncio
async def test_get_basic_discussion_context(client, test_graph):
    """Test getting basic discussion context."""
    context = await get_discussion_context(
        url="memory://test/root"
    )
    
    assert isinstance(context, GraphContext)
    assert len(context.primary_entities) == 1
    assert context.primary_entities[0].permalink == "test/root"
    assert len(context.related_entities) > 0
    
    # Verify metadata
    assert context.metadata["uri"] == "test/root"
    assert context.metadata["depth"] == 2  # default depth
    assert context.metadata["timeframe"] is not None
    assert isinstance(context.metadata["generated_at"], str)
    assert context.metadata["matched_entities"] == 1

@pytest.mark.asyncio
async def test_get_discussion_context_pattern(client, test_graph):
    """Test getting context with pattern matching."""
    context = await get_discussion_context(
        url="memory://test/*",
        depth=1
    )
    
    assert isinstance(context, GraphContext)
    assert len(context.primary_entities) > 1  # Should match multiple test/* paths
    assert all("test/" in e.permalink for e in context.primary_entities)
    assert context.metadata["depth"] == 1

@pytest.mark.asyncio
async def test_get_discussion_context_timeframe(client, test_graph):
    """Test timeframe parameter filtering."""
    # Get recent context
    recent_context = await get_discussion_context(
        url="memory://test/root",
        timeframe="1d"  # Last 24 hours
    )
    
    # Get older context
    older_context = await get_discussion_context(
        url="memory://test/root",
        timeframe="30d"  # Last 30 days
    )
    
    assert len(older_context.related_entities) >= len(recent_context.related_entities)

@pytest.mark.asyncio
async def test_get_discussion_context_not_found(client):
    """Test handling of non-existent URIs."""
    context = await get_discussion_context(
        url="memory://test/does-not-exist"
    )
    
    assert isinstance(context, GraphContext)
    assert len(context.primary_entities) == 0
    assert len(context.related_entities) == 0
    assert context.metadata["matched_entities"] == 0
