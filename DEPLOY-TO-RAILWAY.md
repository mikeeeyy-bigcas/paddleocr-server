# Deploy PaddleOCR Server to Railway.app

## 🚀 Why Railway?

- ✅ **Free tier:** $5 credit/month (enough for moderate usage)
- ✅ **Easy deployment:** Connect GitHub and deploy automatically
- ✅ **Public URL:** Accessible from Google Apps Script
- ✅ **Always online:** No need to keep your computer running
- ✅ **Fast:** Good performance for OCR processing

## 📋 Prerequisites

1. **GitHub Account** (free) - https://github.com/signup
2. **Railway Account** (free) - https://railway.app/
3. **Git installed** on your computer

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `paddleocr-server`
3. Description: `PaddleOCR server for PhilHealth processing`
4. Set to **Public** (required for free Railway deployment)
5. Click **Create repository**

### Step 2: Push Code to GitHub

Open Command Prompt in the `LocalOCRServer` folder:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - PaddleOCR server"

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/paddleocr-server.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Create Railway Project

1. Go to https://railway.app/
2. Click **Start a New Project**
3. Click **Deploy from GitHub repo**
4. Authorize Railway to access your GitHub
5. Select your `paddleocr-server` repository
6. Click **Deploy Now**

### Step 4: Configure Environment

Railway will automatically detect it's a Python app and install dependencies.

**Wait for deployment** (~3-5 minutes for first deploy)

### Step 5: Get Your Public URL

1. In Railway dashboard, click your project
2. Click **Settings** tab
3. Scroll to **Networking**
4. Click **Generate Domain**
5. Copy the URL (looks like: `https://paddleocr-server-production-xxxx.up.railway.app`)

### Step 6: Test Your Deployment

Open your browser and visit:
```
https://your-railway-url.up.railway.app/health
```

Should show:
```json
{
  "status": "healthy",
  "service": "PaddleOCR Server",
  "version": "1.0.0"
}
```

### Step 7: Configure in Your App

1. Open your app
2. Go to **OCR Settings**
3. Select **Local Server (PaddleOCR)**
4. Enter your Railway URL: `https://your-railway-url.up.railway.app`
5. Click **Test** button
6. Should show: ✅ **"Connected! Server is running and ready."**

## 📝 Required Files for Railway

Railway needs these files (already included):

### 1. `requirements.txt` or `requirements_paddleocr.txt`
Railway will automatically install Python dependencies.

### 2. `Procfile` (CREATE THIS)
Tells Railway how to start your server.

### 3. `runtime.txt` (OPTIONAL)
Specifies Python version.

## 🔧 Create Required Files

### Create `Procfile`
```bash
web: python paddleocr_server.py
```

### Create `runtime.txt` (optional)
```bash
python-3.11.0
```

### Update `paddleocr_server.py` (for Railway)

Change the last line from:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

To:
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=False)
```

This allows Railway to assign the port dynamically.

## 💰 Cost Estimation

### Railway Free Tier:
- **$5 credit/month** (free)
- **500 hours** of usage
- **100GB bandwidth**

### Estimated Usage:
- **Per OCR request:** ~2-5 seconds
- **100 folders/day:** ~$0.50/month
- **500 folders/day:** ~$2.50/month
- **1000 folders/day:** ~$5/month

**Conclusion:** Free tier is enough for moderate usage!

## 🔄 Updating Your Deployment

When you make changes:

```bash
# Make your changes to the code
# Then commit and push:

git add .
git commit -m "Update server code"
git push

# Railway will automatically redeploy!
```

## ⚡ Performance

### Railway Server:
- **CPU:** Shared vCPU
- **RAM:** 512MB-1GB
- **Speed:** ~3-7 seconds per image
- **Uptime:** 99.9%

### Comparison:
| Provider | Speed | Cost | Setup |
|----------|-------|------|-------|
| **Groq API** | ⭐⭐⭐⭐ | Free tier | Easy |
| **Railway** | ⭐⭐⭐ | $5/month | Medium |
| **Local** | ⭐⭐⭐ | Free | Easy |

## 🛠️ Troubleshooting

### "Application failed to respond"
- Check Railway logs for errors
- Verify `Procfile` is correct
- Make sure port is dynamic: `port = int(os.environ.get('PORT', 5000))`

### "Out of memory"
- PaddleOCR uses ~500MB-1GB RAM
- Railway free tier has 512MB-1GB
- Consider upgrading to Railway Pro ($5/month for 2GB RAM)

### "Deployment failed"
- Check `requirements_paddleocr.txt` is correct
- Verify all files are pushed to GitHub
- Check Railway build logs for specific errors

### "Too slow"
- Railway free tier uses shared CPU
- Consider upgrading to Railway Pro for dedicated resources
- Or use Groq API for faster processing

## 🔐 Security

### Environment Variables (Optional)

Add API keys or secrets in Railway:

1. Go to Railway dashboard
2. Click your project
3. Go to **Variables** tab
4. Add variables like:
   - `SECRET_KEY=your-secret-key`
   - `ALLOWED_ORIGINS=https://your-app-domain.com`

### CORS Configuration

The server already has CORS enabled for all origins. To restrict:

Edit `paddleocr_server.py`:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://your-app-domain.com"]
    }
})
```

## 📊 Monitoring

### View Logs:
1. Go to Railway dashboard
2. Click your project
3. Click **Deployments** tab
4. Click latest deployment
5. View real-time logs

### Check Usage:
1. Go to Railway dashboard
2. Click **Usage** tab
3. See credit usage and bandwidth

## 🎉 Success!

Once deployed, you have:
- ✅ Public OCR server accessible from anywhere
- ✅ No need to keep your computer running
- ✅ Automatic updates when you push to GitHub
- ✅ Free tier for moderate usage
- ✅ Professional deployment with monitoring

## 🆘 Need Help?

### Railway Support:
- Documentation: https://docs.railway.app/
- Discord: https://discord.gg/railway
- Twitter: @Railway

### Alternative Options:
1. **Groq API** - Fastest, easiest, free tier
2. **ngrok** - Quick testing, temporary URL
3. **Google Cloud Run** - Pay per use, scales to zero
4. **Heroku** - Similar to Railway, $5/month

## 📚 Next Steps

After deployment:
1. ✅ Test the health endpoint
2. ✅ Test OCR endpoint with sample image
3. ✅ Configure in your app
4. ✅ Process some folders
5. ✅ Monitor usage in Railway dashboard

Enjoy your cloud-hosted OCR server! 🚀
