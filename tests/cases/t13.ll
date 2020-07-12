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
  %"v" = alloca [1 x [0 x i32]], align 4
  %"c" = alloca i32, align 4
  %"d" = alloca i32, align 4
  %"swap" = alloca i32, align 4
  %".2" = bitcast [10 x i32]* @".str.0" to i8*
  %".3" = bitcast [1 x [0 x i32]]* %"v" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 0, i1 false)
  store i32 0, i32* %"c"
  br label %"%3"
"%3":
  %".7" = load i32, i32* %"c", align 4
  %".8" = icmp slt i32 %".7", 9
  br i1 %".8", label %"%4", label %"%5"
"%4":
  store i32 0, i32* %"d"
  br label %"%12"
"%12":
  %".12" = load i32, i32* %"c", align 4
  %".13" = sub i32 10, %".12"
  %".14" = sub i32 %".13", 1
  %".15" = load i32, i32* %"d", align 4
  %".16" = icmp slt i32 %".15", %".14"
  br i1 %".16", label %"%13", label %"%14"
"%13":
  %".18" = load i32, i32* %"d", align 4
  %".19" = sdiv i32 %".18", 0
  %".20" = srem i32 %".18", 0
  %".21" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".19"
  %".22" = getelementptr [0 x i32], [0 x i32]* %".21", i32 0, i32 %".20"
  %".23" = load i32, i32* %"d", align 4
  %".24" = add i32 %".23", 1
  %".25" = sdiv i32 %".24", 0
  %".26" = srem i32 %".24", 0
  %".27" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".25"
  %".28" = getelementptr [0 x i32], [0 x i32]* %".27", i32 0, i32 %".26"
  %".29" = load i32, i32* %".22", align 8
  %".30" = load i32, i32* %".28", align 8
  %".31" = icmp sgt i32 %".29", %".30"
  br i1 %".31", label %"%23", label %"%24"
"%23":
  %".33" = load i32, i32* %"d", align 4
  %".34" = sdiv i32 %".33", 0
  %".35" = srem i32 %".33", 0
  %".36" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".34"
  %".37" = getelementptr [0 x i32], [0 x i32]* %".36", i32 0, i32 %".35"
  %".38" = load i32, i32* %".37", align 8
  store i32 %".38", i32* %"swap", align 4
  %".40" = load i32, i32* %"d", align 4
  %".41" = add i32 %".40", 1
  %".42" = sdiv i32 %".41", 0
  %".43" = srem i32 %".41", 0
  %".44" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".42"
  %".45" = getelementptr [0 x i32], [0 x i32]* %".44", i32 0, i32 %".43"
  %".46" = load i32, i32* %".45", align 8
  %".47" = load i32, i32* %"d", align 4
  %".48" = sdiv i32 %".47", 0
  %".49" = srem i32 %".47", 0
  %".50" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".48"
  %".51" = getelementptr [0 x i32], [0 x i32]* %".50", i32 0, i32 %".49"
  store i32 %".46", i32* %".51", align 4
  %".53" = load i32, i32* %"swap", align 4
  %".54" = load i32, i32* %"d", align 4
  %".55" = add i32 %".54", 1
  %".56" = sdiv i32 %".55", 0
  %".57" = srem i32 %".55", 0
  %".58" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".56"
  %".59" = getelementptr [0 x i32], [0 x i32]* %".58", i32 0, i32 %".57"
  store i32 %".53", i32* %".59", align 4
  br label %"%24"
"%24":
  %".62" = load i32, i32* %"d", align 4
  %".63" = add i32 %".62", 1
  store i32 %".63", i32* %"d", align 4
  br label %"%12"
"%14":
  %".66" = load i32, i32* %"c", align 4
  %".67" = add i32 %".66", 1
  store i32 %".67", i32* %"c", align 4
  br label %"%3"
"%5":
  %".70" = bitcast [3 x i8]* @".fmt" to i8*
  %".71" = call i32 (i8*, ...) @"printf"(i8* %".70", [33 x i8]* @".str.1")
  store i32 0, i32* %"c"
  br label %"%56"
"%56":
  %".74" = load i32, i32* %"c", align 4
  %".75" = icmp slt i32 %".74", 10
  br i1 %".75", label %"%57", label %"%58"
"%57":
  %".77" = load i32, i32* %"c", align 4
  %".78" = sdiv i32 %".77", 0
  %".79" = srem i32 %".77", 0
  %".80" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"v", i32 0, i32 %".78"
  %".81" = getelementptr [0 x i32], [0 x i32]* %".80", i32 0, i32 %".79"
  %".82" = load i32, i32* %".81", align 8
  %".83" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".84" = call i32 (i8*, ...) @"printf"(i8* %".83", i32 %".82")
  %".85" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".86" = call i32 (i8*, ...) @"printf"(i8* %".85", [2 x i8]* @".str.2")
  %".87" = load i32, i32* %"c", align 4
  %".88" = add i32 %".87", 1
  store i32 %".88", i32* %"c", align 4
  br label %"%56"
"%58":
  %".91" = bitcast [2 x i8]* @".fmt.3" to i8*
  %".92" = call i32 (i8*, ...) @"printf"(i8* %".91")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.1" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.2" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.3" = internal constant [2 x i8] c"\0a\00", align 1