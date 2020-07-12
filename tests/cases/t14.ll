; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 10:5\00", align 1
@".str.1" = constant [23 x i8] c"assertion_fail on 11:5\00", align 1
@".str.2" = constant [23 x i8] c"assertion_fail on 12:5\00", align 1
@".str.3" = constant [23 x i8] c"assertion_fail on 13:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"n1" = alloca i32, align 4
  %"n2" = alloca i32, align 4
  %"n3" = alloca i32, align 4
  store i32 407, i32* %"n1", align 4
  store i32 1634, i32* %"n2", align 4
  store i32 8207, i32* %"n3", align 4
  %".5" = load i32, i32* %"n1", align 4
  %".6" = call i32 @"armstrong"(i32 %".5")
  %".7" = icmp eq i32 %".6", 1
  br i1 %".7", label %"%9", label %"%10"
"%9":
  br label %"%11"
"%10":
  %".10" = bitcast [3 x i8]* @".fmt" to i8*
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", [23 x i8]* @".str.0")
  br label %"%0"
"%11":
  %".13" = load i32, i32* %"n2", align 4
  %".14" = call i32 @"armstrong"(i32 %".13")
  %".15" = icmp eq i32 %".14", 1
  br i1 %".15", label %"%16", label %"%17"
"%16":
  br label %"%18"
"%17":
  %".18" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", [23 x i8]* @".str.1")
  br label %"%0"
"%18":
  %".21" = load i32, i32* %"n3", align 4
  %".22" = call i32 @"armstrong"(i32 %".21")
  %".23" = icmp eq i32 %".22", 0
  br i1 %".23", label %"%23", label %"%24"
"%23":
  br label %"%25"
"%24":
  %".26" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26", [23 x i8]* @".str.2")
  br label %"%0"
"%25":
  %".29" = call i32 @"armstrong"(i32 153)
  %".30" = icmp eq i32 %".29", 1
  br i1 %".30", label %"%30", label %"%31"
"%30":
  br label %"%32"
"%31":
  %".33" = bitcast [3 x i8]* @".fmt.3" to i8*
  %".34" = call i32 (i8*, ...) @"printf"(i8* %".33", [23 x i8]* @".str.3")
  br label %"%0"
"%32":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".38" = load i32, i32* %"1", align 4
  ret i32 %".38"
}

define i32 @"armstrong"(i32 %".1") 
{
"%entry":
  %"2" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"temp" = alloca i32, align 4
  %"remainder" = alloca i32, align 4
  %"sum" = alloca i32, align 4
  %"digits" = alloca i32, align 4
  store i32 %".1", i32* %"n", align 4
  store i32 0, i32* %"sum", align 4
  store i32 0, i32* %"digits", align 4
  %".6" = load i32, i32* %"n", align 4
  store i32 %".6", i32* %"temp", align 4
  br label %"%6"
"%6":
  %".9" = load i32, i32* %"temp", align 4
  %".10" = icmp ne i32 %".9", 0
  br i1 %".10", label %"%7", label %"%8"
"%7":
  %".12" = load i32, i32* %"digits", align 4
  %".13" = add i32 1, %".12"
  store i32 %".13", i32* %"digits", align 4
  %".15" = load i32, i32* %"temp", align 4
  %".16" = sdiv i32 %".15", 10
  store i32 %".16", i32* %"temp", align 4
  br label %"%6"
"%8":
  %".19" = load i32, i32* %"n", align 4
  store i32 %".19", i32* %"temp", align 4
  br label %"%19"
"%19":
  %".22" = load i32, i32* %"temp", align 4
  %".23" = icmp ne i32 %".22", 0
  br i1 %".23", label %"%20", label %"%21"
"%20":
  %".25" = load i32, i32* %"temp", align 4
  %".26" = srem i32 %".25", 10
  store i32 %".26", i32* %"remainder", align 4
  %".28" = load i32, i32* %"remainder", align 4
  %".29" = load i32, i32* %"digits", align 4
  %".30" = call i32 @"power"(i32 %".28", i32 %".29")
  %".31" = load i32, i32* %"sum", align 4
  %".32" = add i32 %".31", %".30"
  store i32 %".32", i32* %"sum", align 4
  %".34" = load i32, i32* %"temp", align 4
  %".35" = sdiv i32 %".34", 10
  store i32 %".35", i32* %"temp", align 4
  br label %"%19"
"%21":
  %".38" = load i32, i32* %"n", align 4
  %".39" = load i32, i32* %"sum", align 4
  %".40" = icmp eq i32 %".38", %".39"
  br i1 %".40", label %"%36", label %"%37"
"%36":
  store i32 1, i32* %"2", align 4
  br label %"%1"
"%37":
  store i32 0, i32* %"2", align 4
  br label %"%1"
"%38":
  br label %"%1"
"%1":
  %".47" = load i32, i32* %"2", align 4
  ret i32 %".47"
}

@".fmt" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.1" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.2" = internal constant [3 x i8] c"%s\00", align 1
@".fmt.3" = internal constant [3 x i8] c"%s\00", align 1
define i32 @"power"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32, align 4
  %"n" = alloca i32, align 4
  %"r" = alloca i32, align 4
  %"p" = alloca i32, align 4
  %"c" = alloca i32, align 4
  store i32 %".1", i32* %"n", align 4
  store i32 %".2", i32* %"r", align 4
  store i32 1, i32* %"p", align 4
  store i32 1, i32* %"c", align 4
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"c", align 4
  %".10" = load i32, i32* %"r", align 4
  %".11" = icmp sle i32 %".9", %".10"
  br i1 %".11", label %"%6", label %"%7"
"%6":
  %".13" = load i32, i32* %"p", align 4
  %".14" = load i32, i32* %"n", align 4
  %".15" = mul i32 %".13", %".14"
  store i32 %".15", i32* %"p", align 4
  %".17" = load i32, i32* %"c", align 4
  %".18" = add i32 %".17", 1
  store i32 %".18", i32* %"c", align 4
  br label %"%5"
"%7":
  %".21" = load i32, i32* %"p", align 4
  store i32 %".21", i32* %"3", align 4
  br label %"%2"
"%2":
  %".24" = load i32, i32* %"3", align 4
  ret i32 %".24"
}
