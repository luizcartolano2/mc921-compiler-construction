; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 11:5\00"
define i32 @"main"() 
{
"%entry":
  %"i" = alloca i32
  %"k" = alloca i32
  store i32 3, i32* %"i"
  store i32 1, i32* %"k"
  br label %"%4"
"%4":
  %".5" = load i32, i32* %"k"
  %".6" = icmp slt i32 %".5", 6
  br i1 %".6", label %"%5", label %"%6"
"%5":
  %".8" = load i32, i32* %"i"
  %".9" = icmp sge i32 %".8", 6
  br i1 %".9", label %"%6", label %"%12"
"%12":
  %".11" = load i32, i32* %"i"
  %".12" = add i32 %".11", 1
  store i32 %".12", i32* %"i"
  br label %"%13"
"%13":
  %".15" = load i32, i32* %"k"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %"k"
  br label %"%4"
"%6":
  %".19" = load i32, i32* %"i"
  %".20" = icmp eq i32 %".19", 6
  br i1 %".20", label %"%0", label %"%27"
"%27":
  %".22" = bitcast [3 x i8]* @".fmt" to i8*
  %".23" = call i32 (i8*, ...) @"printf"(i8* %".22", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00"