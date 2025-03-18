from agentscope.models import ModelWrapperBase
import requests
from agentscope.message import Msg

class MyModelWrapper(ModelWrapperBase):
    model_type: str = "my_model"

    def __init__(self, config_name, **kwargs):
        super().__init__(config_name=config_name)
        self.api_key = kwargs.get("api_key")
        self.api_url = kwargs.get("api_url")
        self.model_name = kwargs.get("model_name")  # 添加model_name

    def __call__(self, input, **kwargs):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }
        messages = input.get("messages", [])  # 获取消息列表

        payload = {
            "model": self.model_name,  # 使用self.model_name
            "messages": [{"role": msg.get("role"), "content": msg.get("content")} for msg in messages],
            "stream": kwargs.get("stream", False)
        }

        try:
            response = requests.post(f"{self.api_url}/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()  # 如果响应状态码不是 200，将引发异常
            
            return response  # 返回完整的响应对象

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"请求失败：{e}")

        except Exception as e:
            raise RuntimeError(f"发生异常：{e}")

    def format(self, *args):
        messages = []
        for msg in args:
            if isinstance(msg, Msg):
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            elif isinstance(msg, list):
                for sub_msg in msg:
                    if isinstance(sub_msg, Msg):
                        messages.append({
                            "role": sub_msg.role,
                            "content": sub_msg.content
                        })
        return {
            "model": self.model_name,  # 使用self.model_name
            "messages": messages,
            "stream": False  # 默认不使用流式输出
        }

