int fun_cont(int n) {
    int i = 0;
    do {
        i = i + 1;
        if(i % 2) {
        continue;
        }
    } while (i < n);
    return i;
}