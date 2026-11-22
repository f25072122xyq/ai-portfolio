from mcp.server import MCPServer

# 创建服务端
mcp = MCPServer("HSK_MCP_Server")

@mcp.tool()
def hsk_level(word: str) -> str:
    """查 HSK 等级。输入词语，返回等级。"""
    vocab_dict = {"把": "3", "坚持": "4", "商量": "4"}
    return f"{word} 是 {vocab_dict.get(word, '未知')} 级"

if __name__ == "__main__":
    # 启动服务端（等待客户端连接）
    mcp.run()
