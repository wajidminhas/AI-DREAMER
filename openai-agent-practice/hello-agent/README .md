# Hello Agent

A Chainlit-based AI chatbot application that integrates with Google Gemini and OpenAI APIs to provide a conversational interface. This project allows users to interact with a customizable AI assistant, with support for streaming responses and session-based conversation history.

## Features

- **Dual API Support**: Integrates with Google Gemini (`gemini-pro`) and OpenAI (`gpt-3.5-turbo`, `gpt-4`) APIs.
- **Interactive Chat UI**: Built with Chainlit for a seamless web-based chat experience.
- **Streaming Responses**: Real-time response streaming for both Gemini and OpenAI models.
- **Session Management**: Maintains conversation history per user session.
- **Customizable Models**: Switch between supported models via UI settings.
- **Error Handling**: Robust error handling for API failures and invalid configurations.

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- API keys for Google Gemini and/or OpenAI

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd hello-agent
   ```

2. **Set Up Virtual Environment with uv**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Ensure `pyproject.toml` is present, then run:
   ```bash
   uv sync
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key  # Optional if using Gemini
   ```
   Obtain API keys from:
   - [Google AI Studio](https://makersuite.google.com/) for Gemini
   - [OpenAI](https://platform.openai.com/) for OpenAI

## Project Structure

```
hello-agent/
├── .env              # Environment variables (API keys)
├── main.py           # Main Chainlit application script
├── pyproject.toml    # Project metadata and dependencies
├── hello_agent/
│   ├── __init__.py   # Package initialization (optional CLI entry point)
```

## Usage

1. **Run the Application**:
   ```bash
   uv run chainlit run main.py
   ```
   This starts the Chainlit server, typically at `http://localhost:8000`. Open the URL in your browser.

2. **Interact with the Chatbot**:
   - The welcome message displays with a Chainlit logo.
   - Type messages to interact with the AI assistant.
   - Use the settings panel to switch between supported models (`gemini-pro`, `gpt-3.5-turbo`, `gpt-4`).

3. **Run the CLI (Optional)**:
   If using the `hello-agent` script entry point:
   ```bash
   uv run hello-agent
   ```
   This executes the `main()` function in `hello_agent/__init__.py`, printing "Hello from hello-chainlit!".

## Dependencies

Defined in `pyproject.toml`:
- `chainlit>=2.5.5`
- `google-generativeai>=0.8.5`
- `openai>=1.86.0`
- `pydantic>=2.11.7`
- `python-dotenv>=1.1.0`
- `sqlalchemy>=2.0.41`

## Troubleshooting

- **"File does not exist: main.py"**:
  - Ensure `main.py` is in the project root or specify the correct path (e.g., `chainlit run hello_agent/main.py`).
  - Verify the file name and location:
    ```bash
    ls -l
    ```

- **API Key Errors**:
  - Confirm `.env` is correctly set up and loaded:
    ```bash
    python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
    ```
  - Test the Gemini API key:
    ```python
    # test_gemini.py
    import google.generativeai as genai
    import os
    from dotenv import load_dotenv

    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, world!")
    print(response.text)
    ```
    Run with:
    ```bash
    uv run python test_gemini.py
    ```

- **Dependency Issues**:
  - Verify installed packages:
    ```bash
    uv pip list | grep -E "chainlit|google-generativeai|openai|python-dotenv"
    ```
  - Update dependencies:
    ```bash
    uv sync
    ```

- **Network Issues**:
  - Ensure connectivity to `https://generativelanguage.googleapis.com` (Gemini) or `https://api.openai.com` (OpenAI).
  - Test with:
    ```bash
    curl https://generativelanguage.googleapis.com
    ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for bugs, features, or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Author: Wajid Minhas  
Email: shanitent667@gmail.com