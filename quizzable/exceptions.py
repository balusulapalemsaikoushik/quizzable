class BaseQuizzableException(Exception):
    """The base exception for all `quizzable` errors."""

    pass


class InvalidLengthError(BaseQuizzableException):
    """The length specified is not valid (i.e. too short or too long)

    ## Parameters
    * `length`: invalid length of the quiz
    """

    def __init__(self, length, *args, **kwargs):
        super().__init__(
            f"The length {length} is not permitted for this quiz.", *args, **kwargs
        )


class InvalidOptionsError(BaseQuizzableException):
    """The number of options (for MCQs) specified is not valid (i.e. too small or too large)

    ## Parameters
    * `n_options`: invalid number of options per MCQ question
    """

    def __init__(self, n_options, *args, **kwargs):
        super().__init__(
            f"{n_options} options is not permitted for an MCQ question for this quiz.",
            *args,
            **kwargs,
        )


class InvalidTermsError(BaseQuizzableException):
    """The number of terms (for matching questions) specified is not valid (i.e. too small or too large)

    ## Parameters
    * `n_terms`: invalid number of terms per matching question
    """

    def __init__(self, n_terms, *args, **kwargs):
        super().__init__(
            f"{n_terms} terms is not permitted for a matching question for this quiz.",
            *args,
            **kwargs,
        )


class InvalidQuestionError(BaseQuizzableException):
    """The type of question specified is not valid (should only be `"mcq"`, `"frq"`, `"tf"`, or `"match"`).

    ## Parameters
    * `question`: invalid type of question
    """

    def __init__(self, question, *args, **kwargs):
        super().__init__(
            f"The question type '{question}' does not exist.", *args, **kwargs
        )


class DataIncompleteError(BaseQuizzableException):
    """The data passed into the constructor for `Question` is incomplete.

    ## Parameters
    * `data`: incomplete data
    """

    def __init__(self, key, *args, **kwargs):
        super().__init__(
            f"The key '{key}' is missing from the question data.", *args, **kwargs
        )
