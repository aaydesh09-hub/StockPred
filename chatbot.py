import google.generativeai as genai
from financials import get_financials
import pandas as pd
import json
import os

# -----------------------------
# Gemini Configuration
# -----------------------------
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

tools = [{
    "name": "get_financials",
    "description": "Fetch stock financials, insider trades, sentiment and news",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {"type": "string"}
        },
        "required": ["symbol"]
    }
}]

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools={"function_declarations": tools}
)

# -----------------------------
# Save full financial dataset
# -----------------------------
def save_final_data(symbol, result):
    filename = "data/final_data.json"

    # Convert DataFrames
    for k, v in result.items():
        if isinstance(v, pd.DataFrame):
            result[k] = v.to_dict(orient="records")

    os.makedirs("data", exist_ok=True)

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                existing = json.load(f)
            except:
                existing = {}
    else:
        existing = {}

    existing[symbol] = result

    with open(filename, "w") as f:
        json.dump(existing, f, indent=4)

# -----------------------------
# Let Gemini format selectively
# -----------------------------
def format_response_with_llm(user_prompt: str, symbol: str, data: dict) -> str:
    """
    Uses Gemini to:
    - Decide which financials are relevant
    - Explain them in natural language
    - Format tables cleanly with line breaks
    """

    prompt = f"""
You are a financial assistant.

The user asked:
"{user_prompt}"

You are given FULL financial data for stock symbol {symbol}.
Only show the data the user explicitly asked for.
If they asked broadly (e.g. "all financials"), show everything.

Rules:
- Write in clear, natural language
- Use tables where appropriate
- Tables must be readable in plain text
- Add spacing and line breaks
- Do NOT mention data the user did not ask for

Financial Data (JSON):
{json.dumps(data, indent=2)}
"""

    response = model.generate_content(prompt)
    return response.text or "No relevant data found."

# -----------------------------
# MAIN CHATBOT FUNCTION
# -----------------------------
def run_chatbot(message: str) -> str:
    try:
        response = model.generate_content(message)

        for part in response.parts:
            fn = part.function_call
            if fn and fn.name == "get_financials":
                symbol = fn.args["symbol"].upper()

                # Fetch full dataset
                result = get_financials(symbol)

                # Persist full data
                save_final_data(symbol, result)

                # Let Gemini decide what to show
                return format_response_with_llm(
                    user_prompt=message,
                    symbol=symbol,
                    data=result
                )

        # No function call → normal LLM reply
        if response.text:
            return response.text

        return "I'm sorry, I couldn't generate a response."

    except Exception as e:
        return f"Error processing message: {str(e)}"
