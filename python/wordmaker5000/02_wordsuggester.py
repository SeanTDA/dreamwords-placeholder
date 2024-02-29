import gensim.downloader as api
from gensim.models import KeyedVectors
import gensim
from typing import List
import random

# Your list of words
with open("01_auto_words.txt", 'r') as f:
    words = [line.strip() for line in f]

# Shuffle the words before processing
random.shuffle(words)

print("Loading Model")

model_path = 'GoogleNews-vectors-negative300.bin'
model = KeyedVectors.load_word2vec_format(model_path, binary=True)

print("Loaded Model")


# Find similar words
def find_similar_words(word_list: List[str], top_n: int = 5) -> List[str]:
    similar_words = set()

    wordsProcessed = 0

    for word in word_list:

        if word in model:
            print("--- Processing [" + word + "]")
            print(str(wordsProcessed) + " / " + str(len(word_list)))
            wordsProcessed+=1
            results = model.most_similar(word, topn=top_n)
            for result in results:
                similar_word, similarity = result
                similar_word = similar_word.replace('_', ' ').lower()
                if len(similar_word.split()) > 1:
                    similar_word = similar_word.split()[0]
                similar_words.add(similar_word)
                print("Adding: " + similar_word)
        else:
            print(f"{word} not in the pre-trained model vocabulary.")
        
        # Save the unique suggested words into a file called 'words_suggested.txt'
        with open('02_auto_words_suggested.txt', 'w') as f:
            for word in similar_words:
                f.write(f"{word}\n")

    return list(similar_words)

# Generate new suggested words
suggested_words = find_similar_words(words, top_n=5)

# Remove any words that already exist in the original list
suggested_words = [word for word in suggested_words if word not in words]

# Print suggested words
print("\nSuggested words to add:")
for word in suggested_words:
    print(word)
