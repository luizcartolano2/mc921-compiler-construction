; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 11:5\00"
define i32 @"main"() 
{
"%entry":
  %"n" = alloca i32
  %"r" = alloca i32
  %"sum" = alloca double
  store double              0x0, double* %"sum"
  store i32 5743475, i32* %"n"
  br label %"%5"
"%5":
  %".5" = load i32, i32* %"n"
  %".6" = icmp sgt i32 %".5", 0
  br i1 %".6", label %"%6", label %"%7"
"%6":
  %".8" = load i32, i32* %"n"
  %".9" = srem i32 %".8", 10
  store i32 %".9", i32* %"r"
  %".11" = load double, double* %"sum"
  %".12" = fmul double %".11", 0x4024000000000000
  %".13" = load i32, i32* %"r"
  %".14" = sitofp i32 %".13" to double
  %".15" = fadd double %".12", %".14"
  store double %".15", double* %"sum"
  %".17" = load i32, i32* %"n"
  %".18" = sdiv i32 %".17", 10
  store i32 %".18", i32* %"n"
  br label %"%5"
"%7":
  %".21" = load double, double* %"sum"
  %".22" = fptosi double %".21" to i32
  %".23" = icmp eq i32 5743475, %".22"
  br i1 %".23", label %"%0", label %"%28"
"%28":
  %".25" = bitcast [3 x i8]* @".fmt" to i8*
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00"