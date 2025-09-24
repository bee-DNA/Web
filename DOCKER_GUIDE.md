# 🐳 Docker 部署指南

## 📋 前置需求

### 安裝 Docker

- **Windows**: 下載並安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **macOS**: 下載並安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**:
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### 驗證安裝

```bash
docker --version
docker-compose --version
```

## 🚀 快速開始

### 方法 1：使用自動化腳本

#### Windows

```cmd
deploy.bat
```

#### Linux/macOS

```bash
chmod +x deploy.sh
./deploy.sh
```

### 方法 2：手動執行

#### 基本版應用程式

```bash
# 建立並啟動容器
docker-compose up --build world-map-app

# 在背景執行
docker-compose up -d --build world-map-app
```

#### 進階版應用程式

```bash
# 建立並啟動容器
docker-compose --profile advanced up --build advanced-world-map-app

# 在背景執行
docker-compose --profile advanced up -d --build advanced-world-map-app
```

#### 同時執行兩個版本

```bash
# 建立並啟動所有容器
docker-compose --profile advanced up --build

# 在背景執行
docker-compose --profile advanced up -d --build
```

## 🌐 存取應用程式

啟動完成後，在瀏覽器中開啟：

- **基本版**: http://localhost:8050
- **進階版**: http://localhost:8051

## 🛠️ 管理指令

### 檢視運行中的容器

```bash
docker ps
```

### 檢視日誌

```bash
# 檢視特定容器日誌
docker-compose logs world-map-app
docker-compose logs advanced-world-map-app

# 即時跟蹤日誌
docker-compose logs -f world-map-app
```

### 停止服務

```bash
# 停止所有服務
docker-compose down

# 停止特定服務
docker-compose stop world-map-app
```

### 重新建立映像

```bash
# 強制重新建立映像
docker-compose build --no-cache

# 重新建立並啟動
docker-compose up --build --force-recreate
```

### 清理資源

```bash
# 移除停止的容器
docker container prune

# 移除未使用的映像
docker image prune

# 移除所有未使用的資源
docker system prune
```

## 🔧 環境變數配置

可以建立 `.env` 檔案來自訂設定：

```env
# .env 檔案
DASH_DEBUG=False
FLASK_ENV=production
PORT_BASIC=8050
PORT_ADVANCED=8051
```

## 📊 資料掛載

應用程式支援外部資料掛載：

```yaml
# 在 docker-compose.yml 中
volumes:
  - ./data:/app/data:ro # 將本地 data 目錄掛載為唯讀
```

將您的 CSV 資料檔案放在 `./data` 目錄中，應用程式即可讀取。

## 🐛 故障排除

### 端口衝突

如果端口被佔用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:8050" # 將本地端口改為 8080
```

### 記憶體不足

為容器增加記憶體限制：

```yaml
deploy:
  resources:
    limits:
      memory: 1G
    reservations:
      memory: 512M
```

### 容器無法啟動

1. 檢查日誌：`docker-compose logs [服務名]`
2. 確認 Docker 有足夠權限
3. 檢查防火牆設定

## 🎯 生產環境部署

### 使用 Docker Swarm

```bash
# 初始化 Swarm
docker swarm init

# 部署堆疊
docker stack deploy -c docker-compose.yml world-map-stack
```

### 使用 Kubernetes

將 Docker Compose 轉換為 Kubernetes 配置：

```bash
# 安裝 kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.28.0/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose

# 轉換配置
kompose convert -f docker-compose.yml
```

## 🔐 安全考量

### 生產環境建議

1. 使用非 root 使用者執行容器
2. 設定適當的資源限制
3. 定期更新基礎映像
4. 使用秘密管理系統存放敏感資訊

### 網路安全

```yaml
# 自訂網路配置
networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 📈 效能優化

### 映像大小優化

- 使用多階段建立
- 清理不必要的套件
- 使用 `.dockerignore`

### 啟動時間優化

- 預先建立映像
- 使用映像快取
- 優化 Python 匯入

## 🤝 開發工作流程

### 開發模式

```bash
# 使用開發模式啟動（啟用熱重載）
docker-compose -f docker-compose.dev.yml up
```

### 測試

```bash
# 執行測試
docker-compose exec world-map-app python -m pytest
```

---

🎉 **恭喜！您現在可以使用 Docker 輕鬆部署和管理您的世界地圖專案了！**
