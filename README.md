# fuzzycd


### Requirements

- Python 2.7 or higher


### Installation

```
git clone https://github.com/pboi20/fuzzycd.git
cd fuzzycd
sudo ./install.sh
```

If the installation succeeds, you will be prompted to add the following lines
to your bash configuration:
```
export FUZZYCD_DIR="/usr/local/share/fuzzycd"
[ -s "$FUZZYCD_DIR/fuzzycd_helper.sh" ] && \. "$FUZZYCD_DIR/fuzzycd_helper.sh"
alias f="fuzzycd"
```

**Install Location**

The default install location is `/usr/local/share/fuzzycd`.

You can specify an alternative location with the `INSTALL_DIR` variable:
```
INSTALL_DIR="$HOME/.fuzzycd" ./install.sh
```

**Development**

If you wish to run the script directly from the cloned git repository,
set the `FUZZYCD_DIR` variable in your bash configuration accordingly:
```
export FUZZYCD_DIR="$HOME/code/fuzzycd"
[ -s "$FUZZYCD_DIR/fuzzycd_helper.sh" ] && \. "$FUZZYCD_DIR/fuzzycd_helper.sh"
alias f="fuzzycd"
```


### Usage

```
$ f -h
usage: f [-h] [-n] [-a] [-l] [search]

Change the current working directory using fuzzy string matching

positional arguments:
  search                the string to use for fuzzy matching

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-links        ignore symlinks
  -a, --include-hidden  include hidden files (ignored by default)
  -l, --list            use a newline-separated listing format
```

**Example**

```
# Current working directory is `~/Documents`

# Print directories in curent working directory
~/Documents $ f
Something/  ThereThere/  TwoPlusTwo/  four/  one/  three/  two/

# Change working directory
~/Documents $ f tpt

# Current working directory is now `~/Documents/TwoPlusTwo`
```


### Running the tests

```
python test.py -v
```


### Disclaimer

This is a work in progress :)

[MIT License](https://github.com/pboi20/fuzzycd/blob/master/LICENSE)
