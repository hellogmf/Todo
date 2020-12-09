from flask import Flask,render_template,request,session
import sqlite3 as sql
app = Flask(__name__)

app.config["SECRET_KEY"]="Prisha"
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",title="Shaurya favourite city")
    
@app.route("/quizlogin")
def quizlogin():
    return render_template("login.html")





@app.route("/login",methods= ["GET", "POST"])
def login():
    if session.get("authenticated") ==True:
        # return render_template("loginSuccess.html")
        return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/start_quiz")
def start_quiz():
    if session.get("authenticated") ==True:
        session["score"]=0
        return render_template("q1.html", score = 0)
    else:
        return render_template("loginfailure.html")
   

@app.route("/verify",methods=['POST','GET'])
def verify():
    username=request.form.get("username")
    password=request.form.get("password")
    # returnvale=loginsucess(user_details,username,password)
    returnvale=verifyuser(username,password)

      
    if(returnvale==True):
        session["authenticated"]=True
        return render_template("loginSucess.html",username=username)
    else:
        session["authenticated"]=False
        return render_template("loginfailure.html")

@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/register_verify",methods=['POST','GET'])
def register_verify():
    print("adding the user", request.method)
    message=""
    if request.method =='POST':
        try:
            username=request.form["username"]
            password=request.form["password"]
            firstname=request.form["firstname"]
            lastname=request.form["lastname"]
            email=request.form["email"]
            phonenumber=request.form["phonenumber"]
            print(username)
            with sql.connect("database.db") as con  :
                cur=con.cursor()
                print("database created")
                cur.execute("INSERT into user(username,password,firstname,lastname,email,phonenumber) VALUES(?,?,?,?,?,?)",(username,password,firstname,lastname,email,phonenumber))
                con.commit 
                print("commited")
                message = "Opeartion successfull"
        except Exception as e  :
             con.rollback()
             message = "Operation unsuccessful " +e.message
             return render_template("register_result.html", message = message)
        finally:
            con.close()
            return render_template("register_result.html", message = message)


@app.route("/showuser",methods=["POST","GET"])
def showuser():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user")
    records=cur.fetchall()
    print("record",records)
    return render_template("listuser.html",records=records)
    

def verifyuser(username,password):
    loginsucess=False
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    print (username)
    cur=con.cursor()
    cur.execute("select password from user where username=?",[username])
    records=cur.fetchall()
    dbpassword=""
    for record in records:
            dbpassword=record[0]
    print(password)
    if(dbpassword==password):
        loginsucess=True
    else:
        loginsucess=False
    return loginsucess
        

def loginsucess(dictionary,username,password):
    if (dictionary.get(username,"Invaild details")==password):
        return True
    else:
        return False 


@app.route ("/aboutme")
def aboutme():
    return render_template("aboutme.html")

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("404.html")


@app.route("/createtask")
def createtask():
    return render_template("Create_task.html")  

@app.route("/addtask" ,methods=["POST","GET"])
def addtask():
    print("adding the user", request.method)
    message=""
    if request.method =='POST':
        try:
            task_name=request.form["task_name"]
            priority=request.form["priority"]
            with sql.connect("database.db") as con  :
                cur=con.cursor()
                print("database created")
                cur.execute("INSERT into todo(task_name,priority) VALUES(?,?)",(task_name,priority))
                con.commit ()
                print("commited")
                message = "Opeartion successfull"
        except Exception as e  :
             con.rollback()
             message = "Operation unsuccessful " +e.message
             return render_template("register_result.html", message = message)
        finally:
            con.close()
            return render_template("addtask.html", message = message)  

@app.route("/viewtodo",methods=["POST","GET"])
def viewtodo():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from todo")
    records=cur.fetchall()
    print("record",records)
    return render_template("viewtodo.html",records=records)
      
@app.route("/deletetodo")
def deletetodo():
    id=request.args.get("id")
    con=sql.connect ("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("delete from todo where id=?",(id))
    con.commit()
    message="Todo deleted sucessfully"
    return render_template("deletetodo.html",message=message)

@app.route("/completetodo")
def completetodo():
    id=request.args.get("id")
    con=sql.connect ("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("update todo set status=? where id=?",("completed",id))           
    con.commit()
    message="Todo completed sucessfully"
    return render_template("completetodo.html",message=message)



if __name__ == '__main__': 
    app.run(debug=True)