; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [22 x i8] c"assertion_fail on 5:5\00", align 1
define i32 @"main"() 
{
"%entry":
  br label %"%0"
"%0":
  ret i32 0
}
