from flask import Flask, request, jsonify
from gpt4all import GPT4All

app = Flask(__name__)
gpt_model = GPT4All(model_name="orca-mini-3b-gguf2-q4_0.gguf",
                    model_path='/home/karan/Downloads', allow_download=False)

chat_sessions = {}  # Store chat sessions for different clients


@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    user_id = data.get('user_id', None)
    prompt = data.get('prompt')

    if user_id not in chat_sessions:
        chat_sessions[user_id] = gpt_model.chat_session()

    chat = chat_sessions[user_id]
    response = chat.generate(prompt, temp=0)

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
