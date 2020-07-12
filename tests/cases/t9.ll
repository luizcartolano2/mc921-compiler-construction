; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"n" = global i32 10, align 4
@".str.0" = constant [23 x i8] c"assertion_fail on 10:5\00", align 1
define i32 @"foo"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32, align 4
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  store i32 %".1", i32* %"a", align 4
  store i32 %".2", i32* %"b", align 4
  %".6" = load i32, i32* %"a", align 4
  %".7" = load i32, i32* %"b", align 4
  %".8" = add i32 %".6", %".7"
  %".9" = load i32, i32* @"n", align 4
  %".10" = mul i32 %".9", %".8"
  store i32 %".10", i32* %"3", align 4
  br label %"%2"
"%2":
  %".13" = load i32, i32* %"3", align 4
  ret i32 %".13"
}

define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"d" = alloca i32, align 4
  %"e" = alloca i32, align 4
  store i32 2, i32* %"c", align 4
  store i32 3, i32* %"d", align 4
  %".4" = load i32, i32* %"c", align 4
  %".5" = load i32, i32* %"d", align 4
  %".6" = call i32 @"foo"(i32 %".4", i32 %".5")
  store i32 %".6", i32* %"e", align 4
  %".8" = load i32, i32* %"e", align 4
  %".9" = icmp eq i32 %".8", 50
  br i1 %".9", label %"%10", label %"%11"
"%10":
  br label %"%12"
"%11":
  %".12" = bitcast [3 x i8]* @".fmt" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", [23 x i8]* @".str.0")
  br label %"%0"
"%12":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".17" = load i32, i32* %"1", align 4
  ret i32 %".17"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1