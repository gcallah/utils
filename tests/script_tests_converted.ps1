#!/bin/sh

# exit on any error with that error status:
$erroractionpreference -eq "stop"

function diff_output {
Write-Host "Going to diff $TEST_DATA/args[1]_out.txt $TEST_DATA/args[1]_tmp.txt"
diff $TEST_DATA/args[1]_out.txt $TEST_DATA/args[1]_tmp.txt
Write-Host "args[1] passed."
rm $TEST_DATA/args[1]_tmp.txt
}

# customized diff function for gloss_links
function diff_output_gloss_links {
Write-Host "Going to diff $TEST_DATA/args[1]_out.txt $TEST_DATA/args[2].txt"
diff $TEST_DATA/args[1]_out.txt $TEST_DATA/args[2].txt
Write-Host "args[1] passed."
rm $TEST_DATA/args[2].txt
}

function run_diff_test_std {
Write-Host "Running python ./args[1].py "args[2]" args[3] < $TEST_DATA/args[1]_inp.txt > $TEST_DATA/args[1]_tmp.txt"
python ./"args[1].py" "args[2]" args[3] < $TEST_DATA/args[1]_inp.txt > $TEST_DATA/args[1]_tmp.txt
diff_output args[1]
}

function run_diff_test_file {
Write-Host "Running python ./args[1].py $TEST_DATA/args[1]_inp.txt > $TEST_DATA/args[1]_tmp.txt"
python ./"args[1].py" $TEST_DATA/args[1]_inp.txt > $TEST_DATA/args[1]_tmp.txt -or true
diff_output args[1]
}

function run_sieve_test {
Write-Host "Running python ./args[1].py > $TEST_DATA/args[1]_tmp.txt"
python ./"args[1].py" > $TEST_DATA/args[1]_tmp.txt
diff_output args[1]
}

function run_quiz_test_work {
Write-Host "Running python ./args[1].py args[2] > $TEST_DATA/args[1]_tmp.txt"
python ./"args[1].py" "args[2]" > $TEST_DATA/args[1]_tmp.txt
diff_output args[1]
}

function run_gloss_links_file {
Write-Host "Running python ./args[1].py with keyword "args[3]" > $TEST_DATA/args[3].txt"
python ./"args[1].py" $TEST_DATA/"args[2].txt" $TEST_DATA --lf "$TEST_DATA/args[1]_inp.txt"
diff_output_gloss_links args[1] args[3]
}

function run_url_checker {
Write-Host "Running python ./args[1].py $TEST_DATA/args[1]_inp.txt > $TEST_DATA/args[1]_tmp.txt"
python ./"args[1].py" $TEST_DATA/args[1]_inp.txt args[2] > $TEST_DATA/args[1]_tmp.txt -or true
diff_output args[1]
}

function run_spell_checker {
Write-Host "Running the spell checker: python"
python ./"args[1].py" "args[2].txt" "args[3].txt"
}

$title-eq"Test"
$title2-eq"work"
$key-eq"gloss_key"
$key_word-eq"Django"
$page-eq"http://www.thedevopscourse.com"
run_diff_test_std create_page "$title" "http://www.testingit.com/"
run_diff_test_file create_gloss
#run_gloss_links_file gloss_links "$key" "$key_word"
run_diff_test_file create_menu
run_diff_test_file html_checker
run_sieve_test sieve
# run_quiz_test_work qexport "$title2"
run_url_checker url_checker $page
exit 0
