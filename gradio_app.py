import os
import requests
import gradio as gr
from dotenv import load_dotenv
import utils

load_dotenv()

css = """
body {
    font-family: 'Montserrat', 'Noto Sans Arabic', Arial, sans-serif;
    background: #f9f9f9;
    color: #222;
}

.gradio-container {
    max-width: 800px !important;
    margin: 0 auto !important;
}

.main-container {
    max-width: 500px;
    margin: 2rem auto;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    color: white !important;
}

.page-title {
    margin-bottom: 1rem;
    text-align: center;
    font-weight: 600;
    color: white !important;
}

.risk-section {
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.risk-icon {
    font-size: 2rem;
}

.risk-text {
    font-weight: 600;
}

.risk-green { color: #4ade80; }
.risk-yellow { color: #fbbf24; }
.risk-red { color: #f87171; }

.info-row {
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: white !important;
}

.arabic-text-box {
    margin-top: 1.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 6px;
    font-size: 1.1rem;
    line-height: 1.7;
    text-align: right;
    font-family: 'Noto Sans Arabic', Arial, sans-serif;
    letter-spacing: 0.01em;
    white-space: pre-line;
}

.action-buttons {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.action-btn {
    flex: 1;
    min-width: 150px;
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    background: #222;
    color: #fff;
    transition: all 0.3s ease;
}

.action-btn:hover {
    background: #333;
}

.error-message {
    color: #dc2626;
    text-align: center;
    padding: 1rem;
    background: transparent !important;
    border-radius: 6px;
    margin: 1rem 0;
}

.loading-message {
    text-align: center;
    padding: 2rem;
    color: #666;
}
"""


def check_website(website, api_key):
    """Handle website check request"""
    if not website or not website.strip():
        return "Please enter a website URL", None

    website = website.strip()

    # use input API key if provided, otherwise use environment variable
    api_key = api_key.strip() if api_key else os.getenv("API_KEY")

    if not api_key:
        return (
            "API key is required. Please enter your Tabayyun API key or set it in environment variables.",
            None,
        )

    url = f"https://business.tabayyun.com.sa/business-api/v1/inquiry?inquiry={website}"
    headers = {"X-Authorization": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
        else:
            data = {"text": response.text}

        result = {
            "status_code": response.status_code,
            "website": website,
            "response": data,
        }

        formatted = utils.format_data(result)

        if not formatted:
            return "Invalid response format from API", None

        # Create HTML output
        risk_info = formatted["risk_info"]
        html_output = f"""
        <div class="main-container">
            <h2 class="page-title">Result for: {formatted['website']}</h2>
            <div class="risk-section">
                <span class="risk-icon">{risk_info['icon']}</span>
                <span class="risk-text risk-{formatted['risk_protocol'].lower()}">Risk: {formatted['risk_protocol']}</span>
            </div>
            <div class="info-row"><b>Organization:</b> {formatted['organization']['name_en']} / {formatted['organization']['name_ar']}</div>
            <div class="info-row"><b>Sector:</b> {formatted['sector']['name_en']} / {formatted['sector']['name_ar']}</div>
            <div class="info-row"><b>Created At:</b> {formatted['created_at']}</div>
            <div class="info-row"><b>Belongs To:</b> {formatted['belongs_to']}</div>
            <div class="arabic-text-box">{formatted['arabic_text']}</div>
        </div>
        """

        return html_output, formatted["raw_json"]

    except requests.RequestException as e:
        return f"Request failed: {str(e)}", None
    except Exception as e:
        return f"Error: {str(e)}", None


with gr.Blocks(css=css, title="Tabayyun API") as demo:
    gr.HTML(
        """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-family: 'Montserrat', sans-serif;">Tabayyun API</h1>
    </div>
    """
    )

    with gr.Row():
        with gr.Column(scale=6):
            show_api_key = gr.Checkbox(label="Use custom API key", value=False)
            api_key = gr.Textbox(
                label="API Key",
                placeholder="Enter your Tabayyun API key",
                lines=1,
                type="password",
                visible=False,
            )
            website_input = gr.Textbox(
                label="Website URL", placeholder="Enter website URL", lines=1
            )
            check_btn = gr.Button("Check", variant="primary")

    output_html = gr.HTML(label="Results")
    output_json = gr.JSON(label="Raw JSON Data", visible=False)

    with gr.Column():
        with gr.Row():
            show_json_btn = gr.Button(
                "Download JSON Data", variant="secondary", scale=5
            )
            clear_btn = gr.Button("Clear", variant="secondary", scale=5)

    def _toggle(show):
        return gr.Textbox(visible=show)

    def download_json(json_data):
        if not json_data:
            return "No data to download"

        # Create download link with JavaScript
        download_html = f"""
        <script>
        function downloadJSON() {{
            const data = `{json_data}`;
            const blob = new Blob([data], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tabayyun_result.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
        downloadJSON();
        </script>
        <div>Downloading JSON file...</div>
        """
        return download_html

    def clear_inputs():
        return "", "", "", None, gr.Checkbox(value=False)

    show_api_key.change(fn=_toggle, inputs=[show_api_key], outputs=[api_key])

    show_json_btn.click(fn=download_json, inputs=[output_json], outputs=[output_html])

    check_btn.click(
        fn=check_website,
        inputs=[website_input, api_key],
        outputs=[output_html, output_json],
    )

    website_input.submit(
        fn=check_website,
        inputs=[website_input, api_key],
        outputs=[output_html, output_json],
    )

    clear_btn.click(
        fn=clear_inputs,
        outputs=[website_input, api_key, output_html, output_json, show_api_key],
    )

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
