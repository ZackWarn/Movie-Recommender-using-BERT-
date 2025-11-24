# Vercel + Render Deployment Guide

## Architecture
- Frontend (Next.js): Vercel
- Backend (Flask): Render
- Total Cost: $0/month (Free tier)

## Part 1: Deploy Backend to Render

### Step 1: Push to GitHub
git add .
git commit -m "Add Render deployment config"
git push origin main

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" > "Web Service"
4. Connect your GitHub repository
5. Render auto-detects render.yaml and configures everything
6. Click "Create Web Service"
7. Wait 10-15 minutes for build (installing PyTorch takes time)

### Step 3: Get Your Backend URL
After deployment, copy your backend URL:
https://your-app-name.onrender.com

Test it:
https://your-app-name.onrender.com/api/health

## Part 2: Deploy Frontend to Vercel

### Step 1: Create .env file
Create .env.local in your project root:
NEXT_PUBLIC_FLASK_URL=https://your-app-name.onrender.com

### Step 2: Commit environment config
git add .env.example
git commit -m "Add Vercel deployment config"
git push origin main

### Step 3: Deploy on Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." > "Project"
4. Import your repository
5. Configure:
   - Framework Preset: Next.js (auto-detected)
   - Root Directory: ./
   - Add Environment Variable:
     * Key: NEXT_PUBLIC_FLASK_URL
     * Value: https://your-app-name.onrender.com
6. Click "Deploy"
7. Wait 2-3 minutes

### Step 4: Access Your App
Your app is live at:
https://your-project.vercel.app

## Important Notes

### Render Free Tier:
- 750 hours/month (enough for most projects)
- Sleeps after 15 min inactivity
- First request after sleep: ~20-30 seconds
- Subsequent requests: <1 second

### Keeping Backend Awake (Optional):
Use a free service like UptimeRobot or Cron-job.org to ping your backend every 10 minutes:
https://your-app-name.onrender.com/api/health

### Environment Variables:
Render:
- PYTHON_VERSION: 3.12.8 (set in render.yaml)

Vercel:
- NEXT_PUBLIC_FLASK_URL: Your Render backend URL

## Troubleshooting

### Backend Build Fails:
- Check Render logs for errors
- Common issue: Out of memory during PyTorch install
- Solution: Wait and retry (Render sometimes has transient issues)

### Frontend Can''t Connect to Backend:
- Verify NEXT_PUBLIC_FLASK_URL is set correctly in Vercel
- Test backend health endpoint directly
- Check CORS settings in flask_api.py

### Backend Times Out:
- First request takes 30-60s (loading BERT model)
- This is normal, subsequent requests are fast
- Consider adding a loading state in your frontend

## Updating Your App

### Update Backend:
git push origin main
# Render auto-deploys on push

### Update Frontend:
git push origin main
# Vercel auto-deploys on push

## Monitoring

### Backend Logs:
https://dashboard.render.com > Your Service > Logs

### Frontend Logs:
https://vercel.com/dashboard > Your Project > Deployments > View Function Logs

## Cost Estimates

Free Tier (750 hours/month):
- Light usage (<100 requests/day): FREE
- Medium usage (500 requests/day): FREE
- Heavy usage (always on): FREE for first 750 hours

If you exceed 750 hours:
- Render Starter Plan: $7/month (512MB RAM)
- Vercel: Still FREE

