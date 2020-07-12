; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 11:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"r" = alloca i32, align 4
  %"temp" = alloca i32, align 4
  %"sum" = alloca double, align 8
  store double              0x0, double* %"sum", align 8
  store i32 5743475, i32* %"n", align 4
  %".4" = load i32, i32* %"n", align 4
  store i32 %".4", i32* %"temp", align 4
  br label %"%5"
"%5":
  %".7" = load i32, i32* %"n", align 4
  %".8" = icmp sgt i32 %".7", 0
  br i1 %".8", label %"%6", label %"%7"
"%6":
  %".10" = load i32, i32* %"n", align 4
  %".11" = srem i32 %".10", 10
  store i32 %".11", i32* %"r", align 4
  %".13" = load double, double* %"sum", align 8
  %".14" = fmul double %".13", 0x4024000000000000
  %".15" = load i32, i32* %"r", align 4
  %".16" = sitofp i32 %".15" to double
  %".17" = fadd double %".14", %".16"
  store double %".17", double* %"sum", align 8
  %".19" = load i32, i32* %"n", align 4
  %".20" = sdiv i32 %".19", 10
  store i32 %".20", i32* %"n", align 4
  br label %"%5"
"%7":
  %".23" = load double, double* %"sum", align 8
  %".24" = fptosi double %".23" to i32
  %".25" = load i32, i32* %"temp", align 4
  %".26" = icmp eq i32 %".25", %".24"
  br i1 %".26", label %"%27", label %"%28"
"%27":
  br label %"%29"
"%28":
  %".29" = bitcast [3 x i8]* @".fmt" to i8*
  %".30" = call i32 (i8*, ...) @"printf"(i8* %".29", [23 x i8]* @".str.0")
  br label %"%0"
"%29":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".34" = load i32, i32* %"1", align 4
  ret i32 %".34"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1