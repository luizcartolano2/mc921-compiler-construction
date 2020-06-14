int main() {
    int i = 3, n = 6;
    for (int k = 1; k < n; k++) {
        if (i >= n) {
            break;
        }
        else {
            i = i + 1;
        }
    }
    assert i == n;
    return 0;
}
