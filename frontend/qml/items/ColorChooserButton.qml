// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: colorChooserButton

    radius: 20

    color: mouseHandler.containsMouse ? window.hoverButtonColor : window.buttonColor

    property alias buttonText: buttonTextContainer.text

    MouseArea {
        id: mouseHandler

        anchors.fill: parent
        
        hoverEnabled: true

        onClicked: {
            vehicle_tracking_configurator_model.color_chooser_button_clicked(buttonTextContainer.text);
        }
    }

    Text {
        id: buttonTextContainer

        text: buttonText
        color: window.buttonTextColor
        font.pixelSize: 20

        anchors.centerIn: parent
        horizontalAlignment: Text.AlignHCenter
    }
}