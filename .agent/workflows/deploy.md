---
description: Deploy ScamGuard AI to Render and Vercel
---

# 🚀 Deployment Workflow for ScamGuard AI

This workflow guides you through deploying your ScamGuard AI application to production.

## Architecture
- **Backend (FastAPI)**: Deploy to Render
- **Frontend (React)**: Deploy to Vercel

---

## Step 1: Prepare for Deployment

### 1.1 Ensure all code is committed to Git
```bash
git status
git add .
git commit -m "Prepare for deployment"
```

### 1.2 Push to GitHub
```bash
git push origin main
```

If you haven't set up a GitHub repository yet, see `GITHUB_SETUP.md`.

---

## Step 2: Deploy Backend to Render

### 2.1 Sign up/Login to Render
1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### 2.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository (`Scam-Guard-AI`)
4. Click **"Connect"** next to your repository

### 2.3 Configure Service
Fill in the following settings:

- **Name**: `scamguard-api` (or your preferred name)
- **Region**: Oregon (US West) or closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty (use root)
- **Runtime**: `Python 3`
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: `Free`

### 2.4 Add Environment Variables (if needed)
No environment variables required for basic deployment.

### 2.5 Deploy!
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Your API will be deployed at: `https://scamguard-api.onrender.com`
4. **Copy this URL** - you'll need it for frontend deployment

### 2.6 Test Backend
Visit: `https://scamguard-api.onrender.com/docs` to see the API documentation.

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Sign up/Login to Vercel
1. Go to https://vercel.com
2. Sign up with GitHub (recommended)
3. Authorize Vercel to access your repositories

### 3.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Find and import your GitHub repository (`Scam-Guard-AI`)
3. Click **"Import"**

### 3.3 Configure Project
Fill in the following settings:

- **Framework Preset**: `Vite` (should auto-detect)
- **Root Directory**: `frontend` (click "Edit" next to Root Directory)
- **Build Command**: `npm run build` (default)
- **Output Directory**: `dist` (default)
- **Install Command**: `npm install` (default)

### 3.4 Add Environment Variables
Click **"Environment Variables"** and add:

- **Key**: `VITE_API_URL`
- **Value**: `https://scamguard-api.onrender.com` (your Render backend URL)
- **Environment**: All (Production, Preview, Development)

### 3.5 Deploy!
1. Click **"Deploy"**
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://scamguard-ai.vercel.app` (or similar)

### 3.6 Test Frontend
1. Visit your Vercel URL
2. Try analyzing a domain (e.g., `google.com`)
3. Check browser console for any errors

---

## Step 4: Update Backend CORS (CRITICAL!)

After deploying the frontend, you need to update the backend to allow requests from your Vercel domain.

### 4.1 Update `backend/main.py`
Change the CORS configuration (around line 35) from:
```python
allow_origins=["*"],  # In production, specify exact origins
```

To:
```python
allow_origins=[
    "http://localhost:5173",  # Local development
    "https://YOUR-VERCEL-URL.vercel.app",  # Replace with your actual Vercel URL
],
```

### 4.2 Commit and Push
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push origin main
```

### 4.3 Render Auto-Deploys
Render will automatically detect the changes and redeploy your backend (takes 2-3 minutes).

---

## Step 5: Verify Deployment

### 5.1 Test Complete Flow
1. Visit your Vercel frontend URL
2. Enter a domain to check (e.g., `google.com`, `example.com`)
3. Verify the analysis completes successfully
4. Check all results display correctly

### 5.2 Check for Issues
- **Backend Logs**: Render Dashboard → Logs tab
- **Frontend Errors**: Browser Console (F12)
- **API Response**: Network tab in browser DevTools

---

## 🎉 Deployment Complete!

Your app is now live at:
- **Frontend**: `https://YOUR-APP.vercel.app`
- **Backend API**: `https://scamguard-api.onrender.com`
- **API Docs**: `https://scamguard-api.onrender.com/docs`

---

## 📝 Important Notes

### Free Tier Limitations

**Render (Backend)**:
- ⚠️ **Spins down after 15 minutes of inactivity**
- 🕐 **First request after sleep takes ~30 seconds** (cold start)
- ✅ **750 free hours/month**
- 💰 Upgrade to $7/mo for always-on service

**Vercel (Frontend)**:
- ✅ **Always on, instant response**
- ✅ **100GB bandwidth/month**
- ✅ **Global CDN**
- ✅ **Automatic HTTPS**

### Auto Deployment
Both platforms support automatic deployment:
- **Push to `main`** → Deploys to production
- **Push to other branches** → Creates preview deployments

---

## 🐛 Troubleshooting

### "Failed to connect to backend"
1. Check that `VITE_API_URL` is set in Vercel
2. Verify backend is running (visit `/docs` endpoint)
3. Check CORS settings in `backend/main.py`
4. Check browser console for the actual error

### "Backend returns 500 error"
1. Check Render logs: Dashboard → Logs
2. Look for Python errors or missing dependencies
3. Verify `requirements.txt` is complete

### "Frontend shows blank page"
1. Check Vercel build logs
2. Run `npm run build` locally to test
3. Verify `vercel.json` exists in frontend folder

### "CORS error in browser"
1. Make sure your Vercel URL is in the `allow_origins` list
2. Commit and push the changes to trigger redeployment
3. Wait for Render to finish redeploying

---

## 🔄 Making Updates

### Update Frontend
```bash
# Make your changes
git add .
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys in 2-3 minutes
```

### Update Backend
```bash
# Make your changes
git add .
git commit -m "Update backend"
git push origin main
# Render auto-deploys in 3-5 minutes
```

---

## 🌐 Custom Domain (Optional)

### For Frontend (Vercel)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### For Backend (Render)
1. Go to Dashboard → Settings → Custom Domain
2. Add your API subdomain (e.g., `api.yourdomain.com`)
3. Update DNS records as instructed

---

**Need help?** Check the official documentation:
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
