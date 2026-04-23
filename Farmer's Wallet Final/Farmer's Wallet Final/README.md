# 🌾 Farmer Advisory App

An intelligent Flask-based application providing farmers with AI-powered financial advice, crop price predictions, expense tracking, and personalized loan recommendations.

---

## ✨ Features

### 🤖 AI Financial Advisor
- Personalized financial planning based on risk profile and investment term
- Multi-language support (English & Kannada)
- AI-generated investment portfolios using Google Gemini API
- Tailored recommendations for farm investments

### 📈 Crop Price Prediction
- Machine Learning-based price forecasting
- Support for: Jowar, Wheat, Cotton, Sugarcane, Bajra
- Historical data analysis
- Monthly and yearly price trends

### 💰 Expense Tracker
- Track daily farm expenses
- Categorize spending by type
- Budget planning and monitoring
- Visual analytics and reports
- CSV export for record-keeping

### 🏦 Loan Recommender
- XGBoost-based recommendation engine
- Analyzes: crop type, land type, location, land size, income
- Provides top 3 personalized loan options
- Government scheme integration
- Fallback rule-based recommendations

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Flask 3.1 |
| **ML/AI** | XGBoost, scikit-learn, Google Generative AI |
| **Data** | Pandas, NumPy |
| **Environment** | Python 3.9+ |

---

## 📁 Project Structure

```
Antigravity_1-cp/
├── code_1/                              # Main application
│   ├── app_new.py                       # Flask app entry point
│   ├── crop_price.py                    # Crop price prediction models
│   ├── exp_budget.py                    # Expense tracker
│   ├── loan_recommender.py              # Loan recommendations
│   ├── requirements-clean.txt           # Python dependencies
│   ├── static/
│   │   ├── css/main.css                # Styling
│   │   ├── js/main.js                  # Client-side logic
│   │   └── images/                     # Assets
│   └── templates/
│       ├── home.html                   # Homepage
│       ├── financial_combined.html      # Financial advisor UI
│       ├── crop_prediction.html         # Price prediction UI
│       ├── expense_form.html            # Expense tracker UI
│       ├── budget_summary.html          # Budget dashboard
│       └── loan_recommendations.html    # Loan suggestions UI
├── farmer_Loan_recommender-main/        # Loan recommendation system
│   ├── train_model.py                  # Model training script
│   ├── loan_model.pkl                  # Trained XGBoost model
│   ├── label_encoders.pkl              # Feature encoders
│   ├── loan_recomm.ipynb               # Original notebook
│   └── project_dataset.xls             # Training data
├── .env                                 # Environment variables (API keys)
├── SETUP.md                             # Detailed setup instructions
├── README.md                            # This file
└── venv/                                # Virtual environment
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- Git
- Google API Key ([Get Here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone/Navigate to project:**
   ```bash
   cd ~/Desktop/Antigravity_1-cp
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r code_1/requirements-clean.txt
   ```

4. **Train loan model (first time only):**
   ```bash
   python3 farmer_Loan_recommender-main/train_model.py
   ```

5. **Set up environment variables:**
   ```bash
   # Create .env file with:
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

6. **Run application:**
   ```bash
   python3 code_1/app_new.py
   ```

7. **Open in browser:**
   ```
   http://localhost:5001
   ```

---

## 📝 API Endpoints

### Financial Advice
- **POST** `/financial-advice` - Get AI-powered financial recommendations
- **GET** `/financial-advice` - Display form

### Crop Price Prediction
- **POST** `/predict-price` - JSON API for price prediction
- **GET/POST** `/price-form` - Web form interface

### Expense Tracking
- **GET** `/expense-form` - View expense form
- **POST** `/add-expense` - Add new expense
- **POST** `/set-budget` - Set budget limit
- **GET** `/get-summary` - Get expense summary
- **GET** `/expense-chart-data` - Get visualization data
- **POST** `/add-category` - Add expense category
- **GET** `/get-categories` - List categories
- **GET** `/budget-summary-page` - View dashboard

### Loan Recommendations
- **GET** `/loan-recommendations` - Display recommendations form
- **POST** `/get-loan-recommendations` - Get personalized loans

---

## 📊 Data Files

| File | Purpose |
|------|---------|
| `farmer_expenses.csv` | Expense records |
| `farmer_categories.json` | Expense categories |
| `jmodel.pkl` | Jowar price model |
| `wmodel.pkl` | Wheat price model |
| `cmodel.pkl` | Cotton price model |
| `smodel.pkl` | Sugarcane price model |
| `bmodel.pkl` | Bajra price model |
| `preprocessor.pkl` | Feature preprocessor |
| `loan_model.pkl` | XGBoost loan classifier |
| `label_encoders.pkl` | ML feature encoders |

---

## 🔧 Configuration

### Environment Variables (`.env`)
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Flask Settings (`code_1/app_new.py`)
- **Host:** 0.0.0.0 (accessible from any network interface)
- **Port:** 5001 (configurable)
- **Debug:** True (development mode)

---

## 📚 Model Details

### Crop Price Models
- **Type:** Gradient Boosting (XGBoost)
- **Features:** Month, Year, Rainfall
- **Output:** Price index, min/max range, average price
- **Crops:** Jowar, Wheat, Cotton, Sugarcane, Bajra

### Loan Recommender
- **Type:** XGBoost Classifier
- **Features:** Land Type, Land Size, Location, Crop Type, Income
- **Output:** Top 3 recommended loan schemes with probabilities
- **Fallback:** Rule-based recommendations by income level

---

## 🐛 Troubleshooting

### Port Already in Use
Modify `app_new.py` line:
```python
app.run(host='0.0.0.0', port=5002, debug=True)
```

### Missing API Key
Ensure `.env` file exists in project root with valid Google API key.

### Model Not Loading
Verify model files exist in `code_1/` directory:
- `jmodel.pkl`, `wmodel.pkl`, `cmodel.pkl`, `smodel.pkl`, `bmodel.pkl`
- `preprocessor.pkl`

### Loan Model Not Found
Run training script:
```bash
python3 farmer_Loan_recommender-main/train_model.py
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `debug=False` in Flask
- [ ] Use production WSGI server (Gunicorn, Waitress)
- [ ] Set up HTTPS/SSL certificates
- [ ] Secure API keys in production environment
- [ ] Set up database (SQLite → PostgreSQL)
- [ ] Configure CORS for frontend domains
- [ ] Add rate limiting
- [ ] Set up monitoring and logging

### Deploy to Render
```bash
# Add Procfile
echo "web: gunicorn code_1.app_new:app" > Procfile

# Add runtime.txt
echo "python-3.11.5" > runtime.txt

# Deploy
git push heroku main
```

---

## 📖 Documentation

See `SETUP.md` for detailed platform-specific installation instructions.

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes and test
3. Commit with clear messages
4. Submit pull request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues or questions, please:
1. Check `SETUP.md` troubleshooting section
2. Review application logs
3. Verify all model files are present

---

## 🎯 Future Enhancements

- [ ] Multi-language UI
- [ ] Mobile app (React Native)
- [ ] Real-time weather integration
- [ ] Live crop market data API
- [ ] Advanced analytics dashboard
- [ ] Blockchain-based transactions
- [ ] IoT sensor integration
- [ ] SMS notifications
- [ ] WhatsApp bot integration
- [ ] Offline mode support

---

**Last Updated:** November 20, 2025  
**Version:** 1.0.0

---

**Happy Farming! 🌾**
