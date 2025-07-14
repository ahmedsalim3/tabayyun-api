Tabayyun API Web Interface
==========================

<div align="center">
  
[[`Demo App`](https://huggingface.co/spaces/ahmed-salim/tabayyun-api)]

</div>

![Demo App](./static/images/demo.png)

How to install?
===============

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
```

```bash
# On Linux
source .venv/bin/activate
```

```bash
# On Windows
.venv\Scripts\activate
```

Install dependencies:
=====================

```bash
pip install -r requirements.txt 
```

3. Rename [`.env.example`](./.env.example) to `.env`, and add your [API_KEY](./.env.example#L1)

Usage
=====

### 1. Flask Web Interface

Run the Flask web application:

```bash
python app.py
```

Then open http://localhost:5000

### 2. Gradio App

```
pip install gradio>=4.44.0
```

Run the Gradio application:

```bash
python gradio_app.py
```

Or try the [live demo](https://huggingface.co/spaces/ahmed-salim/tabayyun-api).

### 3. Command Line

Use the command-line interface for batch processing:

```bash
# check a specific website
python main.py facebook.com

# check with custom output directory
python main.py facebook.com -o results

# or simply run this, and proceed interactively
python main.py
```

Repo Structure
==============

```sh
├── app.py                 <- Flask web app
├── gradio_app.py          <- Gradio web app
├── main.py                <- Command-line script
├── templates/             <- HTML templates
│   └── app.html
├── output/
└── requirements.txt
```
