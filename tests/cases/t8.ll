; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [22 x i8] c"assertion_fail on 5:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"x" = alloca i32, align 4
  %"y" = alloca i32, align 4
  %"z" = alloca i32, align 4
  store i32 2, i32* %"x", align 4
  %".3" = load i32, i32* %"x", align 4
  %".4" = add i32 %".3", 1
  store i32 %".4", i32* %"x", align 4
  store i32 %".4", i32* %"y", align 4
  %".7" = load i32, i32* %"x", align 4
  %".8" = add i32 %".7", 1
  store i32 %".8", i32* %"x", align 4
  store i32 %".7", i32* %"z", align 4
  %".11" = load i32, i32* %"y", align 4
  %".12" = icmp eq i32 %".11", 3
  %".13" = load i32, i32* %"z", align 4
  %".14" = icmp eq i32 %".13", 3
  %".15" = and i1 %".12", %".14"
  br i1 %".15", label %"%16", label %"%17"
"%16":
  br label %"%18"
"%17":
  %".18" = bitcast [3 x i8]* @".fmt" to i8*
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", [22 x i8]* @".str.0")
  br label %"%0"
"%18":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".23" = load i32, i32* %"1", align 4
  ret i32 %".23"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1