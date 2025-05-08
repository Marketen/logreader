import os
import time
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from llama_cpp import Llama

# Configurable values
MODEL_PATH = "/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
LOG_DIR = "/logs"
SLEEP_INTERVAL = 60  # in seconds
MAX_OUTPUT_TOKENS = 300
MAX_CONTEXT_TOKENS = 4096
RESERVED_TOKENS = 64
MAX_INPUT_TOKENS = MAX_CONTEXT_TOKENS - RESERVED_TOKENS

def summarize_file(filename):
    try:
        # Load LLM in each process
        llm = Llama(model_path=MODEL_PATH, n_ctx=MAX_CONTEXT_TOKENS)

        log_path = os.path.join(LOG_DIR, filename)
        summary_path = os.path.join(LOG_DIR, f"summary_{filename}")

        # Skip if log is unchanged
        if os.path.exists(summary_path) and os.path.getmtime(summary_path) > os.path.getmtime(log_path):
            return f"⏩ {filename} skipped (unchanged)"

        with open(log_path, "r") as f:
            log_text = f.read()

        if not log_text.strip():
            return f"⚠️ {filename} skipped (empty)"

        # Tokenize + truncate
        tokens = llm.tokenize(log_text.encode("utf-8"))
        if len(tokens) > MAX_INPUT_TOKENS:
            tokens = tokens[:MAX_INPUT_TOKENS]
        truncated_log = llm.detokenize(tokens).decode("utf-8")

        # Prompt
        prompt = f"""
        [INST] Summarize the following system logs for a non-technical user.
        - Focus on entries marked as FATAL, CRITICAL, or ERROR.
        - Highlight any issues affecting stability or functionality.
        - Do not repeat the log lines verbatim.
        - Avoid starting the summary with “These logs...” or similar.
        - At the end of the summary, provide an overall system health score from 0 (very bad) to 10 (perfect), based on the severity of the issues detected.

        Logs:
        {truncated_log}
        [/INST]
        """
        result = llm(prompt, max_tokens=MAX_OUTPUT_TOKENS)
        summary = result["choices"][0]["text"].strip()

        with open(summary_path, "w") as out:
            out.write(summary)

        return f"✅ {filename} summarized"

    except Exception as e:
        return f"❌ {filename} error: {e}"

def summarize_logs():
    log_files = [
        f for f in os.listdir(LOG_DIR)
        if f.endswith(".log") and not f.startswith("summary_")
    ]

    if not log_files:
        print(f"[{datetime.now()}] No logs found.")
        return

    print(f"\n📥 [{datetime.now()}] Starting summarization for {len(log_files)} logs...\n")

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = executor.map(summarize_file, log_files)

    for res in results:
        print(res)

    print(f"\n📦 [{datetime.now()}] Summarization cycle complete.\n")

if __name__ == "__main__":
    while True:
        summarize_logs()
        time.sleep(SLEEP_INTERVAL)
