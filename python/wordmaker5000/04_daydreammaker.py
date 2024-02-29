import random
import json

# Load the JSON file
with open("03_saved_categories.json") as f:
    categories = json.load(f)

# Define the probabilities and patterns
patterns = [
    {"c": ["nouns", "nouns", "nouns"],"p": 50}, # pond panda snowman
    {"c": ["nouns", "nouns", "adjectives"],"p": 30},  #molten dog cat
    {"c": ["nouns", "adjectives", "adjectives"],"p": 25}, #nautical spherical bar
    {"c": ["nouns", "nouns", "verbs"],"p": 15}, 
    {"c": ["nouns", "nouns", "adverbs"],"p": 15}, 
    {"c": ["nouns", "adjectives", "object"],"p": 15}, 
    {"c": ["nouns", "adjectives", "animal"],"p": 15}, 
    {"c": ["nouns", "object", "object"],"p": 15}, 
    {"c": ["nouns", "adjectives", "object"],"p": 15}, 


]


'''
nouns : 2695
verbs : 201
adjectives : 151
adverbs : 24

shape : 62
object : 209
animal : 493
'''




def has_matching_letters(words):
    for i, word1 in enumerate(words):
        for j, word2 in enumerate(words):
            if i != j:
                if any(letter in word2 for letter in word1):
                    break
        else:
            return False
    return True



for i in range(10):

    word_sets = []
    for i in range(150):
        # Choose a pattern based on the probabilities
        rand_num = random.random()
        pattern = None
        for p in patterns:
            if rand_num < p["p"]:
                pattern = p
                break
        if pattern is None:
            pattern = patterns[-1]

        # Choose three random words from the selected categories
        words = []
        while len(words) < 3:
            word = random.choice(categories[pattern["c"][len(words)]])
            if word not in words:
                words.append(word)

        # Make sure the words are not featured in any previous set
        while any(set(words) == set(ws) for ws in word_sets):
            words = []
            while len(words) < 3:
                word = random.choice(categories[pattern["c"][len(words)]])
                if word not in words:
                    words.append(word)

        # Add the set of words to the list of word sets
        word_sets.append(words)

    # Print the sets of words
    
    filtered_word_sets = [words for words in word_sets if has_matching_letters(words)]
    for words in filtered_word_sets:
        print(" ".join(words))
