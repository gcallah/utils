#!/bin/sh

# exit on any error with that error status:
set -e

diff_output() {
    echo "Going to diff $TEST_DATA/$1_out.txt $TEST_DATA/$1_tmp.txt"
    diff $TEST_DATA/$1_out.txt $TEST_DATA/$1_tmp.txt
    echo "$1 passed."
    rm $TEST_DATA/$1_tmp.txt
}

run_diff_test_std() {
    echo "Running python ./$1.py $2 < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    python3 ./"$1.py" "$2" < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

run_diff_test_file() {
    echo "Running python ./$1.py $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    python3 ./"$1.py" $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt || true
    diff_output $1
}

run_quiz_test_work() {
    echo "Running python ./$1.py $2 > $TEST_DATA/$1_tmp.txt"
    python3 ./"$1.py" "$2" > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

export title="Test page"
export title2="work"
run_diff_test_std create_page "$title"
run_diff_test_file create_gloss
#run_diff_test_file create_menu
run_diff_test_file html_checker
#run_quiz_test_work qexport "$title2"
exit 0
