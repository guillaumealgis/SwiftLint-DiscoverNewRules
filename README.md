# SwiftLint-DiscoverNewRules

A script to discover and list opt-in rules you have not yet enabled in your [SwiftLint](https://github.com/realm/SwiftLint) config.

# How to use
## Setup

You need Python 3 installed on your system. The easiest way is probably to install it using [homebrew](https://brew.sh/):

```shell
brew install python3
```

but if you want to keep things clean an organized (and if you're using multiple python versions in parallel, I'd recommend looking at [pyenv](https://github.com/pyenv/pyenv)).

## Running the script

Move to your project directory (where the `.swiftlint.yml` file is), then run:

```shell
python3 swiftlint_discover.py
```



