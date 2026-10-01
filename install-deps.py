from io import BytesIO
from os import path
from shutil import rmtree
from typing import cast
import urllib.request as request
from http.client import HTTPResponse
from zipfile import ZipFile
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--glut_version", default="3.8.0")
parser.add_argument("--glew_version", default="2.3.1")
parser.add_argument("--freeimage_version", default="3.19.18")
parser.add_argument("--glui_version", default="2.37")
parser.add_argument(
    "-f", "--force", action="store_true",
    help="Remove deps directory before downloading the dependencies."
)
args = parser.parse_args()

if args.force:
    try:
        rmtree(path.join(path.dirname(__file__), "deps"))
    except FileNotFoundError as e:
        pass

GLUT_VERSION: str = args.glut_version
GLEW_VERSION: str = args.glew_version
FREEIMAGE_VERSION: str = args.freeimage_version
GLUI_VERSION: str = args.glui_version

class DownloadError(Exception): pass

def get_zip(download_url: str, error: DownloadError):
    with cast(HTTPResponse, request.urlopen(download_url)) as response:
        if response.getcode() != 200: raise error
        data = response.read()

    return ZipFile(BytesIO(data))

def unzip_top_folder(zip: ZipFile, download_path):
    top_folder = zip.filelist[0].filename
    for member in zip.filelist[1:]:
        if member.filename.startswith(top_folder):
            member.filename = member.filename[len(top_folder):]
            zip.extract(member, download_path)

def download_glut():
    download_path = path.join("deps", "freeglut")
    if (path.exists(download_path)): return
    download_url = f"https://github.com/freeglut/freeglut/archive/refs/tags/v{GLUT_VERSION}.zip"
    zip = get_zip(download_url, DownloadError("freeglut", GLUT_VERSION))
    unzip_top_folder(zip, download_path)

def download_glew():
    download_path = path.join("deps", "glew")
    if (path.exists(download_path)): return
    download_url = f"https://github.com/nigels-com/glew/releases/download/glew-{GLEW_VERSION}/glew-{GLEW_VERSION}.zip"
    zip = get_zip(download_url, DownloadError("glew", GLEW_VERSION))
    unzip_top_folder(zip, download_path)

def download_glui():
    download_path = path.join("deps", "glui")
    if (path.exists(download_path)): return
    download_url = f"https://github.com/libglui/glui/archive/refs/tags/{GLUI_VERSION}.zip"
    zip = get_zip(download_url, DownloadError("glui", GLUT_VERSION))
    unzip_top_folder(zip, download_path)

def download_freeimage():
    download_path = path.join("deps", "freeimage")
    if (path.exists(download_path)): return
    # Usamos un fork de github
    download_url = f"https://github.com/danoli3/FreeImage/archive/refs/tags/{FREEIMAGE_VERSION}.zip"
    zip = get_zip(download_url, DownloadError("freeimage", FREEIMAGE_VERSION))
    unzip_top_folder(zip, download_path)

try:
    print("Downloading GLUT... ", end = "", flush=True)
    download_glut()
    print("Done.")

    print("Downloading GLEW... ", end = "", flush=True)
    download_glew()
    print("Done.")

    print("Downloading FreeImage... ", end = "", flush=True)
    download_freeimage()
    print("Done.")

    print("Downloading GLUI... ", end = "", flush=True)
    download_glui()
    print("Done.")

except DownloadError as e:
    lib, version = e.args
    print(f"ERROR: Could not download {lib}={version}")
