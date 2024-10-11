from flask import Flask, render_template, request, jsonify
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Azure endpoint and key
endpoint = "https://dogiparthy.cognitiveservices.azure.com/"
key = "861dba2e592c48df92b69018de88fa82"

# Initialize the Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    image = request.files['image'].read()

    # Analyze the uploaded image
    result = client.analyze(
        image_data=image,
        visual_features=[VisualFeatures.READ]
    )

    # Extract and prepare text to send to the frontend
    line_text = ''
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            line_text += line.text + '\n'

    return jsonify({"text": line_text})

if __name__ == '__main__':
    app.run(debug=True)
