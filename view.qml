import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.11
import OpenCV 1.0

ApplicationWindow {
    visible: true
    width: 960
    height: 480

    ColumnLayout {
        anchors.fill: parent
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "black"
            VideoCapture {
                id: videoCapture
                source: "0"
                anchors.fill: parent
            }
        }
        Button {
            text: "Start"
            Layout.fillWidth: true
            onClicked: {
                videoCapture.start()
            }
        }
        Button {
            text: "Stop"
            Layout.fillWidth: true
            onClicked: {
                videoCapture.stop()
            }
        }
    }
}
