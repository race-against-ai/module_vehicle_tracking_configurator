// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: configButton

    anchors.verticalCenter: parent.verticalCenter
    anchors.top: parent.top

    width: parent.width / 3
    height: parent.height / 2

    radius: 20

    color: mouseHandler.containsMouse ? window.hoverButtonColor : window.buttonColor

    property alias buttonText: buttonText.text

    MouseArea {
        id: mouseHandler

        anchors.fill: parent

        hoverEnabled: true

        onClicked: {
            vehicle_tracking_configurator_model.config_button_pressed(configButton.buttonText);
        }
    }

    Text {
        id: buttonText

        color: window.buttonTextColor
        font.pixelSize: 5000
        minimumPixelSize: 10
        fontSizeMode: Text.Fit

        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
