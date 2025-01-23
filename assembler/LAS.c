#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char *args[argc + 2];

    args[0] = "python";
    args[1] = "assembler.py";

    for (int i = 1; i < argc; i++) {
        args[i + 1] = argv[i];
    }

    args[argc + 1] = NULL;

    execvp(args[0], args);
    return 0;
}