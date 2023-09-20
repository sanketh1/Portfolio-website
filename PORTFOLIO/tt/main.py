from flask import Flask, render_template, request
import os
from pymongo import MongoClient

app = Flask(__name__)
mongo_uri = "mongodb://localhost:27017" 

try:
    client = MongoClient(mongo_uri)
    db = client["Cha"]

except Exception as e:
    print(f"Error: {e}")
finally:
    print("Connected to MongoDB")

@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route('/handle_subs', methods=['POST'])
def handle_subs():
    collection = db["cha"]
    if request.method == 'POST':
        existing_record = collection.find_one({"email": request.form['email']})
        if not existing_record:
            useremail = request.form['email']
            collection = db["cha"]
            document = {
                "email": useremail,
                'messages' : []
            }
            result = collection.insert_one(document)
            print(f"Inserted document ID: {result.inserted_id}")
    return render_template('index.html')

@app.route("/gallery")
def gallery():
    info = []
    for file in os.listdir('static/images'):
        info.append(os.path.join('static/images', file))
    return render_template('gallery.html', links=info)

@app.route('/blog')
def blog():
    collection = db["cha"]
    top_15_names = collection.find()
    len_ = 0
    for i in top_15_names:
        len_+=1
    return render_template('blog.html',names = len_)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contactmsg',methods=['POST'])
def contactmsg():
    if request.method == 'POST':
        collection = db["cha"]
        useremail = request.form['email']
        usermsg = request.form['msg']
        existing_record = collection.find_one({"email": useremail})

        if existing_record:
            collection.update_one({"email": useremail}, {"$push": {"messages": usermsg}})
        else:
            new_record = {
                "email": useremail,
                "messages": [usermsg]
            }
            collection.insert_one(new_record)
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
    client.close() 
