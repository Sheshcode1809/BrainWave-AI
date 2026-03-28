# BrainWave AI

A simple AI-powered Q&A application built with Streamlit and LangChain, using Ollama's Gemma3 model for intelligent responses.

## Features

- Interactive Q&A interface
- Powered by Ollama's Gemma3:1b model
- LangSmith integration for tracing and monitoring
- Streamlit-based web interface

## Prerequisites

- Python 3.12 or higher
- Ollama installed and running
- Gemma3:1b model pulled in Ollama

## Installation

1. Clone or download this repository.

2. Create a virtual environment:
   ```bash
   python -m venv myenv
   ```

3. Activate the virtual environment:
   - On Windows: `myenv\Scripts\activate`
   - On macOS/Linux: `source myenv/bin/activate`

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Install and set up Ollama:
   - Download and install Ollama from [ollama.ai](https://ollama.ai)
   - Pull the Gemma3 model: `ollama pull gemma3:1b`

6. Create a `.env` file in the project root and add your LangSmith credentials:
   ```
   LANGSMITH_API_KEY=your_api_key_here
   LANGSMITH_PROJECT=your_project_name_here
   ```

## Usage

1. Ensure Ollama is running in the background.

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to the provided URL (usually `http://localhost:8501`).

4. Enter your question in the text input field and get AI-powered responses.

## Project Structure

- `app.py`: Main application file
- `requirements.txt`: Python dependencies
- `myenv/`: Virtual environment (created during setup)

## Contributing

Feel free to fork this project and submit pull requests for improvements.

## License

This project is open-source. Please check the license file for details.