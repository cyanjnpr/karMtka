from kaitai import rm_v6
from packet import *
from page import *
import io
import uuid
from typing import Tuple
import sys
import click
import io
from xochitl.xochitl import inject, InjectMode
import pathlib

@click.command()
@click.option("-t", "--text", "text", default=[""], multiple=True,
    help="text content of the reMarkable page")
@click.option("-s", "--style", "styles", default=[1], multiple=True,
    help="text style of the content", type=click.IntRange(1, 7))
@click.option("-w", "--weight", "weights", default=[1], multiple=True,
    help="font weight of the content",
    type=click.IntRange(1,4))
@click.option("-u", "--uuid", "uid", default=uuid.uuid4(),
    help="UUID of the page",  type=click.UUID)
@click.option("-m", "--margin", "margin", default=234,
    help="margin of the text content",
    type=click.IntRange(0, 700))
@click.option("-d", "--device", "device", default=DeviceResolution.RM.name,
    help="target device for the generated page, default is 'rm'",
    type=click.Choice(DeviceResolution.choices(), case_sensitive=False))
@click.option("-O", "output_to_file", is_flag=True,
    help="save the page to a local file named after the uuid")
@click.option("-o", "--output", "output", 
    help="save the page to a local file",
    type=click.Path())
@click.option("-x", "--xochitl", "is_xochitl", is_flag=True,
    help="run in reMarkable mode (on the device)\n\n\
this mode will inject generated page into an existing notebook")
@click.option("-i", "--inject", "inject_mode", default=InjectMode.APPEND.name,
    help="inject mode for the xochitl option, default is 'append'\n\n\
append - inject new page into last closed notebook\n\n\
current - inject new (overwrite) content into last closed page\n\n\
next - inject new (overwrite) content into page next to the 'current' one\n\n\
last - inject new (overwrite) content into last page in last closed notebook",
    type=click.Choice(InjectMode.choices(), case_sensitive=False))
def karmtka(text: Tuple[str], styles: Tuple[int], weights: Tuple[int], 
        uid: uuid.UUID, margin: int, device: str, output_to_file: bool, output, 
        is_xochitl: bool, inject_mode: str):
    page = Page(uid, DeviceResolution[device], margin)

    if not sys.stdin.isatty():
        piped = sys.stdin.read()
        if len(text) == 1 and text[0] == "":
            text = [piped]
        else:
            text = [*text, piped]

    page.build(text, styles, weights)
    page._check()

    ar = rm_v6.KaitaiStream(io.BytesIO(bytearray(len(page.header) +
        sum(e.len for e in page.packets))))
    page._write(ar)
    ar = ar.to_byte_array()

    if (is_xochitl):
        inject(InjectMode[inject_mode], ar)
    else:
        if (output != None):
            path = pathlib.Path(output)
            if (path.exists() and path.is_dir()):
                output = "{}/{}.rm".format(output, uid)
            with open(output, 'wb') as f:
                f.write(ar)
        elif (output_to_file):
            with open("{}.rm".format(uid), 'wb') as f:
                f.write(ar)
        else:
            sys.stdout.buffer.write(ar)

if __name__ == "__main__":
    karmtka()
