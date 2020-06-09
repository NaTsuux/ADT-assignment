#include "function.h"

const char* structPath = "bjtu.edu.cn/structure.txt";
Node* head;
int TotalNum;
int rank[200][200];

int main(int argc, char* argv[]) {
    FILE* fp = fopen(structPath, "r");
    if (fp == NULL) {
        printf("Error with opening file\n");
        return 0;
    }
    head = mallocNode('!');
    char buffer[100];
    while (fscanf(fp, "%s", buffer) != EOF) {
        insert(buffer);
    }
    return 0;
}