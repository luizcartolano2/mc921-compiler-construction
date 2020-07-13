; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [23 x i8] c"assertion_fail on 10:5\00"
@".str.1" = constant [23 x i8] c"assertion_fail on 11:5\00"
@".str.2" = constant [23 x i8] c"assertion_fail on 12:5\00"
@".str.3" = constant [23 x i8] c"assertion_fail on 13:5\00"
define i32 @"main"() 
{
"%entry":
  %".2" = call i32 @"armstrong"(i32 407)
  %".3" = icmp eq i32 %".2", 1
  br i1 %".3", label %"%11", label %"%10"
"%10":
  %".5" = bitcast [3 x i8]* @".fmt" to i8*
  %".6" = call i32 (i8*, ...) @"printf"(i8* %".5", [23 x i8]* @".str.0")
  br label %"%0"
"%11":
  %".8" = call i32 @"armstrong"(i32 1634)
  %".9" = icmp eq i32 %".8", 1
  br i1 %".9", label %"%18", label %"%17"
"%17":
  %".11" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".12" = call i32 (i8*, ...) @"printf"(i8* %".11", [23 x i8]* @".str.1")
  br label %"%0"
"%18":
  %".14" = call i32 @"armstrong"(i32 8207)
  %".15" = icmp eq i32 %".14", 0
  br i1 %".15", label %"%25", label %"%24"
"%24":
  %".17" = bitcast [3 x i8]* @".fmt.2" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17", [23 x i8]* @".str.2")
  br label %"%0"
"%25":
  %".20" = call i32 @"armstrong"(i32 153)
  %".21" = icmp eq i32 %".20", 1
  br i1 %".21", label %"%0", label %"%31"
"%31":
  %".23" = bitcast [3 x i8]* @".fmt.3" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23", [23 x i8]* @".str.3")
  br label %"%0"
"%0":
  ret i32 0
}

define i32 @"armstrong"(i32 %".1") 
{
"%entry":
  %"2" = alloca i32
  %"n" = alloca i32
  %"temp" = alloca i32
  %"remainder" = alloca i32
  %"sum" = alloca i32
  %"digits" = alloca i32
  store i32 %".1", i32* %"n"
  store i32 0, i32* %"sum"
  store i32 0, i32* %"digits"
  %".6" = load i32, i32* %"n"
  store i32 %".6", i32* %"temp"
  br label %"%6"
"%6":
  %".9" = load i32, i32* %"temp"
  %".10" = icmp ne i32 %".9", 0
  br i1 %".10", label %"%7", label %"%8"
"%7":
  %".12" = load i32, i32* %"digits"
  %".13" = add i32 1, %".12"
  store i32 %".13", i32* %"digits"
  %".15" = load i32, i32* %"temp"
  %".16" = sdiv i32 %".15", 10
  store i32 %".16", i32* %"temp"
  br label %"%6"
"%8":
  %".19" = load i32, i32* %"n"
  store i32 %".19", i32* %"temp"
  br label %"%19"
"%19":
  %".22" = load i32, i32* %"temp"
  %".23" = icmp ne i32 %".22", 0
  br i1 %".23", label %"%20", label %"%21"
"%20":
  %".25" = load i32, i32* %"temp"
  %".26" = srem i32 %".25", 10
  store i32 %".26", i32* %"remainder"
  %".28" = load i32, i32* %"remainder"
  %".29" = load i32, i32* %"digits"
  %".30" = call i32 @"power"(i32 %".28", i32 %".29")
  %".31" = load i32, i32* %"sum"
  %".32" = add i32 %".31", %".30"
  store i32 %".32", i32* %"sum"
  %".34" = load i32, i32* %"temp"
  %".35" = sdiv i32 %".34", 10
  store i32 %".35", i32* %"temp"
  br label %"%19"
"%21":
  %".38" = load i32, i32* %"n"
  %".39" = load i32, i32* %"sum"
  %".40" = icmp eq i32 %".38", %".39"
  br i1 %".40", label %"%36", label %"%37"
"%36":
  store i32 1, i32* %"2"
  br label %"%1"
"%37":
  store i32 0, i32* %"2"
  br label %"%1"
"%1":
  %".46" = load i32, i32* %"2"
  ret i32 %".46"
}

@".fmt" = internal constant [3 x i8] c"%s\00"
@".fmt.1" = internal constant [3 x i8] c"%s\00"
@".fmt.2" = internal constant [3 x i8] c"%s\00"
@".fmt.3" = internal constant [3 x i8] c"%s\00"
define i32 @"power"(i32 %".1", i32 %".2") 
{
"%entry":
  %"3" = alloca i32
  %"n" = alloca i32
  %"r" = alloca i32
  %"p" = alloca i32
  %"c" = alloca i32
  store i32 %".1", i32* %"n"
  store i32 %".2", i32* %"r"
  store i32 1, i32* %"p"
  store i32 1, i32* %"c"
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"c"
  %".10" = load i32, i32* %"r"
  %".11" = icmp sle i32 %".9", %".10"
  br i1 %".11", label %"%6", label %"%7"
"%6":
  %".13" = load i32, i32* %"p"
  %".14" = load i32, i32* %"n"
  %".15" = mul i32 %".13", %".14"
  store i32 %".15", i32* %"p"
  %".17" = load i32, i32* %"c"
  %".18" = add i32 %".17", 1
  store i32 %".18", i32* %"c"
  br label %"%5"
"%7":
  %".21" = load i32, i32* %"p"
  store i32 %".21", i32* %"3"
  br label %"%2"
"%2":
  %".24" = load i32, i32* %"3"
  ret i32 %".24"
}
