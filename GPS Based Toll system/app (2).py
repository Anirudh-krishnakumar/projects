from flask import Flask, render_template, request,redirect, url_for,jsonify
from datetime import datetime, timedelta
import mysql.connector
from geopy.distance import geodesic
import folium
import math
import csv
app = Flask(__name__)

# MySQL database configuration
db_config = {            ## replace it with your database details 
    'host': 'Anik005.mysql.pythonanywhere-services.com',
    'user': 'Anik005',
    'password': 'ani12345',
    'database': 'Anik005$intern'
}

# Geofence parameters (entry and exit points, and radius in kilometers)
entry_point = (37.7749, -122.4194)  # Example entry point (latitude, longitude)
exit_point = (37.7849, -122.4094)   # Example exit point (latitude, longitude)
geofence_radius_km = 2.0            # Radius in kilometers beyond entry/exit points

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['POST','GET'])
def login():
     return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        car_number = request.form['car_number']
        balance = float(request.form['balance'])
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cars (car_number, balance) VALUES (%s, %s)", (car_number, balance))
        conn.commit()
        cursor.execute("SELECT car_id, car_number, balance, transaction FROM cars")
        cars = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('index.html', cars=cars)
    else:
        return render_template('register.html')
@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        security_question = data.get('security_question')
        security_answer = data.get('security_answer')

        # Append the new user's data to the CSV file
        with open('static/login.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([username, password, security_question, security_answer])

        return jsonify({'message': 'Registration successful'}), 200
@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        # Implement the logic to reset the password
        # This could involve querying the database, sending an email, etc.
        return 'Password reset instructions sent to your email'
    return render_template('forgot.html')
@app.route('/update_csv', methods=['POST'])
def update_csv():
    csv_data = request.get_data(as_text=True)
    with open('static/login.csv', 'w', newline='') as csvfile:
        csvfile.write(csv_data)
    return 'CSV file updated successfully', 200
@app.route('/index',methods=['POST','GET'])
def root():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT car_id, car_number, balance,transaction FROM cars")
        cars = cursor.fetchall()
    except mysql.connector.Error as e:
        cars = []
        print(f"Database error: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return render_template('index.html',  cars=cars)


# Flask route for handling requests
@app.route('/add', methods=['GET', 'POST'])

def index():
    car_results = []
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        gps_data_str = request.form.get('gps_data')

        if car_id and gps_data_str:
            gps_data_list = gps_data_str.split(';')
            gps_data = []
            for i, coord in enumerate(gps_data_list):
                if coord.strip():  # Check if coordinate string is not empty or whitespace
                    try:
                        lat, lon = map(float, coord.split(','))
                        timestamp = datetime.now() + timedelta(minutes=i)
                        gps_data.append((car_id, timestamp, lat, lon))
                    except ValueError:
                        return "Invalid coordinate format", 400

            try:
                conn = connect_db()
                cursor = conn.cursor()

                # Insert GPS data into gps_data table
                insert_query = "INSERT INTO gps_data (car_id, timestamp, latitude, longitude) VALUES (%s, %s, %s, %s)"
                cursor.executemany(insert_query, gps_data)
                conn.commit()

                # Plotting vehicle route using Folium
                plot_html = plot_route(gps_data, entry_point, exit_point)

                # Calculating total distance traveled with geofencing
                total_distance, total_distance_within_geofence = calculate_distance_traveled(gps_data, entry_point, exit_point, geofence_radius_km)
                rate_per_km = 0.10  # Example rate per kilometer
                total_toll = total_distance * rate_per_km

                # Retrieve car balance and update
                select_query = "SELECT car_id, car_number, balance, transaction FROM cars WHERE car_id = %s"
                cursor.execute(select_query, (car_id,))
                result = cursor.fetchone()

                if result:
                    car_results.append({
                        'car_id': result[0],
                        'car_number': result[1],
                        'balance': result[2],
                        'transaction': result[3],
                        'total_distance': total_distance_within_geofence,  # Displaying distance within geofence
                        'total_toll': total_toll,
                        'new_balance': result[2] - total_toll,
                        'plot_html': plot_html
                    })

                    # Update balance after deducting toll
                    update_query = "UPDATE cars SET balance = %s WHERE car_id = %s"
                    cursor.execute(update_query, (result[2] - total_toll, car_id))
                    conn.commit()

                else:
                    return "Car ID not found", 404

            except mysql.connector.Error as e:
                conn.rollback()
                return f"Database error: {str(e)}", 500
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

        else:
            return "Invalid input", 400

    # Fetch all cars for transaction history
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT car_id, car_number, balance, transaction FROM cars")
        cars = cursor.fetchall()
    except mysql.connector.Error as e:
        cars = []
        print(f"Database error: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    name = request.args.get('name') 
    return render_template('index.html',name=name, car_results=car_results, cars=cars)

# Function to fetch GPS data for a specific car from the database
def fetch_gps_data(car_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        select_query = "SELECT timestamp, latitude, longitude FROM gps_data WHERE car_id = %s"
        cursor.execute(select_query, (car_id,))
        gps_data = cursor.fetchall()

        cursor.close()
        conn.close()

        return gps_data

    except mysql.connector.Error as e:
        print(f"Error fetching GPS data: {e}")
        return []

# Flask route for displaying car details and Folium map
@app.route('/car/<int:car_id>')
def car_detail(car_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT car_id, car_number, balance FROM cars WHERE car_id = %s", (car_id,))
    car = cursor.fetchone()

    cursor.execute("SELECT latitude, longitude FROM gps_data WHERE car_id = %s ORDER BY id DESC LIMIT 1", (car_id,))
    gps_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if gps_data:
        map_html = create_map(gps_data[0], gps_data[1])
    else:
        map_html = None

    return render_template('car_detail.html', car=car, map_html=map_html)

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon]).add_to(m)
    return m._repr_html_()

# Function to plot the vehicle route using Folium
def plot_route(gps_data, entry_point, exit_point):
    try:
        map_center = [(entry_point[0] + exit_point[0]) / 2, (entry_point[1] + exit_point[1]) / 2]
        m = folium.Map(location=map_center, zoom_start=13)

        # Adding entry and exit points to the map
        folium.Marker(entry_point, popup='Entry Point', icon=folium.Icon(color='red')).add_to(m)
        folium.Marker(exit_point, popup='Exit Point', icon=folium.Icon(color='red')).add_to(m)

        # Adding vehicle path to the map if gps_data is not empty
        if gps_data:
            coords = [(point[2], point[3]) for point in gps_data if len(point) >= 4]  # Check tuple length
            folium.PolyLine(coords, color='blue', weight=2.5, opacity=1).add_to(m)

        # Adding geofence boundary to the map
        geofence_coords = get_geofence_boundary(entry_point, exit_point, geofence_radius_km)
        folium.Polygon(locations=geofence_coords, color='green', fill=True, fill_opacity=0.2).add_to(m)

        # Save map to HTML and return the HTML string
        map_html = m._repr_html_()
        return map_html

    except Exception as e:
        print(f"Error in plot_route: {str(e)}")
        return None


def plot_route1(gps_data, entry_point, exit_point):
    try:
        map_center = [(entry_point[0] + exit_point[0]) / 2, (entry_point[1] + exit_point[1]) / 2]
        m = folium.Map(location=map_center, zoom_start=13)

        # Adding entry and exit points to the map
        folium.Marker(entry_point, popup='Entry Point', icon=folium.Icon(color='red')).add_to(m)
        folium.Marker(exit_point, popup='Exit Point', icon=folium.Icon(color='red')).add_to(m)

        # Adding vehicle path to the map if gps_data is not empty
        if gps_data:
            coords = [(point[1], point[2]) for point in gps_data]  # Extract latitude and longitude
            folium.PolyLine(coords, color='blue', weight=2.5, opacity=1).add_to(m)

        # Adding geofence boundary to the map
        geofence_coords = get_geofence_boundary1(entry_point, exit_point, geofence_radius_km)
        folium.Polygon(locations=geofence_coords, color='green', fill=True, fill_opacity=0.2).add_to(m)

        # Save map to HTML and return the HTML string
        map_html = m._repr_html_()
        return map_html

    except Exception as e:
        print(f"Error in plot_route: {str(e)}")
        return None


# Function to calculate the total distance traveled with geofencing
def calculate_distance_traveled(gps_data, entry_point, exit_point, geofence_radius_km):
    total_distance = 0.0
    total_distance_within_geofence = 0.0
    for i in range(1, len(gps_data)):
        point1 = (gps_data[i-1][2], gps_data[i-1][3])  # latitude, longitude of previous point
        point2 = (gps_data[i][2], gps_data[i][3])      # latitude, longitude of current point
        distance = geodesic(point1, point2).kilometers

        # Check if both points are within the geofence boundary
        if is_within_geofence(point1, entry_point, exit_point, geofence_radius_km) and is_within_geofence(point2, entry_point, exit_point, geofence_radius_km):
            total_distance_within_geofence += distance
        elif is_within_geofence(point1, entry_point, exit_point, geofence_radius_km) or is_within_geofence(point2, entry_point, exit_point, geofence_radius_km):
            # Calculate distance within geofence for segments crossing the geofence boundary
            total_distance_within_geofence += distance * 0.5

        total_distance += distance

    return total_distance, total_distance_within_geofence

# Function to check if a point is within the geofence boundary
def is_within_geofence(point, entry_point, exit_point, radius_km):
    # Assuming a rectangular geofence for simplicity
    min_lat = min(entry_point[0], exit_point[0]) - (radius_km / 111)  # 1 degree of latitude ~ 111 km
    max_lat = max(entry_point[0], exit_point[0]) + (radius_km / 111)
    min_lon = min(entry_point[1], exit_point[1]) - (radius_km / (111 * math.cos(math.radians(point[0]))))
    max_lon = max(entry_point[1], exit_point[1]) + (radius_km / (111 * math.cos(math.radians(point[0]))))

    return min_lat <= point[0] <= max_lat and min_lon <= point[1] <= max_lon

# Function to get the geofence boundary coordinates based on entry and exit points
def get_geofence_boundary(entry_point, exit_point, radius_km):
    # Calculate midpoint between entry and exit points
    mid_lat = (entry_point[0] + exit_point[0]) / 2
    mid_lon = (entry_point[1] + exit_point[1]) / 2

    # Calculate bearing from midpoint to entry point
    bearing = math.atan2(entry_point[1] - mid_lon, entry_point[0] - mid_lat)

    # Calculate geofence boundary coordinates
    geofence_coords = []
    for angle in range(0, 360, 30):  # Adjust angle increment based on desired resolution
        lat = mid_lat + (radius_km / 111) * math.cos(math.radians(angle))
        lon = mid_lon + (radius_km / (111 * math.cos(math.radians(mid_lat)))) * math.sin(math.radians(angle))
        geofence_coords.append((lat, lon))

    # Close the geofence polygon
    geofence_coords.append(geofence_coords[0])

    return geofence_coords


def calculate_distance_traveled1(gps_data, entry_point, exit_point, geofence_radius_km):
    total_distance = 0.0
    total_distance_within_geofence = 0.0
    for i in range(1, len(gps_data)):
        point1 = (gps_data[i-1][1], gps_data[i-1][2])  # latitude, longitude of previous point
        point2 = (gps_data[i][1], gps_data[i][2])      # latitude, longitude of current point
        distance = geodesic(point1, point2).kilometers

        # Check if both points are within the geofence boundary
        if is_within_geofence1(point1, entry_point, exit_point, geofence_radius_km) and is_within_geofence1(point2, entry_point, exit_point, geofence_radius_km):
            total_distance_within_geofence += distance
        elif is_within_geofence1(point1, entry_point, exit_point, geofence_radius_km) or is_within_geofence1(point2, entry_point, exit_point, geofence_radius_km):
            # Calculate distance within geofence for segments crossing the geofence boundary
            total_distance_within_geofence += distance * 0.5

        total_distance += distance

    return total_distance, total_distance_within_geofence

# Function to check if a point is within the geofence boundary
def is_within_geofence1(point, entry_point, exit_point, radius_km):
    # Assuming a rectangular geofence for simplicity
    min_lat = min(entry_point[0], exit_point[0]) - (radius_km / 111)  # 1 degree of latitude ~ 111 km
    max_lat = max(entry_point[0], exit_point[0]) + (radius_km / 111)
    min_lon = min(entry_point[1], exit_point[1]) - (radius_km / (111 * math.cos(math.radians(point[0]))))
    max_lon = max(entry_point[1], exit_point[1]) + (radius_km / (111 * math.cos(math.radians(point[0]))))

    return min_lat <= point[0] <= max_lat and min_lon <= point[1] <= max_lon

# Function to get the geofence boundary coordinates based on entry and exit points
def get_geofence_boundary1(entry_point, exit_point, radius_km):
    # Calculate midpoint between entry and exit points
    mid_lat = (entry_point[0] + exit_point[0]) / 2
    mid_lon = (entry_point[1] + exit_point[1]) / 2

    # Calculate bearing from midpoint to entry point
    bearing = math.atan2(entry_point[1] - mid_lon, entry_point[0] - mid_lat)

    # Calculate geofence boundary coordinates
    geofence_coords = []
    for angle in range(0, 360, 30):  # Adjust angle increment based on desired resolution
        lat = mid_lat + (radius_km / 111) * math.cos(math.radians(angle))
        lon = mid_lon + (radius_km / (111 * math.cos(math.radians(mid_lat)))) * math.sin(math.radians(angle))
        geofence_coords.append((lat, lon))

    # Close the geofence polygon
    geofence_coords.append(geofence_coords[0])

    return geofence_coords

@app.route('/logout')
def lo():
     return redirect(url_for('login'))


# Error handler for internal server errors
@app.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5007)
