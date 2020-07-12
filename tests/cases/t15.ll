; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"m" = global [3 x [2 x i32]] [[2 x i32] [i32 1, i32 2], [2 x i32] [i32 3, i32 4], [2 x i32] [i32 5, i32 6]], align 4
@".str.0" = constant [22 x i8] c"assertion_fail on 8:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"sum" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"sum"
  store i32 0, i32* %"i"
  br label %"%3"
"%3":
  %".5" = load i32, i32* %"i", align 4
  %".6" = icmp slt i32 %".5", 3
  br i1 %".6", label %"%4", label %"%5"
"%4":
  %".8" = load i32, i32* %"i", align 4
  %".9" = mul i32 2, %".8"
  %".10" = add i32 %".9", 0
  %".11" = sdiv i32 %".10", 2
  %".12" = srem i32 %".10", 2
  %".13" = getelementptr [3 x [2 x i32]], [3 x [2 x i32]]* @"m", i32 0, i32 %".11"
  %".14" = getelementptr [2 x i32], [2 x i32]* %".13", i32 0, i32 %".12"
  %".15" = load i32, i32* %"i", align 4
  %".16" = mul i32 2, %".15"
  %".17" = add i32 %".16", 1
  %".18" = sdiv i32 %".17", 2
  %".19" = srem i32 %".17", 2
  %".20" = getelementptr [3 x [2 x i32]], [3 x [2 x i32]]* @"m", i32 0, i32 %".18"
  %".21" = getelementptr [2 x i32], [2 x i32]* %".20", i32 0, i32 %".19"
  %".22" = load i32, i32* %".14", align 8
  %".23" = load i32, i32* %".21", align 8
  %".24" = add i32 %".22", %".23"
  %".25" = load i32, i32* %"sum", align 4
  %".26" = add i32 %".24", %".25"
  store i32 %".26", i32* %"sum", align 4
  %".28" = load i32, i32* %"i", align 4
  %".29" = add i32 %".28", 1
  store i32 %".29", i32* %"i", align 4
  br label %"%3"
"%5":
  %".32" = load i32, i32* %"sum", align 4
  %".33" = icmp eq i32 %".32", 21
  br i1 %".33", label %"%0", label %"%34"
"%34":
  %".35" = bitcast [3 x i8]* @".fmt" to i8*
  %".36" = call i32 (i8*, ...) @"printf"(i8* %".35", [22 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret i32 0
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1