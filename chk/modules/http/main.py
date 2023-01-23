"""
Main driver
"""
from typing import Any

from chk.infrastructure.contexts import app
from chk.infrastructure.work import handle_worker
from chk.infrastructure.file_loader import FileContext

from chk.modules.http.entities import HttpSpec
from chk.modules.http.presentation import present_result


def execute(file_ctx: FileContext) -> Any:
    """Execute command functionality"""

    http_spec = HttpSpec(file_ctx)
    try:
        response = handle_worker(http_spec)
        if app.config(file_ctx.filepath_hash, "dump"):
            app.print_fmt(response, present_result)

        return response
    except RuntimeError as err:
        return (
            print("\r\n---\r\n", str(err))
            if app.config(file_ctx.filepath_hash, "dump")
            else err
        )
