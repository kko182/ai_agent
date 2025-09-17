# AI Agent (Python)

This project is a Python-based AI agent designed to interact with your local environment.  
It can list files, read file contents, write to files, and even run Python scripts — all from natural language prompts.  

---

## 🚀 Features

- **List files and directories** in a working directory  
- **Read file contents** safely within the working directory  
- **Write content to files** (creates files if they don’t exist)  
- **Run Python scripts** (with optional arguments)  
- **Chain tasks together** (e.g., run a script, then read its output)  

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/kko182/ai-agent.git
cd ai-agent
pip install -r requirements.txt
```
---

## ▶️ Usage

Run the agent by passing a natural language prompt:
uv run main.py "your prompt here"

Example:
uv run main.py "Can you list all the files and directories in the current directory?"

---

## 💡Example Prompts

Here are some prompts you can try to showcase the agent’s functionality:

List files:
"Can you list all the files and directories in the current directory?"

Read a file:
"I have a file named 'my_script.py'. Can you read its content?"

Run a Python script:
"I have a Python script named 'my_script.py'. Can you execute it?"

Run a Python script with arguments:
"I have a Python script named 'my_script.py' that takes two arguments. Can you run it with 'hello' and 'world'?"

Write to a file:
"Can you write the text 'Hello, world!' to a file named 'output.txt'?"

List files, then read a file:
"List the files in the current directory. Then, read the content of 'my_file.txt'."

Write to a file, then read it back:
"Write 'This is a test' to 'test.txt'. Then, read the content of 'test.txt'."

Run a script, then read the output:
"Run 'my_script.py'. Then, assuming it created 'output.txt', read the contents of 'output.txt'."

Complex workflow:
"I have a python script called 'process_data.py'. It takes a file as input and outputs results to 'output.txt'. Run it with 'data.txt', then read 'output.txt'."

---

## ⚙️ Project Structure
```ai_agent/
│── main.py               # Entry point for the agent
│── pkg/                  # Core functionality (calculator, render, etc.)
│── get_files_info.py     # Lists files in a directory
│── get_file_content.py   # Reads file contents
│── run_python.py         # Executes Python files
│── write_file_contents.py# Writes content to a file
│── config.py             # Configurations (working dir, max chars, etc.)
│── tests.py              # Unit tests
```
---

## 🛠 Requirements

Python 3.8+, 
Google GenAI SDK, 
uv for running scripts