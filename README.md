# quizzical
`quizzical` provides an easy-to-implement interface to build a framework for educational quiz apps built on top of Python. The `quizzical` library contains functions for the generation of quizzes consisting of MCQ, FRQ, True-or-false, or Matching questions, allowing you to build educational apps that leverage the power of Python with great ease. Learn more in the documentation below.

## Table of Contents
* [Classes](#classes)
    * [`Quiz`](#quiz)
        * [`Quiz.to_list()`](#quizto_list)
    * [`Question`](#question)
        * [`Question.check_answer(...)`](#questioncheck_answer)
        * [`Question.to_dict()`](#questionto_dict)
    * [`MCQQuestion`](#mcqquestion)
    * [`FRQQuestion`](#frqquestion)
    * [`TrueFalseQuestion`](#truefalsequestion)
    * [`MatchQuestion`](#matchquestion)
* [Functions](#classes)
    * [`get_terms`](#get_terms)
    * [`get_frq_question`](#get_frq_question)
    * [`get_mcq_question`](#get_match_question)
    * [`get_true_false_question`](#get_true_false_question)
    * [`get_match_question`](#get_match_question)
    * [`get_quiz`](#get_quiz)
* [Contributors](#contributors)

## Classes

### `Quiz`
Quiz object with the following attributes:
* `questions`: list of questions within the quiz, represented by a list of arbitrary `Question` objects.

#### `Quiz.to_list()`
Returns a listlike representation of the quiz, with each `Question` object being represented as its dictionary representation. For example, it could look like this:
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

Please see documentation for [`MCQQuestion`](#mcqquestion), [`FRQQuestion`](#frqquestion), [`TrueFalseQuestion`](#truefalsequestion), and [`MatchQuestion`](#matchquestion) for more information on the format of the above questions.

### `Question`
Generic question object used for reconstruction of a question from JSON data, with the following input parameters:
* `data`: dictionary used to reconstruct the `Question` object

And these attributes:
* `term`: question that the user is prompted with
* `answer`: correct answer to the prompt `term`.

#### `Question.check_answer(...)`
Parameters:
* `answer`: answer provided by the user

Returns a tuple: the first item is a boolean whose value is `True` if `answer` matches the question's `answer` attribute or `False` otherwise, and the second item is the value for the question's `answer` attribute.

#### `Question.to_dict()`
Returns a dictionary representation of the question. Each question has a `_type` key that can be used to determine how to render a question on the frontend (i.e. display multiple options for MCQ, textbox for FRQ, etc.), and a `term` key which represents the term the user is prompted with. Please see documentation for [`MCQQuestion`](#mcqquestion), [`FRQQuestion`](#frqquestion), [`TrueFalseQuestion`](#truefalsequestion), and [`MatchQuestion`](#matchquestion) for more information.

### `MCQQuestion`
Representation of an MCQ-format question. Has the same attributes as [`Question`](#question) objects, with the following additional properties:
* `options`: list of potential answer choices.

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
* `definition`: what the user has to determine is True or False.

The dictionary representation returned by the `to_dict` method of a `TrueFalseQuestion` object looks like this:
```py
{
    "_type": "tf",
    "term": "term",
    "def": "definition",
    "answer": "answer"
}
```

Here's a brief overview:
* `term` is what the user will be prompted with, whether that be to select True or False if the definition given matches with a specific term, or vice/versa.
* `def` is what the user has to determine is True or False.
* `answer` is the actual definition that matches with the given `prompt`, or term.

### `MatchQuestion`
Representation of an MCQ-format question. Has the same attributes as [`Question`](#question) objects, with the following additional properties:
* `options`: list of potential answer choices.
* `def` what the user has to match with the corresponding terms.

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
* `term` is what the user will be prompted with, whether that be to match the term with the definition, or vice/versa.
* `def` is what the user has to match with the corresponding terms.
* `answer` maps the terms `term` to their actual definitions `def`.

## Functions
Every function below takes a dictionary argument `terms` and optional values for positive integer `length` and string value `answer_with`.

`length` is very simply the desired number of questions on the quiz.

`answer_with` describes how the user should answer the question, where `"term"` means a question should be answered by giving the term, `"def"` implies that the question should be answered by providing the definition, and `"both"` means that there is a 50/50 chance of the question needing a term or a definition as input.

`terms` should be a dictionary mapping _terms_ to _definitions_, where in this case a _term_ represents a question or vocabulary term, and a _definition_ is used to refer to the answer or vocabulary definition. For example, here is an example value for the object `terms` where each term is an English word, and its definition is its English translation:

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

### `get_terms`
Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered (see [Functions](#functions))

Returns the dictionary `terms` modified based on the value for `answer_with`. May be useful for making flashcards for which terms and definitions may need to be swapped on-demand.

### `get_frq_question`
Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))

Returns an [`FRQQuestion`](#frqquestion) object with a random FRQ-format question generated from `terms`.

### `get_mcq_question`
Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `n_options = 4`: number of options per question.

Returns an [`MCQQuestion`](#mcqquestion) object with a random MCQ-format question generated from `terms`.

### `get_true_false_question`
Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))

Returns a [`TrueFalseQuestion`](#truefalsequestion) object with a random True-or-false format question generated from `terms`.

### `get_match_question`
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `n_terms = 5`: how many terms have to be matched

Returns a [`MatchQuestion`](#matchquestion) object with a random matching-format question generated from `terms`.

### `get_quiz`
Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, `"tf"`, or `"match"`; types of questions that appear on the quiz
* `length = 10`: number of questions on quiz
* `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered (see [Functions](#functions))
* `n_options = 4`: (if MCQs are involved) number of options per MCQ question
* `n_terms = 5`: (if matching questions are involved) number of terms to match per matching question

Returns a [`Quiz`](#quiz) object with random questions based on the above parameters.

## Contributors
### Sai Koushik Balusulapalem
[GitHub](https://github.com/balusulapalemsaikoushik)
