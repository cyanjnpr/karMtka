import json
from typing import List
import os
from dataclasses import dataclass
from . import XOCHITL_PATH

@dataclass
class RecentItem():
    id: str
    last_access: int
    last_page: int

    def __init__(self, id, last_access, last_page):
        self.id = id
        self.last_access = last_access
        self.last_page = last_page


def retrieve_recent_list() -> List[RecentItem]:
    recent: List[RecentItem] = []
    files = os.listdir(XOCHITL_PATH)
    for file in files:
        parts = file.split(".")
        if parts[len(parts) - 1] == "metadata":
            with open("{}{}".format(XOCHITL_PATH, file), 'r') as f:
                metadata = json.load(f)
                if ("lastOpened" in metadata and "lastOpenedPage" in metadata):
                    last_access = metadata["lastOpened"] 
                    last_page = metadata["lastOpenedPage"]
                    recent.append(RecentItem(parts[0], last_access, last_page))
    recent = sorted(recent, key=lambda r: r.last_access, reverse=True)
    return recent
