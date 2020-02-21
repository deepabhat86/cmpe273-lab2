from flask import Flask, escape, request
import random 
from random import randint

app = Flask(__name__)

DB = {		 
		 "students":{},
	     "classes":{}
}

RAND_MAX=10000
RAND_MIN=1

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students', methods=['POST'])
def create_student():
    content = request.json
    name = content["name"]
    id = random.randint(RAND_MIN,RAND_MAX)
    DB["students"].update({id:name})
    return {'id' : id ,"name" : DB["students"].get(id) },201


@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    if id in DB["students"]:
        return {'id' : id ,"name" : DB["students"].get(id) },201
    else:
        return {"error": "student not found"}


@app.route('/classes', methods=['POST']) 
def create_class():
    content = request.json
    name = content["name"]
    id = random.randint(RAND_MIN,RAND_MAX)
    DB["classes"].update({id:[name,[]]})
    return {'id':id , "name" : name , "students":[] },201


@app.route('/classes/<int:id>',methods=['GET'])
def get_class(id):
    if id in DB["classes"]:
        output_students=[]
        for student in DB["classes"].get(id)[1]:
            for key in student:
                output_students.append({"id":key, "name":student.get(key)})
        return {'id' : id ,"name" : DB["classes"].get(id)[0] , "students" :output_students } ,201
    else:
        return {"error": "class not found"}


@app.route('/classes/<int:id>',methods=['PATCH'])
def update_students_of_class(id):
    content = request.json
    student_id=content["student_id"]
    if not student_id in DB["students"]:
        return {"error": "student not found"}
    student_name=DB["students"].get(int(student_id))
    if not id in DB["classes"]:
        return {"error": "class not found"}
    DB["classes"].get(id)[1].append({student_id:student_name })
 
    return get_class(id)


