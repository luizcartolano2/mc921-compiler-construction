; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"v" = global [4 x i32] [i32 1, i32 2, i32 3, i32 4], align 16
@".str.0" = constant [22 x i8] c"assertion_fail on 9:5\00", align 1
define void @"main"() 
{
entry:
  %"sum" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"sum"
  br label %"2"
"2":
  %".4" = load i32, i32* %"i", align 4
  %".5" = icmp slt i32 %".4", 4
  br i1 %".5", label %"3", label %"4"
"3":
  %".7" = load i32, i32* %"i", align 4
  %".8" = getelementptr [4 x i32], [4 x i32]* @"v", i32 0, i32 %".7"
  %".9" = load i32, i32* %"sum", align 4
  %".10" = load i32, i32* %".8", align 4
  %".11" = add i32 %".9", %".10"
  store i32 %".11", i32* %"sum", align 4
  %".13" = load i32, i32* %"i", align 4
  %".14" = add i32 %".13", 1
  store i32 %".14", i32* %"i", align 4
  br label %"2"
"4":
  %".17" = load i32, i32* %"sum", align 4
  %".18" = icmp eq i32 %".17", 10
  br i1 %".18", label %"0", label %"21"
"21":
  %".20" = bitcast [3 x i8]* @".fmt" to i8*
  %".21" = call i32 (i8*, ...) @"printf"(i8* %".20", [22 x i8]* @".str.0")
  br label %"0"
"0":
  ret void
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1