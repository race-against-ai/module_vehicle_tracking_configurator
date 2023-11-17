// Copyright (C) 2023 NGITL

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: colorTextContainer

    property string assingedColor
    property string placeholderText

    color: "transparent"

    height: 80

    Text {
        id: colorText

        anchors.left: parent.left
        anchors.leftMargin: 0
        horizontalAlignment: Text.AlignHCenter

        height: parent.height / 2
        width: parent.width

        text: assingedColor

        font.pixelSize: 25
        color: window.headlineColor
    }

    TextField {
        id: colorTextField

        height: parent.height / 2
        width: parent.width

        placeholderText: colorTextContainer.placeholderText

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: colorText.bottom
        anchors.topMargin: 5
        horizontalAlignment: Text.AlignHCenter


        font.pixelSize: 25
        color: window.headlineColor

        onTextEdited: {
            window.onColorTextChanged(assingedColor, colorTextField.text)
        }

        background: Rectangle {
            color: window.buttonColor
        }
    }
}
