🧠 NoteVault Backend API
The robust REST API powering NoteVault, built with Django and Django REST Framework (DRF). It handles secure data storage, JWT authentication, and advanced query filtering.

🚀 Tech Stack
1.Framework: Django 5.0+

2.API: Django REST Framework

3.Authentication: SimpleJWT (JSON Web Tokens)

4.Database: SQLite (Development)

5.Documentation: drf-spectacular (Swagger/OpenAPI 3.0)


🧠 NoteVault Backend API
The robust REST API powering NoteVault, built with Django and Django REST Framework (DRF). It handles secure data storage, JWT authentication, and advanced query filtering.

🚀 Tech Stack
Framework: Django 5.0+

API: Django REST Framework

Authentication: SimpleJWT (JSON Web Tokens)

Database: SQLite (Development)

Documentation: drf-spectacular (Swagger/OpenAPI 3.0)

🛠️ Features
1.JWT Auth: Secure token-based authentication with Login, Signup, and Logout (Blacklist).

2.CRUD Operations: Full Create, Read, Update, and Delete endpoints for Notes and Categories.

3.Advanced Filtering: * Search: Full-text search across titles and content.

4.Category Filter: Filter notes by specific category IDs.

5.Ordering: Sort by date created or title.

6.Owner Isolation: Users can only view, edit, or delete data they created.

7.Auto-Pagination: Results are paginated (6 items per page) to ensure fast load times.

📦 Backend Installation
1. Clone & Navigate:
    git clone https://github.com/Nabin9817/Notes.git
    cd backend

2. Setup Virtual Environment:
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate

3.Install Dependencies:
    pip install -r requirements.txt

4.Run Migrations:
    python manage.py makemigrations
    python manage.py migrate

5.Start Server:
    python manage.py runserver

📖 API Documentation
    Swagger UI: http://localhost:8000/api/docs/

