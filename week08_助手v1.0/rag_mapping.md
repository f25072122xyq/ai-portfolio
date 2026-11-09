# 官方 RAG 流水线 ↔ 我的 rag_qa.py 映射表

| 官方流水线步骤 | 官方/llm-universe 对应做法 | 我的 rag_qa.py / assistant_v1.py 实现 |
| :--- | :--- | :--- |
| **1. Load + Split (加载与分块)** | 官方：Document loader + Text splitter<br>llm-universe C3：读取、清洗与切片 | **我的实现**：`TextLoader` + `RecursiveCharacterTextSplitter`(500/50)。读取了我的 `我的资料.txt` 并进行了分块。 |
| **2. Embed + Store (向量化入库)** | 官方：Embeddings 与 VectorStore 可替换组件<br>llm-universe C3：搭建并使用向量数据库 | **我的实现**：`OllamaEmbeddings(nomic-embed-text)` + `Chroma` 本地持久化。由于我的系统限制，模拟了将文本作为背景知识直接入库的逻辑。 |
| **3. Retrieve (检索)** | 官方 2-Step RAG：检索总在生成之前<br>llm-universe C4：检索问答链 | **我的实现**：编写了 `retrieve(question)` 函数，提取 top-k 相关的资料文本。在 `use_rag=True` 时，先查资料再答。 |
| **4. Prompt + Generate (拼词与生成)** | 官方：检索片段与问题一起加进 prompt<br>llm-universe C4：LLM 接入 LangChain | **我的实现**：`build_prompt()` 拼接 `SYSTEM_HINT` + 资料 + 问题，最后交由 W6 封装的 `LLM().ask(prefer="local")` 生成答案。 |
| **5. Deploy + Evaluate (部署与评估)** | llm-universe C4 用 Streamlit 部署；C5 系统评估与优化 | **我的实现**：在 `assistant_v1.py` 中实现了三问三答演示（见 `answer_log.md`）；W7 幻觉对照表作为最朴素的评估。 |
