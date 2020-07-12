; ModuleID = "/Users/luizeduardocartolano/OneDrive/DUDU/Unicamp/IC/mc921/mc921-compiler-construction/uc_llvm.py"
target triple = "x86_64-apple-darwin19.5.0"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"scanf"(i8* %".1", ...) 

@"n" = global i32 2, align 4
@".str.0" = constant [10 x i8] c"TajMahal.\00", align 1
@".str.1" = constant [2 x i8] c".\00", align 1
@".str.2" = constant [2 x i8] c"a\00", align 1
@".str.3" = constant [2 x i8] c"e\00", align 1
@".str.4" = constant [2 x i8] c"i\00", align 1
@".str.5" = constant [2 x i8] c"o\00", align 1
@".str.6" = constant [2 x i8] c"u\00", align 1
@".str.7" = constant [23 x i8] c"assertion_fail on 20:5\00", align 1
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
  %".8" = load i32, i32* @"n", align 4
  %".9" = icmp ne i32 %".8", 1
  br i1 %".9", label %"%5", label %"%12"
"%5":
  %".11" = load i32, i32* @"n", align 4
  %".12" = bitcast [3 x i8]* @".fmt" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i32 %".11")
  br label %"%12"
"%12":
  %".15" = load i32, i32* %"i", align 4
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* %"i", align 4
  %".18" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".15"
  %".19" = load i8, i8* %".18", align 8
  %".20" = icmp ne i8 %".19", @".str.1"
  br i1 %".20", label %"%13", label %"%14"
"%13":
  %".22" = load i32, i32* %"i", align 4
  %".23" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".22"
  %".24" = load i8, i8* %".23", align 8
  %".25" = icmp eq i8 %".24", @".str.2"
  %".26" = load i32, i32* %"i", align 4
  %".27" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".26"
  %".28" = load i8, i8* %".27", align 8
  %".29" = icmp eq i8 %".28", @".str.3"
  %".30" = or i1 %".25", %".29"
  %".31" = load i32, i32* %"i", align 4
  %".32" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".31"
  %".33" = load i8, i8* %".32", align 8
  %".34" = icmp eq i8 %".33", @".str.4"
  %".35" = or i1 %".30", %".34"
  %".36" = load i32, i32* %"i", align 4
  %".37" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".36"
  %".38" = load i8, i8* %".37", align 8
  %".39" = icmp eq i8 %".38", @".str.5"
  %".40" = or i1 %".35", %".39"
  %".41" = load i32, i32* %"i", align 4
  %".42" = getelementptr [9 x i8], [9 x i8]* %"s", i32 0, i32 %".41"
  %".43" = load i8, i8* %".42", align 8
  %".44" = icmp eq i8 %".43", @".str.6"
  %".45" = or i1 %".40", %".44"
  br i1 %".45", label %"%21", label %"%22"
"%21":
  %".47" = load i32, i32* %"vowels", align 4
  %".48" = add i32 %".47", 1
  store i32 %".48", i32* %"vowels", align 4
  br label %"%22"
"%22":
  %".51" = load i32, i32* %"consonants", align 4
  %".52" = add i32 %".51", 1
  store i32 %".52", i32* %"consonants", align 4
  br label %"%12"
"%14":
  %".55" = load i32, i32* %"vowels", align 4
  %".56" = icmp eq i32 %".55", 3
  %".57" = load i32, i32* %"consonants", align 4
  %".58" = icmp eq i32 %".57", 5
  %".59" = and i1 %".56", %".58"
  br i1 %".59", label %"%0", label %"%62"
"%62":
  %".61" = bitcast [3 x i8]* @".fmt.1" to i8*
  %".62" = call i32 (i8*, ...) @"printf"(i8* %".61", [23 x i8]* @".str.7")
  br label %"%0"
"%0":
  ret i32 0
}

declare void @"llvm.memcpy.p0i8.p0i8.i64"(i8* %".1", i8* %".2", i64 %".3", i1 %".4") 

@".fmt" = internal constant [3 x i8] c"%d\00", align 1
@".fmt.1" = internal constant [3 x i8] c"%s\00", align 1