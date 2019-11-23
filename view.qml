import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.11
import OpenCV 1.0

ApplicationWindow {
    visible: true
    width: 960
    height: 480

    Column {
        anchors.fill: parent
        Rectangle {
            width: parent.width
            height: parent.height - startButton.height - stopButton.height
            color: "black"
            VideoCapture {
                id: videoCapture
                anchors.fill: parent
                source: "0"
            }
        }
        Button {
            id: startButton
            width: parent.width
            height: 50
            text: "Start"
            onClicked: {
                videoCapture.start()
            }
        }
        Button {
            id: stopButton
            width: parent.width
            height: 50
            text: "Stop"
            onClicked: {
                videoCapture.stop()
            }
        }
    }
}
