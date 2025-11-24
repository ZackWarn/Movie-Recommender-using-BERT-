# Heroku Deployment Guide

## Files Created:
 Procfile - Heroku startup command
 runtime.txt - Python version
 requirements.txt - Production dependencies (optimized)
 requirements-dev.txt - Development dependencies (backup)
 .slugignore - Files to exclude from deployment
 .gitattributes - Git LFS configuration for *.pkl files

## Next Steps:

### 1. Install Heroku CLI
Download from: https://devcli.heroku.com/

### 2. Login to Heroku
heroku login

### 3. Create Heroku App
heroku create your-movie-recommender-app

### 4. Apply Student Credit
Go to: https://dashboard.heroku.com/account/billing
Add GitHub Student Pack credit

### 5. Set Dyno Type
heroku ps:type eco

### 6. Set Environment Variables (if needed)
heroku config:set RAPIDAPI_IMDB_KEY=your_key_here

### 7. Commit and Deploy
git add .
git commit -m "Add Heroku deployment configuration"
git push heroku main

### 8. Scale Web Dyno
heroku ps:scale web=1

### 9. View Logs
heroku logs --tail

### 10. Open App
heroku open

## Important Notes:
- First deployment takes 10-15 minutes (installing PyTorch)
- First request takes 30-60 seconds (loading BERT model)
- Memory usage: ~570MB (fits in 512MB Eco dyno)
- If memory issues occur, upgrade to Standard-1X

## Test Locally First:
gunicorn flask_api:app --bind 0.0.0.0:5000 --timeout 120

