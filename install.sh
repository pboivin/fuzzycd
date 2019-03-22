#!/usr/bin/env bash

FUZZYCD_PY="fuzzycd.py"
FUZZYCD_HELPER="fuzzycd_helper.sh"
INSTALL_DIR="${INSTALL_DIR:-"/usr/local/share/fuzzycd"}"

function error() {
    echo "Error: $1" >&2
    exit 1
}

function check_install_dir() {
    if [ ! -e "$INSTALL_DIR" ]; then
        mkdir -p "$INSTALL_DIR"
        (test $? != 0) && error "Can't install to directory $INSTALL_DIR"
    fi
}

function install_file() {
    local file="$1"
    local destination="$INSTALL_DIR/$file"

    if [ ! -e "$file" ]; then
        error "Can't find source file $file"
    else
        cp -f "$file" "$destination"
        (test $? != 0) && error "Can't install source file to $destination"
    fi
}

check_install_dir
install_file "$FUZZYCD_PY"
install_file "$FUZZYCD_HELPER"

echo 
echo "Successfully installed to $INSTALL_DIR"
echo 
echo 'Please add the following lines to your bash configuration (~/.bashrc):'
echo 
echo 'export FUZZYCD_DIR="'$INSTALL_DIR'"'
echo '[ -s "$FUZZYCD_DIR/fuzzycd_helper.sh" ] && \. "$FUZZYCD_DIR/fuzzycd_helper.sh"'
echo 'alias f="fuzzycd"'
echo 
