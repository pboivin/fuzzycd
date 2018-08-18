echo '
FUZZYCD_PYTHON="'$(which python)'"
FUZZYCD_SCRIPT="'$PWD'/fuzzycd.py"

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
