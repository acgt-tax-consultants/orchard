#include <stdio.h>
#include <stdlib.h>


void read_file(char* in_filename){

}

void write_file(char* out_filename, int x){
    FILE *out_file = fopen(out_filename, "wb");
    fprintf(out_file, "This is the output of test module 1.\n");
    fprintf(out_file, "%d", x);
}

int main(int argc, char** argv) {

  if (argc != 4){
        printf("usage: module1 inputfilename outputfilename int");
        return(-1);
    }

    int temp = atoi(argv[3]);
    read_file(argv[1]);
    write_file(argv[2], temp);


    return 0;
}
