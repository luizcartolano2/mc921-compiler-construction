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
  %"a" = alloca [10 x [10 x i32]], align 16
  %"transpose" = alloca [10 x [10 x i32]], align 16
  %"i" = alloca i32, align 4
  %"j" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"%4"
"%4":
  %".4" = load i32, i32* %"i", align 4
  %".5" = icmp slt i32 %".4", 5
  br i1 %".5", label %"%5", label %"%6"
"%5":
  store i32 0, i32* %"j"
  br label %"%11"
"%11":
  %".9" = load i32, i32* %"j", align 4
  %".10" = icmp slt i32 %".9", 4
  br i1 %".10", label %"%12", label %"%13"
"%12":
  %".12" = load i32, i32* %"i", align 4
  %".13" = mul i32 %".12", 2
  %".14" = add i32 10, %".13"
  %".15" = load i32, i32* %"j", align 4
  %".16" = add i32 %".14", %".15"
  %".17" = load i32, i32* %"i", align 4
  %".18" = mul i32 10, %".17"
  %".19" = load i32, i32* %"j", align 4
  %".20" = add i32 %".18", %".19"
  %".21" = sdiv i32 %".20", 10
  %".22" = srem i32 %".20", 10
  %".23" = getelementptr [10 x [10 x i32]], [10 x [10 x i32]]* %"a", i32 0, i32 %".21"
  %".24" = getelementptr [10 x i32], [10 x i32]* %".23", i32 0, i32 %".22"
  store i32 %".16", i32* %".24", align 4
  %".26" = load i32, i32* %"j", align 4
  %".27" = add i32 %".26", 1
  store i32 %".27", i32* %"j", align 4
  br label %"%11"
"%13":
  %".30" = load i32, i32* %"i", align 4
  %".31" = add i32 %".30", 1
  store i32 %".31", i32* %"i", align 4
  br label %"%4"
"%6":
  %".34" = bitcast [3 x i8]* @".fmt" to i8*
  %".35" = call i32 (i8*, ...) @"printf"(i8* %".34", [8 x i8]* @".str.0")
  %".36" = bitcast [2 x i8]* @".fmt.1" to i8*
  %".37" = call i32 (i8*, ...) @"printf"(i8* %".36")
  store i32 0, i32* %"i"
  br label %"%37"
"%37":
  %".40" = load i32, i32* %"i", align 4
  %".41" = icmp slt i32 %".40", 5
  br i1 %".41", label %"%38", label %"%39"
"%38":
  store i32 0, i32* %"j"
  br label %"%44"
"%44":
  %".45" = load i32, i32* %"j", align 4
  %".46" = icmp slt i32 %".45", 4
  br i1 %".46", label %"%45", label %"%46"
"%45":
  %".48" = load i32, i32* %"i", align 4
  %".49" = mul i32 10, %".48"
  %".50" = load i32, i32* %"j", align 4
  %".51" = add i32 %".49", %".50"
  %".52" = sdiv i32 %".51", 10
  %".53" = srem i32 %".51", 10
  %".54" = getelementptr [10 x [10 x i32]], [10 x [10 x i32]]* %"a", i32 0, i32 %".52"
  %".55" = getelementptr [10 x i32], [10 x i32]* %".54", i32 0, i32 %".53"
  %".56" = load i32, i32* %".55", align 8
  %".57" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".58" = call i32 (i8*, ...) @"printf"(i8* %".57", i32 %".56")
  %".59" = bitcast [3 x i8]* @".fmt.3" to i8*
  %".60" = call i32 (i8*, ...) @"printf"(i8* %".59", [3 x i8]* @".str.1")
  %".61" = load i32, i32* %"j", align 4
  %".62" = icmp eq i32 %".61", 3
  br i1 %".62", label %"%58", label %"%59"
"%58":
  %".64" = bitcast [2 x i8]* @".fmt.4" to i8*
  %".65" = call i32 (i8*, ...) @"printf"(i8* %".64")
  br label %"%59"
"%59":
  %".67" = load i32, i32* %"j", align 4
  %".68" = add i32 %".67", 1
  store i32 %".68", i32* %"j", align 4
  br label %"%44"
"%46":
  %".71" = load i32, i32* %"i", align 4
  %".72" = add i32 %".71", 1
  store i32 %".72", i32* %"i", align 4
  br label %"%37"
"%39":
  store i32 0, i32* %"i"
  br label %"%72"
"%72":
  %".77" = load i32, i32* %"i", align 4
  %".78" = icmp slt i32 %".77", 5
  br i1 %".78", label %"%73", label %"%74"
"%73":
  store i32 0, i32* %"j"
  br label %"%79"
"%79":
  %".82" = load i32, i32* %"j", align 4
  %".83" = icmp slt i32 %".82", 4
  br i1 %".83", label %"%80", label %"%81"
"%80":
  %".85" = load i32, i32* %"i", align 4
  %".86" = mul i32 10, %".85"
  %".87" = load i32, i32* %"j", align 4
  %".88" = add i32 %".86", %".87"
  %".89" = sdiv i32 %".88", 10
  %".90" = srem i32 %".88", 10
  %".91" = getelementptr [10 x [10 x i32]], [10 x [10 x i32]]* %"a", i32 0, i32 %".89"
  %".92" = getelementptr [10 x i32], [10 x i32]* %".91", i32 0, i32 %".90"
  %".93" = load i32, i32* %".92", align 8
  %".94" = load i32, i32* %"j", align 4
  %".95" = mul i32 10, %".94"
  %".96" = load i32, i32* %"i", align 4
  %".97" = add i32 %".95", %".96"
  %".98" = sdiv i32 %".97", 10
  %".99" = srem i32 %".97", 10
  %".100" = getelementptr [10 x [10 x i32]], [10 x [10 x i32]]* %"transpose", i32 0, i32 %".98"
  %".101" = getelementptr [10 x i32], [10 x i32]* %".100", i32 0, i32 %".99"
  store i32 %".93", i32* %".101", align 4
  %".103" = load i32, i32* %"j", align 4
  %".104" = add i32 %".103", 1
  store i32 %".104", i32* %"j", align 4
  br label %"%79"
"%81":
  %".107" = load i32, i32* %"i", align 4
  %".108" = add i32 %".107", 1
  store i32 %".108", i32* %"i", align 4
  br label %"%72"
"%74":
  %".111" = bitcast [3 x i8]* @".fmt.5" to i8*
  %".112" = call i32 (i8*, ...) @"printf"(i8* %".111", [25 x i8]* @".str.2")
  %".113" = bitcast [2 x i8]* @".fmt.6" to i8*
  %".114" = call i32 (i8*, ...) @"printf"(i8* %".113")
  store i32 0, i32* %"i"
  br label %"%105"
"%105":
  %".117" = load i32, i32* %"i", align 4
  %".118" = icmp slt i32 %".117", 4
  br i1 %".118", label %"%106", label %"%0"
"%106":
  store i32 0, i32* %"j"
  br label %"%112"
"%112":
  %".122" = load i32, i32* %"j", align 4
  %".123" = icmp slt i32 %".122", 5
  br i1 %".123", label %"%113", label %"%114"
"%113":
  %".125" = load i32, i32* %"i", align 4
  %".126" = mul i32 10, %".125"
  %".127" = load i32, i32* %"j", align 4
  %".128" = add i32 %".126", %".127"
  %".129" = sdiv i32 %".128", 10
  %".130" = srem i32 %".128", 10
  %".131" = getelementptr [10 x [10 x i32]], [10 x [10 x i32]]* %"transpose", i32 0, i32 %".129"
  %".132" = getelementptr [10 x i32], [10 x i32]* %".131", i32 0, i32 %".130"
  %".133" = load i32, i32* %".132", align 8
  %".134" = bitcast [3 x i8]* @".fmt.7" to i8*
  %".135" = call i32 (i8*, ...) @"printf"(i8* %".134", i32 %".133")
  %".136" = bitcast [3 x i8]* @".fmt.8" to i8*
  %".137" = call i32 (i8*, ...) @"printf"(i8* %".136", [3 x i8]* @".str.1")
  %".138" = load i32, i32* %"j", align 4
  %".139" = icmp eq i32 %".138", 4
  br i1 %".139", label %"%126", label %"%127"
"%126":
  %".141" = bitcast [2 x i8]* @".fmt.9" to i8*
  %".142" = call i32 (i8*, ...) @"printf"(i8* %".141")
  br label %"%127"
"%127":
  %".144" = load i32, i32* %"j", align 4
  %".145" = add i32 %".144", 1
  store i32 %".145", i32* %"j", align 4
  br label %"%112"
"%114":
  %".148" = load i32, i32* %"i", align 4
  %".149" = add i32 %".148", 1
  store i32 %".149", i32* %"i", align 4
  br label %"%105"
"%0":
  ret i32 0
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