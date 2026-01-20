# podns_py

![enbyware](https://pride-badges.pony.workers.dev/static/v1?label=enbyware&labelColor=%23555&stripeWidth=8&stripeColors=FCF434%2CFFFFFF%2C9C59D1%2C2C2C2C)
![license](https://img.shields.io/github/license/ijsbol/podns_py)
![pypi-version](https://img.shields.io/pypi/v/podns)
![python-version](https://img.shields.io/pypi/pyversions/podns)
![github-issues](https://img.shields.io/github/issues/ijsbol/podns_py)
![github-issues](https://img.shields.io/github/issues/ijsbol/podns_py)


A [Pronouns over DNS](https://github.com/CutieZone/pronouns-over-dns/) specification compliant Python API.


## Documentation

### Fetching from domain record.

If you want to fetch someones pronouns from their domain, see the below:

Note that we support both synchronous and asynchronous lookups.


```python
import asyncio

import podns.dns


async def main() -> None:
    domain = "abigail.sh"
    podns.dns.fetch_pronouns_from_domain_sync(domain)
    await podns.dns.fetch_pronouns_from_domain_async(domain)


if __name__ == "__main__":
    asyncio.run(main())
```

### Parsing a raw list

If you already have fetched the users pronouns, or are just parsing a raw literal:

```python
import podns.parser

podns.parser.parse_pronoun_records([
    "she/her",
    "they/them/theirs;preferred"
])
```

### Optional pedantic `kwarg` on user APIs

For all user-level APIs (that is, `podns.dns.fetch_pronouns_from_domain_*` and `podns.parser.parse_pronoun_records`), there is an optional kwarg, `pedantic`, that defaults to `False`.

- Setting this to `True` will raise errors on all specification-violating parse errors from the provided records.
- Setting this to `False` will only raise errors on egregious specification violations that make parsing impossible. When set to `False`, podns will do its' best to infer intent when met with trivial violations, it will however never return a `podns.pronouns.PronounsResponse` that violates the specification.


> [!NOTE]
> there was exactly zero usage of generative ai involved during the development of this package, including autocomplete.
