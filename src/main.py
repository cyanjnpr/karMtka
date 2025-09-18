from packet import *
from page import *
import uuid
from typing import Tuple
import sys
import click
from xochitl.xochitl import inject, InjectMode, list_notebooks
from sketch import ImageConversion
import pathlib

VERSION = "v0.2.4"

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
current - inject new content (overwrite) into last closed page\n\n\
next - inject new content (overwrite) into page next to the 'current' one\n\n\
last - inject new content (overwrite) into last page in last closed notebook",
    type=click.Choice(InjectMode.choices(), case_sensitive=False))
@click.option("-f", "--overwrite", "is_overwrite_set", is_flag=True,
    help="confirm overwrite operation if such mode is selected")
@click.option("-g", "--image", "images", default=[], multiple=True,
    help="path to the image file to be injected into the page",
    type=click.Path(exists=True, dir_okay=False))
@click.option("-G", "--conversion-method", "conversion_method", default=[ImageConversion.NAIVE.name], multiple=True,
    help="conversion method for the provided image, default is 'naive'\n\n\
naive - convert line by line, placing new point whenever color changes\n\n\
cutoff - same as naive, but always assume two shades and use -q as cutoff threshold\n\n\
potrace - trace outlines with potrace",
    type=click.Choice(ImageConversion.choices(), case_sensitive=False))
@click.option("-q", "--quality", "--threshold", "quality", default=[3], multiple=True,
    help="quality/threshold parameter for the injected images, default is '3'\n\n\
naive conversion - using values higher than the default may result in a huge file size",
    type=click.IntRange(2, 255))
@click.option("--dry", "is_dry_run", is_flag=True, 
    help="prints which notebook and page would be modified on a normal run if used with -x")
@click.option("-n", "--notebook", "notebook", default="",
    help="set alternative notebook as injection target instead of the most recent one. \
This has to be a full path to the notebook, for example:\n\n\
Notebook named 'notes' in directory 'projects' should be specified as 'projects/notes'")
@click.option("-l", "--list", "is_list_mode", is_flag=True, help="do not generate anything, list the most recent notebooks, must be used with -x")
@click.option("-v", "--version", "print_version", is_flag=True, help="print version of this tool")
def karmtka(text: Tuple[str], styles: Tuple[int], weights: Tuple[int], 
            uid: uuid.UUID, margin: int, device: str, output_to_file: bool, 
            output: str, is_xochitl: bool, inject_mode: str, 
            images: Tuple[str], quality: Tuple[int], is_overwrite_set: bool, 
            print_version: bool, is_dry_run: bool, notebook: str,
            is_list_mode: bool, conversion_method: Tuple[str]):
    if (print_version): return print("karMtka {}".format(VERSION))
    if (is_dry_run and not is_xochitl): return print("dry run can be only used with -x option", file=sys.stderr)
    if (is_list_mode and not is_xochitl): return print("list mode can be only used with -x option", file=sys.stderr)
    if (is_dry_run and is_list_mode): return print("conflicting options: --dry and --list", file=sys.stderr)

    page = Page(uid, DeviceResolution[device], margin)
    if not sys.stdin.isatty():
        piped = sys.stdin.read()
        text = [piped, *text]

    ar: bytearray = bytearray()
    if (not is_list_mode and not is_dry_run):
        page.build(text, styles, weights, images, quality, conversion_method)
        ar = page.serialize()

    if (is_xochitl):
        # option for editing the upper bound?
        if (is_list_mode): return list_notebooks(25)
        mode = InjectMode[inject_mode]
        if (not mode.is_overwrite_mode() or is_overwrite_set):
            inject(notebook, mode, is_dry_run, ar)
        else:
            return print("--overwrite flag is not set, but overwrite mode was selected", file=sys.stderr)
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
