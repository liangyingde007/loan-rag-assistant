# 条例检索演示启动与部署

## 能力与边界

同一个 FastAPI 服务提供网页、JSON 问答接口和只读示例文档。无需数据库、API Key 或模型服务。查询按内置文档的主题关键词与同义表达定位章节，以字符二元组重合度辅助排序，最多返回三个段落。

答案由检索到的原文摘录组成，保留引用编号、章节、位置与版本；没有主题匹配时不回答，问具体数值而文档没有这些数值时提示“依据不足”。这是可运行的文本检索与引用演示，不是大模型生成、Embedding 向量检索或经过 RAGAS 评估的完整 RAG。

`knowledge_base/demo_rules.json` 是构造的演示文档，不是银行政策、真实合同或金融建议。原 `knowledge_base/loan_rules.txt` 保留。网页没有文件上传、贷款申请、真实审批或对话持久化功能。

## 本地启动

Python 3.12。在仓库根目录创建并激活独立环境：

```bash
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# Linux: source .venv/bin/activate
python -m pip install -r requirements-deploy.txt
python -m backend.serve
```

打开 `http://127.0.0.1:8000/`。部署入口监听 `0.0.0.0`，读取平台提供的 `PORT`。仅本机预览用：

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 4181
```

接口：

- `GET /healthz`：状态、版本与章节数。
- `POST /api/chat`：JSON `{"question":"贷款期限如何确定？"}`。
- `GET /api/documents/demo-loan-v1`：公开的示例原文，无本机路径。
- `GET /docs`：接口文档。
- `POST /chat?question=...`：原查询参数接口，保留 answer 字符串与 context 列表。

## 部署

容器命令：

```bash
docker build -t lyd-loan-demo .
docker run --rm -p 8000:8000 -e PORT=8000 lyd-loan-demo
```

Docker 使用非 root 用户，按白名单复制业务模块、示例文档与网页。本机 Docker daemon 当前不可用，镜像构建与 Linux 运行尚未实测；本地 Python 运行不等于容器验证。

`render.yaml` 为可选免费方案模板，`lyd-rag` 只是建议服务名，域名尚未分配。也可用 Render Python Web Service，Python 选择 3.12，构建命令 `python -m pip install -r requirements-deploy.txt`，启动命令 `python -m backend.serve`，健康路径 `/healthz`。

Render 免费服务空闲 15 分钟后休眠，唤醒约一分钟；求职展示需要考虑首次打开的等待。服务本身使用随版本发布的只读知识库，不依赖临时文件系统保存数据。[官方说明](https://render.com/docs/free)

发布需要账号与正确的源代码版本。不要将原始求职资料、环境文件、其他仓库或账号密钥上传。当前连接器的 GitHub 账号与本项目所有者不同，不能直接推送到错误账号。实际发布后核对匿名访问、HTTPS、引用跳转、拒答与手机布局，再交付不超过 40 字符的完整 URL。

## 当前本机工作环境

本轮复用 D:\mywebsite\deployment\.venv 的固定 FastAPI / Uvicorn 依赖，启动 4181 端口。完整 HTTP 检查脚本 `D:\mywebsite\deployment\check_loan.py` 可用 `--url` 指定服务、`--output` 保存记录；部署白名单包在同工作目录 artifacts 中。公网地址尚未创建。
