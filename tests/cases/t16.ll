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
  %".14" = fcmp one i8 %".13", @".str.1"
  br i1 %".14", label %"%6", label %"%7"
"%6":
  %".16" = load i32, i32* %"i", align 4
  %".17" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".16"
  %".18" = load i8, i8* %".17", align 8
  %".19" = icmp eq i8 %".18", @".str.2"
  %".20" = load i32, i32* %"i", align 4
  %".21" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".20"
  %".22" = load i8, i8* %".21", align 8
  %".23" = icmp eq i8 %".22", @".str.3"
  %".24" = or i1 %".19", %".23"
  %".25" = load i32, i32* %"i", align 4
  %".26" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".25"
  %".27" = load i8, i8* %".26", align 8
  %".28" = icmp eq i8 %".27", @".str.4"
  %".29" = or i1 %".24", %".28"
  %".30" = load i32, i32* %"i", align 4
  %".31" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".30"
  %".32" = load i8, i8* %".31", align 8
  %".33" = icmp eq i8 %".32", @".str.5"
  %".34" = or i1 %".29", %".33"
  %".35" = load i32, i32* %"i", align 4
  %".36" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".35"
  %".37" = load i8, i8* %".36", align 8
  %".38" = icmp eq i8 %".37", @".str.6"
  %".39" = or i1 %".34", %".38"
  br i1 %".39", label %"%14", label %"%15"
"%14":
  %".41" = load i32, i32* %"vowels", align 4
  %".42" = add i32 %".41", 1
  store i32 %".42", i32* %"vowels", align 4
  br label %"%15"
"%15":
  %".45" = load i32, i32* %"consonants", align 4
  %".46" = add i32 %".45", 1
  store i32 %".46", i32* %"consonants", align 4
  br label %"%5"
"%7":
  %".49" = load i32, i32* %"vowels", align 4
  %".50" = icmp eq i32 %".49", 3
  %".51" = load i32, i32* %"consonants", align 4
  %".52" = icmp eq i32 %".51", 5
  %".53" = and i1 %".50", %".52"
  br i1 %".53", label %"%0", label %"%55"
"%55":
  %".55" = bitcast [3 x i8]* @".fmt" to i8*
  %".56" = call i32 (i8*, ...) @"printf"(i8* %".55", [23 x i8]* @".str.7")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1