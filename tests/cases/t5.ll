; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [22 x i8] c"assertion_fail on 9:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"n" = alloca i32, align 4
  %"reverse" = alloca i32, align 4
  %"rem" = alloca i32, align 4
  store i32 0, i32* %"reverse"
  store i32 17328, i32* %"n"
  br label %"%7"
"%7":
  %".5" = load i32, i32* %"n", align 4
  %".6" = icmp sgt i32 %".5", 0
  br i1 %".6", label %"%8", label %"%9"
"%8":
  %".8" = load i32, i32* %"n", align 4
  %".9" = srem i32 %".8", 10
  store i32 %".9", i32* %"rem", align 4
  %".11" = load i32, i32* %"reverse", align 4
  %".12" = mul i32 %".11", 10
  %".13" = load i32, i32* %"rem", align 4
  %".14" = add i32 %".12", %".13"
  store i32 %".14", i32* %"reverse", align 4
  %".16" = load i32, i32* %"n", align 4
  %".17" = sdiv i32 %".16", 10
  store i32 %".17", i32* %"n", align 4
  br label %"%7"
"%9":
  %".20" = load i32, i32* %"reverse", align 4
  %".21" = icmp eq i32 %".20", 82371
  br i1 %".21", label %"%0", label %"%28"
"%28":
  %".23" = bitcast [3 x i8]* @".fmt" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", [22 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1