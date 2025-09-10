# ⭐AI Code Assistant

An AI-powered code assistant web app that helps you with **code completion**, **debugging suggestions**, and **automatic documentation**.  
Backend is built with Flask and uses Hugging Face's GPT-Neo 125M model.  
Frontend is a static site served separately (e.g., via a local development server on port 3000).

## Features

- **Code Completion:** Continue your code snippets intelligently.
- **Debugging Suggestion:** Find bugs and get fix suggestions.
- **Automatic Documentation:** Generate detailed comments and documentation for your code.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Node.js and npm (if you use a frontend dev server like `live-server` or similar)
- Internet connection (required only for initial setup and model download)

## Setup and Running Instructions:-

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
### 2. Backend Setup
a. Create and activate a Python virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
b. Install backend dependencies
```bash
pip install -r requirements.txt
```
c. Run the backend server
```bash
python backend.py
```
The backend will start on:
```
http://127.0.0.1:5000
```
"Note: The first time you run the backend, the GPT-Neo model (~500MB) will be downloaded. This requires an active internet connection."

### 3. Frontend Setup
You can serve the frontend files in the frontend/ folder using any static file server.
For example, using live-server (Node.js):
```bash
npm install -g live-server
live-server frontend --port=3000
```
Or using Python's built-in HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Open your browser and navigate to:
```
http://127.0.0.1:3000/index.html
```

### 4. Using the App
- The frontend will send API requests to the backend at 
`http://127.0.0.1:5000/complete.`
- Make sure the backend is running before using the frontend.
- Select a feature (Code Completion, Debugging, Documentation).
- Enter your code snippet or prompt.
- Click Generate to get AI-generated results.

## Offline Usage (After Initial Setup)
Once the GPT-Neo model is downloaded and cached locally by Hugging Face Transformers:

- You can turn off your internet connection or enable flight mode.
- Restart the backend server (python backend.py).
- Serve the frontend as before.
- Use all features without internet connection.

## Project Structure
```
├── backend/             
│   ├── requirements.txt    # Python dependencies for backend
│   └── server.py           # Flask backend server script
└── frontend/             
    └── index.html          # Frontend HTML file
```

## Troubleshooting
- **CORS errors:** If frontend and backend run on different ports, ensure your backend enables CORS (your backend.py already includes flask-cors).
- **Model download issues:** Ensure internet connection during first backend run.
- **Frontend not loading:** Check you are opening the correct URL  (http://127.0.0.1:3000/index.html).

## License
MIT License

## Acknowledgments
- Hugging Face for GPT-Neo and Transformers.
- Tailwind CSS for styling.
- Flask for backend framework.
