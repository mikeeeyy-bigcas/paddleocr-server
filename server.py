"""
Local OCR Server for PhilHealth Document Extraction
Uses Ollama with Llama 3.2 Vision model
Provides REST API compatible with Google Apps Script
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import base64
import io
import os
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Allow Apps Script to call this API

# Configuration
OLLAMA_MODEL = 'minicpm-v:8b'  # Lighter model for systems with 16GB RAM
TEMP_IMAGE_PATH = 'temp_image.png'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test if Ollama is running
        ollama.list()
        return jsonify({
            'status': 'healthy',
            'model': OLLAMA_MODEL,
            'message': 'Local OCR server is running'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Ollama is not running or model not available'
        }), 503

@app.route('/ocr', methods=['POST'])
def extract_text():
    """
    OCR extraction endpoint
    Expects JSON with:
    - image: base64 encoded image (with or without data URL prefix)
    - prompt: extraction prompt text
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        image_data = data['image']
        prompt = data.get('prompt', 'Extract all text from this image')
        
        # Handle data URL format (data:image/png;base64,...)
        if image_data.startswith('data:'):
            image_data = image_data.split(',', 1)[1]
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save temporarily for Ollama
            image.save(TEMP_IMAGE_PATH)
            logger.info(f"Image saved: {image.size[0]}x{image.size[1]} pixels")
            
        except Exception as e:
            logger.error(f"Image decode error: {str(e)}")
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        # Call Ollama vision model
        logger.info(f"Calling Ollama model: {OLLAMA_MODEL}")
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [TEMP_IMAGE_PATH]
            }]
        )
        
        extracted_text = response['message']['content']
        logger.info(f"Extraction successful, response length: {len(extracted_text)}")
        
        # Clean up temp file
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
        
        return jsonify({
            'success': True,
            'content': extracted_text,
            'model': OLLAMA_MODEL
        }), 200
        
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        
        # Clean up temp file on error
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List available Ollama models"""
    try:
        models = ollama.list()
        return jsonify({
            'models': [m['name'] for m in models.get('models', [])]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Local OCR Server Starting...")
    print("=" * 60)
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Port: 5000")
    print(f"Health Check: http://localhost:5000/health")
    print(f"OCR Endpoint: http://localhost:5000/ocr")
    print("=" * 60)
    print("\n⚠️  Make sure Ollama is running and model is installed:")
    print(f"   ollama pull {OLLAMA_MODEL}")
    print("\n🌐 To expose to internet (for Apps Script):")
    print("   ngrok http 5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
