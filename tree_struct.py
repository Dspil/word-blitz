import pickle

class tree:

    def __init__(self, letter, alphabet = None):
        self.letter = letter
        self.finished_word = None
        if alphabet == None:
            self.alphabet = [chr(ord('A') + i) for i in range(26)]
        else:
            self.alphabet = alphabet
        self.neighbors = {}

    
    def from_words_rec_(self, words, sofar = None):
        if sofar == None:
            sofar = []
        words1 = [i[1:] for i in words]
        if len(words1[0]) == 0:
            if self.finished_word == None:
                self.finished_word = sofar + [self.letter]
            words1 = words1[1:]
        if len(words1) == 0:
            return None
        subwords = dict([(i,[]) for i in self.alphabet])
        for i in words1:
            subwords[i[0]].append(i)
        for l, w in subwords.items():
            if len(w) > 0:
                if self.neighbors.get(l) == None:
                    self.neighbors[l] = tree(l, alphabet = self.alphabet)
                self.neighbors[l].from_words_rec_(w, sofar + [self.letter])

                
    def from_words(self, words, sofar = None):
        self.from_words_rec_(sorted(set(words), key = len), sofar)

        
    def display(self):
        self.display_()
        print()

        
    def display_(self):
        print("[" + str(self.letter) + ", {}, [".format(self.finished_word), end = "")
        for i in self.neighbors.values():
            if i != None:
                i.display_()
                print(" ", end = "")
        print("]]", end = "")


class lexicon:

    def __init__(self, words = None, alphabet = None):
        if alphabet == None:
            self.alphabet = [chr(ord('A') + i) for i in range(26)]
        else:
            self.alphabet = alphabet
        self.trees_ = dict()
        self.add_words(words)

    def add_words(self, words):
        if words == None:
            return None
        subwords = dict([(i,[]) for i in self.alphabet])
        for i in words:
            subwords[i[0]].append(i)
        for l, w in subwords.items():
            if len(w) > 0:
                if self.trees_.get(l) == None:
                    self.trees_[l] = tree(l, alphabet = self.alphabet)
                self.trees_[l].from_words(w)

    def save(self, filename):
        with open(filename, 'wb') as fhandle:
            pickle.dump((self.alphabet, self.trees_), fhandle)


    def load(self, filename):
        with open(filename, 'rb') as fhandle:
            self.alphabet, self.trees_ = pickle.load(fhandle)

            
    def display(self):
        for i, t in self.trees_.items():
            print("{}: ".format(i), end = "")
            t.display()
