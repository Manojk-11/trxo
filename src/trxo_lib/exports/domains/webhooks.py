"""
Webhooks export service.
"""

from typing import Any
from trxo_lib.config.api_endpoints import AMEndpoints
from trxo_lib.config.api_headers import get_headers
from trxo_lib.config.constants import DEFAULT_REALM
from trxo_lib.exports.processor import BaseExporter


class WebhooksExportService:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def execute(self) -> Any:
        realm = self.kwargs.get("realm", DEFAULT_REALM)
        exporter = BaseExporter()
        headers = get_headers("webhooks")

        safe_kwargs = self.kwargs.copy()
        if "commit" in safe_kwargs:
            safe_kwargs["commit_message"] = safe_kwargs.pop("commit")

        return exporter.export_data(
            command_name="webhooks",
            api_endpoint=AMEndpoints.Webhooks.list_all(realm),
            headers=headers,
            **safe_kwargs,
        )
