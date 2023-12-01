from gpt4all import GPT4All
from flask import Flask, request, jsonify

app = Flask(__name__)
model_path = "orca-mini-3b-gguf2-q4_0.gguf"  # Replace with your actual model path
gpt_model = GPT4All(model_path)

log_content = None

@app.route('/upload_log', methods=['POST'])
def upload_log():
    global log_content
    file = request.files['file']
    if file:
        log_content = file.read().decode("utf-8")
        return jsonify({'message': 'Log file uploaded successfully'})
    return jsonify({'message': 'No file uploaded'})

@app.route('/generate', methods=['POST'])
def generate_text():
    global log_content
    data = request.get_json()
    prompt = data.get('prompt')

    if log_content:
    	# Truncate log content to stay within token limits
        max_log_tokens = 1500  # Adjust this value as needed
        truncated_log = log_content[:max_log_tokens]

        prompt += f"\nLog Context: {truncated_log}"

    response = gpt_model.generate(prompt, temp=0)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
