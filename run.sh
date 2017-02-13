date > begin
python main.py
sort --parallel=3 -uo sorted-pairs pairs
rm pairs
cat sorted-pairs | uniq -d -c > counted-pairs
rm sorted-pairs
sort --parallel=3 -uo sorted-counted-pairs counted-pairs
rm counted-pairs
date > end
