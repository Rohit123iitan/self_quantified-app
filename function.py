from app import *
from model import *
def add_reg(user_name,password):
    reg=User(
        user_name=user_name,
        password=password
    )
    db.session.add(reg)
    db.session.commit()

def add_tr(Name,Desc,Tracker_type,settings):
    if Tracker_type=="Multiple Choice":
        tr=Tracker(
            Name=Name,
            Description=Desc,
            Tracker_type=Tracker_type,
            settings=settings
        )
    else:
        tr=Tracker(
        Name=Name,
        Description=Desc,
        Tracker_type=Tracker_type,
        settings=False
        )
    db.session.add(tr)
    db.session.commit()

def add_logs(Tracker_name,Time,Value,Notes,Date):
    log=Logs(
        Tracker_name=Tracker_name,
        Time=Time,
        Value=Value,
        Notes=Notes,
        date=Date
    )
    db.session.add(log)
    db.session.commit()

def validate_value(Tracker_type,Value):
    if Tracker_type=="Numerical":
        try:
            c=int(Value)
            return True
        except:
            return False
    elif Tracker_type=="Boolean":
        if Value=="True" or "False":
            return True
        else:
            return False
    else:
        return True
        
def graph(xd,xt,y,Tracker_type,Time_stamp):
    if Tracker_type=="Numerical":
        if Time_stamp=="Today":
            plt.cla()
            plt.plot(xt,y)
            plt.xlabel('Time')
        else:
            plt.cla()
            plt.plot(xd,y)
            plt.xlabel('Date')
    elif Tracker_type=="Boolean":
        if Time_stamp=="Today":
            plt.cla()
            plt.plot(xt,y)
            plt.xlabel('Time')
        else:
            plt.cla()
            plt.plot(xd,y)
            plt.xlabel('Date')
    else:
        if Time_stamp=="Today":
            plt.cla()
            plt.plot(xt,y)
            plt.xlabel('Time')
        else:
            plt.cla()
            plt.plot(xd,y)
            plt.xlabel('Date')
    plt.ylabel('Value')
    plt.savefig("static/image1.png")
def validate_settings(check,settings):
    for j in settings:
        if check[0]==j:
            return True
    return False