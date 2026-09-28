# zoho-crm-migration-auditor (moved)

This project moved to [zoho-implementation-toolkit](https://github.com/prashobnair/zoho-implementation-toolkit) as the `migration` module. Its full commit history was preserved there.

It audits a CRM migration export before import — duplicates, orphans, and unmapped stages surface while they are still cheap to fix.

## Use it now

```sh
pip install https://github.com/prashobnair/zoho-implementation-toolkit/releases/download/v0.1.0/zohokit-0.1.0-py3-none-any.whl
```

or

```sh
uv tool install git+https://github.com/prashobnair/zoho-implementation-toolkit@v0.1.0
```

The old `python cli.py examples.json [--strict]` is now:

```sh
zohokit migration audit source.json [--strict]
```

`--strict` exits 2 when the export is not ready for import. Reports render with `--format json|table|markdown|html` and `--out`.

## Links

- Module guide: https://prashobnair.github.io/zoho-implementation-toolkit/modules/migration/
- What changed versus this repo: https://prashobnair.github.io/zoho-implementation-toolkit/legacy-parity/
- Source: https://github.com/prashobnair/zoho-implementation-toolkit/tree/main/src/zohokit/modules/migration

This repository is archived and read-only.
