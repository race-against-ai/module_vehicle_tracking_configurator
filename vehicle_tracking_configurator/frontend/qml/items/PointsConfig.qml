// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: pointsConfig

    property alias configName: configNameText.text
    property alias chosenPointDefaultText: chosenConfigText.text
    property int textBoxWidth: width * 0.1
    property int textBoxHeight: height * 0.1594

    color: window.accentColor

    function setPoints(coords) {
        imagePointXInput.text = coords[0];
        imagePointYInput.text = coords[1];
        realPointXInput.text = coords[2];
        realPointYInput.text = coords[3];
    }

    function setChosenPoint(chosenPoint) {
        chosenConfigText.text = chosenPoint;
    }

    Text {
        id: configNameText

        text: configName

        anchors.top: pointsConfig.top
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        width: parent.width * 0.5
        height: parent.height * 0.2151

        color: window.headlineColor
        fontSizeMode: Text.Fit
        font.pixelSize: 5000
        minimumPixelSize: 10
    }

    Text {
        id: imageCoordsText

        text: "Image Coordinates"

        anchors.top: configNameText.bottom
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        width: parent.width * 0.5
        height: parent.height * 0.1594

        color: window.headlineColor
        minimumPixelSize: 10
        font.pixelSize: 5000
        fontSizeMode: Text.Fit
    }

    CoordinateTextField {
        id: imagePointXInput

        assingedId: "imagePointXInput"
        placeholderText: "X"

        height: textBoxHeight
        width: textBoxWidth

        anchors.top: imageCoordsText.bottom
        anchors.left: parent.left
    }

    CoordinateTextField {
        id: imagePointYInput

        assingedId: "imagePointYInput"
        placeholderText: "Y"

        height: textBoxHeight
        width: textBoxWidth

        anchors.top: imageCoordsText.bottom
        anchors.left: imagePointXInput.right
    }

    Text {
        id: realCoordsText

        text: "Real World Coordinates"

        anchors.top: imagePointYInput.bottom
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        width: parent.width * 0.5
        height: parent.height * 0.1594

        color: window.headlineColor
        minimumPixelSize: 10
        font.pixelSize: 5000
        fontSizeMode: Text.Fit
    }

    CoordinateTextField {
        id: realPointXInput

        assingedId: "realPointXInput"
        placeholderText: "X"

        height: textBoxHeight
        width: textBoxWidth

        anchors.top: realCoordsText.bottom
        anchors.left: pointsConfig.left
    }

    CoordinateTextField {
        id: realPointYInput

        assingedId: "realPointYInput"
        placeholderText: "Y"

        height: textBoxHeight
        width: textBoxWidth

        anchors.top: realCoordsText.bottom
        anchors.left: realPointXInput.right
    }

    Rectangle {
        id: binBackground

        width: parent.width * 0.0535
        height: parent.height * 0.1992

        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.top: parent.top
        anchors.topMargin: 5

        color: mouseHandler.containsMouse ? "#30ffffff" : "transparent"

        Image {
            id: binImage

            source: "../../assets/svg/bin.svg"

            anchors.fill: parent
        }

        MouseArea {
            id: mouseHandler

            anchors.fill: parent

            hoverEnabled: true

            onClicked: {
                vehicle_tracking_configurator_model.delete_button_clicked(configName);
            }
        }
    }

    Rectangle {
        id: chooserContainer
        width: parent.width * 0.3215
        height: parent.height * 0.1992

        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5

        color: window.buttonColor

        Rectangle {
            id: leftArrow

            anchors.left: parent.left
            anchors.top: parent.top
            height: parent.height
            width: parent.width * 0.1

            color: leftArrowMouseHandler.containsMouse ? window.hoverButtonColor : "transparent"

            Text {
                id: leftArrowText

                width: parent.width
                height: parent.height

                text: "←"
                minimumPointSize: 10
                font.pointSize: 60
                fontSizeMode: Text.Fit

                anchors.centerIn: parent
            }

            MouseArea {
                id: leftArrowMouseHandler

                hoverEnabled: true

                anchors.fill: parent

                onClicked: {
                    vehicle_tracking_configurator_model.arrow_button_clicked(configNameText.text, "left");
                }
            }
        }

        Rectangle {
            id: rightArrow

            anchors.right: parent.right
            anchors.top: parent.top

            height: parent.height
            width: parent.width * 0.1

            color: rightArrowMouseHandler.containsMouse ? window.hoverButtonColor : "transparent"

            Text {
                id: rightArrowText

                anchors.fill: parent
                anchors.centerIn: parent

                text: "→"
                minimumPointSize: 10
                font.pointSize: 60
                fontSizeMode: Text.Fit
            }

            MouseArea {
                id: rightArrowMouseHandler

                hoverEnabled: true

                anchors.fill: parent

                onClicked: {
                    vehicle_tracking_configurator_model.arrow_button_clicked(configNameText.text, "right");
                }
            }
        }

        Rectangle {
            id: pointText

            height: parent.height
            width: parent.width - (leftArrowText.width + rightArrowText.width)

            anchors.top: parent.top
            anchors.left: leftArrow.right

            color: "transparent"

            Text {
                id: chosenConfigText

                anchors.fill: parent
                anchors.centerIn: parent
                horizontalAlignment: Text.AlignHCenter

                minimumPointSize: 10
                font.pointSize: 60
                fontSizeMode: Text.Fit
            }
        }
    }
}
