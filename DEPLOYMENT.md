# GitHub Deployment Guide

> Step-by-step guide to deploy the Policy Simulation Assistant to GitHub

## 🚀 Quick Start

This guide will help you deploy your Policy Simulation Assistant project to GitHub and set it up for development and production use.

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] GitHub account
- [ ] Git installed on your machine
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed (for frontend development)
- [ ] Basic familiarity with command line

## 🔧 Step 1: Initialize Git Repository

### 1.1 Navigate to Project Directory
```bash
cd /Users/dylanlindert/Desktop/Tutai/ADAPT/project_root
```

### 1.2 Initialize Git Repository
```bash
git init
```

### 1.3 Add All Files to Git
```bash
git add .
```

### 1.4 Create Initial Commit
```bash
git commit -m "Initial commit: Policy Simulation Assistant MVP

- Complete 5-feature MVP implementation
- Interactive demo server with all features
- Streamlit EDA dashboard
- Comprehensive documentation
- ADAPT framework analysis artifacts"
```

## 🌐 Step 2: Create GitHub Repository

### 2.1 Create New Repository on GitHub
1. Go to [GitHub.com](https://github.com)
2. Click the **"+"** button in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `policy-simulation-assistant`
   - **Description**: `GenAI-powered healthcare policy simulation tool for policy makers, ministries, and NGOs`
   - **Visibility**: Choose **Public** or **Private**
   - **Initialize**: Leave unchecked (we already have files)
5. Click **"Create repository"**

### 2.2 Connect Local Repository to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/policy-simulation-assistant.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## 📁 Step 3: Verify Repository Structure

Your GitHub repository should now contain:

```
policy-simulation-assistant/
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── DEPLOYMENT.md
├── comprehensive_demo_server.py
├── full_interactive_demo.html
├── streamlit_eda_dashboard.py
├── requirements.txt
├── requirements_streamlit.txt
├── package.json
├── adapt_context/
│   ├── analysis_summary.md
│   ├── artifacts/
│   └── data/
├── docs/
│   ├── features/
│   ├── PROJECT_BRIEF.md
│   └── scope.md
└── src/
    ├── backend/
    └── frontend/
```

## 🛠️ Step 4: Set Up Development Environment

### 4.1 Clone Repository (for other developers)
```bash
git clone https://github.com/YOUR_USERNAME/policy-simulation-assistant.git
cd policy-simulation-assistant
```

### 4.2 Install Python Dependencies
```bash
# Install main requirements
pip install -r requirements.txt

# Install Streamlit requirements (optional)
pip install -r requirements_streamlit.txt
```

### 4.3 Install Frontend Dependencies (Optional)
```bash
cd src/frontend
npm install
cd ../..
```

### 4.4 Set Up Environment Variables
```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Add your OpenAI API key and other settings
```

## 🚀 Step 5: Run the Application

### 5.1 Start the Main Demo Server
```bash
python comprehensive_demo_server.py
```

**Access Points:**
- **Main Demo**: http://localhost:8005/full
- **API Documentation**: http://localhost:8005/docs
- **Health Check**: http://localhost:8005/health

### 5.2 Start Streamlit Dashboard (Optional)
```bash
streamlit run streamlit_eda_dashboard.py
```

**Access Point:**
- **EDA Dashboard**: http://localhost:8503

## 📝 Step 6: Update README.md

### 6.1 Update Repository URLs
Edit the `README.md` file to update any placeholder URLs:

```markdown
# Replace this line:
git clone <repository-url>

# With your actual repository URL:
git clone https://github.com/YOUR_USERNAME/policy-simulation-assistant.git
```

### 6.2 Commit and Push Changes
```bash
git add README.md
git commit -m "Update README with correct repository URLs"
git push
```

## 🔄 Step 7: Set Up Continuous Development

### 7.1 Create Development Branch
```bash
git checkout -b develop
git push -u origin develop
```

### 7.2 Set Up Branch Protection (Optional)
1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Add rule for `main` branch
4. Enable "Require pull request reviews before merging"

### 7.3 Create Feature Branches
```bash
# For new features
git checkout -b feature/new-feature-name
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature-name
```

## 🌍 Step 8: Deploy to Production (Optional)

### 8.1 GitHub Pages (Static Frontend)
1. Go to repository **Settings** → **Pages**
2. Select **Deploy from a branch**
3. Choose `main` branch and `/` folder
4. Your site will be available at: `https://YOUR_USERNAME.github.io/policy-simulation-assistant`

### 8.2 Cloud Deployment Options

**Heroku:**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python comprehensive_demo_server.py" > Procfile
# Deploy
heroku create your-app-name
git push heroku main
```

**Railway:**
```bash
# Install Railway CLI
# Login and deploy
railway login
railway init
railway up
```

**Render:**
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python comprehensive_demo_server.py`

## 📊 Step 9: Set Up Monitoring and Analytics

### 9.1 GitHub Insights
- **Insights** → **Traffic**: View repository traffic
- **Insights** → **Contributors**: Track contributions
- **Insights** → **Community**: Community standards

### 9.2 Add Badges to README
```markdown
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/policy-simulation-assistant)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/policy-simulation-assistant)
![GitHub pull requests](https://img.shields.io/github/issues-pr/YOUR_USERNAME/policy-simulation-assistant)
```

## 🔒 Step 10: Security and Best Practices

### 10.1 Add Security Files
```bash
# Create SECURITY.md
echo "# Security Policy

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability
Please report security vulnerabilities to [your-email@domain.com]
" > SECURITY.md

# Create CONTRIBUTING.md
echo "# Contributing

## How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
" > CONTRIBUTING.md
```

### 10.2 Add License
```bash
# Create MIT License
echo "MIT License

Copyright (c) 2024 Policy Simulation Assistant

Permission is hereby granted..." > LICENSE
```

## 🎯 Step 11: Final Verification

### 11.1 Test All Features
1. **Feature 1**: Policy Simulation Engine
2. **Feature 2**: Health Benchmark Dashboard  
3. **Feature 3**: Narrative Insight Generator
4. **Feature 4**: Data Quality Assurance
5. **Feature 5**: Advanced Analytics & Reporting

### 11.2 Verify Documentation
- [ ] README.md is complete and accurate
- [ ] ARCHITECTURE.md covers all technical details
- [ ] DEPLOYMENT.md provides clear setup instructions
- [ ] All links work correctly

### 11.3 Test Repository Access
```bash
# Test cloning from a different location
cd /tmp
git clone https://github.com/YOUR_USERNAME/policy-simulation-assistant.git
cd policy-simulation-assistant
python comprehensive_demo_server.py
```

## 🎉 Success!

Your Policy Simulation Assistant is now successfully deployed to GitHub! 

### Next Steps:
1. **Share the repository** with stakeholders
2. **Set up issue tracking** for bug reports and feature requests
3. **Create releases** for version management
4. **Consider CI/CD** for automated testing and deployment
5. **Add collaborators** if working with a team

### Repository URLs:
- **Repository**: `https://github.com/YOUR_USERNAME/policy-simulation-assistant`
- **Issues**: `https://github.com/YOUR_USERNAME/policy-simulation-assistant/issues`
- **Releases**: `https://github.com/YOUR_USERNAME/policy-simulation-assistant/releases`

---

## 🆘 Troubleshooting

### Common Issues:

**Git Authentication:**
```bash
# If you get authentication errors, set up SSH keys or use personal access tokens
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/policy-simulation-assistant.git
```

**Python Dependencies:**
```bash
# If you get import errors, ensure all dependencies are installed
pip install -r requirements.txt
pip install -r requirements_streamlit.txt
```

**Port Conflicts:**
```bash
# If ports are in use, change them in the server files
# Edit comprehensive_demo_server.py and change the port number
```

**File Permissions:**
```bash
# Ensure files are executable
chmod +x comprehensive_demo_server.py
chmod +x streamlit_eda_dashboard.py
```

---

**🎯 Your Policy Simulation Assistant is ready for the world!**
