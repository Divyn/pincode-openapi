# Handle a PIN code that does not exist

The API returns HTTP 200 even when nothing is found, so read `Status` in the body.

When the PIN code does not exist, `Status` is `Error` and `PostOffice` is null.

```python
result = body[0]
if result["Status"] == "Error":
    print("No post office found:", result["Message"])
```
