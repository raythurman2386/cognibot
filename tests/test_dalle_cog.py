import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from cogs.dalle import DALLE  # Adjust the import path as needed


@pytest.fixture
def dalle_cog():
    bot_mock = MagicMock()
    return DALLE(bot_mock)


@pytest.mark.asyncio
async def test_img_generation_invalid_params(dalle_cog):
    dalle_cog.client.images.generate = AsyncMock()
    await dalle_cog._img_generation("test prompt", "invalid", "invalid", "invalid")

    # Check if default values are used for invalid params
    dalle_cog.client.images.generate.assert_called_once_with(
        model=dalle_cog.client.images.generate.call_args[1]["model"],
        prompt="test prompt",
        size="1024x1024",  # default for "standard"
        quality="standard",
        style="vivid",
        n=1,
    )


@pytest.mark.asyncio
async def test_deploy_gallery_success(dalle_cog):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201

        await dalle_cog._deploy_gallery()

        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_deploy_gallery_failure(dalle_cog):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500

        await dalle_cog._deploy_gallery()

        mock_post.assert_called_once()
