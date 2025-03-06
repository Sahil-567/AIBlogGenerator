import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

IMAGE_FOLDER = os.path.join(app.root_path, 'static/images')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

# Ensure API key is set correctly
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "Missing OpenAI API key. Set OPENAI_API_KEY in environment variables.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sports')
def sports():
    return render_template('sports.html')


@app.route('/cricket/readme')
def sports_cricket_readme():
    return render_template('cricketreadme.html')


@app.route('/download/<filename>')
def download_image(filename):
    try:
        return send_from_directory(IMAGE_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/football/readme')
def sports_footballl_readme():
    return render_template('footballreadme.html')


@app.route('/basketball/readme')
def sports_basketball_readme():
    return render_template('basketballreadme.html')


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        topic = data.get('prompt', "").strip()

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        prompt = PromptTemplate.from_template(
            "You are a helpful assistant that writes an article about {topic}."
        )

        llm = OpenAI(openai_api_key=OPENAI_API_KEY,
                     temperature=0.3)  # Set API key
        chain = LLMChain(llm=llm, prompt=prompt)

        output = chain.run(topic)
        return jsonify({"generated_text": output})

    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
