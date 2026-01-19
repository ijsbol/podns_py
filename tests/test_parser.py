import unittest

import podns.error
import podns.parser
from podns.pronouns import (
    PronounRecord,
    Pronouns,
    PronounsResponse,
    PronounTag,
)


class TestValidCanonicalFromSpec(unittest.TestCase):
    def test_she_her(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["she/her"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_he_him_his_his_himself_preferred(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["he/him/his/his/himself;preferred"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner="his",
                            possessive_pronoun="his",
                            reflexive="himself",
                        ),
                        tags={
                            PronounTag.PREFERRED,
                        },
                    ),
                ],
            )
        )

    def test_they_them_their_theirs_themself_inferred_plural(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["they/them/their/theirs/themself"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner="their",
                            possessive_pronoun="theirs",
                            reflexive="themself",
                        ),
                        tags={
                            PronounTag.PLURAL,
                        },
                    ),
                ],
            )
        )

    def test_they_them_preferred_explicit_plural(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["they/them;preferred;plural"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PREFERRED,
                            PronounTag.PLURAL,
                        },
                    ),
                ],
            )
        )

    def any_pronouns(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["*"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=True,
                uses_name_only=False,
                records=[],
            )
        )

    def name_only(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["!"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=True,
                records=[],
            )
        )

    def test_that_one_that_one_that_ones(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["that one/that one/that one's"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="that one",
                            object="that one",
                            possessive_determiner="that one's",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_ze_zir_zir_zirself(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["ze/zir/zir/zirself"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="ze",
                            object="zir",
                            possessive_determiner="zir",
                            possessive_pronoun="zirself",
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )


class TestValidNonCanonicalFromSpec(unittest.TestCase):
    def test_she_her_caps_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["SHE/HER #"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_she_her_caps_spaces_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["SHE /    HER #"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_he_him_preferred_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["he/him;;;preferred #"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PREFERRED,
                        },
                    ),
                ],
            )
        )

    def test_invalid_illegal_characters(self):
        self.assertRaises(
            podns.error.PODNSParserIllegalCharacterInPronouns,
            lambda: podns.parser.parse_pronoun_records(['in!valid/in*valid'], pedantic=True)
        )


class TestInvalidFromSpec(unittest.TestCase):
    def test_she_her_trailing_slash(self):
        self.assertRaises(
            podns.error.PODNSParserTrailingSlash,
            lambda: podns.parser.parse_pronoun_records(["she/her/"], pedantic=True),
        )

    def test_she(self):
        self.assertRaises(
            podns.error.PODNSParserInsufficientPronounSetValues,
            lambda: podns.parser.parse_pronoun_records(["she"], pedantic=True),
        )

    def test_they_them_their_theirs_themself_extra(self):
        self.assertRaises(
            podns.error.PODNSParserTooManyPronounSetValues,
            lambda: podns.parser.parse_pronoun_records(["they/them/their/theirs/themself/extra"], pedantic=True),
        )

    def test_she_her_unknown_tag(self):
        self.assertRaises(
            podns.error.PODNSParserInvalidTag,
            lambda: podns.parser.parse_pronoun_records(["she/her;unknown-tag"], pedantic=True),
        )


class TestInvalidEdgeCases(unittest.TestCase):
    def test_preferred_with_no_pronouns_set(self):
        self.assertRaises(
            podns.error.PODNSParserEmptySegmentInPronounSet,
            lambda: podns.parser.parse_pronoun_records([";preferred"], pedantic=True),
        )

    def test_preferred_plural_with_no_pronouns_set(self):
        self.assertRaises(
            podns.error.PODNSParserEmptySegmentInPronounSet,
            lambda: podns.parser.parse_pronoun_records([";preferred;plural"], pedantic=True),
        )

    def test_they_them_invalid_tag_declaration(self):
        self.assertRaises(
            podns.error.PODNSParserInvalidTag,
            lambda: podns.parser.parse_pronoun_records(["they/them;"], pedantic=True),
        )

    def test_they_them_invalid_tag_name(self):
        self.assertRaises(
            podns.error.PODNSParserInvalidTag,
            lambda: podns.parser.parse_pronoun_records(["they/them;notreal"], pedantic=True),
        )

    def test_preceding_slash_they_them(self):
        self.assertRaises(
            podns.error.PODNSParserEmptySegmentInPronounSet,
            lambda: podns.parser.parse_pronoun_records(["/they/them"], pedantic=True),
        )

    def test_she_her_plural_invalid_end_tag(self):
        self.assertRaises(
            podns.error.PODNSParserInvalidTag,
            lambda: podns.parser.parse_pronoun_records(["she/her;plural;"], pedantic=True),
        )


class TestValidEdgeCases(unittest.TestCase):
    def test_stand_alone_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["#comment"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[],
            )
        )

    def test_she_h_er(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["she   /h er"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="h er",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_th__ey_them_preferred(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["th  ey/them;preferred"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="th  ey",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PREFERRED,
                        },
                    ),
                ],
            )
        )

    def test_she_her_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["she/her#comment;plural"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=set(),
                    ),
                ],
            )
        )

    def test_comment_they_them(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["#they/them"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[],
            )
        )

    def test_they_them_explicit_plural_comment(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["they/them;plural#comment"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PLURAL,
                        },
                    ),
                ],
            )
        )

    def test_she_her_her_double_semicolon_plural(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["she/her/her;;plural"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="her",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PLURAL,
                        },
                    ),
                ],
            )
        )

    def test_she_her_plural_preferred(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["she/her;plural;preferred"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags={
                            PronounTag.PLURAL,
                            PronounTag.PREFERRED,
                        },
                    ),
                ],
            )
        )


class TestParserConversions(unittest.TestCase):
    def test_parser_conversion_it_its(self):
        self.assertEqual(
            podns.parser.parse_pronoun_records(["it/its"], pedantic=True),
            PronounsResponse(
                uses_any_pronouns=False,
                uses_name_only=False,
                records=[
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="it",
                            object="it",
                            possessive_determiner="its",
                            possessive_pronoun="its",
                            reflexive="itself",
                        ),
                        tags=set(),
                    ),
                ],
            )
        )


if __name__ == "__main_":
    unittest.main()
