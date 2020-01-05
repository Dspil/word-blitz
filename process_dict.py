from tree_struct import *

witht = 'άέήίϊΐόύϋΰώ'
withoutt = 'αεηιιιουυυω'
d = dict(zip(list(witht), list(withoutt)))
words = []
fhandle = ["".join([d.get((j.lower()), j).upper() for j in i]) for i in open("greek2.raw", 'r').read().split('\n')[:-1]]
fhandle = [i for i in fhandle if len(i) > 1]
l = lexicon(alphabet = list('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'))
l.add_words(fhandle)
l.save("lexicon.wb")
print("done")

