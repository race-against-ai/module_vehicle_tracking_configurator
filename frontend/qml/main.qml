// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

import "./items"

//TODO: Link up the functions from the window to the backend

Window {
    id: window

    property color backgroundColor: "#0f0e17"
    property color headlineColor: "#fffffe"
    property color paragraphColor: "#a7a9be"
    property color buttonColor: "#ff8906"
    property color hoverButtonColor: "#ffad52"
    property color buttonTextColor: "#fffffe"
    property color placeholderColor: "#505050"
    property color accentColor: "#f25f4c"
    property color accentColor2: "#e53170"
    property int videosX: window.width * 0.37109375
    property int videosY: window.height * 0.490740
    property real targetAspectRatio: 16 / 9

    width: 1920
    height: 1080
    minimumWidth: 1536
    minimumHeight: 864
    maximumWidth: 1536
    maximumHeight: 864


    color: backgroundColor
    visibility: Window.FullScreen
    visible: true

    title: "Configurator Interface"

    function onConfigButtonPressed(button_text) {
        console.log(button_text, "has been pressed");
    }
    function onCoordinateTextChanged(input_id, config_name, text) {
        console.log(input_id, config_name, text);
    }
    function onDeleteButtonClicked(config_name) {
        console.log(config_name, "delete button has been pressed");
    }
    function onArrowButtonClicked(config_name, direction) {
        console.log(config_name, direction);
    }

    Item {
        // Container for keys.onPressed
        anchors.fill: parent
        focus: true

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_F11) {
                if (window.visibility === Window.FullScreen) {
                    window.visibility = Window.Windowed
                } else {
                    window.visibility = Window.FullScreen
                }
            } else if (event.key === Qt.Key_Space) {
                console.log(window.width, window.height)
            }
        }

        Rectangle {
            // The top video
            id: pointsDrawer

            anchors.top: parent.top
            anchors.topMargin: 5
            anchors.left: parent.left
            anchors.leftMargin: 5

            height: window.videosY
            width: window.videosX

            color: window.placeholderColor

            Image {
                id: pointsDrawerStream

                property int id: 0

                anchors.fill: parent
                fillMode: Image.PreserveAspectFit

                visible: true
                cache: false
                source: "image://point_drawer/" + id

                function reload() {
                    id++;
                }

            }

            MouseArea {
                id: pointsDrawerMouseArea

                anchors.fill: parent

                onClicked: {
                    console.log(pointsDrawerMouseArea.mouseX, pointsDrawerMouseArea.mouseY)
                }
            }

            Image {
                id: fullscreenButton
                source: "../svg/maximize.svg"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                height: parent.height * 0.05
                fillMode: Image.PreserveAspectFit

                onClicked: {
                    if(pointsDrawer.height == window.videosY) {
                        pointsDrawer.height = window.height
                        pointsDrawer.width = window.width
                    }
                    else {
                        pointsDrawer.height = window.videosY
                        pointsDrawer.width = window.videosX
                    }
                }
            }
        }

        Rectangle {
            // The bottom video
            anchors.top: pointsDrawer.bottom
            anchors.topMargin: 5
            anchors.left: parent.left
            anchors.leftMargin: 5

            height: window.videosY
            width: window.videosX


            color: window.placeholderColor
        }

        Rectangle {
            id: optionsRectangle

            anchors.top: parent.top
            anchors.topMargin: 5
            anchors.left: pointsDrawer.right
            anchors.leftMargin: 5

            height: window.height - 10
            width: window.width - window.videosX - 10

            color: "transparent"

            property int confBoxSizeY: (parent.height / 10 - 2.5) * 3

            PointsConfig {
                id: regionOfInterestPoints

                anchors.top: parent.top
                anchors.left: parent.left

                width: parent.width
                height: optionsRectangle.confBoxSizeY

                configName: "Region of Interest"
            }

            PointsConfig {
                id: transformationPoints

                anchors.top: regionOfInterestPoints.bottom
                anchors.topMargin: 5
                anchors.left: parent.left

                height: parent.confBoxSizeY
                width: parent.width

                configName: "Transformation Points"
            }

            CoordinateDisplay {
                id: realWorldCoordinatePoints

                anchors.top: transformationPoints.bottom
                anchors.topMargin: 5

                height: parent.confBoxSizeY
                width: parent.width

                configName: "Real World Coordinate Points"
            }

            Rectangle {
                id: configButtonContainer

                anchors.left: parent.left
                anchors.top: realWorldCoordinatePoints.bottom

                width: parent.width
                height: parent.height / 5 / 2 + 5

                color: "transparent"

                ConfigButton {
                    id: receiveConfig

                    buttonText: "Receive Config"

                    anchors.left: parent.left
                    anchors.leftMargin: 25
                }

                ConfigButton {
                    id: sendConfig

                    buttonText: "Transmit Config"

                    anchors.right: parent.right
                    anchors.rightMargin: 25
                }
            }
        }
    }

    Connections {
        target: vehicle_tracking_configurator_model

        function onReloadImage() {
            pointsDrawerStream.reload()
        }
    }
}
