import aircanvas_app as aircanvas
from flask import Flask, render_template, Response
import cv2 as cv

app = Flask(__name__)
# app.config['']
cap = cv.VideoCapture(0)

def gen():
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        else:
            # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            newFrame = aircanvas.canvas(frame)
            ret, buf = cv.imencode('.jpg', newFrame)
            b = buf.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + b + b'\r\n') 

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/socket_video_feed')
# def socket_video_feed():

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)