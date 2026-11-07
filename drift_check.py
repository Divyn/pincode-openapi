"""Fail when a guide still uses a field or a value that the new spec removed.

Usage: python3 drift_check.py OLD_SPEC NEW_SPEC DOCS_FOLDER
Exits with 1 if any guide uses a removed name, so a pull request check fails.
"""

import pathlib
import re
import sys

import yaml


def names(node, found):
    """Collect every property name and every enum or const value in a spec."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "properties":
                found.update(value)
            elif key == "enum":
                found.update(str(v) for v in value)
            elif key == "const":
                found.add(str(value))
            names(value, found)
    elif isinstance(node, list):
        for item in node:
            names(item, found)
    return found


old = names(yaml.safe_load(open(sys.argv[1])), set())
new = names(yaml.safe_load(open(sys.argv[2])), set())
removed = sorted(old - new)
print("Removed from the spec:", ", ".join(removed) or "nothing")

hits = 0
for page in sorted(pathlib.Path(sys.argv[3]).rglob("*.md")):
    for number, line in enumerate(page.read_text().splitlines(), 1):
        for name in removed:
            if re.search(rf"\b{re.escape(name)}\b", line):
                hits += 1
                print(f"{page}:{number}: uses {name}")

print(f"{hits} stale reference(s) in the guides")
sys.exit(1 if hits else 0)
