# Docker部署指南

## 本地Docker部署

### 1. 安装Docker和Docker Compose

确保您的系统已安装Docker和Docker Compose：
- Windows: 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Mac: 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: 按照官方文档安装

### 2. 启动服务

在项目根目录下执行：

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（会删除数据库数据）
docker-compose down -v
```

### 4. 访问服务

- 后端API: http://localhost:5555
- 健康检查: http://localhost:5555/health

## 云平台Docker部署

### 部署到Render

1. **修改docker-compose.yml**（Render使用单个容器）
   - Render不支持docker-compose，需要单独部署后端容器
   - 使用Render的MySQL数据库服务

2. **在Render上创建MySQL数据库**
   - 登录Render控制台
   - 创建新的MySQL数据库
   - 获取数据库连接信息

3. **在Render上部署后端服务**
   - 创建新的Web Service
   - 选择"Dockerfile"作为运行环境
   - 配置环境变量：
     ```
     DATABASE_URI=mysql+pymysql://username:password@host:3306/database_name
     JWT_SECRET_KEY=your-secret-key
     MAIL_SERVER=smtp.qq.com
     MAIL_PORT=465
     MAIL_USE_TLS=False
     MAIL_USE_SSL=True
     MAIL_USERNAME=your-email@qq.com
     MAIL_PASSWORD=your-authorization-code
     MAIL_DEFAULT_SENDER=your-email@qq.com
     PORT=5555
     ```

4. **部署**
   - Render会自动从Dockerfile构建镜像
   - 部署完成后，获得访问URL

### 部署到Heroku

1. **安装Heroku CLI**
   ```bash
   # Windows
   # 下载并安装 Heroku CLI

   # Mac
   brew tap heroku/brew && brew install heroku

   # Linux
   snap install heroku --classic
   ```

2. **登录Heroku**
   ```bash
   heroku login
   ```

3. **创建应用**
   ```bash
   heroku create growth-monitor-backend
   ```

4. **添加MySQL插件**
   ```bash
   heroku addons:create cleardb:ignite
   ```

5. **配置环境变量**
   ```bash
   heroku config:set DATABASE_URI=mysql+pymysql://username:password@host:3306/database_name
   heroku config:set JWT_SECRET_KEY=your-secret-key
   heroku config:set MAIL_SERVER=smtp.qq.com
   heroku config:set MAIL_PORT=465
   heroku config:set MAIL_USE_TLS=False
   heroku config:set MAIL_USE_SSL=True
   heroku config:set MAIL_USERNAME=your-email@qq.com
   heroku config:set MAIL_PASSWORD=your-authorization-code
   heroku config:set MAIL_DEFAULT_SENDER=your-email@qq.com
   heroku config:set PORT=5555
   ```

6. **部署**
   ```bash
   heroku container:login
   heroku container:push web -a growth-monitor-backend
   heroku container:release web -a growth-monitor-backend
   ```

### 部署到阿里云/腾讯云

1. **购买云服务器**
   - 选择合适的配置（2核4G推荐）
   - 安装Docker和Docker Compose

2. **上传项目文件**
   ```bash
   scp -r "Lighthouse of Growth1" user@your-server-ip:/home/user/
   ```

3. **启动服务**
   ```bash
   ssh user@your-server-ip
   cd "Lighthouse of Growth1"
   docker-compose up -d
   ```

4. **配置Nginx反向代理**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5555;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **配置HTTPS**
   ```bash
   # 使用Let's Encrypt免费证书
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Docker镜像管理

### 构建镜像

```bash
# 构建后端镜像
docker build -t growth-monitor-backend .

# 构建并启动所有服务
docker-compose build
```

### 推送镜像到Docker Hub

```bash
# 登录Docker Hub
docker login

# 标记镜像
docker tag growth-monitor-backend your-username/growth-monitor-backend:latest

# 推送镜像
docker push your-username/growth-monitor-backend:latest
```

### 从Docker Hub拉取镜像

```bash
# 拉取镜像
docker pull your-username/growth-monitor-backend:latest

# 运行容器
docker run -d -p 5555:5555 \
  -e DATABASE_URI=mysql+pymysql://user:pass@host:3306/db \
  -e JWT_SECRET_KEY=your-secret-key \
  your-username/growth-monitor-backend:latest
```

## 故障排查

### 查看容器日志

```bash
# 查看所有容器日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs db

# 实时查看日志
docker-compose logs -f backend
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec db mysql -u root -p
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 清理资源

```bash
# 停止并删除所有容器
docker-compose down

# 删除所有未使用的镜像
docker image prune -a

# 删除所有未使用的卷
docker volume prune
```

## 性能优化

### 1. 使用多阶段构建优化镜像大小

```dockerfile
FROM python:3.9-slim as builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY backend/ .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5555", "app:app"]
```

### 2. 使用缓存加速构建

```dockerfile
FROM python:3.9-slim
WORKDIR /app

# 先复制依赖文件，利用缓存
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制应用代码
COPY backend/ .
```

### 3. 配置健康检查

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5555/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 安全建议

1. **不要在代码中硬编码敏感信息**
   - 使用环境变量存储密码和密钥
   - 使用Docker secrets管理敏感数据

2. **定期更新基础镜像**
   ```dockerfile
   FROM python:3.9-slim
   ```

3. **限制容器权限**
   - 不要使用root用户运行应用
   - 使用只读文件系统

4. **扫描镜像漏洞**
   ```bash
   docker scan growth-monitor-backend
   ```

## 监控和日志

### 使用Docker日志驱动

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 集成监控工具

- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog
- New Relic

## 备份和恢复

### 数据库备份

```bash
# 备份数据库
docker-compose exec db mysqldump -u root -proot growth_monitor1 > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -u root -proot growth_monitor1 < backup.sql
```

### 数据卷备份

```bash
# 备份数据卷
docker run --rm -v mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_data.tar.gz -C /data .

# 恢复数据卷
docker run --rm -v mysql_data:/data -v $(pwd):/backup alpine tar xzf /backup/mysql_data.tar.gz -C /data
```

## 常见问题

### Q: 容器启动失败怎么办？
A: 查看日志 `docker-compose logs`，检查配置是否正确。

### Q: 如何修改环境变量？
A: 修改docker-compose.yml文件，然后执行 `docker-compose up -d`。

### Q: 数据库连接失败？
A: 检查数据库容器是否正常运行，确认DATABASE_URI配置正确。

### Q: 如何升级应用？
A: 修改代码后，执行 `docker-compose up -d --build`。

## 联系支持

如有问题，请查看：
- Docker官方文档: https://docs.docker.com/
- Docker Compose文档: https://docs.docker.com/compose/
- 项目GitHub仓库