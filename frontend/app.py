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
        <title>DAppNode Log Summaries</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 1200px;
                margin: 30px auto;
                background-color: #fff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
            }
            .search-box {
                width: 100%;
                margin-bottom: 20px;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                font-size: 1em;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            .log-entry {
                border-bottom: 1px solid #e0e0e0;
                padding: 15px 0;
            }
            .log-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .log-name {
                font-weight: bold;
                color: #007bff;
                font-size: 1.1em;
            }
            .log-name:hover {
                text-decoration: underline;
            }
            .meta-info {
                font-size: 0.9em;
                color: #555;
            }
            .summary-content,
            .log-content {
                background-color: #f1f1f1;
                padding: 10px;
                margin-top: 10px;
                border-radius: 5px;
                font-family: monospace;
                white-space: pre-wrap;
                display: none;
            }
            .toggle-button {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.85em;
            }
            .toggle-button:hover {
                background-color: #218838;
            }
            .status {
                font-size: 0.85em;
            }
        </style>
        <script>
            function toggleSection(id) {
                const section = document.getElementById(id);
                if (section.style.display === "none" || section.style.display === "") {
                    section.style.display = "block";
                } else {
                    section.style.display = "none";
                }
            }

            function filterLogs() {
                const input = document.getElementById("searchInput").value.toLowerCase();
                const entries = document.getElementsByClassName("log-entry");

                for (let entry of entries) {
                    const name = entry.getAttribute("data-name").toLowerCase();
                    entry.style.display = name.includes(input) ? "" : "none";
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📋 DAppNode Log Summaries</h1>

            <div class="search-box">
                <input type="text" id="searchInput" onkeyup="filterLogs()" placeholder="Search logs by name...">
            </div>

            {% for log in logs %}
            <div class="log-entry" data-name="{{ log.filename }}">
                <div class="log-header">
                    <div class="log-name" title="{{ log.filename }}">{{ log.filename[:50] }}{% if log.filename|length > 50 %}...{% endif %}</div>
                    <button class="toggle-button" onclick="toggleSection('log-{{ loop.index }}')">📝 Toggle Details</button>
                </div>
                <div class="meta-info">
                    📁 Modified: {{ log.log_mtime }} |
                    📄 Summary: {{ log.summary_mtime }} |
                    ✅ Status: <strong>{{ log.summary_status }}</strong>
                </div>

                <div class="summary-content" style="display: block;">
                    <strong>🧠 Summary:</strong><br>
                    {{ log.summary if log.summary.strip() else "No summary available." }}
                </div>

                <div id="log-{{ loop.index }}" class="log-content">
                    <strong>📄 Full Log:</strong><br>
                    {{ log.content }}
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """

    return render_template_string(html_template, logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8070)
