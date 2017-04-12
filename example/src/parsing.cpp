//
// Created by OtherPlayers on 4/10/17.
//

#include <string>
#include <sstream>
#include <iostream>

std::string parse_for_arg(char* args[], int arglength, std::string target) {
    for (int i = 0; i < arglength - 1; ++i) {
        if (std::string(args[i]) == target) {
            return std::string(args[i+1]);
        }
    }
    return "";
}

bool flag_is_set(char* args[], int arglength, std::string flag) {
    for (int i = 0; i < arglength; ++i) {
        if (std::string(args[i]) == flag) {
            return true;
        }
    }
    return false;
}