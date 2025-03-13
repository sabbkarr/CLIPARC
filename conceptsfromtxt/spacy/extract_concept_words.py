import json
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

with open("descriptions.jsonl", "r") as f:
    data = json.load(f)

print(data[:2])
for item in data:
    doc = nlp(item["description"])
    item["nouns"] = [token.text for token in doc if token.pos_ == "NOUN"]
    item["verbs"] = [token.text for token in doc if token.pos_ == "VERB"]
    item["adjectives"] = [token.text for token in doc if token.pos_ == "ADJ"]
    item["adverbs"] = [token.text for token in doc if token.pos_ == "ADV"]

with open("output_with_pos.json", "w") as f:
    json.dump(data, f, indent=2)

print(len(data))
# descriptions_df = pd.DataFrame(data)
# descriptions_df.to_csv("descriptions_df.csv", index=False)

import re
import ast

descriptions_df = pd.read_csv("descriptions_df.csv")

descriptions_df['nouns'] = descriptions_df['nouns'].apply(ast.literal_eval)
descriptions_df['verbs'] = descriptions_df['verbs'].apply(ast.literal_eval)
descriptions_df['adjectives'] = descriptions_df['adjectives'].apply(ast.literal_eval)
descriptions_df['adverbs'] = descriptions_df['adverbs'].apply(ast.literal_eval)

def has_non_letter(word):
    return re.search(r'[^a-zA-Z]', word)

non_letter_words = {"nouns": set(),"verbs": set(),"adjectives": set(),"adverbs": set()}

for _, row in descriptions_df.iterrows():
    for noun in row['nouns']:
        if has_non_letter(noun):
            non_letter_words['nouns'].add(noun)
    for verb in row['verbs']:
        if has_non_letter(verb):
            non_letter_words['verbs'].add(verb)
    for adjective in row['adjectives']:
        if has_non_letter(adjective):
            non_letter_words['adjectives'].add(adjective)
    for adverb in row['adverbs']:
        if has_non_letter(adverb):
            non_letter_words['adverbs'].add(adverb)
print(descriptions_df.head())

for pos, words in non_letter_words.items():
    print(f"\n{pos.upper()} with non-letter characters:")
    for word in sorted(words):
        print(word)


print()
print()

from collections import Counter

all_nouns = [word for row in descriptions_df["nouns"] for word in row]
all_verbs = [word for row in descriptions_df["verbs"] for word in row]
all_adjectives = [word for row in descriptions_df["adjectives"] for word in row]
all_adverbs = [word for row in descriptions_df["adverbs"] for word in row]


all_words = all_nouns + all_verbs + all_adjectives + all_adverbs
word_counts = Counter(all_words)

word_stats_df = pd.DataFrame(word_counts.items(), columns=["word", "count"])
word_stats_df = word_stats_df.sort_values(by="count", ascending=False) # Sort
num_unique_words = len(word_stats_df) # Number of unique words
most_repeated = word_stats_df.head(20) # Most repeated words
least_repeated = word_stats_df[word_stats_df["count"] == 1] # Least repeated words

print(f"Total unique words: {num_unique_words}")
print("\nMost repeated words:")
print(most_repeated)

print("\nWords with only one occurrence:")
print(least_repeated)


def process_all_words(df, column_name):
    all_words = set(word for row in df[column_name] for word in row)
    return all_words
print("Number of nouns", len(process_all_words(descriptions_df, 'nouns')))
print("Number of verbs", len(process_all_words(descriptions_df, 'verbs')))
print("Number of adjectives", len(process_all_words(descriptions_df, 'adjectives')))
print("Number of adverbs", len(process_all_words(descriptions_df, 'adverbs')))


brackets = [(0, 20), (20, 40), (40, 60), (60, 80), (80, 101)]
bracket = [(0, 20)]
for bracket in brackets:
    bracket_min, bracket_max = bracket
    peraccuracybracketid = descriptions_df[(descriptions_df['human_accuracy']*100 >= bracket_min) & (descriptions_df['human_accuracy']*100 < bracket_max)]
    print(f'{len(peraccuracybracketid)} descriptions from accuracy bracket {bracket}.')
    print(process_all_words(peraccuracybracketid, 'nouns'))
    print(process_all_words(peraccuracybracketid, 'verbs'))
    print(process_all_words(peraccuracybracketid, 'adjectives'))
    print(process_all_words(peraccuracybracketid, 'adverbs'))
    for _, row in peraccuracybracketid.iterrows():
        #print(row['nouns'])
        strrr = row['task_id']+'.json'
        #process_json_file(os.path.join(evaluation_challenges_path, strrr))

    print('\n')

brackets = [(80, 101), (60, 80), (40, 60), (20, 40), (0, 20)]

used_concepts_so_far = {}
used_concepts_so_far['nouns'] = set()
used_concepts_so_far['verbs'] = set()
used_concepts_so_far['adjectives'] = set()
used_concepts_so_far['adverbs'] = set()

def nemidoonamchifelan(bracket_df, column_name, used_concepts_so_far):
    process_all_words(bracket_df, column_name)
    all_gt_in_bracket = set()
    for _, row in bracket_df.iterrows():
        all_gt_in_bracket.update(row[column_name])
    new_concepts = all_gt_in_bracket - used_concepts_so_far
    print(f'Bracket ({bracket_min}-{bracket_max}) has {len(new_concepts)} new {column_name}.')
    return new_concepts

for bracket_min, bracket_max in brackets:
    print(f'Accuracy Bracket ({bracket_min}-{bracket_max})')
    bracket_df = descriptions_df[(descriptions_df['human_accuracy']*100 >= bracket_min) & (descriptions_df['human_accuracy']*100 < bracket_max)]
    print(len(bracket_df))
    colmns = ['nouns', 'verbs', 'adjectives', 'adverbs']
    for colmn in colmns:
        conceptsssss = nemidoonamchifelan(bracket_df, colmn, used_concepts_so_far[colmn])
        used_concepts_so_far[colmn].update(conceptsssss)
        print(conceptsssss)
    print()

import json
import re

def sanity_check(task_id_to_check):
    with open("output_with_pos.json", "r") as f:
        data = json.load(f)
    for idx, item in enumerate(data):
        if item["task_id"] == task_id_to_check:
            print('idx', idx)
            print(f"Description: {item['description']}")
            print(f"Nouns: {item['nouns']}")
            print(f"Verbs: {item['verbs']}")
            print(f"Adjectives: {item['adjectives']}")
            print(f"Adverbs: {item['adverbs']}")
    strrr = task_id_to_check+'.json'
    process_json_file(os.path.join(evaluation_challenges_path, strrr))

    print(f"Task ID '{task_id_to_check}' not found in the data.")

sanity_check("05a7bcf2")