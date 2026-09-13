cmake_minimum_required(VERSION 3.16)
set(PROJECT_NAME main)
# project(<project_name> <language>)
project(${PROJECT_NAME} C)

add_executable(${PROJECT_NAME}
    src/main.c
)

# Set TARGET_PLATFORM variable
set(TARGET_PLATFORM "${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}")
# Set output directory to lib/TARGET_PLATFORM.
set(PREBUILT_LIB_DIR "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")
set(CMAKE "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")

# Equivalent of -I in clang/gcc
target_include_directories(${PROJECT_NAME} PRIVATE
    deps/freeglut/include
    deps/glew/include
)
target_link_libraries(${PROJECT_NAME} PRIVATE
    # got the name from add_library inside freeglut/CMakeLists.txt
    freeglut_static
    # got the name from the GLEW documentation
    glew_s
)

# Set output directory for the final executable
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/${TARGET_PLATFORM}"
)

# ====== FREEGLUT CONFIG ======

add_subdirectory(deps/freeglut)

# Modify FREEGLUT CMake flags
set(FREEGLUT_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(FREEGLUT_BUILD_DEMOS OFF CACHE BOOL "" FORCE)

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
