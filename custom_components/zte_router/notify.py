import subprocess
import logging
from homeassistant.components.notify import BaseNotificationService

_LOGGER = logging.getLogger(__name__)

class ZTESMSNotificationService(BaseNotificationService):
    """Implementierung des SMS-Dienstes für den ZTE Router."""

    def __init__(self, host, password):
        self._host = host
        self._password = password

    def send_message(self, message="", **kwargs):
        targets = kwargs.get("target", [])
        if not targets:
            _LOGGER.error("Keine Zielrufnummer angegeben.")
            return

        for target in targets:
            subprocess.run([
                "python3",
                "/config/custom_components/zte_router/mc.py",
                self._host,
                self._password,
                "send_sms",
                target,
                message
            ])
