"""
PaddleOCR Local Server
Provides OCR services using PaddleOCR for offline processing
Can be deployed locally or to cloud platforms like Railway.app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from paddleocr import PaddleOCR
import base64
import io
import os
from PIL import Image
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for Apps Script

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize PaddleOCR (loads once at startup)
logger.info("Initializing PaddleOCR...")
ocr = PaddleOCR(
    use_textline_orientation=True,  # Enable text rotation detection
    lang='en'                        # English language
    # Note: GPU settings are now configured via environment variables or device parameter
    # To use GPU, set device='gpu' instead of use_gpu=True
)
logger.info("PaddleOCR initialized successfully!")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PaddleOCR Server',
        'version': '1.0.0'
    })

@app.route('/ocr', methods=['POST'])
def process_ocr():
    """
    Process OCR on base64 encoded image
    
    Request body:
    {
        "image": "base64_encoded_image_data"
    }
    
    Response:
    {
        "text": "extracted text",
        "hasFaces": false,
        "faceCount": 0,
        "confidence": 0.95
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'error': 'No image data provided'
            }), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to temporary bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Run OCR
        logger.info("Processing OCR...")
        result = ocr.ocr(img_byte_arr.getvalue(), cls=True)
        
        # Extract text and confidence
        extracted_text = []
        total_confidence = 0
        count = 0
        
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]  # Get text
                confidence = line[1][1]  # Get confidence score
                extracted_text.append(text)
                total_confidence += confidence
                count += 1
        
        full_text = ' '.join(extracted_text)
        avg_confidence = total_confidence / count if count > 0 else 0
        
        # Simple face detection (check for common face-related keywords)
        # Note: PaddleOCR doesn't detect faces, so we use text analysis
        face_keywords = ['face', 'photo', 'portrait', 'mugshot']
        has_faces = any(keyword in full_text.lower() for keyword in face_keywords)
        
        logger.info(f"OCR complete. Extracted {len(full_text)} characters")
        
        return jsonify({
            'text': full_text,
            'hasFaces': has_faces,
            'faceCount': 1 if has_faces else 0,
            'confidence': round(avg_confidence, 2),
            'lines': len(extracted_text)
        })
        
    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/ocr/batch', methods=['POST'])
def process_batch_ocr():
    """
    Process multiple images in one request
    
    Request body:
    {
        "images": ["base64_1", "base64_2", "base64_3"]
    }
    
    Response:
    {
        "results": [
            {"text": "...", "hasFaces": false, ...},
            {"text": "...", "hasFaces": false, ...},
            {"text": "...", "hasFaces": false, ...}
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'images' not in data:
            return jsonify({
                'error': 'No images data provided'
            }), 400
        
        images = data['images']
        results = []
        
        for idx, img_base64 in enumerate(images):
            try:
                # Decode base64 image
                image_data = base64.b64decode(img_base64)
                image = Image.open(io.BytesIO(image_data))
                
                # Convert to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save to temporary bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Run OCR
                logger.info(f"Processing image {idx + 1}/{len(images)}...")
                result = ocr.ocr(img_byte_arr.getvalue(), cls=True)
                
                # Extract text and confidence
                extracted_text = []
                total_confidence = 0
                count = 0
                
                if result and result[0]:
                    for line in result[0]:
                        text = line[1][0]
                        confidence = line[1][1]
                        extracted_text.append(text)
                        total_confidence += confidence
                        count += 1
                
                full_text = ' '.join(extracted_text)
                avg_confidence = total_confidence / count if count > 0 else 0
                
                # Simple face detection
                face_keywords = ['face', 'photo', 'portrait', 'mugshot']
                has_faces = any(keyword in full_text.lower() for keyword in face_keywords)
                
                results.append({
                    'text': full_text,
                    'hasFaces': has_faces,
                    'faceCount': 1 if has_faces else 0,
                    'confidence': round(avg_confidence, 2),
                    'lines': len(extracted_text)
                })
                
            except Exception as e:
                logger.error(f"Error processing image {idx + 1}: {str(e)}")
                results.append({
                    'text': '',
                    'hasFaces': False,
                    'faceCount': 0,
                    'confidence': 0,
                    'error': str(e)
                })
        
        logger.info(f"Batch OCR complete. Processed {len(results)} images")
        
        return jsonify({
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Batch OCR Error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 PaddleOCR Server Starting...")
    print("=" * 50)
    
    # Get port from environment variable (Railway) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"📍 Server will run on: http://localhost:{port}")
    print(f"🔍 Health check: http://localhost:{port}/health")
    print(f"📝 OCR endpoint: http://localhost:{port}/ocr")
    print(f"📦 Batch endpoint: http://localhost:{port}/ocr/batch")
    print("=" * 50)
    print("⚠️  Keep this window open while using the app")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=False)
