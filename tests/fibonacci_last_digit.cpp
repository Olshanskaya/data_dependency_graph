#include <iostream>

uint64_t get_fibonacci_last_digit_naive(int n) {
    if (n <= 1)
        return n;

    uint64_t previous = 0;
    uint64_t current  = 1;

    for (uint64_t i = 1; i < n; ++i) {
        uint64_t tmp_previous = previous;
        previous = current;
        current = tmp_previous + current;
    }

    return current % 10;
}

uint64_t get_fibonacci_last_digit(int n) {
    if (n <= 1)
        return n;

    uint64_t previous = 0;
    uint64_t current  = 1;

    for (uint64_t i = 1; i < n; ++i) {
        uint64_t tmp_previous = previous;
        previous = current;
        current = tmp_previous + current;

        current%=10;

        previous%=10;
    }

    return current % 10;
}

int main() {
    int n;
    std::cin >> n;
    int c = get_fibonacci_last_digit(n);
    std::cout << c << '\n';
}
