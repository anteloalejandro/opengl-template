cmake_minimum_required(VERSION 3.16)
project(glui_custom CXX)

# Collect source files from the actual GLUI directory
file(GLOB GLUI_SRCS "${CMAKE_SOURCE_DIR}/deps/glui/*.cpp")

add_library(glui_static STATIC ${GLUI_SRCS})

target_include_directories(glui_static PUBLIC
    "${CMAKE_SOURCE_DIR}/deps/glui/include"
    "${CMAKE_SOURCE_DIR}/deps/freeglut/include"
)

target_link_libraries(glui_static PRIVATE freeglut_static)

# Silcence warnings
target_compile_options(glui_static PRIVATE
    -Wno-unused-comparison
    -Wno-format
    -Wno-writable-strings
    -Wno-dangling-else
    -Wno-deprecated-declarations
)
