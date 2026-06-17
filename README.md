# 🚀 CodeBridge – Cross-Language Code Conversion System

CodeBridge is an AI-powered offline cross-language code conversion system that converts source code between multiple programming languages while preserving the original logic. It also supports intelligent recovery of minor syntax issues and large codebases using smart chunking technology.

---

## 📌 Features

### 🔹 Cross-Language Code Conversion

Supports conversion between:

* Python
* PHP
* Laravel
* JavaScript
* Java
* C++
* HTML
* CSS

---

### 🔹 AI-Powered Conversion

* Uses **Ollama**
* Powered by **Qwen 2.5 Coder 1.5B**
* Works completely offline after model download
* Preserves original program logic
* Generates executable target code

---

### 🔹 Intelligent Code Recovery

Automatically handles minor issues such as:

* Python indentation errors
* Missing line breaks
* Multiple statements on one line
* Minor keyword typos (e.g., `eturn` → `return`)
* Formatting inconsistencies

---

### 🔹 Large File Support

* Smart Chunking Technology
* Supports approximately **2000 lines reliably**
* Efficient conversion of **500–1000 line files**
* Prevents AI context overflow

---

### 🔹 User Interface

* Same-page conversion
* Responsive Bootstrap UI
* Dark Mode / Light Mode
* Drag-and-drop file upload

---

### 🔹 File Support

Supported file types:

* `.py`
* `.php`
* `.js`
* `.java`
* `.cpp`
* `.html`
* `.css`
* `.txt`

---

### 🔹 Output Features

* Copy converted code
* Download converted code
* Automatic file extension generation

---

### 🔹 Automatic Language Detection

Detects source languages automatically:

* Python
* PHP
* Laravel
* JavaScript
* Java
* C++
* HTML
* CSS

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Backend

* Flask (Python)

### AI Engine

* Ollama
* Qwen 2.5 Coder 1.5B

### Processing

* Python AST
* Custom Recovery Logic
* Smart Chunking

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeBridge.git
cd CodeBridge
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download and install Ollama from:

https://ollama.com

Pull the model:

```bash
ollama pull qwen2.5-coder:1.5b
```

---

## ▶️ Run the Application

Start Flask:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```text
CodeBridge/
│
├── app.py
├── converter.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── .gitignore
```

---

## 🎯 Future Enhancements

* Additional programming languages
* Conversion history
* Syntax validation
* Accuracy confidence score
* Cloud deployment

---

## 👨‍💻 Author

**Vraj Khatri**

Software Developer Intern | AI & Full Stack Enthusiast

---

## 📄 License

This project is developed for educational and academic purposes.
