# Render Deployment Guide for Crop Disease Identification API

## 🚀 Quick Deployment Steps

### Option 1: Using Render Dashboard (Recommended)

1. **Sign up/Login to Render**
   - Go to [render.com](https://render.com)
   - Sign up or login with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your `CDI_Backends` repository

3. **Configure the Service**
   ```
   Name: crop-disease-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main_fastapi:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   In the Environment tab, add:
   ```
   API_KEY=u12lFbhGXOPacNJgi4pqK2scNsm34OryIiw99IIPJLKzjgntD5
   DEEPSEEK_API_KEY=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
   PYTHON_VERSION=3.11.9
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

### Option 2: Using render.yaml (Infrastructure as Code)

If you prefer automated deployment, Render will use the `render.yaml` file in your repository.

## 🔧 Render vs Railway Differences

| Feature | Railway | Render |
|---------|---------|--------|
| **Free Tier** | 500 hours/month | 750 hours/month |
| **Startup Speed** | Faster | Slower cold starts |
| **URL Format** | `*.up.railway.app` | `*.onrender.com` |
| **Build Time** | Faster | Slower |
| **Persistence** | Ephemeral | Ephemeral |

## 📁 Files for Render Deployment

Your project now includes:

1. ✅ **requirements.txt** - Python dependencies
2. ✅ **runtime.txt** - Python version (3.11.9)
3. ✅ **render.yaml** - Render service configuration
4. ✅ **start.sh** - Optional startup script
5. ✅ **main_fastapi.py** - Your FastAPI application

## 🛠️ Configuration Details

### Environment Variables Required:
- `API_KEY` - For KindWise crop disease API
- `DEEPSEEK_API_KEY` - For AI treatment recommendations
- `PORT` - Automatically set by Render

### Health Check:
- Endpoint: `/health`
- Expected response: `{"status": "healthy", "service": "Crop Disease Identification API"}`

## 📊 Expected Deployment URLs

After deployment, your API will be available at:
```
https://your-service-name.onrender.com
```

### Key Endpoints:
- 🏥 Health: `https://your-service-name.onrender.com/health`
- 📊 Info: `https://your-service-name.onrender.com/api/info`
- 🌐 Web UI: `https://your-service-name.onrender.com/`
- 🔍 Analysis: `https://your-service-name.onrender.com/analyze` (POST)

## 🔍 Testing Your Deployment

Use the test script:
```bash
python test_deployment.py
```

## ⚠️ Important Notes for Render

1. **Cold Starts**: Free tier services sleep after 15 minutes of inactivity
2. **Build Time**: First deployment may take 5-10 minutes
3. **Logs**: Check Render dashboard for build and runtime logs
4. **File Storage**: Files uploaded are not persistent across deployments

## 🔄 Continuous Deployment

Render automatically redeploys when you push to your main branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

## 💡 Optimization Tips

1. **Reduce Build Time**: Pin exact package versions in requirements.txt
2. **Health Checks**: Render uses `/health` endpoint to monitor service
3. **Environment**: Use environment variables for all secrets
4. **Monitoring**: Check Render metrics for performance insights

## 🆚 When to Choose Render vs Railway

**Choose Render if:**
- You need more free tier hours (750 vs 500)
- You prefer detailed build logs
- You want Infrastructure as Code (render.yaml)

**Choose Railway if:**
- You prioritize faster deployments
- You want quicker cold start times
- You prefer simpler dashboard UI

## 📞 Support Resources

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- FastAPI on Render: https://render.com/docs/deploy-fastapi
