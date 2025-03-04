import json
import spacy

nlp = spacy.load("en_core_web_sm")

with open("descriptions.jsonl", "r") as f:
    data = json.load(f)

for item in data:
    doc = nlp(item["description"])
    item["nouns"] = [token.text for token in doc if token.pos_ == "NOUN"]
    item["verbs"] = [token.text for token in doc if token.pos_ == "VERB"]
    item["adjectives"] = [token.text for token in doc if token.pos_ == "ADJ"]
    item["adverbs"] = [token.text for token in doc if token.pos_ == "ADV"]

with open("output_with_pos.json", "w") as f:
    json.dump(data, f, indent=2)
