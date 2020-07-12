; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@".str.0" = constant [10 x i8] c"TajMahal.\00", align 1
@".str.1" = constant [1 x i8] c"\00", align 1
@".str.2" = constant [23 x i8] c"assertion_fail on 14:5\00", align 1
define i32 @"main"() 
{
"%entry":
  %"1" = alloca i32, align 4
  %"s" = alloca [9 x i8], align 4
  %"i" = alloca i32, align 4
  %"vowels" = alloca i32, align 4
  %"consonants" = alloca i32, align 4
  %".2" = bitcast [10 x i8]* @".str.0" to i8*
  %".3" = bitcast [9 x i8]* %"s" to i8*
  call void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".3", i8* %".2", i64 9, i1 false)
  store i32 0, i32* %"i", align 4
  store i32 0, i32* %"vowels", align 4
  store i32 0, i32* %"consonants", align 4
  br label %"%5"
"%5":
  %".9" = load i32, i32* %"i", align 4
  %".10" = add i32 %".9", 1
  store i32 %".10", i32* %"i", align 4
  %".12" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".9"
  %".13" = load i8, i8* %".12", align 8
  %".14" = icmp ne i8 %".13", @".str.1"
  br i1 %".14", label %"%6", label %"%7"
"%6":
  %".16" = load i32, i32* %"i", align 4
  %".17" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".16"
  %".18" = load i8, i8* %".17", align 8
  %".19" = icmp eq i8 %".18", @".str.1"
  %".20" = load i32, i32* %"i", align 4
  %".21" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".20"
  %".22" = load i8, i8* %".21", align 8
  %".23" = icmp eq i8 %".22", @".str.1"
  %".24" = or i1 %".19", %".23"
  %".25" = load i32, i32* %"i", align 4
  %".26" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".25"
  %".27" = load i8, i8* %".26", align 8
  %".28" = icmp eq i8 %".27", @".str.1"
  %".29" = or i1 %".24", %".28"
  %".30" = load i32, i32* %"i", align 4
  %".31" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".30"
  %".32" = load i8, i8* %".31", align 8
  %".33" = icmp eq i8 %".32", @".str.1"
  %".34" = or i1 %".29", %".33"
  %".35" = load i32, i32* %"i", align 4
  %".36" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".35"
  %".37" = load i8, i8* %".36", align 8
  %".38" = icmp eq i8 %".37", @".str.1"
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
  br label %"%16"
"%16":
  br label %"%5"
"%7":
  %".50" = load i32, i32* %"vowels", align 4
  %".51" = icmp eq i32 %".50", 3
  %".52" = load i32, i32* %"consonants", align 4
  %".53" = icmp eq i32 %".52", 5
  %".54" = and i1 %".51", %".53"
  br i1 %".54", label %"%54", label %"%55"
"%54":
  br label %"%56"
"%55":
  %".57" = bitcast [3 x i8]* @".fmt" to i8*
  %".58" = call i32 (i8*, ...) @"printf"(i8* %".57", [23 x i8]* @".str.2")
  br label %"%0"
"%56":
  store i32 0, i32* %"1", align 4
  br label %"%0"
"%0":
  %".62" = load i32, i32* %"1", align 4
  ret i32 %".62"
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%s\00", align 1