#!/bin/sh

# exit on any error with that error status:
set -e

diff_output() {
    echo "Going to diff $TEST_DATA/$1_out.txt $TEST_DATA/$1_tmp.txt"
    diff $TEST_DATA/$1_out.txt $TEST_DATA/$1_tmp.txt
    echo "$1 passed."
    rm $TEST_DATA/$1_tmp.txt
}

# customized diff function for gloss_links
diff_output_gloss_links() {
    echo "Going to diff $TEST_DATA/$1_out.txt $TEST_DATA/$2.txt"
    diff $TEST_DATA/$1_out.txt $TEST_DATA/$2.txt
    echo "$1 passed."
    rm $TEST_DATA/$2.txt
}

run_diff_test_std() {
    echo "Running python ./$1.py $2 < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    python ./"$1.py" "$2" < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

run_diff_test_std_monitor() {
    echo "Running python ./$1.py $2 < $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    python ./"$1.py" "$2" > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

run_diff_test_file() {
    echo "Running python ./$1.py $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt"
    python ./"$1.py" $TEST_DATA/$1_inp.txt > $TEST_DATA/$1_tmp.txt || true
    diff_output $1
}

run_quiz_test_work() {
    echo "Running python ./$1.py $2 > $TEST_DATA/$1_tmp.txt"
    python ./"$1.py" "$2" > $TEST_DATA/$1_tmp.txt
    diff_output $1
}

run_gloss_links_file() {
    echo "Running python ./$1.py with keyword "$3" > $TEST_DATA/$3.txt"
    python ./"$1.py" $TEST_DATA/"$2.txt" $TEST_DATA --lf "$TEST_DATA/$1_inp.txt"
    diff_output_gloss_links $1 $3

}

export title="Test page"
export title2="work"
export key="gloss_key"
export key_word="Django"
export page="http://www.thedevopscourse.com"
run_diff_test_std create_page "$title"
run_diff_test_file create_gloss
run_gloss_links_file gloss_links "$key" "$key_word"
run_diff_test_file create_menu
run_diff_test_file html_checker
run_diff_test_std_monitor monitor "$page"
# run_quiz_test_work qexport "$title2"
# url checker not ready for testing!
# run_diff_test_file url_checker
exit 0
