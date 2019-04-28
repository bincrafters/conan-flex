project(test_package)
cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS NO_OUTPUT_DIRS)

find_package(FLEX)

set(FLEX_VARS
    FLEX_FOUND
    FLEX_EXECUTABLE
    FLEX_LIBRARIES
    FLEX_INCLUDE_DIRS
)

foreach(FLEX_VAR ${FLEX_VARS})
    message("${FLEX_VAR}: ${${FLEX_VAR}}")
    if(NOT ${FLEX_VAR})
        message(FATAL_ERROR "${FLEX_VAR} NOT FOUND")
    endif()
endforeach()


FLEX_TARGET(TestParser basic_nr.l "${CMAKE_CURRENT_BINARY_DIR}/lexer.cpp")

add_executable(${PROJECT_NAME}
    ${FLEX_TestParser_OUTPUTS}
)

enable_testing()
add_test(TestLexer
    "${PROJECT_NAME}" "${CMAKE_CURRENT_LIST_DIR}/basic_nr.txt"
)
