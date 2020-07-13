; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [10 x i8] c"TajMahal.\00", align 1
@".str.1" = constant [2 x i8] c".\00", align 1
@".str.2" = constant [2 x i8] c"a\00", align 1
@".str.3" = constant [2 x i8] c"e\00", align 1
@".str.4" = constant [2 x i8] c"i\00", align 1
@".str.5" = constant [2 x i8] c"o\00", align 1
@".str.6" = constant [2 x i8] c"u\00", align 1
@".str.7" = constant [23 x i8] c"assertion_fail on 14:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"s" = alloca [9 x i8], align 4
  %"i" = alloca i32, align 4
  %"vowels" = alloca i32, align 4
  %"consonants" = alloca i32, align 4
  %".2" = bitcast [10 x i8]* @".str.0" to i8*
  %".3" = bitcast [9 x i8]* %"s" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 9, i1 false)
  store i32 0, i32* %"i"
  store i32 0, i32* %"vowels"
  store i32 0, i32* %"consonants"
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"i", align 4
  %".10" = add i32 %".9", 1
  store i32 %".10", i32* %"i", align 4
  %".12" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".9"
  %".13" = load i8, i8* %".12", align 8
  %".14" = bitcast [2 x i8]* @".str.1" to i8*
  %".15" = icmp ne i8 %".13", %".14"
  br i1 %".15", label %"%6", label %"%7"
"%6":
  %".17" = load i32, i32* %"i", align 4
  %".18" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".17"
  %".19" = load i8, i8* %".18", align 8
  %".20" = icmp eq i8 %".19", @".str.2"
  %".21" = load i32, i32* %"i", align 4
  %".22" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".21"
  %".23" = load i8, i8* %".22", align 8
  %".24" = icmp eq i8 %".23", @".str.3"
  %".25" = or i1 %".20", %".24"
  %".26" = load i32, i32* %"i", align 4
  %".27" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".26"
  %".28" = load i8, i8* %".27", align 8
  %".29" = icmp eq i8 %".28", @".str.4"
  %".30" = or i1 %".25", %".29"
  %".31" = load i32, i32* %"i", align 4
  %".32" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".31"
  %".33" = load i8, i8* %".32", align 8
  %".34" = icmp eq i8 %".33", @".str.5"
  %".35" = or i1 %".30", %".34"
  %".36" = load i32, i32* %"i", align 4
  %".37" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".36"
  %".38" = load i8, i8* %".37", align 8
  %".39" = icmp eq i8 %".38", @".str.6"
  %".40" = or i1 %".35", %".39"
  br i1 %".40", label %"%14", label %"%15"
"%14":
  %".42" = load i32, i32* %"vowels", align 4
  %".43" = add i32 %".42", 1
  store i32 %".43", i32* %"vowels", align 4
  br label %"%15"
"%15":
  %".46" = load i32, i32* %"consonants", align 4
  %".47" = add i32 %".46", 1
  store i32 %".47", i32* %"consonants", align 4
  br label %"%5"
"%7":
  %".50" = load i32, i32* %"vowels", align 4
  %".51" = icmp eq i32 %".50", 3
  %".52" = load i32, i32* %"consonants", align 4
  %".53" = icmp eq i32 %".52", 5
  %".54" = and i1 %".51", %".53"
  br i1 %".54", label %"%0", label %"%55"
"%55":
  %".56" = bitcast [3 x i8]* @".fmt" to i8*
  %".57" = call i32 (i8*, ...) @"printf"(i8* %".56", [23 x i8]* @".str.7")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1