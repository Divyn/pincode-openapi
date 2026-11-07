# Find the post offices for a PIN code

Send a GET request with the six digit PIN code:

```
GET https://api.postalpincode.in/pincode/560034
```

The response is a list with one object. Check `Status` first. It is `Success` when post offices were found.

```python
import json
import urllib.request

with urllib.request.urlopen("https://api.postalpincode.in/pincode/560034") as r:
    body = json.load(r)

if body[0]["Status"] == "Success":
    for office in body[0]["PostOffice"]:
        print(office["Name"], office["Pincode"])
```

Each post office has `Name`, `BranchType`, `District`, `State` and `Pincode`.
