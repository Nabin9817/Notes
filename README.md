# 🧠 NoteVault Backend API

The robust REST API powering NoteVault, built with **Django** and **Django REST Framework (DRF)**. It handles secure data storage, JWT authentication, and advanced query filtering.

## 🚀 Tech Stack

* **Framework:** [Django 5.0+](https://www.djangoproject.com/)
* **API Toolkit:** [Django REST Framework](https://www.django-rest-framework.org/)
* **Authentication:** SimpleJWT (JSON Web Tokens)
* **Database:** SQLite (Development)
* **Documentation:** drf-spectacular (Swagger/OpenAPI 3.0)

## 🛠️ Features

* **🔐 JWT Auth:** Secure token-based authentication (Login, Signup, Logout with Blacklisting).
* **📝 CRUD Operations:** Full endpoints for managing Notes and Categories.
* **🔍 Advanced Filtering:**
  - **Search:** Full-text search across titles and content.
  - **Category Filter:** Filter notes by specific category IDs.
  - **Ordering:** Sort dynamically by date created or title.
* **🛡️ Owner Isolation:** Strict permission classes ensure users only access their own data.
* **📄 Auto-Pagination:** Results are paginated (6 items per page) for optimized performance.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:
* **Python:** `v3.13.2`

## 📦 Backend Installation

### 1. Clone & Navigate
```bash
git clone [https://github.com/Nabin9817/Notes.git](https://github.com/Nabin9817/Notes.git)
cd Notes
```
### 2. Setup Virtual Environment
```bash
python -m venv .venv
```
### Windows:
```bash
.venv\Scripts\activate
```
### Mac/Linux:
```bash
source .venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Start Server
```bash
python manage.py runserver
```
## 📖 API Documentation
Once the server is running, you can explore and test the API endpoints visually:

* Swagger UI: http://localhost:8000/api/docs/

## 🧪 Testing
The backend uses DRF's APITestCase to ensure data integrity and security.

To run the test suite, execute:
```bash
python manage.py test
```
**🔗 Frontend Repository:** This API is designed to work with the [NoteVault Frontend](https://github.com/Nabin9817/Notes_frontend.git).

Developed by [Nabin](https://github.com/Nabin9817)


