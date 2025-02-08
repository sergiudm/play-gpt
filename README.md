# PlayGPT

PlayGPT 是一个利用 AI 提供个性化玩乐（旅行、休闲等）方案的 Web 应用。用户可以通过简单的对话界面与 AI 助手交流，根据自己的需求和个性化特征，获取定制化的行程安排与建议。

## 功能介绍

- **个性化测评**  
  通过简单的问卷调查，帮助用户构建个人画像（例如：消费偏好、旅行方式、旅行节奏等）。

- **定制化对话**  
  用户通过对话界面输入需求，系统结合用户画像及 OpenAI 提供的智能回复，生成详细的出行或玩乐方案。

- **简洁的前端页面**  
  提供首页、对话界面等页面，使用 Bootstrap 框架实现简洁、响应式的页面布局。

- **自动化部署**  
  通过 GitHub Actions 实现静态页面（如首页、对话页面）的自动部署到 GitHub Pages（仅适用于静态内容）。

## 技术栈

- **后端**：  
  - [Flask](https://flask.palletsprojects.com/)（Python Web 框架）  
  - SQLAlchemy（ORM，用于数据存储，开发阶段可使用 SQLite）

- **AI 服务**：  
  - [OpenAI API](https://openai.com/api/)（生成定制化旅行方案）

- **前端**：  
  - HTML5 / CSS3  
  - [Bootstrap](https://getbootstrap.com/)（前端样式框架）

- **部署与持续集成**：  
  - GitHub Actions（自动构建、部署）  
  - GitHub Pages（静态页面托管，仅适用于无后端功能的页面）

## 项目目录结构

```plaintext
playgpt/
├── app.py               # Flask 应用入口
├── models.py            # 数据库模型定义
├── requirements.txt     # 项目依赖包列表
├── templates/           # HTML 模板文件夹
│   ├── base.html        # 基础公共模板
│   ├── index.html       # 首页
│   ├── chat.html        # 对话页面
│   └── ...              # 其他页面模板
└── static/              # 静态资源（CSS、JS、图片等）
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your_username/play-gpt.git
cd play-gpt
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. 配置环境变量

确保设置环境变量 `OPENAI_API_KEY` 为你的 OpenAI API 密钥，例如在终端中：

```bash
export OPENAI_API_KEY=your_openai_api_key
```

或者在项目根目录创建一个 `.env` 文件，并使用相关包加载环境变量。

### 4. 运行应用

```bash
python app.py
```

在浏览器中打开 [http://127.0.0.1:5000](http://127.0.0.1:5000) 即可查看效果。

## 部署说明

### 使用 GitHub Actions 部署静态页面到 GitHub Pages

本项目中包含一个 GitHub Actions 工作流（位于 `.github/workflows/github-pages.yml`），用于自动将静态页面部署到 GitHub Pages。需要注意：

- GitHub Pages 仅支持静态内容。如果需要部署完整的 Flask 后端，请考虑其他平台（如 Heroku、Render、Vercel 等）。
- 请确保你的仓库中有静态页面（例如 `index.html` 等），并且工作流配置中的 `publish_dir` 指向正确的目录。