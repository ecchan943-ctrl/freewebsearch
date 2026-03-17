@echo off
REM 🚀 Quick Deploy Script for DuckDuckGo Search API to Render

echo ============================================================
echo 🚀 DuckDuckGo Search API - Quick Deploy to Render
echo ============================================================
echo.

REM Step 1: Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: main.py not found!
    echo Please run this script from the render_ddg_search folder
    pause
    exit /b 1
)

echo ✅ Files found, continuing...
echo.

REM Step 2: Initialize Git repository (if needed)
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    echo.
) else (
    echo ✅ Git already initialized
    echo.
)

REM Step 3: Add all files
echo 📝 Adding all files to Git...
git add .
echo.

REM Step 4: Commit changes
echo 💾 Committing changes...
git commit -m "🚀 Deploy to Render - DuckDuckGo Search API"
echo.

REM Step 5: Check if remote is set
git remote -v | findstr "origin" >nul
if errorlevel 1 (
    echo 🔗 Setting up GitHub remote...
    echo.
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/ecchan943-ctrl/freewebsearch.git
    set /p REPO_URL="Repository URL: "
    git remote add origin %REPO_URL%
    echo.
) else (
    echo ✅ Remote already configured
    echo.
)

REM Step 6: Rename branch to main
echo 🌿 Setting default branch to 'main'...
git branch -M main
echo.

REM Step 7: Push to GitHub
echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  If prompted for credentials:
echo    - Use GitHub Personal Access Token instead of password
echo    - Or use: https://docs.github.com/en/authentication
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed! Please check:
    echo    1. GitHub credentials
    echo    2. Repository permissions
    echo    3. Repository URL
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ SUCCESS! Code pushed to GitHub
echo ============================================================
echo.
echo 📋 NEXT STEPS:
echo.
echo 1. Go to https://dashboard.render.com/
echo 2. Click "New +" → "Web Service"
echo 3. Connect your repository: freewebsearch
echo 4. Configure with these settings:
echo.
echo    Name: freewebsearch
echo    Region: Oregon
echo    Branch: main
echo    Build Command: pip install -r requirements.txt
echo    Start Command: python main.py
echo    Instance Type: Free
echo.
echo 5. Click "Create Web Service"
echo 6. Wait 2-3 minutes for deployment
echo.
echo 🎉 Your API will be at: https://freewebsearch-xxxx.onrender.com
echo ============================================================
echo.
pause
