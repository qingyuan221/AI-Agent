import json
import asyncio
import os
from datetime import datetime
from typing import List, Dict

class ChatMemory:
    def __init__(self, file_path: str = "chat_history.json"):
        self.file_path = file_path
        self.history = self._load_from_disk()

    def _load_from_disk(self) -> List[Dict]:
        """从磁盘加载历史记录，如果文件不存在则返回空列表"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_to_disk(self):
        """将当前内存中的历史记录保存到磁盘"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_message(self, role: str, content: str):
        """添加一条消息并记录时间戳"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.save_to_disk()

    def get_messages_for_llm(self, limit: int = 10) -> List[Dict]:
        """
        获取最近的 N 条消息，并格式化为 LLM 需要的格式
        这是防止 Token 溢出的简单策略
        """
        recent_history = self.history[-limit:]
        return [{"role": m["role"], "content": m["content"]} for m in recent_history]

# --- 实战演示 ---
async def chat_with_memory():
    memory = ChatMemory()
    print(f"📜 已加载 {len(memory.history)} 条历史记录")

    # 模拟用户输入
    user_query = "我还记得我昨天问你的第一个问题是什么吗？"
    
    # 逻辑：先从 memory 获取历史，再发给 AI
    messages = [
        {"role": "system", "content": "你是一个有记忆的助手。"}
    ] + memory.get_messages_for_llm()
    
    # 模拟 AI 记录
    memory.add_message("user", user_query)
    print(f"🆕 已记录新消息：{user_query}")
    
    # 模拟助手回复
    assistant_reply = "抱歉，目前的存储逻辑仅记录文本。你可以查看 chat_history.json 确认内容。"
    memory.add_message("assistant", assistant_reply)

if __name__ == "__main__":
    asyncio.run(chat_with_memory())
