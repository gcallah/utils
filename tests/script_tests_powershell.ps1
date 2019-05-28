$TEST_DIR = "tests"
$TEST_DATA = "test_data"
$LIB_DIR = "pylib"
$CODE_DIR = "."
$HTML_DIR = "."
$DATA_DIR = $CODE_DIR + "/data"
$DOCKER_DIR = "docker"

#!/bin/sh

# exit on any error with that error status:
$erroractionpreference = "stop"

function diff_output {
Write-Host "Going to diff $TEST_DATA/$($args[0])_out.txt $TEST_DATA/$($args[0])_tmp.txt"
if ( -not (Compare-Object (Get-Content $TEST_DATA/$($args[0])_out.txt) (Get-Content $TEST_DATA/$($args[0])_tmp.txt)) ) {
Write-Host "$($args[0]) passed."
Remove-Item $TEST_DATA/$($args[0])_tmp.txt
}
else {
Write-Host "Comparison failed."
}
}

# customized diff function for gloss_links
function diff_output_gloss_links {
Write-Host ""
Write-Host "Going to diff $TEST_DATA/$($args[0])_out.txt $TEST_DATA/$($args[1]).txt"
if ( -not (Compare-Object (Get-Content $TEST_DATA/$($args[0])_out.txt) (Get-Content $TEST_DATA/$($args[1]).txt)) ) {
Write-Host "$($args[0]) passed."
Remove-Item $TEST_DATA/$($args[1]).txt
}
else {
Write-Host "Comparison failed."
}
}

function run_diff_test_std {
Write-Host ""
Write-Host "Running python ./$($args[0]).py "$($args[1])" $($args[2]) < $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt"
Get-Content $TEST_DATA/$($args[0])_inp.txt | python ./"$($args[0]).py" "$($args[1])" $($args[2]) > $TEST_DATA/$($args[0])_tmp.txt
diff_output $($args[0])
}

function run_diff_test_file {
Write-Host ""
Write-Host "Running python ./$($args[0]).py $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt"
(python ./"$($args[0]).py" $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt ) -or  $true | out-null
diff_output $($args[0])
}

function run_sieve_test {
Write-Host ""
Write-Host "Running python ./$($args[0]).py > $TEST_DATA/$($args[0])_tmp.txt"
python ./"$($args[0]).py" > $TEST_DATA/$($args[0])_tmp.txt
diff_output $($args[0])
}

function run_quiz_test_work {
Write-Host ""
Write-Host "Running python ./$($args[0]).py $($args[1]) > $TEST_DATA/$($args[0])_tmp.txt"
python ./"$($args[0]).py" "$($args[1])" > $TEST_DATA/$($args[0])_tmp.txt
diff_output $($args[0])
}

function run_gloss_links_file {
Write-Host ""
Write-Host "Running python ./$($args[0]).py with keyword "$($args[2])" > $TEST_DATA/$($args[2]).txt"
python ./"$($args[0]).py" $TEST_DATA/"$($args[1]).txt" $TEST_DATA --lf "$TEST_DATA/$($args[0])_inp.txt"
diff_output_gloss_links $($args[0]) $($args[2])
}

function run_url_checker {
Write-Host ""
Write-Host "Running python ./$($args[0]).py $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt"
(python ./"$($args[0]).py" $TEST_DATA/$($args[0])_inp.txt $($args[1]) > $TEST_DATA/$($args[0])_tmp.txt ) -or  $true | out-null
diff_output $($args[0])
}

function run_spell_checker {
Write-Host ""
Write-Host "Running the spell checker: python"
python ./"$($args[0]).py" "$($args[1]).txt" "$($args[2]).txt"
}

function run_bash_powershell {
Write-Host ""
Write-Host "Running python ./$($args[0]).py $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt"
(python ./"$($args[0]).py" $TEST_DATA/$($args[0])_inp.sh ) -or  $true | out-null
Write-Host "Going to diff $TEST_DATA/$($args[0])_out.ps1 $TEST_DATA/$($args[0])_inp_powershell.ps1"
if ( -not (Compare-Object (Get-Content $TEST_DATA/$($args[0])_out.ps1) (Get-Content $TEST_DATA/$($args[0])_inp_powershell.ps1)) ) {
Write-Host "$($args[0]) passed."
Remove-Item $TEST_DATA/$($args[0])_inp_powershell.ps1
}
else {
Write-Host "Comparison failed."
}
}

$title="Test"
$title2="work"
$key="gloss_key"
$key_word="Django"
$page="http://www.thedevopscourse.com"
run_diff_test_std create_page "$title" "http://www.testingit.com/"
run_diff_test_file create_gloss
#run_gloss_links_file gloss_links "$key" "$key_word"
run_diff_test_file create_menu
run_diff_test_file html_checker
run_sieve_test sieve
# run_quiz_test_work qexport "$title2"
run_url_checker url_checker $page
run_bash_powershell bash_to_powershell
exit 0
