from llama_cpp import Llama
import os

# Load the model with 4096-token context window
llm = Llama(
    model_path="/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    n_ctx=4096
)

# Directory for logs
log_dir = "/logs"

# Reserve some tokens for prompt wrappers like [INST]...[/INST]
RESERVED_TOKENS = 64
MAX_INPUT_TOKENS = 4096 - RESERVED_TOKENS

def truncate_to_fit(text, max_tokens):
    """Truncate text so it fits within max token limit."""
    tokens = llm.tokenize(text.encode("utf-8"))
    if len(tokens) > max_tokens:
        print(f"⚠️ Truncating input: {len(tokens)} tokens -> {max_tokens}")
        tokens = tokens[:max_tokens]
    else:
        print(f"✅ Input fits within token limit: {len(tokens)} tokens")
    return llm.detokenize(tokens).decode("utf-8")

def summarize_logs():
    print("📥 Starting log summarization...\n")
    for filename in os.listdir(log_dir):
        if filename.endswith(".log") and not filename.startswith("summary_"):
            log_path = os.path.join(log_dir, filename)

            with open(log_path, "r") as f:
                log_text = f.read()

            if not log_text.strip():
                print(f"⚠️ Skipping empty log: {filename}")
                continue

            try:
                truncated_log = truncate_to_fit(log_text, MAX_INPUT_TOKENS)
                prompt = f"[INST] Summarize these logs for a non-technical user:\n{truncated_log}\n[/INST]"

                print(f"🧠 Running model on: {filename}")
                result = llm(prompt, max_tokens=300)
                summary = result["choices"][0]["text"].strip()

                if not summary:
                    print(f"⚠️ Empty summary returned for: {filename}")
                    continue

                summary_file = os.path.join(log_dir, f"summary_{filename}")
                with open(summary_file, "w") as out:
                    out.write(summary)

                print(f"✅ Summary written to: summary_{filename}")

            except Exception as e:
                print(f"❌ Error summarizing {filename}: {e}")

    print("\n📦 Log summarization complete.\n")

if __name__ == "__main__":
    summarize_logs()
