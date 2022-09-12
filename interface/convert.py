import base64
import os

image_n = [
    "Search",
    "Settings",
    "Order",
    "Chaos",
    "Top",
    "Jungle",
    "Mid", 
    "Bottom",
    "Support",
    "next",
    "prev",
    "Tutorial",
    "AutoPath",
    "Icon"
]

def pic2str(file, functionName, fn):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open(fn, 'w') as f:
        f.write(content)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("images/__init__.py", "w") as f:
    for imagename in image_n:
        pic2str(f'images/{imagename}.png', f'{imagename}_byte', f'images/{imagename}.py')
        f.write(f"from .{imagename} import {imagename}_byte\n")


print("\n\nConvert Image Finished\n\n")