
from transformers import AutoTokenizer, AutoModelForCausalLM
from openvino.tools import mo
import torch

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

dummy_input = tokenizer("Hello, how are you?", return_tensors="pt")

# Export to ONNX
torch.onnx.export(model,
                  (dummy_input["input_ids"],),
                  "gpt2.onnx",
                  input_names=["input_ids"],
                  output_names=["logits"],
                  dynamic_axes={"input_ids": {0: "batch", 1: "seq"}},
                  opset_version=13)

# Convert ONNX to OpenVINO
mo.convert_model("gpt2.onnx", output_dir="model", model_name="chat_model")
