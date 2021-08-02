from flask import Flask, redirect, url_for, request, render_template, jsonify
import csv

# Initialize Flask App
app = Flask(__name__)

database = {'admin':'123', 'abhi':'aac'}
filename = 'data.csv'

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login',methods=['POST','GET'])
def login():
    uname=request.form['username']
    pwd=request.form['password']
    if uname not in database:
	    return render_template('login.html', info='Invalid User')
    else:
        if database[uname] != pwd:
            return render_template('login.html',info='Invalid Password')
        else:
	        return render_template('webpage.html', user = uname)

def read_data_csv():
    res_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            res_data.append(row)
    return res_data

@app.route('/addData',methods=['POST'])
def Adding_data():
    data =  request.form['data']
    res_data = read_data_csv()
    if len(res_data) > 0:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            try:
                for i in range(len(res_data)):
                    writer.writerow(res_data[i])
            except:
                print("no data previously")
            writer.writerow([data])
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])
    return render_template('webpage.html',info='data added')

@app.route('/display')
def display():
    res_data = read_data_csv()
    return render_template("output.html", data = res_data)

@app.route('/delete')
def delete():
    with open(filename, 'w', newline='') as file:
        csv.writer(file)
    return render_template('output.html',info='data deleted')

# @app.route('/update/<int:id>',methods=['GET', 'POST'])
# def update(id):
#     if request.method =='POST':
#         data3 =  request.form['new_data2']
#         cur = mysql.connection.cursor()
#         cur.execute("UPDATE dolist SET data=%s where id=%s ",(data3,id))
#         mysql.connection.commit()
#         cur.close() 
#     return redirect('/display') 


if __name__ == "__main__":
    app.run(debug = True)
