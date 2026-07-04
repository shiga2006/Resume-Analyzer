# 📄 Resume Analyzer

> **AI-Powered Resume Analysis Tool** — Get intelligent insights on your resume using Google Gemini API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red.svg)](https://streamlit.io/)

---

## ✨ Features

- 🤖 **AI-Powered Analysis** — Leverage Google Gemini API for intelligent resume insights
- 👤 **User Authentication** — Secure login and signup system
- 📊 **Detailed Reports** — Get comprehensive feedback on resume structure, content, and keywords
- 📜 **Analysis History** — View and track previous resume analyses
- 🎨 **User-Friendly Interface** — Clean and intuitive Streamlit frontend
- 🔐 **Secure Backend** — RESTful API with CORS support
- 📱 **Responsive Design** — Works seamlessly on desktop and mobile

---

## 🛠 Tech Stack

### Backend

- **Framework:** Flask
- **Language:** Python 3.8+
- **API:** Google Gemini API
- **Authentication:** JWT-based auth
- **CORS:** Flask-CORS for cross-origin requests

### Frontend

- **Framework:** Streamlit
- **Language:** Python
- **UI Components:** Streamlit pages

### Services

- **NLP Parser:** Resume parsing and extraction
- **Gemini Service:** AI analysis integration
- **Database:** SQLite/Configured database

---

## 📋 Project Structure

```
Resume-Analyzer/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   └── resume.py          # Resume analysis endpoints
│   ├── services/
│   │   ├── gemini_service.py  # Gemini API integration
│   │   └── parser_service.py  # Resume parsing service
│   └── tests/
│       ├── test_db.py         # Database tests
│       ├── test_gemini.py     # Gemini service tests
│       └── test_parser.py     # Parser service tests
├── frontend/
│   ├── streamlit_app.py       # Main Streamlit app
│   └── pages/
│       ├── analyzer.py        # Resume analysis page
│       ├── history.py         # Analysis history page
│       ├── login.py           # User login page
│       └── signup.py          # User registration page
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/shiga2006/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   # Copy the example file
   cp backend/.env.example backend/.env

   # Edit backend/.env with your credentials
   # Add your Google Gemini API key
   ```

5. **Run the backend**

   ```bash
   cd backend
   python app.py
   ```

   The backend will run on `http://localhost:5000`

6. **Run the frontend (in a new terminal)**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
   The frontend will open at `http://localhost:8501`

---

## 🔌 API Endpoints

### Authentication

- **POST** `/auth/signup` — Register a new user

  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```

- **POST** `/auth/login` — User login
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```

### Resume Analysis

- **POST** `/resume/analyze` — Analyze a resume

  ```json
  {
    "resume_text": "John Doe\n...",
    "job_description": "We are looking for..."
  }
  ```

- **GET** `/resume/history` — Get analysis history (requires authentication)

- **GET** `/health` — Health check endpoint

---

## 📖 Usage

### Backend API Testing

```bash
# Health check
curl http://localhost:5000/health

# Home endpoint
curl http://localhost:5000/
```

### Frontend Usage

1. **Sign Up** — Create a new account on the signup page
2. **Login** — Log in with your credentials
3. **Analyze** — Upload or paste your resume for analysis
4. **View Results** — Get AI-powered insights and recommendations
5. **History** — Review previous analyses

---

## 🔧 Configuration

Edit `backend/config.py` to customize:

- Database connection strings
- API configurations
- Security settings
- CORS origins

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=your_database_url

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key

# JWT
JWT_SECRET=your_jwt_secret
```

---

## 🧪 Testing

Run the test suite:

```bash
# Test database
python backend/test_db.py

# Test Gemini service
python backend/test_gemini.py

# Test parser service
python backend/test_parser.py
```

---

## 📊 Features in Detail

### Resume Analysis

- Grammar and spelling check
- ATS (Applicant Tracking System) optimization
- Keyword matching
- Formatting recommendations
- Professional summary suggestions

### User Dashboard

- Track analysis history
- Compare multiple resume versions
- Get personalized recommendations
- Export analysis reports

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
## ⚠️ Security Notes

- **Never commit** your `.env` file with API keys
- Always use **environment variables** for sensitive data
- Rotate your API keys regularly
- Use HTTPS in production
- Keep dependencies updated

---

## 🐛 Troubleshooting

### "Module not found" error

```bash
pip install -r backend/requirements.txt
```

### Streamlit connection refused

Ensure the backend is running on `http://localhost:5000`

### API key not working

- Verify your Google Gemini API key in `.env`
- Check API quotas in Google Cloud Console
- Ensure the API is enabled

---

## 📞 Support

For issues, questions, or suggestions:

- Open an [Issue](https://github.com/shiga2006/Resume-Analyzer/issues)
- Start a [Discussion](https://github.com/shiga2006/Resume-Analyzer/discussions)

---

## 🎯 Roadmap

- [ ] PDF resume upload support
- [ ] Multiple resume comparison
- [ ] Job market insights
- [ ] LinkedIn integration
- [ ] Mobile app
- [ ] Advanced analytics dashboard

---

## 📚 Resources

- [Google Gemini API Documentation](https://ai.google.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

<div align="center">

**Made with ❤️ by Shivashiga A.M**

⭐ If you found this helpful, please consider giving it a star!

</div>
