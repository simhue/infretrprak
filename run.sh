date > begin
python main.py
sort --parallel=3 -uo sorted-pairs pairs
rm pairs
cat sorted-pairs | uniq -c > counted-pairs
rm sorted-pairs
date > end
