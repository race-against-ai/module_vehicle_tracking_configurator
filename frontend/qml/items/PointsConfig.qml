// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Controls 2.15

import "../items"

Rectangle {
    id: pointsConfig

    property string configName

    color: window.accentColor

    Text {
        id: configNameText

        text: configName

        anchors.top: pointsConfig.top
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 40
    }

    Text {
        id: imageCoordsText

        text: "Image Coordinates"

        anchors.top: configNameText.bottom
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 30
    }

    CoordinateTextField {
        id: imagePointXInput

        assingedId: "imagePointXInput"
        placeholderTextText: "X"

        anchors.top: imageCoordsText.bottom
        anchors.left: parent.left
    }

    CoordinateTextField {
        id: imagePointYInput

        assingedId: "imagePointYInput"
        placeholderTextText: "Y"

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

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 30
    }

    CoordinateTextField {
        id: realPointXInput

        assingedId: "realPointXInput"
        placeholderTextText: "X"

        anchors.top: realCoordsText.bottom
        anchors.left: pointsConfig.left
    }

    CoordinateTextField {
        id: realPointYInput

        assingedId: "realPointYInput"
        placeholderTextText: "Y"

        anchors.top: realCoordsText.bottom
        anchors.left: realPointXInput.right
    }

    Rectangle {
        id: binBackground

        width: 50
        height: 50
        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.top: parent.top
        anchors.topMargin: 5

        color: mouseHandler.containsMouse ? "#30ffffff" : "transparent"

        Image {
            // trash can image
            source: "../../svg/bin.svg"

            anchors.fill: parent
        }

        MouseArea {
            id: mouseHandler

            anchors.fill: parent

            hoverEnabled: true

            onClicked: {
                window.onDeleteButtonClicked(configName);
            }
        }
    }

    Rectangle {
        // Point Chooser
        width: 300
        height: 50
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
            width: 30

            color: leftArrowMouseHandler.containsMouse ? window.hoverButtonColor : "transparent"

            Text {
                // Left arrow text
                anchors.fill: parent
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
                    window.onArrowButtonClicked(pointsConfig.configName, "left");
                }
            }
        }

        Rectangle {
            // Right arrow
            anchors.right: parent.right
            anchors.top: parent.top
            height: parent.height
            width: 30

            color: rightArrowMouseHandler.containsMouse ? window.hoverButtonColor : "transparent"

            Text {
                // right arrow
                anchors.fill: parent
                text: "→"
                minimumPointSize: 10
                font.pointSize: 60
                fontSizeMode: Text.Fit
                anchors.centerIn: parent
            }

            MouseArea {
                id: rightArrowMouseHandler

                hoverEnabled: true

                anchors.fill: parent

                onClicked: {
                    window.onArrowButtonClicked(pointsConfig.configName, "right");
                }
            }
        }

        Rectangle {
            // Point Text
            height: parent.height
            width: parent.width - (30 * 2)

            anchors.top: parent.top
            anchors.left: leftArrow.right

            color: "transparent"

            Text {
                id: chosenConfigText

                anchors.fill: parent
                anchors.centerIn: parent
                horizontalAlignment: Text.AlignHCenter

                text: "Placeholder"
                minimumPointSize: 10
                font.pointSize: 60
                fontSizeMode: Text.Fit
            }
        }
    }
}
