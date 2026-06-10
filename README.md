# Restorate – Restaurant & Facility Rating Platform

Restorate is a web-based review platform that helps users discover and evaluate restaurants and other facilities such as cafés, hotels, parks, and cinemas. It also allows facility owners to manage their establishments and improve their services based on user feedback.

## Project Description

This project provides a structured platform where owners can add and manage their facilities, while users can search, filter, review, rate, and save their favorite places. The system supports role-based access, allowing each type of user to interact with the platform according to their permissions.

## Features

- User and owner registration and login
- Role-based access control for guests, users, and owners
- Facility discovery through search and filtering
- Filtering by facility type, category, and minimum rating
- Facility details page with rating summaries and review statistics
- Owner dashboard for managing facilities
- Add, edit, and delete facilities by owners
- Facility image upload support
- User rating system based on:
  - Service quality
  - Food quality
  - Mood / atmosphere
- Comments on ratings
- Likes on user reviews
- Favorites list for users
- Automatic rating average calculation
- SQLite database integration

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, Flask-SQLAlchemy
- **Forms & Validation:** Flask-WTF, WTForms
- **Sessions:** Flask-Session
- **Frontend:** HTML, CSS, Jinja2 Templates
- **Security:** Password hashing using Werkzeug
- **Architecture:** Repository pattern, Service layer, Strategy pattern, State pattern

## Project Structure

```text
Resturant-ratings/
│
├── app/
│   ├── forms/              # WTForms used for login, registration, facility, and rating forms
│   ├── models/             # Database models
│   ├── repositories/       # Data access layer
│   ├── routes/             # Flask routes and blueprints
│   ├── services/           # Business logic layer
│   ├── States/             # Role/state-based behavior
│   ├── strategies/         # Filtering strategies
│   ├── static/             # CSS and uploaded facility images
│   └── templates/          # HTML templates
│
├── app.py                  # Application entry point
├── requirements.txt        # Project dependencies
└── instance/               # SQLite database location
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
cd REPOSITORY-NAME
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

For macOS / Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000/
```

## Usage

### As a Guest

- Browse the home page
- Search and filter facilities
- View facility details and rating summaries

### As a User

- Create a user account
- Log in
- Rate facilities
- Add comments to reviews
- Like reviews
- Save facilities to favorites

### As an Owner

- Create an owner account
- Log in to the owner dashboard
- Add new facilities
- Edit facility information
- Delete facilities owned by the account

## Database

The project uses SQLite through Flask-SQLAlchemy. When the application starts, the database tables are created automatically, and the main roles are initialized:

- user
- owner
- admin

## Notes

Before publishing the project on GitHub, it is recommended to exclude unnecessary local files such as:

```text
venv/
__pycache__/
*.pyc
flask_session/
instance/*.db
.env
```

## Future Improvements

- Add an admin dashboard
- Improve UI responsiveness
- Add pagination for facilities and reviews
- Add advanced search by location and price range
- Add profile pages for users and owners
- Add image management for multiple facility photos

## License

This project is currently not licensed.
