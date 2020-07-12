; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 15:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"i" = alloca i32, align 4
  %"flag" = alloca i32, align 4
  store i32 0, i32* %"flag"
  store i32 2, i32* %"i"
  br label %"%4"
"%4":
  %".5" = load i32, i32* %"i", align 4
  %".6" = icmp sle i32 %".5", 95
  br i1 %".6", label %"%5", label %"%6"
"%5":
  %".8" = load i32, i32* %"i", align 4
  %".9" = call i32 @"checkPrime"(i32 %".8")
  %".10" = icmp eq i32 %".9", 1
  br i1 %".10", label %"%13", label %"%14"
"%13":
  %".12" = load i32, i32* %"i", align 4
  %".13" = sub i32 190, %".12"
  %".14" = call i32 @"checkPrime"(i32 %".13")
  %".15" = icmp eq i32 %".14", 1
  br i1 %".15", label %"%20", label %"%14"
"%20":
  store i32 1, i32* %"flag"
  br label %"%14"
"%14":
  %".19" = load i32, i32* %"i", align 4
  %".20" = add i32 %".19", 1
  store i32 %".20", i32* %"i", align 4
  br label %"%4"
"%6":
  %".23" = load i32, i32* %"flag", align 4
  %".24" = icmp eq i32 %".23", 1
  br i1 %".24", label %"%0", label %"%37"
"%37":
  %".26" = bitcast [3 x i8]* @".fmt" to i8*
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

define i32 @"checkPrime"(i32 %".1") 
{
"%entry":
  %"2" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"i" = alloca i32, align 4
  %"isPrime" = alloca i32, align 4
  store i32 %".1", i32* %"n", align 4
  store i32 1, i32* %"isPrime"
  store i32 2, i32* %"i"
  br label %"%4"
"%4":
  %".7" = load i32, i32* %"n", align 4
  %".8" = sdiv i32 %".7", 2
  %".9" = load i32, i32* %"i", align 4
  %".10" = icmp sle i32 %".9", %".8"
  br i1 %".10", label %"%5", label %"%6"
"%5":
  %".12" = load i32, i32* %"n", align 4
  %".13" = load i32, i32* %"i", align 4
  %".14" = srem i32 %".12", %".13"
  %".15" = icmp eq i32 %".14", 0
  br i1 %".15", label %"%13", label %"%14"
"%13":
  store i32 0, i32* %"isPrime"
  br label %"%6"
"%14":
  %".19" = load i32, i32* %"i", align 4
  %".20" = add i32 %".19", 1
  store i32 %".20", i32* %"i", align 4
  br label %"%4"
"%6":
  %".23" = load i32, i32* %"isPrime", align 4
  store i32 %".23", i32* %"2", align 4
  br label %"%1"
"%1":
  %".26" = load i32, i32* %"2", align 4
  ret i32 %".26"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1