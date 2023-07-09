cmake_minimum_required(VERSION 3.25)
project(honk_cli)

set(CMAKE_CXX_STANDARD 23)
find_package(unofficial-curlpp CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
add_executable(honk_cli src/main.cpp)
target_link_libraries(honk_cli PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(honk_cli PRIVATE unofficial::curlpp::curlpp)
