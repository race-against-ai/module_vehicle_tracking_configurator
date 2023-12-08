// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: configButton

    anchors.verticalCenter: parent.verticalCenter
    anchors.top: parent.top
    anchors.topMargin: 5

    width: parent.width / 3
    height: parent.height / 2

    radius: 20

    color: mouseHandler.containsMouse ? window.hoverButtonColor : window.buttonColor

    property string buttonText

    MouseArea {
        id: mouseHandler

        anchors.fill: parent

        hoverEnabled: true

        onClicked: {
            vehicle_tracking_configurator_model.config_button_pressed(configButton.buttonText);
        }
    }

    Text {
        // Button Text
        text: parent.buttonText
        color: window.buttonTextColor
        font.pixelSize: 30

        anchors.centerIn: parent
        horizontalAlignment: Text.AlignHCenter
    }
}
