int n = 3;

int doubleMe () {
    return 3 * 3;
}

void main () {
    int v = n;
    v = doubleMe (3);
    assert v == n * n;
    return;
}
