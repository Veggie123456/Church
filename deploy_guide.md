# 🚀 **Bot Deployment Guide**

## **Option 1: Railway (Recommended)**

### **Step 1: Prepare Your Code**
1. **Create GitHub repository:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it "crypto-church-bot"
   - Make it public or private

2. **Upload your files:**
   - Upload all your bot files to the repository
   - Make sure `main.py`, `requirements.txt`, `Procfile`, `runtime.txt` are included

### **Step 2: Deploy on Railway**
1. **Go to:** [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will auto-detect Python and deploy**

### **Step 3: Set Environment Variables**
In Railway dashboard:
1. **Go to your project**
2. **Click "Variables" tab**
3. **Add these variables:**
   ```
   BOT_TOKEN=7927515576:AAHAR-Hswwx3s_IsMq1IRu_xT1aKaBk06bU
   ALLOWED_GROUP_ID=-1003072381490
   ```

### **Step 4: Deploy**
- **Click "Deploy"**
- **Your bot will be live 24/7!**

---

## **Option 2: Heroku**

### **Step 1: Install Heroku CLI**
- Download from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### **Step 2: Deploy**
```bash
# Login to Heroku
heroku login

# Create app
heroku create crypto-church-bot

# Set environment variables
heroku config:set BOT_TOKEN=7927515576:AAHAR-Hswwx3s_IsMq1IRu_xT1aKaBk06bU
heroku config:set ALLOWED_GROUP_ID=-1003072381490

# Deploy
git add .
git commit -m "Deploy bot"
git push heroku main

# Scale worker
heroku ps:scale worker=1
```

---

## **Option 3: PythonAnywhere**

### **Step 1: Create Account**
- Go to [pythonanywhere.com](https://pythonanywhere.com)
- Sign up for free account

### **Step 2: Upload Files**
1. **Go to "Files" tab**
2. **Upload all your bot files**
3. **Create folder structure**

### **Step 3: Set Up Task**
1. **Go to "Tasks" tab**
2. **Create new task:**
   - **Command:** `python3.10 /home/yourusername/crypto-church-bot/main.py`
   - **Schedule:** Always (keeps running)

### **Step 4: Set Environment Variables**
- **Go to "Consoles" tab**
- **Create new console**
- **Run:** `export BOT_TOKEN="7927515576:AAHAR-Hswwx3s_IsMq1IRu_xT1aKaBk06bU"`
- **Run:** `export ALLOWED_GROUP_ID="-1003072381490"`

---

## **✅ After Deployment:**

Your bot will be **live 24/7** and will:
- ✅ **Respond to commands** in your Telegram group
- ✅ **Send random blessings** every 2.5 hours
- ✅ **Track prayers** and maintain leaderboard
- ✅ **Survive restarts** and server maintenance

## **🔧 Monitoring:**
- **Railway/Heroku:** Check logs in dashboard
- **PythonAnywhere:** Check "Tasks" tab for status
- **All platforms:** Bot will restart automatically if it crashes

**Choose the option that works best for you!** 🙏✝️
