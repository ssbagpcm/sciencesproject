from flask import Flask, request, jsonify, send_from_directory
from groq import Groq
import os
import markdown

app = Flask(__name__, static_url_path='', static_folder='.')

# api Groq
client = Groq(
    api_key="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"
)

@app.route('/')
def index():
    return app.send_static_file('sguibeta.html')

@app.route('/chatgpt')
def chatgpt():
    return app.send_static_file('chatgpt.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.1-70b-versatile"
        )

        # Récupérer la réponse du modèle
        response_message = chat_completion.choices[0].message.content
        return jsonify({'response': response_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files')
def get_files():
    articles_dir = 'articles'  # Assurez-vous que ce chemin est correct
    files = [f for f in os.listdir(articles_dir) if f.endswith('.md')]
    return jsonify(files)

@app.route('/api/file/<filename>')
def get_file_content(filename):
    file_path = os.path.join('articles', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content)
            return html_content
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)