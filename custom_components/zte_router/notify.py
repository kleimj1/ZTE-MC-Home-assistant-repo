import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.notify import PLATFORM_SCHEMA, BaseNotificationService
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .mc import send_sms

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required("host"): cv.string,
    vol.Required("password"): cv.string,
})

async def async_get_service(hass: HomeAssistant, config, discovery_info=None):
    """Holt den SMS-Notify-Dienst."""
    return ZTESMSNotificationService(config["router_ip"], config["router_password"])

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Richtet den SMS-Notify-Dienst ein."""
    hass.services.async_register(
        "notify", "zte_sms", ZTESMSNotificationService(entry.data["host"], entry.data["password"])
    )
    return True

class ZTESMSNotificationService(BaseNotificationService):
    """Implementierung des SMS-Benachrichtigungsdienstes für den ZTE Router."""

    def __init__(self, host, password):
        """Initialisiert den Dienst."""
        self._host = host
        self._password = password

    def send_message(self, message="", **kwargs):
        """Sendet eine SMS über den Router."""
        targets = kwargs.get("target", [])
        if not targets:
            _LOGGER.error("Keine Zielrufnummer angegeben.")
            return

        for target in targets:
            send_sms(self._host, self._password, target, message)
            _LOGGER.info(f"SMS an {target} gesendet: {message}")
