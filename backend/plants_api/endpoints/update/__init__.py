"""
Data update endpoints are defined here.
"""
import importlib
from pathlib import Path

for file in sorted(Path(__file__).resolve().parent.iterdir()):
    if file.name.endswith(".py") and file.name not in ("__init__.py", "router.py"):
        importlib.import_module(f".{file.name[:-3]}", __package__)

from .router import update_router  # pylint: disable=wrong-import-position

__all__ = [
    "update_router",
]
