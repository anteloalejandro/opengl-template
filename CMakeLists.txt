cmake_minimum_required(VERSION 3.15)
project(main C)

# Set TARGET_PLATFORM variable
set(TARGET_PLATFORM "${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}")
# Set output directory to lib/TARGET_PLATFORM.
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")

add_subdirectory(deps/freeglut)

# Modify FREEGLUT CMake flags
set(FREEGLUT_BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(FREEGLUT_BUILD_DEMOS OFF CACHE BOOL "" FORCE)

# Overwrite FREEGLUT output directory and name
if(TARGET freeglut_static)
    set_target_properties(freeglut_static PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}"
        OUTPUT_NAME "freeglut"
    )
endif()
