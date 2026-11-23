from mcp.server import MCPServer

mcp = MCPServer("HSK_MCP_Server")

VOCAB_DATA = [
    {"词汇": "把", "等级": "3"},
    {"词汇": "坚持", "等级": "4"},
    {"词汇": "商量", "等级": "4"},
    {"词汇": "愚公", "等级": "5"}
]

@mcp.tool()
def hsk_level(word: str) -> str:
    """查询某个词属于 HSK 几级。"""
    for row in VOCAB_DATA:
        if row["词汇"] == str(word).strip():
            return f"{word} -> {row['等级']} 级"
    return f"未找到 {word}"

@mcp.tool()
def list_by_level(level: str) -> str:
    """列出某一 HSK 等级的全部词汇。"""
    out = [row["词汇"] for row in VOCAB_DATA if row["等级"] == str(level).strip()]
    return "、".join(out) if out else "该等级暂无词汇"

# 🌟 这就是老师要求的第3个工具！
@mcp.tool()
def count_by_level(level: str) -> str:
    """返回某一 HSK 等级的词汇总数。"""
    count = len([row for row in VOCAB_DATA if row["等级"] == str(level).strip()])
    return f"{level} 级共有 {count} 个词汇。"

if __name__ == "__main__":
    try:
        print("【系统】MCP 服务端已启动，正在等待客户端连接...")
        mcp.run()
    except KeyboardInterrupt:
        pass
