#include <stdio.h>

extern int hello();

int main() {
    printf("hello() returned %i\n", hello());
}
