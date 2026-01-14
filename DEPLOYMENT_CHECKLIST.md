# ✅ Pre-Deployment Checklist - ScamGuard AI

Complete this checklist before deploying to ensure smooth deployment.

## 📋 Backend (Render) Checklist

- [ ] **Code pushed to GitHub**
  ```bash
  git status
  git push origin main
  ```

- [x] **`backend/requirements.txt` exists and is complete**
  - Contains all necessary dependencies

- [x] **`runtime.txt` exists in project root**
  - Specifies Python version: `python-3.11.9`

- [x] **`render.yaml` configured correctly**
  - Build command: `cd backend && pip install -r requirements.txt`
  - Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

- [ ] **Test backend locally**
  ```bash
  cd backend
  python main.py
  # Visit http://localhost:8000/docs
  ```

---

## 📋 Frontend (Vercel) Checklist

- [x] **`frontend/vercel.json` exists**
  - Configured for SPA routing

- [ ] **Frontend builds successfully**
  ```bash
  cd frontend
  npm install
  npm run build
  ```

- [ ] **Environment variable prepared**
  - `VITE_API_URL` = Your Render backend URL
  - Will be set in Vercel dashboard during deployment

- [ ] **Code pushed to GitHub**
  ```bash
  git push origin main
  ```

---

## 🚀 Deployment Steps

### Step 1: Deploy Backend to Render

1. Go to https://render.com
2. Sign up/Login with GitHub
3. New + → Web Service
4. Connect repository
5. Configure:
   - Name: `scamguard-api`
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Free
6. Click "Create Web Service"
7. Wait 3-5 minutes
8. **Copy your backend URL**: `https://scamguard-api.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Sign up/Login with GitHub
3. Add New → Project
4. Import repository
5. Configure:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://scamguard-api.onrender.com` (your Render URL)
7. Click "Deploy"
8. Wait 2-3 minutes
9. **Copy your frontend URL**: `https://scamguard-ai.vercel.app`

### Step 3: Update Backend CORS

1. Edit `backend/main.py` line 35
2. Change from:
   ```python
   allow_origins=["*"],
   ```
   To:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "https://YOUR-VERCEL-URL.vercel.app",  # Replace with actual URL
   ],
   ```
3. Commit and push:
   ```bash
   git add backend/main.py
   git commit -m "Update CORS for production"
   git push origin main
   ```
4. Render will auto-redeploy (2-3 minutes)

### Step 4: Test Everything

- [ ] Visit frontend URL
- [ ] Test domain analysis (e.g., `google.com`)
- [ ] Check results display correctly
- [ ] Open browser console - no errors
- [ ] Test on mobile device

---

## 🎉 Deployment Complete!

Your application is now live:
- **Frontend**: https://YOUR-APP.vercel.app
- **Backend API**: https://scamguard-api.onrender.com
- **API Docs**: https://scamguard-api.onrender.com/docs

---

## ⚠️ Important Notes

### Render Free Tier
- Backend **spins down after 15 min** of inactivity
- **First request after sleep = ~30 seconds** (cold start)
- This is normal on free tier!

### Vercel Free Tier
- Frontend is **always on**
- No cold starts
- Fast global CDN

---

## 🔄 Making Updates

After deployment, any push to `main` branch will:
- Auto-deploy to Render (backend) in 3-5 min
- Auto-deploy to Vercel (frontend) in 2-3 min

---

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check Render logs
# Render Dashboard → Your Service → Logs
```

### Frontend Issues
```bash
# Check browser console (F12)
# Vercel Dashboard → Deployments → Latest → View Build Logs
```

### CORS Errors
- Ensure Vercel URL is in `allow_origins` list
- Redeploy backend after updating CORS

---

**For detailed instructions, see**: `.agent/workflows/deploy.md`
