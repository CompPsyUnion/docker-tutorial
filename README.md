# docker-tutorial

Docker本体部分

## Flask应用实战

首先，我们创建一个简单的Flask应用，用于演示Docker的使用。

先移动到practise目录下

```bash
cd practise
```

### 事先说明，所有的源码在src文件夹下都是存在的，这里只是展示了app.py文件的内容，便于你们一步步走来感受自己手搓的快乐（狗头）

创建一个名为`app.py`的文件，内容如下：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Python的相关内容我就不进行具体的讲解了，因为本次周常的中心是Docker，而不是Python。

你们可以自行去查阅相关内容。

### Dockerfile

为了让Docker知道要构建一个怎么样的镜像，我们需要在项目内编写Dockerfile文件（无后缀）

Dockerfile必须和app.py文件在同一级目录下

```dockerfile
#1. basic information
FROM python:3.10-slim

#2. set workspace
WORKDIR /app

#3. install dependencies
RUN pip install flask

#4. copy app.py to /app dir in the container
COPY app.py /app/

#5. set environment variables
ENV PYTHONUNBUFFERED=1  
#let python print log immediately

#6. define the command to run in default when container starts
CMD ["python", "app.py"]

```

针对上面这段代码：

- `FROM`: 说明基本的项目所需环境（如Python版本或C++版本）

- `WORKDIR`: 说明项目在容器中的工作空间的根目录

- `RUN`: 执行命令，这里用于安装Flask依赖

- `COPY`: 将当前文件夹（和Dockerfile同一级）的文件复制到指定的容器内位置

- `ENV`: 添加环境变量

- `CMD`: 定义当容器启动的时候默认运行的指令

有了这段Dockerfile，Docker就知道对应的镜像应该是怎么样的，进而构建出你想要的镜像。

### 镜像基本操作

#### 创建

那么我们要如何创建镜像呢？

我们可以通过运行以下命令来进行镜像的创建：

`一定要在Dockerfile所在目录下运行`

```bash
docker build -t my-flask-app:v1 .
```

其中：

- `-t`说明这个镜像的名称，一般格式为：`名称：版本`

#### 查看

如果想要查看目前已存在多少镜像，可以运行以下指令：

```bash
docker images
```

终端就会返回所有的镜像信息

#### 打包

将镜像打包为tar文件（用于跨设备物理传输）：

你可以理解为zip压缩文件，只是它的后缀名是.tar

```bash
docker save -o my-flask-app-v1.tar my-flask-app:v1
```

其中 `-o` 是输出的意思，后面接你要输出的tar文件名，然后接你要打包的镜像名

这样就会产生对应的tar文件

#### 导入tar包

你可以通过以下命令将tar文件导入到docker中：

```bash
docker load -i my-flask-app-v1.tar
```

docker会将tar文件中的镜像导入到本地，你可以通过 `docker images` 来查看是否成功导入

#### 删除

你可以通过以下命令来删除镜像：

```bash
docker rmi -f my-flask-app:v1
```

其中 `-f` 是强制删除的意思,正常情况下无需添加 -f（因为docker会提示你是否确认删除）

---

还有一种方法来清除无用镜像：

```bash
docker image prune -a # -a :清除所有未使用的镜像
```

---

操作完了镜像，那自然而然就要操作容器了。

---

### 容器基本操作

和容器相关的命令如下：

#### 创建容器

```bash
docker run -d --name my-flask-container -p 8080:5000 my-flask-app:v1
```

关于上述命令，有以下需要进行讲解的点（或者你们自己查也可以）：

- `-d`: 后台运行，不实时展示模拟终端

- `--name`: 自定义容器名（随便你写）

- `-p`: 端口映射（如果打包的项目不涉及flask等网络内容则不需要）

这个命令的作用是将容器内的5000端口映射到主机的8080端口，这样我们就可以通过主机的8080端口来访问容器内的5000端口了。

#### 查看容器状态

```bash
docker ps #查看运行中的容器

docker ps -a #查看所有的容器
```

#### 启动容器

```bash
docker start container_name
```

start后面接你自己定义的容器名即可

#### 运行内部程序

```bash
# 进入容器内部交互式终端
docker exec -it container_name /bin/bash

# 在容器内执行单个命令
docker exec container_name ls -la
```

你可以替换 ls -la 为你想要执行的命令，例如：

```bash
docker exec container_name python -m flask run
```

都是可行的。

---

作为一个程序员，怎么能够不看日志呢？(*^_^*)

#### 查看容器日志

```bash
docker logs container_name

# 实时查看日志
docker logs -f container_name
```

#### 关闭容器

关闭容器有两种方式：

1.优雅停止（推荐）：

```bash
docker stop container_name
```

2.暴力停止（迫不得已）：

```bash
docker kill container_name
```

#### 重启容器

```bash
docker restart container_name
```

#### 删除容器

和镜像一样，容器也有两种方式来删除：

```bash
docker rm -f my-flask-container #强制删除指定容器

docker container prune #清理所有停止运行的容器
```

其中 -f 是强制删除的意思，如果想要温和一些的方式，将 -f 去除即可。

---

#### 数据卷操作

数据卷是Docker中用于持久化数据的机制，可以在容器之间共享数据，也可以在主机和容器之间共享数据。

```bash
# 创建数据卷
docker volume create my-volume

# 查看数据卷
docker volume ls

# 查看数据卷详情
docker volume inspect my-volume

# 在运行容器时挂载数据卷
docker run -d --name my-container -v my-volume:/app/data my-image

# 挂载主机目录到容器
docker run -d --name my-container -v /host/path:/container/path my-image

# 删除数据卷
docker volume rm my-volume

# 清理未使用的数据卷
docker volume prune
```

在这里，`-v`的作用是说明容器内的目录和主机内的目录的映射关系，例如：

```bash
docker run -d --name my-container -v /host/path:/container/path my-image
```

就说明容器内的`/container/path`目录和主机内的`/host/path`目录是映射关系，容器内的文件变化会同步到主机内，主机内的文件变化也会同步到容器内。

---

我之前提到过，容器是被隔离的进程。

那我们写的可是有网络请求的，没有网络我们的程序该怎么活啊（悲）

还好Docker早就考虑到了这一点，所以Docker提供了多种网络模式，用于容器之间的通信。

---

## Docker网络

Docker提供了多种网络模式，用于容器之间的通信：

- **bridge模式**：默认网络模式，容器通过虚拟网络桥接与主机通信
- **host模式**：容器直接使用主机网络，性能最好但隔离性差
- **none模式**：容器没有网络连接
- **overlay模式**：用于多主机 Docker 集群

```bash
# 创建网络
docker network create my-network

# 查看网络
docker network ls

# 运行容器时指定网络
docker run -d --name my-container --network my-network my-image

# 连接容器到网络
docker network connect my-network my-container

# 断开容器与网络的连接
docker network disconnect my-network my-container

# 删除网络
docker network rm my-network
```

`注意`：在使用过端口映射后，容器会自动使用bridge网络模式。

因此大部分情况下无需特别进行配置，除非你需要让容器之间进行通信。

~`反正我们这次周常不用（^_^）`~
---

---

最后的最后，我们现在已经学会了一些Docker的基本操作。

# 但是

你有没有想过一个问题：

以 `docker run` 为例：

每次我要创建容器时，我都要深吸一口气，然后直接一套：

```bash
docker run -d --name my-container -p 8080:5000 my-image
```

累死累活的打完吗？

传说中最擅长偷懒的程序员难道会甘愿忍受这样的屈辱吗！！！（╯‵□′）╯︵┻━┻

具体的解决方案，就请大家期待本次周常的下半部分内容：

# Docker compose
