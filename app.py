import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

st.set_page_config(page_title="Azure Copilot for Architects", page_icon="🧠")

st.title("🧠 Azure Copilot for Architects")
st.markdown("Ask Azure architecture questions and get answers powered by Phi-3 🚀")

with st.form("question_form"):
    question = st.text_input("🧠 Enter your Azure architecture query:")
    submitted = st.form_submit_button("💡 Get Answer")

@st.cache_resource
def load_model():
    model_id = "microsoft/phi-3-mini-4k-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        device_map=None  # Force CPU
    ).to("cpu")
    return tokenizer, model

if submitted and question:
    tokenizer, model = load_model()

    prompt = f"""You are an expert Azure Cloud Architect.
Answer the following question clearly and concisely:
{question}
"""

    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    st.markdown("### 💬 Answer")
    st.success(answer)
