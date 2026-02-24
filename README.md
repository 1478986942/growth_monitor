# 儿童生长发育智能监测与干预平台

## 项目介绍

本平台旨在帮助家长监测儿童生长发育情况，识别潜在风险，并提供个性化干预方案。通过AI整合生长数据，识别矮小症、肥胖等风险，提供个性化干预方案与就医绿色通道，早期干预价值明确，还可延伸对接母婴、儿科医疗产业链资源。

## 技术栈

### 后端
- **Python 3.7+**
- **Flask** - Web 框架
- **MySQL 5.7+** - 数据库
- **SQLAlchemy** - ORM
- **PyJWT** - JWT 认证
- **Flask-CORS** - 跨域支持
- **scikit-learn** - AI 机器学习模型
- **bcrypt** - 密码加密

### 前端
- **React 18+** - UI 框架
- **Vite** - 构建工具
- **Ant Design** - UI 组件库
- **React Router** - 路由管理
- **Axios** - HTTP 客户端

## 系统功能

1. **用户管理**：注册、登录、个人信息管理
2. **儿童管理**：添加、编辑、删除儿童信息
3. **生长数据**：录入、查询、图表展示生长数据（身高、体重、BMI等）
4. **风险评估**：基于AI模型的生长发育风险评估（矮小症、肥胖等）
5. **干预方案**：根据风险评估结果生成个性化干预方案
6. **就医绿色通道**：对接合作医疗机构，提供优先就诊服务
7. **资源中心**：母婴资源、儿科医疗资源展示

## 快速开始

### 1. 环境准备

- Python 3.7+
- Node.js 14+
- MySQL 5.7+

### 2. 数据库配置

1. 启动 MySQL 服务
2. 创建数据库：
   ```sql
   CREATE DATABASE growth_monitor1 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 导入数据库结构：
   ```bash
   mysql -u root -p growth_monitor1 < database.sql
   ```
4. 修改 `backend/.env` 文件中的数据库连接信息：
   ```
   DATABASE_URI=mysql+pymysql://root:password@localhost:3306/growth_monitor1
   JWT_SECRET=najdlajbdjasbdajdbajdbab
   ```

### 3. 启动后端服务

#### 方法1：使用启动脚本
```bash
start_backend.bat
```

#### 方法2：手动执行
```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5555` 启动。

### 4. 启动前端服务

#### 方法1：使用启动脚本
```bash
frontend\start_frontend.bat
```

#### 方法2：手动执行
```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

## 项目结构

```
Lighthouse of Growth1/
├── backend/              # 后端项目
│   ├── ai/             # AI模型模块
│   │   └── growth_analyzer.py  # 生长发育分析模型
│   ├── models/          # 数据库模型
│   ├── routes/          # API路由
│   ├── .env            # 环境变量
│   ├── app.py          # 后端应用入口
│   └── requirements.txt # 后端依赖
├── frontend/            # 前端项目
│   ├── src/            # 前端源代码
│   │   ├── components/  # 组件
│   │   ├── pages/       # 页面
│   │   ├── services/    # API服务封装
│   │   ├── styles/      # 样式
│   │   ├── App.jsx      # 应用入口
│   │   └── main.jsx     # 主文件
│   ├── package.json     # 前端依赖
│   └── vite.config.js   # Vite配置
├── database.sql         # 数据库结构
├── start_backend.bat    # 后端启动脚本
└── frontend/
    └── start_frontend.bat # 前端启动脚本
```

## 使用指南

### 1. 注册登录

- 访问 `http://localhost:3000/login` 登录系统
- 访问 `http://localhost:3000/register` 注册新账号

### 2. 添加儿童信息

- 登录后，点击左侧菜单的「儿童管理」
- 点击「添加儿童」按钮，填写儿童基本信息

### 3. 录入生长数据

- 在「儿童管理」页面，点击对应儿童的「生长数据」按钮
- 点击「添加数据」按钮，录入测量日期、身高、体重等数据
- 系统会自动计算 BMI 并生成生长趋势图表

### 4. 风险评估

- 在「儿童管理」页面，点击对应儿童的「风险评估」按钮
- 选择儿童后，点击「开始评估」按钮
- 系统会基于 AI 模型进行风险评估
- 查看评估结果，包括矮小症风险、肥胖风险等

### 5. 生成干预方案

- 在风险评估页面，点击「生成干预方案」按钮
- 系统会根据评估结果生成个性化的干预方案
- 查看和管理干预方案的执行状态

### 6. 使用就医绿色通道

- 点击左侧菜单的「就医绿色通道」
- 查看合作医疗机构信息
- 联系医疗机构进行预约就诊

### 7. 浏览资源中心

- 点击左侧菜单的「资源中心」
- 查看母婴资源和儿科医疗资源

## API 接口文档

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 儿童管理
- `GET /api/children` - 获取儿童列表
- `POST /api/children` - 添加儿童
- `PUT /api/children/:id` - 更新儿童信息
- `DELETE /api/children/:id` - 删除儿童

### 生长数据
- `GET /api/growth/child/:child_id` - 获取儿童生长数据
- `POST /api/growth` - 添加生长记录
- `PUT /api/growth/:id` - 更新生长记录
- `DELETE /api/growth/:id` - 删除生长记录

### 风险评估
- `GET /api/risk/child/:child_id` - 获取儿童评估记录
- `POST /api/risk/assess/:child_id` - 发起风险评估

### 干预方案
- `GET /api/intervention/child/:child_id` - 获取儿童干预方案
- `POST /api/intervention/generate` - 生成干预方案
- `PATCH /api/intervention/:id/status` - 更新干预方案状态

### 医院资源
- `GET /api/hospital` - 获取医院列表

### 资源中心
- `GET /api/resource` - 获取资源列表

## 开发说明

### 后端开发
- 使用 Flask Blueprint 模块化路由
- 使用 SQLAlchemy ORM 进行数据库操作
- 使用 JWT 进行用户认证
- 使用 scikit-learn 构建 AI 模型

### 前端开发
- 使用 React Hooks 管理状态
- 使用 Ant Design 组件库构建 UI
- 使用 React Router 进行路由管理
- 使用 Axios 封装 API 请求

## 部署说明

### 生产环境部署
1. 修改 `.env` 文件中的配置为生产环境配置
2. 使用 `gunicorn` 或 `uWSGI` 部署 Flask 应用
3. 使用 `nginx` 反向代理前后端
4. 构建前端：`npm run build`
5. 将前端构建产物部署到静态服务器

## 注意事项

- 本项目不使用云服务，纯本地部署
- 确保 MySQL 服务已启动并可连接
- 确保 Python 和 Node.js 环境已正确配置
- 首次运行需要安装依赖

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系项目维护者。
