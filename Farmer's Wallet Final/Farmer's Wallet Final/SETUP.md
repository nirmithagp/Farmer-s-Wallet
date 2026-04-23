# 🌾 Farmer Advisory App - Local Setup Guide

Complete instructions for running the Farmer Advisory app locally on **macOS** and **Windows**.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.9+** installed ([Download Python](https://www.python.org/downloads/))
- **Git** installed ([Download Git](https://git-scm.com/))
- **pip** (comes with Python)
- A **Google API Key** for the Generative AI features ([Get API Key](https://makersuite.google.com/app/apikey))

### Verify Installation

**macOS/Linux:**
```bash
python3 --version
pip3 --version
git --version
```

**Windows (Command Prompt):**
```cmd
python --version
pip --version
git --version
```

---

## 🚀 Quick Start

### Step 1: Clone/Navigate to Project Directory

**macOS/Linux:**
```bash
cd ~/Desktop/Antigravity_1-cp
```

**Windows:**
```cmd
cd %USERPROFILE%\Desktop\Antigravity_1-cp
```

---

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

✅ You should see `(venv)` prefix in your terminal when activated.

---

### Step 3: Install Dependencies

```bash
# macOS/Linux
pip3 install -r code_1/requirements-clean.txt

# Windows
pip install -r code_1/requirements-clean.txt
```

**Expected output:** "Successfully installed..." with all packages listed

---

### Step 4: Train Loan Recommender Model (One-time)

The loan recommendation model needs to be trained before first use:

**macOS/Linux:**
```bash
python3 farmer_Loan_recommender-main/train_model.py
```

**Windows:**
```cmd
python farmer_Loan_recommender-main/train_model.py
```

✅ Success: You'll see `✅ Training complete!` and model files saved

---

### Step 5: Configure Environment Variables

Create a `.env` file in the project root with your Google API key:

**macOS/Linux:**
```bash
cat > .env << 'EOF'
GOOGLE_API_KEY=your_actual_google_api_key_here
EOF
```

**Windows (Command Prompt):**
```cmd
(
  echo GOOGLE_API_KEY=your_actual_google_api_key_here
) > .env
```

**Windows (PowerShell):**
```powershell
@'
GOOGLE_API_KEY=your_actual_google_api_key_here
'@ | Out-File -Encoding utf8 .env
```

⚠️ **Important:** Replace `your_actual_google_api_key_here` with your actual API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

### Step 6: Run the Application

**macOS/Linux:**
```bash
python3 code_1/app_new.py
```

**Windows:**
```cmd
python code_1/app_new.py
```

**Expected output:**
```
✓ All models and preprocessor loaded successfully!
 * Running on http://0.0.0.0:5001
 * Debug mode: on
```

---

## 🌐 Access the Application

Open your web browser and navigate to:
```
http://localhost:5001
```

You should see the **Farmer Advisory App** homepage.

---

## 📱 Available Pages

1. **Home** (`/`) - Dashboard
2. **Financial Advice** (`/financial-advice`) - AI-powered financial guidance
3. **Crop Price Prediction** (`/price-form`) - Predict crop prices
4. **Expense Tracker** (`/expense-form`) - Track farm expenses
5. **Budget Summary** (`/budget-summary-page`) - View budget analytics
6. **Loan Recommendations** (`/loan-recommendations`) - Get personalized loan suggestions

---

## 🛑 Stopping the Application

Press `Ctrl+C` in your terminal to stop the Flask development server.

---

## 🔄 Deactivate Virtual Environment

When done, deactivate the virtual environment:

**macOS/Linux:**
```bash
deactivate
```

**Windows:**
```cmd
deactivate
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError`

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Then reinstall
pip install -r code_1/requirements-clean.txt
```

---

### Issue: Port 5001 Already in Use

**Solution:** The app uses port 5001. If it's in use, modify `code_1/app_new.py`:

Change line:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

To:
```python
app.run(host='0.0.0.0', port=5002, debug=True)  # or any available port
```

---

### Issue: `GOOGLE_API_KEY not found`

**Solution:** Ensure `.env` file exists in project root with valid API key:
```bash
# macOS/Linux - verify
cat .env

# Windows - verify
type .env
```

---

### Issue: Loan Model Not Found

**Solution:** Train the model (requires internet for Google packages):
```bash
# macOS/Linux
python3 farmer_Loan_recommender-main/train_model.py

# Windows
python farmer_Loan_recommender-main/train_model.py
```

---

## 📁 Project Structure

```
Antigravity_1-cp/
├── code_1/
│   ├── app_new.py                 # Main Flask app
│   ├── crop_price.py              # Crop price prediction model
│   ├── exp_budget.py              # Expense tracker logic
│   ├── loan_recommender.py        # Loan recommendations
│   ├── requirements-clean.txt     # Python dependencies
│   ├── static/                    # CSS, JS, images
│   └── templates/                 # HTML pages
├── farmer_Loan_recommender-main/
│   ├── train_model.py             # Train loan model
│   ├── loan_model.pkl             # Trained XGBoost model
│   ├── label_encoders.pkl         # ML encoders
│   └── loan_recomm.ipynb          # Original notebook
├── .env                           # Configuration (API keys)
└── venv/                          # Virtual environment
```

---

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| google-generativeai | AI financial advice |
| scikit-learn | Machine learning |
| xgboost | Loan recommendation model |
| pandas | Data processing |
| python-dotenv | Environment variables |

---

## 🎯 Next Steps

1. **Explore the UI** - Try all pages and features
2. **Add real data** - Replace synthetic data with actual crop data
3. **Deploy** - Use Render, AWS, or Heroku for production
4. **Design updates** - Customize templates in `code_1/templates/`

---

## 📝 Notes

- **Debug Mode:** App runs in debug mode (auto-reloads on code changes)
- **CORS:** By default, only localhost can access the API
- **Database:** Expenses stored in `farmer_expenses.csv`
- **Models:** Crop price models loaded at startup from pickle files

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs in terminal output
3. Verify all model files exist in `code_1/` and `farmer_Loan_recommender-main/`

---

**Happy Farming! 🌾**
