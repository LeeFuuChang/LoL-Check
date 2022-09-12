import os

name = "main.py"
key = "helloworldishard"
ico_path = "images\\128.ico"
upx_path = "upx-3.96-win64"
packages_path = "enc\\Lib\\site-packages"
result = "LoL-Check"

os.chdir(os.path.dirname(os.path.realpath(__file__)))

os.system("python .\convert.py")

commands = [
    "pyinstaller",
    f".\\{name}",
    f"--name {result}",
    f"--paths .\\{packages_path}",
    f"--upx-dir .\\{upx_path}",
    f"--i .\\{ico_path}",
    f"--key {key}",
    "--onefile",
    "--noconsole",
    "main.spec"
]
command = " ".join(commands)
print(command)
os.system(command)
