# fuzzycd


### Requirements

- Python 2.7 or higher
- fuzzywuzzy
- python-Levenshtein


### Installation

```
git clone https://github.com/pboi20/fuzzycd.git
cd fuzzycd
pip install -r requirements.txt
bash make_helper.sh >> ~/.bashrc
source ~/.bashrc
```

A bash function `f` is added to your shell configuration.


### Usage

```
$ f -h
usage: fuzzycd.py [-h] [-n] [-a] [-l] [search]

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
