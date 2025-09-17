import json
from typing import List, Dict, Tuple
import os
from dataclasses import dataclass
from . import XOCHITL_PATH
from enum import Enum

class ItemType(Enum):
    COLLECTION = "CollectionType"
    DOCUMENT = "DocumentType"

@dataclass
class RecentItem():
    id: str
    last_access: int
    last_page: int
    name: str
    parent: str

    def __init__(self, id, last_access, last_page, name, parent):
        self.id = id
        self.last_access = last_access
        self.last_page = last_page
        self.name = name
        self.parent = parent


@dataclass
class Collection():
    id: str
    name: str
    parent: str

    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent


def is_collection_valid(metadata: Dict) -> bool:
    return ("visibleName" in metadata and
            "type" in metadata and metadata["type"] == ItemType.COLLECTION.value and
            "parent" in metadata)

def is_metadata_valid(metadata: Dict) -> bool:
    return ("lastOpened" in metadata and 
            "lastOpenedPage" in metadata and
            "lastModified" in metadata and 
            "createdTime" in metadata and
            "visibleName" in metadata and
            "type" in metadata and metadata["type"] == ItemType.DOCUMENT.value and
            "parent" in metadata)

def resolve_names(documents: List[RecentItem], collections: Dict[str, Collection]):
    for item in documents:
        if (len(item.parent) > 0 and item.parent in collections):
            item.name = os.path.join(collections[item.parent].name, item.name)

def retrieve_metadata() -> Tuple[Dict[str, Collection], List[RecentItem]]:
    recent: List[RecentItem] = []
    collections: Dict[str, Collection] = {}
    files = os.listdir(XOCHITL_PATH)
    for file in files:
        parts = file.split(".")
        if parts[len(parts) - 1] == "metadata":
            with open("{}{}".format(XOCHITL_PATH, file), 'r') as f:
                metadata = json.load(f)
                if (is_collection_valid(metadata)):
                    name = metadata["visibleName"]
                    parent = metadata["parent"]
                    collections[parts[0]] = Collection(parts[0], name, parent)
                elif (is_metadata_valid(metadata)):
                    # lastOpened may be 0 right after creation
                    last_access = max(metadata["lastOpened"], metadata["lastModified"], metadata["createdTime"])
                    last_page = metadata["lastOpenedPage"]
                    name = metadata["visibleName"]
                    parent = metadata["parent"]
                    if (parent != 'trash'): recent.append(RecentItem(parts[0], last_access, last_page, name, parent))
    # resolve full paths
    for col in collections.values():
        parent = col.parent
        while (len(parent) > 0 and parent in collections):
            col.name = os.path.join(collections[parent].name, col.name)
            parent = collections[parent].parent
    resolve_names(recent, collections)
    recent = sorted(recent, key=lambda r: r.last_access, reverse=True)
    return collections, recent


def retrieve_collections() -> Dict[str, Collection]:
    collections, _ = retrieve_metadata()
    return collections

def retrieve_recent_list() -> List[RecentItem]:
    _, documents = retrieve_metadata()
    return documents
