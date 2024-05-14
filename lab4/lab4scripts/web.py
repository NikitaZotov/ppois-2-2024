from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/turnedOn')
def about():
    return render_template("index2.html")


@app.route('/turnedOn/entertainment')
def entertainment():
    return render_template("index3.html")


@app.route('/turnedOn/sports')
def sports():
    return render_template("index4.html")


@app.route('/turnedOn/culinary')
def culinary():
    return render_template("index5.html")


@app.route('/turnedOn/childrens')
def children():
    return render_template("index6.html")


@app.route('/tvInfo')
def display_television_data():
    conn = sqlite3.connect('templates/television_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM TelevisionInfo")
    tv_data = c.fetchall()

    conn.close()

    return render_template('index7.html', tv_data=tv_data)


@app.route('/controleInfo')
def display_remote_controle_data():
    conn = sqlite3.connect('templates/controle_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM ControleInfo")
    controle_data = c.fetchall()

    conn.close()

    return render_template('index8.html', controle_data=controle_data)


@app.route('/technicalInfo')
def display_technical_data():
    conn = sqlite3.connect('templates/technical_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Technical_Info")
    technical_data = c.fetchall()

    conn.close()

    return render_template('index9.html', technical_data=technical_data)


@app.route('/turnedOn/graphicInfo')
def graphic():
    conn = sqlite3.connect('templates/graphical_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Graphical_Info")
    graphical_data = c.fetchall()

    conn.close()

    return render_template("index10.html",  graphical_data=graphical_data)


@app.route('/turnedOn/changeGraphicInfo')
def newGraphic():
    os.system('python ../lab1scripts/New_Graphical_database.py')
    conn = sqlite3.connect('templates/graphical_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Graphical_Info")
    graphical_data = c.fetchall()

    conn.close()

    return render_template("index11.html",  graphical_data=graphical_data)


@app.route('/turnedOn/soundLevel')
def sound():
    conn = sqlite3.connect('templates/sound_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Sound_Info")
    sound_data = c.fetchall()

    conn.close()

    return render_template("index12.html",  sound_data=sound_data)


@app.route('/turnedOn/newSoundLevel')
def newSound():
    os.system('python ../lab1scripts/New_Sound_database.py')
    conn = sqlite3.connect('templates/sound_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Sound_Info")
    sound_data = c.fetchall()

    conn.close()

    return render_template("index13.html",  sound_data=sound_data)


if __name__ == "__main__":
    app.run(debug=True)
