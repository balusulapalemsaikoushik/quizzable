from copy import deepcopy
import random
# import json

def get_frq(terms, length=10, reverse=False, **kwargs):
    frq = {}
    if reverse:
        terms_copy = {}
        for term in terms:
            terms_copy[terms[term]] = term
    else:
        terms_copy = deepcopy(terms)
    for i in range(length):
        possible_terms = list(terms_copy.keys())
        term = random.choice(possible_terms)
        frq[term] = {"_type": "frq", "answer": terms_copy[term]}
        del terms_copy[term]
    return frq

def get_mcq(terms, length=10, n_options=4, reverse=False, **kwargs):
    mcq = {}
    if reverse:
        terms_copy = {}
        for term in terms:
            terms_copy[terms[term]] = term
    else:
        terms_copy = deepcopy(terms)
    for i in range(length):
        possible_terms = list(terms_copy.keys())
        term = random.choice(possible_terms)
        options = [(terms_copy[term], True)]
        del terms_copy[term]
        possible_options = list(terms_copy.keys())
        for k in range(n_options - 1):
            option_term = random.choice(possible_options)
            options.append([terms_copy[option_term], False])
        random.shuffle(options)
        mcq[term] = {"_type": "mcq", "options": dict(options)}
    return mcq

def get_true_false(terms, length=10, reverse=False, **kwargs):
    true_false = {}
    if reverse:
        terms_copy = {}
        for term in terms:
            terms_copy[terms[term]] = term
    else:
        terms_copy = deepcopy(terms)
    for i in range(length):
        possible_terms = list(terms_copy.keys())
        term = random.choice(possible_terms)
        definition, answer = terms_copy[term], True
        del terms_copy[term]
        possible_decoys = list(terms_copy.keys())
        if (random.random() < 0.5):
            definition = terms_copy[random.choice(possible_decoys)]
            answer = False
        true_false[term] = {"_type": "tf", "def": definition, "answer": answer}
    return true_false

def get_quiz(terms, types=["mcq", "frq", "tf"], length=10, answer_with="def", n_options=4):
    quiz_types = {
        "mcq": get_mcq,
        "frq": get_frq,
        "tf": get_true_false,
    }
    quiz = {}
    for i in range(length):
        get_question = quiz_types[random.choice(types)]
        reverse = False
        if answer_with == "both":
            reverse = random.random() < 0.5
        elif answer_with == "term":
            reverse = True
        question = get_question(terms, length=1, reverse=reverse, n_options=n_options)
        quiz.update(question)
    return quiz

if __name__ == "__main__":
    # with open("literature.json") as terms_file:
    #     terms = json.loads(terms_file.read())
    
    # questions = get_quiz(terms, answer_with="both")
    # with open("questions.json", "w") as questions_file:
    #     questions_file.write(json.dumps(questions))

    pass
