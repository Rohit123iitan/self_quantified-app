from app import *
from function import *
from model import *
import datetime
@app.route("/")
def Front_page():
    if "username" not in session:
        return render_template("login.html")
    else:
        return redirect("/dashboard")

@app.route("/dashboard")
def Dashboard():
    if "username" not in session:
        flash(f"User has'nt logged in",category="danger")
        return redirect("/login")
    return render_template("dashboard.html")
    
@app.route("/tracker_index")
def T_index():
    if "username" not in session:
        flash(f"User has'nt logged in",category="danger")
        return redirect("/login")
    trac=Tracker.query.all()
    return render_template("tracker_index.html",trac=trac)

@app.route("/registration",methods=["GET","POST"])
def User_Registration():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        mySalt = bcrypt.gensalt()
        hash1 = bcrypt.hashpw(password.encode('utf-8'), mySalt)
        add_reg(username, hash1)
        flash('Successfully Registered',category="success")
        db.session.commit()
        return redirect("/login")
    return render_template("registration.html")

@app.route("/login",methods=['GET','POST'])
def Login():
    if "username" in session:
        return redirect("/dashboard")
    if request.method=='POST':
        username=request.form.get("username")
        password=request.form.get("password")
        password=password.encode('utf-8')
        u_n=User.query.filter_by(user_name=username).first()
        if u_n != None:
            if (u_n.user_name==username):
                hash1=u_n.password
                if bcrypt.checkpw(password, hash1):
                    session['username']=username
                    return redirect("/dashboard")
                else:
                    flash(f"Incorrect Password",category="danger")
                    return render_template("login.html")
        else:
            flash(f"Incorrect Username",category="danger")
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username",None)
    session.pop("subject",None)
    flash('Successfully Logout',category="success")
    return redirect("/login")

@app.route("/Tracker_detail/<string:Name>",methods=['GET','POST'])
def T_details(Name):
    if "username" not in session:
        flash(f"User has'nt logged in",category="danger")
        return redirect("/login")
    logs=Logs.query.filter_by(Tracker_name=Name).all()
    tr=Tracker.query.filter_by(Name=Name).all()
    t=tr[0].Tracker_type
    if request.method=='POST':
        Time_stamp=request.form.get("Time_stamp")
        ct = datetime.datetime.now()
        if Time_stamp=="Today":
            gap=(ct)-datetime.timedelta(hours=24)
            d= gap.strftime("%d-%m-%Y" )
            t= gap.strftime("%H:%M:%S")
            xd=[]
            xt=[]
            y=[]
            for log in logs:
                if log.date>d or (log.date==d and log.Time>t):
                    xd.append(log.date)
                    xt.append(log.Time)
                    y.append(log.Value)
            y=graph(xd,xt,y,t,Time_stamp)
        elif Time_stamp=="This Week":
            gap=(ct)-datetime.timedelta(days=7)
            d= gap.strftime("%d-%m-%Y" )
            t= gap.strftime("%H:%M:%S")
            xd=[]
            xt=[]
            y=[]
            for log in logs:
                if log.date>d or (log.date==d and log.Time>t):
                    xd.append(log.date)
                    xt.append(log.Time)
                    y.append(log.Value)
            y=graph(xd,xt,y,t,Time_stamp)
        elif Time_stamp=="This month":
            gap=(ct)-datetime.timedelta(days=29)
            d= gap.strftime("%d-%m-%Y" )
            t= gap.strftime("%H:%M:%S")
            xd=[]
            xt=[]
            y=[]
            for log in logs:
                if log.date[4:6]>d[4:6] or (log.date[4:6]==d[4:6]  and log.date>d):
                    xd.append(log.date)
                    xt.append(log.Time)
                    y.append(log.Value)
            y=graph(xd,xt,y,t,Time_stamp)
    return render_template("Tracker_Details.html",logs=logs,Name=Name,t_type=t)
# -----------------------------------> Tracker crud <------------------------------------------
@app.route("/Add_tracker",methods=['GET','POST'])
def Add_t():
    if "username" not in session:
        flash(f"User has'nt logged in",category="danger")
        return redirect("/login")
    if request.method=='POST':
        Name=request.form.get("Name")
        Desc=request.form.get("Desc")
        Tracker_type=request.form.get("Tracker_type")
        settings=request.form.get("choice",None)
        if Tracker_type=="Multiple Choice":
            check=[',']
            if validate_settings(check,settings):
                add_tr(Name, Desc, Tracker_type,settings)
                return redirect("/tracker_index")
            else:
                flash(f"Incorrect settings",category="danger")
                return render_template("add_tracker.html")
        else:
            if settings != "":
                flash(f"Incorrect settings",category="danger")
                return render_template("add_tracker.html")
            else:
                add_tr(Name, Desc, Tracker_type,settings)
                return redirect("/tracker_index")
    return render_template("add_tracker.html")

@app.route("/Update_tracker/<int:tracker_id>",methods=['GET','POST'])
def Update_t(tracker_id):
    trc = Tracker.query.filter_by(tracker_id = tracker_id).first()
    if request.method=='POST':
        U_Name=request.form.get("Name")
        U_Desc=request.form.get("Desc")
        U_Tracker_type=request.form.get("Tracker_type")
        Name=trc.Name
        l=Logs.query.filter_by(Tracker_name=Name).delete()
        trc.Name=U_Name
        trc.Description=U_Desc
        trc.Tracker_type=U_Tracker_type
        db.session.commit()
        return redirect("/tracker_index")
    return render_template("update_tracker.html",tracker=trc)   

@app.route("/Delete_tracker/<int:tracker_id>",methods=['GET','POST'])
def Delete_t(tracker_id):
    t=Tracker.query.filter_by(tracker_id=tracker_id).first()
    Name=t.Name
    l=Logs.query.filter_by(Tracker_name=Name).delete()
    db.session.delete(t)
    db.session.commit()
    return redirect("/tracker_index")

# --------------------------------> Logs CRUD <----------------------------------------------------------------------------------------

@app.route("/Add_logs/<int:tracker_id>/<string:Name>",methods=['GET','POST'])
def Add_log(tracker_id,Name):
    tr=Tracker.query.filter_by(tracker_id=tracker_id).all()
    ty=tr[0].Tracker_type
    s=tr[0].settings
    l=s.split(",")
    ct = datetime.datetime.now()
    d= ct.strftime("%d-%m-%Y" )
    t= ct.strftime("%H:%M:%S")
    if request.method=='POST':
        Tracker_name=Name
        Date=d
        Time=request.form.get("Time")
        Value=request.form.get("Value")
        Notes=request.form.get("Notes")
        if validate_value(ty, Value):
            add_logs(Tracker_name,Time, Value, Notes,Date)
            return redirect("/tracker_index")
        else:
            flash(f"Incorrect Value",category="danger")
            return render_template("add logs.html",t_name=Name,Date=d,Time=t,t_id=tracker_id,Tracker_type=ty,list=l)
    return render_template("add logs.html",t_name=Name,Date=d,Time=t,t_id=tracker_id,Tracker_type=ty,list=l)

@app.route("/Update_logs/<int:logs_id>",methods=['GET','POST'])
def Update_logs(logs_id):
    log_u=Logs.query.filter_by(logs_id=logs_id).first()
    Name=log_u.Tracker_name
    tr=Tracker.query.filter_by(Name=Name).first()
    ty=tr.Tracker_type
    s=tr.settings
    l=s.split(",")
    ct = datetime.datetime.now()
    d= ct.strftime("%d-%m-%Y" )
    t= ct.strftime("%H:%M:%S")
    if request.method=='POST':
        Date=request.form.get("Date")
        Time=request.form.get("Time")
        Value=request.form.get("Value")
        Notes=request.form.get("Notes")
        print(Date)
        log_u.date=Date
        log_u.Time=Time
        log_u.Value=Value
        log_u.Notes=Notes
        db.session.commit()
        return redirect("/tracker_index")
    return render_template("update_logs.html",logs_id=logs_id,Date=d,Time=t,Tracker_type=ty,t_name=Name,list=l)
@app.route("/delete_logs/<int:logs_id>")
def delete(logs_id):
    Logs.query.filter_by(logs_id=logs_id).delete()
    db.session.commit()
    return redirect("/tracker_index")
