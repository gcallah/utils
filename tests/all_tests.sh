#!/bin/sh
#  This file should include all tests run on the utils directory.

# exit on any error with that error status:
set -e

$TEST_DIR/html_tests.sh
$TEST_DIR/script_tests.sh
$TEST_DIR/django_tests.sh
$TEST_DIR/unit_tests.sh
$TEST_DIR/js_tests.sh
