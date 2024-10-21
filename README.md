# 项目名称

这是一个基于 Flask 的云函数管理系统，允许用户动态创建、编辑和删除函数，并通过 API 密钥进行身份验证。

## 目录结构

```
.
├── app.py                  # 主应用程序文件
├── config.py               # 配置文件
├── config.json             # 初始用户和 API 密钥配置
├── Dockerfile              # Docker 配置文件
├── docker-compose.yml      # Docker Compose 配置文件
├── models.py               # 数据库模型
├── requirements.txt        # 项目依赖
├── functions/              # 存放动态函数的目录
│   ├── gathering_message.py # 示例函数
│   ├── qqbot.py            # QQ 机器人函数
│   ├── search.py           # 搜索函数
│   ├── example.py          # 示例函数
│   └── test.py             # 测试函数
├── templates/              # 存放 HTML 模板的目录
│   ├── admin.html          # 管理页面模板
│   ├── edit_function.html  # 编辑函数页面模板
│   └── login.html          # 登录页面模板
└── .gitattributes          # Git 属性文件
```

## 安装与运行

1. 克隆项目到本地：

   ```bash
   git clone <项目地址>
   cd <项目目录>
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动应用：

   ```bash
   python app.py
   ```

   或者使用 Docker 启动：

   ```bash
   docker-compose up --build
   ```

## Docker 部署说明

1. 确保已安装 Docker 和 Docker Compose。
2. 在项目根目录下，使用以下命令构建 Docker 镜像：

   ```bash
   docker-compose build
   ```

3. 启动 Docker 容器：

   ```bash
   docker-compose up
   ```

4. 访问 `http://localhost:8888/login` 进行登录。

## 使用说明

- 登录后可以访问管理页面，进行函数的创建、编辑和删除。
- 支持通过 API 密钥进行身份验证。

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证

本项目采用 MIT 许可证，详细信息请查看 LICENSE 文件。
