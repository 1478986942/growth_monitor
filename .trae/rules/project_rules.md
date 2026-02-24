# 儿童生长发育智能监测与干预平台

## 项目介绍

本平台旨在帮助家长监测儿童生长发育情况，识别潜在风险，并提供个性化干预方案。通过AI整合生长数据，识别矮小症、肥胖等风险，提供个性化干预方案与就医绿色通道，早期干预价值明确，还可延伸对接母婴、儿科医疗产业链资源。

## 技术栈

- **后端**：Python + Flask + MySQL
- **前端**：React + Vite
- **AI模型**：scikit-learn
- **不使用云服务**，纯本地部署

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

1. 启动MySQL服务
2. 创建数据库：
   ```sql
   CREATE DATABASE growth_monitor DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 导入数据库结构：
   ```bash
   mysql -u root -p growth_monitor < database.sql
   ```
4. 修改`.env`文件中的数据库连接信息：
   ```
   DATABASE_URI=mysql+pymysql://root:password@localhost:3306/growth_monitor
   ```

### 3. 启动后端服务

```bash
# 方法1：直接运行脚本
start_backend.bat

# 方法2：手动执行
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 4. 启动前端服务

```bash
# 方法1：直接运行脚本
frontend\start_frontend.bat

# 方法2：手动执行
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

## 项目结构

```
Lighthouse of Growth/
├── ai/                  # AI模型模块
│   └── growth_analyzer.py  # 生长发育分析模型
├── frontend/            # 前端项目
│   ├── src/             # 前端源代码
│   │   ├── components/  # 组件
│   │   ├── pages/       # 页面
│   │   ├── styles/      # 样式
│   │   ├── App.jsx      # 应用入口
│   │   └── main.jsx     # 主文件
│   ├── package.json     # 前端依赖
│   └── vite.config.js   # Vite配置
├── models/              # 数据库模型
├── routes/              # API路由
├── .env                 # 环境变量
├── app.py               # 后端应用入口
├── database.sql         # 数据库结构
├── requirements.txt     # 后端依赖
└── start_backend.bat    # 后端启动脚本
```

## 使用指南

### 1. 注册登录

- 访问 `http://localhost:3000/register` 注册新账号
- 访问 `http://localhost:3000/login` 登录系统

### 2. 添加儿童信息

- 登录后，点击左侧菜单的「儿童管理」
- 点击「添加儿童」按钮，填写儿童基本信息

### 3. 录入生长数据

- 在「儿童管理」页面，点击对应儿童的「生长数据」按钮
- 点击「添加数据」按钮，录入测量日期、身高、体重等数据
- 系统会自动计算BMI并生成生长趋势图表

### 4. 风险评估

- 在「儿童管理」页面，点击对应儿童的「风险评估」按钮
- 点击「开始评估」按钮，系统会基于AI模型进行风险评估
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

这个是我要做的项目，接下来我让你做怎么就怎么做怎么，不要乱创建新文件和文件夹，只在已有的项目结构中操作。

用这个激活命令-# 激活虚拟环境
.\venv\Scripts\Activate.ps1

