# SwiftLint-DiscoverNewRules

A script to discover and list opt-in rules you have not yet enabled in your [SwiftLint](https://github.com/realm/SwiftLint) config.

# How to use

## Setup

You need Python 3 installed on your system. The easiest way is probably to install it using [homebrew](https://brew.sh/):

```shell
brew install python3
```

but if you want to keep things clean and organised (and if you're using multiple python versions in parallel) I'd recommend looking at [pyenv](https://github.com/pyenv/pyenv).

## Usage

Clone this repository, and run the script by passing your Swift project directory (where the `.swiftlint.yml` file is) as argument:

```shell
./swiftlint_discover.py /path/to/your/swift/project
```

### Only list new SwiftLint rules

If you run this script regularly, you'll notice that it will output the same opt-in rules that you don't want to enable again and again. To prevent that, you can explicitly disable these rules in your `.swiftlint.yml`, and the script will be smart enough to not propose these rules ever again.

For the script to be able to read your SwiftLint configuration though, you have to install the PyYAML dependency. You can either install it globally or in a virtualenv (recommended):

```shell
python3 -m venv $(pwd)/venv
. ./venv/bin/activate
pip install -r requirements.txt # This will install PyYAML
```

For example, if you don't want to ever enable the opt-in rule `explicit_acl`, you can add this to your `.swiftlint.yml`, and it will not be listed as a possible rule to enable by the script:

```yaml
disabled_rules:
  # The following are opt-in rules that we don't want to enable, but that we're
  # keeping here to be able to know which rules are new to SwiftLint when it
  # is updated:
  - explicit_acl
```

(I personally like to keep the comment in the example to remember why I have disabled opt-in rules in my config, which does nothing from a SwiftLint point of view).

# Contact

Guillaume Algis ([@guillaumealgis](https://twitter.com/guillaumealgis))
