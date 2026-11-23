# MCP 实验3：标准化工具接口实践

## 1. 配置记录
- **客户端**：Python 编写的 `demo_client.py`，使用 `stdio_client` 连接。
- **服务端配置**：`StdioServerParameters(command="python", args=["hsk_mcp_server.py"])`。

## 2. 调用证据（工具列表与返回）
我已经成功拉起服务端并验证了工具。
- 工具列表：`['hsk_level', 'list_by_level']`
- 调用 `hsk_level('把')` 返回：`把 -> 3 级`
- 调用 `list_by_level('4')` 返回：`坚持、商量`

（请把你刚才跑出三行绿勾的截图拖拽<img width="1948" height="1414" alt="屏幕截图 2026-11-23 133051" src="https://github.com/user-attachments/assets/3dc133ec-303f-4584-b567-e5c100381c69" />
/粘贴到此处）

## 3. 三者辨析
- **Function Calling**：是模型侧的机制，解决大模型在对话中如何输出“想调用什么工具”的指令。
- **MCP**：是工具侧的协议，解决不同提供方的工具如何以标准接口被统一发现和调用。
- **普通 API 调用**：是程序侧的直连，由程序员写死请求格式，没有大模型的自主决策参与。
