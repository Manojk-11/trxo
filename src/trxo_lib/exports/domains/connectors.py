"""
Connectors export export service.
"""

from typing import Any
from trxo_lib.config.api_endpoints import IDMEndpoints
from trxo_lib.config.api_headers import get_headers
from trxo_lib.exports.processor import BaseExporter


class ConnectorsExportService:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def execute(self) -> Any:
        exporter = BaseExporter()
        headers = get_headers("connectors")

        safe_kwargs = self.kwargs.copy()
        if "commit" in safe_kwargs:
            safe_kwargs["commit_message"] = safe_kwargs.pop("commit")

        return exporter.export_data(
            command_name="connectors",
            api_endpoint=IDMEndpoints.Config.LIST_CONNECTORS,
            headers=headers,
            **safe_kwargs,
        )
