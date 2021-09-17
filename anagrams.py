from collections import Counter
from copy import deepcopy

with open('/usr/share/dict/words', 'r') as file:
    os_word_list = file.readlines()
    os_word_list = [word.strip('\n').lower() for word in os_word_list]
    os_word_list = list(filter(lambda x: len(x) > 2, os_word_list))

word_lookup = {word:1 for word in os_word_list}

starts_of_words = {}
for word in os_word_list:
    for ind in range(1,len(word)+1):
        starts_of_words[word[:ind]] = 1

class AnagramFinder():
    def __init__(self, seed):
        self.seed = seed
    
    def get_anagrams(self):
        seed = self.seed

        if len(seed) > 10:
            raise Exception("Input is too long.")

        seed_counter = Counter(seed)

        anagrams = {}

        nexts = []
        for ind in range(len(seed)):
            ltr, tmp =  seed[ind], dict(Counter(seed[:ind]+seed[ind+1:]))
            nexts.append((ltr, tmp))
            if word_lookup.get(ltr):
                anagrams[ltr] = 1

        while len(nexts) > 0:
            new_nexts = []

            for item in nexts:
                for next_letter in item[1].keys():
                    next_stem = item[0]+next_letter
                    if starts_of_words.get(next_stem):
                        if word_lookup.get(next_stem):
                            anagrams[next_stem] = 1
                        new_dict = deepcopy(item[1])
                        new_dict[next_letter] = new_dict[next_letter] - 1
                        if new_dict[next_letter] == 0:
                            del new_dict[next_letter]
                        new_nexts.append((next_stem, new_dict))
            nexts = new_nexts

        anagrams = list(anagrams.keys())

        return anagrams

    def anagrams_by_length(self):
        length_to_anagrams = {}
        for anagram in self.get_anagrams():
            prev_val = length_to_anagrams.get(len(anagram), [])
            length_to_anagrams[len(anagram)] = prev_val + [anagram]

        return(length_to_anagrams)