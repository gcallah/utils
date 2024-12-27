#!/bin/sh

if [ -z $1 ]
then
    echo "Usage: new_pair.sh <base_name>"
    exit 1
fi

# package might need more path in it!
package=$(basename "$PWD")

export mod_name=$1
export code_file=$mod_name.py
export test_dir="tests"
export test_file="$test_dir/test_$1.py"
echo "Writing to $code_file and $test_file."

if [ ! -d $test_dir ]
then
    mkdir $test_dir
fi

echo "Enter the purpose of the pair:"
read purpose

echo "# $purpose\n" > $code_file
cat <<EOF >> $code_file
def main():
    return 0


if __name__ == '__main__':
    main()
EOF

cat <<EOF > $test_file
import $package.$mod_name as $mod_name


def test_main():
    assert $mod_name.main() == 0
EOF
