#include <curlpp/cURLpp.hpp>
#include <curlpp/Options.hpp>
#include <curlpp/Easy.hpp>
#include <filesystem>
#include <sstream>
#include <fstream>
#include <iostream>
#include <string>
#include "../include/nlohmann/json.hpp"


using json = nlohmann::json;

// get the user credentials on the XDG_PATH
std::string get_credentials() {
    char *env = std::getenv("XDG_CONFIG_PATH");
    std::string env_path;
    if (env == nullptr) {
        env = std::getenv("HOME");
        env_path = env;
        env_path = env_path + "/.config";
        if (env == nullptr) {
            std::cout << "shit's wild" << std::endl;
            exit(1);
        }
    }

    env_path = env_path + "/honk";

    if (!std::filesystem::is_directory(env_path) || !std::filesystem::exists(env_path)) {
        std::filesystem::create_directory(env_path);
    }

    std::string config_file_path = env_path + "/config.json";

    json data;
    if (std::filesystem::exists(config_file_path)) {
        std::ifstream f(config_file_path);
        data = json::parse(f);
    } else {
        std::cout << "Shit's wild" << std::endl;
    }

    return data["api_credentials"];
}

int main() {
    std::string api_credentials = get_credentials();
//    std::stringstream result;

    std::cout << api_credentials << std::endl;
    curlpp::Cleanup myCleanup;
    curlpp::Easy myRequest;
    myRequest.setOpt<cURLpp::Options::Url>("https://honk.rafaelmc.net/api/honks/");
    std::list <std::string> header;
    header.push_back("Authorization: Token " + api_credentials);
    myRequest.setOpt(new curlpp::options::HttpHeader(header));
//    myRequest.setOpt(cURLpp::options::WriteStream(&result));
    myRequest.perform();



    std::cout << "Hello, World!" << std::endl;
    return 0;
}
