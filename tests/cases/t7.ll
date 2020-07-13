; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 15:5\00"
define i32 @"gcd"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32
  %"x" = alloca i32
  %"y" = alloca i32
  %"g" = alloca i32
  store i32 %".1", i32* %"x"
  store i32 %".2", i32* %"y"
  %".6" = load i32, i32* %"y"
  store i32 %".6", i32* %"g"
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"x"
  %".10" = icmp sgt i32 %".9", 0
  br i1 %".10", label %"%6", label %"%7"
"%6":
  %".12" = load i32, i32* %"x"
  store i32 %".12", i32* %"g"
  %".14" = load i32, i32* %"y"
  %".15" = load i32, i32* %"x"
  %".16" = sdiv i32 %".14", %".15"
  %".17" = load i32, i32* %"x"
  %".18" = mul i32 %".16", %".17"
  %".19" = load i32, i32* %"y"
  %".20" = sub i32 %".19", %".18"
  store i32 %".20", i32* %"x"
  %".22" = load i32, i32* %"g"
  store i32 %".22", i32* %"y"
  br label %"%5"
"%7":
  %".25" = load i32, i32* %"g"
  store i32 %".25", i32* %"3"
  br label %"%2"
"%2":
  %".28" = load i32, i32* %"3"
  ret i32 %".28"
}

define void @"main"() 
{
"%entry":
  %".2" = call i32 @"gcd"(i32 198, i32 36)
  %".3" = icmp eq i32 %".2", 18
  br i1 %".3", label %"%0", label %"%9"
"%9":
  %".5" = bitcast [3 x i8]* @".fmt" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".5", [23 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret void
}

@".fmt" = internal constant [3 x i8] c"%s\00"