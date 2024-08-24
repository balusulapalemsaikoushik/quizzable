# quizzical

## Overview
`quizzical` provides an easy-to-implement interface to build a framework for educational quiz apps built on top of Python. The standard `quizzical` library contains functions for the generation of MCQ, FRQ, or True-or-false quizzes, or a general-purpose quiz that consists of a random number of the previous forms of questions.

## Functions
Every function below takes a dictionary argument `terms` as well as an optional value for positive integer `length`. `length` is very simply the desired number of questions on the quiz. `terms` should be a dictionary mapping _terms_ to _definitions_, where in this case a _term_ represents a question or vocabulary term, and a _definition_ is used to refer to the answer or vocabulary definition. For example, here is an example value for the object `terms` where each term is an English word, and its definition is its English translation:

```py
{
    "painter": "la pintura",
    "brush": "el pincel",
    "sculptor": "la escultura",
    "palette:": "la paleta",
    "self-portrait": "el autorretrato",
    "abstract": "abstracto/a"
}
```

Every function returns a dictionary containing the questions generated by `quizzical`, each in dictionary format also. Each question has a `_type` key, which can be used to determine how to render a question on the frontend (i.e. display multiple options for MCQ, textbox for FRQ, etc.).

### `get_frq`

Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `length = 10`: number of questions on quiz

Returns a dictionary object in the following format:
```py
{
    "prompt": {
        "_type": "frq",
        "answer": "answer"
    },
    # more questions...
}
```

Here's a brief overview:
* `prompt` is what the user will be prompted with, whether that be to define a term's definition or vice/versa.
* `answer` is the response that will be accepted as correct given the user's prompt.

### `get_mcq`

Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `length = 10`: number of questions on quiz
* `n_options = 4`: number of options per question.

Returns a dictionary object in the following format:
```py
{
    "prompt": {
        "_type": "mcq",
        "options": {
            "option1": False,
            "option2": False,
            "option3": True,
            "option4": False,
        }
    },
    # more questions...
}
```

Here's a brief overview:
* `prompt` is what the user will be prompted with, whether that be to choose a term's definition or vice/versa.
* `options` is a dictionary mapping the potential answer choices to whether they are the correct answer (i.e. `True` means correct, `False` means incorrect).

### `get_true_false`

Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `length = 10`: number of questions on quiz

Returns a dictionary object in the following format:
```py
{
    "prompt": {
        "_type": "tf",
        "definition": "definition",
        "answer": "answer"
    },
    # more questions...
}
```

Here's a brief overview:
* `prompt` is what the user will be prompted with, whether that be to select True or False if the definition given matches with a specific term, or vice/versa.
* `definition` is what the user has to determine is True or False. `answer` is the actual definition that matches with the given `prompt`, or term.

### `get_quiz`

Parameters:
* `terms`: map of terms and definitions for quiz (see [Functions](#functions))
* `types = ["mcq", "frq", "tf"]`: list that can contain `"mcq"`, `"frq"`, or `"tf"`; types of questions that appear on the quiz
* `length = 10`: number of questions on quiz
* `answer_with = "def"`: can be `"term"`, `"def"`, or `"both"`; how the question should be answered with
* `n_options = 4`: (if MCQs are involved) number of options per MCQ question

Example 3 question quiz returned by this function:
```py
{
    "la iglesia": {
        "_type": "tf",
        "definition": "shop",
        "answer": "church"
    },
    "la playa": {
        "_type": "mcq",
        "options": {
            "beach": True,
            "park": False,
            "downtown": False,
            "museum": False,
        }
    },
    "park": {
        "_type": "frq",
        "answer": "el parque"
    }
}
```

Please see [`get_frq`](#get_frq), [`get_mcq`](#get_mcq), and [`get_true_false`](#get_true_false) for more information on the format of the above questions.

## Contributors
### Sai Koushik Balusulapalem
[GitHub](https://github.com/balusulapalemsaikoushik)
