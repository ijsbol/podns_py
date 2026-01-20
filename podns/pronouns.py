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

    def to_list(self) -> list[str | None]:
        return [
            self.subject,
            self.object,
            self.possessive_determiner,
            self.possessive_pronoun,
            self.reflexive,
        ]

    def is_strict_subset_of(self, other: Pronouns) -> bool:
        assert len(set(self.to_list()).difference({None})) >= 2
        assert len(set(other.to_list()).difference({None})) >= 2

        if self == other:
            return False

        for s_p, o_p in zip(self.to_list(), other.to_list()):
            if s_p == o_p:
                continue
            elif s_p == None and o_p != None:
                return True
            elif s_p != o_p:
                return False

        raise AssertionError("This should never be executed.")

    def __repr__(self) -> str:
        parts = [p for p in self.to_list() if p is not None]
        return "/".join(parts)


@dataclass(slots=True, frozen=True)
class PronounRecord:
    pronouns: Pronouns
    tags: frozenset[PronounTag]

    def __repr__(self) -> str:
        if not self.tags:
            return str(self.pronouns)
        tags = ", ".join(sorted(t.value for t in self.tags))
        return f"{self.pronouns} [{tags}]"


@dataclass(slots=True, frozen=True)
class PronounsResponse:
    uses_any_pronouns: bool
    uses_name_only: bool
    records: frozenset[PronounRecord]

    def __repr__(self) -> str:
        if not self.records:
            return (
                "PronounsResponse("
                f"uses_any_pronouns={self.uses_any_pronouns}, "
                f"uses_name_only={self.uses_name_only}, "
                "records=[]"
                ")"
            )

        rendered = [str(r) for r in self.records]
        one_liner = (
            "PronounsResponse("
            f"uses_any_pronouns={self.uses_any_pronouns}, "
            f"uses_name_only={self.uses_name_only}, "
            f"records=[{', '.join(rendered)}]"
            ")"
        )

        # if it’s getting long, switch to a multiline
        if len(one_liner) <= 110 and all(len(x) <= 60 for x in rendered):
            return one_liner

        lines = [
            "PronounsResponse(",
            f"  uses_any_pronouns={self.uses_any_pronouns},",
            f"  uses_name_only={self.uses_name_only},",
            "  records=[",
            *[f"    {x}," for x in rendered],
            "  ]",
            ")",
        ]
        return "\n".join(lines)
