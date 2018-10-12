#!/bin/sh

# exit on any error with that error status:
set -e

./create_gloss.py $TEST_DATA/create_gloss_inp.txt > $TEST_DATA/create_gloss_tmp.txt
diff $TEST_DATA/create_gloss_out.txt $TEST_DATA/create_gloss_tmp.txt
echo "Create gloss test passed."
rm $TEST_DATA/create_gloss_tmp.txt

./create_menu.py $TEST_DATA/create_menu_inp.txt $TEST_DATA/create_menu_tmp.txt
diff $TEST_DATA/create_menu_out.txt $TEST_DATA/create_menu_tmp.txt
echo "Create menu test passed."
rm $TEST_DATA/create_menu_tmp.txt

