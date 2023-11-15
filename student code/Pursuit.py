gamma = 0.02
lambdda = 0.001
theta = 0.9
lexicon = {}
def pursuitVanilla(utterance, associations):
    for word in utterance[0]:
        wmax = 0
        if word not in associations.keys():
            associations[word] = {initializePursuit(utterance, associations) : gamma}
        for meaning, weight in associations[word].items():
            if weight > wmax:
                wmax = weight
                match = meaning
        if match in utterance[1]:
            associations[word][match] = associations[word][match] + gamma * (1 - associations[word][match])
            if lexicalize(word, associations[word]):
                associations.pop(word)
                break
        else:
            associations[word][match] = associations[word][match] * (1 - gamma)
    return(associations)


def initializePursuit(utterance, associations):
    amin = 1
    for meaning in utterance[1]:
        amax = 0
        for w in associations.values():
            weight = w.get(meaning)
            if weight is not None and weight > amax:
                amax = w.get(meaning)
        if amax < amin:
            amin = amax
            hypothesis0 = meaning
    return hypothesis0

def lexicalize(word, wordspace):
    sum = 0
    lexicalized = False
    for weight in wordspace.values():
        sum += weight
    for meaning in wordspace:
        prob = (wordspace[meaning] + lambdda) / sum + (gamma * len(wordspace))
        if prob > theta:
            lexicon[word] = meaning
            lexicalized = True
            break
    return lexicalized


example = [["cat"], ["CAT", "DOG"]]

ex_associations = {
    "dog": {
        "DOG": 0.8,
        "CAT": 0.1
    },
    "whisker": {
        "CAT": 0.6
    },
    "ball": {
        "CAT": 0.1
    }
}

pursuitVanilla(example, ex_associations)

##cleanup
corpus = []
f = open("train.txt", "r")
for line in f:
    arr = line.split()
    corpus.append(arr)
words = corpus[::3]
meanings = corpus[1::3]
