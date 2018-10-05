# Find paths to python and script

FUZZYCD_PYTHON="$(which python)"
if [ "$FUZZYCD_PYTHON" == "" ]; then
    FUZZYCD_PYTHON="$(which python3)"
fi

FUZZYCD_SCRIPT="$PWD/fuzzycd.py"


# Generate helper script

echo '
FUZZYCD_PYTHON="'$FUZZYCD_PYTHON'"
FUZZYCD_SCRIPT="'$FUZZYCD_SCRIPT'"

function f() {
    local output=$($FUZZYCD_PYTHON $FUZZYCD_SCRIPT $@)
    local split=($output)
    if [ "${split[0]}" == "found:" ]; then
        unset split[0]
        cd "$(echo ${split[@]})"
    else
        echo "$output"
    fi
}
'
