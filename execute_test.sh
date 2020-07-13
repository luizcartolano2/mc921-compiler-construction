PROCESSOS=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15")

for i in "${PROCESSOS[@]}"; do
    python3 uc.py tests/cases/t"$i" -i -o -l
done
