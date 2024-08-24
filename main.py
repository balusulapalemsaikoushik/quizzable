from copy import deepcopy
import random
# import json

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

def _get_quiz(func, terms, length=10, answer_with="def", **kwargs):
    quiz = []
    terms_copy = get_terms(terms, answer_with)
    for i in range(length):
        question, term = func(terms_copy, **kwargs)
        quiz.append(question)
        for t in term:
            del terms_copy[t]
    return quiz

def _get_random_terms(terms, n_terms=1):
    possible_terms = list(terms.keys())
    random_terms = []
    for i in range(n_terms):
        random_terms.append(random.choice(possible_terms))
    return random_terms

def _get_frq_question(terms, **kwargs):
    term = _get_random_terms(terms)
    return {"_type": "frq", "term": term[0], "answer": term[0]}, term

def _get_mcq_question(terms, n_options=4, **kwargs):
    term = _get_random_terms(terms)
    options = [(terms[term[0]], True)]
    possible_options = list(terms.keys())
    for k in range(n_options - 1):
        option_term = random.choice(possible_options)
        options.append([terms[option_term], False])
    random.shuffle(options)
    return {"_type": "mcq", "term": term[0], "options": dict(options)}, term

def _get_true_false_question(terms, **kwargs):
    term = _get_random_terms(terms)
    definition, answer = terms[term[0]], True
    possible_decoys = list(terms.keys())
    if (random.random() < 0.5):
        definition = terms[random.choice(possible_decoys)]
        answer = False
    return {"_type": "tf", "term": term[0], "def": definition, "answer": answer}, term

def _get_match_question(terms, **kwargs):
    term = _get_random_terms(terms, n_terms=5)
    definitions = []
    for t in term:
        definitions.append(terms[t])
    answer = dict(zip(term, definitions))
    random.shuffle(definitions)
    return {"_type": "match", "term": term, "def": definitions, "answer": answer}, term

def _get_random_question(terms, types=["mcq", "frq", "tf"], n_options=4, n_terms=5):
    quiz_types = {
        "mcq": _get_mcq_question,
        "frq": _get_frq_question,
        "tf": _get_true_false_question,
        "match": _get_match_question,
    }
    get_question = quiz_types[random.choice(types)]
    return get_question(terms, n_options=n_options, n_terms=n_terms)

def get_frq(terms, length=10, answer_with="def"):
    return _get_quiz(_get_frq_question, terms, length, answer_with)

def get_mcq(terms, length=10, answer_with="def", n_options=4):
    return _get_quiz(_get_mcq_question, terms, length, answer_with, n_options=n_options)

def get_true_false(terms, length=10, answer_with="def"):
    return _get_quiz(_get_true_false_question, terms, length, answer_with)

def get_match(terms, length=10, answer_with="def", n_terms=5):
    return _get_quiz(_get_match_question, terms, length, answer_with, n_terms=n_terms)

def get_random(
        terms,
        types=["mcq", "frq", "tf"],
        length=10,
        answer_with="def",
        n_options=4,
        n_terms=5):
    return _get_quiz(
        _get_random_question,
        terms,
        length,
        answer_with,
        types=types,
        n_options=n_options,
        n_terms=n_terms
    )

if __name__ == "__main__":
    # with open("literature.json") as terms_file:
    #     terms = json.loads(terms_file.read())
    
    # questions = get_random(terms, types=["mcq", "frq", "match", "tf"], answer_with="def")
    # with open("questions.json", "w") as questions_file:
    #     questions_file.write(json.dumps(questions))

    pass
