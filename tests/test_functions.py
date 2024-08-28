import pytest

from ..quizzable import Terms, exceptions


class TestFunctions:
    """Test methods of `Terms` exposed by the `quizzable` library."""

    @pytest.fixture
    def terms(self):
        """Sample terms for the content of a basic quiz."""

        return Terms(
            {
                "A state divided into several regions with some degree of autonomy under one government.": "Federal state",
                "A state with a centralized government that holds all power.": "Unitary state",
                "A group of people with a common cultural or political identity.": "Nation",
                "A state whose population largely consists of a single nation holding power.": "Nation state",
                "A nation whose population is distributed amongst multiple states.": "Multi-state nation",
                "Anything that brings a people together.": "Centripetal force",
                "Anything that divides people apart.": "Centrifugal force",
                "A type of language that forms due to extensive contact between different groups of people": "Pidgin",
                "A type of language that is a blend of multiple languages (typically as a result of colonialization).": "Creole",
                "The blending of multiple aspects of culture to form a unique identity.": "Syncretism",
                "When a cultural group is completely absorbed into (the majority of) society.": "Assimilation",
                "When aspects of different cultures influence another without replacing either one.": "Acculturation",
            }
        )

    @pytest.mark.parametrize("answer_with", ["term", "def", "both"])
    def test_get_terms(self, answer_with, terms):
        terms_copy = terms.get_terms(answer_with)

        for term in terms:
            if term in terms_copy:
                assert terms_copy[term] == terms[term]
            else:
                assert terms_copy[terms[term]] == term

    def test_get_frq_question(self, terms):
        """Test that `get_frq_question` returns an `FRQQuestion` with a term and its answer."""

        frq = terms.get_frq_question()
        assert frq.answer == terms[frq.term]

    @pytest.mark.parametrize("n_options", [0, 3, 13])
    def test_get_mcq_question(self, terms, n_options):
        """Test that `get_frq_question` returns an `MCQQuestion` with a term, its answer, and `n_options` options."""

        try:
            mcq = terms.get_mcq_question(n_options)
            assert mcq.answer == terms[mcq.term]
            assert len(mcq.options) == n_options
        except exceptions.InvalidOptionsError:
            assert True

    def test_get_true_false_question(self, terms):
        """Test that `get_true_false_question` returns a `TrueFalseQuestion` with a term, a definition, and answer."""

        tf = terms.get_true_false_question()
        assert tf.answer == (terms[tf.term] == tf.definition)

    @pytest.mark.parametrize("n_terms", [0, 6, 13])
    def test_get_match_question(self, n_terms, terms):
        """Test that `get_frq_question` returns a `MatchQuestion` with a term, its answer, and `n_terms` definitions."""

        try:
            match = terms.get_match_question(n_terms)
            for definition in match.answer:
                assert match.answer[definition] == terms[definition]
            assert len(match.definitions) == n_terms
        except exceptions.InvalidTermsError:
            assert True

    @pytest.mark.parametrize(
        "types",
        [["mcq"], ["frq"], ["tf"], ["match"], ["mcq", "frq", "tf", "match"], ["test"]],
    )
    def test_get_random_question(self, types, terms):
        """Test that `get_random_question` returns a random question with a term and answer."""

        try:
            question = terms.get_random_question(types, n_options=4, n_terms=5)
            assert question.check_answer(question.answer)
        except exceptions.InvalidQuestionError:
            assert True

    @pytest.mark.parametrize("length", [0, 5, 13])
    def test_get_quiz(self, length, terms):
        """Test that `get_quiz` returns a randomly generated quiz `length` questions."""

        try:
            quiz = terms.get_quiz(
                types=["mcq", "frq", "tf", "match"],
                length=length,
                answer_with="both",
                n_options=4,
                n_terms=5,
            )
            assert len(quiz.questions) == length
        except exceptions.InvalidLengthError:
            assert True
