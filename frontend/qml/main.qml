// Copyright (C) 2023 NGITL

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

import "./items"


Window {
    id: window

    signal configButtonPressedSignal(string button_text)

    property color backgroundColor: "#0f0e17"
    property color headlineColor: "#fffffe"
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
    visible: true

    title: "Configurator Interface"

    Rectangle {
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
                vehicle_tracking_configurator_model.points_drawer_clicked(pointsDrawerMouseArea.mouseX, pointsDrawerMouseArea.mouseY, pointsDrawerStream.width, pointsDrawerStream.height);
            }
        }

        Item {
            id: fullscreenButtonContainer
            anchors.fill: parent

            Rectangle {
                id: fullscreenButtonBackground
                x: fullscreenButton.x
                y: fullscreenButton.y
                color: "white"
                opacity: 0.5
                visible: fullScreenButtonMouseArea.containsMouse ? true : false
                radius: 5
                height: fullscreenButton.height
                width: fullscreenButton.width
            }

            Svg {
                id: fullscreenButton
                source: "../svg/maximize.svg"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                height: parent.height * 0.1
                fillMode: Image.PreserveAspectFit


                MouseArea {
                    id: fullScreenButtonMouseArea

                    anchors.fill: parent
                    hoverEnabled: true

                    onClicked: {
                        if(pointsDrawer.height == window.videosY) {
                            fullscreenButton.source = "../svg/minimize.svg"
                            pointsDrawer.height = window.height
                            pointsDrawer.width = window.width
                        }
                        else {
                            fullscreenButton.source = "../svg/maximize.svg"
                            pointsDrawer.height = window.videosY
                            pointsDrawer.width = window.videosX
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        id: pointsShower
        anchors.top: pointsDrawer.bottom
        anchors.topMargin: 5
        anchors.left: parent.left
        anchors.leftMargin: 5

        height: window.videosY
        width: window.videosX


        color: window.placeholderColor

        Image {
            id: pointsShowerStream

            property int id: 0

            anchors.fill: parent
            fillMode: Image.PreserveAspectFit

            visible: true
            cache: false
            source: "image://point_shower/" + id

            function reload() {
                id++;
            }
        }

        MouseArea {
            id: pointsShowerMouseArea

            anchors.fill: parent

            onClicked: {
                vehicle_tracking_configurator_model.points_shower_clicked(pointsShowerMouseArea.mouseX, pointsShowerMouseArea.mouseY, pointsShowerStream.width, pointsShowerStream.height);
            }
        }
    }

    Item {
        id: optionsRectangle

        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.left: pointsDrawer.right
        anchors.leftMargin: 5

        height: window.height - 10
        width: window.width - window.videosX - 10

        property int confBoxSizeY: (parent.height / 10 - 2.5) * 3

        Flickable {
            anchors.fill: parent
            contentWidth: optionsRectangle.width
            contentHeight: Math.max(column.height, parent.height)

            ScrollBar.vertical: ScrollBar {
                id: vertScrollBar
                policy: ScrollBar.AsNeeded
                size: 15
                interactive: true
            }

            Column {
                id: column
                width: parent.width - vertScrollBar.width
                spacing: 5

                PointsConfig {
                    id: regionOfInterestPoints

                    width: parent.width
                    height: optionsRectangle.confBoxSizeY

                    configName: "Region of Interest"
                    chosenPointDefaultText: "new"
                }

                PointsConfig {
                    id: transformationPoints

                    height: optionsRectangle.confBoxSizeY
                    width: parent.width

                    configName: "Transformation Points"
                    chosenPointDefaultText: "top_left"
                }

                Item {
                    // Container for Real World Coordinates and Color Picker Buttons

                    height: optionsRectangle.confBoxSizeY
                    width: parent.width

                    CoordinateDisplay {
                        id: realWorldCoordinatePoints

                        anchors.top: parent.top

                        height: parent.height
                        width: parent.width / 10 * 6

                        configName: "Real World Coordinate Points"
                    }

                    Rectangle {
                        // Color picker buttons

                        anchors.left: realWorldCoordinatePoints.right
                        anchors.leftMargin: 5
                        anchors.top: parent.top

                        width: parent.width / 10 * 4
                        height: optionsRectangle.confBoxSizeY

                        color: window.accentColor

                        ColorTextField {
                            id: redColorTextField

                            placeholderText: "0-255"
                            assingedColor: "red"
                            text: "0"

                            anchors.top: parent.top
                            anchors.topMargin: 5
                            anchors.left: parent.left
                            anchors.leftMargin: 5

                            width: parent.width / 4 - 10
                        }

                        ColorTextField {
                            id: greenColorTextField

                            placeholderText: "0-255"
                            assingedColor: "green"
                            text: "0"

                            anchors.top: parent.top
                            anchors.topMargin: 5
                            anchors.left: redColorTextField.right
                            anchors.leftMargin: 5

                            width: parent.width / 4 - 10
                        }

                        ColorTextField {
                            id: blueColorTextField

                            placeholderText: "0-255"
                            assingedColor: "blue"
                            text: "0"

                            anchors.top: parent.top
                            anchors.topMargin: 5
                            anchors.left: greenColorTextField.right
                            anchors.leftMargin: 5

                            width: parent.width / 4 - 10
                        }

                        ColorTextField {
                            id: alphaColorTextField

                            placeholderText: "0-255"
                            assingedColor: "alpha"
                            text: "255"

                            anchors.top: parent.top
                            anchors.topMargin: 5
                            anchors.left: blueColorTextField.right
                            anchors.leftMargin: 5

                            width: parent.width / 4 - 10
                        }

                        ColorChooserButton {
                            id: grayColorChooserButton

                            anchors.top: redColorTextField.bottom
                            anchors.topMargin: 10
                            anchors.left: parent.left
                            anchors.leftMargin: 5

                            width: parent.width / 3 - 10
                            height: 40

                            buttonText: "Gray"
                        }

                        ColorChooserButton {
                            id: blackColorChooserButton

                            anchors.top: redColorTextField.bottom
                            anchors.topMargin: 10
                            anchors.left: grayColorChooserButton.right
                            anchors.leftMargin: 5

                            width: parent.width / 3 - 10
                            height: 40

                            buttonText: "Black"
                        }

                        ColorChooserButton {
                            id: whiteColorChooserButton

                            anchors.top: redColorTextField.bottom
                            anchors.topMargin: 10
                            anchors.left: blackColorChooserButton.right
                            anchors.leftMargin: 5

                            width: parent.width / 3 - 10
                            height: 40

                            buttonText: "White"
                        }
                    }
                }


                Rectangle {
                    id: configButtonContainer

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
    }

    Connections {
        target: vehicle_tracking_configurator_model

        function onReloadImage() {
            pointsDrawerStream.reload()
            pointsShowerStream.reload()
        }

        function onColorTextChanged(texts) {
            redColorTextField.text = texts[0];
            greenColorTextField.text = texts[1];
            blueColorTextField.text = texts[2];
            alphaColorTextField.text = texts[3];
        }

        function onRegionOfInterestPointsChanged(points) {
            regionOfInterestPoints.setPoints(points);
        }

        function onTransformationPointsChanged(points) {
            transformationPoints.setPoints(points);
        }

        function onRealWorldPointsChanged(points) {
            realWorldCoordinatePoints.setPoints(points);
        }

        function onRegionOfInterestPointChosen(point) {
            regionOfInterestPoints.setChosenPoint(point);
        }

        function onTransformationPointChosen(point) {
            transformationPoints.setChosenPoint(point);
        }
    }
}
