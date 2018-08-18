alias fuzzycd="python $PWD/fuzzycd.py"

function f() {
    local output=$(fuzzycd $@)
    local split=($output)
    if [ "${split[0]}" == "found:" ]; then
        unset split[0]
        cd "$(echo ${split[@]})"
    else
        echo "$output"
    fi
}
