import pytest

from ..quizzable import Question, Quiz, exceptions


class TestQuiz:
    """Test attributes and methods of the `Quiz` class."""

    @pytest.fixture
    def data(self):
        """Sample data for a basic 4-question quiz."""

        return [
            {
                "_type": "frq",
                "term": "Anything that brings a people together.",
                "answer": "Centripetal force",
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
                "_type": "mcq",
                "term": "The blending of multiple aspects of culture to form a unique identity.",
                "options": [
                    "Syncretism",
                    "Assimilation,",
                    "Acculturation",
                ],
                "answer": "Syncretism",
            },
        ]

    def test_attributes(self, data):
        """Tests the attributes for class `Quiz`."""

        questions = []
        for question_data in data:
            questions.append(Question(question_data))

        quiz = Quiz(questions)
        assert quiz.questions == questions

    def test_to_list(self, data):
        """Checks if `Question.to_list()` returns the question's dictionary representation."""

        questions = []
        for question_data in data:
            questions.append(Question(question_data))

        quiz = Quiz(questions)
        assert quiz.to_list() == data


class TestQuestion:
    """Test attributes and methods of the `Question` class."""

    @pytest.fixture
    def data(self):
        """Sample data for a basic MCQ-format question."""

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

    def test_attributes(self, data):
        """Tests the attributes for class `Question`."""

        question = Question(data)
        assert question.term == data["term"]
        assert question.answer == data["answer"]

    def test_attributes_incomplete(self, bad_data):
        """Tests error handling in the case of incomplete data for class `Question`."""

        try:
            question = Question(bad_data)
            assert not question
        except exceptions.DataIncompleteError:
            assert True

    @pytest.mark.parametrize(
        "answer, is_answer",
        [("Federal state", True), ("Nation state", False), ("Divided state", False)],
    )
    def test_check_answer(self, answer, is_answer, data):
        """Checks if `Question.check_answer()` returns the correct value."""

        question = Question(data)
        assert question.check_answer(answer) == (is_answer, data["answer"])

    def test_to_dict(self, data):
        """Checks if `Question.to_dict()` returns the question's dictionary representation."""

        question = Question(data)
        assert question.to_dict() == data
