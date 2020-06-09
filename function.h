#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

struct Node {
    char value;
    int id_of_which_ends_here;
    vector<Node*> nxt;
};
Node* mallocNode(char key);
Node* fd(Node* cur, char key);
Node* ins(Node* cur, char key);
void insert(char* str);

extern Node* head;
extern int TotalNum;
extern double rnk[200][200];
extern char urlMap[200][100];
extern int outq[200];

const char* rootPath = "bjtu.edu.cn/";
const int HashSeed = 37;