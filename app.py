
from flask import Flask, request, jsonify
from transformers import AutoTokenizer
from openvino.runtime import Core
import numpy as np

app = Flask(__name__)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# Load OpenVINO model
ie = Core()
model_ir = ie.read_model(model="model/chat_model.xml")
compiled_model = ie.compile_model(model=model_ir, device_name="CPU")

input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")

    inputs = tokenizer(prompt, return_tensors="np")
    input_ids = inputs["input_ids"]

    result = compiled_model([input_ids])[output_layer]
    response_ids = np.argmax(result, axis=-1)

    response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
