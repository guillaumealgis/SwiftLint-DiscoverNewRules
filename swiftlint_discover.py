#!/usr/bin/env python3

import subprocess
from subprocess import PIPE, STDOUT


class Rule:
    # pylint: disable=too-many-arguments
    def __init__(
        self, identifier, opt_in, correctable, enabled, kind, analyzer, configuration
    ):
        self.identifier = identifier.strip()
        self.opt_in = bool_from_string(opt_in.strip())
        self.correctable = bool_from_string(correctable.strip())
        self.enabled = bool_from_string(enabled.strip())
        self.kind = kind.strip()
        self.analyzer = bool_from_string(analyzer.strip())
        self.configuration = configuration.strip()

    def pretty_print(self, ident=2):
        # pylint: disable=invalid-name
        s = " " * ident
        print(f"{s}- {self.identifier}")
        print(f"{s}  https://realm.github.io/SwiftLint/{self.identifier}.html")
        print()


def bool_from_string(bool_str):
    lower_bool_str = bool_str.lower()
    if lower_bool_str == "yes":
        return True
    if lower_bool_str == "no":
        return False

    raise ValueError(f"Unexpected boolean string '{bool_str}'")


def print_section(rules_type, rules):
    if not rules:
        return

    print()
    print(f"{rules_type.capitalize()} rules you could enable:")
    for rule in rules:
        rule.pretty_print()


def main():
    process = subprocess.run(
        ["swiftlint", "rules"], stdout=PIPE, stderr=STDOUT, universal_newlines=True
    )

    rules = []

    stdout_lines = process.stdout.splitlines()
    for line in stdout_lines[4:-1]:
        columns = [c.strip() for c in line.split("|") if c]
        rule = Rule(*columns)
        rules.append(rule)

    disabled_opt_in_rules = []
    disabled_analyzer_rules = []
    for rule in rules:
        if rule.enabled:
            continue
        if rule.analyzer:
            disabled_analyzer_rules.append(rule)
        if rule.opt_in:
            disabled_opt_in_rules.append(rule)

    if disabled_opt_in_rules or disabled_analyzer_rules:
        print_section("opt-in", disabled_opt_in_rules)
        print_section("analyzer", disabled_analyzer_rules)
    else:
        print("No new rules to enable!")


if __name__ == "__main__":
    main()
