"""Save the real responses of the India Post PIN code API, one file per case.

Usage: python3 capture.py
The spec is written from these files, not from the docs page.
"""

import json
import pathlib
import urllib.request

BASE = "https://api.postalpincode.in"
CASES = {
    "pincode_found": "/pincode/560034",
    "pincode_not_found": "/pincode/56003",
    "pincode_not_a_number": "/pincode/abcdef",
    "postoffice_found": "/postoffice/Koramangala",
    "postoffice_not_found": "/postoffice/zzzz",
}

if __name__ == "__main__":
    out = pathlib.Path("responses")
    out.mkdir(exist_ok=True)
    for name, path in CASES.items():
        with urllib.request.urlopen(BASE + path, timeout=20) as r:
            body = json.load(r)
            print(f"{name:<22} HTTP {r.status}  Status={body[0]['Status']!r}")
        (out / f"{name}.json").write_text(json.dumps(body, indent=2))
