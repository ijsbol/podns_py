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

from typing import Final, Literal

from podns.error import (
    PODNSParserEmptySegmentInPronounSet,
    PODNSParserIllegalCharacterInPronouns,
    PODNSParserInsufficientPronounSetValues,
    PODNSParserInvalidTag,
    PODNSParserSetsAfterNone,
    PODNSParserTagWithoutPronounSet,
    PODNSParserTooManyPronounSetValues,
    PODNSParserTrailingSlash,
)
from podns.pronouns import (
    PronounRecord,
    Pronouns,
    PronounsResponse,
    PronounTag,
)


__all__: tuple[str, ...] = (
    "parse_pronoun_records",
)


ILLEGAL_PRONOUN_CHARACTERS: Final[Literal[r'";/!#']] = r'";/!#'
PARSER_CONVERSIONS: Final[dict[str, str]] = {
    "it/its": "it/it/its/its/itself",
}


def _normalise_record(record: str) -> str:
    # remove comments, capitalisation and leading/trailing whitespace.
    record = record.split("#")[0].lower().strip()

    # remove spaces around /'s
    pronoun_segment: str = record.split(";")[0]
    pronoun_segments: list[str] = pronoun_segment.split("/")
    pronoun_segment: str = '/'.join(seg.strip() for seg in pronoun_segments)

    # ensure that there are no illegal characters present
    illegal_characters_set: set[str] = set(ILLEGAL_PRONOUN_CHARACTERS)
    for seg in pronoun_segments:
        if illegal_characters_set.difference(seg) != illegal_characters_set:
            raise PODNSParserIllegalCharacterInPronouns(f"{seg=} contains an illegal character defined by: {ILLEGAL_PRONOUN_CHARACTERS=}")

    # add tag part back to record
    tag_segment_parts: list[str] = record.split(";")
    if len(tag_segment_parts) == 1:
        full_record = pronoun_segment
    else:
        tag_segment: str = ';'.join(tag_segment_parts[1:])
        full_record: str = pronoun_segment + ";" + tag_segment

    # normalise repeating ;
    _strip_chars: bool = False
    stripped_record: str = ""
    for char in full_record:
        if char == ";" and not _strip_chars:
            _strip_chars = True
            stripped_record += char
        elif char != ";" and _strip_chars:
            _strip_chars = False
            stripped_record += char
        elif not _strip_chars:
            stripped_record += char

    return stripped_record


def _parse_pronouns(record, *, pedantic: bool) -> Pronouns:
    # we do not care about the tag section here.
    pronoun_part = record.split(";")[0]

    if pronoun_part in PARSER_CONVERSIONS.keys():
        pronoun_part = PARSER_CONVERSIONS[pronoun_part]

    # check for trailing slash
    if pronoun_part.endswith("/") and pedantic:
        raise PODNSParserTrailingSlash(f"Trailing slash in pronouns with {pedantic=} - {record=}")

    # check for empty segment
    pronouns_set = pronoun_part.split("/")
    if any(True for p in pronouns_set if len(p) == 0):
        raise PODNSParserEmptySegmentInPronounSet(f"Empty pronoun segment: {record=}")

    # ensure at least subject/object are present
    if len(pronouns_set) < 2:
        raise PODNSParserInsufficientPronounSetValues(f"There must be at least subject and object pronouns: {record=}")

    if len(pronouns_set) > 5 and pedantic:
        raise PODNSParserTooManyPronounSetValues(f"There are too many provided pronoun values: {record=}")

    # appropriately parse into a `Pronouns` object
    possessive_determiner = None
    if len(pronouns_set) > 2:
        possessive_determiner = pronouns_set[2]

    possessive_pronoun = None
    if len(pronouns_set) > 3:
        possessive_pronoun = pronouns_set[3]

    reflexive = None
    if len(pronouns_set) > 4:
        reflexive = pronouns_set[4]

    return Pronouns(
        subject=pronouns_set[0],
        object=pronouns_set[1],
        possessive_determiner=possessive_determiner,
        possessive_pronoun=possessive_pronoun,
        reflexive=reflexive,
    )


def _parse_tags(record, *, pedantic: bool) -> set[PronounTag]:
    parts = record.rsplit(";")
    if len(parts) == 1 and ";" in record:
        if pedantic:
            raise PODNSParserTagWithoutPronounSet(f"A tag was defined without a preceding pronoun set declaration: {record=}")
        else:
            return set()

    pronoun_tags: set[PronounTag] = set()
    parsed_tags = set(parts[1:]).difference("")
    for parsed_tag in parsed_tags:
        try:
            pronoun_tags.add(PronounTag(parsed_tag))
        except ValueError:
            if pedantic:
                raise PODNSParserInvalidTag(f"Invalid tag: {parsed_tag=}")

    return pronoun_tags


def _parse_record(record: str, *, pedantic: bool) -> PronounRecord:
    # parse the pronouns and tags part into an appropriate record
    pronouns: Pronouns = _parse_pronouns(record, pedantic=pedantic)
    tags: set[PronounTag] = _parse_tags(record, pedantic=pedantic)

    if (  # specifically mark they/them as plural
        pronouns.subject == "they"
        and pronouns.object == "them"
        and PronounTag.PLURAL not in tags
    ):
        tags.add(PronounTag.PLURAL)

    return PronounRecord(pronouns=pronouns, tags=tags)


def parse_pronoun_records(pronoun_records: list[str], *, pedantic: bool = False) -> PronounsResponse:
    uses_any_pronouns: bool = False
    uses_name_only: bool = False
    records: list[PronounRecord] = []

    for record in pronoun_records:
        normalised_record: str = _normalise_record(record)
        if len(normalised_record) == 0:          # empty record
            continue
        elif normalised_record.startswith("!"):  # none; use name only declarator
            uses_name_only = True
            continue
        elif normalised_record.startswith("*"):  # wildcard; any pronoun is declarator
            uses_any_pronouns = True
            continue
        else:                                    # pronoun set
            parsed_record: PronounRecord = _parse_record(normalised_record, pedantic=pedantic)
            records.append(parsed_record)

    if pedantic and uses_name_only and len(records) > 0:
        raise PODNSParserSetsAfterNone(f"{uses_name_only=} and {len(records) > 0=}.")

    return PronounsResponse(
        uses_any_pronouns=uses_any_pronouns,
        uses_name_only=uses_name_only,
        records=[] if uses_name_only else records,
    )
