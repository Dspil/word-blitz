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
            self.finished_word = sofar + [self.letter]
            words1 = words1[1:]
        subwords = dict([(i,[]) for i in self.alphabet])
        for i in words1:
            subwords[i[0]].append(i)
        for l, w in subwords.items():
            if len(w) > 0:
                self.neighbors[l] = tree(l, alphabet = self.alphabet)
                self.neighbors[l].from_words(w, sofar + [self.letter])
            else:
                self.neighbors[l] = None

                
    def from_words(self, words, sofar = None):
        self.from_words_rec_(sorted(words, key = len), sofar)


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


