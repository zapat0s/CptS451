from flask import Flask, render_template
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'yelpdata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/reviews/")
def reviews_view(): # TODO: allow business_id to be specified
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM Businesses WHERE business_id = 'IK8ID-Dq7LZsPppx4sKLhg'")
    business = cursor.fetchone()
    cursor.execute("SELECT * FROM Reviews WHERE business_id = 'IK8ID-Dq7LZsPppx4sKLhg' ORDER BY review_date")
    reviews = cursor.fetchall()
    cursor.execute("SELECT * FROM Checkins WHERE business_id = 'IK8ID-Dq7LZsPppx4sKLhg' ORDER BY day_time")
    checkins = cursor.fetchall()
    cursor.execute("SELECT Businesses.business_id, name, city, category, stars, review_count, latitude, longitude FROM Businesses INNER JOIN BusinessCategories ON Businesses.business_id = BusinessCategories.business_id WHERE category = 'Donuts' AND latitude BETWEEN (" + str(business[5]) + " - 0.15) AND (" + str(business[5]) + " + 0.15) AND longitude BETWEEN (" + str(business[6]) + " - 0.15) AND (" + str(business[6]) + " + 0.15) ORDER BY stars DESC, review_count DESC")
    competition = cursor.fetchall()
    return render_template('reviews.html', business=business, reviews=reviews, checkins=checkins, competition=competition)

@app.route("/area/")
def area_view(): # TODO allow category and location to be specified
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT Businesses.business_id, name, city, category, stars, review_count, latitude, longitude FROM Businesses INNER JOIN BusinessCategories ON Businesses.business_id = BusinessCategories.business_id WHERE category = 'Bikes' AND latitude BETWEEN (33.4500 - 0.15) AND (33.45000 + 0.15) AND longitude BETWEEN (-112.0667 - 0.15) AND (-112.0667 + 0.15) ORDER BY stars DESC, review_count DESC")
    nearby_bussinesses = cursor.fetchall()
    #cursor.execute("SELECT * FROM Reviews WHERE business_id = 'IK8ID-Dq7LZsPppx4sKLhg' ORDER BY review_date")
    #reviews = cursor.fetchall()
    #cursor.execute("SELECT * FROM Checkins WHERE business_id = 'IK8ID-Dq7LZsPppx4sKLhg' ORDER BY day_time")
    #checkins = cursor.fetchall()
    return render_template('area.html', nearby_bussinesses=nearby_bussinesses)

if __name__ == '__main__':
    app.run()
