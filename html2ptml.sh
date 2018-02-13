FILES=*.html
for f in $FILES
do
  echo "Processing $f file..."
  # you are going to run:
  	filename=$(basename "$f")
	#echo "Processing $filename file..."
	extension="${filename##*.}"
	#echo "Processing $extension file..."
	filename="${filename%.*}"
	#echo "Processing $filename file..."
  	../utils/html2ptml.awk < $f > test/$filename.ptml
  # html2ptml.awk <$f > (What goes here?!)
done
