# 高可用部署指南 / High Availability Deployment Guide

本文档介绍如何在各种环境中部署 AI 导航助手的高可用架构。

This document describes how to deploy the AI Navigation Assistant with high availability in various environments.

## 目录 / Table of Contents

- [架构概览](#架构概览)
- [Docker 部署](#docker-部署)
- [Docker Compose 部署](#docker-compose-部署)
- [Kubernetes 部署](#kubernetes-部署)
- [物理机/虚拟机部署](#物理机虚拟机部署)
- [监控和维护](#监控和维护)

## 架构概览

### 高可用特性 / HA Features

✅ **无单点故障** - 多副本部署，任一实例失败不影响服务  
✅ **负载均衡** - 自动分发请求到健康的实例  
✅ **自动恢复** - 失败实例自动重启  
✅ **滚动更新** - 零停机更新  
✅ **健康检查** - 主动监控实例健康状态  
✅ **水平扩展** - 根据负载自动扩缩容（K8S HPA）  
✅ **资源隔离** - 容器化保证环境一致性  

### 架构图

```
┌─────────────────────────────────────────┐
│          Load Balancer / Ingress         │
│        (Nginx / K8S Service)             │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│ Pod 1 │  │ Pod 2 │  │ Pod 3 │
│FastAPI│  │FastAPI│  │FastAPI│
└───────┘  └───────┘  └───────┘
```

## Docker 部署

### 1. 构建镜像

```bash
docker build -t ai-navigator:latest .
```

### 2. 运行单个容器（测试）

```bash
docker run -d \
  --name ai-navigator \
  -p 8000:8000 \
  --restart unless-stopped \
  ai-navigator:latest
```

### 3. 验证健康状态

```bash
curl http://localhost:8000/health
```

## Docker Compose 部署

Docker Compose 提供了简单的多实例部署方案，适合开发和小规模生产环境。

### 特性

- 3个应用实例 + 1个 Nginx 负载均衡器
- 自动健康检查和重启
- 资源限制（CPU/内存）
- 轮询负载均衡

### 1. 启动服务

```bash
docker-compose up -d
```

### 2. 查看服务状态

```bash
docker-compose ps
docker-compose logs -f
```

### 3. 扩展实例数量

```bash
docker-compose up -d --scale ai-navigator=5
```

### 4. 访问服务

- **负载均衡入口**: http://localhost
- **直接访问实例1**: http://localhost:8000
- **直接访问实例2**: http://localhost:8001
- **直接访问实例3**: http://localhost:8002

### 5. 停止服务

```bash
docker-compose down
```

### Nginx 负载均衡配置

`nginx.conf` 配置了：
- **Least Connection** 算法：将请求发送到连接数最少的后端
- **故障转移**：自动跳过失败的后端（3次失败后30秒内不再路由）
- **健康检查**：定期检查 `/health` 端点

## Kubernetes 部署

Kubernetes 提供了企业级的高可用部署方案，支持自动扩缩容、滚动更新等高级特性。

### 前置要求

- Kubernetes 集群（版本 >= 1.20）
- kubectl 命令行工具
- （可选）Ingress Controller（如 nginx-ingress）

### 部署清单说明

| 文件 | 用途 |
|------|------|
| `deployment.yaml` | 应用部署配置（3副本，滚动更新） |
| `service.yaml` | 服务暴露（ClusterIP + LoadBalancer） |
| `ingress.yaml` | Ingress 路由配置 |
| `hpa.yaml` | 水平自动扩缩容（3-10副本） |
| `configmap.yaml` | 配置管理 |
| `kustomization.yaml` | Kustomize 部署配置 |

### 1. 快速部署（使用 kubectl）

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

### 2. 使用 Kustomize 部署

```bash
kubectl apply -k k8s/
```

### 3. 查看部署状态

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa
kubectl get ingress
```

### 4. 查看日志

```bash
kubectl logs -l app=ai-navigator -f
kubectl logs -l app=ai-navigator --tail=100
```

### 5. 访问服务

#### 方式1: 通过 LoadBalancer

```bash
# 获取 LoadBalancer 外部 IP
kubectl get svc ai-navigator-loadbalancer

# 访问服务
curl http://<EXTERNAL-IP>/health
```

#### 方式2: 通过 Ingress

```bash
# 添加 hosts 记录
echo "127.0.0.1 ai-navigator.local" | sudo tee -a /etc/hosts

# 访问服务
curl http://ai-navigator.local/health
```

#### 方式3: 端口转发（测试）

```bash
kubectl port-forward svc/ai-navigator-service 8000:80
curl http://localhost:8000/health
```

### 6. 更新应用

```bash
# 构建新镜像
docker build -t ai-navigator:v2 .

# 更新镜像
kubectl set image deployment/ai-navigator ai-navigator=ai-navigator:v2

# 查看滚动更新状态
kubectl rollout status deployment/ai-navigator

# 回滚（如需要）
kubectl rollout undo deployment/ai-navigator
```

### 7. 扩缩容

#### 手动扩缩容

```bash
kubectl scale deployment ai-navigator --replicas=5
```

#### 自动扩缩容 (HPA)

HPA 已配置为根据 CPU 和内存使用率自动扩缩容：
- **最小副本数**: 3
- **最大副本数**: 10
- **CPU 目标**: 70%
- **内存目标**: 80%

```bash
kubectl get hpa ai-navigator-hpa
kubectl describe hpa ai-navigator-hpa
```

### 8. 删除部署

```bash
kubectl delete -k k8s/
# 或
kubectl delete -f k8s/
```

### Kubernetes 高可用特性

#### 1. Pod 反亲和性
`deployment.yaml` 配置了 Pod 反亲和性，尽量将副本调度到不同的节点，避免单节点故障影响所有副本。

#### 2. 健康检查
- **Liveness Probe**: 检测容器是否存活，失败则重启
- **Readiness Probe**: 检测容器是否就绪，未就绪则从 Service 中移除
- **Startup Probe**: 检测容器启动是否成功

#### 3. 滚动更新
- **maxSurge**: 1 - 更新时最多额外创建1个 Pod
- **maxUnavailable**: 1 - 更新时最多1个 Pod 不可用
- 保证更新过程中服务不中断

#### 4. 资源限制
每个 Pod 设置了资源请求和限制：
- **请求**: CPU 250m, 内存 256Mi
- **限制**: CPU 500m, 内存 512Mi

## 物理机/虚拟机部署

对于物理机或虚拟机环境，推荐使用 Systemd + Nginx 的方案。

### 架构

```
┌─────────────────┐
│  Nginx (Port 80)│
└────────┬────────┘
         │
    ┌────┼─────┬─────┐
    │    │     │     │
┌───▼┐ ┌─▼──┐┌─▼──┐┌─▼──┐
│8000│ │8001││8002││8003│
│App1│ │App2││App3││App4│
└────┘ └────┘└────┘└────┘
```

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip nginx

# CentOS/RHEL
sudo yum install python3.11 python3-pip nginx
```

### 2. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /opt/ai-navigator
sudo cp -r . /opt/ai-navigator/

# 安装 Python 依赖
cd /opt/ai-navigator
pip3 install -r requirements.txt
```

### 3. 创建 Systemd 服务文件

创建 `/etc/systemd/system/ai-navigator@.service`:

```ini
[Unit]
Description=AI Navigator Instance %i
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ai-navigator
Environment="PYTHONUNBUFFERED=1"
Environment="PORT=%i"
ExecStart=/usr/bin/python3 -m uvicorn src.ai_navigator_api:app --host 0.0.0.0 --port %i --workers 2
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

### 4. 启动多个实例

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-navigator@8000
sudo systemctl enable ai-navigator@8001
sudo systemctl enable ai-navigator@8002
sudo systemctl enable ai-navigator@8003

sudo systemctl start ai-navigator@8000
sudo systemctl start ai-navigator@8001
sudo systemctl start ai-navigator@8002
sudo systemctl start ai-navigator@8003
```

### 5. 配置 Nginx 负载均衡

编辑 `/etc/nginx/sites-available/ai-navigator`:

```nginx
upstream ai_navigator_backend {
    least_conn;
    server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8003 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name ai-navigator.example.com;

    location / {
        proxy_pass http://ai_navigator_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }

    location /health {
        proxy_pass http://ai_navigator_backend/health;
        access_log off;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/ai-navigator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. 验证部署

```bash
# 检查服务状态
sudo systemctl status ai-navigator@8000
sudo systemctl status ai-navigator@8001
sudo systemctl status ai-navigator@8002
sudo systemctl status ai-navigator@8003

# 检查健康状态
curl http://localhost/health

# 查看日志
sudo journalctl -u ai-navigator@8000 -f
```

## 监控和维护

### 健康检查端点

```bash
curl http://your-server/health
```

响应示例：
```json
{
  "status": "healthy",
  "service": "AI Navigation Assistant"
}
```

### Docker 环境监控

```bash
# 查看容器状态
docker ps
docker-compose ps

# 查看资源使用
docker stats

# 查看日志
docker logs ai-navigator -f
docker-compose logs -f
```

### Kubernetes 监控

```bash
# 查看 Pod 状态
kubectl get pods -l app=ai-navigator

# 查看资源使用
kubectl top pods -l app=ai-navigator

# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 查看 HPA 状态
kubectl get hpa
```

### 物理机/虚拟机监控

```bash
# 查看服务状态
sudo systemctl status ai-navigator@*

# 查看日志
sudo journalctl -u ai-navigator@8000 -f

# 查看进程
ps aux | grep uvicorn
```

## 性能调优建议

### 1. Worker 进程数

根据 CPU 核心数调整 worker 数量：

```bash
# Dockerfile
CMD ["uvicorn", "src.ai_navigator_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# 推荐: workers = (CPU 核心数 × 2) + 1
```

### 2. 资源限制

K8S 环境根据实际负载调整资源限制：

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### 3. HPA 阈值

根据实际性能调整自动扩缩容阈值：

```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70  # 调整此值
```

## 故障排查

### 问题1: Pod 启动失败

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### 问题2: 健康检查失败

```bash
# 手动测试健康检查
kubectl exec -it <pod-name> -- curl http://localhost:8000/health

# 查看探针配置
kubectl describe pod <pod-name> | grep -A 10 Liveness
```

### 问题3: 负载不均衡

```bash
# 检查 Service endpoints
kubectl get endpoints ai-navigator-service

# 查看 Nginx 日志
kubectl logs <nginx-pod>
```

## 安全建议

1. **使用非 root 用户运行**（Dockerfile 已配置）
2. **启用 HTTPS**（生产环境使用 TLS 证书）
3. **限制资源访问**（使用 K8S NetworkPolicy）
4. **定期更新镜像**（修补安全漏洞）
5. **配置防火墙规则**（仅开放必要端口）

## 总结

本指南覆盖了 AI 导航助手在以下环境的高可用部署：

- ✅ **Docker**: 单容器部署
- ✅ **Docker Compose**: 多容器 + 负载均衡
- ✅ **Kubernetes**: 企业级编排和自动化
- ✅ **物理机/虚拟机**: Systemd + Nginx

选择合适的部署方案：
- **开发/测试**: Docker 单容器
- **小规模生产**: Docker Compose
- **大规模生产**: Kubernetes
- **传统环境**: 物理机/虚拟机 + Systemd

所有方案均支持：
- 无单点故障
- 自动故障恢复
- 负载均衡
- 健康检查
- 资源隔离
