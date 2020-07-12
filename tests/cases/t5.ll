; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [22 x i8] c"assertion_fail on 9:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"reverse" = alloca i32, align 4
  %"rem" = alloca i32, align 4
  store i32 1, i32* %"n", align 4
  store i32 0, i32* %"reverse", align 4
  %".4" = load i32, i32* %"n", align 4
  %".5" = add i32 17327, %".4"
  store i32 %".5", i32* %"n", align 4
  br label %"%7"
"%7":
  %".8" = load i32, i32* %"n", align 4
  %".9" = icmp sgt i32 %".8", 0
  br i1 %".9", label %"%8", label %"%9"
"%8":
  %".11" = load i32, i32* %"n", align 4
  %".12" = srem i32 %".11", 10
  store i32 %".12", i32* %"rem", align 4
  %".14" = load i32, i32* %"reverse", align 4
  %".15" = mul i32 %".14", 10
  %".16" = load i32, i32* %"rem", align 4
  %".17" = add i32 %".15", %".16"
  store i32 %".17", i32* %"reverse", align 4
  %".19" = load i32, i32* %"n", align 4
  %".20" = sdiv i32 %".19", 10
  store i32 %".20", i32* %"n", align 4
  br label %"%7"
"%9":
  %".23" = load i32, i32* %"reverse", align 4
  %".24" = icmp eq i32 %".23", 82371
  br i1 %".24", label %"%27", label %"%28"
"%27":
  br label %"%29"
"%28":
  %".27" = bitcast [3 x i8]* @".fmt" to i8*
  %".28" = call i32 (i8*, ...) @"printf"(i8* %".27", [22 x i8]* @".str.0")
  br label %"%0"
"%29":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".32" = load i32, i32* %"1", align 4
  ret i32 %".32"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1