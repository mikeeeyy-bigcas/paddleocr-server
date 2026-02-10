# PaddleOCR Server

A Flask-based OCR server using PaddleOCR for processing PhilHealth images.

## 🎯 Features

- ✅ **Free & Open Source** - No API costs
- ✅ **Privacy-Focused** - Process images locally or on your own server
- ✅ **Accurate** - 90-95% OCR accuracy
- ✅ **Batch Processing** - Handle multiple images in one request
- ✅ **Easy Deployment** - Run locally or deploy to Railway/Cloud

## 🚀 Quick Start

### Option 1: Run Locally (Windows)

```bash
# Double-click this file:
start-paddleocr.bat

# Or manually:
pip install -r requirements_paddleocr.txt
python paddleocr_server.py
```

Server runs on: http://localhost:5000

**Note:** Local server won't work with Google Apps Script (cloud-based). Use Railway deployment instead.

### Option 2: Deploy to Railway (Recommended)

See: **[RAILWAY-QUICKSTART.md](RAILWAY-QUICKSTART.md)** (5-minute setup)

## 📁 Files

| File | Description |
|------|-------------|
| `paddleocr_server.py` | Main Flask server |
| `requirements_paddleocr.txt` | Python dependencies |
| `Procfile` | Railway deployment config |
| `runtime.txt` | Python version for Railway |
| `start-paddleocr.bat` | Windows startup script |
| `RAILWAY-QUICKSTART.md` | 5-minute Railway deployment guide |
| `DEPLOY-TO-RAILWAY.md` | Detailed Railway deployment guide |
| `PADDLEOCR-SETUP.md` | Local setup guide |
| `FINAL-STATUS.md` | Current status and troubleshooting |

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "PaddleOCR Server",
  "version": "1.0.0"
}
```

### Single Image OCR
```bash
POST /ocr
Content-Type: application/json

{
  "image": "base64_encoded_image_data"
}
```

Response:
```json
{
  "text": "extracted text",
  "hasFaces": false,
  "faceCount": 0,
  "confidence": 0.95,
  "lines": 10
}
```

### Batch OCR (3 images)
```bash
POST /ocr/batch
Content-Type: application/json

{
  "images": ["base64_1", "base64_2", "base64_3"]
}
```

Response:
```json
{
  "results": [
    {"text": "...", "hasFaces": false, "confidence": 0.95},
    {"text": "...", "hasFaces": false, "confidence": 0.92},
    {"text": "...", "hasFaces": false, "confidence": 0.98}
  ]
}
```

## 🛠️ Configuration

### Enable GPU (Optional)

Edit `paddleocr_server.py` line 23:
```python
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang='en',
    device='gpu'  # Add this for GPU acceleration
)
```

Requires: NVIDIA GPU + CUDA toolkit

### Change Port

Edit `paddleocr_server.py` last line:
```python
port = int(os.environ.get('PORT', 8080))  # Change 5000 to 8080
```

### CORS Configuration

Edit `paddleocr_server.py` line 16:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://your-domain.com"]  # Restrict origins
    }
})
```

## 📊 Performance

### Local (CPU):
- **Speed:** ~2-5 seconds per image
- **RAM:** ~500MB-1GB
- **Concurrent:** 1-2 requests

### Railway (Cloud):
- **Speed:** ~3-7 seconds per image
- **RAM:** 512MB-1GB
- **Concurrent:** 2-3 requests
- **Cost:** $5 credit/month (free tier)

### With GPU:
- **Speed:** ~0.5-1 second per image
- **RAM:** ~1-2GB
- **Concurrent:** 5-10 requests

## 🔐 Security

### For Production:

1. **Add Authentication:**
```python
from flask import request

@app.before_request
def check_auth():
    token = request.headers.get('Authorization')
    if token != 'your-secret-token':
        return jsonify({'error': 'Unauthorized'}), 401
```

2. **Rate Limiting:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])
```

3. **HTTPS Only:**
Use Railway/Cloud deployment (automatic HTTPS)

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'paddleocr'"
```bash
pip install -r requirements_paddleocr.txt
```

### "Unknown argument" errors
Make sure you're using PaddleOCR 3.4.0+ with updated parameters:
- ✅ `use_textline_orientation=True`
- ❌ `use_angle_cls=True` (deprecated)
- ❌ `show_log=False` (removed)
- ❌ `use_gpu=True` (use `device='gpu'` instead)

### "Port already in use"
Change port in `paddleocr_server.py` or kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### "Out of memory"
- Close other applications
- Reduce batch size
- Upgrade to Railway Pro (2GB RAM)
- Use Groq API instead

## 📚 Documentation

- **Quick Start:** [RAILWAY-QUICKSTART.md](RAILWAY-QUICKSTART.md)
- **Full Deployment:** [DEPLOY-TO-RAILWAY.md](DEPLOY-TO-RAILWAY.md)
- **Local Setup:** [PADDLEOCR-SETUP.md](PADDLEOCR-SETUP.md)
- **Status & Fixes:** [FINAL-STATUS.md](FINAL-STATUS.md)

## 🤝 Contributing

Improvements welcome! Common enhancements:
- Add authentication
- Implement rate limiting
- Support more languages
- Add image preprocessing
- Optimize for speed

## 📄 License

MIT License - Free to use and modify

## 🆘 Support

- **PaddleOCR Docs:** https://github.com/PaddlePaddle/PaddleOCR
- **Railway Docs:** https://docs.railway.app/
- **Flask Docs:** https://flask.palletsprojects.com/

## 🎉 Credits

- **PaddleOCR** - Baidu's open-source OCR toolkit
- **Flask** - Python web framework
- **Railway** - Cloud deployment platform

---

Made with ❤️ for PhilHealth image processing
