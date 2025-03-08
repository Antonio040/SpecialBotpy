from logging import exception
from multiprocessing.connection import answer_challenge
from random import choice, randint
from math import *
def get_response(user_input: str) -> str:   
    lowered: str = user_input.lower()

    if lowered == '':
        return "kys."
    elif 'roll dice' in lowered:
        return f'You rolled a {randint(1, 6)}'
    elif 'kys' in lowered:
        return 'no u kys'
    elif 'say' in lowered:
       return f'{user_input[4:]}'
    elif 'skibidi' in lowered:
        return 'brücke?'
    elif 'are you proud of me' in lowered:
        return 'no'
    elif "sigma english" in lowered:
        return 'Sigma, sigma boy, sigma boy, sigma boy\nevery girl wants to dance with you\nSigma, sigma boy, sigma boy, sigma boy\nIm the kind of person you will need a year to win over'
    elif 'math' in lowered:
        try:
            answer = round(eval(user_input[5:]),4)
            if answer == int:
                return f'{answer}'
            return f'{answer}'
        except Exception as e:
            return f'You cant do that stupid, because of {e}'
    elif 'wait' in lowered:
        return choice([
            'no',
            'they dont love you.',
            'they dont love you like i love you :fire:',
            'its annoying stop'
            ])
    elif 'sigma' in lowered:
        return 'Sigma, sigma boy, sigma boy, sigma boy\nКаждая девчонка хочет танцевать с тобой\nSigma, sigma boy, sigma boy, sigma boy\nЯ такая вся, что добиваться будешь год'
    elif 'good boy' in lowered:
        return choice([
            'arf arf',
            'me me me'
        ])
    else:
        return choice([
            'r u retarded?',
            'stop talking',
            'shhhhhhhhh',
            'stop',
            'ew',
            'bombe?',
            'sag mal bein auf english... Leg meine Eier AHHAHAHAH :fire: :sunglasses:',])
