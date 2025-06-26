from flask import Flask, request, render_template, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="2a654408-5e68-4ad6-9fe9-4a7962cc433d",
    base_url="https://api.sambanova.ai/v1"
)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.form['code']

    prompt = f"""
You are a concise Python 3 bug fixer. Your task is to analyze the given Python code, identify errors, and provide the corrected code. Respond in the following format:

**❌ Error:** [Show error code/names]

**✅ Corrected Code:**
```python
[corrected code here]
```

**💡 Reason:** [Very brief reason for the fix, 1-2 sentences maximum. If there's an alternative scenario (like using a variable), add a one-line note in parentheses.]

Do not explain unless necessary. Keep the response extremely short. If the code has no errors, simply output the code in a code block with no explanation.
{code}
"""

    response = client.chat.completions.create(
        model="DeepSeek-V3-0324",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that finds and explains bugs in Python code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        top_p=0.9
    )

    ai_markdown = response.choices[0].message.content.strip()

    return jsonify({"result": ai_markdown})

if __name__ == "__main__":
    app.run(debug=True)
