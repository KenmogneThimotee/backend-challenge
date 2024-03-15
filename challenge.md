## Documentation: How to Pull and Run a Django Project

This documentation will guide you through the process of pulling and running a Django project from a version control repository.

### Prerequisites

- Python installed on your system
- pip installed
- Git installed on your system
- virtualenv

### Step 1: Clone the Repository

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to store your Django project.
3. Use the `git clone` command to clone the repository.
   ```bash
   git clone https://github.com/KenmogneThimotee/backend-challenge.git
   ```

### Step 2: Set Up a Virtual Environment

1. Navigate into the project directory.

   ```bash
   cd backend-challenge
   ```
2. Create a virtual environment using `virtulaenv`.

   ```bash
   virtualenv venv
   ```
3. Activate the virtual environment.

   On Windows:

   ```
   venv\Scripts\activate
   ```

   On macOS and Linux:

   ```
   source venv/bin/activate
   ```

### Step 3: Install Dependencies

1. Ensure that your virtual environment is activated.
2. Use `pip` to install the project dependencies listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Migrate the Database

1. Run the following command to apply migrations and set up the database.
   ```bash
   python manage.py migrate
   ```

### Step 5: Run the Development Server

1. Start the Django development server using the following command:
   ```bash
   python manage.py runserver
   ```
2. Open a web browser and navigate to `http://127.0.0.1:8000/` to view your Django project.

### Step 6: Access the Admin Panel

1. Log in to the Django admin panel by visiting `http://127.0.0.1:8000/admin/` in your web browser.
3. User's credentials:
   1. email: user1@example.com, password: Xandercage03
   2. email user2@example.com, password: Xandercage03
