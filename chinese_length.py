import stiff.fixes  # noqa: F401

from nltk.corpus import wordnet

for lang in ["cmn", "qcn", "qwc"]:
    cnt = 0
    errs = 0
    synsets = set()
    senses = 0
    for lemma in wordnet.all_lemma_names(lang=lang):
        try:
            new_synsets = wordnet.synsets(lemma, lang=lang)
        except:
            errs += 1
        else:
            senses += len(new_synsets)
            synsets.update(new_synsets)
        if len(lemma) == 1:
            cnt += 1
    print(lang)
    print("Single character words", cnt)
    print("Number of lemmas", len(wordnet.all_lemma_names(lang=lang)))
    print("Number of synsets", len(synsets))
    print("Number of senses", senses)
    print("Errors", errs)
