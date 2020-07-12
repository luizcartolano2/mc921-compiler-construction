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
  %"i" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"k" = alloca i32, align 4
  store i32 3, i32* %"i", align 4
  store i32 6, i32* %"n", align 4
  store i32 1, i32* %"k", align 4
  br label %"%4"
"%4":
  %".6" = load i32, i32* %"k", align 4
  %".7" = load i32, i32* %"n", align 4
  %".8" = icmp slt i32 %".6", %".7"
  br i1 %".8", label %"%5", label %"%6"
"%5":
  %".10" = load i32, i32* %"i", align 4
  %".11" = load i32, i32* %"n", align 4
  %".12" = icmp sge i32 %".10", %".11"
  br i1 %".12", label %"%11", label %"%12"
"%11":
  br label %"%6"
"%12":
  %".15" = load i32, i32* %"i", align 4
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %"i", align 4
  br label %"%13"
"%13":
  %".19" = load i32, i32* %"k", align 4
  %".20" = add i32 %".19", 1
  store i32 %".20", i32* %"k", align 4
  br label %"%4"
"%6":
  %".23" = load i32, i32* %"i", align 4
  %".24" = load i32, i32* %"n", align 4
  %".25" = icmp eq i32 %".23", %".24"
  br i1 %".25", label %"%26", label %"%27"
"%26":
  br label %"%28"
"%27":
  %".28" = bitcast [3 x i8]* @".fmt" to i8*
  %".29" = call i32 (i8*, ...) @"printf"(i8* %".28", [23 x i8]* @".str.0")
  br label %"%0"
"%28":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".33" = load i32, i32* %"1", align 4
  ret i32 %".33"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1