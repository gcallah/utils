set -e
export PYTHONPATH="$GIT_ROOT/utils"
echo $PYTHONPATH
export user_type="test"
export test_dir="tests"
export templ_dir="../templates"
export ignores="FOO"   # dummy file

if [ -z $1 ]
then
    export capture=""
else
    export capture="--nocapture"
fi

nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=pylib $capture

exit 0
