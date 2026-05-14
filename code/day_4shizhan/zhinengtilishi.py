import json
import os

# 1. 模拟生成一个“混乱”的历史记录文件
def create_mock_history():
    mock_data = [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮你的？"},
        {"role": "user", "content": "帮我分析一下《流浪地球2》"},
        {"role": "assistant", "content": "这是一部非常棒的科幻电影... (此处省略500字剧情)"},
        {"role": "user", "content": "a" * 2000},  # 模拟用户乱敲的长字符串（脏数据）
        {"role": "assistant", "content": "对不起，我没听懂。"},
    ]
    with open("chat_history_raw.json", "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)

# 2. 核心挑战任务：清洗与统计
def audit_and_clean_memory(input_file: str, output_file: str):
    if not os.path.exists(input_file):
        print("文件不存在")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        history = json.load(f)

    cleaned_history = []
    total_chars = 0
    removed_count = 0

    for msg in history:
        content = msg.get("content", "")
        # 挑战逻辑1：剔除长度超过 1000 字符的异常数据
        if len(content) > 1000:
            removed_count += 1
            continue
        
        cleaned_history.append(msg)
        total_chars += len(content)

    # 挑战逻辑2：Token 估算 (假设 1个汉字/字符 约 0.7 Token)
    estimated_tokens = int(total_chars * 0.7)
    
    # 保存清洗后的数据
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_history, f, ensure_ascii=False, indent=2)

    print("=== 审计报告 ===")
    print(f"✅ 原始记录条数: {len(history)}")
    print(f"🧹 已清洗异常记录: {removed_count} 条")
    print(f"📊 剩余字符总数: {total_chars}")
    print(f"💰 预估消耗 Token: {estimated_tokens}")
    print(f"💾 清洗后的数据已存入: {output_file}")

# 3. 进阶逻辑：知识提取与持久化
def extract_knowledge_to_db(input_file: str, db_file: str):
    """模拟从对话中提取电影知识并存入‘数据库’"""
    with open(input_file, "r", encoding="utf-8") as f:
        history = json.load(f)
    
    # 简单的关键词提取模拟（实际开发中会配合第一天的 Pydantic）
    movie_db = []
    for msg in history:
        if "《" in msg["content"] and "》" in msg["content"]:
            # 简单模拟提取逻辑
            movie_db.append({
                "source_msg": msg["content"],
                "extracted_at": "2026-05-07"
            })
    
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(movie_db, f, ensure_ascii=False, indent=2)
    print(f"📚 提取到知识点: {len(movie_db)} 条，已存入 {db_file}")

if __name__ == "__main__":
    create_mock_history()
    audit_and_clean_memory("chat_history_raw.json", "chat_history_cleaned.json")
    extract_knowledge_to_db("chat_history_cleaned.json", "movies_knowledge.json")