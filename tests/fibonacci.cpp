int fibonacci_fast(int n) {
    if(n <= 1) {
        return n;
        }
    int a = 0;
    int b = 1;
    int c;
    for(int i = 1; i < n; ++i) {
        c = a + c;
        if(c==0) {
        a = b;
        b = c;
        }

    }
    return b;
}