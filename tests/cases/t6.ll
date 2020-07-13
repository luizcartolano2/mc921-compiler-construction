; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5]
@".str.1" = constant [5 x i8] c"xpto\00"
@".str.2" = constant [22 x i8] c"assertion_fail on 9:5\00"
define i32 @"main"() 
{
"%entry":
  %"v" = alloca [5 x i32]
  %"c" = alloca [4 x i8]
  %"w" = alloca [4 x i8]
  %".2" = bitcast [5 x i32]* @".str.0" to i8*
  %".3" = bitcast [5 x i32]* %"v" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 20, i1 false)
  %".5" = bitcast [5 x i8]* @".str.1" to i8*
  %".6" = bitcast [4 x i8]* %"c" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".6", i8* %".5", i64 4, i1 false)
  %".8" = getelementptr [4 x i8], [4 x i8]* %"c", i32 0, i32 1
  %".9" = load i8, i8* %".8"
  %".10" = getelementptr [4 x i8], [4 x i8]* %"w", i32 0, i32 2
  store i8 %".9", i8* %".10"
  %".12" = getelementptr [5 x i32], [5 x i32]* %"v", i32 0, i32 2
  store i32 9, i32* %".12"
  %".14" = getelementptr [4 x i8], [4 x i8]* %"w", i32 0, i32 2
  %".15" = getelementptr [4 x i8], [4 x i8]* %"c", i32 0, i32 1
  %".16" = load i8, i8* %".14"
  %".17" = load i8, i8* %".15"
  %".18" = icmp eq i8 %".16", %".17"
  %".19" = getelementptr [5 x i32], [5 x i32]* %"v", i32 0, i32 2
  %".20" = load i32, i32* %".19"
  %".21" = icmp eq i32 %".20", 9
  %".22" = and i1 %".18", %".21"
  br i1 %".22", label %"%0", label %"%34"
"%34":
  %".24" = bitcast [3 x i8]* @".fmt" to i8*
  %".25" = call i32 (i8*, ...) @"printf"(i8* %".24", [22 x i8]* @".str.2")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00"