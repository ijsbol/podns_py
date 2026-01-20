"""
MIT License

Copyright (c) 2024-present abigail phoebe <abigail@phoebe.sh>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import dns.asyncresolver
import dns.resolver

from podns.parser import parse_pronoun_records
from podns.pronouns import PronounsResponse


__all__: tuple[str, ...] = (
    "fetch_pronouns_from_domain_sync",
    "fetch_pronouns_from_domain_async",
)


def fetch_pronouns_from_domain_sync(
    domain: str, *, pedantic: bool = False
) -> PronounsResponse | None:
    try:
        dns_answers = dns.resolver.resolve(f"pronouns.{domain}", "TXT")
    except dns.resolver.NXDOMAIN:
        return None
    return parse_pronoun_records(list(dns_answers), pedantic=pedantic)


async def fetch_pronouns_from_domain_async(
    domain: str, *, pedantic: bool = False
) -> PronounsResponse | None:
    try:
        dns_answers = await dns.asyncresolver.resolve(f"pronouns.{domain}", "TXT")
    except dns.resolver.NXDOMAIN:
        return None
    return parse_pronoun_records(list(dns_answers), pedantic=pedantic)
