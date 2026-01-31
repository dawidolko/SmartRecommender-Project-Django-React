# SmartRecommender Distribution Package

## 📦 About This Package

This is a **complete distribution package** of the SmartRecommender project, containing all necessary dependencies pre-installed and ready for deployment. This package eliminates the need for manual dependency installation, making deployment faster and more reliable.

## 🎯 What's Included

This archive contains:

- ✅ **Complete source code** of the SmartRecommender application
- ✅ **All Python dependencies** installed in `backend/venv/` or `backend/.venv/`
- ✅ **All Node.js dependencies** installed in `frontend/node_modules/`
- ✅ **Backend dependencies** installed in `backend/node_modules/` (if applicable)
- ✅ **Configuration files** ready for production
- ✅ **Media and static files** directories
- ✅ **Database setup scripts**

## 📋 System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.8 or higher (must be already installed on the target system)
- **Node.js**: 14.x or higher (must be already installed on the target system)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 2 GB free space
- **Database**: PostgreSQL 12+ or SQLite (for development)

## 🚀 Quick Start Guide

### Step 1: Extract the Archive

```bash
# Extract the archive to your desired location
unzip SmartRecommender-Project.zip -d /path/to/destination
cd /path/to/destination
```

### Step 2: Configure Environment Variables

#### Backend Configuration

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create or edit the `.env` file:

   ```bash
   # Windows
   copy .env.example .env

   # Linux/macOS
   cp .env.example .env
   ```

3. Configure your environment variables:
   ```env
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@localhost:5432/smartrecommender
   ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
   CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
   ```

#### Frontend Configuration

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Create or edit the `.env` file:
   ```bash
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_API_BASE_URL=http://localhost:8000/api
   ```

### Step 3: Database Setup

```bash
cd backend

# Windows
python manage.py migrate
python manage.py createsuperuser

# Linux/macOS
python3 manage.py migrate
python3 manage.py createsuperuser
```

### Step 4: Run the Application

#### Option A: Using Start Scripts (Recommended)

**Windows:**

```bash
# Terminal 1 - Backend
cd backend
start.bat

# Terminal 2 - Frontend
cd frontend
start.bat
```

**Linux/macOS:**

```bash
# Terminal 1 - Backend
cd backend
chmod +x start.sh
./start.sh

# Terminal 2 - Frontend
cd frontend
chmod +x start.sh
./start.sh
```

#### Option B: Manual Start

**Backend:**

```bash
cd backend

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Run server
python manage.py runserver
```

**Frontend:**

```bash
cd frontend
npm start
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🔧 Advanced Configuration

### Production Deployment

For production deployment, ensure you:

1. **Set DEBUG to False** in backend settings
2. **Configure proper SECRET_KEY**
3. **Set up PostgreSQL database** instead of SQLite
4. **Configure HTTPS** and SSL certificates
5. **Set ALLOWED_HOSTS** and CORS_ALLOWED_ORIGINS properly
6. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Using a Different Port

**Backend:**

```bash
python manage.py runserver 0.0.0.0:8080
```

**Frontend:**
Update `package.json` or use:

```bash
PORT=3001 npm start
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump smartrecommender > backup.sql

# SQLite backup (if using SQLite)
sqlite3 db.sqlite3 ".backup 'backup.db'"
```

## 📚 Project Structure

```
SmartRecommender-Project/
├── backend/                 # Django backend application
│   ├── venv/               # Python virtual environment (pre-installed)
│   ├── core/               # Core settings and configuration
│   ├── home/               # Main application logic
│   ├── media/              # User-uploaded media files
│   ├── static/             # Static files
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies list
│   └── start.bat/start.sh  # Quick start scripts
│
├── frontend/               # React frontend application
│   ├── node_modules/       # Node.js dependencies (pre-installed)
│   ├── public/             # Public assets
│   ├── src/                # React source code
│   ├── package.json        # Node.js dependencies list
│   └── start.bat/start.sh  # Quick start scripts
│
└── README.md              # This file
```

## 🛠️ Troubleshooting

### Common Issues

#### "Module not found" Error

If you encounter module errors despite dependencies being included:

```bash
# Reinstall Python dependencies
cd backend
pip install -r requirements.txt

# Reinstall Node.js dependencies
cd frontend
npm install
```

#### Port Already in Use

If port 8000 or 3000 is already in use:

```bash
# Find and kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Find and kill the process (Linux/macOS)
lsof -ti:8000 | xargs kill -9
```

#### Database Connection Error

Ensure your database is running and credentials in `.env` are correct:

```bash
# Check PostgreSQL status (Linux)
sudo systemctl status postgresql

# Check PostgreSQL status (macOS)
brew services list
```

#### Permission Denied (Linux/macOS)

```bash
chmod +x backend/start.sh
chmod +x frontend/start.sh
```

### Getting Help

If you encounter issues not covered here:

1. Check the main project README at the root directory
2. Review the Django and React documentation
3. Check logs in `backend/logs/` (if configured)
4. Contact the development team

## 📝 Important Notes

- **Virtual Environment**: The Python virtual environment is included. Do NOT delete the `venv/` or `.venv/` folder.
- **Node Modules**: The `node_modules/` directories are included. They may be large but are necessary.
- **Security**: Always change default SECRET_KEY and passwords before production deployment.
- **Updates**: This package contains dependencies at the time of creation. Regular updates may be needed for security patches.
- **Platform Compatibility**: If moving between different operating systems, you may need to reinstall platform-specific dependencies.

## 🔐 Security Considerations

Before deploying to production:

- [ ] Change all default passwords and secret keys
- [ ] Review and update `ALLOWED_HOSTS` setting
- [ ] Configure proper CORS settings
- [ ] Enable HTTPS/SSL
- [ ] Set `DEBUG=False`
- [ ] Configure proper logging
- [ ] Set up regular database backups
- [ ] Review security headers and middleware

## 📄 License

This project is distributed under the license specified in the LICENSE file at the root of the project.

## 🤝 Support

For technical support or questions about this distribution package, please refer to the main project documentation or contact the development team.

---

**Package Version**: 1.0.0  
**Created**: January 2026  
**Python Version**: 3.8+  
**Node.js Version**: 14.x+

**Note**: This is a complete, self-contained distribution package. All dependencies are pre-installed and ready to use. Simply extract, configure, and run!
