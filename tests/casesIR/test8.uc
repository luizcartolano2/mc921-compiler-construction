
int (operation)(int x, int y);

int add(int x, int y) {
    return x + y;
}

int subtract(int x, int y) {
    return x - y;
}

int main() {
   int  foo = 2, bar = 3;
   //read(foo, bar);
   //operation = subtract;
   print(foo, " + ", bar, " = ", operation(foo, bar), ", ");

   return 0;
}


