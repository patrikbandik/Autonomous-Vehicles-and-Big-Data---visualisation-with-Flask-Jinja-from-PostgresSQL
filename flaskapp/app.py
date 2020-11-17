import psycopg2
from flask import Flask, request, redirect, url_for, render_template, session

try:
    connection = psycopg2.connect(user="postgres",
                                  password="pw", 
                                  host="127.0.0.1",
                                  port="5432",              
                                  database="av_dataprocessing_finalassignment") #change name of database 

    app = Flask(__name__)
    app.secret_key = 'patoromimatotentoprojektstojizato'

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    
    @app.route("/")
    def index():
        cursor.execute("SELECT * FROM alertness ORDER BY driver_session_time ASC")
        rows = cursor.fetchall()

        stats = []

        for row in rows:
            driver_id = row[0]
            eye_poss = row[1]
            time = row[2]
            

            stats.append(list((driver_id, eye_poss, time)))

            print(F"id:{driver_id}, eye:{eye_poss}, time{time}")


        cursor.execute("SELECT * FROM vehicle")
        cows = cursor.fetchall()

        cars = []

        for cow in cows:
            driver_id_vehicle = cow[0]
            vehicle_id = cow[1]
            gps_x = cow[2]
            gps_y = cow[3]
            time = cow[4]
            speed = cow[5]

            cars.append(list((driver_id_vehicle, vehicle_id, gps_x, gps_y, time, speed)))
            
        return render_template("index.html",driver_id = driver_id ,eye_poss = eye_poss, time = time, stats = stats , driver_id_vehicle = driver_id_vehicle, vehicle_id = vehicle_id , gps_x = gps_x , gps_y = gps_y , speed = speed, cars = cars)
            
    @app.route("/map")
    def map():   
            cursor.execute("select gps_x, gps_y from vehicle")
            get = cursor.fetchall()
            location = []

            for row in get:
                gps_x = row[1]
                gps_y = row[0]
    
                location.append(list((gps_x, gps_y)))
            print(F"gps_x:{gps_x}, gps_y:{gps_y}")
            markers = location
                
            return render_template("map.html", gps_x = gps_y, gps_y = gps_x, location = location, markers = markers)

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
