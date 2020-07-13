; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = global [10 x i32] [i32 5, i32 3, i32 7, i32 8, i32 4, i32 1, i32 9, i32 2, i32 0, i32 6], align 16
@".str.1" = constant [33 x i8] c"Sorted list in ascending order: \00", align 1
@".str.2" = constant [2 x i8] c" \00", align 1
@".str.3" = constant [23 x i8] c"assertion_fail on 18:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"v" = alloca [10 x i32], align 16
  %"c" = alloca i32, align 4
  %"d" = alloca i32, align 4
  %"swap" = alloca i32, align 4
  %".2" = bitcast [10 x i32]* @".str.0" to i8*
  %".3" = bitcast [10 x i32]* %"v" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 40, i1 false)
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
  %".19" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".18"
  %".20" = load i32, i32* %"d", align 4
  %".21" = add i32 %".20", 1
  %".22" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".21"
  %".23" = load i32, i32* %".19", align 8
  %".24" = load i32, i32* %".22", align 8
  %".25" = icmp sgt i32 %".23", %".24"
  br i1 %".25", label %"%23", label %"%24"
"%23":
  %".27" = load i32, i32* %"d", align 4
  %".28" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".27"
  %".29" = load i32, i32* %".28", align 8
  store i32 %".29", i32* %"swap", align 4
  %".31" = load i32, i32* %"d", align 4
  %".32" = add i32 %".31", 1
  %".33" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".32"
  %".34" = load i32, i32* %".33", align 8
  %".35" = load i32, i32* %"d", align 4
  %".36" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".35"
  store i32 %".34", i32* %".36", align 4
  %".38" = load i32, i32* %"swap", align 4
  %".39" = load i32, i32* %"d", align 4
  %".40" = add i32 %".39", 1
  %".41" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".40"
  store i32 %".38", i32* %".41", align 4
  br label %"%24"
"%24":
  %".44" = load i32, i32* %"d", align 4
  %".45" = add i32 %".44", 1
  store i32 %".45", i32* %"d", align 4
  br label %"%12"
"%14":
  %".48" = load i32, i32* %"c", align 4
  %".49" = add i32 %".48", 1
  store i32 %".49", i32* %"c", align 4
  br label %"%3"
"%5":
  %".52" = bitcast [3 x i8]* @".fmt" to i8*
  %".53" = call i32 (i8*, ...) @"printf"(i8* %".52", [33 x i8]* @".str.1")
  store i32 0, i32* %"c"
  br label %"%56"
"%56":
  %".56" = load i32, i32* %"c", align 4
  %".57" = icmp slt i32 %".56", 10
  br i1 %".57", label %"%57", label %"%58"
"%57":
  %".59" = load i32, i32* %"c", align 4
  %".60" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 %".59"
  %".61" = load i32, i32* %".60", align 8
  %".62" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".63" = call i32 (i8*, ...) @"printf"(i8* %".62", i32 %".61")
  %".64" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".65" = call i32 (i8*, ...) @"printf"(i8* %".64", [2 x i8]* @".str.2")
  %".66" = load i32, i32* %"c", align 4
  %".67" = add i32 %".66", 1
  store i32 %".67", i32* %"c", align 4
  br label %"%56"
"%58":
  %".70" = bitcast [2 x i8]* @".fmt.3" to i8*
  %".71" = call i32 (i8*, ...) @"printf"(i8* %".70")
  %".72" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 0
  %".73" = load i32, i32* %".72", align 8
  %".74" = icmp eq i32 %".73", 0
  %".75" = getelementptr [10 x i32], [10 x i32]* %"v", i32 0, i32 9
  %".76" = load i32, i32* %".75", align 8
  %".77" = icmp eq i32 %".76", 9
  %".78" = and i1 %".74", %".77"
  br i1 %".78", label %"%0", label %"%81"
"%81":
  %".80" = bitcast [3 x i8]* @".fmt.4" to i8*
  %".81" = call i32 (i8*, ...) @"printf"(i8* %".80", [23 x i8]* @".str.3")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.1" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.2" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.3" = internal constant [2 x i8] c"\0a\00", align 1
@".fmt.4" = internal constant [3 x i8] c"%s\00", align 1