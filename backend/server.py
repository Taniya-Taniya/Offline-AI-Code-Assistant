from flask import Flask, request, jsonify, send_from_directory
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Load tokenizer and model once at startup
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

def prepare_prompt(feature, user_prompt):
    """
    Modify the prompt based on the feature to guide the model.
    """
    if feature == "debug":
        return f"### Debug the following code and suggest fixes:\n{user_prompt}\n### Suggested fixes:\n"
    elif feature == "documentation":
        return f"### Write detailed documentation for the following code:\n{user_prompt}\n### Documentation:\n"
    elif feature == "completion":
        return user_prompt
    else:
        return user_prompt

# Serve frontend index.html at root
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, images, etc.)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# API endpoint for code completion
@app.route("/complete", methods=["POST"])
def complete():
    data = request.json
    raw_prompt = data.get("prompt", "")
    max_length = data.get("max_length", 200)
    min_length = data.get("min_length", 50)
    temperature = data.get("temperature", 1.0)
    top_p = data.get("top_p", 0.95)
    num_return_sequences = data.get("num_return_sequences", 1)

    if not raw_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Extract feature from prompt prefix if present
    feature = "completion"  # default
    if raw_prompt.startswith("### Feature:"):
        try:
            first_line, rest = raw_prompt.split("\n", 1)
            feature = first_line.replace("### Feature:", "").strip().lower()
            user_prompt = rest.strip()
        except Exception:
            user_prompt = raw_prompt
    else:
        user_prompt = raw_prompt

    prompt = prepare_prompt(feature, user_prompt)

    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                min_length=min_length,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.eos_token_id,
            )

        completions = []
        for i in range(num_return_sequences):
            completion = tokenizer.decode(outputs[i], skip_special_tokens=True)
            # Remove prompt from completion to return only generated text
            if completion.startswith(prompt):
                completion = completion[len(prompt):].strip()
            completions.append(completion)

        if num_return_sequences == 1:
            return jsonify({"completion": completions[0]})
        else:
            return jsonify({"completions": completions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
