from nltk.corpus import wordnet
from finntk.wordnet.reader import fiwn
from stiff.data.fixes import fix_all

fix_all()

for wn, lang in ((wordnet, "eng"), (fiwn, "eng"), (wordnet, "fin")):
    lemmas = 0
    errs = 0
    synsets = set()
    for lemma in wn.all_lemma_names(lang=lang):
        try:
            new_synsets = wn.synsets(lemma, lang=lang)
        except:
            errs += 1
        else:
            synsets.update(new_synsets)
        lemmas += 1
    print(wn, lang)
    print("Number of synsets", len(synsets), "errs", errs, "lemmas", lemmas)
