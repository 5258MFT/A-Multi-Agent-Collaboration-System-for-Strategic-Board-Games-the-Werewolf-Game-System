# 文件构成说明

## 1. 项目概述

这是一个基于agentscope架构的多智能体狼人杀项目。在这个项目中，你既可以欣赏agent扮演不同角色进行狼人杀游戏，也可以随机扮演其中一位角色参与到游戏中。同时本项目适配了市面上主流大模型的api，包括但不限于deepseek、chatgpt、qwen、GLM，配置简单、上手容易。在这个项目中，我们使用了多种文件来构建和管理我们的系统。每个文件都有其特定的作用和结构。以下是对主要文件和文件夹的详细说明。

## 2.运行效果

![1742278158059](images/README/1742278158059.png)

## 3.文件夹结构

project/

├── res/

│ ├── agent_prompt/

│ │ ├── seer.txt

│ │ ├── villager.txt

│ │ ├── werewolf.txt

│ │ └── valid.txt

│ ├── configs/

│ │ ├── agent_configs.json

│ │ └── model_configs.json

│ ├── other_res/

│ │ ├── 略

│ │ └── 略

├── configs.py

├── User_player.py

├── werewolf_gui.py

├── werewolf_utils.py

├── werewolf.py

└── README.md

## 4. 主要文件说明

## 文件和文件夹说明

### res/

包含了与资源相关的子目录和文件。

#### agent_prompt/

存储了不同角色的提示文件。

- `seer.txt`: 预言家的提示文件。
- `villager.txt`: 村民的提示文件。
- `werewolf.txt`: 狼人的提示文件。
- `witch.txt`: 女巫的提示文件。

#### configs/

存储了与代理和模型配置相关的JSON文件。

- `agent_configs.json`: 代理配置文件。
- `model_configs.json`: 模型配置文件。

#### other_res/

存储了其他资源文件，这些文件在此处略去。

### configs.py

用于配置的Python脚本。

### User_player.py

用户玩家相关的Python脚本。

### werewolf_gui.py

用于图形用户界面（GUI）处理的Python脚本。

### werewolf_utils.py

包含狼人游戏的实用工具函数的Python脚本。

### werewolf.py

主狼人游戏逻辑的Python脚本。

### README.md

项目的说明文件，提供了项目的概述、使用方法、安装步骤等信息。

## 5.安装指南

为了安装AgentScope，您需要安装Python 3.9或更高版本。我们建议专门为AgentScope设置一个新的虚拟环境：

## 创建虚拟环境

### 使用Conda

如果您使用Conda作为环境管理工具，您可以使用以下命令创建一个新的Python 3.9虚拟环境：

```bash
# 使用Python 3.9创建一个名为"agentscope"的新虚拟环境
conda create -n agentscope python=3.9

# 激活虚拟环境
conda activate agentscope
```

```###

如果您使用virtualenv，您可以首先安装它（如果尚未安装），然后按照以下步骤创建一个新的虚拟环境：

```

# 如果尚未安装virtualenv，请先安装它

pip install virtualenv

# 使用Python 3.9创建一个名为"agentscope"的新虚拟环境

virtualenv agentscope --python=python3.9

# 激活虚拟环境

source agentscope/bin/activate  # 在Windows上使用`agentscope\Scripts\activate`

```
## 安装AgentScope

### 从源码安装

按照以下步骤从源代码安装AgentScope，并以可编辑模式安装AgentScope：

**注意：该项目正在积极开发中，建议从源码安装AgentScope！**

```

# 从GitHub上拉取AgentScope的源代码

git clone https://github.com/modelscope/agentscope.git
cd agentscope

# 针对本地化的multi-agent应用

pip install -e .

# 为分布式multi-agent应用

pip install -e .[distribute]  # 在Mac上使用`pip install -e .\[distribute\]`

```
### 

**注意：[distribute]选项安装了分布式应用程序所需的额外依赖项。在运行这些命令之前，请激活您的虚拟环境。**

### 使用Pip安装

如果您选择从Pypi安装AgentScope，可以使用pip轻松地完成：

```

# 针对本地化的multi-agent应用

pip install agentscope --pre

# 为分布式multi-agent应用

pip install agentscope[distribute] --pre  # 在Mac上使用`pip install agentscope\[distribute\] --pre`

```
### 接下来只需要将本项目放入agentscope\examples文件夹下即可

## 5. 总结

以上文件和文件夹构成了我们项目的基础。每个文件都承担了特定的角色，确保了项目的有序管理和高效执行。如有任何问题或需要进一步的解释，请参阅相关文件或联系我们的团队。邮箱为：3147761835@qq.com
```
