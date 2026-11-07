# pincode-openapi

An OpenAPI spec for the India Post PIN code API, written from its real responses, and a contract test that checks the live API against it.

The spec written only from the docs page (`openapi_from_docs.yaml`) matches 0 of 5 live responses. The spec written from the real responses (`openapi.yaml`) matches 5 of 5.

## Files

- `capture.py` calls the API for five cases and saves each response to `responses/`.
- `openapi_from_docs.yaml` is the spec copied from http://www.postalpincode.in/Api-Details.
- `openapi.yaml` is the spec fixed from the real responses.
- `contract_test.py` calls every case live and validates it against a spec. It exits with 1 on any mismatch, so it can run on a schedule in CI.
- `output_*.txt` are the outputs from the runs in the video.

## Run it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python capture.py
.venv/bin/python contract_test.py openapi_from_docs.yaml
.venv/bin/python contract_test.py openapi.yaml
```

## What the docs get wrong

- Status is `Success` / `Error`, not `SUCCESS` / `ERROR`.
- The field is `Pincode`, not `PINCode`.
- `Description` comes back as `null`.
- The PIN code search returns an extra `Block` field.
- A PIN code that is not a number returns a different shape, with `"Status": "404"` inside an HTTP 200.

## Docs drift check

`drift_check.py` fails a pull request when a guide in `docs/` still uses a field name or a value that the new spec removed.

```bash
git show origin/main:openapi.yaml > openapi_main.yaml
python3 drift_check.py openapi_main.yaml openapi.yaml docs
```

`.github/workflows/docs-drift.yml` runs it on every pull request that changes `openapi.yaml` or `docs/`.

- `output_drift_fail.txt`: the spec from the docs page against the spec from real responses, with the old guides. 6 stale references, exit code 1.
- `output_drift_pass.txt`: the same check after the guides were fixed. 0 stale references, exit code 0.
- `output_guide_snippet.txt`: the old guide code prints nothing and shows no error. The fixed code prints 4 post offices.

It checks field names and enum or const values only. Renamed endpoint paths are not covered.

