#!/bin/sh

# exit on any error with that error status:
set -e

diff_output() {
    diff $TEST_DATA/$1_out.txt $TEST_DATA/$1_tmp.txt
    echo "$1 passed."
    rm $TEST_DATA/$1_tmp.txt
}

run_diff_test() {
    echo "Running ./$1.py $2 < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    ./"$1.py" "$2" < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

export title="Test page"
run_diff_test create_page "$title"


./create_gloss.py $TEST_DATA/create_gloss_inp.txt > $TEST_DATA/create_gloss_tmp.txt
diff $TEST_DATA/create_gloss_out.txt $TEST_DATA/create_gloss_tmp.txt
echo "Create gloss test passed."
rm $TEST_DATA/create_gloss_tmp.txt

./create_menu.py $TEST_DATA/create_menu_inp.txt $TEST_DATA/create_menu_tmp.txt
diff $TEST_DATA/create_menu_out.txt $TEST_DATA/create_menu_tmp.txt
echo "Create menu test passed."
rm $TEST_DATA/create_menu_tmp.txt

