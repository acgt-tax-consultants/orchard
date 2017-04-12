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

    // Now we can finally open up our outfile
    std::ofstream output(outfile, std::ifstream::out);
    if (!output.good()) {
        std::cerr << "Error: invalid outfile " << outfile;
        return 1;
    }

    // Actual functionality, print every token from input into output
    // with spaces between and then print the digit at the end
    std::string token;
    while (input >> token) {
        output << token << " ";
    }
    output << digit;

    // Close up our streams
    input.close();
    output.close();
    return 0;
}