#!/usr/bin/env bash

if [ "$FUZZYCD_DIR" == "" ]; then
    echo "Error: FUZZYCD_DIR is not set" >&2
    return
fi

function fuzzycd() {
    local PYTHON=$(which python || which python3)
    local FUZZYCD_PY="$FUZZYCD_DIR/fuzzycd.py"
    local OUTPUT=$($PYTHON $FUZZYCD_PY $@)
    local SPLIT=($OUTPUT)

    if [ "${SPLIT[0]}" == "found:" ]; then
        unset SPLIT[0]
        cd "$(echo ${SPLIT[@]})"
    else
        echo "$OUTPUT"
    fi
}
