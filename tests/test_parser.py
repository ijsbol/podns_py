import logging
import sys
import unittest
from itertools import permutations
from typing import Any, Iterable
from unittest.case import _AssertRaisesContext

import podns.error
import podns.parser
from podns.pronouns import (
    PronounRecord,
    Pronouns,
    PronounsResponse,
    PronounTag,
)


def alert_assert_equal_test_failed(
    parse_input: Iterable[str],
    parse_target: PronounsResponse,
    parse_result: PronounsResponse,
    self: Any,
) -> None:
    print(
        f"\n-----------\nTest failed: {self}\n{parse_input=}\n{parse_target=}\n{parse_result=}\n-----------"
    )


def alert_assert_raises_test_failed(
    parse_input: Iterable[str],
    expected_error: type[Exception],
    context: _AssertRaisesContext | None,
) -> None:
    print(
        f"\n-----------\nTest failed:\n{parse_input=}\n{expected_error=}\n{context=}\n-----------"
    )


class TestValidCanonicalFromSpec(unittest.TestCase):
    def test_she_her(self):
        parse_input: list[str] = ["she/her"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_he_him_his_his_himself_preferred(self):
        parse_input: list[str] = ["he/him/his/his/himself;preferred"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner="his",
                            possessive_pronoun="his",
                            reflexive="himself",
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_they_them_their_theirs_themself_inferred_plural(self):
        parse_input: list[str] = ["they/them/their/theirs/themself"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner="their",
                            possessive_pronoun="theirs",
                            reflexive="themself",
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_they_them_preferred_explicit_plural(self):
        parse_input: list[str] = ["they/them;preferred;plural"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_any_pronouns(self):
        parse_input: list[str] = ["*"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=True,
            uses_name_only=False,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_name_only(self):
        parse_input: list[str] = ["!"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=True,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_that_one_that_one_that_ones(self):
        parse_input: list[str] = ["that one/that one/that one's"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="that one",
                            object="that one",
                            possessive_determiner="that one's",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_ze_zir_zir_zirself(self):
        parse_input: list[str] = ["ze/zir/zir/zirself"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="ze",
                            object="zir",
                            possessive_determiner="zir",
                            possessive_pronoun="zirself",
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e


class TestValidNonCanonicalFromSpec(unittest.TestCase):
    def test_she_her_caps_comment(self):
        parse_input: list[str] = ["SHE/HER #"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_she_her_caps_spaces_comment(self):
        parse_input: list[str] = ["SHE /    HER #"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_he_him_preferred_comment(self):
        parse_input: list[str] = ["he/him;;;preferred #"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e


class TestInvalidFromSpec(unittest.TestCase):
    def test_she_her_trailing_slash(self):
        parse_input: list[str] = ["she/her/"]
        expected_error = podns.error.PODNSParserTrailingSlash
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_she(self):
        parse_input: list[str] = ["she"]
        expected_error = podns.error.PODNSParserInsufficientPronounSetValues
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_they_them_their_theirs_themself_extra(self):
        parse_input: list[str] = ["they/them/their/theirs/themself/extra"]
        expected_error = podns.error.PODNSParserTooManyPronounSetValues
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_she_her_unknown_tag(self):
        parse_input: list[str] = ["she/her;unknown-tag"]
        expected_error = podns.error.PODNSParserInvalidTag
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_invalid_illegal_characters(self):
        parse_input: list[str] = ["in!valid/in*valid"]
        expected_error = podns.error.PODNSParserIllegalCharacterInPronouns
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e


class TestInvalidEdgeCases(unittest.TestCase):
    def test_preferred_with_no_pronouns_set(self):
        parse_input: list[str] = [";preferred"]
        expected_error = podns.error.PODNSParserEmptySegmentInPronounSet
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_preferred_plural_with_no_pronouns_set(self):
        parse_input: list[str] = [";preferred;plural"]
        expected_error = podns.error.PODNSParserEmptySegmentInPronounSet
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_they_them_invalid_tag_declaration(self):
        parse_input: list[str] = ["they/them;"]
        expected_error = podns.error.PODNSParserInvalidTag
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_they_them_invalid_tag_name(self):
        parse_input: list[str] = ["they/them;notreal"]
        expected_error = podns.error.PODNSParserInvalidTag
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_preceding_slash_they_them(self):
        parse_input: list[str] = ["/they/them"]
        expected_error = podns.error.PODNSParserEmptySegmentInPronounSet
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_she_her_plural_invalid_end_tag(self):
        parse_input: list[str] = ["she/her;plural;"]
        expected_error = podns.error.PODNSParserInvalidTag
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_name_only_invalid_chars_after(self):
        parse_input: list[str] = ["!abigail"]
        expected_error = podns.error.PODNSParserContentAfterMagicDeclaration
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_any_pronouns_invalid_chars_after(self):
        parse_input: list[str] = ["*abigail"]
        expected_error = podns.error.PODNSParserContentAfterMagicDeclaration
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_any_pronouns_invalid_chars_after_comment(self):
        parse_input: list[str] = ["*abigail#comment"]
        expected_error = podns.error.PODNSParserContentAfterMagicDeclaration
        context = None

        try:
            with self.assertRaises(expected_error) as context:
                podns.parser.parse_pronoun_records(
                    parse_input,
                    pedantic=True,
                )
        except AssertionError as e:
            alert_assert_raises_test_failed(
                parse_input=parse_input, expected_error=expected_error, context=context
            )
            raise e

    def test_records_after_none_any(self):
        parse_input: list[str] = ["*", "!"]
        expected_error = podns.error.PODNSParserRecordsAfterNone
        context = None

        for permutation in permutations(parse_input):
            try:
                with self.assertRaises(expected_error) as context:
                    podns.parser.parse_pronoun_records(
                        permutation,
                        pedantic=True,
                    )
            except AssertionError as e:
                alert_assert_raises_test_failed(
                    parse_input=permutation,
                    expected_error=expected_error,
                    context=context,
                )
                raise e

    def test_records_after_none_she_her(self):
        parse_input: list[str] = ["!", "she/her"]
        expected_error = podns.error.PODNSParserRecordsAfterNone
        context = None

        for permutation in permutations(parse_input):
            try:
                with self.assertRaises(expected_error) as context:
                    podns.parser.parse_pronoun_records(
                        permutation,
                        pedantic=True,
                    )
            except AssertionError as e:
                alert_assert_raises_test_failed(
                    parse_input=permutation,
                    expected_error=expected_error,
                    context=context,
                )
                raise e


class TestValidEdgeCases(unittest.TestCase):
    def test_stand_alone_comment(self):
        parse_input: list[str] = ["#comment"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_she_h_er(self):
        parse_input: list[str] = ["she   /h er"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="h er",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_th__ey_them_preferred(self):
        parse_input: list[str] = ["th  ey/them;preferred"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="th  ey",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_she_her_comment(self):
        parse_input: list[str] = ["she/her#comment;plural"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_comment_they_them(self):
        parse_input: list[str] = ["#they/them"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_they_them_explicit_plural_comment(self):
        parse_input: list[str] = ["they/them;plural#comment"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="they",
                            object="them",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_she_her_her_double_semicolon_plural(self):
        parse_input: list[str] = ["she/her/her;;plural"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="her",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_she_her_plural_preferred(self):
        parse_input: list[str] = ["she/her;plural;preferred"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PLURAL,
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_name_only_comment(self):
        parse_input: list[str] = ["!#comment"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=True,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_any_pronouns_comment(self):
        parse_input: list[str] = ["*#comment"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=True,
            uses_name_only=False,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e


class TestDeduplication(unittest.TestCase):
    def _assert_permutations(
        self, parse_input: list[str], parse_target: PronounsResponse
    ) -> None:
        for permutation in permutations(parse_input):
            parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
                permutation,
                pedantic=True,
            )

            try:
                self.assertEqual(
                    parse_result,
                    parse_target,
                )
            except AssertionError as e:
                alert_assert_equal_test_failed(
                    parse_input=permutation,
                    parse_target=parse_target,
                    parse_result=parse_result,
                    self=self,
                )
                raise e

    def test_deduplicate_name_only(self):
        parse_input: list[str] = ["!", "!"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=True,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_deduplicate_any_pronouns(self):
        parse_input: list[str] = ["*", "*"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=True,
            uses_name_only=False,
            records=frozenset(),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_deduplicate_she_her(self):
        parse_input: list[str] = ["she/her", "she/her"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e

    def test_deduplicate_she_her_one_preferred_different_order(self):
        parse_input: list[str] = ["she/her;preferred", "she/her"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_she_her_and_she_her_hers(self):
        parse_input: list[str] = ["she/her", "she/her/hers"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="hers",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_she_her_preferred_and_she_her(self):
        parse_input: list[str] = ["she/her;preferred", "she/her/hers"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="hers",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_she_her_preferred_and_she_her_plural(self):
        parse_input: list[str] = ["she/her;preferred", "she/her;plural"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner=None,
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PLURAL,
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_she_her_and_she_her_hers_preferred(self):
        parse_input: list[str] = ["she/her", "she/her/hers;preferred"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="hers",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_edge_case(self):
        parse_input: list[str] = ["a/b/c", "a/b/b"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="a",
                            object="b",
                            possessive_determiner="c",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="a",
                            object="b",
                            possessive_determiner="b",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_multiple_she_hers_different_tag_ordering(self):
        parse_input: list[str] = [
            "she/her;preferred",
            "she/her/hers",
            "she/her/hers;plural",
        ]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="she",
                            object="her",
                            possessive_determiner="hers",
                            possessive_pronoun=None,
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_multiple_he_double_bubble_up(self):
        parse_input: list[str] = ["he/him;preferred", "he/him/his", "he/him/his/his"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner="his",
                            possessive_pronoun="his",
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_multiple_he_double_consecutive_bubble_up(self):
        parse_input: list[str] = [
            "he/him;preferred",
            "he/him/his;plural",
            "he/him/his/his",
        ]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner="his",
                            possessive_pronoun="his",
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)

    def test_deduplicate_multiple_he_double_consecutive_bubble_up_with_duplicate_superset(
        self,
    ):
        parse_input: list[str] = [
            "he/him;preferred",
            "he/him/his;plural",
            "he/him/his/his",
            "he/him/his/his",
        ]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="he",
                            object="him",
                            possessive_determiner="his",
                            possessive_pronoun="his",
                            reflexive=None,
                        ),
                        tags=frozenset(
                            {
                                PronounTag.PREFERRED,
                                PronounTag.PLURAL,
                            }
                        ),
                    ),
                }
            ),
        )

        self._assert_permutations(parse_input, parse_target)


class TestParserConversions(unittest.TestCase):
    def test_parser_conversion_it_its(self):
        parse_input: list[str] = ["it/its"]
        parse_target: PronounsResponse = PronounsResponse(
            uses_any_pronouns=False,
            uses_name_only=False,
            records=frozenset(
                {
                    PronounRecord(
                        pronouns=Pronouns(
                            subject="it",
                            object="it",
                            possessive_determiner="its",
                            possessive_pronoun="its",
                            reflexive="itself",
                        ),
                        tags=frozenset(),
                    ),
                }
            ),
        )
        parse_result: PronounsResponse = podns.parser.parse_pronoun_records(
            parse_input,
            pedantic=True,
        )

        try:
            self.assertEqual(
                parse_result,
                parse_target,
            )
        except AssertionError as e:
            alert_assert_equal_test_failed(
                parse_input=parse_input,
                parse_target=parse_target,
                parse_result=parse_result,
                self=self,
            )
            raise e


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main()
