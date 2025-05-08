from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def home():
    summaries = {}
    for file in os.listdir('/logs'):
        if file.startswith('summary_'):
            with open(f"/logs/{file}", "r") as f:
                summaries[file] = f.read()
    html = "<h1>Log Summaries</h1>" + "".join(
        f"<h2>{k}</h2><pre>{v}</pre>" for k, v in summaries.items()
    )
    return render_template_string(html)

app.run(host='0.0.0.0', port=8080)
