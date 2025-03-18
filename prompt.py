# -*- coding: utf-8 -*-
"""Used to record prompts, will be replaced by configuration"""
from agentscope.parsers.json_object_parser import MarkdownJsonDictParser


class Prompts:
    """Prompts for werewolf game"""
    to_wolves_initial = "狼人们，请在讨论阶段确认彼此身份：{}"
    to_wolves = (
        "{}, 如果你是唯一的狼人，选择一个玩家淘汰。如果不是，请与你的队友讨论并达成一致意见。"
    )

    wolves_discuss_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "对你有利的发言",
            "finish_discussion": "讨论是否达成一致(true/false)"
        },
        required_keys=["thought", "speak", "finish_discussion"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["finish_discussion"],
    )

    to_wolves_vote = "你投票淘汰{}中哪个玩家？"

    wolves_vote_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "vote": "player_name",
        },
        required_keys=["thought", "vote"],
        keys_to_memory="vote",
        keys_to_content="vote",
    )
    to_wolves_no_consensus = "你们并没有达成一致的意见，看来需要进一步的讨论"
    to_wolves_no_elimination = "狼人们决定今晚不淘汰玩家。"
    to_wolves_res = "得票最多的玩家是{}."

    to_witch_resurrect = (
        "{witch_name}，你是女巫。今晚{dead_name}被淘汰。你想复活{dead_name}吗？"
    )
    
    to_user_witch_resurrect = ("{witch_name}，你是女巫。今晚{dead_name}被淘汰。你想复活{dead_name}吗？（请回答是或否）")
    
    to_witch_resurrect_no = "女巫选择不复活{}。"
    
    to_witch_resurrect_yes = "女巫选择复活{}。"

    witch_resurrect_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "是否复活该玩家及其原因",
            "resurrect": "是否复活该玩家(true/false)",
        },
        required_keys=["thought", "speak", "resurrect"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["resurrect"],
    )

    to_witch_poison = (
        "{}，你是女巫，今晚你想淘汰{}中的一个玩家吗？如果是，请指定玩家的名字。"
    )
    
    to_user_witch_poison = (
        "{}，你是女巫，今晚你想淘汰{}中的一个玩家吗？（请先回答“是或否”）"
    )
    to_user_witch_poison_name = (
        "请说出你想淘汰的玩家姓名。"
    )
    to_witch_poison_yes = (
        "{}已被你淘汰"
    )
    
    to_witch_poison_loop = ("你选择了错误的玩家姓名，请重新选择")
    
    to_witch_poison_no = ("好的，游戏继续")

    witch_poison_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "对你有利的发言",
            "eliminate": "是否淘汰一名玩家(true/false)",
        },
        required_keys=["thought", "speak", "eliminate"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["eliminate"],
    )

    to_seer = (
        "{}, 你是预言家。今晚你想查验{}中的哪个玩家？"
    )
    
    to_seer_no = (
        "你的选择不在存活玩家内，请选择{}中的玩家进行查验。"
    )

    seer_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "only one player_name(不能是你)",
        },
        required_keys=["thought", "speak"],
        keys_to_memory="speak",
        keys_to_content="speak",
    )

    to_seer_result = "好的，{}的角色是{}."

    to_all_danger = (
        "天亮了，所有玩家睁开眼睛。昨晚，以下玩家被淘汰：{}。 "
    )

    to_all_peace = (
        "天亮了，所有玩家睁开眼睛。昨晚平安无事，没有玩家被淘汰。"
    )

    to_all_discuss = (
        "现在存活的玩家有{}。根据游戏规则和你的角色，基于当前的情况和你获得的信息，要在存活的玩家中投票淘汰一个玩家并赢得游戏，你想对其他人说些什么？你可以决定是否揭示你的角色。"
    )


    to_all_no_elimination = (
        "经过再次投票，今天没有玩家被淘汰。"
    )

    to_all_nonsense = (
        "你们之间意见并不一致，请再互相讨论一下，达成一致的意见。"
    )
    to_all_no_player = (
        "你们投票选出的{}并不在幸存的玩家之中。"
    )
    survivors_discuss_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "对你有利的发言",
        },
        required_keys=["thought", "speak"],
        keys_to_memory="speak",
        keys_to_content="speak",
    )

    survivors_vote_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "vote": " player_name",
        },
        required_keys=["thought", "vote"],
        keys_to_memory="vote",
        keys_to_content="vote",
    )

    to_all_vote = (
        "根据游戏规则和你的角色，基于当前的情况和你获得的信息，为了赢得游戏，现在是时候在存活的玩家中投票淘汰一个玩家。你投票淘汰{}中哪个玩家？"
    )

    to_all_res = "{}被投票淘汰了。"

    to_all_wolf_win = (
        "狼人获胜，占领了村庄。下次好运！"
    )

    to_all_village_win = (
        "游戏结束。狼人被击败，村庄再次安全了！"
    )

    to_all_continue = "游戏继续。"
