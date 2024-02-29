import os
import json

def get_json_files_with_metadata(path):
    json_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def get_unique_words_from_solution(json_files):
    unique_words = set()

    for file in json_files:
        with open(file, "r") as f:
            data = json.load(f)

            if "solution" in data:
                words = data["solution"].split(" ")
                for word in words:
                    unique_words.add(word)

    return unique_words

def save_unique_words_to_file(unique_words, output_file):
    with open(output_file, "w") as f:
        for word in sorted(unique_words):
            f.write(f"{word}\n")




if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    output_file = "01_auto_words.txt"

    json_files = get_json_files_with_metadata(root_dir)
    unique_words = get_unique_words_from_solution(json_files)
    save_unique_words_to_file(unique_words, output_file)
    '''
    
    categories = categorise_words(output_file)
    with open('03_categories.json', 'w') as f:
        json.dump(categories, f, indent=2)
    print("Categories saved")
    '''
    
