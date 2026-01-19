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

from dataclasses import dataclass
from enum import StrEnum


__all__: tuple[str, ...] = (
    "PronounsResponse",
    "PronounTag",
    "Pronouns",
)


class PronounTag(StrEnum):
    PREFERRED = "preferred"
    PLURAL = "plural"


@dataclass(slots=True, frozen=True)
class Pronouns:
    subject: str
    object: str
    possessive_determiner: str | None
    possessive_pronoun: str | None
    reflexive: str | None


@dataclass(slots=True, frozen=True)
class PronounRecord:
    pronouns: Pronouns
    tags: set[PronounTag]


@dataclass(slots=True, frozen=True)
class PronounsResponse:
    uses_any_pronouns: bool
    uses_name_only: bool
    records: list[PronounRecord]
