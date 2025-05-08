from flask import Flask, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    logs = []
    log_dir = "/logs"

    for file in os.listdir(log_dir):
        if file.endswith(".log") and not file.startswith("summary_"):
            log_path = os.path.join(log_dir, file)
            with open(log_path, "r") as f:
                content = f.read()

            summary_path = os.path.join(log_dir, f"summary_{file}")
            summary = ""
            summary_status = "Missing"
            if os.path.exists(summary_path):
                with open(summary_path, "r") as f:
                    summary = f.read()
                summary_status = "Available" if summary.strip() else "Empty"

            logs.append({
                "filename": file,
                "content": content,
                "summary": summary,
                "log_mtime": datetime.fromtimestamp(os.path.getmtime(log_path)).strftime('%Y-%m-%d %H:%M:%S'),
                "summary_mtime": datetime.fromtimestamp(os.path.getmtime(summary_path)).strftime('%Y-%m-%d %H:%M:%S') if os.path.exists(summary_path) else "N/A",
                "summary_status": summary_status
            })

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log Summaries</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1000px;
                margin: 40px auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .log-entry {
                margin-bottom: 40px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 20px;
            }
            h2 {
                color: #0066cc;
            }
            .meta-info {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .log-content, .summary-content {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 6px;
                white-space: pre-wrap;
                font-family: monospace;
                overflow-x: auto;
                display: none;
            }
            .summary-content {
                display: block;
            }
            .summary-label {
                font-weight: bold;
                margin-top: 10px;
                display: block;
                color: #555;
            }
            button.toggle {
                margin-top: 8px;
                padding: 5px 10px;
                font-size: 0.9em;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button.toggle:hover {
                background-color: #0056b3;
            }
        </style>
        <script>
            function toggleLog(id) {
                const elem = document.getElementById(id);
                elem.style.display = (elem.style.display === "block") ? "none" : "block";
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📋 Log Summaries</h1>
            {% for log in logs %}
                <div class="log-entry">
                    <h2>{{ log.filename }}</h2>
                    <div class="meta-info">
                        📁 Log modified: {{ log.log_mtime }}<br>
                        📄 Summary modified: {{ log.summary_mtime }}<br>
                        ✅ Summary status: <strong>{{ log.summary_status }}</strong>
                    </div>

                    <span class="summary-label">Summary:</span>
                    <div class="summary-content">
                        {{ log.summary if log.summary.strip() else "No summary available." }}
                    </div>

                    <button class="toggle" onclick="toggleLog('log-{{ loop.index }}')">Toggle Raw Log</button>
                    <div id="log-{{ loop.index }}" class="log-content">{{ log.content }}</div>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """

    return render_template_string(html_template, logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
