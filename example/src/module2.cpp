#include <iostream>
#include <fstream>
#include "parsing.h"

int main( int argc, char *argv[]) {
    // Check to make sure we at least meet the minimum arguments
    if (argc < 2) {
        std::cerr << "Error: Too few arguments";
        return 1;
    }

    // Get the infile and check if it is good
    std::string infile = argv[1];
    std::ifstream input(infile, std::ifstream::in);
    if (!input.good()) {
        std::cerr << "Error: invalid infile " << infile;
        return 1;
    }

    // Get the optional infile if it exists and check if it is good
    std::string optinfile = parse_for_arg(argv, argc, "--optin");
    bool optin = false;
    std::ifstream optinput;
    if (optinfile != "") {
        optin = true;
        optinput.open(optinfile, std::ifstream::in);
        if (!optinput.good()) {
            std::cerr << "Error: invalid optional infile " << optinfile;
            return 1;
        }
    }

    // Get the outfile, don't open it yet though so we don't create it only
    // to error out later
    std::string outfile = parse_for_arg(argv, argc, "--out");
    if (outfile == "") {
        std::cerr << "Error: invalid outfile";
        return 1;
    }

    // Get the digit we need to print
    long digit = strtol(parse_for_arg(argv, argc, "-d").c_str(), NULL, 10);
    if (digit == 0) {
        std::cerr << "Error: digit must be non-zero";
        return 1;
    }

    // Exclusive checking, error if both is set, but since they are optionals not
    // if neither is set
    bool forwards = flag_is_set(argv, argc, "-—optional_exclusive_forward");
    bool reverse = flag_is_set(argv, argc, "—-optional_exclusive_reverse");
    if (forwards && reverse) {
        std::cerr << "Error: reverse and forwards set";
        return 1;
    }
    bool exclusive = forwards;

    // Now we can finally open up our optional outfile and outfile
    std::string optoutfile = parse_for_arg(argv, argc, "--optout");
    bool optout = false;
    std::ofstream optoutput;
    if (optoutfile != "") {
        optout = true;
        optoutput.open(optoutfile, std::ifstream::out);
        if (!optoutput.good()) {
            std::cerr << "Error: invalid optional outfile " << optoutfile;
            return 1;
        }
    }
    std::ofstream output(outfile, std::ifstream::out);
    if (!output.good()) {
        std::cerr << "Error: invalid outfile " << outfile;
        return 1;
    }

    // Actual functionality, print the digit and string to the optional output file.
    // Then print the digit at the front/end of the file if the optional forwards/reverse
    // was set, and then print everything from both input and optinput into our output
    // in that order.
    if (optout) {
        optoutput << digit << " Extra digit output file";
    }
    if (exclusive) {
        output << digit << " ";
    }
    std::string token;
    while (input >> token) {
        output << token << " ";
    }
    if (optin) {
        while (optinput >> token) {
            output << token << " ";
        }
    }
    if (!exclusive) {
        output << digit;
    }
    // Close our streams
    optinput.close();
    optoutput.close();
    input.close();
    output.close();
    return 0;
}