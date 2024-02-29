import nltk
from nltk.corpus import wordnet as wn
import json





def categorise_words(input_files, categories_list):
    nltk.download('wordnet')
    word_list = []
    for input_file in input_files:
        with open(input_file, 'r') as f:
            input_file_word_list = [line.strip() for line in f]
            for word in input_file_word_list:
                word_list.append(word)
    categories = {}
    for category in categories_list:
        categories[category] = []
    for word in word_list:
        synsets = wn.synsets(word)
        for syn in synsets:
            if syn.pos() == 'n':
                categories['nouns'].append(word)
                break
            elif syn.pos() == 'v':
                categories['verbs'].append(word)
                break
            elif syn.pos() == 'a':
                categories['adjectives'].append(word)
                break
            elif syn.pos() == 'r':
                categories['adverbs'].append(word)
                break
        # Check for specific categories
        for syn in synsets:
            for category in categories_list:
                if category in syn.lexname():
                    categories[category].append(word)
                    break
    return categories





if __name__ == "__main__":
    input_files = ["01_saved_words.txt", "02_saved_words_suggested.txt"]

    categories_list = ['nouns', 'verbs', 'adjectives', 'adverbs', 'shape', 'object', 'animal']
    categories = categorise_words(input_files, categories_list)


    for categoryKey in categories.keys():
        print(categoryKey + " : " + str(len(categories[categoryKey])))


    with open('03_auto_categories.json', 'w') as f:
        json.dump(categories, f, indent=2)
    print("Categories saved")