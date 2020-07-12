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
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  store i32 11, i32* %"a", align 4
  store i32 99, i32* %"b", align 4
  %".4" = load i32, i32* %"a", align 4
  %".5" = load i32, i32* %"b", align 4
  %".6" = add i32 %".4", %".5"
  store i32 %".6", i32* %"a", align 4
  %".8" = load i32, i32* %"a", align 4
  %".9" = load i32, i32* %"b", align 4
  %".10" = sub i32 %".8", %".9"
  store i32 %".10", i32* %"b", align 4
  %".12" = load i32, i32* %"a", align 4
  %".13" = load i32, i32* %"b", align 4
  %".14" = sub i32 %".12", %".13"
  store i32 %".14", i32* %"a", align 4
  %".16" = load i32, i32* %"a", align 4
  %".17" = icmp eq i32 %".16", 99
  %".18" = load i32, i32* %"b", align 4
  %".19" = icmp eq i32 %".18", 11
  %".20" = and i1 %".17", %".19"
  br i1 %".20", label %"%20", label %"%21"
"%20":
  br label %"%22"
"%21":
  %".23" = bitcast [3 x i8]* @".fmt" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", [23 x i8]* @".str.0")
  br label %"%0"
"%22":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".28" = load i32, i32* %"1", align 4
  ret i32 %".28"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1