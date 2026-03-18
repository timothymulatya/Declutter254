# Declutter254

https://declutter254-giqb.onrender.com

Declutter254 is a community-driven platform designed to connect people with extra items they no longer need to those who can put them to good use. Our goal is to reduce waste and foster a culture of giving.

## Key Features

- **Mobile-First Design**: A premium, responsive user interface optimized for mobile devices.
- **Secure Authentication**: User registration and login powered by JWT (JSON Web Tokens).
- **Item Management**: 
  - Post items with titles, descriptions, conditions, and pickup locations.
  - Efficient listing with server-side **pagination** and **sorting** (Newest, Popular, etc.).
  - Dynamic **search and filtering** by categories.
- **Request System**: 
  - Express interest in items with personalized messages.
  - Item owners can track, approve, or reject incoming requests.
- **Real-time Status Tracking**: Instantly see how many people are interested in an item.

## Tech Stack

### Frontend
- **React**: Modern UI component library.
- **React Router**: For seamless navigation.
- **Formik & Yup**: Robust form handling and validation.
- **Vanilla CSS**: Premium mobile-first styling with a custom design system.

### Backend
- **Flask**: Lightweight Python web framework.
- **SQLAlchemy**: Powerful ORM for database interactions.
- **Flask-JWT-Extended**: Secure user authentication.
- **Alembic/Flask-Migrate**: Database version control and migrations.
- **SQLite**: Reliable local development database.

## Installation and Setup

To get started with Declutter254, follow these steps to set up the application and its required data.

### Forking and Cloning

1. **Fork** the repository on GitHub.
2. **Clone** your fork to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Declutter254.git
   cd Declutter254
   ```

### Backend Setup

1. **Navigate** to the backend directory:
   ```bash
   cd backend
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Create a `.env` file in the `backend` directory and add your configuration. You can use the provided `.env.example` as a template:
   ```bash
   cp .env.example .env
   ```
5. **Run migrations** and initialize the database:
   ```bash
   flask db upgrade
   ```
6. **Seed the database** with initial data:
   ```bash
   python seed_data.py
   ```
7. **Start the backend server**:
   ```bash
   python app.py
   ```
   *The API will be available at `http://localhost:5555`*

### Frontend Setup

1. **Navigate** to the frontend directory:
   ```bash
   cd frontend/client
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Start the development server**:
   ```bash
   npm start
   ```
   *The app will be available at `http://localhost:3000`*

## Testing

To run backend unit tests:
```bash
cd backend
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Trigger redeploy
