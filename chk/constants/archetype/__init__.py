"""
ArchetypeConfigModules lists all archetypes by version string
@deprecate
"""
from typing import Dict


class ArchetypeConfigModules:
    data: Dict = {
        "default:http:0.7.2": "chk.archetypes.defaults.http_config.HttpV072",
    }
