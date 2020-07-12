; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = global [5 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5], align 16
@".str.1" = constant [5 x i8] c"xpto\00", align 1
@".str.2" = constant [22 x i8] c"assertion_fail on 9:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"v" = alloca [5 x i32], align 16
  %"c" = alloca [4 x i8], align 4
  %"w" = alloca [4 x i8], align 4
  %"i" = alloca i32, align 4
  %"j" = alloca i32, align 4
  %"k" = alloca i32, align 4
  %".2" = bitcast [5 x i32]* @".str.0" to i8*
  %".3" = bitcast [5 x i32]* %"v" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 20, i1 false)
  %".5" = bitcast [5 x i8]* @".str.1" to i8*
  %".6" = bitcast [4 x i8]* %"c" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".6", i8* %".5", i64 4, i1 false)
  store i32 2, i32* %"i", align 4
  store i32 3, i32* %"j", align 4
  store i32 4, i32* %"k", align 4
  %".11" = getelementptr [4 x i8], [4 x i8]* %"c", i32 0, i32 1
  %".12" = load i8, i8* %".11", align 8
  %".13" = getelementptr [4 x i8], [4 x i8]* %"w", i32 0, i32 2
  store i8 %".12", i8* %".13", align 1
  %".15" = load i32, i32* %"i", align 4
  %".16" = load i32, i32* %"j", align 4
  %".17" = add i32 %".15", %".16"
  %".18" = load i32, i32* %"k", align 4
  %".19" = add i32 %".17", %".18"
  %".20" = load i32, i32* %"i", align 4
  %".21" = getelementptr [5 x i32], [5 x i32]* %"v", i32 0, i32 %".20"
  store i32 %".19", i32* %".21", align 4
  %".23" = load i32, i32* %"j", align 4
  %".24" = sub i32 %".23", 2
  store i32 %".24", i32* %"j", align 4
  %".26" = load i32, i32* %"i", align 4
  %".27" = getelementptr [4 x i8], [4 x i8]* %"w", i32 0, i32 %".26"
  %".28" = load i32, i32* %"j", align 4
  %".29" = getelementptr [4 x i8], [4 x i8]* %"c", i32 0, i32 %".28"
  %".30" = load i8, i8* %".27", align 8
  %".31" = load i8, i8* %".29", align 8
  %".32" = icmp eq i8 %".30", %".31"
  %".33" = load i32, i32* %"i", align 4
  %".34" = getelementptr [5 x i32], [5 x i32]* %"v", i32 0, i32 %".33"
  %".35" = load i32, i32* %".34", align 8
  %".36" = icmp eq i32 %".35", 9
  %".37" = and i1 %".32", %".36"
  br i1 %".37", label %"%33", label %"%34"
"%33":
  br label %"%35"
"%34":
  %".40" = bitcast [3 x i8]* @".fmt" to i8*
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".40", [22 x i8]* @".str.2")
  br label %"%0"
"%35":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".45" = load i32, i32* %"1", align 4
  ret i32 %".45"
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1