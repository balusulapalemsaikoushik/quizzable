from copy import deepcopy
import random
# import json

def get_terms(terms, answer_with="def"):
    reverse = False
    if answer_with == "both":
        reverse = random.random() < 0.5
    elif answer_with == "term":
        reverse = True
    if reverse:
        terms_copy = {}
        for term in terms:
            terms_copy[terms[term]] = term
    else:
        terms_copy = deepcopy(terms)
    return terms_copy

def _get_quiz(func, terms, length=10, answer_with="def", **kwargs):
    quiz = {}
    terms_copy = get_terms(terms, answer_with)
    for i in range(length):
        possible_terms = list(terms_copy.keys())
        term = random.choice(possible_terms)
        quiz[term] = func(terms, term, **kwargs)
    return quiz

def _get_frq_question(terms, term, **kwargs):
    return {"_type": "frq", "answer": terms[term]}

def _get_mcq_question(terms, term, n_options=4, **kwargs):
    options = [(terms[term], True)]
    possible_options = list(terms.keys())
    for k in range(n_options - 1):
        option_term = random.choice(possible_options)
        options.append([terms[option_term], False])
    random.shuffle(options)
    return {"_type": "mcq", "options": dict(options)}

def _get_true_false_question(terms, term, **kwargs):
    definition, answer = terms[term], True
    possible_decoys = list(terms.keys())
    if (random.random() < 0.5):
        definition = terms[random.choice(possible_decoys)]
        answer = False
    return {"_type": "tf", "def": definition, "answer": answer}

def _get_random_question(terms, term, types=["mcq", "frq", "tf"], n_options=4):
    quiz_types = {
        "mcq": _get_mcq_question,
        "frq": _get_frq_question,
        "tf": _get_true_false_question,
    }
    get_question = quiz_types[random.choice(types)]
    return get_question(terms, term, n_options=n_options)

def get_frq(terms, length=10, answer_with="def"):
    return _get_quiz(_get_frq_question, terms, length, answer_with)

def get_mcq(terms, length=10, answer_with="def", n_options=4):
    return _get_quiz(_get_mcq_question, terms, length, answer_with, n_options=n_options)

def get_true_false(terms, length=10, answer_with="def"):
    return _get_quiz(_get_true_false_question, terms, length, answer_with)

def get_random(terms, types=["mcq", "frq", "tf"], length=10, answer_with="def", n_options=4):
    return _get_quiz(_get_random_question, terms, length, answer_with, types=types, n_options=n_options)

if __name__ == "__main__":
    # with open("literature.json") as terms_file:
    #     terms = json.loads(terms_file.read())
    
    # questions = get_random(terms, answer_with="both")
    # with open("questions.json", "w") as questions_file:
    #     questions_file.write(json.dumps(questions))

    pass
