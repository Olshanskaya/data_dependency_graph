int fibonacci_fast(int n) {
    if(n <= 1) {
        return n;
        }
    int a = 0;
    int b = 1;

    for(int i = 1; i < n; ++i) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}