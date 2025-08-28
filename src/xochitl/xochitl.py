import json
import uuid
from enum import Enum
from typing import Dict, List
from .recent import retrieve_recent_list, RecentItem
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

    def __repr__(self):
        return self.idx

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


def is_content_valid(content: Dict):
    return ("pageCount" in content and
            content["pageCount"] > 0 and
            "cPages" in content and
            "pages" in content["cPages"] and
            "lastOpened" in content["cPages"] and 
            "value" in content["cPages"]["lastOpened"])

class Notebook():

    metadata: RecentItem
    pages: List[PageInfo]
    lastOpenedIndex: int
    raw_content: Dict

    def __init__(self, metadata: RecentItem):
        self.metadata = metadata
        self.pages = []
        with open("{}{}.content".format(XOCHITL_PATH, metadata.id), 'r') as f:
            self.raw_content = json.load(f)
            if (is_content_valid(self.raw_content)):
                self.retrieve_pages()

    def is_valid(self):
        return len(self.pages) > 0

    def retrieve_pages(self):
        for page in self.raw_content["cPages"]["pages"]:
            page_info = PageInfo.from_dict(page)
            if (not page_info.deleted): self.pages.append(page_info)
            if (self.raw_content["cPages"]["lastOpened"]["value"] == page_info.id):
                self.lastOpenedIndex = len(self.pages) - 1
        sorted(self.pages, key=lambda p: p.idx)

    def next_idx(self) -> str:
        idx = self.pages[-1].idx.lower()
        for i in range(len(idx) - 1, -1, -1):
            if idx[i] < 'z':
                idx = idx[:i] + chr(ord(idx[i]) + 1) + ('a' * (len(idx) - i - 1))
                return idx
        return idx + 'a'
    
    def new_page(self):
        self.raw_content["pageCount"] += 1
        self.pages.append(PageInfo(uuid.uuid4(), self.next_idx()))
        self.raw_content["cPages"]["pages"].append(self.pages[-1].to_dict())
    

def inject_content_info(document_id: str, content):
    with open("{}{}.content".format(XOCHITL_PATH, document_id), 'w') as f:
        json.dump(content, f, indent=4)

def inject_lines(document_id: str, uid: str, page: bytearray):
    with open("{}{}/{}.rm".format(XOCHITL_PATH, document_id, uid), 'wb') as f:
        f.write(page)
        
def inject_page(notebook: Notebook, page: bytearray):
    notebook.new_page()
    inject_lines(notebook.metadata.id, notebook.pages[-1].id, page)
    inject_content_info(notebook.metadata.id, notebook.raw_content)

def print_target_info(notebook: Notebook, mode: InjectMode):
    print("Notebook: {}".format(notebook.metadata.name))
    if (mode == InjectMode.APPEND):
        notebook.new_page()
        print("Page: {}".format(len(notebook.pages)))
    elif (mode == InjectMode.CURRENT):
        print("Page: {}".format(notebook.lastOpenedIndex + 1))
    elif (mode == InjectMode.NEXT):
        print("Page: {}".format(notebook.lastOpenedIndex + 2))
    elif (mode == InjectMode.LAST):
        print("Page: {}".format(len(notebook.pages)))
    print("Total: {}".format(len(notebook.pages)))

def notebook_with_name(recent: List[RecentItem], notebook_name: str) -> Notebook:
    if len(notebook_name) == 0: return Notebook(recent[0])
    for item in recent:
        if item.name == notebook_name: return Notebook(item)
    return None

def list_notebooks():
    recent = retrieve_recent_list()
    for item in recent:
        print(item.name)

def inject(notebook_name: str, mode: InjectMode, simulate: bool, page: bytearray):
    recent = retrieve_recent_list()
    if (len(recent) == 0): return
    notebook = notebook_with_name(recent, notebook_name)
    if (notebook == None or not notebook.is_valid()): return
    if (mode == InjectMode.APPEND):
        if (simulate): return print_target_info(notebook, mode)
        inject_page(notebook, page)
    elif (mode == InjectMode.CURRENT):
        if (simulate): return print_target_info(notebook, mode)
        inject_lines(notebook.metadata.id, notebook.pages[notebook.lastOpenedIndex].id, page)
    elif (mode == InjectMode.NEXT):
        if len(notebook.pages) - 1 == notebook.lastOpenedIndex: return
        if (simulate): return print_target_info(notebook, mode)
        inject_lines(notebook.metadata.id, notebook.pages[notebook.lastOpenedIndex+1].id, page)
    elif (mode == InjectMode.LAST):
        if (simulate): return print_target_info(notebook, mode)
        inject_lines(notebook.metadata.id, notebook.pages[-1].id, page)
