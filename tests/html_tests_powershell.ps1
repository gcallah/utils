$TEST_DIR = "tests"
$TEST_DATA = "test_data"
$LIB_DIR = "pylib"
$CODE_DIR = "."
$HTML_DIR = "."
$DATA_DIR = $CODE_DIR + "/data"
$DOCKER_DIR = "docker"

#!/bin/sh
#  This file should include all tests run on our html code.

# exit on any error with that error status:
$erroractionpreference = "stop"

foreach ($test_file in Get-ChildItem -Path  $HTML_DIR/*.html -Force)
{
Write-Host ''
Write-Host 'Html-checking file:' $test_file
python $CODE_DIR/html_checker.py "$test_file"
Write-Host 'URL-checking file:' $test_file
python $CODE_DIR/url_checker.py "$test_file" "https://gcallah.github.io/utils/"
Write-Host 'Spell-checking file:' $test_file
if ( $null -eq $PS1 )
{
python $CODE_DIR/html_spell.py -i $test_file $DATA_DIR/main-dict.txt $DATA_DIR/custom-dict.txt
} 
else {
python $CODE_DIR/html_spell.py $test_file $DATA_DIR/main-dict.txt $DATA_DIR/custom-dict.txt
}
}
