cmake_minimum_required(VERSION 3.15)
# project(<project_name> <language>)
project(main C)

add_executable(main
    src/main.c
)

# Set TARGET_PLATFORM variable
set(TARGET_PLATFORM "${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}")
# Set output directory to lib/TARGET_PLATFORM.
set(PREBUILT_LIB_DIR "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")
set(CMAKE "${CMAKE_SOURCE_DIR}/lib/${TARGET_PLATFORM}")

target_include_directories(main PRIVATE
    deps/freeglut/include
    deps/glew/include
)
target_link_libraries(main PRIVATE
    # got the name from add_library inside freeglut/CMakeLists.txt
    freeglut_static
)

# Set output directory for the final executable
set_target_properties(main PROPERTIES
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
