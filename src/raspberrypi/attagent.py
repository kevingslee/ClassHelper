import requests

BASE = "http://192.168.1.176:5000/"

#api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:test>")
#api.add_resource(UpdateStudentData, "/updatestudentdata/<string:name>/<string:data>", )
#api.add_resource(StudentList, "/studentlist")
#api.add_resource(StudentData, "/studentdata/<string:name>")

#response = requests.get(BASE + "helloworld/hank/46")
response = requests.post(BASE + "updatestudentdata/hanklee/112")
print(response.json())
response = requests.get(BASE + "studentlist")
print(response.json())
response = requests.get(BASE + "studentdata/hanklee")
print(response.json())
