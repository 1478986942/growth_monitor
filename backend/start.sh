#!/bin/bash

# 加载环境变量
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 初始化数据库
python init_db.py

# 启动应用
exec gunicorn app:app
