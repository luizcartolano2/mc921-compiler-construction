; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"n" = global i32 10
@".str.0" = constant [23 x i8] c"assertion_fail on 10:5\00"
define i32 @"foo"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32
  %"a" = alloca i32
  %"b" = alloca i32
  store i32 %".1", i32* %"a"
  store i32 %".2", i32* %"b"
  %".6" = load i32, i32* %"a"
  %".7" = load i32, i32* %"b"
  %".8" = add i32 %".6", %".7"
  %".9" = load i32, i32* @"n"
  %".10" = mul i32 %".9", %".8"
  store i32 %".10", i32* %"3"
  br label %"%2"
"%2":
  %".13" = load i32, i32* %"3"
  ret i32 %".13"
}

define i32 @"main"() 
{
"%entry":
  %"e" = alloca i32
  %".2" = call i32 @"foo"(i32 2, i32 3)
  store i32 %".2", i32* %"e"
  %".4" = load i32, i32* %"e"
  %".5" = icmp eq i32 %".4", 50
  br i1 %".5", label %"%0", label %"%11"
"%11":
  %".7" = bitcast [3 x i8]* @".fmt" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00"