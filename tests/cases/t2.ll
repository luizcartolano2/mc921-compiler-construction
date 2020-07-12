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
  %"k" = alloca i32, align 4
  %"p" = alloca i32, align 4
  %"q" = alloca i32, align 4
  %"t" = alloca i32, align 4
  store i32 %".1", i32* %"n", align 4
  store i32 %".2", i32* %"k", align 4
  %".6" = load i32, i32* %"n", align 4
  %".7" = icmp slt i32 %".6", 2
  br i1 %".7", label %"%4", label %"%5"
"%4":
  store i32 0, i32* %"k", align 4
  %".10" = load i32, i32* %"n", align 4
  store i32 %".10", i32* %"3", align 4
  br label %"%2"
"%5":
  %".13" = load i32, i32* %"n", align 4
  %".14" = sub i32 %".13", 1
  %".15" = load i32, i32* %"p", align 4
  %".16" = call i32 @"f"(i32 %".14", i32 %".15")
  %".17" = load i32, i32* %"n", align 4
  %".18" = sub i32 %".17", 2
  %".19" = load i32, i32* %"q", align 4
  %".20" = call i32 @"f"(i32 %".18", i32 %".19")
  %".21" = add i32 %".16", %".20"
  store i32 %".21", i32* %"t", align 4
  %".23" = load i32, i32* %"p", align 4
  %".24" = load i32, i32* %"q", align 4
  %".25" = add i32 %".23", %".24"
  %".26" = add i32 %".25", 1
  store i32 %".26", i32* %"k", align 4
  %".28" = load i32, i32* %"t", align 4
  store i32 %".28", i32* %"3", align 4
  br label %"%2"
"%2":
  %".31" = load i32, i32* %"3", align 4
  ret i32 %".31"
}

define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"m" = alloca i32, align 4
  store i32 9, i32* %"m", align 4
  %".3" = load i32, i32* %"m", align 4
  %".4" = call i32 @"f"(i32 3, i32 %".3")
  %".5" = load i32, i32* %"m", align 4
  %".6" = mul i32 %".4", %".5"
  %".7" = load i32, i32* %"m", align 4
  %".8" = load i32, i32* %"m", align 4
  %".9" = add i32 %".7", %".8"
  %".10" = icmp eq i32 %".6", %".9"
  br i1 %".10", label %"%12", label %"%13"
"%12":
  br label %"%14"
"%13":
  %".13" = bitcast [3 x i8]* @".fmt" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", [23 x i8]* @".str.0")
  br label %"%0"
"%14":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".18" = load i32, i32* %"1", align 4
  ret i32 %".18"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1