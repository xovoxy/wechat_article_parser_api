# 📰 WeChat Article Parser API

一个用于 **解析微信公众号文章内容** 的 RESTful API 服务。  
支持提取文章标题、作者、发布时间、正文、封面图、阅读量、点赞数等结构化信息。

---

## 🚀 功能特性

- ✅ 解析任意公众号文章（`mp.weixin.qq.com/s/...`）
- ✅ 自动渲染 JavaScript 内容（Playwright）
- ✅ 提取结构化信息（标题、作者、正文等）
- ✅ 提供 RESTful API 接口
- ✅ 可部署于 Docker / n8n / 本地环境

---

## 🧱 系统架构

```
Client → FastAPI → Playwright → BeautifulSoup
```

---

## 🧩 项目结构

```
wechat-article-parser/
├── app/
│   ├── main.py           # FastAPI 主入口
│   ├── crawler.py        # Playwright 爬虫
│   ├── parser.py         # HTML 解析模块
│   ├── models.py         # 数据模型 (Pydantic)
│   ├── config.py         # 环境配置
│   └── utils.py          # 工具函数
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📦 安装与运行

### 方式一：Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方式二：本地运行

1. **安装依赖**

```bash
pip install -r requirements.txt
playwright install chromium
```

2. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，配置 Redis 等参数
```

3. **启动 Redis**

```bash
# 使用 Docker 启动 Redis
docker run -d -p 6379:6379 redis:7-alpine

# 或使用本地 Redis
redis-server
```

4. **启动 API 服务**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 API 使用说明

### 1️⃣ 解析文章接口

**GET** `/api/parse?url=<公众号文章链接>`

#### 请求示例

```bash
curl "http://localhost:8000/api/parse?url=https://mp.weixin.qq.com/s/abcd1234"
```

#### 返回示例

```json
{
  "title": "深度学习的三个阶段",
  "author": "AI小站",
  "publish_time": "2025-10-20 08:30",
  "cover": "https://mmbiz.qpic.cn/xyz.jpg",
  "content_html": "<p>近年来，深度学习...</p>",
  "content_text": "近年来，深度学习的发展经历了三个阶段...",
  "read_count": 12345,
  "like_count": 678,
  "url": "https://mp.weixin.qq.com/s/abcd1234",
  "parsed_at": "2025-11-04T21:35:12Z"
}
```

---

### 2️⃣ 健康检查接口

**GET** `/api/health`

返回：

```json
{
  "status": "ok",
  "uptime": "1423s"
}
```

---

### 3️⃣ API 文档

启动服务后，访问以下地址查看交互式 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧠 技术栈

| 模块       | 技术                      |
| -------- | ----------------------- |
| Web 框架   | FastAPI                 |
| 异步浏览器    | Playwright              |
| 解析引擎     | BeautifulSoup / lxml    |
| 缓存       | Redis                   |
| 数据存储（可选） | MongoDB                 |
| 部署       | Docker / Docker Compose |

---

## 🧰 环境变量 (.env)

| 名称              | 示例值                      | 说明         |
| --------------- | ------------------------ | ---------- |
| MAX_CONCURRENCY | 5                        | 最大并发抓取数    |
| USER_AGENT      | Mozilla/5.0 ...          | 浏览器UA字符串   |
| API_TOKEN       | abc123                   | （可选）访问验证   |

---

## 🛡️ 反爬与限流策略

* 随机 User-Agent 池
* 每请求随机延迟 1~3s
* 自动重试与错误捕获
* 浏览器指纹模拟（非 headless 模式可选）

---

## 🔮 后续扩展

| 模块       | 功能                          |
| -------- | --------------------------- |
| 文本摘要     | 使用 GPT 或 Pegasus 生成摘要       |
| 内容分类     | TF-IDF / Embedding 分类       |
| OCR 图文提取 | 从文章图像中提取文字                  |
| 翻译支持     | 集成 DeepL / Google Translate |
| Web 控制台  | 可视化任务与缓存管理                  |

---

## 📝 开发说明

### 项目结构说明

- `app/main.py`: FastAPI 应用主入口，定义路由和中间件
- `app/crawler.py`: Playwright 爬虫封装，负责抓取网页内容
- `app/parser.py`: HTML 解析器，提取文章结构化信息
- `app/models.py`: Pydantic 数据模型，定义 API 请求/响应格式
- `app/config.py`: 配置管理，从环境变量读取配置
- `app/utils.py`: 工具函数集合

### 测试

```bash
# 测试解析接口
curl "http://localhost:8000/api/parse?url=https://mp.weixin.qq.com/s/YOUR_ARTICLE_ID"

# 测试健康检查
curl "http://localhost:8000/api/health"
```

---

## 📄 License

MIT License
