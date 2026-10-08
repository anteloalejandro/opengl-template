import os
from argparse import ArgumentParser
from shutil import rmtree

parser = ArgumentParser()
parser.add_argument(
    "--ninja", action="store_true",
    help="Set it if you want to use ninja as the build system. Only needs to be done once."
)
parser.add_argument(
    "-f", "--force", action="store_true",
    help="Remove build directory before generating the build scripts."
)
parser.add_argument(
    "-r", "--release", action="store_true",
    help="Generate build scripts in Release mode"
)
args = parser.parse_args()

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
