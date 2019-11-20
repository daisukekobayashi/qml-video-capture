import QtQuick 2.13
import QtQuick.Controls 2.13
import OpenCV 1.0

ApplicationWindow {
    visible: true
    width: 960
    height: 400

    Rectangle {
        anchors.fill: parent
        color: "black"
        VideoCapture {
            id: videoCapture
            source: "0"
            anchors.fill: parent
            anchors.centerIn: parent
        }
    }
}
