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
    property color buttonColor: "#658e8e"
    property color hoverButtonColor: "#99b5b5"
    property color buttonTextColor: "#fffffe"
    property color buttonSelectColor: "#2c4444"
    property color placeholderColor: "#505050"
    property color accentColor: "#162424"
    property color accentColor2: "#e53170"
    property int videosX: window.width * 0.37109375
    property int videosY: window.height * 0.490740 + 3.75
    property real targetAspectRatio: 9 / 16

    width: 1536
    height: 864
    minimumWidth: 1536
    minimumHeight: 864

    color: backgroundColor
    visible: true

    title: "Configurator Interface"

    onVisibilityChanged: {
        if (window.visibility == Window.Maximized) {
            window.visibility = Window.FullScreen;
        }
    }

    Item {
        id: baseContainer

        implicitWidth: window.width
        implicitHeight: window.width * targetAspectRatio

        focus: true

        Keys.onPressed: (event) => {
            if (event.key == Qt.Key_Left) {
                vehicle_tracking_configurator_model.arrow_button_clicked("button", "left");
                event.accepted = true;
            } else if (event.key == Qt.Key_Right) {
                vehicle_tracking_configurator_model.arrow_button_clicked("button", "right");
                event.accepted = true;
            } else if (event.key == Qt.Key_F11) {
                if (window.visibility == Window.FullScreen) {
                    window.visibility = Window.Windowed;
                } else {
                    window.visibility = Window.FullScreen;
                }
            }
        }

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
                    vehicle_tracking_configurator_model.points_drawer_clicked(
                        pointsDrawerMouseArea.mouseX,
                        pointsDrawerMouseArea.mouseY,
                        pointsDrawerStream.paintedWidth,
                        pointsDrawerStream.paintedHeight,
                        pointsDrawerStream.width,
                        pointsDrawerStream.height
                    );
                }
            }

            Item {
                id: fullscreenButtonContainer

                anchors.fill: parent

                Rectangle {
                    id: fullscreenButtonBackground

                    x: fullscreenButton.x
                    y: fullscreenButton.y

                    height: fullscreenButton.height
                    width: fullscreenButton.width

                    color: "white"
                    opacity: 0.5
                    visible: fullScreenButtonMouseArea.containsMouse ? true : false
                    radius: 5
                }

                Svg {
                    id: fullscreenButton

                    source: "../assets/svg/maximize.svg"

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
                                fullscreenButton.source = "../assets/svg/minimize.svg"
                                pointsDrawer.height = window.height
                                pointsDrawer.width = window.width
                            }
                            else {
                                fullscreenButton.source = "../assets/svg/maximize.svg"
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
                    vehicle_tracking_configurator_model.points_shower_clicked(
                        pointsShowerMouseArea.mouseX,
                        pointsShowerMouseArea.mouseY,
                        pointsShowerStream.paintedWidth,
                        pointsShowerStream.paintedHeight,
                        pointsShowerStream.width,
                        pointsShowerStream.height
                    );
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

                    interactive: true
                    policy: ScrollBar.AsNeeded
                }

                Column {
                    id: column

                    width: parent.width - 23

                    anchors.top: parent.top
                    anchors.left: parent.left

                    spacing: 5

                    CheckboxContainer {
                        id: checkboxContainer
                        width: parent.width
                        height: parent.height / 10
                    }

                    PointsConfig {
                        id: regionOfInterestPoints

                        width: parent.width
                        height: optionsRectangle.confBoxSizeY

                        configName: "Region of Interest"
                        chosenPointDefaultText: "new"

                        Rectangle {
                            id: regionOfInterestPointsCover
                            visible: false
                            anchors.fill: parent
                            color: "black"
                            opacity: 0.5
                        }
                    }

                    PointsConfig {
                        id: transformationPoints

                        width: parent.width
                        height: optionsRectangle.confBoxSizeY

                        configName: "Transformation Points"
                        chosenPointDefaultText: "top_left"

                        Rectangle {
                            id: transformationPointsCover

                            anchors.fill: parent

                            visible: true
                            color: "black"
                            opacity: 0.5
                        }
                    }

                    Item {
                        id: realWorldAndColorPickerContainer

                        height: optionsRectangle.confBoxSizeY
                        width: parent.width

                        CoordinateDisplay {
                            id: realWorldCoordinatePoints

                            anchors.top: parent.top

                            height: parent.height
                            width: parent.width * 0.6

                            configName: "Real World Coordinate Points"
                        }

                        Rectangle {
                            id: colorPickerContainer

                            anchors.left: realWorldCoordinatePoints.right
                            anchors.leftMargin: 5
                            anchors.top: parent.top

                            width: parent.width * 0.4
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
                                height: parent.height * 0.1593

                                buttonText: "Gray"
                            }

                            ColorChooserButton {
                                id: blackColorChooserButton

                                anchors.top: redColorTextField.bottom
                                anchors.topMargin: 10
                                anchors.left: grayColorChooserButton.right
                                anchors.leftMargin: 5

                                width: parent.width / 3 - 10
                                height: parent.height * 0.1593

                                buttonText: "Black"
                            }

                            ColorChooserButton {
                                id: whiteColorChooserButton

                                anchors.top: redColorTextField.bottom
                                anchors.topMargin: 10
                                anchors.left: blackColorChooserButton.right
                                anchors.leftMargin: 5

                                width: parent.width / 3 - 10
                                height: parent.height * 0.1593

                                buttonText: "White"
                            }
                        }
                    }


                    Rectangle {
                        id: configButtonContainer

                        width: parent.width
                        height: parent.height / 10 + 5

                        color: "transparent"

                        ConfigButton {
                            id: receiveConfig
                            buttonText: "Receive Config"
                            anchors.left: parent.left
                            anchors.leftMargin: parent.width / 4 - width / 2
                        }

                        ConfigButton {
                            id: sendConfig
                            buttonText: "Transmit Config"
                            anchors.right: parent.right
                            anchors.rightMargin: parent.width / 4 - width / 2
                        }
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
