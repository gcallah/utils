#!/bin/sh
#  This file should include all tests run on our html code.

# exit on any error with that error status:
set -e

for test_file in $HTML_DIR/*.html;
do
    echo ''
    echo 'Html-checking file:' $test_file
    python3 $CODE_DIR/html_checker.py "$test_file"
    # echo 'URL-checking file:' $test_file
    # python3 $CODE_DIR/url_checker.py "$test_file" "https://gcallah.github.io/utils/"
    echo 'Spell-checking file:' $test_file
    if [ -z $PS1 ]
    then
        python3 $CODE_DIR/html_spell.py -i $test_file $DATA_DIR/main-dict.txt $DATA_DIR/custom-dict.txt
    else
        python3 $CODE_DIR/html_spell.py $test_file $DATA_DIR/main-dict.txt $DATA_DIR/custom-dict.txt
    fi
done
