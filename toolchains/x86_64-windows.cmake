set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

# Specify the Resource Compiler for .rc files
set(CMAKE_RC_COMPILER llvm-windres)

set(CMAKE_C_FLAGS_INIT "--target=x86_64-w64-mingw32 -fuse-ld=lld")
set(CMAKE_CXX_FLAGS_INIT "--target=x86_64-w64-mingw32 -fuse-ld=lld")
