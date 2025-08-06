import json
import uuid
from enum import Enum
from . import XOCHITL_PATH

class InjectMode(Enum):
    RECENT = 0
    CURRENT = 1

class PageInfo:

    def __init__(self, id: str, idx: str):
        self.id = id
        self.idx = idx
        self.template_name = "Blank"
    
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

def retrieve_content_info(document_id: str):
    with open("{}{}.content".format(XOCHITL_PATH, document_id), 'r') as f:
        content = json.load(f)
        if content["cPages"] == None:
            content["cPages"] = {}
        if content["cPages"]["pages"] == None:
            content["cPages"]["pages"] = []
        return content
    
def find_newest_idx(content):
    idx = "a"
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
    idx = next_idx(find_newest_idx(content))
    page_info = PageInfo(str(uuid.uuid4()), idx)
    content["pageCount"] = content["pageCount"] + 1 if content["pageCount"] != None else 1
    content["cPages"]["pages"].append(page_info.to_dict())
    inject_lines(document_id, page_info.id, page)
    inject_content_info(document_id, content)