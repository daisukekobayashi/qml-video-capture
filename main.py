import sys
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import qmlRegisterType, QQmlApplicationEngine

from video_capture import VideoCapture

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qmlRegisterType(VideoCapture, "OpenCV", 1, 0, "VideoCapture")

    engine.load('view.qml')

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
