import pytest

from ..quizzable import (
    FRQQuestion,
    MCQQuestion,
    Question,
    Quiz,
    TrueFalseQuestion,
    exceptions,
)


class TestQuiz:
    """Test functions/methods of the `Quiz` class."""

    @pytest.fixture
    def data(self):
        """Sample data representation of a basic 3-question quiz."""

        return [
            {
                "_type": "frq",
                "term": "A type of language that forms due to extensive contact between different groups of people",
                "answer": "Pidgin",
            },
            {
                "_type": "mcq",
                "term": "The blending of multiple aspects of culture to form a unique identity.",
                "options": [
                    "Syncretism",
                    "Assimilation,",
                    "Acculturation",
                ],
                "answer": "Syncretism",
            },
            {
                "_type": "tf",
                "term": "Anything that brings a people together.",
                "definition": "Centrifugal force",
                "answer": False,
            },
        ]

    @pytest.fixture
    def quiz(self):
        """Sample basic 3-question quiz based on fixture `data`."""
        return Quiz(
            [
                FRQQuestion(
                    "A type of language that forms due to extensive contact between different groups of people",
                    "Pidgin",
                ),
                MCQQuestion(
                    "The blending of multiple aspects of culture to form a unique identity.",
                    [
                        "Syncretism",
                        "Assimilation,",
                        "Acculturation",
                    ],
                    "Syncretism",
                ),
                TrueFalseQuestion(
                    "Anything that brings a people together.",
                    "Centrifugal force",
                    False,
                ),
            ]
        )

    def test_from_data(self, data):
        """Tests if a list of data can be used to reconstruct a `Quiz` object."""

        quiz = Quiz.from_data(data)
        for question, question_data in zip(quiz.questions, data):
            assert question.to_dict() == question_data

    def test_to_data(self, quiz, data):
        """Checks if `Quiz.to_data()` returns the quiz's list representation."""

        assert quiz.to_data() == data


class TestQuestion:
    """Test functions/methods of the `Question` class."""

    @pytest.fixture
    def data(self):
        """Sample data representation of the `question` fixture."""

        return {
            "_type": "mcq",
            "term": "A state divided into several regions with some degree of autonomy under one government.",
            "options": [
                "Unitary state",
                "Multi-state nation",
                "Federal state",
                "Nation state",
            ],
            "answer": "Federal state",
        }

    @pytest.fixture
    def bad_data(self):
        """Sample incomplete data for a quiz question."""

        return {
            "_type": "mcq",
            "term": "A state divided into several regions with some degree of autonomy under one government.",
        }

    @pytest.fixture
    def question(self):
        """Sample MCQ-format question based on fixture `data`."""
        return MCQQuestion(
            "A state divided into several regions with some degree of autonomy under one government.",
            [
                "Unitary state",
                "Multi-state nation",
                "Federal state",
                "Nation state",
            ],
            "Federal state",
        )

    def test_from_dict(self, data):
        """Tests if a dictionary can be used to reconstruct a `Question`."""

        question = Question.from_dict(data)
        assert question.term == data["term"]
        assert question.answer == data["answer"]

    def test_from_dict_incomplete(self, bad_data):
        """Tests error handling in the case of incomplete data for class `Question`."""

        try:
            question = Question.from_dict(bad_data)
            assert not question
        except exceptions.DataIncompleteError:
            assert True

    @pytest.mark.parametrize(
        "answer, is_answer",
        [("Federal state", True), ("Nation state", False), ("Divided state", False)],
    )
    def test_check_answer(self, answer, is_answer, question, data):
        """Checks if `Question.check_answer()` returns the correct value."""

        assert question.check_answer(answer) == (is_answer, data["answer"])

    def test_to_dict(self, question, data):
        """Checks if `Question.to_dict()` returns the question's dictionary representation."""

        assert question.to_dict() == data
