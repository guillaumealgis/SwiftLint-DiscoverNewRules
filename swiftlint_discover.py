#!/usr/bin/env python3

import argparse
import os
import subprocess
from subprocess import DEVNULL, PIPE


class ParserError(Exception):
    def __init__(self, message, input_line):
        message = f"{message}\nOffending line was:\n  {input_line}"
        super().__init__(message)


class InvalidDirectoryError(Exception):
    pass


class Rule:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        identifier,
        opt_in=False,
        correctable=False,
        enabled=False,
        kind="",
        analyzer=False,
        configuration="",
    ):
        self.identifier = identifier.strip()
        self.opt_in = bool_from_string(opt_in)
        self.correctable = bool_from_string(correctable)
        self.enabled = bool_from_string(enabled)
        self.kind = kind.strip()
        self.analyzer = bool_from_string(analyzer)
        self.configuration = configuration.strip()

    def pretty_print(self, ident=2):
        # pylint: disable=invalid-name
        s = " " * ident
        print(f"{s}- {self.identifier}")
        print(f"{s}  https://realm.github.io/SwiftLint/{self.identifier}.html")
        print()

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.identifier == other.identifier
        return False

    def __hash__(self):
        return hash(self.identifier)

    def __repr__(self):
        str_repr = f'Rule<"{self.identifier}"'
        if self.enabled:
            str_repr += " enabled"
        else:
            str_repr += " disabled"
        if self.opt_in:
            str_repr += " opt_in"
        if self.analyzer:
            str_repr += " analyzer"
        str_repr += ">"
        return str_repr


def bool_from_string(bool_str):
    if isinstance(bool_str, bool):
        return bool_str

    clean_str = bool_str.strip().lower()
    if clean_str == "yes":
        return True
    if clean_str == "no":
        return False

    raise ValueError(f"Unexpected boolean string '{bool_str}'")


def print_summary(new_rules):
    disabled_opt_in_rules = []
    disabled_analyzer_rules = []
    for rule in new_rules:
        if rule.enabled:
            continue
        if rule.analyzer:
            disabled_analyzer_rules.append(rule)
        elif rule.opt_in:
            disabled_opt_in_rules.append(rule)

    if disabled_opt_in_rules or disabled_analyzer_rules:
        print_section("opt-in", disabled_opt_in_rules)
        print_section("analyzer", disabled_analyzer_rules)
    else:
        print("No new rules to enable!")


def print_section(rules_type, rules):
    if not rules:
        return

    print()
    print(f"{rules_type.capitalize()} rules you could enable:")

    rules.sort(key=lambda x: x.identifier)
    for rule in rules:
        rule.pretty_print()


def collect_disabled_rules(project_dir):
    process = subprocess.run(
        ["swiftlint", "rules"],
        stdout=PIPE,
        stderr=DEVNULL,
        universal_newlines=True,
        check=True,
        cwd=project_dir,
    )

    rules = []

    stdout_lines = process.stdout.splitlines()
    for line in stdout_lines[4:-1]:
        columns = [c.strip() for c in line.split("|") if c]

        if len(columns) != 7:
            raise ParserError(
                "Expected `swiftlint rules` output to be formatted on 7 columns.", line
            )

        rule = Rule(*columns)
        rules.append(rule)

    return {rule for rule in rules if not rule.enabled}


def load_swiftlint_conf(project_dir):
    # pylint: disable=import-outside-toplevel

    try:
        import yaml
    except ModuleNotFoundError:
        print(
            "PyYAML not found. Not checking disabled rules in your SwiftLint configuration file."
        )
        return None

    # Try to use the LibYAML C bindings if available.
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    conf_path = os.path.join(project_dir, ".swiftlint.yml")
    try:
        with open(conf_path, "r") as stream:
            conf = yaml.load(stream, Loader=Loader)
            return conf
    except FileNotFoundError:
        return None


def collect_explicitly_disabled_rules(project_dir):
    conf = load_swiftlint_conf(project_dir)
    if conf is None:
        return set()

    try:
        disabled_rules = conf["disabled_rules"]
    except KeyError:
        return set()

    return {Rule(identifier) for identifier in disabled_rules}


def parse_args():
    def dir_path(string):
        if not os.path.isdir(string):
            raise InvalidDirectoryError(string)
        return string

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dir",
        type=dir_path,
        help="path to the project directory containing the .swiftlint configuration file. Defaults to the current working directory if omited",
        default=os.getcwd(),
        nargs="?",
    )

    args = parser.parse_args()
    args.dir = os.path.abspath(args.dir)

    return args


def main():

    args = parse_args()

    disabled_rules = collect_disabled_rules(args.dir)
    explicitly_disabled_rules = collect_explicitly_disabled_rules(args.dir)
    new_rules = disabled_rules - explicitly_disabled_rules

    print_summary(new_rules)


if __name__ == "__main__":
    main()
