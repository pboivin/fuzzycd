alias fuzzycd="python $PWD/fuzzycd.py"

function f() {
    local output=$(fuzzycd $@)
    local split=($output)
    if [ "${split[0]}" == "found:" ]; then
        cd "${split[1]}"
    else
        echo "$output"
    fi
}
