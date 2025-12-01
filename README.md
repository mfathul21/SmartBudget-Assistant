# 💰 SmartBudget-Assistant

AI-powered Personal Finance Management System with intelligent chatbot assistant for expense tracking, budget management, and financial insights.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Live Demo

🚀 **[https://smartbudget-assistant.onrender.com](https://smartbudget-assistant.onrender.com)**

## 🌟 Features

### 🎨 Authentication & Security
- 🔐 **Secure User Registration** - Email verification with OTP (One-Time Password)
- 🔑 **Password Recovery** - Forgot password with email reset link
- 🌐 **Bilingual Support** - Indonesian & English interface
- 🎯 **Strong Password Generator** - Built-in password suggestion tool
- ✅ **Modern UI/UX** - Professional glassmorphism design with smooth animations
- 📱 **Fully Responsive** - Optimized for desktop, tablet, and mobile devices

### 🤖 AI Financial Assistant
- 💬 **AI SmartBudget Assistant** - Powered by OpenAI GPT-4o-mini & Google Gemini 2.5 Flash
- 💸 **Smart Transaction Tracking** - Natural language expense/income recording
- 📊 **Budget Management** - Track spending by category with visual insights
- 🎯 **Savings Goals** - Set and monitor financial targets with progress tracking
- 💳 **Multi-Account Support** - Manage multiple payment methods (Cash, BCA, OVO, Gopay, etc.)
- 🔄 **Fund Transfers** - Transfer between accounts and savings goals
- 📈 **Financial Reports** - Monthly summaries and analytics
- 🧠 **Conversation Memory** - Context-aware chatbot with long-term memory

## 🚀 Tech Stack

**Backend:**
- Python 3.11+
- Flask 3.0.0
- PostgreSQL 15+ (Production - Neon Database)
- SQLite (Development)
- OpenAI API (GPT-4o-mini)
- Google Generative AI (Gemini 2.5 Flash)
- Gmail SMTP (Email Service)

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- FontAwesome 6.4.0 Icons
- Responsive Design (Mobile-First)
- Pure CSS Animations

**Deployment:**
- Render.com Web Service
- Gunicorn 21.2.0 WSGI Server

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 15+ (production) or SQLite (development)
- OpenAI API key
- Google Gemini API key
- Gmail account for SMTP email service

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/mfathul21/SmartBudget-Assistant.git
cd SmartBudget-Assistant
```

2. **Create virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy example env file
cp .env.example backend/.env

# Edit backend/.env with your credentials
FLASK_SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key
GOOGLE_API_KEY=your-google-gemini-api-key
DATABASE_URL=sqlite:///smartbudget.db  # For local development

# Email Configuration (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM=your-email@gmail.com
```

> **Note:** For Gmail, you need to create an App Password. See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed instructions.

5. **Initialize database**
```bash
cd backend
python -c "from database import init_db; init_db()"
```

6. **Run the application**
```bash
python main.py
```

The application will be available at `http://localhost:8000`

## 🎯 Usage

### Register & Login
1. Navigate to `http://localhost:8000/register.html`
2. Create an account with email and password
3. Verify your email with the OTP code sent to your inbox
4. Login at `http://localhost:8000/login.html`
5. Use "Forgot Password" if you need to reset your password

### Chat with AI Assistant

The AI assistant understands natural language commands:

**Record Expenses:**
```
"catat pengeluaran makan siang 50rb dari cash"
"beli kopi 25000 pakai gopay"
```

**Record Income:**
```
"catat pemasukan gaji 5 juta ke BCA"
"dapat bonus 1 juta masuk ke rekening"
```

**Transfer Funds:**
```
"transfer 100rb dari cash ke ovo"
"pindahkan 500000 dari BCA ke savings"
```

**Update Transactions:**
```
"ubah transaksi id 123 kategorinya jadi transport"
"edit deskripsi transaksi 456 jadi bensin motor"
```

**Create Savings Goals:**
```
"buat target tabungan dana darurat 10 juta sampai desember"
"target nabung liburan 5 juta dalam 6 bulan"
```

**Query Financial Data:**
```
"tampilkan pengeluaran bulan ini"
"berapa total pemasukan januari?"
"progress tabungan dana darurat"
```

## 🗂️ Project Structure

```
SmartBudget-Assistant/
├── backend/
│   ├── archive/              # Development & testing files
│   ├── __pycache__/          # Python cache
│   ├── auth.py               # Authentication, OTP, password reset
│   ├── config.py             # Configuration management
│   ├── database.py           # Database connection & initialization
│   ├── embeddings.py         # Vector embeddings for semantic search
│   ├── helpers.py            # Email utilities & helper functions
│   ├── llm_executor.py       # AI model interaction & execution
│   ├── llm_tools.py          # AI function definitions
│   ├── main.py               # Main Flask application & API endpoints
│   ├── memory.py             # Conversation memory management
│   ├── requirements.txt      # Python dependencies
│   ├── schema.sql            # PostgreSQL/SQLite database schema
│   ├── init_admin.py         # Admin user initialization script
│   └── reset_db.py           # Database reset utility
├── public/
│   ├── static/
│   │   ├── app.js            # Core frontend logic & translations
│   │   ├── modals.js         # Terms & Privacy modal content
│   │   ├── admin.js          # Admin dashboard logic
│   │   ├── profile.js        # Profile management
│   │   ├── savings-helper.js # Savings goal utilities
│   │   └── styles.css        # Global styles with responsive design
│   ├── uploads/avatars/      # User profile pictures
│   ├── index.html            # Main SmartBudget assistant interface
│   ├── login.html            # Login page (bilingual)
│   ├── register.html         # Registration with OTP verification
│   ├── forgot.html           # Password recovery page
│   ├── reset-password.html   # Password reset with token
│   ├── profile.html          # User profile management
│   ├── settings.html         # User settings & preferences
│   └── admin.html            # Admin dashboard
├── assets/                   # Static assets & images
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── render.yaml               # Render.com deployment configuration
├── startup.sh                # Production startup script
├── wsgi.py                   # WSGI entry point for Gunicorn
├── requirements.txt          # Root Python dependencies
├── EMAIL_SETUP.md            # Gmail SMTP configuration guide
├── PRODUCTION_CHECKLIST.md   # Pre-deployment security checklist
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_SECRET_KEY` | Flask session secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key (GPT-4o-mini) | Yes |
| `GOOGLE_API_KEY` | Google Gemini API key (2.5 Flash) | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes (Production) |
| `SMTP_HOST` | Email server (smtp.gmail.com) | Yes |
| `SMTP_PORT` | Email port (587) | Yes |
| `SMTP_USER` | Gmail address | Yes |
| `SMTP_PASSWORD` | Gmail App Password | Yes |
| `SMTP_FROM` | From email address | Yes |
| `APP_URL` | Application URL | Yes (Production) |
| `RECAPTCHA_SITE_KEY` | reCAPTCHA v3 site key | Optional |
| `RECAPTCHA_SECRET_KEY` | reCAPTCHA v3 secret key | Optional |

### Supported Accounts

- Cash
- BCA
- Maybank
- Seabank
- Shopeepay
- Gopay
- Jago
- ISaku
- Ovo
- Superbank
- Blu Account (saving)

## 🚀 Deployment

### Deploy to Render

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy: Production ready"
git push origin main
```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

3. **Set environment variables** in Render dashboard:
   - `FLASK_SECRET_KEY` - Random secret key for session management
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `GOOGLE_API_KEY` - Your Google Gemini API key
   - `DATABASE_URL` - PostgreSQL connection string (auto-set by Render)
   - `SMTP_HOST` - smtp.gmail.com
   - `SMTP_PORT` - 587
   - `SMTP_USER` - Your Gmail address
   - `SMTP_PASSWORD` - Gmail App Password
   - `SMTP_FROM` - Same as SMTP_USER
   - `APP_URL` - https://smartbudget-assistant.onrender.com

> **Important:** Review [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) before deploying to production

4. **Deploy!** Render will automatically deploy your app

## 🧪 Testing

The project includes comprehensive testing scripts in `backend/archive/`:

- `test_chat_api.py` - API endpoint testing
- `test_debug_prints.py` - Debug print validation
- `test_db_execution.py` - Database operation testing

Run tests:
```bash
cd backend/archive
python test_chat_api.py
```

## 📝 API Documentation

### Authentication Endpoints

**POST /register**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**POST /verify-otp**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**POST /login**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**POST /forgot-password**
```json
{
  "email": "user@example.com"
}
```

**POST /reset-password**
```json
{
  "token": "reset-token-from-email",
  "new_password": "new_secure_password"
}
```

### Chat Endpoint

**POST /chat**
```json
{
  "message": "catat pengeluaran makan 50rb",
  "provider": "openai",  // or "gemini"
  "language": "id"       // id or en
}
```

### Transaction Endpoints

- `GET /transactions` - Get all transactions
- `GET /transactions/summary` - Monthly summary
- `POST /transactions` - Create transaction
- `PUT /transactions/<id>` - Update transaction
- `DELETE /transactions/<id>` - Delete transaction

### Savings Goals Endpoints

- `GET /savings_goals` - Get all goals
- `POST /savings_goals` - Create goal
- `PUT /savings_goals/<id>` - Update goal
- `DELETE /savings_goals/<id>` - Delete goal

## 🐛 Troubleshooting

### Database Issues
```bash
cd backend
python -c "from database import init_db; init_db()"
```

### API Key Errors
- Verify `.env` file exists in `backend/` directory
- Check API keys are valid and have sufficient credits
- Ensure no quotes around API keys in `.env`

### Port Already in Use
```bash
# Change port in backend/main.py
app.run(host='0.0.0.0', port=8001)  # Use different port
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Muhammad Fathul Hakim**
- GitHub: [@mfathul21](https://github.com/mfathul21)
- Project: [SmartBudget-Assistant](https://github.com/mfathul21/SmartBudget-Assistant)
- Live Demo: [https://smartbudget-assistant.onrender.com](https://smartbudget-assistant.onrender.com)

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Google for Gemini API
- Flask community for excellent documentation
- All contributors and testers

## 📧 Support

For support, open an issue on [GitHub Issues](https://github.com/mfathul21/SmartBudget-Assistant/issues)

## 📚 Additional Documentation

- [EMAIL_SETUP.md](EMAIL_SETUP.md) - Gmail SMTP configuration guide
- [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) - Pre-deployment security checklist

---

⭐ **Star this repo if you find it helpful!** ⭐
