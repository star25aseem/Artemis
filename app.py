import gradio as gr
from main import run_pipeline

def artemis_query(query):
    result = run_pipeline(query)
    return f"""
Query: {result['query']}

Rewritten: {result['rewritten_query']}

Answer:
{result['answer']}
"""

iface = gr.Interface(
    fn=artemis_query,
    inputs=gr.Textbox(lines=2, placeholder="Ask anything..."),
    outputs="text",
    title="🚀 Artemis Research Assistant"
)

iface.launch(server_name="0.0.0.0", server_port=7860)