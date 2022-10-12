from distutils.log import debug
import mimetypes
from unittest import result
from flask      import Flask, request, jsonify, current_app, redirect, url_for, render_template, Response
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from flask_cors import CORS
import json
from camera import Camera
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def update_switch(value):
    return current_app.database.execute(text("""
        UPDATE switch 
            SET switch = :switch
        WHERE id = 1
    """), value).lastrowid

def selectSwitch():
    return current_app.database.execute(text("""
        SELECT switch FROM switch
    """)).fetchall()

def insertVideoName(name):
    return current_app.database.execute(text("""
        INSERT INTO doorlock_video (
            name
        ) VALUES (
            :name
        )
    """), name).lastrowid

def selectAllVideo():
    return current_app.database.execute(text("""
        SELECT * FROM doorlock_video
    """)).fetchall()

def create_app(test_config = None):
    app = Flask(__name__)

    @app. route('/')
    @app. route('/mainpage')
    def dataHtml():
        return render_template('mainpage.html')

    if __name__ == '__main__':
        app.run(host="192.168.0.24",port=5000, debug=True, threaded=True)
    CORS(app, resources={r'*': {'origins': '*'}})
	
    # unit-test를 실행할 때 테스트 데이터 베이스에 대한 정보를 넣어준다.
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
	
    # 데이터 베이스와 연동해준다.
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database

    @app.route("/video", methods=['POST'])
    def saveVideoName():
        newValue = request.json
        newValueId = insertVideoName(newValue)

        return jsonify(newValueId)

    @app.route("/video", methods=['GET'])
    def getVideos():
        doorlockList = selectAllVideo()

        ret = []
        for e in doorlockList:
            temp = {'id':e[0], 'name':e[1], 'date_created':e[2]}
            ret.append(temp)

        return jsonify(ret)

    @app.route('/display/<filename>')
    def displayVideo(filename):
        return redirect(url_for('static', filename='uploads/' + filename), code=301)

    @app.route("/switch", methods=['PUT'])
    def updateSwitch():
        newSwitch = request.json
        curSwitchVal = newSwitch['switch']
        if curSwitchVal != 0 and curSwitchVal != 1:
            return jsonify("Please insert 0 or 1"), 500
        newSwitch_id = update_switch(newSwitch)
        return "ok", 200

    @app.route("/switch", methods=['GET'])
    def getSwitch():
        switch = selectSwitch()
        switchJson = {'switch': switch[0][0]}
        return jsonify(switchJson)
 
    @app.route('/cam')
    def index():
        return render_template('cam.html')

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        cctv = Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        return cctv

    return app


