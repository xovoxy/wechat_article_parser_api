
---

````markdown
# 📰 WeChat Article Parser API

一个用于 **解析微信公众号文章内容** 的 RESTful API 服务。  
支持提取文章标题、作者、发布时间、正文、封面图、阅读量、点赞数等结构化信息。

---

## 🚀 功能特性

- ✅ 解析任意公众号文章（`mp.weixin.qq.com/s/...`）
- ✅ 自动渲染 JavaScript 内容（Playwright）
- ✅ 提取结构化信息（标题、作者、正文等）
- ✅ Redis 缓存 & 请求限流
- ✅ 提供 RESTful API 接口
- ✅ 可部署于 Docker / n8n / 本地环境

---

## 🧱 系统架构

```text
Client → FastAPI → Playwright → BeautifulSoup → Redis → (MongoDB 可选)
````

---

## 🧩 项目结构

```
wechat-article-parser/
├── app/
│   ├── main.py           # FastAPI 主入口
│   ├── crawler.py        # Playwright 爬虫
│   ├── parser.py         # HTML 解析模块
│   ├── cache.py          # Redis 缓存封装
│   ├── models.py         # 数据模型 (Pydantic)
│   ├── config.py         # 环境配置
│   └── utils.py          # 工具函数
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
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
{ "status": "ok", "uptime": "1423s" }
```

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

## 📦 Docker 运行

### 构建并运行

```bash
docker-compose up -d
```

### 示例 docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
  redis:
    image: redis:alpine
```

---

## 🧰 环境变量 (.env)

| 名称              | 示例值                      | 说明         |
| --------------- | ------------------------ | ---------- |
| REDIS_URL       | redis://localhost:6379/0 | Redis 缓存地址 |
| MAX_CONCURRENCY | 5                        | 最大并发抓取数    |
| USER_AGENT      | Mozilla/5.0 ...          | 浏览器UA字符串   |
| API_TOKEN       | abc123                   | （可选）访问验证   |

---

## 🛡️ 反爬与限流策略

* 随机 User-Agent 池
* 每请求随机延迟 1~3s
* Redis 限流：单 IP 每分钟 ≤ 10 次
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

