import time

class UserJsonDictParser:
    def __init__(self, content_hint, required_keys, keys_to_memory = 'speak', keys_to_content = "speak", keys_to_metadata = ""):
        self.content_hint = content_hint
        self.required_keys = required_keys
        self.keys_to_memory = keys_to_memory
        self.keys_to_content = keys_to_content
        self.keys_to_metadata = keys_to_metadata

    def parse(self, user_input):
        return user_input

def get_user_witch_healing_input():
    time.sleep(0.5)
    speak = input("是否复活该玩家及其原因: ")
    resurrect = input("是否复活该玩家(true/false): ")
    thought = ""
    return {
        "thought": thought,
        "speak": speak,
        "resurrect": resurrect
    }

def get_user_wolf_discussing_input():
    time.sleep(0.5)
    speak = input("对你有利的发言：")
    finish_discussion= input("是否达成一致意见(true/false): ")
    thought = ""
    return {
        "thought": thought,
        "speak": speak,
        "finish_discussion": finish_discussion
    }

def get_user_wolf_vote_input():
    time.sleep(0.5)
    vote= input("请投票你想淘汰的玩家：")
    thought = ""
    return {
        "thought": thought,
        "vote":vote
    }

def get_user_seer_input():
    time.sleep(0.5)
    thought = ""
    speak = input("请给出你的选择(不能是你自己): ")

    return {
        "thought": thought,
        "speak": speak,
    }

def get_user_survivors_discuss_input():
    time.sleep(0.5)
    thought = ""
    speak = input("对你有利的发言: ")

    return {
        "thought": thought,
        "speak": speak,
    }

def get_user_survivors_vote_input():
    time.sleep(0.5)
    thought = ""
    vote = input("请输入你想投票的玩家姓名:")

    return {
        "thought": thought,
        "vote": vote,
    }

def get_user_witch_poison_input():
    time.sleep(0.5)
    thought = ""
    speak = input("对你有利的发言: ")
    eliminate = input("是否淘汰一名玩家(true/false): ")

    return {
        "thought": thought,
        "speak": speak,
        "eliminate": eliminate,
    }


def pop_agent_by_name(my_list, name):
    for i, obj in enumerate(my_list):
        if obj.name == name:
            return my_list.pop(i)
    raise ValueError(f"对象 {name} 不在列表中")





