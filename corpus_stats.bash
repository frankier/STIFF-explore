echo "Sentences"
grep -c '<sentence ' $1/corpus.xml
echo "Instances"
wc -l $1/corpus.sup.key
echo "Synsets"
cut -d ' ' -f 2 $1/corpus.sup.key | sort | uniq | wc -l
