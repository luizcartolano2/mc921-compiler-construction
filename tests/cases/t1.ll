; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"v" = global [4 x i32] [i32 1, i32 2, i32 3, i32 4]
@".str.0" = constant [22 x i8] c"assertion_fail on 9:5\00"
define void @"main"() 
{
"%entry":
  %"sum" = alloca i32
  %"i" = alloca i32
  store i32 0, i32* %"sum"
  store i32 0, i32* %"i"
  br label %"%2"
"%2":
  %".5" = load i32, i32* %"i"
  %".6" = icmp slt i32 %".5", 4
  br i1 %".6", label %"%3", label %"%4"
"%3":
  %".8" = load i32, i32* %"i"
  %".9" = getelementptr [4 x i32], [4 x i32]* @"v", i32 0, i32 %".8"
  %".10" = load i32, i32* %"sum"
  %".11" = load i32, i32* %".9"
  %".12" = add i32 %".10", %".11"
  store i32 %".12", i32* %"sum"
  %".14" = load i32, i32* %"i"
  %".15" = add i32 %".14", 1
  store i32 %".15", i32* %"i"
  br label %"%2"
"%4":
  %".18" = load i32, i32* %"sum"
  %".19" = icmp eq i32 %".18", 10
  br i1 %".19", label %"%0", label %"%21"
"%21":
  %".21" = bitcast [3 x i8]* @".fmt" to i8*
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21", [22 x i8]* @".str.0")
  br label %"%0"
"%0":
  ret void
}

@".fmt" = internal constant [3 x i8] c"%s\00"