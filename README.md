# Exam Cell Automation System 🎓

[![Django](https://img.shields.io/badge/Backend-Django%204.2-green?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018-blue?style=for-the-badge&logo=react)](https://reactjs.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
---

# Exam Cell Automation System 🎓

## 👥 The Team

* **Youssef Hassan** (231001243)
* **Omar Hany** (231001556)
* **Seif Sheriff** (231001332)
* **Mario Sameh** (231001484)

---

## 📌 Project Overview

The **Exam Cell Automation System** is a modular web platform designed to digitize and automate university examination cell operations. It eliminates manual paperwork by providing automated hall ticket generation, marksheet publishing, and a centralized communication hub using a modern **React-Django** stack.

## 🚀 Core Features

* **Secure Authentication:** Student registration and admin login using **JWT** (JSON Web Tokens) and role-based access control (RBAC).
* **Automated Emailing:** Trigger-based welcome emails upon registration and automated exam schedule alerts via SMTP.
* **Digital Document Management:** Automated generation of Hall Tickets and digital publishing of Marksheets for instant student access.
* **Bidirectional Communication:** A dedicated inquiry system allowing students to message administrators directly through their dashboard.

---

## 🛠 Project Structure

```text
exam-cell-automation/
├── backend/                # Django Project Root
│   ├── accounts/           # User registration & Auth (JWT)
│   ├── emailservice/       # SMTP Logic & HTML Templates
│   ├── student/            # Student profiles & dashboard logic
│   ├── hallticket/         # PDF/Digital ticket generation
│   ├── marksheets/         # Grade management & publishing
│   └── adminpanel/         # Unified administrative dashboard
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   └── services/       # Axios API configurations
└── README.md

```

---

## ⚙️ Setup Instructions

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver

```

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React application
npm start

```

---

## 📊 System Requirements & KPIs

* **Performance:** Optimized REST API with response times under **300ms**.
* **Security:** Industry-standard password hashing (Argon2/BCrypt) and JWT session management.
* **Reliability:** Redundant SMTP configuration ensuring a **95%+ email delivery rate**.

---

## 🛡 License

This project is developed for academic purposes.

---
