"""Manager for shipping and auto-registering the bundled Genius Lyrics card."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Any

from homeassistant.components.lovelace import DOMAIN as LOVELACE_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later

from .const import CARD_FILENAME, CARD_RESOURCE_DIR, DOMAIN, SERVICE_REGISTER_CARD_RESOURCES

_LOGGER = logging.getLogger(__name__)

# Bump to force Lovelace resource cache refresh after card changes.
CARD_VERSION = "1.0.0"
WWW_SOURCE_DIR = Path(__file__).parent / "www"


async def async_setup_cards(hass: HomeAssistant) -> bool:
    """Copy bundled card assets into Home Assistant's /config/www path."""
    source = WWW_SOURCE_DIR / CARD_FILENAME
    if not source.exists():
        _LOGGER.error("Bundled card file is missing: %s", source)
        return False

    www_dir = Path(hass.config.path("www"))
    target_dir = www_dir / CARD_RESOURCE_DIR
    target = target_dir / CARD_FILENAME

    try:
        await hass.async_add_executor_job(target_dir.mkdir, 0o755, True, True)
        await hass.async_add_executor_job(shutil.copy2, source, target)
    except OSError as err:
        _LOGGER.error("Failed to install Genius Lyrics card asset: %s", err)
        return False

    _LOGGER.debug("Installed bundled Genius Lyrics card to %s", target)
    return True


async def async_register_cards(hass: HomeAssistant) -> None:
    """Ensure the bundled Genius Lyrics card resource exists in Lovelace."""
    lovelace = hass.data.get(LOVELACE_DOMAIN)
    if not lovelace:
        _LOGGER.debug("Lovelace is not loaded yet; skipping card resource registration")
        return

    if not getattr(lovelace, "resources", None) or not lovelace.resources.loaded:
        _LOGGER.debug("Lovelace resources not ready; retrying card registration")
        async_call_later(
            hass, 5, lambda _: hass.create_task(async_register_cards(hass))
        )
        return

    resources = lovelace.resources
    base_url = f"/local/{CARD_RESOURCE_DIR}/{CARD_FILENAME}"
    full_url = f"{base_url}?v={CARD_VERSION}"

    found_resource: dict[str, Any] | None = None
    for resource in resources.async_items():
        if resource["url"].split("?")[0] == base_url:
            found_resource = resource
            break

    if found_resource:
        if found_resource["url"] != full_url:
            _LOGGER.info("Updating Lovelace resource to %s", full_url)
            await resources.async_update_item(
                found_resource["id"],
                {"res_type": "module", "url": full_url},
            )
        return

    _LOGGER.info("Registering Lovelace resource %s", full_url)
    await resources.async_create_item({"res_type": "module", "url": full_url})


async def async_register_resources_service(hass: HomeAssistant) -> None:
    """Register a service to manually re-register Lovelace resources."""
    if hass.services.has_service(DOMAIN, SERVICE_REGISTER_CARD_RESOURCES):
        return

    async def handle_register_resources(_call) -> None:
        await async_register_cards(hass)

    hass.services.async_register(
        DOMAIN,
        SERVICE_REGISTER_CARD_RESOURCES,
        handle_register_resources,
    )
