from flask import Flask
from flask import abort
from flask import url_for
from flask import render_template
from flask_restful import Api
from flask_restful import Resource
from flask import request
from flask.json import jsonify
import threading
import logging
import time
import shutil

app = Flask(__name__)
api = Api(app)

###################################################
ATTITUDE_LEVELS = ["Concentrating", "Participating", "Less Focusing", "In Class", "Unknown"]
ATTITUDE_SET ={
    "CS": 2,      # Currnt Status
    "SWS": 5,     # Short term window size
    "LWS": 30,    # Long term window size
    "SS": 0,      # Short term Score
    "LS": 0,      # Long term Score
    "SC": 5 * 2,    # Short term Criteria
    "LC": 30 + 1,    # Long term Criteria
}
# BAD_CRITERIA = 20
# MAX_PERIOD = 30

# MIN_RECENT_SCORE = 5
MINIMUM_FACEWIDTH = 11.5

BF_POSTURERANGE = [-59, 30]
LR_POSTURERANGE = [-30, 30]
###################################################

DEFAULTSCOREARR = [1] * 30

DEFAULTVALUE = {"name":"Nobody",
                    "width":0,
                    "height":0,
                    "x":0,
                    "y":0,
                    "w":0,
                    "h":0,
                    "bf":0, # back and forth angle degree
                    "lr":0, # left and right angle degree
                    #"posz":0,
                    "score": 30 + 1,    # 5 seconds to "bad" status
                    "attitude": 2,
                    "scoreArr":DEFAULTSCOREARR,
                    "temporal":0,
                    "record": False,
                    "timebase": 0
                }

_attLog = open("attlog.csv", "w")
_studentData = DEFAULTVALUE.copy()
# _recordFlag = False
# _attiTemporal = 0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record/<string:command>", methods=["GET", "POST"])
def record(command):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        if command == "start":
            _studentData["record"] = True
            _studentData["timebase"] = time.perf_counter()

            header = "--------------------------------------------------------\r\ntime,face,posture,score,attitude\r\n"
            _attLog.write(header)
            _attLog.flush()
            #_attLog.open("attlog.csv", "w")
        else:
            _studentData["record"] = False
            #_studentData["timebase"] = time.perf_counter()
    return "OK"

@app.route("/getstatus", methods=['GET'])
def getstatus():
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        data = _studentData
        status = {  "name":data["name"],
                    "width":data["width"],
                    "height":data["height"],
                    "x":data["x"],
                    "y":data["y"],
                    "w":data["w"],
                    "h":data["h"],
                    "bf":data["bf"],             # back and forth angle degree
                    "lr":data["lr"],             # left and right angle degree
                    "score":data["score"],       # 5 seconds to "bad" status
                    "attitude": data["attitude"]
                }
        return jsonify(status)


# <string:name>/<string:width>/<string:height>/<string:x>/<string:y>/<string:w>/<string:h>/<string:posx>/<string:posy>/<string:posz>")
# @app.route("/setstatus/<string:name>/<int:width>/<int:height>/<int:x>/<int:y>/<int:w>/<int:h>/<int:posx>/<int:posy>/<int:posz>", methods=["POST"])
@app.route("/setstatus/<string:name>/<string:width>/<string:height>/<string:x>/<string:y>/<string:w>/<string:h>/<string:posx>/<string:posy>/<string:posz>", methods=["POST"])
def setstatus(name, width,height,x,y,w,h,posx,posy,posz):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        # updateStatus(name, width, height, x, y, w, h, posx, posy)
        print("setstatus ", width,height,x,y,w,h,posx,posy,posz)
        # logging.info("#setstatus ", int(width),int(height),int(x),int(y),int(w),int(h),float(posx),float(posy),float(posz))
        updateData(name, int(width),int(height),int(x),int(y),int(w),int(h),float(posx),float(posy),float(posz))
        return "OK"


def judgeAttitudeWithTime(scoreArr):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():

        CS = ATTITUDE_SET["CS"]     #: Current Score
        SWS = ATTITUDE_SET["SWS"]   #: 5,  # Short term window size
        LWS = ATTITUDE_SET["LWS"]   #: 30,  # Long term window size
        SS = ATTITUDE_SET["SS"]     #: 0,  # Short term Score
        LS = ATTITUDE_SET["LS"]     #: 0,  # Long term Score
        SC = ATTITUDE_SET["SC"]     #: 5 * 2,  # Short term Criteria
        LC = ATTITUDE_SET["LC"]     #: 30 + 1,  # Long term Criteria

        try:
            # 1. total score
            LS = 0

            for s in scoreArr:
                LS = LS + s

            # 2. recent score
            SS = 0
            for s in scoreArr[-1:(-1 - SWS):-1]:
                SS = SS + s

            if SS == SC:  # perfect during recent 5 seconds
                CS = 3
                if LS < LS:
                    scoreArr = _studentData["scoreArr"]
                    for s in range(len(scoreArr) - SWS):
                        scoreArr[s] = 1
            elif LS > LC:
                if SS > SWS:
                    CS = 3
                else:
                    CS = 2
            elif LS <= LC:
                if LS < 5:
                    CS = 0
                else:
                    CS = 1

            return CS
        except Exception as e:
            print("Exception ", e)
            return 0


'''
 make judgement of current attitude without any concerning about 
 earlier score, the result is 1 or -1
'''
faceArray = [1] * 5
def judgeAttitudeTemporal(width, height, x, y, w, h, posx, posy, posz):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        hPercent = 0
        vPercent = 0
        if width == 0 or height == 0 or x == 0 or y == 0:
            pass
        else:
            hPercent = w / width * 100
            vPercent = h / height * 100

        pose = 1 if (posx > LR_POSTURERANGE[0]
                        and posx < LR_POSTURERANGE[1]
                        and posy > BF_POSTURERANGE[0]
                        and posy < BF_POSTURERANGE[1]) else 0
        faceNow = 1 if hPercent > MINIMUM_FACEWIDTH else 0

        ############################################
        # push to face circular queue
        # if face is appeared one or more time
        face = 0
        faceArray.insert(len(faceArray), faceNow)
        faceArray.pop(0)
        for f in faceArray:
            face = face | f == 1
        ###########################################
        return pose + face

# update judgement every 1 second
def periodicUpdatData(*arg, **keyargs):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        ################################################################
        # push current value to the array
        value = _studentData
        scoreArr = value["scoreArr"]
        scoreArr.insert(len(scoreArr), value["temporal"]) #_attiTemporal)
        scoreArr.pop(0)     # remove from index 0
        ################################################################
        ############################################################
        # recent 30 second sumation
        accu = 0
        for s in scoreArr:
            accu = accu + s
        ############################################################
        ############################################################
        # attitude scoring algorithm
        value["temporal"] = 0 # temporal data clear
        attiFinal = judgeAttitudeWithTime(scoreArr)
        ############################################################

        value["score"] = accu            # accumulated score
        value["attitude"] = attiFinal    # pass or fail
        print("Periodic update:", _studentData["scoreArr"], _studentData["attitude"], _studentData["score"])
        #####################################################################################################
        # make data for logging
        pose = True if (LR_POSTURERANGE[0] < value["lr"] < LR_POSTURERANGE[1]
                        and BF_POSTURERANGE[0] < value["bf"] < BF_POSTURERANGE[1]) else False
        if _studentData["record"] :
            if _attLog is not None:
                tt = time.localtime(time.time())
                timestamp = "{}/{}/{} {}:{}:{}".format(tt.tm_mon, tt.tm_mday, tt.tm_year, tt.tm_hour, tt.tm_min, tt.tm_sec)
                logline = "{timestamp},{face},{posture},{score},{attitude}\n".format(timestamp=timestamp, face=(value["w"]/value["width"]*30),
                    posture=(5 if pose is True else 0), score=value["score"]/60 * 30, attitude=(value["attitude"]/3*30))
                _attLog.write(logline)
                _attLog.flush()
        ####################################################################################################
        #logging.info("Sample periodic~~~~", value)
        timer = threading.Timer(1, periodicUpdatData, None, value)
        timer.start()


def updateData(name, width, height, x, y, w, h, posx, posy, posz):
    global ATTITUDE_LEVELS
    global ATTITUDE_SET
    global MINIMUM_FACEWIDTH
    global BF_POSTURERANGE
    global LR_POSTURERANGE
    global DEFAULTSCOREARR
    global DEFAULTVALUE
    global _attLog
    global _studentData

    with app.app_context():
        attiTemporal = judgeAttitudeTemporal(width, height, x, y, w, h, posx, posy, posz)
        # _attiTemporal = attiTemporal
        _studentData["name"] = name
        _studentData["width"] = width
        _studentData["height"] = height
        _studentData["x"] = x
        _studentData["y"] = y
        _studentData["w"] = w
        _studentData["h"] = h
        _studentData["bf"] = posy
        _studentData["lr"] = posx
        _studentData["temporal"] = attiTemporal
        # print("updateData", _studentData)

        
if __name__ == "__main__":
    with app.app_context():
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')
        timer = threading.Timer(2, periodicUpdatData, None, _studentData)
        timer.start()

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)



def face_detect():
    pass
def posture_detect():
    pass
def update_ui():
    pass

def judgeAttitudeWithTime(scoreArr):
        
        
    MINIMUM_FACEWIDTH = 11.5        # minimum face width percent 
    BF_POSTURERANGE = [-55, 30]     # posture range bf-angle
    LR_POSTURERANGE = [-30, 30]     # posture range lr-angle    
    scoreArr =[1]*30 #: Recent 30 seconds score array
    CS = 0           #: Current Score
    SWS = 5          #: 5 seconds, Short term window size
    LWS = 30         #: 30 seconds, Long term window size
    SS = 0           #: 0, Short term Score
    LS = 0           #: 0, Long term Score
    SC = SWS * 2     #: 5 * 2, Short term Criteria
    LC = LWS + 1     #: 30 + 1, Long term Criteria
    ATTI = ["Out of Class","Present","Concentrating","Participating"]
    
    while True:
        current = face_detect() + posture_detect()  # 0 or 1 or 2
        scoreArr.push_tail(current)
        scoreArr.pop_front()

        for s in scoreArr:  # long term score accumulation
            LS = LS + s        
        for s in scoreArr[-1:(-1 - SWS):-1]:    # short term score acumulation
            SS = SS + s

        if SS == SC:    # perfect during recent 5 seconds
            CS = 3
            # if recent SWS score(SS) is perfect but past 30 seconds record is not good,
            # recover past LWS ~ SWS second data as 1   
            if LS < LS:
                for s in range(len(scoreArr) - SWS):
                    scoreArr[s] = 1
        elif LS > LC:   # long term score is high
            if SS > SWS:
                CS = 3
            else:
                CS = 2
        elif LS <= LC:  # long term score is low
            if LS >= 5:
                CS = 1
            else:
                CS = 0
        update_ui(ATTI[CS])
