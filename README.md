# Flask Examples - Getting Started Guide

Welcome! This guide will help you set up your development environment and run Flask applications using a modern IDE instead of Jupyter notebooks. This guide is written for complete beginners and is current as of Fall 2025.

## Table of Contents
- [1. Download This Repository](#1-download-this-repository)
- [2. Install an IDE](#2-install-an-ide)
- [3. Install Python](#3-install-python)
- [4. Set Up a Virtual Environment](#4-set-up-a-virtual-environment)
- [5. Run the Applications](#5-run-the-applications)
- [Troubleshooting](#troubleshooting)

---

## 1. Download This Repository

### What is Git?
Git is a version control system that tracks changes in your code. GitHub is a website that hosts git repositories online.

### Option A: Using Git (Recommended)

**Step 1: Install Git**

- **macOS**: Open Terminal and type:
  ```bash
  git --version
  ```
  If git is not installed, macOS will prompt you to install Xcode Command Line Tools. Click "Install".

- **Windows**: Download and install from [git-scm.com](https://git-scm.com/download/win)
  - Use all default settings during installation
  - Check "Git from the command line and also from 3rd-party software"

- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install git
  ```

**Step 2: Clone the Repository**

Open your terminal (Terminal on macOS/Linux, Git Bash or Command Prompt on Windows) and run:

```bash
cd ~/Documents  # or wherever you want to store the project
git clone https://github.com/innov8r-44/mines.git flask-examples
cd flask-examples
```

### Option B: Download as ZIP (Easier for Beginners)

1. Go to `https://github.com/innov8r-44/mines`
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to your Documents folder
5. Rename the folder to `flask-examples`

---

## 2. Install an IDE

An IDE (Integrated Development Environment) is a powerful text editor designed for coding. Here are two excellent modern options:

### Option A: Cursor (Recommended for 2025)

**What is Cursor?**  
Cursor is a modern IDE built on VS Code with AI assistance built-in. It's excellent for learning and getting help as you code.

**Installation:**

1. Go to [cursor.com](https://cursor.com)
2. Click **"Download"**
3. Choose your operating system (macOS, Windows, or Linux)
4. Install the downloaded file:
   - **macOS**: Drag Cursor to Applications folder
   - **Windows**: Run the installer and follow prompts
   - **Linux**: Follow the instructions on the website

**First-Time Setup:**
1. Open Cursor
2. You may be prompted to install command-line tools - click "Yes"
3. Click **"File → Open Folder"** and navigate to your `flask-examples` folder

### Option B: Visual Studio Code (VS Code)

**What is VS Code?**  
VS Code is the most popular code editor, with millions of users and thousands of extensions.

**Installation:**

1. Go to [code.visualstudio.com](https://code.visualstudio.com)
2. Click **"Download"** for your operating system
3. Install:
   - **macOS**: Drag to Applications folder
   - **Windows**: Run installer with default settings
   - **Linux**: Follow instructions for your distribution

**Recommended Extensions:**
1. Open VS Code
2. Click the Extensions icon (four squares) on the left sidebar
3. Search for and install:
   - **Python** (by Microsoft) - Essential for Python development
   - **Pylance** (by Microsoft) - Python language support
   - **Python Debugger** (by Microsoft) - Debugging support

**Open Your Project:**
1. Click **"File → Open Folder"**
2. Navigate to and select your `flask-examples` folder

---

## 3. Install Python

### Check If Python Is Already Installed

Open your terminal and run:

```bash
python3 --version
```

If you see `Python 3.11.x` or higher, you're good to go! Skip to [Section 4](#4-set-up-a-virtual-environment).

### Install Python 3.13 (Latest as of Fall 2025)

#### macOS

**Option 1: Official Installer (Recommended)**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.13.x** for macOS
3. Run the installer
4. **Important**: Check the box "Add Python to PATH"
5. Verify installation:
   ```bash
   python3 --version
   ```

**Option 2: Using Homebrew**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.13
```

#### Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.13.x** for Windows
3. Run the installer
4. **CRITICAL**: Check the box **"Add Python to PATH"** at the bottom of the installer
5. Click "Install Now"
6. After installation, open Command Prompt and verify:
   ```bash
   python --version
   ```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

Verify installation:
```bash
python3.13 --version
```

---

## 4. Set Up a Virtual Environment

### What is a Virtual Environment?

A virtual environment is an isolated Python environment for your project. It keeps your project's dependencies separate from other projects and your system Python. Think of it as a sandbox for your project.

### Why Use Virtual Environments?

- **Isolation**: Different projects can use different versions of packages
- **Reproducibility**: Makes it easy to share your project with others
- **Clean**: Keeps your system Python installation clean
- **Best Practice**: Industry standard for Python development

### Creating a Virtual Environment

Navigate to your project folder in the terminal, then follow the steps for your project:

#### For the Basic Flask Project

```bash
# Navigate to the basic-flask directory
cd ~/Documents/flask-examples/basic-flask

# Create a virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

#### For the Sklearn Flask Project

```bash
# Navigate to the sklearnflask directory
cd ~/Documents/flask-examples/sklearnflask

# Create a virtual environment
python3 -m venv .venv

# Activate it (same commands as above)
source .venv/bin/activate  # macOS/Linux
```

#### For the Shopping Project

```bash
# Navigate to the shoppingProject directory
cd ~/Documents/flask-examples/shoppingProject

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
```

### How to Know Your Virtual Environment is Active

When activated, you'll see `(.venv)` or the name of your virtual environment at the beginning of your terminal prompt:

```bash
(.venv) username@computer flask-examples %
```

### Using Virtual Environments in Your IDE

**Cursor/VS Code:**
1. Open the Command Palette:
   - macOS: `Cmd + Shift + P`
   - Windows/Linux: `Ctrl + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose the interpreter that shows `.venv` or `venv` in the path

The IDE will automatically use this virtual environment for running and debugging your code.

---

## 5. Run the Applications

### Prerequisites for All Projects

Make sure your virtual environment is activated (you see `(.venv)` in your terminal).

---

### Project 1: Basic Flask App

**What it does**: A simple Flask application with data processing and machine learning.

**Setup:**

```bash
# Navigate to the project
cd ~/Documents/flask-examples/basic-flask

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

**Run the application:**

```bash
# Set Flask environment variables
export FLASK_APP=app.py  # macOS/Linux
set FLASK_APP=app.py     # Windows Command Prompt
$env:FLASK_APP="app.py"  # Windows PowerShell

# Run in development mode
export FLASK_ENV=development  # macOS/Linux (optional but recommended)
flask run
```

**Or simply:**
```bash
python app.py
```

**Access the application:**
- Open your web browser
- Go to: `http://127.0.0.1:5000` or `http://localhost:5000`

**Stop the application:**
- Press `Ctrl + C` in the terminal

---

### Project 2: Sklearn Flask App

**What it does**: A Flask application that trains machine learning models on the Titanic dataset.

**Setup:**

```bash
# Navigate to the project
cd ~/Documents/flask-examples/sklearnflask

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

**Run the application:**

```bash
python main.py
```

**Access the application:**
- Open your browser to: `http://127.0.0.1:5000`
- You can train models and make predictions through the web interface

---

### Project 3: Shopping Project

**What it does**: A Flask application that predicts online shopping behavior using both scikit-learn and TensorFlow models.

**Setup:**

```bash
# Navigate to the project
cd ~/Documents/flask-examples/shoppingProject

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux

# Install dependencies (note: file is currently named "requriements.txt" - typo)
pip install -r requriements.txt
```

**Train the models (first time only):**

```bash
# Train the scikit-learn model
python train_sklearn.py

# Train the TensorFlow model (optional, takes longer)
python train_tf.py
```

**Run the application:**

```bash
python app.py
```

**Access the application:**
- Open your browser to: `http://127.0.0.1:5000`

---

## Troubleshooting

### Common Issues and Solutions

#### "python3: command not found"

**macOS/Linux**: Python might be installed as `python` instead:
```bash
python --version
```

**Windows**: Make sure you checked "Add Python to PATH" during installation. If not, reinstall Python.

#### "Permission Denied" errors on macOS/Linux

Use `python3` instead of `python`, and make sure to use `pip3`:
```bash
pip3 install -r requirements.txt
```

#### Virtual environment won't activate on Windows PowerShell

PowerShell has execution policy restrictions. Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### "Module not found" errors

Your virtual environment might not be activated, or packages aren't installed:
```bash
# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux

# Install/reinstall requirements
pip install -r requirements.txt
```

#### Port 5000 already in use

Another application is using port 5000. You can:
1. Stop the other application
2. Or run Flask on a different port:
   ```bash
   flask run --port 5001
   ```

#### "Address already in use" on macOS with AirPlay

macOS Monterey and later use port 5000 for AirPlay:
1. Go to System Settings → General → AirDrop & Handoff
2. Disable "AirPlay Receiver"
3. Or use a different port (see above)

#### IDE doesn't recognize Python or packages

Make sure you've selected the correct Python interpreter:
1. Open Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the one showing `.venv` in the path

---

## Key Differences from Jupyter Notebooks

If you're coming from Jupyter notebooks, here are some key differences:

### File Structure
- **Jupyter**: Everything in one `.ipynb` file
- **IDE**: Code split across multiple `.py` files (better organization)

### Running Code
- **Jupyter**: Run cells individually
- **IDE**: Run entire files or use the debugger to step through code

### Debugging
- **Jupyter**: Print statements
- **IDE**: Powerful debugger with breakpoints, variable inspection, and step-through execution

### Version Control
- **Jupyter**: Difficult to version control (notebooks contain output and metadata)
- **IDE**: Clean `.py` files that work perfectly with Git

### Dependencies
- **Jupyter**: Often install globally with `!pip install`
- **IDE**: Use virtual environments and `requirements.txt` files (much better practice)

---

## Learning Resources

- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Python Tutorial**: [docs.python.org/3/tutorial](https://docs.python.org/3/tutorial/)
- **Git Basics**: [git-scm.com/book/en/v2](https://git-scm.com/book/en/v2)
- **VS Code Python Tutorial**: [code.visualstudio.com/docs/python](https://code.visualstudio.com/docs/python/python-tutorial)

---

## Project Structure

```
flask-examples/
│
├── basic-flask/           # Simple Flask app with ML
│   ├── app.py            # Main application
│   ├── modeling.py       # ML model code
│   ├── data/             # Data files
│   ├── templates/        # HTML templates
│   └── requirements.txt  # Python dependencies
│
├── sklearnflask/         # Titanic ML prediction app
│   ├── main.py           # Main application
│   ├── data/             # Titanic dataset
│   ├── templates/        # HTML templates
│   └── requirements.txt
│
└── shoppingProject/      # Shopping behavior prediction
    ├── app.py            # Main application
    ├── train_sklearn.py  # Train sklearn model
    ├── train_tf.py       # Train TensorFlow model
    ├── data/             # Shopping dataset
    ├── templates/        # HTML templates
    └── requriements.txt  # Dependencies (note typo in filename)
```

---

## Next Steps

1. ✅ Clone/download the repository
2. ✅ Install an IDE (Cursor or VS Code)
3. ✅ Install Python 3.13+
4. ✅ Create and activate a virtual environment
5. ✅ Install project dependencies
6. ✅ Run an application!

**After running your first app:**
- Explore the code in your IDE
- Try modifying the HTML templates in the `templates/` folders
- Experiment with the models
- Learn to use the debugger in your IDE
- Start building your own Flask applications!

---

## Getting Help

If you run into issues:
1. Read the error message carefully - it often tells you exactly what's wrong
2. Check the [Troubleshooting](#troubleshooting) section above
3. Google the error message (this is what professional developers do!)
4. Ask in coding communities like Stack Overflow or Reddit's r/learnpython

Happy coding! 🚀
