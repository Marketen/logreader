from llama_cpp import Llama
import os

# Load the model
llm = Llama(model_path="/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# Directory containing logs
log_dir = "/logs"

# Process each log file
for filename in os.listdir(log_dir):
    if filename.endswith(".log") and not filename.startswith("summary_"):
        log_path = os.path.join(log_dir, filename)

        with open(log_path, "r") as f:
            log_text = f.read()

        if not log_text.strip():
            continue

        # Format prompt
        prompt = f"<s>[INST] Summarize these logs for a non-technical user:\n{log_text}\n[/INST]"

        # Run model
        result = llm(prompt, max_tokens=300)
        summary = result["choices"][0]["text"].strip()

        # Save summary
        summary_file = os.path.join(log_dir, f"summary_{filename}")
        with open(summary_file, "w") as f:
            f.write(summary)

        print(f"Summarized {filename}")
