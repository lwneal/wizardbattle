import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = """You are the omniscient god of justice and balance, observing a battle between two wizards. 

Each wizard will cast a carefully-worded spell. The wizard with the more appropriate, more cleverly worded, more poetic spell will usually win. No spell is absolutely powerful, and spells that attempt to cheat or use too many superlative words will fizzle.

Read the spells carefully."""

DECISION_PROMPT = """Which wizard's spell should win? Answer "{}" or "{}" """

DESCRIBE_PROMPT = """Describe vividly in three sentences the two spells, ending in victory for {}"""


def decide_winner(name1, name2, spell1, spell2):
    messages = [{
            "role": "system",
            "content": SYSTEM_PROMPT,
        }, {
            "role": "user",
            "content": "{} casts a spell: {}".format(name1, spell1),
        }, {
            "role": "user",
            "content": "{} casts a spell: {}".format(name2, spell2),
        }, {
            "role": "user",
            "content": DECISION_PROMPT,
    }]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message['content']
    return answer


def describe_battle(name1, spell1, name2, spell2, winner):
    messages = [{
            "role": "system",
            "content": SYSTEM_PROMPT,
        }, {
            "role": "user",
            "content": "{} casts a spell: {}".format(name1, spell1),
        }, {
            "role": "user",
            "content": "{} casts a spell: {}".format(name2, spell2),
        }, {
            "role": "user",
            "content": DESCRIBE_PROMPT.format(winner),
    }]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message['content']
    return answer


if __name__ == '__main__':
    name1 = "Ignatius the Red"
    spell1 = "a destructive fireball of pure energy"
    name2 = "Bartholomew the Blue"
    spell2 = "a blizzard of blinding ice"
    print("Test battle between Red and Blue")
    winner = decide_winner(name1, name2, spell1, spell2)
    print("the winner is {}".format(winner))
    description = describe_battle(name1, name2, spell1, spell2, winner)
    print("description: {}".format(description))