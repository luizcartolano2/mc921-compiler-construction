; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 16:5\00", align 1
define i32 @"f"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"p" = alloca i32, align 4
  %"q" = alloca i32, align 4
  %"t" = alloca i32, align 4
  store i32 %".1", i32* %"n", align 4
  %".5" = load i32, i32* %"n", align 4
  %".6" = icmp slt i32 %".5", 2
  br i1 %".6", label %"%4", label %"%5"
"%4":
  %".8" = load i32, i32* %"n", align 4
  store i32 %".8", i32* %"3", align 4
  br label %"%2"
"%5":
  %".11" = load i32, i32* %"n", align 4
  %".12" = sub i32 %".11", 1
  %".13" = load i32, i32* %"p", align 4
  %".14" = call i32 @"f"(i32 %".12", i32 %".13")
  %".15" = load i32, i32* %"n", align 4
  %".16" = sub i32 %".15", 2
  %".17" = load i32, i32* %"q", align 4
  %".18" = call i32 @"f"(i32 %".16", i32 %".17")
  %".19" = add i32 %".14", %".18"
  store i32 %".19", i32* %"t", align 4
  %".21" = load i32, i32* %"p", align 4
  %".22" = load i32, i32* %"q", align 4
  %".23" = add i32 %".21", %".22"
  %".24" = add i32 %".23", 1
  %".25" = load i32, i32* %"t", align 4
  store i32 %".25", i32* %"3", align 4
  br label %"%2"
"%2":
  %".28" = load i32, i32* %"3", align 4
  ret i32 %".28"
}

define i32 @"main"() 
{
"%entry":
  %".2" = call i32 @"f"(i32 3, i32 9)
  %".3" = mul i32 %".2", 9
  %".4" = icmp eq i32 %".3", 18
  br i1 %".4", label %"%0", label %"%13"
"%13":
  %".6" = bitcast [3 x i8]* @".fmt" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1