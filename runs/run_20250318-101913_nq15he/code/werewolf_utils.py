# -*- coding: utf-8 -*-
"""utils."""
import re
from typing import Union, Any, Sequence

import numpy as np
from loguru import logger
import random
from prompt import Prompts
from agentscope.agents import AgentBase
from agentscope.message import Msg

'''
def check_winning(alive_agents: list, wolf_agents: list, host: str) -> bool:
    """check which group wins"""
    if len(wolf_agents) * 2 >= len(alive_agents):
        msg = Msg(host, Prompts.to_all_wolf_win, role="assistant")
        logger.chat(msg)
        return True
    if alive_agents and not wolf_agents:
        msg = Msg(host, Prompts.to_all_village_win, role="assistant")
        logger.chat(msg)
        return True
    return False
'''

def extract_name_and_id(name: str) -> tuple[str, int]:
    """extract player name and id from a string"""
    # print("待提取样本为：", name)
    
    if name is None or not isinstance(name, str) or name.lower() == "none":
        # 如果传入值为 None 或 "none"，返回 "Abstain" 和 -1
        logger.warning("vote: received None or 'none' as input, set to Abstain")
        return "Abstain", -1

    try:
        # Allow for non-word characters before "Player"
        match = re.search(r"(Player\d+)", name, re.IGNORECASE)
        name = match.group(1).capitalize()
        idx = int(re.search(r"Player(\d+)", name, re.IGNORECASE).group(1)) - 1
    except AttributeError:
        # In case Player remains silent or speaks to abstain.
        logger.warning(f"vote: invalid name {name}, set to Abstain")
        name = "Abstain"
        idx = -1
    return name, idx


def update_alive_players(
    survivors: Sequence[AgentBase],
    wolves: Sequence[AgentBase],
    dead_names: Union[str, list[str]],
) -> tuple[list, list]:
    """update the list of alive agents"""
    if not isinstance(dead_names, list):
        dead_names = [dead_names]
    return [_ for _ in survivors if _.name not in dead_names], [
        _ for _ in wolves if _.name not in dead_names
    ]


def majority_vote(votes: list) -> Any:
    """majority_vote function"""
    votes_valid = [item for item in votes if item != "Abstain"]
    if not votes_valid:
        return None  # 如果没有有效票数，返回 None
    
    # 统计每个玩家的票数
    unit, counts = np.unique(votes_valid, return_counts=True)
    max_count = np.max(counts)
    candidates = unit[counts == max_count]

    if len(candidates) > 1:
        return None  # 如果有多个玩家票数相同，返回 None

    return candidates[0]  # 否则返回票数最高的玩家



def n2s(agents: Sequence[Union[AgentBase, str]]) -> str:
    """combine agent names into a string, and use "and" to connect the last
    two names."""

    def _get_name(agent_: Union[AgentBase, str]) -> str:
        return agent_.name if isinstance(agent_, AgentBase) else agent_

    if len(agents) == 1:
        return _get_name(agents[0])

    return (
        ", ".join([_get_name(_) for _ in agents[:-1]])
        + " and "
        + _get_name(agents[-1])
    )


def set_parsers(
    agents: Union[AgentBase, list[AgentBase]],
    parser_name: str,
) -> None:
    """Add parser to agents"""
    if not isinstance(agents, list):
        agents = [agents]
    for agent in agents:
        agent.set_parser(parser_name)


def generate_roles(num_werewolves = 2, num_villagers = 2, num_seers=1, num_witchs=1):
    '''
    用来控制游戏中生成几个平民，几个狼人，几个女巫，几个预言家
    '''
    roles = []

    # 添加指定数量的狼人角色
    for _ in range(num_werewolves):
        roles.append("werewolf")

    # 添加指定数量的平民角色
    for _ in range(num_villagers):
        roles.append("villager")

    for _ in range(num_seers):
        roles.append("seer")
    for _ in range(num_witchs):
        roles.append("witch")
    
    # 随机打乱角色列表
    random.shuffle(roles)
    return roles

def select_roles(survivors, roles):
    # 初始化角色组
    wolves, seer, witch = [], None, None
    for i, role in enumerate(roles):
        # print(role, i)
        if role == "werewolf":
            wolves.append(survivors[i])
        elif role == "witch":
            witch = survivors[i]
        elif role == "seer":
            seer = survivors[i]

    return wolves, witch, seer

