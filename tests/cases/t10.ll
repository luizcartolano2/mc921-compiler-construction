; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [8 x i8] c"Matrix:\00", align 1
@".str.1" = constant [3 x i8] c"  \00", align 1
@".str.2" = constant [25 x i8] c"Transpose of the matrix:\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"a" = alloca [1 x [0 x i32]], align 4
  %"transpose" = alloca [1 x [0 x i32]], align 4
  %"r" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"i" = alloca i32, align 4
  %"j" = alloca i32, align 4
  store i32 5, i32* %"r", align 4
  store i32 4, i32* %"c", align 4
  store i32 0, i32* %"i", align 4
  br label %"%4"
"%4":
  %".6" = load i32, i32* %"i", align 4
  %".7" = load i32, i32* %"r", align 4
  %".8" = icmp slt i32 %".6", %".7"
  br i1 %".8", label %"%5", label %"%6"
"%5":
  store i32 0, i32* %"j", align 4
  br label %"%11"
"%11":
  %".12" = load i32, i32* %"j", align 4
  %".13" = load i32, i32* %"c", align 4
  %".14" = icmp slt i32 %".12", %".13"
  br i1 %".14", label %"%12", label %"%13"
"%12":
  %".16" = load i32, i32* %"i", align 4
  %".17" = mul i32 %".16", 2
  %".18" = add i32 10, %".17"
  %".19" = load i32, i32* %"j", align 4
  %".20" = add i32 %".18", %".19"
  %".21" = load i32, i32* %"i", align 4
  %".22" = mul i32 10, %".21"
  %".23" = load i32, i32* %"j", align 4
  %".24" = add i32 %".22", %".23"
  %".25" = sdiv i32 %".24", 0
  %".26" = srem i32 %".24", 0
  %".27" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"a", i32 0, i32 %".25"
  %".28" = getelementptr [0 x i32], [0 x i32]* %".27", i32 0, i32 %".26"
  store i32 %".20", i32* %".28", align 4
  %".30" = load i32, i32* %"j", align 4
  %".31" = add i32 %".30", 1
  store i32 %".31", i32* %"j", align 4
  br label %"%11"
"%13":
  %".34" = load i32, i32* %"i", align 4
  %".35" = add i32 %".34", 1
  store i32 %".35", i32* %"i", align 4
  br label %"%4"
"%6":
  %".38" = bitcast [3 x i8]* @".fmt" to i8*
  %".39" = call i32 (i8*, ...) @"printf"(i8* %".38", [8 x i8]* @".str.0")
  %".40" = bitcast [2 x i8]* @".fmt.1" to i8*
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".40")
  store i32 0, i32* %"i", align 4
  br label %"%37"
"%37":
  %".44" = load i32, i32* %"i", align 4
  %".45" = load i32, i32* %"r", align 4
  %".46" = icmp slt i32 %".44", %".45"
  br i1 %".46", label %"%38", label %"%39"
"%38":
  store i32 0, i32* %"j", align 4
  br label %"%44"
"%44":
  %".50" = load i32, i32* %"j", align 4
  %".51" = load i32, i32* %"c", align 4
  %".52" = icmp slt i32 %".50", %".51"
  br i1 %".52", label %"%45", label %"%46"
"%45":
  %".54" = load i32, i32* %"i", align 4
  %".55" = mul i32 10, %".54"
  %".56" = load i32, i32* %"j", align 4
  %".57" = add i32 %".55", %".56"
  %".58" = sdiv i32 %".57", 0
  %".59" = srem i32 %".57", 0
  %".60" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"a", i32 0, i32 %".58"
  %".61" = getelementptr [0 x i32], [0 x i32]* %".60", i32 0, i32 %".59"
  %".62" = load i32, i32* %".61", align 8
  %".63" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".64" = call i32 (i8*, ...) @"printf"(i8* %".63", i32 %".62")
  %".65" = bitcast [3 x i8]* @".fmt.3" to i8*
  %".66" = call i32 (i8*, ...) @"printf"(i8* %".65", [3 x i8]* @".str.1")
  %".67" = load i32, i32* %"c", align 4
  %".68" = sub i32 %".67", 1
  %".69" = load i32, i32* %"j", align 4
  %".70" = icmp eq i32 %".69", %".68"
  br i1 %".70", label %"%58", label %"%59"
"%58":
  %".72" = bitcast [2 x i8]* @".fmt.4" to i8*
  %".73" = call i32 (i8*, ...) @"printf"(i8* %".72")
  br label %"%59"
"%59":
  %".75" = load i32, i32* %"j", align 4
  %".76" = add i32 %".75", 1
  store i32 %".76", i32* %"j", align 4
  br label %"%44"
"%46":
  %".79" = load i32, i32* %"i", align 4
  %".80" = add i32 %".79", 1
  store i32 %".80", i32* %"i", align 4
  br label %"%37"
"%39":
  store i32 0, i32* %"i", align 4
  br label %"%72"
"%72":
  %".85" = load i32, i32* %"i", align 4
  %".86" = load i32, i32* %"r", align 4
  %".87" = icmp slt i32 %".85", %".86"
  br i1 %".87", label %"%73", label %"%74"
"%73":
  store i32 0, i32* %"j", align 4
  br label %"%79"
"%79":
  %".91" = load i32, i32* %"j", align 4
  %".92" = load i32, i32* %"c", align 4
  %".93" = icmp slt i32 %".91", %".92"
  br i1 %".93", label %"%80", label %"%81"
"%80":
  %".95" = load i32, i32* %"i", align 4
  %".96" = mul i32 10, %".95"
  %".97" = load i32, i32* %"j", align 4
  %".98" = add i32 %".96", %".97"
  %".99" = sdiv i32 %".98", 0
  %".100" = srem i32 %".98", 0
  %".101" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"a", i32 0, i32 %".99"
  %".102" = getelementptr [0 x i32], [0 x i32]* %".101", i32 0, i32 %".100"
  %".103" = load i32, i32* %".102", align 8
  %".104" = load i32, i32* %"j", align 4
  %".105" = mul i32 10, %".104"
  %".106" = load i32, i32* %"i", align 4
  %".107" = add i32 %".105", %".106"
  %".108" = sdiv i32 %".107", 0
  %".109" = srem i32 %".107", 0
  %".110" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"transpose", i32 0, i32 %".108"
  %".111" = getelementptr [0 x i32], [0 x i32]* %".110", i32 0, i32 %".109"
  store i32 %".103", i32* %".111", align 4
  %".113" = load i32, i32* %"j", align 4
  %".114" = add i32 %".113", 1
  store i32 %".114", i32* %"j", align 4
  br label %"%79"
"%81":
  %".117" = load i32, i32* %"i", align 4
  %".118" = add i32 %".117", 1
  store i32 %".118", i32* %"i", align 4
  br label %"%72"
"%74":
  %".121" = bitcast [3 x i8]* @".fmt.5" to i8*
  %".122" = call i32 (i8*, ...) @"printf"(i8* %".121", [25 x i8]* @".str.2")
  %".123" = bitcast [2 x i8]* @".fmt.6" to i8*
  %".124" = call i32 (i8*, ...) @"printf"(i8* %".123")
  store i32 0, i32* %"i", align 4
  br label %"%105"
"%105":
  %".127" = load i32, i32* %"i", align 4
  %".128" = load i32, i32* %"c", align 4
  %".129" = icmp slt i32 %".127", %".128"
  br i1 %".129", label %"%106", label %"%107"
"%106":
  store i32 0, i32* %"j", align 4
  br label %"%112"
"%112":
  %".133" = load i32, i32* %"j", align 4
  %".134" = load i32, i32* %"r", align 4
  %".135" = icmp slt i32 %".133", %".134"
  br i1 %".135", label %"%113", label %"%114"
"%113":
  %".137" = load i32, i32* %"i", align 4
  %".138" = mul i32 10, %".137"
  %".139" = load i32, i32* %"j", align 4
  %".140" = add i32 %".138", %".139"
  %".141" = sdiv i32 %".140", 0
  %".142" = srem i32 %".140", 0
  %".143" = getelementptr [1 x [0 x i32]], [1 x [0 x i32]]* %"transpose", i32 0, i32 %".141"
  %".144" = getelementptr [0 x i32], [0 x i32]* %".143", i32 0, i32 %".142"
  %".145" = load i32, i32* %".144", align 8
  %".146" = bitcast [3 x i8]* @".fmt.7" to i8*
  %".147" = call i32 (i8*, ...) @"printf"(i8* %".146", i32 %".145")
  %".148" = bitcast [3 x i8]* @".fmt.8" to i8*
  %".149" = call i32 (i8*, ...) @"printf"(i8* %".148", [3 x i8]* @".str.1")
  %".150" = load i32, i32* %"r", align 4
  %".151" = sub i32 %".150", 1
  %".152" = load i32, i32* %"j", align 4
  %".153" = icmp eq i32 %".152", %".151"
  br i1 %".153", label %"%126", label %"%127"
"%126":
  %".155" = bitcast [2 x i8]* @".fmt.9" to i8*
  %".156" = call i32 (i8*, ...) @"printf"(i8* %".155")
  br label %"%127"
"%127":
  %".158" = load i32, i32* %"j", align 4
  %".159" = add i32 %".158", 1
  store i32 %".159", i32* %"j", align 4
  br label %"%112"
"%114":
  %".162" = load i32, i32* %"i", align 4
  %".163" = add i32 %".162", 1
  store i32 %".163", i32* %"i", align 4
  br label %"%105"
"%107":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".168" = load i32, i32* %"1", align 4
  ret i32 %".168"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.1" = internal constant [2 x i8] c"\0a\00", align 1
@".fmt.2" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.3" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.4" = internal constant [2 x i8] c"\0a\00", align 1
@".fmt.5" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.6" = internal constant [2 x i8] c"\0a\00", align 1
@".fmt.7" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.8" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.9" = internal constant [2 x i8] c"\0a\00", align 1