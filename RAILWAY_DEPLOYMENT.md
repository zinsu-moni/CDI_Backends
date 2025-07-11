# Railway Deployment Guide for Crop Disease Identification API

## 🚀 Quick Deployment Steps

1. **Connect Repository to Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `CDI_Backends` repository

2. **Set Environment Variables**
   In Railway dashboard → Variables tab, add:
   ```
   API_KEY=u12lFbhGXOPacNJgi4pqK2scNsm34OryIiw99IIPJLKzjgntD5
   DEEPSEEK_API_KEY=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
   ```

3. **Verify Configuration Files**
   - ✅ `Procfile`: Contains startup command
   - ✅ `requirements.txt`: Lists dependencies
   - ✅ `runtime.txt`: Specifies Python 3.11.9
   - ✅ `railway.json`: Railway configuration

## 🔧 Common Issues & Solutions

### Issue 1: Build Failures
**Solution**: Check Railway build logs for missing dependencies
- Ensure all packages in `requirements.txt` are correctly specified
- Verify Python version compatibility

### Issue 2: App Crashes on Startup
**Solution**: Check Railway deployment logs
- Verify environment variables are set
- Ensure port binding is correct (`$PORT` variable)

### Issue 3: API Endpoints Not Responding
**Solution**: 
- Test health endpoint first: `/health`
- Check CORS configuration
- Verify FastAPI app is properly configured

### Issue 4: File Upload Issues
**Solution**:
- Ensure `uploads/` directory handling in code
- Check file size limits
- Verify multipart form data handling

## 📊 Monitoring Your Deployment

### Key Endpoints to Monitor:
1. `GET /health` - Health check
2. `GET /api/info` - API information
3. `GET /` - Web interface
4. `POST /analyze` - Main functionality

### Performance Tips:
- Monitor Railway metrics dashboard
- Check response times
- Monitor memory usage
- Set up proper error logging

## 🛡️ Security Considerations

1. **Environment Variables**: Never commit API keys to Git
2. **CORS**: Currently set to allow all origins (`*`) - consider restricting for production
3. **File Uploads**: Implement file type validation
4. **Rate Limiting**: Consider adding rate limiting for production use

## 📱 Testing Your API

Use the included `test_railway_deployment.py` script:
```bash
python test_railway_deployment.py
```

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to your main branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

## 📞 Support Resources

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- FastAPI Documentation: https://fastapi.tiangolo.com
