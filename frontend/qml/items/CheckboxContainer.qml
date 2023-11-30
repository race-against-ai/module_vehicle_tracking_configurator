import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: modeContainer
    property int items: 3

    Rectangle {
        anchors.fill: parent
        color: window.accentColor
    }

    Row {

        Item {
            id: regionOfInterestCheckbox
            property bool checked: true

            width: parent.parent.width / modeContainer.items
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? window.buttonSelectColor : window.buttonColor

                Text {
                    text: "ROI"
                    color: window.buttonTextColor
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        regionOfInterestCheckbox.checked = true
                        timeTrackingCheckbox.checked = false
                        transformationPointsCheckbox.checked = false

                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, timeTrackingCheckbox.checked)

                        regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                        transformationPointsCover.visible = !transformationPointsCheckbox.checked
                    }
                }
            }
        }

        Item {
            id: transformationPointsCheckbox
            property bool checked: false

            width: parent.parent.width / modeContainer.items
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? window.buttonSelectColor : window.buttonColor

                Text {
                    text: "T-Points"
                    color: window.buttonTextColor
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        transformationPointsCheckbox.checked = true
                        regionOfInterestCheckbox.checked = false
                        timeTrackingCheckbox.checked = false

                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, timeTrackingCheckbox.checked)

                        regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                        transformationPointsCover.visible = !transformationPointsCheckbox.checked
                    }
                }
            }
        }

        Item {
            id: timeTrackingCheckbox
            property bool checked: false

            width: parent.parent.width / modeContainer.items
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? window.buttonSelectColor : window.buttonColor

                Text {
                    text: "Time Tracking"
                    color: window.buttonTextColor
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        timeTrackingCheckbox.checked = true
                        regionOfInterestCheckbox.checked = false
                        transformationPointsCheckbox.checked = false

                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, timeTrackingCheckbox.checked)

                        regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                        transformationPointsCover.visible = !transformationPointsCheckbox.checked
                    }
                }
            }
        }
    }
}
