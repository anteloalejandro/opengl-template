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
    os.system(f"cmake -B build/{target} -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/{toolchain} {'-G Ninja' if args.ninja else ''}")
    print(f"======= DONE =========================", end = "\n\n")

print("You can now build the project with `cmake --build build/<target>`")
print("\nExecutables will be named `bin/<target>/main")
