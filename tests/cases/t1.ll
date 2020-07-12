; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"v" = global [4 x i32] [i32 1, i32 2, i32 3, i32 4], align 16
@"n" = global i32 10, align 4
@"c" = constant [5 x i8] c"xpto\00", align 1