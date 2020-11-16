import psycopg2
from flask import Flask, request, redirect, url_for, render_template, session

try:
    connection = psycopg2.connect(user="postgres",
                                  password="olalacik1",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="av_dataprocessing_finalassignment")

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
            return render_template("index.html")
            
    @app.route("/map")
    def map():   
            cursor.execute("select gps_x, gps_y from vehicle")
            location = cursor.fetchall()
            return render_template("map.html")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # Closing database connection
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

