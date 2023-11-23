import QtQuick 2.15
import QtQuick.Controls 2.15

Item {

    Row {

        Rectangle {
            height: parent.parent.height
            width: parent.parent.width / 3
            color: "white"
            radius: 10

            CheckBox {
                id: regionOfInterestCheckbox
                text: "ROI"
                checked: false
                anchors.centerIn: parent

                onCheckedChanged: {
                    console.log("ROI checkbox triggered")
                    worldCordCover.visible = !worldCordCheckbox.checked
                    regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                    transformationPointsCover.visible = !transformationPointsCheckbox.checked
                    transformationPointsCheckbox.checked = false
                    worldCordCheckbox.checked = false
                }
            }
        }

        Rectangle {
            height: parent.parent.height
            width: parent.parent.width / 3
            color: "white"
            radius: 10

            CheckBox {
                id: transformationPointsCheckbox
                text: "T-Points"
                checked: false
                anchors.centerIn: parent

                onCheckedChanged: {
                    console.log("Transformation Point checkbox triggered")
                    worldCordCover.visible = !worldCordCheckbox.checked
                    regionOfInterestPointsCover.visible = !regionOfInterestCheckbox.checked
                    transformationPointsCover.visible = !transformationPointsCheckbox.checked
                    regionOfInterestCheckbox.checked = false
                    worldCordCheckbox.checked = false
                }
            }
        }

        Rectangle {
            height: parent.parent.height
            width: parent.parent.width / 3
            color: "white"
            radius: 10

            CheckBox {
                id: worldCordCheckbox
                text: "World Cords"
                checked: false
                anchors.centerIn: parent

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
}
