# 🚀 Deployment Guide - ScamGuard AI

## Deployment Architecture

Your application needs **two separate deployments**:

1. **Backend (FastAPI)** → **Render** ✅ Recommended
2. **Frontend (React)** → **Vercel** or **Netlify** ✅ Recommended

---

## 📦 Option 1: Render + Vercel (Recommended)

### **Step 1: Deploy Backend to Render**

#### Prerequisites
- GitHub account
- Push your code to GitHub

#### Deployment Steps

1. **Create `runtime.txt` in backend folder:**
```bash
python-3.11
```

2. **Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: scamguard-api
    env: python
    region: oregon
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

3. **Go to [render.com](https://render.com)**
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

4. **Configure:**
   - **Name**: `scamguard-api`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your API will be at: `https://scamguard-api.onrender.com`

---

### **Step 2: Deploy Frontend to Vercel**

#### Prerequisites
- Vercel account (free)

#### Deployment Steps

1. **Update `frontend/.env` with your Render backend URL:**
```env
VITE_API_URL=https://scamguard-api.onrender.com
```

2. **Add `vercel.json` in frontend folder:**
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

3. **Go to [vercel.com](https://vercel.com)**
   - Sign up with GitHub
   - Click "Add New" → "Project"
   - Import your GitHub repository

4. **Configure:**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL` = `https://scamguard-api.onrender.com`

5. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be at: `https://scamguard-ai.vercel.app`

---

## 📦 Option 2: Netlify (Frontend Alternative)

### **Deploy Frontend to Netlify**

1. **Add `netlify.toml` in frontend folder:**
```toml
[build]
  base = "frontend"
  publish = "dist"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

2. **Go to [netlify.com](https://netlify.com)**
   - Sign up with GitHub
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub and select repository

3. **Configure:**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
   - **Environment Variables**:
     - `VITE_API_URL` = `https://scamguard-api.onrender.com`

4. **Deploy!**
   - Click "Deploy site"
   - Your app will be at: `https://scamguard-ai.netlify.app`

---

## 🔧 Backend CORS Update

**IMPORTANT**: After deploying, update your backend CORS settings!

Edit `backend/main.py`:

```python
# Update the CORS origins to include your deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://scamguard-ai.vercel.app",  # Add your Vercel URL
        "https://scamguard-ai.netlify.app", # Or your Netlify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-redeploy!

---

## 📋 Pre-Deployment Checklist

### Backend
- ✅ `requirements.txt` is up to date
- ✅ `runtime.txt` created (Python 3.11)
- ✅ CORS configured with production URLs
- ✅ Code pushed to GitHub

### Frontend
- ✅ `VITE_API_URL` environment variable set
- ✅ Build tested locally: `npm run build`
- ✅ `vercel.json` or `netlify.toml` added
- ✅ Code pushed to GitHub

---

## 🎯 Quick Deploy Commands

### Prepare Backend for Render
```bash
cd backend
echo "python-3.11" > runtime.txt
git add .
git commit -m "Add Render deployment config"
git push
```

### Prepare Frontend for Vercel
```bash
cd frontend
# Create vercel.json
echo '{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}' > vercel.json
git add .
git commit -m "Add Vercel deployment config"
git push
```

---

## 🆓 Free Tier Limits

### Render (Backend)
- ✅ 750 hours/month free
- ✅ Auto-sleep after 15 min inactivity
- ⚠️ First request after sleep takes ~30 seconds (cold start)
- ✅ Upgrade to $7/mo for always-on

### Vercel (Frontend)
- ✅ Unlimited bandwidth
- ✅ 100 deployments/day
- ✅ Auto SSL/HTTPS
- ✅ Global CDN

### Netlify (Frontend)
- ✅ 100 GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Auto SSL/HTTPS
- ✅ Instant cache invalidation

---

## 🔄 Auto-Deployment

Both platforms support **automatic deployment from Git**:

1. **Push to GitHub main branch** → **Auto-deploys to production**
2. **Push to other branches** → **Creates preview deployments**

---

## 🌐 Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your domain (e.g., `scamguard.com`)
3. Update DNS records as instructed

### Render
1. Go to Dashboard → Settings → Custom Domain
2. Add your domain (e.g., `api.scamguard.com`)
3. Update DNS records as instructed

---

## 🐛 Troubleshooting

### Backend Issues
- **Logs**: Check Render dashboard → Logs tab
- **Cold starts**: First request after sleep is slow (normal on free tier)
- **CORS errors**: Make sure frontend URL is in CORS whitelist

### Frontend Issues
- **API errors**: Check browser console, verify `VITE_API_URL`
- **404 on refresh**: Make sure `vercel.json` or `netlify.toml` is configured
- **Build fails**: Check build logs, run `npm run build` locally first

---

## 📞 Support

- **Render**: [render.com/docs](https://render.com/docs)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Netlify**: [docs.netlify.com](https://docs.netlify.com)

---

## 🎉 After Deployment

Your app will be live at:
- **Frontend**: `https://scamguard-ai.vercel.app` (or `.netlify.app`)
- **Backend API**: `https://scamguard-api.onrender.com`
- **API Docs**: `https://scamguard-api.onrender.com/docs`

**Test it thoroughly!**
1. Enter a domain in the frontend
2. Check analysis results
3. Verify all features work
4. Monitor logs for errors

---

**Need help?** Check the deployment platform docs linked above! 🚀
