import os
import agentscope
from functools import partial
from agentscope.msghub import msghub
from agentscope.message import Msg
from prompt import Prompts
import random
import time
from werewolf_utils import *
import configs
import MyModelWrapper as MyModelWrapper
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from werewolf_gui import WerewolfGameWindow, UserInputSignal  # 假设你的GUI文件名为werewolf_gui.py




class WerewolfGameThread(QThread):
    append_output_signal = pyqtSignal(str)
    request_discussion_end_signal = pyqtSignal(bool)  # 添加请求讨论结束信号

    def __init__(self, roles, survivors, witch, seer,wolves: list, roles_dict, max_game_round, healing, poison, is_user_play_games, user_name = "", user_role = "", parent=None):
        super().__init__(parent)
        self.roles = roles
        self.survivors = survivors
        self.wolves = wolves
        self.witch = witch
        self.seer = seer
        self.roles_dict = roles_dict
        self.healing = healing
        self.poison = poison
        self.is_user_play_games = is_user_play_games
        self.user_name = user_name
        self.user_role = user_role
        self.max_game_round = max_game_round
        self.user_input = None
        self.discussion_end_choice = False

    # 判断是否成功函数
    def check_winning(self, alive_agents: list, wolf_agents: list, host: str) -> bool:
        """check which group wins"""
        if len(wolf_agents) * 2 >= len(alive_agents):
            msg = Msg(host, Prompts.to_all_wolf_win, role="assistant")
            self.append_output_signal.emit(msg.to_str())
            logger.chat(msg)
            return True
        if alive_agents and not wolf_agents:
            msg = Msg(host, Prompts.to_all_village_win, role="assistant")
            self.append_output_signal.emit(msg.to_str())
            logger.chat(msg)
            return True
        return False

    def run(self):
        HostMsg = partial(Msg, name="Moderator", role="assistant", echo=True)
        if self.is_user_play_games:
            UserMsg = partial(Msg, name=f"{self.user_name}", role=f"{self.user_name}", echo=True)
            self.append_output_signal.emit(f"玩家您好，您在本次游戏中的名字为{self.user_name}，您的身份为{self.user_role}，请享受游戏的过程。")
        MAX_WEREWOLF_DISCUSSION_ROUND = 5
        
        initial_discussion_done = False
        # 进入游戏中
        for _ in range(1, self.max_game_round + 1):
            survivor_names = [agent.name for agent in self.survivors]  # 每轮初始时提取当前存活者的名字
            """
            狼人部分
            """
            if not initial_discussion_done:
                # 初始讨论阶段，让狼人认清彼此身份
                hint = HostMsg(content=Prompts.to_wolves_initial.format(n2s(self.wolves)))
                self.append_output_signal.emit(hint.to_str())
                with msghub(self.wolves, announcement=hint) as hub:
                    set_parsers(self.wolves, Prompts.wolves_discuss_parser)
                    for _ in range(MAX_WEREWOLF_DISCUSSION_ROUND):
                        # 打乱顺序并遍历
                        random.shuffle(self.wolves)
                        # 如果玩家是狼人，则参与进来
                        if self.is_user_play_games and self.user_role == "werewolf":
                            previous_msg = hint  # 初始化上一个发言内容
                            for i, wolf in enumerate(self.wolves):
                                if wolf.name == self.user_name:
                                    while self.user_input is None:
                                        time.sleep(0.1)
                                    user_text = self.user_input
                                    # user_text = get_user_wolf_discussing_input().get('speak')
                                    temp_user_Msg = UserMsg(content=user_text)
                                    # 暂时不知道玩家输入是否会显示到界面上，所以先不对玩家的话进行self.append_output_signal.emit
                                    hub.broadcast(temp_user_Msg)
                                    self.append_output_signal.emit(f"玩家: {user_text}")
                                    previous_msg = temp_user_Msg  # 更新上一个发言内容
                                    self.user_input = None
                                else:
                                    x = wolf(previous_msg)
                                    self.append_output_signal.emit(x.to_str())
                                    previous_msg = x  # 更新上一个发言内容
                            # 放回智能体
                            # self.wolves.append(temp_wolf)
                        else:
                            previous_msg = hint
                            for wolf in self.wolves:
                                x = wolf(previous_msg)
                                self.append_output_signal.emit(x.to_str())
                                previous_msg = x
                        if x.metadata.get("finish_discussion", False):
                            break
                initial_discussion_done = True

            # 夜晚阶段，狼人之间交流
            hint = HostMsg(content=Prompts.to_wolves.format(n2s(self.wolves)))
            self.append_output_signal.emit(hint.to_str())
            voting_complete = False
            while not voting_complete:
                with msghub(self.wolves, announcement=hint) as hub:
                    # 设置交流阶段返回内容的格式要求
                    set_parsers(self.wolves, Prompts.wolves_discuss_parser)
                    for _ in range(MAX_WEREWOLF_DISCUSSION_ROUND):
                        random.shuffle(self.wolves)
                        # 如果有玩家参与
                        if self.is_user_play_games and self.user_name in survivor_names and self.user_role == "werewolf":
                            previous_msg = hint  # 初始化上一个发言内容
                            for i, wolf in enumerate(self.wolves):
                                if wolf.name == self.user_name:
                                    while self.user_input is None:
                                        time.sleep(0.1)
                                    user_text = self.user_input
                                    # user_text = get_user_wolf_discussing_input()
                                    temp_user_Msg = UserMsg(content=user_text)
                                    hub.broadcast(temp_user_Msg)
                                    previous_msg = temp_user_Msg  # 更新上一个发言内容
                                    self.append_output_signal.emit(temp_user_Msg.to_str())
                                    self.user_input = None
                                else:
                                    x = wolf(previous_msg)
                                    self.append_output_signal.emit(x.to_str())
                                    previous_msg = x  # 更新上一个发言内容
                            
                            # 判断是否结束交流
                            if x.metadata.get("finish_discussion", False):
                                break
                        # 智能体之间交流
                        else:
                            previous_msg = hint
                            for wolf in self.wolves:
                                x = wolf(previous_msg)
                                self.append_output_signal.emit(x.to_str())
                                previous_msg = x
                            if x.metadata.get("finish_discussion", False):
                                break

                    
                    # 设置投票阶段返回内容的格式要求
                    set_parsers(self.wolves, Prompts.wolves_vote_parser)

                    while not voting_complete:
                        # 上帝要求投票
                        hint = HostMsg(content=Prompts.to_wolves_vote.format(n2s(self.survivors)))
                        self.append_output_signal.emit(hint.to_str())
                        votes = []
                        # 如果用户为狼人,且仍旧存活
                        if self.is_user_play_games and self.user_name in survivor_names and self.user_role == "werewolf":
                            for i, wolf in enumerate(self.wolves):
                                if wolf.name == self.user_name:
                                    while self.user_input is None:
                                        time.sleep(0.1)
                                    user_text = self.user_input
                                    # user_text = get_user_wolf_vote_input()
                                    user_vote = extract_name_and_id(user_text)[0]
                                    temp_user_Msg = UserMsg(content=user_vote)
                                    hub.broadcast(temp_user_Msg)
                                    self.append_output_signal.emit(user_vote)
                                    votes.append(user_vote)
                                    self.user_input = None
                                else:
                                    x = wolf(hint)
                                    self.append_output_signal.emit(x.to_str())
                                    # previous_msg = x  # 更新上一个发言内容
                                    votes.append(extract_name_and_id(x)[0])
                        # 否则全为智能体投票
                        else:
                            for wolf in self.wolves:
                                x = wolf(hint)
                                self.append_output_signal.emit(x.to_str())
                                votes.append(extract_name_and_id(x.content)[0])

                        # 获取投票结果
                        dead_player = majority_vote(votes)
                        # 如果投票全为空或者全为非法投票，则本轮结束
                        if not votes or all(vote == "Abstain" for vote in votes):
                            hint = HostMsg(content=Prompts.to_wolves_no_elimination)
                            hub.broadcast(hint)
                            self.append_output_signal.emit(hint.to_str())
                            voting_complete = True
                        elif dead_player is not None and dead_player in survivor_names:
                            dead_player = [dead_player]
                            hint = HostMsg(content = Prompts.to_wolves_res.format(dead_player[0]))
                            hub.broadcast(hint)
                            self.append_output_signal.emit(hint.to_str())
                            voting_complete = True
                        else:
                            hint = HostMsg(content = Prompts.to_wolves_no_consensus)
                            hub.broadcast(hint)
                            self.append_output_signal.emit(hint.to_str())
                            break
                

            """
            女巫部分
            """
            healing_used_tonight = False
            # 玩家是女巫的执行程序
            if self.is_user_play_games and self.user_role == "witch"  and self.witch in self.survivors:
            # 如果有治愈药水，且有刚刚死去的玩家，则询问是否拯救
                if self.healing and dead_player:
                    hint = HostMsg(
                        content=Prompts.to_user_witch_resurrect.format_map(
                            {
                                "witch_name": self.witch.name,
                                "dead_name": dead_player[0]
                            },
                        ),
                    )
                    self.append_output_signal.emit(hint.to_str())
                    # 获取玩家输入
                    while self.user_input is None:
                        time.sleep(0.1)
                    user_text = self.user_input
                    
                    temp_user_Msg = UserMsg(content=user_text)
                    self.append_output_signal.emit(temp_user_Msg.to_str())
                    
                    if user_text == "是" and dead_player:
                        healing_used_tonight = True
                        hint = HostMsg(content=Prompts.to_witch_resurrect_yes.format(dead_player[0]))
                        self.append_output_signal.emit(hint.to_str())
                        dead_player.pop()
                        self.healing = False
                    else:
                        hint = HostMsg(content = Prompts.to_witch_resurrect_no.format(dead_player[0]))
                        self.append_output_signal.emit(hint.to_str())
                    self.discussion_end_choice = None
                    self.user_input = None
                # 女巫使用毒药的部分
                if self.poison and not healing_used_tonight:
                    # set_parsers(witch, Prompts.witch_poison_parser)
                    poisoning_complete = False
                    # 投毒循环部分
                    while not poisoning_complete:
                        # 上帝询问
                        hint = HostMsg(content = Prompts.to_user_witch_poison.format(self.user_name, n2s(self.survivors)))
                        self.append_output_signal.emit(hint.to_str())
                        # 玩家回答
                        # 确定淘汰姓名
                        while self.user_input is None:
                            time.sleep(0.1)
                        user_text = self.user_input
                        temp_user_Msg = UserMsg(content=user_text)
                        self.append_output_signal.emit(temp_user_Msg.to_str())
                        self.user_input = None
                        # 如果确认投毒

                        if user_text == "是":
                            hint = HostMsg(content = Prompts.to_user_witch_poison_name)
                            self.append_output_signal.emit(hint.to_str())
                            while self.user_input is None:
                                time.sleep(0.1)
                            user_text = self.user_input
                            player_name= extract_name_and_id(user_text)[0]
                            self.user_input = None
                            # 如果投毒的玩家不是非法字符，并且在幸存玩家中
                            if player_name != "Abstain" and player_name in survivor_names:
                                # 如果此时没有死亡的玩家，则创建本轮死亡玩家列表
                                if dead_player is None:
                                    dead_player = [player_name]
                                else: 
                                    dead_player.append(player_name)
                                poison = False
                                poisoning_complete = True
                                hint = HostMsg(content=Prompts.to_witch_poison_yes.format(player_name))
                                self.append_output_signal.emit(hint.to_str())
                            # 如果回复非法，则重新进入循环
                            else:
                                hint = HostMsg(content=Prompts.to_witch_poison_loop)
                                self.append_output_signal.emit(hint.to_str())
                                continue
                        else:
                            hint = HostMsg(content=Prompts.to_witch_poison_no)
                            self.append_output_signal.emit(hint.to_str())
                            poisoning_complete = True
                            # break
                        self.discussion_end_choice = None
                        self.user_input = None
                        
            # 智能体女巫部分
            elif self.witch in self.survivors:
                # 如果有治愈药水，且有刚刚死去的玩家，则询问是否拯救
                if self.healing and dead_player:
                    hint = HostMsg(
                        content=Prompts.to_witch_resurrect.format_map(
                            {
                                "witch_name": self.witch.name,
                                "dead_name": dead_player[0]
                            },
                        ),
                    )
                    self.append_output_signal.emit(hint.to_str())
                    set_parsers(self.witch, Prompts.witch_resurrect_parser)
                    x = self.witch(hint)
                    self.append_output_signal.emit(x.to_str())
                    if dead_player and x.metadata.get("resurrect", False):
                        healing_used_tonight = True
                        hint = HostMsg(content=Prompts.to_witch_resurrect_yes.format(dead_player[0]))
                        self.append_output_signal.emit(hint.to_str())
                        dead_player.pop()
                        self.healing = False
                    else:
                        hint = HostMsg(content=Prompts.to_witch_resurrect_no.format(dead_player[0]))
                        self.append_output_signal.emit(hint.to_str())
                
                # 女巫使用毒药的部分
                if self.poison and not healing_used_tonight:
                    set_parsers(self.witch, Prompts.witch_poison_parser)
                    poisoning_complete = False
                    # 投毒循环部分
                    while not poisoning_complete:
                        hint = HostMsg(content=Prompts.to_witch_poison.format(self.witch.name, n2s(self.survivors)))
                        self.append_output_signal.emit(hint.to_str())
                        x = self.witch(hint)
                        self.append_output_signal.emit(x.to_str())
                        player_name= extract_name_and_id(x.content)[0]
                        # survivor_names = [agent.name for agent in self.survivors]
                        if x.metadata.get("eliminate", False):
                            # 如果投毒的玩家不是非法字符，并且在幸存玩家中
                            if player_name != "Abstain" and player_name in survivor_names:
                                # 如果此时没有死亡的玩家，则创建本轮死亡玩家列表
                                if dead_player is None:
                                    dead_player = [player_name]
                                else: 
                                    dead_player.append(player_name)
                                poison = False
                                poisoning_complete = True
                                hint = HostMsg(content=Prompts.to_witch_poison_yes.format(player_name))
                                self.append_output_signal.emit(hint.to_str())
                            else:
                                hint = HostMsg(content=Prompts.to_witch_poison_loop)
                                self.append_output_signal.emit(hint.to_str())
                                continue
                        else:
                            hint = HostMsg(content=Prompts.to_witch_poison_no)
                            self.append_output_signal.emit(hint.to_str())
                            poisoning_complete = True
                        
            """
            预言家部分
            """
            if self.seer in self.survivors:
                hint = HostMsg(
                        content=Prompts.to_seer.format(self.seer.name, n2s(self.survivors)),
                    )
                self.append_output_signal.emit(hint.to_str())
                # 如果玩家为预言家
                if self.is_user_play_games and self.user_role == "seer":
                    seering_complete = False
                    while not seering_complete:
                        # user_text = get_user_seer_input()
                        while self.user_input is None:
                            time.sleep(0.1)
                        user_text = self.user_input
                        # user_speak = user_text.get("speak")
                        temp_user_Msg = UserMsg(content=user_text)
                        player_name, idx = extract_name_and_id(user_text)
                        self.append_output_signal.emit(temp_user_Msg.to_str())
                        self.user_input = None
                        if player_name != "Abstain" and player_name in survivor_names:
                            role = "狼人" if self.roles[idx] == "werewolf" else "村民"
                            hint = HostMsg(content=Prompts.to_seer_result.format(player_name, role))
                            self.append_output_signal.emit(hint.to_str())
                            seering_complete = True
                        else:
                            hint = HostMsg(content=Prompts.to_seer_no.format(n2s(self.survivors)))
                            self.append_output_signal.emit(hint.to_str())
                # 智能体部分
                else:
                    set_parsers(self.seer, Prompts.seer_parser)
                    seering_complete = False
                    while not seering_complete:
                        x = self.seer(hint)
                        self.append_output_signal.emit(x.to_str())
                        player_name, idx = extract_name_and_id(x.content)
                        if player_name != "Abstain" and player_name in survivor_names:
                            role = "狼人" if self.roles[idx] == "werewolf" else "村民"
                            hint = HostMsg(content=Prompts.to_seer_result.format(player_name, role))
                            self.append_output_signal.emit(hint.to_str())
                            seering_complete = True
                        else:
                            hint = HostMsg(content=Prompts.to_seer_no.format(n2s(self.survivors)))
                            self.append_output_signal.emit(hint.to_str())
                    self.seer.observe(hint)


            # 更新夜晚过后玩家状态
            self.survivors, self.wolves = update_alive_players(
                self.survivors,
                self.wolves,
                dead_player,
            )
            survivor_names = [agent.name for agent in self.survivors] # 更新幸存者名单
            # 判断游戏是否结束
            if self.check_winning(self.survivors, self.wolves, "Moderator"):
                break

            # 白天阶段
            content = (
                Prompts.to_all_danger.format(n2s(dead_player))
                if dead_player
                else Prompts.to_all_peace
            )
            hint1 = HostMsg(content=content)
            hint2 = HostMsg(content=Prompts.to_all_discuss.format(n2s(self.survivors)))
            hints = [
                hint1,
                hint2,
            ]
            self.append_output_signal.emit(hint1.to_str())
            self.append_output_signal.emit(hint2.to_str())
            


            with msghub(self.survivors, announcement=hints) as hub:
                voting_complete = False
                voting_times = 0
                # 当投票没有结果时
                while not voting_complete and voting_times < 2:
                    # 配置返回参数
                    set_parsers(self.survivors, Prompts.survivors_discuss_parser)
                    # 随机发言
                    random.shuffle(self.survivors)
                    # 如果玩家参与，并且还没被淘汰
                    if self.is_user_play_games and self.user_name in survivor_names:
                        # 移出对应智能体
                        previous_msg = hints  # 初始化上一个发言内容

                        for i, survivor in enumerate(self.survivors):
                            if survivor.name == self.user_name:
                                while self.user_input is None:
                                    time.sleep(0.1)
                                user_text = self.user_input
                                # user_text = get_user_survivors_discuss_input().get('speak')
                                temp_user_Msg = UserMsg(content=user_text)
                                hub.broadcast(temp_user_Msg)
                                self.append_output_signal.emit(temp_user_Msg.to_str())
                                previous_msg = temp_user_Msg  # 更新上一个发言内容
                                self.user_input = None
                            else:
                                x = survivor(previous_msg)
                                self.append_output_signal.emit(x.to_str())
                                previous_msg = x  # 更新上一个发言内容
                    # 如果完全是智能体的话，就轮流发言
                    else:
                        previous_msg = hint
                        for survivor in self.survivors:
                            x = survivor(previous_msg)
                            self.append_output_signal.emit(x.to_str())
                            previous_msg = x
                    
                    # 投票部分
                    
                    set_parsers(self.survivors, Prompts.survivors_vote_parser)
                    
                    hint = HostMsg(content=Prompts.to_all_vote.format(n2s(self.survivors)))
                    self.append_output_signal.emit(hint.to_str())
                    random.shuffle(self.survivors)
                    votes = []
                    # 如果玩家参与投票
                    if self.is_user_play_games and self.user_name in survivor_names:
                        for i, survivor in enumerate(self.survivors):
                            if survivor.name == self.user_name:
                                while self.user_input is None:
                                    time.sleep(0.1)
                                user_text = self.user_input
                                self.user_input = None
                                user_vote = extract_name_and_id(user_text)[0]
                                temp_user_Msg = UserMsg(content=user_text)
                                hub.broadcast(temp_user_Msg)
                                self.append_output_signal.emit(temp_user_Msg.to_str())
                                votes.append(user_vote)
                            else:
                                x = survivor(hint)
                                self.append_output_signal.emit(x.to_str())
                                votes.append(extract_name_and_id(x.to_str())[0])
                    # 全部为智能体参加投票
                    else:
                        for survivor in self.survivors:
                            x = survivor(hint)
                            self.append_output_signal.emit(x.to_str())
                            votes.append(extract_name_and_id(x.content)[0])

                    vote_res = majority_vote(votes)
                    voting_times += 1
                    
                    # 如果有最终投票结果，且在名单中。就广播结果，修改玩家状态，投票结束
                    if vote_res is not None :
                        if vote_res in survivor_names:
                            result = HostMsg(content=Prompts.to_all_res.format(vote_res))
                            self.append_output_signal.emit(result.to_str())
                            hub.broadcast(result)
                            # 更新玩家状态
                            self.survivors, self.wolves = update_alive_players(
                                self.survivors,
                                self.wolves,
                                vote_res,
                            )
                            # 更新幸存者名单
                            survivor_names = [agent.name for agent in self.survivors]
                            voting_complete = True
                            break
                        # 此处为玩家已经淘汰的处理方法
                        else:
                            hint = HostMsg(content=Prompts.to_all_no_player.format(vote_res))
                            hub.broadcast(hint)
                            self.append_output_signal.emit(hint.to_str())
                            if voting_times == 2:
                                hint = HostMsg(content=Prompts.to_all_no_elimination)
                                hub.broadcast(hint)
                                self.append_output_signal.emit(hint.to_str())
                    # 此处为意见不合，或者全部弃权的处理方法
                    else: 
                        if voting_times == 2:
                            hint = HostMsg(content=Prompts.to_all_no_elimination)
                            hub.broadcast(hint)
                            self.append_output_signal.emit(hint.to_str())
                            voting_complete = True
                        else:
                            hint = HostMsg(content=Prompts.to_all_nonsense)
                            hub.broadcast(
                                hint,
                            )
                            self.append_output_signal.emit(hint.to_str())
                
                if self.check_winning(self.survivors, self.wolves, "Moderator"):
                        break
                hint = HostMsg(content=Prompts.to_all_continue)
                hub.broadcast(hint)
                self.append_output_signal.emit(hint.to_str())
    
    @pyqtSlot(str)
    def receive_user_input(self, user_input):
        self.user_input = user_input








def main() -> None:
    app = QApplication([])  # 创建一个QApplication实例
    window = WerewolfGameWindow()  # 创建WerewolfGameWindow实例
    window.show()  # 显示窗口


    """werewolf game"""
    # 初始设置
    # 使用相对路径访问res目录中的配置文件
    agent_configs = os.path.join("res", "configs", "agent_configs.json")
    model_configs = os.path.join("res", "configs", "model_configs.json")
    roles_dict = {"werewolf": "狼人","villager": "村民","seer": "预言家","witch": "女巫"}
    # 设置上帝
    HostMsg = partial(Msg, name="Moderator", role="assistant", echo=True)
    # 治愈和投毒
    healing, poison = True, True
    # 狼人最大交流回合数
    # MAX_WEREWOLF_DISCUSSION_ROUND = 5
    # 游戏最大轮数
    MAX_GAME_ROUND = 11
    # 角色字典
    
    # 初始化角色列表
    roles = generate_roles(num_villagers=2)

    # self.append_output_signal.emit(roles)
    # 随机化agentconfigs
    generator = configs.AgentConfigGenerator(roles,agent_configs)
    generator.generate_agents_config()
    
    # 设置玩家是否参与游戏的开关
    is_user_play_games = False
    
    # 初始化玩家
    user_name, user_role = "", ""
    if is_user_play_games:
        user_name, user_role = generator.choose_random_player_from_config()
        # 初始化玩家
        # UserMsg = partial(Msg, name=f"{user_name}", role=f"{user_name}", echo=True)
        # window.append_output(f"玩家您好，您在本次游戏中的名字为{user_name}，您的身份为{roles_dict[user_role]}，请享受游戏的过程。")
    
    # 初始化智能体
    survivors = agentscope.init(   
        model_configs=model_configs,
        agent_configs=agent_configs,
        project="Werewolf"
    )

    # 划分阵营
    wolves, witch, seer = select_roles(survivors, roles)
    game_thread = WerewolfGameThread(roles, survivors, witch, seer, wolves, roles_dict, MAX_GAME_ROUND, healing, poison, is_user_play_games,user_name, user_role)
    game_thread.append_output_signal.connect(window.append_output)
    window.user_input_signal.user_input_received.connect(game_thread.receive_user_input)
    game_thread.request_discussion_end_signal.connect(window.set_discussion_end_buttons_visibility)

    def on_start_game():
        game_thread.start()

    window.start_game_signal.connect(on_start_game)  # 连接窗口的启动游戏信号到on_start_game函数

    app.exec_()  # 启动Qt应用程序事件循环


if __name__ == "__main__":
    # agentscope.studio.init(run_dirs="./runs")
    main()
