"""Call every case live and check the response against the spec.

Usage: python3 contract_test.py openapi.yaml
Exits with 1 if any response does not match, so it can run in CI on a schedule.
"""

import json
import sys
import urllib.request

import yaml
from jsonschema import Draft202012Validator

from capture import BASE, CASES

spec = yaml.safe_load(open(sys.argv[1]))
schemas = spec["components"]["schemas"]
failed = 0

for name, path in CASES.items():
    template = "/pincode/{pincode}" if path.startswith("/pincode") else "/postoffice/{name}"
    ref = spec["paths"][template]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    validator = Draft202012Validator({**ref, "components": {"schemas": schemas}})
    with urllib.request.urlopen(BASE + path, timeout=20) as r:
        body = json.load(r)
    errors = list(validator.iter_errors(body))
    if errors:
        failed += 1
        print(f"FAIL {name}")
        for e in errors[:3]:
            print(f"     {e.message[:110]}")
    else:
        print(f"PASS {name}")

print(f"{len(CASES) - failed} of {len(CASES)} match the spec")
sys.exit(1 if failed else 0)
