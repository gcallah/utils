#!/bin/sh

# exit on any error with that error status:
$erroractionpreference = "stop"

$TEST_DATA = "test_data"

function diff_output {
Write-Host "Going to diff $TEST_DATA/$($args[0])_out.txt $TEST_DATA/$($args[0])_tmp.txt"
if ( -not (Compare-Object (Get-Content $TEST_DATA/$($args[0])_out.txt) (Get-Content $TEST_DATA/$($args[0])_tmp.txt)) ) {
Write-Host "$($args[0]) passed."
Remove-Item $TEST_DATA/$($args[0])_tmp.txt
}
else {
Write-Host "$($args[0]) failed."
}
}

function run_diff_test_file {
Write-Host "Running python ./$($args[0]).py $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt"
python ./"$($args[0]).py" $TEST_DATA/$($args[0])_inp.txt > $TEST_DATA/$($args[0])_tmp.txt
diff_output $($args[0])
}

run_diff_test_file create_gloss
exit 0
