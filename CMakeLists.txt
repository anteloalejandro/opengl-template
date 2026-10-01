cmake_minimum_required(VERSION 3.16)
set(PROJECT_NAME main)
# project(<project_name> <language>)
project(${PROJECT_NAME} C CXX)

# Determine whether to use main.cpp or main.c
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp")
    set(MAIN_SRC src/main.cpp)
elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/main.c")
    set(MAIN_SRC src/main.c)
else()
    message(FATAL_ERROR "Neither src/main.cpp nor src/main.c was found!")
endif()

# Pass the resolved source file to your target
add_executable(${PROJECT_NAME}
    ${MAIN_SRC}
)

# Create a `compile_commands.json` the LSP can read
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# Link it from the build directory of the target to build/ directly
if(CMAKE_EXPORT_COMPILE_COMMANDS)
  file(CREATE_LINK
    "${CMAKE_BINARY_DIR}/compile_commands.json"
    "${CMAKE_SOURCE_DIR}/build/compile_commands.json"
    SYMBOLIC
  )
endif()

# Set TARGET_PLATFORM variable
set(TARGET_PLATFORM "${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}")
# Set output directory to lib/TARGET_PLATFORM.
set(PREBUILT_LIB_DIR "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")
set(CMAKE "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")

# ====== FREEGLUT CONFIG ======

# Modify FREEGLUT CMake flags
set(FREEGLUT_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(FREEGLUT_BUILD_DEMOS OFF CACHE BOOL "" FORCE)

add_subdirectory(deps/freeglut)

# Overwrite FREEGLUT output directory and name
if(TARGET freeglut_static)
    set_target_properties(freeglut_static PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${PREBUILT_LIB_DIR}"
        OUTPUT_NAME "freeglut"
    )
endif()

# ====== GLEW CONFIG ======

add_subdirectory(
    #  ↓ Root directory containing CMakeLists (or whatever -S is set to)
    "${CMAKE_SOURCE_DIR}/deps/glew/build/cmake"
    #  ↓ CWD (or whatever -B is set to)
    "${CMAKE_BINARY_DIR}/deps/glew"
)
if(TARGET glew_s)
    set_target_properties(glew_s PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${PREBUILT_LIB_DIR}"
        OUTPUT_NAME "glew"
    )
endif()

# ====== FreeImage CONFIG ======

if(MINGW OR WIN32)
    # El linker lld para MinGW no encuentra pthread si no se le añade
    add_link_options("LINKER:-lpthread")
    target_link_options(${PROJECT_NAME} PRIVATE -static)
endif()

set(FREEIMAGE_STATIC ON CACHE BOOL "" FORCE)

add_subdirectory(deps/freeimage)


if(TARGET FreeImage)
    set_target_properties(FreeImage PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${PREBUILT_LIB_DIR}"
        OUTPUT_NAME "freeimage"
    )
endif()

# ====== GLUI CONFIG ======

add_subdirectory(
    # Custom CMakeLists.txt instead of deps/glui/CMakeLists.txt
    "${CMAKE_SOURCE_DIR}/cmake/glui"
    "${CMAKE_BINARY_DIR}/deps/glui"
)

if(TARGET glui_static)
    set_target_properties(glui_static PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${PREBUILT_LIB_DIR}"
        OUTPUT_NAME "glui"
    )
endif()

# ====== TARGET DEF ======

# Equivalent of -I in clang/gcc
target_include_directories(${PROJECT_NAME} PRIVATE
    deps/freeglut/include
    deps/glew/include
    deps/glui/include
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    pthread
    # got the name from add_library inside freeglut/CMakeLists.txt
    freeglut_static
    # got the name from the GLEW documentation
    glew_s
    # from freeimage's README
    FreeImage
    # from glui's add_library
    glui_static
)

# Set output directory for the final executable
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${TARGET_PLATFORM}"
)
