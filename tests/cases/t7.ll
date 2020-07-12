; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 15:5\00", align 1
define i32 @"gcd"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32, align 4
  %"x" = alloca i32, align 4
  %"y" = alloca i32, align 4
  %"g" = alloca i32, align 4
  store i32 %".1", i32* %"x", align 4
  store i32 %".2", i32* %"y", align 4
  %".6" = load i32, i32* %"y", align 4
  store i32 %".6", i32* %"g", align 4
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"x", align 4
  %".10" = icmp sgt i32 %".9", 0
  br i1 %".10", label %"%6", label %"%7"
"%6":
  %".12" = load i32, i32* %"x", align 4
  store i32 %".12", i32* %"g", align 4
  %".14" = load i32, i32* %"y", align 4
  %".15" = load i32, i32* %"x", align 4
  %".16" = sdiv i32 %".14", %".15"
  %".17" = load i32, i32* %"x", align 4
  %".18" = mul i32 %".16", %".17"
  %".19" = load i32, i32* %"y", align 4
  %".20" = sub i32 %".19", %".18"
  store i32 %".20", i32* %"x", align 4
  %".22" = load i32, i32* %"g", align 4
  store i32 %".22", i32* %"y", align 4
  br label %"%5"
"%7":
  %".25" = load i32, i32* %"g", align 4
  store i32 %".25", i32* %"3", align 4
  br label %"%2"
"%2":
  %".28" = load i32, i32* %"3", align 4
  ret i32 %".28"
}

define void @"main"() 
{
"%entry":
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  store i32 198, i32* %"a", align 4
  store i32 36, i32* %"b", align 4
  %".4" = load i32, i32* %"a", align 4
  %".5" = load i32, i32* %"b", align 4
  %".6" = call i32 @"gcd"(i32 %".4", i32 %".5")
  %".7" = icmp eq i32 %".6", 18
  br i1 %".7", label %"%8", label %"%9"
"%8":
  br label %"%10"
"%9":
  %".10" = bitcast [3 x i8]* @".fmt" to i8*
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", [23 x i8]* @".str.0")
  br label %"%0"
"%10":
  br label %"%0"
"%0":
  ret void
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1