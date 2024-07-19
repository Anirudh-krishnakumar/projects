# GPS Toll-Based Simulation Project

This project simulates a system to calculate toll charges based on vehicle locations using GPS data. It is designed for end users managing toll data, such as vehicle details, available balances, and last logged GPS data. The project uses Python and MySQL, with Flask for handling requests (GET and POST), Geopy for distance calculations, Folium for updating car balance details, and MySQL Connector for database interactions. An interactive web UI makes it easy for government employees to use.

## Team Members
- Jaaswin S
- Anirudh K
- Edward Samuel L
- Gokul P

## How It Works

1. **Car Registration**: Register your car in the system.
2. **GPS Tracking**: The system tracks the location of registered cars using GPS data.
3. **Toll Calculation**: Tolls are calculated based on the location of the car.
4. **Backend Data Storage**: All data are stored in a backend database for future reference.

## Requirements
- Python (latest version recommended)
- MySQL database (database schema provided in the project)
- Proper web browser (works best on Google Chrome, other browsers are also supported)

## How to Use

1. **Clone the Project Repository**:
   - Open your terminal (Command Prompt, Git Bash, etc.).
   - Navigate to the directory where you want to clone the project.
   - Use the following command to clone the repository:
     ```sh
     git clone https://github.com/JASWINCKS/GPS-Toll-based-System-Simulation.git
     ```

2. **Install Dependencies**:
   - Ensure you have Python and pip installed on your system.
   - Navigate to the cloned project directory:
     ```sh
     cd GPS-Toll-based-System-Simulation
     ```
   - Install the dependencies listed in `requirements.txt` using pip:
     ```sh
     pip install -r requirements.txt
     ```

3. **Database Configuration**:
   - The Data base schema is provide as db schema.txt.
   - Implement the database.
   - Update the database details in the app(2).py file.
   ```sh
    db_config = {
    'host': '<host>',
    'user': '<username>',
    'password': '<password>',
    'database': '<database Name>'}
   ```
   
4. **Start the Application**:
   - Use the following command to start the application:
     ```sh
     python app(2).py
     ```

5. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:5000/`.
   - Log in using your username and password. If you are a new user, proceed with the registration process and follow the on-screen instructions to register and then log in with your username and password.
   - After logging in, you will be redirected to the home page of the application. Enjoy using the application!

## Important Notes

1. **Ensure Password Security**:
   - Make sure your passwords are secure. Use a combination of letters, numbers, and special characters.
   - Avoid using easily guessable information such as birthdays or common words.

2. **Set a Strong Secret Key**:
   - A strong secret key is essential to protect your login sessions.
   - In the Flask application, you can set the secret key in the configuration file. For example:
     ```python
     app.config['SECRET_KEY'] = 'your_strong_secret_key'
     ```
   - Make sure the secret key is complex and kept confidential.

3. **Database Flexibility**:
   - The project uses a simple MySQL database. However, you can modify the database schema if needed.
   - If you prefer using a different database system, such as PostgreSQL or SQLite, you can update the database connection settings and modify the SQL queries accordingly.

## Conclusion

This GPS Toll-Based Simulation Project provides a robust solution for managing toll data based on vehicle locations using GPS. With its user-friendly interface and secure data handling, it is an efficient tool for government employees to manage toll operations seamlessly.
