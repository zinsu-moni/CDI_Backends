"""
FastAPI Crop Disease Identification API
---------------------------------------
A REST API for crop disease identification using KindWise API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import base64
import requests
import json
from PIL import Image
import io
import tempfile
from typing import Optional
import shutil
import subprocess
import sys
from openai import OpenAI

app = FastAPI(title="Crop Disease Identification API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Configuration
API_URL = "https://crop.kindwise.com/api/v1/identification"
API_KEY = os.environ.get("API_KEY", "u12lFbhGXOPacNJgi4pqK2scNsm34OryIiw99IIPJLKzjgntD5")

# DeepSeek Configuration
try:
    DEEPSEEK_CLIENT = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY", "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"),
        base_url="https://openrouter.ai/api/v1"
    )
except Exception as e:
    print(f"Warning: Failed to initialize OpenAI client: {e}")
    DEEPSEEK_CLIENT = None

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def get_deepseek_treatment(crops, diseases):
    """Get treatment recommendations from DeepSeek AI"""
    try:
        # Check if DeepSeek client is available
        if DEEPSEEK_CLIENT is None:
            return "AI treatment recommendations are temporarily unavailable. Please consult with a local agricultural expert for specific treatment advice."
        
        # Create a prompt for DeepSeek
        prompt = "You are an expert agricultural consultant. Based on the following crop analysis results, provide brief treatment and care recommendations:\n\n"
        
        if crops:
            prompt += "Identified Crops:\n"
            for crop in crops:
                prompt += f"- {crop['name']} ({crop['scientific_name']}): {crop['confidence']}% confidence\n"
        
        if diseases:
            prompt += "\nDetected Plant Health Issues:\n"
            for disease in diseases:
                prompt += f"- {disease['name']}: {disease['confidence']}% confidence\n"
        else:
            prompt += "\nNo diseases detected - plant appears healthy.\n"
        
        prompt += "\nPlease provide:\n1. Brief assessment of the plant condition\n2. Immediate treatment recommendations (if needed)\n3. General care tips\n4. When to seek further consultation\n\nKeep the response concise but informative (maximum 200 words)."
        
        # Call DeepSeek API with proper headers
        completion = DEEPSEEK_CLIENT.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert agricultural consultant specializing in crop disease diagnosis and treatment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Crop Disease Identification API"
            }
        )
        
        return completion.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"DeepSeek API Error: {str(e)}")
        # Fallback to basic treatment recommendations
        return get_basic_treatment_recommendations(crops, diseases)

def get_basic_treatment_recommendations(crops, diseases):
    """Provide basic treatment recommendations when AI API is unavailable"""
    recommendations = "🌱 Basic Treatment Recommendations:\n\n"
    
    if diseases and len(diseases) > 0:
        recommendations += "⚠️ Plant Health Issues Detected:\n"
        for disease in diseases:
            disease_name = disease['name'].lower()
            
            # Basic recommendations based on common disease types
            if 'blight' in disease_name or 'spot' in disease_name:
                recommendations += f"• {disease['name']}: Remove affected leaves, improve air circulation, consider copper-based fungicide.\n"
            elif 'rust' in disease_name:
                recommendations += f"• {disease['name']}: Remove infected parts, avoid overhead watering, apply fungicide if severe.\n"
            elif 'mildew' in disease_name:
                recommendations += f"• {disease['name']}: Increase air circulation, reduce humidity, consider organic fungicide treatment.\n"
            elif 'rot' in disease_name:
                recommendations += f"• {disease['name']}: Improve drainage, reduce watering, remove affected parts immediately.\n"
            elif 'wilt' in disease_name:
                recommendations += f"• {disease['name']}: Check soil drainage, adjust watering schedule, may need soil treatment.\n"
            else:
                recommendations += f"• {disease['name']}: Monitor closely, maintain good plant hygiene, consult agricultural expert.\n"
        
        recommendations += "\n🚨 General Disease Management:\n"
        recommendations += "- Remove and dispose of infected plant material\n"
        recommendations += "- Improve air circulation around plants\n"
        recommendations += "- Water at soil level, avoid wetting leaves\n"
        recommendations += "- Apply preventive treatments if recommended\n"
        recommendations += "- Monitor daily for disease progression\n"
    else:
        recommendations += "✅ Plant Health Status: HEALTHY\n"
        recommendations += "No diseases detected. Your crop appears to be in good condition!\n\n"
        recommendations += "🌿 Preventive Care Tips:\n"
        recommendations += "- Maintain regular watering schedule\n"
        recommendations += "- Ensure proper soil drainage\n"
        recommendations += "- Provide adequate nutrition\n"
        recommendations += "- Monitor for early signs of stress\n"
        recommendations += "- Keep growing area clean\n"
    
    if crops and len(crops) > 0:
        crop_name = crops[0]['name'].lower()
        recommendations += f"\n🌾 Specific Care for {crops[0]['name']}:\n"
        
        # Basic care tips for common crops
        if 'tomato' in crop_name:
            recommendations += "- Provide support/stakes for growth\n- Regular pruning of suckers\n- Deep, infrequent watering\n"
        elif 'corn' in crop_name or 'maize' in crop_name:
            recommendations += "- Ensure adequate spacing\n- Side-dress with nitrogen fertilizer\n- Monitor for corn borer\n"
        elif 'wheat' in crop_name:
            recommendations += "- Monitor soil moisture\n- Watch for rust diseases\n- Time harvest properly\n"
        elif 'rice' in crop_name:
            recommendations += "- Maintain proper water levels\n- Monitor for blast disease\n- Ensure good drainage during maturity\n"
        else:
            recommendations += "- Follow standard crop management practices\n- Monitor growth stages\n- Adjust care based on plant needs\n"
    
    recommendations += "\n💡 For detailed consultation, click 'Send to ChatBot' below."
    
    return recommendations

@app.get("/", response_class=HTMLResponse)
async def get_upload_form():
    """Serve a simple HTML form for testing the API"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crop Disease Identification</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            .button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            .button:hover { background: #45a049; }
            .results { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }
            .loading { display: none; color: #666; }
            #imagePreview { max-width: 300px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Crop Disease Identification</h1>
            <p>Upload an image of your crop to identify the plant species and detect any diseases.</p>
            
            <div class="upload-area">
                <input type="file" id="imageInput" accept="image/*" style="display: none;">
                <button class="button" onclick="document.getElementById('imageInput').click()">Choose Image</button>
                <p>or drag and drop an image here</p>
                <img id="imagePreview" style="display: none;">
            </div>
            
            <button class="button" id="analyzeBtn" onclick="analyzeImage()" disabled>Analyze Crop</button>
            <button class="button" id="chatbotBtn" onclick="sendToChatbot()" disabled style="background: #2196F3;">Send to ChatBot</button>
            
            <div class="loading" id="loading">🔍 Analyzing your crop image and getting AI treatment recommendations...</div>
            
            <div class="results" id="results" style="display: none;">
                <h3>Analysis Results:</h3>
                <div id="resultsContent"></div>
                
                <div id="treatmentSection" style="margin-top: 20px; padding: 15px; background: #f0f8ff; border-radius: 5px; border-left: 4px solid #2196F3;">
                    <h4>🤖 AI Treatment Recommendations:</h4>
                    <div id="treatmentContent" style="white-space: pre-wrap;"></div>
                </div>
            </div>
        </div>

        <script>
            let analysisResults = null;
            let uploadedFile = null;

            document.getElementById('imageInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    uploadedFile = file;
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.getElementById('imagePreview');
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                        document.getElementById('analyzeBtn').disabled = false;
                    };
                    reader.readAsDataURL(file);
                }
            });

            async function analyzeImage() {
                if (!uploadedFile) return;

                const formData = new FormData();
                formData.append('file', uploadedFile);

                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();
                    
                    if (result.success) {
                        analysisResults = result;
                        displayResults(result);
                        document.getElementById('chatbotBtn').disabled = false;
                    } else {
                        alert('Analysis failed: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }

            function displayResults(result) {
                let html = '<h4>🌾 Identified Crops:</h4>';
                
                if (result.crops && result.crops.length > 0) {
                    result.crops.forEach((crop, index) => {
                        html += `<div style="margin: 10px 0; padding: 10px; background: #e8f5e8; border-radius: 5px;">
                            <strong>Crop ${index + 1}:</strong> ${crop.name} (${crop.scientific_name})<br>
                            <strong>Confidence:</strong> ${crop.confidence}%
                        </div>`;
                    });
                } else {
                    html += '<p>No crops identified.</p>';
                }

                if (result.diseases && result.diseases.length > 0) {
                    html += '<h4>🏥 Plant Health Conditions:</h4>';
                    result.diseases.forEach((disease, index) => {
                        html += `<div style="margin: 10px 0; padding: 10px; background: #ffe8e8; border-radius: 5px;">
                            <strong>Condition ${index + 1}:</strong> ${disease.name}<br>
                            <strong>Confidence:</strong> ${disease.confidence}%
                        </div>`;
                    });
                } else {
                    html += '<h4>✅ Plant Health:</h4><p>No diseases detected. The plant appears healthy!</p>';
                }

                document.getElementById('resultsContent').innerHTML = html;
                document.getElementById('results').style.display = 'block';
                
                // Display AI treatment recommendations if available
                if (result.ai_treatment) {
                    document.getElementById('treatmentContent').textContent = result.ai_treatment;
                } else {
                    document.getElementById('treatmentContent').textContent = 'AI treatment recommendations not available.';
                }
            }

            async function sendToChatbot() {
                if (!analysisResults) {
                    alert('No analysis results to send to chatbot.');
                    return;
                }

                try {
                    const response = await fetch('/send-to-chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(analysisResults)
                    });

                    const result = await response.json();
                    
                    if (result.success) {
                        alert('ChatBot launched successfully! Check for a new window or tab.');
                    } else {
                        alert('Failed to launch ChatBot: ' + result.error);
                    }
                } catch (error) {
                    alert('Error launching ChatBot: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/analyze")
async def analyze_crop_image(file: UploadFile = File(...)):
    """Analyze uploaded crop image using KindWise API"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_bytes = await file.read()
        
        # Validate image can be opened
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # Resize if too large
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.LANCZOS)
            
            # Convert to RGB and save as JPEG
            image = image.convert('RGB')
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=95)
            image_bytes = output_buffer.getvalue()
            
        except Exception as img_err:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(img_err)}")
        
        # Encode image for API
        encoded_string = base64.b64encode(image_bytes).decode('utf-8')
        
        # Prepare API request
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY
        }
        
        payload = {
            'images': [encoded_string],
            'similar_images': True
        }
        
        # Call KindWise API
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            # Parse results
            crops = []
            diseases = []
            
            if 'result' in data and data['result']:
                result_data = data['result']
                
                # Extract crop information
                if 'crop' in result_data and 'suggestions' in result_data['crop']:
                    for crop in result_data['crop']['suggestions']:
                        crops.append({
                            'name': crop.get('name', 'Unknown'),
                            'scientific_name': crop.get('scientific_name', ''),
                            'confidence': round(crop.get('probability', 0) * 100, 2)
                        })
                
                # Extract disease information
                if 'disease' in result_data and 'suggestions' in result_data['disease']:
                    for disease in result_data['disease']['suggestions']:
                        diseases.append({
                            'name': disease.get('name', 'Unknown'),
                            'confidence': round(disease.get('probability', 0) * 100, 2)
                        })
            
            # Save results for chatbot integration
            result_summary = {
                'success': True,
                'crops': crops,
                'diseases': diseases,
                'raw_data': data,
                'image_filename': file.filename
            }
            
            # Automatically get AI treatment recommendations from DeepSeek
            print("Getting AI treatment recommendations...")
            try:
                ai_treatment = await get_deepseek_treatment(crops, diseases)
                result_summary['ai_treatment'] = ai_treatment
                print("AI treatment recommendations obtained successfully")
            except Exception as ai_error:
                print(f"AI treatment error: {str(ai_error)}")
                # Use basic recommendations as fallback
                ai_treatment = get_basic_treatment_recommendations(crops, diseases)
                result_summary['ai_treatment'] = ai_treatment
            
            # Save to temporary files for chatbot integration
            crop_data_file = os.path.join(UPLOAD_DIR, "latest_analysis.json")
            with open(crop_data_file, "w") as f:
                json.dump(result_summary, f)
            
            # Save the analyzed image
            image_file_path = os.path.join(UPLOAD_DIR, "latest_image.jpg")
            with open(image_file_path, "wb") as f:
                f.write(image_bytes)
            
            return result_summary
            
        else:
            error_detail = f"API returned status code {response.status_code}"
            try:
                error_detail = response.json()
            except:
                try:
                    error_detail = response.text
                except:
                    pass
            
            raise HTTPException(status_code=500, detail=f"API Error: {error_detail}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-to-chatbot")
async def send_to_chatbot(analysis_data: dict):
    """Launch chatbot with analysis results"""
    try:
        # Create formatted summary
        crop_summary = "Crop Analysis Results:\n\n"
        
        if analysis_data.get('crops'):
            crop_summary += "Identified Crops:\n"
            for crop in analysis_data['crops']:
                crop_summary += f"- {crop['name']} ({crop['scientific_name']}): {crop['confidence']}% confidence\n"
        
        if analysis_data.get('diseases'):
            crop_summary += "\nPlant Health Conditions:\n"
            for disease in analysis_data['diseases']:
                crop_summary += f"- {disease['name']}: {disease['confidence']}% confidence\n"
        elif analysis_data.get('crops'):
            crop_summary += "\nNo diseases detected. The plant appears healthy.\n"
        
        # Add AI treatment recommendations if available
        if analysis_data.get('ai_treatment'):
            crop_summary += f"\nAI Treatment Recommendations:\n{analysis_data['ai_treatment']}\n"
        
        # Save data for chatbot
        chatbot_data = {
            "crop_summary": crop_summary,
            "raw_data": analysis_data.get('raw_data', {})
        }
        
        crop_data_file = os.path.join(UPLOAD_DIR, "crop_analysis_data.json")
        with open(crop_data_file, "w") as f:
            json.dump(chatbot_data, f)
        
        # Get paths
        image_file_path = os.path.join(UPLOAD_DIR, "latest_image.jpg")
        launcher_path = os.path.join("..", "chat_bot", "launch_chatbot.py")
        
        # Launch chatbot
        try:
            subprocess.Popen([
                sys.executable, launcher_path,
                "--analysis-data", os.path.abspath(crop_data_file),
                "--image-path", os.path.abspath(image_file_path)
            ])
            
            return {"success": True, "message": "ChatBot launched successfully"}
            
        except Exception as launch_error:
            return {"success": False, "error": f"Failed to launch ChatBot: {str(launch_error)}"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Crop Disease Identification API"}

@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "name": "Crop Disease Identification API",
        "version": "1.0.0",
        "description": "REST API for crop disease identification using KindWise API with automatic AI treatment recommendations from DeepSeek",
        "workflow": "1. Upload image → 2. KindWise analysis → 3. Automatic DeepSeek AI treatment → 4. Combined results output → 5. Optional chatbot consultation",
        "endpoints": {
            "/": "Upload form (HTML interface)",
            "/analyze": "POST - Analyze crop image",
            "/send-to-chatbot": "POST - Launch chatbot with results",
            "/health": "GET - Health check",
            "/api/info": "GET - API information"
        }
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    
    print("🌱 Starting Crop Disease Identification API...")
    print(f"📖 Documentation: http://0.0.0.0:{port}/docs")
    print(f"🌐 Web Interface: http://0.0.0.0:{port}")
    
    uvicorn.run(
        "main_fastapi:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Set to False for production
        log_level="info"
    )
