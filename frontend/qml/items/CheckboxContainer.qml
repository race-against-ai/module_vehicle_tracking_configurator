import QtQuick 2.15
import QtQuick.Controls 2.15

Item {

    Rectangle {
        anchors.fill: parent
        color: window.accentColor
    }

    Row {
        Item {
            id: regionOfInterestCheckbox
            property bool checked: false

            width: parent.parent.width / 3
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? "#8f4d0b" : window.buttonColor

                Text {
                    text: "ROI"
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        parent.parent.checked = !parent.parent.checked
                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, worldCordCheckbox.checked)
                    }
                }
            }

            onCheckedChanged: {
                console.log("Real Word Cord checkbox triggered")
                regionOfInterestPointsCover.visible = !checked
                worldCordCover.visible = !worldCordCheckbox.checked
                transformationPointsCover.visible = !transformationPointsCheckbox.checked
                worldCordCheckbox.checked = false
                transformationPointsCheckbox.checked = false
            }
        }

        Item {
            id: transformationPointsCheckbox
            property bool checked: false

            width: parent.parent.width / 3
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? "#8f4d0b" : window.buttonColor

                Text {
                    text: "T-Points"
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        parent.parent.checked = !parent.parent.checked
                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, worldCordCheckbox.checked)
                    }
                }
            }

            onCheckedChanged: {
                console.log("Transformation Point checkbox triggered")
                worldCordCover.visible = !worldCordCheckbox.checked
                regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                transformationPointsCover.visible = !transformationPointsCheckbox.checked
                regionOfInterestCheckbox.checked = false
                worldCordCheckbox.checked = false
            }
        }

        Item {
            id: worldCordCheckbox
            property bool checked: false

            width: parent.parent.width / 3
            height: parent.parent.height

            Rectangle {
                anchors.centerIn: parent
                height: parent.height * 0.8
                width: parent.width / 2
                border.color: "black"
                radius: 5
                color: parent.checked ? "#8f4d0b" : window.buttonColor

                Text {
                    text: "World Cords."
                    font.pixelSize: parent.height / 4
                    anchors.centerIn: parent
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        parent.parent.checked = !parent.parent.checked
                        window.onStatesUpdated(regionOfInterestCheckbox.checked, transformationPointsCheckbox.checked, worldCordCheckbox.checked)
                    }
                }
            }

            onCheckedChanged: {
                console.log("Real Word Cord checkbox triggered")
                worldCordCover.visible = !checked
                regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                transformationPointsCover.visible = !transformationPointsCheckbox.checked
                regionOfInterestCheckbox.checked = false
                transformationPointsCheckbox.checked = false
            }
        }
    }
}
