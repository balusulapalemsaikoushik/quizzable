"""# quizzable
`quizzable` provides an easy-to-implement interface to build a framework for
educational quiz apps built on top of Python. The `quizzable` library contains
functions for the generation of quizzes consisting of MCQ, FRQ, True-or-false,
or Matching questions, allowing you to build educational apps that leverage the
power of Python with great ease.
## Classes
* `Quiz`: quiz object
* `Question`: question object
* `MCQQuestion`: MCQ-format question object
* `FRQQuestion`: FRQ-format question object
* `TrueFalseQuestion`: True-or-false format question object
* `MatchQuestion`: Matching format question object
## Functions
* `get_terms`: get a modified list of terms
* `get_frq_question`: get a random FRQ question based on some terms
* `get_mcq_question`: get a random MCQ question based on some terms
* `get_true_false_question`: get a random True-or-false question based on some terms
* `get_match_question`: get a random Matching question based on some terms
* `get_quiz`: get a randomly generated quiz consisting of different types of quiz questions from some terms
"""

import random
from copy import deepcopy

from . import exceptions


class Quiz:
    """An arbitrary quiz object."""

    def __init__(self, data):
        self.questions = data

    def to_list(self):
        """Returns a listlike representation of the quiz, with each `Question`
        object being represented as its dictionary representation. For example,
        it could look like this:
        ```py
        [
            {
                "_type": "tf",
                "term": "la iglesia",
                "def": "shop",
                "answer": "church"
            },
            {
                "_type": "mcq",
                "term": "la playa",
                "options": {
                    "beach": True,
                    "park": False,
                    "downtown": False,
                    "museum": False,
                }
            },
            {
                "_type": "frq",
                "term": "park",
                "answer": "el parque"
            }
        ]
        ```
        """
        return [q.to_dict() for q in self.questions]


class Question:
    """A generic question object used for reconstruction of a question from JSON data."""

    def __init__(self, data):
        self._data = data

        try:
            self.term = data["term"]
            self.answer = data["answer"]
        except KeyError as e:
            raise exceptions.DataIncompleteError(e.args[0])

    def check_answer(self, answer):
        """Check if `answer` matches the question's answer."""
        return self.answer == answer, self.answer

    def to_dict(self):
        """Returns a dictionary representation of the question."""
        return self._data


class MCQQuestion(Question):
    """Representation of an MCQ-format question. The dictionary representation
    returned by the `to_dict` method of a `MCQQuestion` object looks like this:
    ```py
    {
        "_type": "mcq",
        "term": "term",
        "options": {
            "option1": False,
            "option2": False,
            "option3": True,
            "option4": False,
        },
        "answer": "answer"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to choose a term's definition or vice/versa.
    * `options` is the list of potential answer choices.
    * `answer` is correct choice out of `options`.
    """

    def __init__(self, term, options, answer):
        super().__init__(
            {"_type": "mcq", "term": term, "options": options, "answer": answer}
        )
        self.options = options


class FRQQuestion(Question):
    """Representation of an FRQ-format question. The dictionary representation
    returned by the `to_dict` method of a `FRQQuestion` object looks like this:
    ```py
    {
        "_type": "frq",
        "term": "term",
        "answer": "answer"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to define a term's definition or vice/versa.
    * `answer` is the response that will be accepted as correct given the user's prompt.
    """

    def __init__(self, term, answer):
        super().__init__({"_type": "frq", "term": term, "answer": answer})


class TrueFalseQuestion(Question):
    """Representation of a True-or-false format question. The dictionary representation
    returned by the `to_dict` method of a `TrueFalseQuestion` object looks like this:
    ```py
    {
        "_type": "tf",
        "term": "term",
        "def": "definition",
        "answer": "answer"
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to select True
    or False if the definition given matches with a specific term, or vice/versa.
    * `def` is what the user has to determine is True or False.
    * `answer` is the actual definition that matches with the given `prompt`, or term.
    """

    def __init__(self, term, definition, answer):
        super().__init__(
            {"_type": "tf", "term": term, "def": definition, "answer": answer}
        )
        self.definition = definition


class MatchQuestion(Question):
    """Representation of a Matching format question. The dictionary representation
    returned by the `to_dict` method of a `MatchQuestion` object looks like this:
    ```py
    {
        "_type": "match",
        "term": [
            "term1",
            "term2",
            "term3",
            "term4"
        ],
        "def": [
            "definition4",
            "definition2",
            "definition1",
            "definition3",
        ],
        "answer": {
            "term1": "definition1",
            "term2": "definition2",
            "term3": "definition3",
            "term4": "definition4"
        }
    }
    ```
    Here's a brief overview:
    * `term` is what the user will be prompted with, whether that be to match the
    term with the definition, or vice/versa.
    * `def` is what the user has to match with the corresponding terms.
    * `answer` maps the terms `term` to their actual definitions `def`.
    """

    def __init__(self, term, definitions, answer):
        super().__init__(
            {"_type": "match", "term": term, "def": definitions, "answer": answer}
        )
        self.definitions = definitions


def _get_term_and_def(terms, term, answer_with="def"):
    """(for internal package use) retrieve a term and definition based on `answer_with`."""
    reverse = False
    if answer_with == "both":
        reverse = random.random() < 0.5
    elif answer_with == "term":
        reverse = True
    if reverse:
        return terms[term], term
    return term, terms[term]


def get_terms(terms, answer_with="def"):
    """Returns the dictionary `terms` modified based on the value for `answer_with`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    * `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered.
    """
    terms_copy = deepcopy(terms)
    for term in terms:
        new_term, new_def = _get_term_and_def(terms, term, answer_with)
        terms_copy[new_term] = new_def
    return terms_copy


def _get_random_terms(terms, n_terms=1):
    """(for internal package use) retrieve `n_terms` terms from `terms`."""
    terms_copy = deepcopy(terms)
    random_terms = []
    for i in range(n_terms):
        possible_terms = list(terms_copy.keys())
        try:
            random_term = random.choice(possible_terms)
        except IndexError:
            return
        random_terms.append(random_term)
        del terms_copy[random_term]
    return random_terms


def get_frq_question(terms, **kwargs):
    """Returns an `FRQQuestion` object with a random FRQ-format question generated from `terms`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    """
    term = _get_random_terms(terms)
    return FRQQuestion(term=term, answer=terms[term[0]])


def get_mcq_question(terms, n_options=4, **kwargs):
    """Returns an `MCQQuestion` object with a random MCQ-format question generated from `terms`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    * `n_options = 4`: number of options per question.
    """
    if (not n_options) or (n_options > len(terms)):
        raise exceptions.InvalidOptionsError(n_options)

    options = _get_random_terms(terms, n_options)
    term = random.choice(options)
    answer_choices = [terms[option] for option in options]
    return MCQQuestion(term=[term], options=answer_choices, answer=terms[term])


def get_true_false_question(terms, **kwargs):
    """Returns an `TrueFalseQuestion` object with a random True-or-false format question generated from `terms`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    """
    term = _get_random_terms(terms, 2)
    definition, answer = terms[term[0]], True
    if random.random() < 0.5:
        definition, answer = terms[term[1]], False
    return TrueFalseQuestion(term=term, definition=definition, answer=answer)


def get_match_question(terms, n_terms=5, **kwargs):
    """Returns a `MatchQuestion` object with a Matching format question generated from `terms`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    * `n_terms = 5`: how many terms have to be matched.
    """
    if (not n_terms) or (n_terms > len(terms)):
        raise exceptions.InvalidTermsError(n_terms)

    term = _get_random_terms(terms, n_terms)
    definitions = []
    for t in term:
        definitions.append(terms[t])
    answer = dict(zip(term, definitions))
    random.shuffle(definitions)
    return MatchQuestion(term=term, definitions=definitions, answer=answer)


def get_random_question(terms, types=["mcq", "frq", "tf"], n_options=4, n_terms=5):
    """Returns a `Question` object of a random-format question generated from `terms`.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    * `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`;
    types of questions that appear on the quiz.
    * `n_options = 4`: (if MCQs are involved) number of options per MCQ question.
    * `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question.
    """
    quiz_types = {
        "mcq": get_mcq_question,
        "frq": get_frq_question,
        "tf": get_true_false_question,
        "match": get_match_question,
    }
    try:
        get_question = quiz_types[random.choice(types)]
    except KeyError as e:
        raise exceptions.InvalidQuestionError(e.args[0])
    return get_question(terms, n_options=n_options, n_terms=n_terms)


def get_quiz(
    terms,
    types=["mcq", "frq", "tf"],
    length=10,
    answer_with="def",
    n_options=4,
    n_terms=5,
):
    """Returns a `Quiz` object with random questions based on the parameters below.

    ## Parameters
    * `terms`: map of terms and definitions for quiz.
    * `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`;
    types of questions that appear on the quiz.
    * `length = 10`: number of questions on quiz.
    * `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered.
    * `n_options = 4`: (if MCQs are involved) number of options per MCQ question.
    * `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question.
    """
    if (not length) or (length > len(terms)):
        raise exceptions.InvalidLengthError(length)

    quiz = []
    terms_copy = get_terms(terms, answer_with)
    for i in range(length):
        question = get_random_question(
            terms_copy, types=types, n_options=n_options, n_terms=n_terms
        )
        quiz.append(question)
        for t in question.term:
            del terms_copy[t]
        if (len(terms_copy) < n_terms) or (len(terms_copy) < n_options):
            terms_copy = get_terms(terms, answer_with)
    return Quiz(quiz)
