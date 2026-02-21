# FleetFlow Deployment Guide

## 🗄️ Database Setup (Supabase PostgreSQL)

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Wait for database provisioning
4. Go to Settings → Database
5. Copy connection string

### Step 2: Get Connection Details
```
Host: db.xxxxxxxxxxxxx.supabase.co
Database: postgres
Port: 5432
User: postgres
Password: [your-password]
```

### Step 3: Update .env File
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Local Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies
```bash
cd fleetflow
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
copy .env.example .env
# Edit .env with your database credentials
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@fleetflow.com
# Password: [your-password]
```

### 6. Load Sample Data
```bash
python manage.py shell < load_sample_data.py
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 🌐 Production Deployment (Railway/Render)

### Railway Deployment

1. **Install Railway CLI**
```bash
npm i -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize Project**
```bash
railway init
```

4. **Add PostgreSQL**
```bash
railway add postgresql
```

5. **Set Environment Variables**
```bash
railway variables set SECRET_KEY="your-production-secret"
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS="your-app.railway.app"
```

6. **Deploy**
```bash
railway up
```

### Render Deployment

1. Create new Web Service on Render
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn fleetflow.wsgi:application`
5. Add environment variables in Render dashboard
6. Add PostgreSQL database (Render provides free tier)
7. Deploy

## 📦 Production Checklist

- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Configure PostgreSQL (Supabase/Neon)
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up SSL certificate
- [ ] Configure backup strategy
- [ ] Set up monitoring

## 🔒 Security Recommendations

1. **Never commit .env file**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS only**
4. **Regular database backups**
5. **Update dependencies regularly**
6. **Monitor error logs**

## 📊 Database Backup

### Supabase Backup
```bash
# Automatic backups enabled by default
# Manual backup via Supabase dashboard
```

### Local Backup
```bash
python manage.py dumpdata > backup.json
```

### Restore
```bash
python manage.py loaddata backup.json
```

## 🧪 Testing Deployment

1. Login with test credentials
2. Create vehicle
3. Create driver
4. Create and dispatch trip
5. Complete trip
6. Add maintenance
7. View analytics
8. Export CSV/PDF

## 🐛 Troubleshooting

### Database Connection Error
- Check .env credentials
- Verify Supabase IP whitelist (allow all: 0.0.0.0/0)
- Test connection: `python manage.py dbshell`

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Migration Issues
```bash
python manage.py migrate --run-syncdb
```

### Port Already in Use
```bash
python manage.py runserver 8080
```

## 📞 Support

For issues, check:
- Django logs
- Database connection
- Environment variables
- Requirements installed

---

**Ready for Production** ✅
