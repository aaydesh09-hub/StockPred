from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from  financials import get_financials
from  storage import save_result

app = Flask(__name__)

tools = [{
    "name": "get_financials",
    "description": "Fetch stock financial data",
    "parameters":
        {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string"

                }
            },
            "required": ["symbol"]
        }
    }
    ]


genai.configure(api_key="AIzaSyB_A6Kd0TSLAe84cMih9eIgHp3HzkROrR0")
model = genai.GenerativeModel(model_name = "gemini-2.5-flash", tools = {"function_declarations": tools})
@app.route("/")
def home():
    return render_template("home.html")
if(__name__ == "__main__"):
    app.run(debug=True)