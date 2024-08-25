from copy import deepcopy
import random

class Quiz:
    def __init__(self, data):
        self.questions = data
    
    def to_list(self):
        return [q.to_dict() for q in self.questions]

class Question:
    def __init__(self, data):
        self._data = data
        self.term = data["term"]
        self.answer = data["answer"]
    
    def check_answer(self, answer):
        return self.answer == answer, self.answer
    
    def to_dict(self):
        return self._data

class MCQQuestion(Question):
    def __init__(self, term, options, answer):
        super().__init__({
            "_type": "mcq",
            "term": term,
            "options": options,
            "answer": answer
        })
        self.options = options

class FRQQuestion(Question):
    def __init__(self, term, answer):
        super().__init__({
            "_type": "frq",
            "term": term,
            "answer": answer
        })

class TrueFalseQuestion(Question):
    def __init__(self, term, definition, answer):
        super().__init__({
            "_type": "tf",
            "term": term,
            "def": definition,
            "answer": answer
        })
        self.definition = definition

class MatchQuestion(Question):
    def __init__(self, term, definitions, answer):
        super().__init__({
            "_type": "match",
            "term": term,
            "def": definitions,
            "answer": answer
        })
        self.definitions = definitions

def _get_term_and_def(terms, term, answer_with="def"):
    reverse = False
    if answer_with == "both":
        reverse = random.random() < 0.5
    elif answer_with == "term":
        reverse = True
    if reverse:
        return terms[term], term
    return term, terms[term]

def get_terms(terms, answer_with="def"):
    terms_copy = deepcopy(terms)
    for term in terms:
        new_term, new_def = _get_term_and_def(terms, term, answer_with)
        terms_copy[new_term] = new_def
    return terms_copy

def _get_random_terms(terms, n_terms=1):
    terms_copy = deepcopy(terms)
    random_terms = []
    for i in range(n_terms):
        possible_terms = list(terms_copy.keys())
        random_term = random.choice(possible_terms)
        random_terms.append(random_term)
        del terms_copy[random_term]
    return random_terms

def get_frq_question(terms, **kwargs):
    term = _get_random_terms(terms)
    return FRQQuestion(term=[term], answer=terms[term[0]])

def get_mcq_question(terms, n_options=4, **kwargs):
    options = _get_random_terms(terms, n_options)
    term = random.choice(options)
    return MCQQuestion(term=[term], options=options, answer=terms[term])

def get_true_false_question(terms, **kwargs):
    term = _get_random_terms(terms, 2)
    definition, answer = terms[term[0]], True
    if (random.random() < 0.5):
        definition, answer = terms[term[1]], False
    return TrueFalseQuestion(term=[term], definition=definition, answer=answer)

def get_match_question(terms, **kwargs):
    term = _get_random_terms(terms, n_terms=5)
    definitions = []
    for t in term:
        definitions.append(terms[t])
    answer = dict(zip(term, definitions))
    random.shuffle(definitions)
    return MatchQuestion(term=term, definitions=definitions, answer=answer)

def get_random_question(terms, types=["mcq", "frq", "tf"], n_options=4, n_terms=5):
    quiz_types = {
        "mcq": get_mcq_question,
        "frq": get_frq_question,
        "tf": get_true_false_question,
        "match": get_match_question,
    }
    get_question = quiz_types[random.choice(types)]
    return get_question(terms, n_options=n_options, n_terms=n_terms)

def get_quiz(
        terms,
        types=["mcq", "frq", "tf"],
        length=10,
        answer_with="def",
        n_options=4,
        n_terms=5):
    quiz = []
    terms_copy = get_terms(terms, answer_with)
    for i in range(length):
        question = get_random_question(
            terms_copy,
            types=types,
            n_options=n_options,
            n_terms=n_terms
        )
        quiz.append(question)
        for t in question.term:
            del terms_copy[t]
    return Quiz(quiz)
