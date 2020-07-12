; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = global [10 x i32] [i32 5, i32 3, i32 7, i32 8, i32 4, i32 1, i32 9, i32 2, i32 0, i32 6], align 16
@".str.1" = constant [33 x i8] c"Sorted list in ascending order: \00", align 1
@".str.2" = constant [2 x i8] c" \00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"v" = alloca [1 x [0 x i32]], align 4
  %"n" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"d" = alloca i32, align 4
  %"swap" = alloca i32, align 4
  %".2" = bitcast [10 x i32]* @".str.0" to i8*
  %".3" = bitcast [1 x [0 x i32]]* %"v" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 0, i1 false)
  store i32 10, i32* %"n", align 4
  store i32 0, i32* %"c", align 4
  br label %"%3"
"%3":
  %".8" = load i32, i32* %"n", align 4
  %".9" = sub i32 %".8", 1
  %".10" = load i32, i32* %"c", align 4
  %".11" = icmp slt i32 %".10", %".9"
  br i1 %".11", label %"%4", label %"%5"
"%4":
  store i32 0, i32* %"d", align 4
  br label %"%12"
"%12":
  %".15" = load i32, i32* %"n", align 4
  %".16" = load i32, i32* %"c", align 4
  %".17" = sub i32 %".15", %".16"
  %".18" = sub i32 %".17", 1
  %".19" = load i32, i32* %"d", align 4
  %".20" = icmp slt i32 %".19", %".18"
  br i1 %".20", label %"%13", label %"%14"
"%13":
  %".22" = load i32, i32* %"d", align 4
  %".23" = sdiv i32 %".22", 0
  %".24" = srem i32 %".22", 0
  %".25" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".23"
  %".26" = getelementptr [0 x i32], [0 x i32]* %".25", i32 0, i32 %".24"
  %".27" = load i32, i32* %"d", align 4
  %".28" = add i32 %".27", 1
  %".29" = sdiv i32 %".28", 0
  %".30" = srem i32 %".28", 0
  %".31" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".29"
  %".32" = getelementptr [0 x i32], [0 x i32]* %".31", i32 0, i32 %".30"
  %".33" = load i32, i32* %".26", align 8
  %".34" = load i32, i32* %".32", align 8
  %".35" = icmp sgt i32 %".33", %".34"
  br i1 %".35", label %"%23", label %"%24"
"%23":
  %".37" = load i32, i32* %"d", align 4
  %".38" = sdiv i32 %".37", 0
  %".39" = srem i32 %".37", 0
  %".40" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".38"
  %".41" = getelementptr [0 x i32], [0 x i32]* %".40", i32 0, i32 %".39"
  %".42" = load i32, i32* %".41", align 8
  store i32 %".42", i32* %"swap", align 4
  %".44" = load i32, i32* %"d", align 4
  %".45" = add i32 %".44", 1
  %".46" = sdiv i32 %".45", 0
  %".47" = srem i32 %".45", 0
  %".48" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".46"
  %".49" = getelementptr [0 x i32], [0 x i32]* %".48", i32 0, i32 %".47"
  %".50" = load i32, i32* %".49", align 8
  %".51" = load i32, i32* %"d", align 4
  %".52" = sdiv i32 %".51", 0
  %".53" = srem i32 %".51", 0
  %".54" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".52"
  %".55" = getelementptr [0 x i32], [0 x i32]* %".54", i32 0, i32 %".53"
  store i32 %".50", i32* %".55", align 4
  %".57" = load i32, i32* %"swap", align 4
  %".58" = load i32, i32* %"d", align 4
  %".59" = add i32 %".58", 1
  %".60" = sdiv i32 %".59", 0
  %".61" = srem i32 %".59", 0
  %".62" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".60"
  %".63" = getelementptr [0 x i32], [0 x i32]* %".62", i32 0, i32 %".61"
  store i32 %".57", i32* %".63", align 4
  br label %"%24"
"%24":
  %".66" = load i32, i32* %"d", align 4
  %".67" = add i32 %".66", 1
  store i32 %".67", i32* %"d", align 4
  br label %"%12"
"%14":
  %".70" = load i32, i32* %"c", align 4
  %".71" = add i32 %".70", 1
  store i32 %".71", i32* %"c", align 4
  br label %"%3"
"%5":
  %".74" = bitcast [3 x i8]* @".fmt" to i8*
  %".75" = call i32 (i8*, ...) @"printf"(i8* %".74", [33 x i8]* @".str.1")
  store i32 0, i32* %"c", align 4
  br label %"%56"
"%56":
  %".78" = load i32, i32* %"c", align 4
  %".79" = load i32, i32* %"n", align 4
  %".80" = icmp slt i32 %".78", %".79"
  br i1 %".80", label %"%57", label %"%58"
"%57":
  %".82" = load i32, i32* %"c", align 4
  %".83" = sdiv i32 %".82", 0
  %".84" = srem i32 %".82", 0
  %".85" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".83"
  %".86" = getelementptr [0 x i32], [0 x i32]* %".85", i32 0, i32 %".84"
  %".87" = load i32, i32* %".86", align 8
  %".88" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".89" = call i32 (i8*, ...) @"printf"(i8* %".88", i32 %".87")
  %".90" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".91" = call i32 (i8*, ...) @"printf"(i8* %".90", [2 x i8]* @".str.2")
  %".92" = load i32, i32* %"c", align 4
  %".93" = add i32 %".92", 1
  store i32 %".93", i32* %"c", align 4
  br label %"%56"
"%58":
  %".96" = bitcast [2 x i8]* @".fmt.3" to i8*
  %".97" = call i32 (i8*, ...) @"printf"(i8* %".96")
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".100" = load i32, i32* %"1", align 4
  ret i32 %".100"
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.1" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.2" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.3" = internal constant [2 x i8] c"\0a\00", align 1