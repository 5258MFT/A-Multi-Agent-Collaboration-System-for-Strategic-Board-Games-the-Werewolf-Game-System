import os
import json
import random

class AgentConfigGenerator:
    def __init__(self, roles, output_file='.\\res\\configs\\agent_configs.json', prompt_folder='.\\res\\agent_prompt'):
        self.roles = roles
        self.output_file = output_file
        self.prompt_folder = prompt_folder
        self.player_names = [f"Player{i+1}" for i in range(len(roles))]  # 根据角色数量生成玩家名称列表

    def generate_agents_config(self):
        agents_config = []
        # 计算玩家数量
        num_players = len(self.player_names)

        # 生成玩家名字列表的字符串
        player_names_str = ", ".join(self.player_names)

        pre_text = f"在狼人杀游戏中，一共有{num_players}个玩家, 分别为{player_names_str}.\n\n"
        for i, role in enumerate(self.roles):
            player_name = self.player_names[i]
            prompt_file = os.path.join(self.prompt_folder, f"{role.lower()}.txt")
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                sys_prompt = f.read().strip()

            last_text = f"你在游戏中是{player_name}\n"
            agent = {
                "class": "DictDialogAgent",
                "args": {
                    "name": player_name,
                    "sys_prompt": pre_text + sys_prompt + last_text,
                    "model_config_name": "my_model_config",
                    "use_memory": True
                }
            }
            agents_config.append(agent)

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(agents_config, f, ensure_ascii=False, indent=4)

        # print(f"生成的代理配置已写入 {self.output_file} 文件。")
    
    
    def choose_random_player_from_config(self):
        # 读取当前配置文件
        with open(self.output_file, 'r', encoding='utf-8') as f:
            agents_config = json.load(f)

        # 如果配置为空，则返回 None, None
        if not agents_config:
            return None, None

        # 随机选择一个玩家的配置
        index = random.randint(0, len(agents_config) - 1)
        
        # 此处为移除选定玩家配置
        # removed_agent = agents_config.pop(index)

        # 更新配置文件
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(agents_config, f, ensure_ascii=False, indent=4)

        # 提取被移除玩家的角色和姓名
        chosen_player_name = agents_config[index]["args"]["name"]
        chosen_role_index = self.player_names.index(chosen_player_name)
        chosen_role = self.roles[chosen_role_index]

        return chosen_player_name, chosen_role

# 使用示例
if __name__ == "__main__":
    roles = ["werewolf", "werewolf", "villager", "villager", "seer", "witch"]
    generator = AgentConfigGenerator(roles)
    generator.generate_agents_config()
    
    # 从配置中移除随机玩家
    removed_player, removed_role = generator.remove_random_player_from_config()
    print(f"移除的玩家: {removed_player}, 角色: {removed_role}")
    print(generator.player_names)