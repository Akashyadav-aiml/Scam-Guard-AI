# 🚀 Quick Deployment Reference

## ✅ Recommended: Render + Vercel

### Why This Combination?
- **Best free tiers** for full-stack apps
- **Easy setup** - just connect GitHub
- **Auto-deploy** on every push
- **HTTPS included** automatically

---

## 📊 Platform Comparison

| Platform | Best For | Free Tier | Pros | Cons |
|----------|----------|-----------|------|------|
| **Render** | Backend (FastAPI) | 750 hrs/mo | Python native, auto-sleep | Cold starts (~30s) |
| **Vercel** | Frontend (React) | Unlimited | Fast CDN, great DX | Backend must be serverless |
| **Netlify** | Frontend (React) | 100GB/mo | Easy setup, forms | Bandwidth limits |
| **Railway** | Backend | $5 credit | No cold starts | Paid only now |

---

## 🎯 Deployment Workflow

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scamguard-ai.git
git push -u origin main
```

### Step 2: Deploy Backend (Render)
1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. New+ → Web Service
4. Select repository
5. Auto-detects `render.yaml` ✅
6. Deploy!

**Your API**: `https://scamguard-api.onrender.com`

### Step 3: Deploy Frontend (Vercel)
1. Go to [vercel.com](https://vercel.com)
2. New Project → Import Git
3. Select repository
4. Root Directory: `frontend`
5. Add Environment Variable:
   - `VITE_API_URL` = `https://scamguard-api.onrender.com`
6. Deploy!

**Your App**: `https://scamguard-ai.vercel.app`

---

## ⚡ Alternative: Netlify Frontend

Same as Vercel, but:
1. Go to [netlify.com](https://netlify.com)
2. Import from Git
3. Auto-detects `netlify.toml` ✅
4. Add same environment variable
5. Deploy!

**Your App**: `https://scamguard-ai.netlify.app`

---

## 🔧 Post-Deployment

### Update Backend CORS
Edit `backend/main.py`:

```python
allow_origins=[
    "http://localhost:5173",
    "https://scamguard-ai.vercel.app",  # Your actual URL
]
```

Commit + push → Auto-redeploys!

---

## 💰 Cost Breakdown

### Free Forever Plan
- **Render**: Free (with cold starts)
- **Vercel**: Free (unlimited)
- **Total**: **$0/month** ✅

### Recommended Paid Plan (No Cold Starts)
- **Render**: $7/month (always-on)
- **Vercel**: Free (still unlimited)
- **Total**: **$7/month** 

---

## 📝 Files Created for You

✅ `backend/runtime.txt` - Python version
✅ `render.yaml` - Render config (root)
✅ `frontend/vercel.json` - Vercel config
✅ `netlify.toml` - Netlify config (root)
✅ `DEPLOYMENT.md` - Full guide

**You're ready to deploy!** 🎉

---

## 🆘 Common Issues

### Backend
- **Cold starts slow**: Normal on free tier, upgrade to $7/mo
- **Build fails**: Check Python version (3.11)
- **Import errors**: Verify `requirements.txt`

### Frontend  
- **CORS errors**: Update backend with your frontend URL
- **404 on refresh**: Check `vercel.json` is present
- **Env vars not working**: Redeploy after adding variables

---

## 📞 Quick Links

- **Render Docs**: https://render.com/docs/web-services
- **Vercel Docs**: https://vercel.com/docs
- **Netlify Docs**: https://docs.netlify.com

---

**Ready to deploy?** Follow `DEPLOYMENT.md` for detailed steps! 🚀
