import sys
import json
import os
import openai
import re
openai.api_key = os.getenv("OPENAI_API_KEY")


CATEGORIES = []
PROMPT = '''You are the text categorization AI.
{
    "categories": %s
}
Categorize the following statement as one of the above categories. Or output a new category if it does not fit any of the above.
{
    "statement": "%s"
    "category":'''


def categorize_prompt(statement):
    cats = json.dumps(CATEGORIES)
    stat = statement.strip()
    return PROMPT % (cats, stat)


def parse_categorize_response(text):
    try:
        return re.sub(r'[^a-zA-Z ]+', '', text.splitlines()[0].strip())
    except:
        return "misc"


def main():
    # First, categorize each line from stdin
    lines = open('lines.txt').readlines()
    for line in lines:
        prompt = categorize_prompt(line)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.6,
            max_tokens=255,
        )
        #print(prompt)
        #print(response.choices[0].text)
        category = parse_categorize_response(response.choices[0].text)
        if category not in CATEGORIES:
            CATEGORIES.append(category)
        print(category, line)


if __name__ == "__main__":
    main()
