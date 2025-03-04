text = "In the input, you will see a 2x2 pattern. To create the output, repeat this pattern to fill a 6x6 grid, but flip the pattern horizontally for every alternate row."
text = "In the input, you will see a black grid with several colored squares scattered across. The colors are surrounded by black pixels, and each colored square is uniquely colored. To generate the output, align all the colored squares along the nearest boundary of the grid, while keeping their original colors and orientations. The squares should be pushed towards the edges of the grid."


prompt = f"""
Extract all nouns and verbs from the following text:
{text}
Return them in a comma-separated list like this:
Nouns: ...,
Verbs: ...
"""
prompt = f"""
You are a helpful assistant that extracts all **nouns** and **verbs** from the given text.
Text: {text}
Please list the nouns and verbs separately.
Nouns:
Verbs:
"""
result = generator(prompt, max_length=200)
print(result[0]["generated_text"])
print('End')
