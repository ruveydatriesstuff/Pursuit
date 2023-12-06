import random
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

gamma = 0.002
lambdda = 0.001
theta = 0.90
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
            ##rewarding random h' when h is disconfirmed
            #randmeaning = random.choice(list(set(utterance[1]) & set(associations[word].items())))
            randmeaning = random.choice(utterance[1])
            if randmeaning not in associations[word].keys() : associations[word][randmeaning] = 0
            associations[word][randmeaning] = associations[word][randmeaning] + gamma * (1 - associations[word][randmeaning])
    return(associations)


def initializePursuit(utterance, associations):
    amin = 1
    if len(associations) == 0:
        return random.choice(utterance[1])
    for meaning in utterance[1]:
        amax = 0
        #hicbir assoc olmadiginda en sonuncuya veriyo oldu.
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
        prob = (wordspace[meaning] + lambdda) / (sum + (gamma * len(wordspace)))
        if prob > theta:
            lexicon[word] = meaning
            lexicalized = True
            break
    return lexicalized

def runModel():
    assoc_space = {}
    for utterance in utterances:
        print(utterance)
        assoc_space = pursuitVanilla(utterance, assoc_space)


def attentionAssigner(utterances, goldcorpus):
    attentions = []
    for line in utterances:
        attention = {}
        n = len(line[1])
        attended = []
        for word in line[0]:
            if word in goldcorpus.keys():
                n += 1
                attended.append(goldcorpus[word])
        if len(attended) == 0:
            n += 1
            attended.append(random.choice(line[1]))
        default = 1 / n
        for referent in line[1]:
            if referent in attended:
                attention[referent] = default * 2
            else:
                attention[referent] = default
        attentions.append(attention)
    return attentions


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

#pursuitVanilla(example, ex_associations)

##cleanup
corpus = []
f = open("train.txt", "r")
for line in f:
    arr = line.split()
    corpus.append(arr)
words = corpus[::3]
meanings = corpus[1::3]
utterances = []
for w, m in zip(words, meanings):
    utterances.append([w,m])


assoc_space = {}
for utterance in utterances:
    print(utterance)
    assoc_space = pursuitVanilla(utterance, assoc_space)
print(assoc_space)
print(lexicon)

f2 = open("train_gold.csv", "r")
goldcorpus = {}
for line in f2:
    assoc = line[:-1].split(",")
    goldcorpus[assoc[0]] = assoc[1]
goldcorpus.pop("Key")
print(goldcorpus)
totalcorrect = 0
totalunmapped = 0
totalincorrect = 0
for word in goldcorpus.keys():
    if word not in lexicon.keys():
        totalunmapped += 1
        continue
    if goldcorpus[word] == lexicon[word]:
        totalcorrect += 1
    else:
        totalincorrect += 1
        #print(word + ", " + goldcorpus[word] + " but " + lexicon[word])
print("'Gold standard' words: " + str(len(goldcorpus.keys())) + "\n Those correctly learned: " + str(totalcorrect) + ", " + str(totalcorrect/len(goldcorpus.keys()))
     + "\n Those not learned: " + str(totalunmapped) + ", " + str(totalunmapped/len(goldcorpus.keys())) +
      "\n Those incorrectly learned: " + str(totalincorrect) + ", " + str(totalincorrect/len(goldcorpus.keys())))

attentions = attentionAssigner(utterances, goldcorpus)
print(attentions)

f3 = open("train_attention.txt", "w")
for w, m, a in zip(words, meanings, attentions):
    word3 = ' '.join(map(str, w))
    meaning3 = ' '.join(map(str, m))
    att3 = ' '.join(map(str, a.values()))

    f3line = word3 + "\n" + meaning3 + "\n" + att3 + "\n\n"
    f3.writelines(f3line)


