//
// Created by OtherPlayers on 4/11/17.
//

#ifndef EXAMPLE_MODULES_PARSING_H
#define EXAMPLE_MODULES_PARSING_H

#include <string>

std::string parse_for_arg(char* args[], int arglength, std::string target);
bool flag_is_set(char* args[], int arglength, std::string flag);

#endif //EXAMPLE_MODULES_PARSING_H
