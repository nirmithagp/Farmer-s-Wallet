import random
from flask import Flask, request, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv
from markdown import markdown
from crop_price import predict_price
from exp_budget import FarmerExpenseTracker

tracker = FarmerExpenseTracker()

app = Flask(__name__)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

risk_term_mapping = {
    "low": "low risk, focused on safety and essential needs",
    "medium": "balanced risk, some growth and some stability",
    "high": "high risk, focused on expansion and profit",
    "conservative": "low risk, focused on safety and essential needs",
    "balanced": "balanced risk, some growth and some stability",
    "aggressive": "high risk, focused on expansion and profit"
}

investment_term_mapping = {
    "short": "less than 5 years",
    "medium": "between 5 and 10 years",
    "long": "more than 10 years"
}


@app.route('/')
def homepage():
    return render_template("home.html")

def get_financial_advice(risk_profile, investment_term, initial_amount, monthly_saving, language):
    try:
        initial_amount = float(initial_amount)
        monthly_saving = float(monthly_saving)

        # Language instruction
        # Language instruction
        if language == "kannada":
            lang_instruction = "Generate the entire financial advice in Kannada. Avoid English except for numbers."
        elif language == "hindi":
            lang_instruction = "Generate the entire financial advice in Hindi. Avoid English except for numbers."
        elif language == "tamil":
            lang_instruction = "Generate the entire financial advice in Tamil. Avoid English except for numbers."
        elif language == "telugu":
            lang_instruction = "Generate the entire financial advice in Telugu. Avoid English except for numbers."
        elif language == "malayalam":
            lang_instruction = "Generate the entire financial advice in Malayalam. Avoid English except for numbers."
        else:
            lang_instruction = "Generate the entire financial advice in English."

        prompt = f"""
You are a rural financial advisor for Indian farmers.

{lang_instruction}

Provide detailed financial advice based on:
- Risk Profile: {risk_profile} ({risk_term_mapping[risk_profile]})
- Term: {investment_term} ({investment_term_mapping[investment_term]})
- Initial Amount: ₹{initial_amount}
- Monthly Saving: ₹{monthly_saving}

Do NOT return JSON.
Return a full explanation, portfolio breakdown, tables, and reasoning in clean Markdown format.
"""

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        if hasattr(response, 'text') and response.text:
            return {"raw_output": response.text.strip()}
        else:
            print("[ERROR] No text in response:", response)
            return {"error": "No output from AI model. Check API key, quota, or network."}

    except Exception as e:
        print("[ERROR] Exception in get_financial_advice:", e)
        return {"error": str(e)}


@app.route("/financial-advice", methods=["GET", "POST"])
def index():
    formatted_output = None
    result = None

    if request.method == "POST":
        risk_profile = request.form.get("risk_profile")
        investment_term = request.form.get("investment_term")
        initial_amount = request.form.get("initial_amount")
        monthly_saving = request.form.get("monthly_saving")
        language = request.form.get("language")  # New

        # Normalize risk_profile to support both 'conservative' and 'low'
        if risk_profile == 'conservative':
            risk_profile = 'low'
        elif risk_profile == 'aggressive':
            risk_profile = 'high'
        elif risk_profile == 'balanced':
            risk_profile = 'medium'

        result = get_financial_advice(
            risk_profile,
            investment_term,
            initial_amount,
            monthly_saving,
            language
        )

        if "raw_output" in result:
            formatted_output = markdown(
                result["raw_output"],
                extensions=["extra", "tables", "sane_lists"]
            )

    return render_template("financial_combined.html", result=result, formatted_output=formatted_output)
########################################################################################################
@app.route("/price-form", methods=["GET", "POST"])
def price_form():
    result = None
    if request.method == "POST":
        try:
            commodity = request.form.get("commodity").lower()
            month = int(request.form.get("month"))
            year = int(request.form.get("year"))
            
            # Automatically set rainfall between 80-120cm (800-1200mm)
            rainfall = random.uniform(800, 1200)

            predicted_index, min_price, max_price, avg_price = predict_price(
                commodity, month, year, rainfall
            )
            result = f"{min_price} - {max_price}"
        except Exception as e:
            result = f"Error: {str(e)}"
            
    return render_template("crop_prediction.html", result=result)

@app.route("/predict-price", methods=["POST"])
def predict_crop_price_api():
    try:
        data = request.get_json()

        commodity = data.get("crop")
        month = int(data.get("month"))
        year = int(data.get("year"))
        rainfall = float(data.get("rainfall"))

        # Call your existing crop_price.py function
        predicted_index, min_price, max_price, avg_price = predict_price(
            commodity, month, year, rainfall
        )

        return {
            "predicted_index": predicted_index,
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": avg_price
        }

    except Exception as e:
        return {"error": str(e)}
###########################################################################################################

########################################################################################################
# ⭐ EXPENSE TRACKER ROUTES (New)
########################################################################################################

@app.route("/expense-form")
def expense_form():
    return render_template("expense_form.html", categories=tracker.get_categories())

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    amount = data.get("amount")
    date = data.get("date")

    result = tracker.add_expense(name, category, amount, date)
    return result

@app.route("/set-budget", methods=["POST"])
def set_budget():
    data = request.get_json()
    amount = data.get("amount") or data.get("budget")
    return tracker.set_budget(amount)

@app.route("/get-summary")
def get_summary():
    budget = tracker.get_budget()
    summary = tracker.get_summary(budget=budget)
    
    if "message" in summary:
        return {
            "budget": budget,
            "total_spent": 0,
            "remaining": budget,
            "category_breakdown": {}
        }
        
    return {
        "budget": budget,
        "total_spent": summary["total_spent"],
        "remaining": summary["remaining"],
        "category_breakdown": summary["by_category"]
    }

@app.route("/expense-chart-data")
def expense_chart_data():
    budget = tracker.get_budget()
    summary = tracker.get_summary(budget=budget)

    if "message" in summary:
        return {
            "labels": [],
            "values": [],
            "percentages": [],
            "budget": budget,
            "total_spent": 0,
            "remaining": budget
        }

    labels = list(summary["by_category"].keys())
    values = list(summary["by_category"].values())

    total_spent = summary["total_spent"]
    remaining = summary["remaining"] or 0

    # Avoid division by zero
    percentages = [
        (v / budget * 100) if budget > 0 else 0
        for v in values
    ]

    return {
        "labels": labels,
        "values": values,
        "percentages": percentages,
        "budget": budget,
        "total_spent": total_spent,
        "remaining": remaining
    }

@app.route("/get-categories")
def get_categories():
    return {"categories": tracker.get_categories()}

@app.route("/add-category", methods=["POST"])
def add_category():
    data = request.get_json()
    return tracker.add_category(data.get("category"))

@app.route("/budget-summary-page")
def budget_summary_page():
    return render_template("budget_summary.html")

########################################################################################################
# ⭐ LOAN RECOMMENDATION ROUTES (New)
########################################################################################################

@app.route("/loan-recommendations")
def loan_recommendations_page():
    return render_template("loan_recommendations.html")

@app.route("/get-loan-recommendations", methods=["POST"])
def get_loan_recommendations():
    try:
        from loan_recommender import get_loan_recommendations as get_recommendations
        
        data = request.get_json()
        crop_type = data.get("crop_type")
        land_type = data.get("land_type")
        location = data.get("location")
        land_size = data.get("land_size")
        income = data.get("income")
        
        recommendations = get_recommendations(
            crop_type, land_type, location, land_size, income
        )
        
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)