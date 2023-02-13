################################################
#               This Dockerfile                #
################################################

# 指定基础镜像
#   FROM <image>
#   FROM <image>:<tag>
FROM python:3.8

# 指定工作目录
#   WORKDIR <path>
WORKDIR /projects

# 添加本地文件（相对路径或网络资源）到容器
#   ADD <src> <dest>

# 复制本地文件（相对路径）到容器
#   COPY <src> <dest>
COPY ./ CodeSearchBackEnd/

# 指定工作目录
#   WORKDIR <path>
WORKDIR /projects/CodeSearchBackEnd

# 执行指令
#   RUN <command>
RUN pip install -r requirements.txt

RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf.py", "app.main:app" ]
# ENTRYPOINT [ "uvicorn","--host","0.0.0.0","--port","8000","app.main:app" ]