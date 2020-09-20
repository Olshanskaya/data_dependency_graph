#include <iostream>
#include <vector>
#include <algorithm>

int MaxPairwiseProduct(const std::vector<int>& numbers) {
    int max_product = 0;
    int n = numbers.size();

    for (int first = 0; first < n; ++first) {
        for (int second = first + 1; second < n; ++second) {
            max_product = std::max(max_product,
                numbers[first] * numbers[second]);
        }
    }

    return max_product;
}

int64_t MaxPairwiseProductFast(const std::vector<int>& numbers) {
    int first_indx = -1;
    int second_indx = -1;
    int maxEl = -1;

    for (int i = 0; i < numbers.size(); ++i) {
        if  (maxEl < numbers[i]) {
            maxEl = numbers[i];
            first_indx = i;
        }
    }
    maxEl = -1;

    for (int i = 0; i < numbers.size(); ++i) {
        if  (maxEl < numbers[i] && i != first_indx) {
            maxEl = numbers[i];
            second_indx = i;
        }
    }
    //std::cout << numbers[first_indx] << numbers[second_indx] << std:: endl;


    return (int64_t)numbers[first_indx] * (int64_t)numbers[second_indx];

}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> numbers(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> numbers[i];
    }

    std::cout << MaxPairwiseProductFast(numbers) << "\n";
    return 0;
}

