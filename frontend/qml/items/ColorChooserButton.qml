// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: colorChooserButton

    radius: 20

    color: mouseHandler.containsMouse ? window.hoverButtonColor : window.buttonColor

    property string buttonText

    MouseArea {
        id: mouseHandler

        anchors.fill: parent
        
        hoverEnabled: true

        onClicked: {
            window.onColorChooserButtonClicked(buttonText);
        }
    }

    Text {
        // Button Text
        text: buttonText
        color: window.buttonTextColor
        font.pixelSize: 20

        anchors.centerIn: parent
        horizontalAlignment: Text.AlignHCenter
    }
}