# 🚀 Railway Deployment - Quick Start

## 5-Minute Setup

### 1️⃣ Create GitHub Repository (2 min)

1. Go to https://github.com/new
2. Name: `paddleocr-server`
3. Set to **Public**
4. Click **Create repository**

### 2️⃣ Push Code to GitHub (1 min)

Open Command Prompt in `LocalOCRServer` folder:

```bash
git init
git add .
git commit -m "Deploy PaddleOCR to Railway"
git remote add origin https://github.com/YOUR_USERNAME/paddleocr-server.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3️⃣ Deploy to Railway (2 min)

1. Go to https://railway.app/
2. Sign up with GitHub (free)
3. Click **New Project**
4. Click **Deploy from GitHub repo**
5. Select `paddleocr-server`
6. Wait for deployment (~3 minutes)

### 4️⃣ Get Your URL

1. Click **Settings** tab
2. Scroll to **Networking**
3. Click **Generate Domain**
4. Copy the URL (e.g., `https://paddleocr-server-production-xxxx.up.railway.app`)

### 5️⃣ Test It

Open in browser:
```
https://your-railway-url.up.railway.app/health
```

Should show:
```json
{"status": "healthy", "service": "PaddleOCR Server", "version": "1.0.0"}
```

### 6️⃣ Configure in App

1. Open your app
2. Go to **OCR Settings**
3. Select **Local Server (PaddleOCR)**
4. Enter: `https://your-railway-url.up.railway.app`
5. Click **Test**
6. Should show: ✅ **Connected!**

## ✅ Done!

Your PaddleOCR server is now:
- 🌐 Accessible from anywhere
- 🔄 Auto-updates when you push to GitHub
- 💰 Free for moderate usage ($5 credit/month)
- 📊 Monitored in Railway dashboard

## 💡 Tips

### Update Your Server:
```bash
# Make changes to code
git add .
git commit -m "Update"
git push
# Railway auto-deploys!
```

### View Logs:
Railway Dashboard → Your Project → Deployments → View Logs

### Check Usage:
Railway Dashboard → Usage tab

## 🆘 Troubleshooting

### "git: command not found"
Install Git: https://git-scm.com/downloads

### "Permission denied (publickey)"
Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/paddleocr-server.git
```

### "Application failed to respond"
Check Railway logs for errors. Common issues:
- Missing `Procfile`
- Wrong Python version
- Out of memory (upgrade to Railway Pro)

### "Connection failed in app"
- Make sure you're using the Railway URL, not `localhost:5000`
- Check if Railway deployment is running
- Test the `/health` endpoint in browser first

## 📚 Full Guide

For detailed instructions, see `DEPLOY-TO-RAILWAY.md`

## 🎉 Success!

You now have a cloud-hosted OCR server that works with Google Apps Script!

Enjoy your private, always-online OCR processing! 🚀
