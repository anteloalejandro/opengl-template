from io import BytesIO
import os
from os import path
from shutil import rmtree
from typing import Callable, cast
import urllib.request as request
from http.client import HTTPResponse
from zipfile import ZipFile
from argparse import ArgumentParser

class DownloadError(Exception): pass
def get_zip(download_url: str):
    with cast(HTTPResponse, request.urlopen(download_url)) as response:
        if response.getcode() != 200: raise Exception()
        data = response.read()

    return ZipFile(BytesIO(data))

def download(name: str, version: str, download_url_fn: Callable[[str], str]):
    download_path = path.join("deps", name)
    if (path.exists(download_path)): return
    try:
        zip = get_zip(download_url_fn(version))
    except Exception:
        raise DownloadError(name, version)
    unzip_top_folder(zip, download_path)

def unzip_top_folder(zip: ZipFile, download_path):
    top_folder = zip.filelist[0].filename
    for member in zip.filelist[1:]:
        if member.filename.startswith(top_folder):
            member.filename = member.filename[len(top_folder):]
            zip.extract(member, download_path)

def deps(args):
    if args.force:
        try:
            rmtree(path.join(path.dirname(__file__), "deps"))
        except FileNotFoundError as e:
            pass

    GLUT_VERSION: str = args.glut_version
    GLEW_VERSION: str = args.glew_version
    FREEIMAGE_VERSION: str = args.freeimage_version
    GLUI_VERSION: str = args.glui_version

    try:
        print("Downloading GLUT... ", end = "", flush=True)
        download(
            "freeglut", GLUT_VERSION,
            lambda v: f"https://github.com/freeglut/freeglut/archive/refs/tags/v{v}.zip"
        )
        print("Done.")

        print("Downloading GLEW... ", end = "", flush=True)
        download(
            "glew", GLEW_VERSION,
            lambda v: f"https://github.com/nigels-com/glew/releases/download/glew-{v}/glew-{v}.zip"
        )
        print("Done.")

        print("Downloading FreeImage... ", end = "", flush=True)
        download(
            "freeimage", FREEIMAGE_VERSION,
            lambda v: f"https://github.com/danoli3/FreeImage/archive/refs/tags/{v}.zip"
        )
        print("Done.")

        print("Downloading GLUI... ", end = "", flush=True)
        download(
            "glui", GLUI_VERSION,
            lambda v: f"https://github.com/libglui/glui/archive/refs/tags/{v}.zip"
        )
        print("Done.")

    except DownloadError as e:
        lib, version = e.args
        print(f"ERROR: Could not download {lib}={version}")

def build_scripts(args):
    if args.force:
        try:
            rmtree(os.path.join(os.path.dirname(__file__), "build"))
        except FileNotFoundError as e:
            pass

    # cmake -B build/windows -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/x86_64-windows.cmake
    toolchains = os.listdir("toolchains")

    for toolchain in toolchains:
        target = toolchain[:toolchain.rfind(".")]
        print(f"======= BUILDING FOR: {target} =======")
        # print(f"cmake -B build/{target} -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/{toolchain}")
        os.system(f"cmake -B build/{target} -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/{toolchain} {'-DCMAKE_BUILD_TYPE=Release -DCMAKE_OPTIMIZE_DEPENDENCIES=1' if args.release else ''} {'-G Ninja' if args.ninja else ''}")
        print(f"======= DONE =========================", end = "\n\n")

    if args.release:
        print("RELEASE MODE: Optimizations are enabled.")
    print("You can now build the project with `cmake --build build/<target>`")
    print("\nExecutables will be named `bin/<target>/main")

def run(args):
    is_windows = args.target.lower().find("windows") != -1
    executable = f"main{'.exe' if is_windows else ''}"
    arch_target = f"{args.architecture}-{args.target.lower()}"
    target_arch = f"{args.target.capitalize()}-{args.architecture}"
    os.system(f"cmake --build build/{arch_target} && {'wine' if is_windows else ''} ./bin/{target_arch}/{executable}")

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

deps_parser = subparsers.add_parser("deps")
build_scripts_parser = subparsers.add_parser("build_scripts")
run_parser = subparsers.add_parser("run")

deps_parser.add_argument("--glut_version", default="3.8.0")
deps_parser.add_argument("--glew_version", default="2.3.1")
deps_parser.add_argument("--freeimage_version", default="3.19.18")
deps_parser.add_argument("--glui_version", default="2.37")
deps_parser.add_argument(
    "-f", "--force", action="store_true",
    help="Remove deps directory before downloading the dependencies."
)
deps_parser.set_defaults(func=deps)

build_scripts_parser.add_argument(
    "--ninja", action="store_true",
    help="Set it if you want to use ninja as the build system. Only needs to be done once."
)
build_scripts_parser.add_argument(
    "-f", "--force", action="store_true",
    help="Remove build directory before generating the build scripts."
)
build_scripts_parser.add_argument(
    "-r", "--release", action="store_true",
    help="Generate build scripts in Release mode"
)
build_scripts_parser.set_defaults(func=build_scripts)

run_parser.add_argument(
    "-t", "--target", default="linux",
)
run_parser.add_argument(
    "-a", "--architecture", default="x86_64"
)
run_parser.set_defaults(func=run)

args = parser.parse_args()

if "func" in args:
    args.func(args)
else:
    parser.print_help()
