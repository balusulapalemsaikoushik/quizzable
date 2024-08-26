# quizzable
[![Test](https://github.com/balusulapalemsaikoushik/quizzable/actions/workflows/test.yml/badge.svg)](https://github.com/balusulapalemsaikoushik/quizzable/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`quizzable` provides an easy-to-implement interface to build a framework for educational quiz apps built on top of Python. The `quizzable` library allows you to create quizzes consisting of MCQ, FRQ, True-or-false, or Matching questions, allowing you to build educational apps that leverage the power of Python with great ease. The full documentation is described below.

## Table of Contents
* [Quickstart](#quickstart)
* [Classes](#classes)
    * [`Terms`](#terms)
        * [`Terms.get_terms()`](#termsget_terms)
        * [`Terms.get_frq_question()`](#termsget_frq_question)
        * [`Terms.get_mcq_question()`](#termsget_mcq_question)
        * [`Terms.get_true_false_question()`](#termsget_true_false_question)
        * [`Terms.get_match_question()`](#termsget_match_question)
        * [`Terms.get_random_question()`](#termsget_random_question)
        * [`Terms.get_quiz()`](#termsget_quiz)
    * [`Quiz`](#quiz)
        * [`Quiz.questions`](#quizquestions)
        * [`Quiz.from_data()`](#quizfrom_data)
        * [`Quiz.to_data()`](#quizto_data)
    * [`Question`](#question)
        * [`Question.from_dict()`](#questionfrom_dict)
        * [`Question.check_answer()`](#questioncheck_answer)
        * [`Question.to_dict()`](#questionto_dict)
    * [`MCQQuestion`](#mcqquestion)
        * [`MCQQuestion.options`](#mcqquestionoptions)
        * [`MCQQuestion.to_dict()`](#mcqquestionto_dict)
    * [`FRQQuestion`](#frqquestion)
        * [`FRQQuestion.to_dict()`](#frqquestionto_dict)
    * [`TrueFalseQuestion`](#truefalsequestion)
        * [`TrueFalseQuestion.def`](#truefalsequestiondef)
        * [`TrueFalseQuestion.to_dict()`](#truefalsequestionto_dict)
    * [`MatchQuestion`](#matchquestion)
        * [`MatchQuestion.def`](#matchquestiondef)
        * [`MatchQuestion.to_dict()`](#matchquestionto_dict)
* [Exceptions](#exceptions)
    * [`BaseQuizzableException`](#basequizzableexception)
    * [`InvalidLengthError`](#invalidlengtherror)
    * [`InvalidOptionsError`](#invalidoptionserror)
    * [`InvalidTermsError`](#invalidtermserror)
    * [`InvalidQuestionError`](#invalidquestionerror)
    * [`DataIncompleteError`](#dataincompleteerror)
* [Authors](#authors)

## Quickstart

To get started, install the `quizzable` package through `pip` on a supported version of Python (`quizzable` currently supports Python 3.9+):
```console
$ python -m pip install quizzable
```
Next, import the `Terms` class from the `quizzable` module:
```py
from quizzable import Terms
```
Then, create a list of terms:
```py
data = {
    "painter": "la pintura",
    "brush": "el pincel",
    "sculpture": "la escultura",
    "palette:": "la paleta",
    "self-portrait": "el autorretrato",
    "abstract": "abstracto/a",
    # more terms...
}
terms = Terms(data)
```
or create one from JSON data:
```py
import json

with open("vocabulary.json") as terms_file:
    terms = Terms(json.loads(terms_file.read()))
```
Aftewards, you can choose to generate random types of questions using the `get_random_question` method:
```py
question = terms.get_random_question()
```
generate an entire quiz of questions using the `get_quiz` method:
```py
quiz = terms.get_quiz(types=["mcq", "match", "tf"])
```
Or create different types of questions manually like so:
```py
frq = terms.get_frq_question()  # free-response
mcq = terms.get_mcq_question()  # multiple-choice
tf = terms.get_true_false_question()  # true-or-false
matching = terms.get_frq_question()  # matching
```
A question has different properties, depending on its type:
```py
print(f"What is the translation of {mcq.term}?")
for option in mcq.options:
    print(option)
print()
answer = input("Answer: ")
```
To score a question, simply use its `check_answer` method:
```py
correct, actual = mcq.check_answer(answer)
if correct:
    print("Correct!")
else:
    print(f"Incorrect...the answer was {actual}")
```
If you'd like, you can convert a question or quiz to back to its raw data at any time:
```py
print(question.to_dict())
print(quiz.to_data())
```

## Classes

### `Terms`
A list of terms.

Should be a dictionary mapping _terms_ to _definitions_, where in this case a _term_ represents a question or vocabulary term, and a _definition_ is used to refer to the answer or vocabulary definition. For example, here is a list of terms in which each term is an English word, and its definition is its English translation:

```py
{
    "painter": "la pintura",
    "brush": "el pincel",
    "sculpture": "la escultura",
    "palette:": "la paleta",
    "self-portrait": "el autorretrato",
    "abstract": "abstracto/a"
}
```

#### `Terms.get_terms()`
Parameters:
* `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered (see [Functions](#functions))

Returns the dictionary `terms` modified based on the value for `answer_with`. May be useful for making flashcards for which terms and definitions may need to be swapped on-demand.

#### `Terms.get_frq_question()`
Returns an [`FRQQuestion`](#frqquestion) object with a random FRQ-format question generated from `terms`.

#### `Terms.get_mcq_question()`
Parameters:
* `n_options = 4`: number of options per question.

Returns an [`MCQQuestion`](#mcqquestion) object with a random MCQ-format question generated from `terms`.

#### `Terms.get_true_false_question()`
Returns a [`TrueFalseQuestion`](#truefalsequestion) object with a random True-or-false format question generated from `terms`.

#### `Terms.get_match_question()`
Parameters:
* `n_terms = 5`: how many terms have to be matched

Returns a [`MatchQuestion`](#matchquestion) object with a random matching-format question generated from `terms`.

#### `Terms.get_random_question()`
Parameters:
* `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`; types of questions that appear on the quiz
* `n_options = 4`: (if MCQs are involved) number of options per MCQ question
* `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question

Returns a `Question` object of a random-format question generated from `terms`.

#### `Terms.get_quiz()`
Returns a [`Quiz`](#quiz) object with random questions based on the below parameters.

Parameters:
* `terms`: map of terms and definitions for quiz (see [`Terms`](#terms))
* `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`; types of questions that appear on the quiz
* `length = 10`: number of questions on quiz
* `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered (see below)
* `n_options = 4`: (if MCQs are involved) number of options per MCQ question
* `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question

`answer_with` describes how the user should answer the question, where `"term"` means a question should be answered by giving the term, `"def"` implies that the question should be answered by providing the definition, and `"both"` means that there is a 50/50 chance of the question needing a term or a definition as input.

### `Quiz`
Arbitrary quiz object.
#### `Quiz.questions`
list of questions within the quiz, represented by a list of arbitrary `Question` objects.

#### `Quiz.from_data()`
Reconstructs a `Quiz` object from a listlike representation. See [`Quiz.to_data()`](#quizto_data) for more information on formatting.

#### `Quiz.to_data()`
Returns a listlike representation of the quiz, with each `Question` object being represented as its dictionary representation. For example, it could look like this:
```py
[
    {
        "_type": "tf",
        "term": "la iglesia",
        "definition": "shop",
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

Please see documentation for [`MCQQuestion`](#mcqquestion), [`FRQQuestion`](#frqquestion), [`TrueFalseQuestion`](#truefalsequestion), and [`MatchQuestion`](#matchquestion) for more information on the format of the above questions.

### `Question`
Generic question object used for reconstruction of a question from JSON data.

Parameters:
* `_type`: question type
* `term`: question term (prompt)
* `answer`: question answer
* `**kwargs`: other question data (e.g. `options`, `definition`, etc.)

#### `Question.term`
Question that the user is prompted with.

#### `Question.answer`
Correct answer to the prompt `term`.

#### `Question.from_dict()`
Returns a reconstructed `Question` object made from `data`. Please see [`MCQQuestion.to_dict()`](#mcqquestionto_dict), [`FRQQuestion.to_dict()`](#frqquestionto_dict), [`TrueFalseQuestion.to_dict()`](#truefalsequestionto_dict), and [`MatchQuestion.to_dict()`](#matchquestionto_dict) for more information on formatting.

Parameters:
* `data`: dictionary containing question data.

#### `Question.check_answer()`
Returns a tuple: the first item is a boolean whose value is `True` if `answer` matches the question's `answer` attribute or `False` otherwise, and the second item is the value for the question's `answer` attribute.

Parameters:
* `answer`: answer provided by the user


#### `Question.to_dict()`
Returns a dictionary representation of the question. Each question has a `_type` key that can be used to determine how to render a question on the frontend (i.e. display multiple options for MCQ, textbox for FRQ, etc.), and a `term` key which represents the term the user is prompted with. Please see [`MCQQuestion.to_dict()`](#mcqquestionto_dict), [`FRQQuestion.to_dict()`](#frqquestionto_dict), [`TrueFalseQuestion.to_dict()`](#truefalsequestionto_dict), and [`MatchQuestion.to_dict()`](#matchquestionto_dict) for more information on formatting.

### `MCQQuestion`
Representation of an MCQ-format question. Has the same attributes as [`Question`](#question) objects, with the following additional properties:

#### `MCQQuestion.options`
List of potential answer choices.

#### `MCQQuestion.to_dict()`
The dictionary representation returned by the `to_dict` method of a `MCQQuestion` object looks like this:
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

### `FRQQuestion`
Representation of an FRQ-format question. Has the same attributes as [`Question`](#question) objects, with the no additional properties.

#### `FRQQuestion.to_dict()`
The dictionary representation returned by the `to_dict` method of a `FRQQuestion` object looks like this:
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

### `TrueFalseQuestion`
Representation of an True-or-false format question. Has the same attributes as [`Question`](#question) objects, with the following additional properties:


#### `TrueFalseQuestion.definition`
What the user has to determine is True or False.

#### `TrueFalseQuestion.to_dict()`
The dictionary representation returned by the `to_dict` method of a `TrueFalseQuestion` object looks like this:
```py
{
    "_type": "tf",
    "term": "term",
    "definition": "definition",
    "answer": "answer"
}
```

Here's a brief overview:
* `term` is what the user will be prompted with, whether that be to select True or False if the definition given matches with a specific term, or vice/versa.
* `definition` is what the user has to determine is True or False.
* `answer` is the actual definition that matches with the given `prompt`, or term.

### `MatchQuestion`
Representation of an MCQ-format question. Has the same attributes as [`Question`](#question) objects, with the following additional properties:

#### `MatchQuestion.def`
What the user has to match with the corresponding terms.

#### `MatchQuestion.to_dict()`
The dictionary representation returned by the `to_dict` method of a `MatchQuestion` object looks like this:
```py
{
    "_type": "match",
    "term": [
        "term1",
        "term2",
        "term3",
        "term4"
    ],
    "definitions": [
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
* `term` is what the user will be prompted with, whether that be to match the term with the definition, or vice/versa.
* `definitions` is what the user has to match with the corresponding terms.
* `answer` maps the terms `term` to their actual definitions `definitions`.

## Exceptions

### `BaseQuizzableException`
The base exception for all `quizzable` errors.

### `InvalidLengthError`
The length specified is not valid (i.e. too short or too long)

Parameters:
* `length`: invalid length of the quiz

### `InvalidOptionsError`
The number of options (for MCQs) specified is not valid (i.e. too small or too large)

Parameters:
* `n_options`: invalid number of options per MCQ question

### `InvalidTermsError`
The number of terms (for matching questions) specified is not valid (i.e. too small or too large)

Parameters:
* `n_terms`: invalid number of terms per matching question

### `InvalidQuestionError`
The type of question specified is not valid (should only be `"mcq"`, `"frq"`, `"tf"`, or `"match"`).

Parameters:
* `question`: invalid type of question

### `DataIncompleteError`
The data passed into the constructor for `Question` is incomplete. See [`MCQQuestion.to_dict()`](#mcqquestionto_dict), [`FRQQuestion.to_dict()`](#frqquestionto_dict), [`TrueFalseQuestion.to_dict()`](#truefalsequestionto_dict), and [`MatchQuestion.to_dict()`](#matchquestionto_dict) for how the data for different types of questions should be formatted.

Parameters:
* `data`: incomplete data

## Authors
### Sai Koushik Balusulapalem
[GitHub](https://github.com/balusulapalemsaikoushik)
