import os
import pandas as pd
import numpy as np
from openai import OpenAI

# 1. Initialize OpenAI client
client = OpenAI()

# 2. Load your historical stock data from CSV (in your Downloads folder)
csv_path = "/Users/divijmathur/Downloads/caci.csv"
df = pd.read_csv(csv_path)

# Rename "Close/Last" to "Close" for easier calculations
df.rename(columns={"Close/Last": "Close"}, inplace=True)

# Convert "Date" to datetime and sort
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)

# -- REMOVED: Moving Averages (MA5, MA20), RSI, and MACD calculations --

# 3. Prepare a textual summary of the last 30 rows (now only includes Date & Close)
recent_data = df.tail(30)
summary_lines = []

for idx, row in recent_data.iterrows():
    summary_lines.append(
        f"Date: {row['Date'].strftime('%Y-%m-%d')}, "
        f"Close: {row['Close']:.2f}"
    )

historical_summary = "\n".join(summary_lines)

# 4. Craft the user prompt (no references to MA, RSI, or MACD)
user_prompt = f"""
You are a financial analyst. Below is stock price data for the last 30 trading days:

Data:
{historical_summary}

Please structure your response using the following headings:

1. Current Observations
2. Historical Trend Changes
3. 1-Year Price Outlook
4. 3-Year Price Outlook
5. 5-Year Price Outlook
6. Conclusion and Hypothetical Long-Term Trading Approach

Under each heading, analyze how you might view this company's stock performance
and potential risks or catalysts in these longer time horizons.
"""

# 5. Call the ChatGPT API using the new format (use your desired model name)
completion = client.chat.completions.create(
    model="gpt-40-mini",  # or whatever model you wish to use
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
    ]
)

# 6. Print the response
response_content = completion.choices[0].message.content
print(response_content)
