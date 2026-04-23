# 🗑️ Smart Garbage Complaint System

A production-style Django web application for citizens to report garbage and waste management issues to municipal authorities. Built with Django 5, Bootstrap 5, and SQLite.

---

## 🌟 Features

### Core Features
- 📸 **Submit Complaints** — Upload photo evidence, location, and description
- 📍 **Google Maps Integration** — Attach precise location links
- 📧 **Email Notifications** — Instant SMTP email to municipal authorities
- ✅ **Success Confirmation** — Reference number for tracking

### Advanced Features
- 📊 **Admin Dashboard** — View, search, and filter all complaints
- 🔄 **Status Tracking** — Pending → In Progress → Resolved
- 🔍 **Search & Filter** — By location, status, priority, or reference
- 🔐 **User Authentication** — Login, register, and track your complaints
- 👨‍💼 **Staff Controls** — Update complaint status and add admin remarks

### Technical Highlights
- 🎨 **Modern Dark UI** — Bootstrap 5 with glassmorphism and animations
- 📱 **Fully Responsive** — Works on desktop, tablet, and mobile
- 🛡️ **Production-Ready** — CSRF protection, input validation, error handling
- 🇮🇳 **Swachh Bharat Compatible** — Designed for future government integration

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Database Migrations
```bash
python manage.py migrate
```

### Step 3: Seed Dummy Data (Optional but Recommended)
```bash
python manage.py seed_data
```
This creates:
- **Admin account**: `admin` / `admin123`
- **Test user**: `testuser` / `test1234`
- **12 realistic complaints** from cities across India

### Step 4: Run the Development Server
```bash
python manage.py runserver
```

### Step 5: Open in Browser
- 🏠 Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📊 Dashboard: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- 📝 Submit Complaint: [http://127.0.0.1:8000/submit/](http://127.0.0.1:8000/submit/)
- ⚙️ Django Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📧 Email Configuration (Gmail SMTP)

By default, emails are printed to the terminal console. To send real emails:

1. **Enable 2-Step Verification** on your Google Account
2. **Generate an App Password** at [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. **Update your `.env` file**:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=Smart Garbage System <your.email@gmail.com>
MUNICIPAL_EMAIL=municipal.officer@yourdomain.com
```

---

## 📁 Project Structure

```
Garbage Complaint System/
├── manage.py                    # Django management entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (local)
├── .env.example                 # Environment template
├── db.sqlite3                   # SQLite database (auto-created)
│
├── garbage_project/             # Django project configuration
│   ├── settings.py              # All settings (DB, email, media, auth)
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── complaints/                  # Main application
│   ├── models.py                # Complaint model with status & priority
│   ├── views.py                 # All view functions
│   ├── urls.py                  # App URL routing
│   ├── forms.py                 # Django forms with Bootstrap styling
│   ├── admin.py                 # Custom Django admin configuration
│   ├── utils.py                 # Email notification helpers
│   └── management/commands/
│       └── seed_data.py         # Dummy data seeder
│
├── templates/                   # HTML templates
│   ├── base.html                # Master template (navbar, footer)
│   ├── home.html                # Landing page with stats
│   ├── submit_complaint.html    # Complaint form
│   ├── success.html             # Confirmation page
│   ├── dashboard.html           # Complaint listing with filters
│   ├── complaint_detail.html    # Single complaint view
│   ├── login.html               # Login page
│   └── register.html            # Registration page
│
├── static/                      # Static assets
│   ├── css/style.css            # Custom CSS (dark theme, glassmorphism)
│   └── js/main.js               # Client-side JavaScript
│
└── media/                       # User uploads (auto-created)
    └── complaints/              # Complaint images
```

---

## 🔗 Future Integration with Government Systems

This system is built with modularity for future integration with:

### Swachh Bharat Mission (SBM)
- **API Integration**: The `Complaint` model fields map directly to SBM's complaint schema
- **Auto-Forwarding**: The `utils.py` email function can be extended to push complaints via SBM APIs
- **Status Sync**: Complaint status can be synchronized with government tracking systems

### Smart City Platform
- **GIS Mapping**: Location data (text + Google Maps) enables geospatial analysis
- **Analytics Dashboard**: Aggregated complaint data for identifying garbage hotspots
- **IoT Integration**: Smart bins can auto-generate complaints when overflow sensors trigger

### CPCB (Central Pollution Control Board)
- **Environmental Reporting**: Critical priority complaints can be auto-escalated
- **Data Export**: Complaint data can be exported in CPCB-compatible formats

---

## 📸 Screenshots for PDF Submission

Suggested screenshots to capture:
1. **Home Page** — Hero section with statistics
2. **Submit Complaint Form** — Filled form with image preview
3. **Success Page** — Confirmation with reference number
4. **Dashboard** — Table view with filters applied
5. **Complaint Detail** — Full complaint with image and timeline
6. **Admin Panel** — Django admin with complaint management
7. **Login/Register** — Authentication pages
8. **Mobile View** — Responsive design on mobile viewport

---

## 🛠️ Technical Details

| Component | Technology |
|-----------|-----------|
| Backend | Django 5.x |
| Database | SQLite |
| Frontend | Bootstrap 5.3, vanilla JS |
| Font | Inter (Google Fonts) |
| Icons | Bootstrap Icons |
| Email | Gmail SMTP |
| Image Handling | Pillow |
| Image Storage | Local filesystem (media/) |
| Config | python-dotenv |

---

## 📜 License

This project is built for educational purposes and civic engagement.
Feel free to use, modify, and deploy for your community.

*Built with ❤️ for a cleaner India 🇮🇳*
