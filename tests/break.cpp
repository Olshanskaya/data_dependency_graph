int fun_br(int n, int i) {
    int r = i;
    int j = 1;
    while (j > 1000) {
        r = i * r;
        j = j + 1;
        if(j == n) {
            break;
        }
    }
    return r;
}
