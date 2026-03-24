def create_prompt_poem(traits_list, poem_length=(4, 8), language='ENGLISH', name='No Name'):
    indexed_traits_list = []
    for index, trait in enumerate(traits_list):
        trait_index = str(index + 1) + '. ' + trait
        indexed_traits_list.append(trait_index)

    traits_string = '\n'.join(indexed_traits_list)

    poem_lenght_string = str(poem_length[0]) + '-' + str(poem_length[1])

    prompt = f'''
You are a world class {language} poet, an expert in writing warm, sentimental and personalized poems for Mother's Day.

INPUT TRAITS:
{traits_string}

TASK:
Write a short, meaningful {language} poem ({poem_lenght_string} lines) incorporating the traits above.
The should be appreciative and meaningful.

CONSTRAINTS:
Return ONLY the test of the poem.
Format the poem to be in markdown format, each lines starts with "#### "
Do NOT include introductory text, titles, or concluding remarks.
Do NOT include any meta commentary
'''

    return prompt