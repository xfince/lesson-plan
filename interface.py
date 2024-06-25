import gradio as gr
import asyncio
from actions.analyze_textbook_content import analyze_textbook_content

async def synthesize_lesson(textbook_content):
    return await analyze_textbook_content(textbook_content)

def run_interface():
    iface = gr.Interface(
        fn=lambda x: asyncio.run(synthesize_lesson(x)),
        inputs=gr.Textbox(lines=10, placeholder="Paste textbook content here..."),
        outputs="json",
        title="Textbook Synthesizer",
        description="Convert textbook content into structured lesson plans."
    )
    iface.launch()

if __name__ == "__main__":
    run_interface()
