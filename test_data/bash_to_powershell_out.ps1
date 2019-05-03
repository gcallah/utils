#!/bin/sh

# exit on any error with that error status:
$erroractionpreference = "stop"

$TEST_DATA = "test_data"
$title = "Test"

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

run_diff_test_std create_page "$title" "http://www.testingit.com/"
run_diff_test_file create_gloss
run_diff_test_file create_menu
run_diff_test_file html_checker
exit 0
