import os

# cmake -B build/windows -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/x86_64-windows.cmake
toolchains = os.listdir("toolchains")

for toolchain in toolchains:
    target = toolchain[:toolchain.rfind(".")]
    print(f"======= BUILDING FOR: {target} =======")
    # print(f"cmake -B build/{target} -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/{toolchain}")
    os.system(f"cmake -B build/{target} -S . -DCMAKE_TOOLCHAIN_FILE=toolchains/{toolchain}")
    print(f"======= DONE =========================", end = "\n\n")

print("You can now build the project with `cmake --build build/<target>`")
print("\nExecutables will be named `bin/<target>/main")
