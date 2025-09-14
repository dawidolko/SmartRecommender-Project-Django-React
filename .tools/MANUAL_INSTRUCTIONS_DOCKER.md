# SmartRecommender – Docker Setup Guide

This guide explains how to set up and run the **SmartRecommender** project using **Docker** on Windows, macOS, and Linux.

---

## 1. Prerequisites

Before running the project, make sure you have:

- **Hardware support for virtualization**

  - **Intel**: Enable **Intel VT-x** in BIOS/UEFI.
  - **AMD**: Enable **AMD-V / SVM Mode** in BIOS/UEFI.
  - **Apple Silicon (M1/M2/M3)**: Virtualization is supported natively, no BIOS changes required.

👉 To check if virtualization is enabled:

- **Windows**: Open **Task Manager → Performance → CPU** (look for “Virtualization: Enabled”).
- **Linux/macOS**: Run:

  ```bash
  sysctl -a | grep -E --color 'machdep.cpu.features|vmx|svm'
  ```

---

## 2. Install Docker Desktop

### Windows

1. Download **Docker Desktop for Windows**: [https://docs.docker.com/desktop/install/windows/](https://docs.docker.com/desktop/install/windows/)
2. Install it like a regular application.
3. Enable **WSL 2 backend** during installation (recommended).
4. After installation, restart your PC.
5. Verify installation:

   ```powershell
   docker --version
   docker compose version
   ```

### macOS

1. Download **Docker Desktop for Mac**: [https://docs.docker.com/desktop/install/mac/](https://docs.docker.com/desktop/install/mac/)

   - Choose **Intel chip** or **Apple Silicon (M1/M2/M3)** depending on your CPU.

2. Install by dragging Docker to **Applications**.
3. Start Docker Desktop.
4. Verify installation:

   ```bash
   docker --version
   docker compose version
   ```

### Linux (Ubuntu/Debian example)

1. Remove old versions (if any):

   ```bash
   sudo apt-get remove docker docker-engine docker.io containerd runc
   ```

2. Install dependencies:

   ```bash
   sudo apt-get update
   sudo apt-get install -y ca-certificates curl gnupg lsb-release
   ```

3. Add Docker’s official GPG key:

   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

4. Add repository:

   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. Install Docker and Compose:

   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

6. Verify installation:

   ```bash
   docker --version
   docker compose version
   ```

---

## 3. Project Setup

### Clone the repository

```bash
git clone https://github.com/dawidolko/SmartRecommender-Project-Django-React
cd SmartRecommender-Project-Django-React
```

### Environment variables

Make sure you have a `.env` file with database settings:

```
DB_NAME=product_recommendation
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-default-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 4. Run the Project with Docker

### Build and start containers

```bash
docker compose -f .tools/docker/docker-compose.yml up --build
```

- **Backend (Django)** → [http://localhost:8000](http://localhost:8000)
- **Frontend (React)** → [http://localhost:3000](http://localhost:3000)
- **Database (PostgreSQL)** → on port `5432`

### Stop containers

```bash
docker compose -f .tools/docker/docker-compose.yml down
```

### Run in background

```bash
docker compose -f .tools/docker/docker-compose.yml up -d --build
```

### Check logs

```bash
docker compose -f .tools/docker/docker-compose.yml logs -f
```

---

## 5. Useful Docker Commands

- List running containers:

  ```bash
  docker ps
  ```

- Enter backend container shell:

  ```bash
  docker exec -it SmartRecommender-Django bash
  ```

- Enter database (Postgres) shell:

  ```bash
  docker exec -it SmartRecommender-PostgreSQL psql -U postgres -d product_recommendation
  ```

- Restart services:

  ```bash
  docker compose -f .tools/docker/docker-compose.yml restart
  ```

---

## 6. Troubleshooting

- **Docker Desktop not starting**: Check if virtualization is enabled in BIOS/UEFI.
- **Port conflicts**: Make sure ports `3000`, `8000`, and `5432` are not in use.
- **Permission errors on Linux**: Add your user to the `docker` group:

  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

- **Apple M1/M2 build issues**: Use `platform: linux/amd64` in your services if some images don’t support ARM.

---

✅ You’re ready! The project should now be accessible at:

- React frontend → **[http://localhost:3000](http://localhost:3000)**
- Django backend → **[http://localhost:8000](http://localhost:8000)**
