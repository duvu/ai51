import configparser
import os
import random

from revChatGPT.V1 import Chatbot as GPTBot
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from Bard import Chatbot as BardChatbot


# define an enum for bot type
class BotType:
    GPT = 'gpt'
    BARD = 'bard'
    EDGE = 'edge'

    # define a method to get ran
    @classmethod
    def get_ran(cls):
        return random.choice([cls.GPT, cls.BARD, cls.EDGE])

    # get bot type from string
    @classmethod
    def get_from_string(cls, _str):
        if _str == cls.GPT:
            return cls.GPT
        elif _str == cls.BARD:
            return cls.BARD
        elif _str == cls.EDGE:
            return cls.EDGE
        else:
            return cls.get_ran()

    @classmethod
    def get_next_ai(cls, ai_last_used=None):
        if ai_last_used is None:
            ai_last_used = get_last_ai_service()
        next_ai = None
        if ai_last_used == cls.GPT:
            next_ai = cls.BARD
        elif ai_last_used == cls.BARD:
            next_ai = cls.EDGE
        elif ai_last_used == cls.EDGE:
            next_ai = cls.GPT
        else:
            next_ai = cls.get_ran()
        set_last_ai_service(next_ai)
        return next_ai


def get_edge_cookie():
    # get current folder path containing this file
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    # get cookie file path
    cookie_file_path = os.path.join(current_folder_path, 'edge_cookie.json')
    return json.loads(open(cookie_file_path, encoding='utf-8').read())


# method to get last AI service used
def get_last_ai_service():
    # get current folder path containing this file
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    # get cookie file path
    cookie_file_path = os.path.join(current_folder_path, 'last_ai_service.json')
    # get the first line of the file
    if os.path.exists(cookie_file_path):
        ai_last_used = open(cookie_file_path, encoding='utf-8').readline()
        return ai_last_used
    else:
        return None


# method to set last AI service used
def set_last_ai_service(ai_service):
    # get current folder path containing this file
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    cookie_file_path = os.path.join(current_folder_path, 'last_ai_service.json')
    with open(cookie_file_path, 'w') as f:
        f.write(ai_service)


async def get_edge_bot():
    # get cookie
    cookies = get_edge_cookie()
    return await Chatbot.create(cookies=cookies)


async def compose_edge_async(_prompt, **kwargs):
    bot = await get_edge_bot()
    answer = await bot.ask(_prompt, conversation_style=ConversationStyle.creative, simplify_response=True)
    await bot.close()
    return answer


# method to load config from file
def load_config():
    # get current folder path containing this file
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_folder_path, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config['account']


class AICommunicator:
    def __init__(self):
        pass

    @classmethod
    def compose(cls, _prompt, **kwargs):
        # get bot type from kwargs, if not found, get a random bot type
        bot_type = kwargs.get('bot_type', BotType.get_next_ai())
        answer = None
        if bot_type == BotType.GPT:
            answer = cls.compose_gpt(_prompt, **kwargs)
        elif bot_type == BotType.BARD:
            answer = cls.compose_bard(_prompt, **kwargs)
        elif bot_type == BotType.EDGE:
            answer = cls.compose_edge(_prompt, **kwargs)
        else:
            raise Exception('Unknown bot type')
        return answer

    @classmethod
    def compose_gpt(cls, _prompt, **kwargs):
        config = load_config()
        chat_gpt_email = config['chat_gpt_email']
        chat_gpt_password = config['chat_gpt_password']

        gbot = GPTBot(config={
            "email": chat_gpt_email,
            "password": chat_gpt_password
        })
        answer = None
        try:
            for data in gbot.ask(prompt=_prompt, model='text-davinci-002-render-sha', auto_continue=True):
                answer = data
                answer['src'] = 'gpt'
            return answer
        except Exception as e:
            print('Something went wrong, try again', e)
            return answer

    @classmethod
    def compose_bard(cls, _prompt, **kwargs):
        config = load_config()
        bard_token1 = config['bard_token1']
        bard_token2 = config['bard_token2']

        bbot = BardChatbot(bard_token1, bard_token2)
        answer = bbot.ask(_prompt)
        # rename the key 'content' to 'message'
        answer['message'] = answer.pop('content')
        answer['src'] = 'bard'
        return answer

    @classmethod
    def compose_edge(cls, _prompt, **kwargs):
        answer = asyncio.run(compose_edge_async(_prompt, **kwargs))
        # rename the key 'text' to 'message'
        answer['message'] = answer.pop('text')
        answer['src'] = 'edge'
        return answer


# test entry point
if __name__ == '__main__':
    prompt = 'Compose a paper article about Hanoi, Vietnam'
    resp = AICommunicator.compose(_prompt=prompt, bot_type=BotType.BARD)
    print(resp)

    # bot_type = 'gpt'
    # type = BotType.get_from_string(bot_type)
    # print(type)
