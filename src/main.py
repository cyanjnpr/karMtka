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
from config import C_SKETCH_IMPLEMENTATION

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
    type=click.IntRange(0, 600))
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
@click.option("--overwrite", "is_overwrite_set", is_flag=True,
    help="confirm overwrite operation if such mode is selected")
@click.option("-g", "--image", "images", default=[], multiple=True,
    help="path to the image file to be injected into the page",
    type=click.Path(exists=True, dir_okay=False))
@click.option("-q", "--quality", "quality", default=3,
    help="quality of the injected images, default is '3'\n\n\
using values higher than the default may result in a huge file size",
    type=click.IntRange(2, 255))
def karmtka(text: Tuple[str], styles: Tuple[int], weights: Tuple[int], 
            uid: uuid.UUID, margin: int, device: str, output_to_file: bool, 
            output: str, is_xochitl: bool, inject_mode: str, 
            images: Tuple[str], quality: int, is_overwrite_set: bool):
    page = Page(uid, DeviceResolution[device], margin)

    if not sys.stdin.isatty():
        piped = sys.stdin.read()
        text = [piped, *text]

    page.build(text, styles, weights, images, quality)
    page._check()

    ar = rm_v6.KaitaiStream(io.BytesIO(bytearray(len(page.header) +
        sum(e.len for e in page.packets))))
    page._write(ar)
    # to_byte_array doesn't convert to byte array
    ar: bytearray = bytearray(ar.to_byte_array())
    if (C_SKETCH_IMPLEMENTATION): ar.extend(page.raw)

    if (is_xochitl):
        mode = InjectMode[inject_mode]
        if (not mode.is_overwrite_mode() or is_overwrite_set):
            inject(mode, ar)
        else:
            raise Exception("--overwrite flag is not set, but overwrite mode was selected")
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
