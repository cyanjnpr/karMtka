import json
import uuid
from enum import Enum
from .recent import retrieve_recent_list
from . import XOCHITL_PATH

class InjectMode(Enum):
    APPEND = 0
    CURRENT = 253
    LAST = 254
    NEXT = 255

    @staticmethod
    def choices():
        return [InjectMode.APPEND.name, InjectMode.CURRENT.name, 
            InjectMode.LAST.name, InjectMode.NEXT.name]
    
    def is_overwrite_mode(self) -> bool:
        return (self.value >> 7) > 0


class PageInfo:

    def __init__(self, id: str, idx: str, template_name = "Blank", deleted = False):
        self.id = id
        self.idx = idx
        self.template_name = template_name
        self.deleted = deleted
    
    def set_template(self, template_name: str):
        self.template_name = template_name

    def to_dict(self):
        return {
            "id": self.id,
            "idx": {
                "timestamp": "1:2",
                "value": self.idx
            },
            "template": {
                "timestamp": "1:2",
                "value": self.template_name
            }
        }
    
    @staticmethod
    def from_dict(info):
        id = ""
        idx = "ba"
        template = "Blank"
        deleted = False
        if ("id" in info):
            id = info["id"]
        if ("idx" in info and "value" in info["idx"]):
            idx = info["idx"]["value"]
        if ("template" in info and "value" in info["template"]):
            template = info["template"]["value"]
        if ("deleted" in info and "value" in info["deleted"]):
            deleted = info["deleted"]["value"] > 0
        return PageInfo(id, idx, template, deleted)

def retrieve_content_info(document_id: str):
    with open("{}{}.content".format(XOCHITL_PATH, document_id), 'r') as f:
        content = json.load(f)
        return content
    
def is_content_valid(content):
    return ("pageCount" in content and
            content["pageCount"] > 0 and
            "cPages" in content and
            "pages" in content["cPages"] and
            "lastOpened" in content["cPages"] and 
            "value" in content["cPages"]["lastOpened"])
    
def find_newest_idx(content):
    idx = "b"
    for page in content["cPages"]["pages"]:
        if page["idx"]["value"] > idx:
            idx = page["idx"]["value"]
    return idx

def next_idx(idx: str):
    idx = idx.lower()
    for i in range(len(idx) - 1, -1, -1):
        if idx[i] < 'z':
            idx = idx[:i] + chr(ord(idx[i]) + 1) + ('a' * (len(idx) - i - 1))
            return idx
    return idx + 'a'

def inject_content_info(document_id: str, content):
    with open("{}{}.content".format(XOCHITL_PATH, document_id), 'w') as f:
        json.dump(content, f, indent=4)

def inject_lines(document_id: str, uid: str, page: bytearray):
    with open("{}{}/{}.rm".format(XOCHITL_PATH, document_id, uid), 'wb') as f:
        f.write(page)

def inject_page(document_id: str, page: bytearray):
    content = retrieve_content_info(document_id)
    if (not is_content_valid(content)): return
    idx = next_idx(find_newest_idx(content))
    page_info = PageInfo(str(uuid.uuid4()), idx)
    content["pageCount"] = content["pageCount"] + 1
    content["cPages"]["pages"].append(page_info.to_dict())
    inject_lines(document_id, page_info.id, page)
    inject_content_info(document_id, content)

def inject(mode: InjectMode, page: bytearray):
    recent = retrieve_recent_list()
    if (len(recent) == 0): return
    if (mode == InjectMode.APPEND):
        inject_page(recent[0].id, page)
    elif (mode == InjectMode.CURRENT):
        content = retrieve_content_info(recent[0].id)
        if (not is_content_valid(content)): return
        inject_lines(recent[0].id, content["cPages"]["lastOpened"]["value"], page)
    elif (mode == InjectMode.NEXT):
        content = retrieve_content_info(recent[0].id)
        if (not is_content_valid(content)): return
        next = False
        pages = sorted(content["cPages"]["pages"], key=lambda p: PageInfo.from_dict(p).idx)
        for page_info in pages:
            info = PageInfo.from_dict(page_info)
            if (next and not info.deleted):
                inject_lines(recent[0].id, info.id, page)
                break
            if (info.id == content["cPages"]["lastOpened"]["value"]):
                next = True
    elif (mode == InjectMode.LAST):
        content = retrieve_content_info(recent[0].id)
        if (not is_content_valid(content)): return
        pages = sorted(content["cPages"]["pages"], key=lambda p: PageInfo.from_dict(p).idx, reverse=True)
        for page_info in pages:
            info = PageInfo.from_dict(page_info)
            if (not info.deleted):
                inject_lines(recent[0].id, info.id, page)
                break
