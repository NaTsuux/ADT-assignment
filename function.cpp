#include "function.h"

const char* logPath = "bjtu.edu.cn/craw.log";
Node* mallocNode(char key) {
    Node* tmp = (Node*) malloc(sizeof(Node));
    if (tmp == NULL) {
        printf("Error with mallocing space for Node\n");
        exit(1);
    }
    tmp->id_of_which_ends_here = 0;
    tmp->value = key;
    tmp->nxt = vector<Node*>();
    return tmp;
}

Node* fd(Node* cur, char key) {
    for (Node* v : cur->nxt)
        if (v->value == key) return v;
    return NULL;
}

Node* ins(Node* cur, char key) {
    Node* tmp = mallocNode(key);
    cur->nxt.push_back(tmp);
    return tmp;
}

void insert(char* str) {
    printf("Inserting %s\n", str);

    Node* cur = head;
    for (int i = 0; i < strlen(str); i++) {
        Node* nxt = fd(cur, str[i]);

        if (nxt == NULL)
            cur = ins(cur, str[i]);
        else
            cur = nxt;
    }
    cur->id_of_which_ends_here = ++TotalNum;
    memcpy(urlMap[TotalNum], str, 100);
    printf("Finish insert, new id = %d\n", cur->id_of_which_ends_here);
}

int query(char* str) {
    Node* cur = head;
    for (int i = 0; i < strlen(str); i++) {
        Node* nxt = fd(cur, str[i]);
        if (nxt == NULL)
            return 0;
        else
            cur = nxt;
    }
    return cur->id_of_which_ends_here;
}
//?
void initMartrix() {
    FILE* fp = fopen(logPath, "r");
    char buff[100];
    int curnode = 0;
    int edgeNum = 0;
    while (fscanf(fp, "s", buff) != EOF) {
        if (buff[0] == '-') {
            int tonode = query(buff + 1);
            if (tonode == 0)
                continue;
            else {
                outq[curnode]++;
                rnk[curnode][tonode] = 1;
            }
        } else {
            for (int i = 1; i <= 170; i++) {
                if (rnk[curnode][i] == 1) rnk[curnode][i] = 1 / outq[curnode];
            }
            curnode = query(buff);
            continue;
        }
    }
}
