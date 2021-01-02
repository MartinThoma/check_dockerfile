#!/usr/bin/env python

# Core Library modules
import sys
from pathlib import Path

# Third party modules
import click

# First party modules
import check_dockerfile


@click.command()
@click.version_option(version=check_dockerfile.__version__)
@click.argument(
    "dockerfile",
    type=click.Path(exists=True, readable=True, file_okay=True),
    required=True,
)
def entry_point(dockerfile):
    """Check a dockerfile for issues."""
    checks = check_dockerfile.check(Path(dockerfile))
    found_issues = sum(not check_result for _, _, check_result in checks)
    for check_title, check_value, check_outcome in checks:
        outcome = "\033[32m✔️\033[0m" if check_outcome else "\033[31m✘\033[0m"
        print(f"{check_title}: {check_value} {outcome}")
    if found_issues:
        print(f"Found {found_issues} issue 😱")
        sys.exit(1)
    else:
        print("All checks are ok 🎉")
        return
