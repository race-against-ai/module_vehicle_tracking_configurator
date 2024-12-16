// Copyright (C) 2023 NGITL

import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: colorTextContainer

    property alias assingedColor: colorText.text
    property alias placeholderText: colorTextField.placeholderText
    property alias text: colorTextField.text

    color: "transparent"

    height: parent.height / 3.5

    function yes() {
        console.log(colorTextContainer.parent.height / colorTextContainer.height)
    }

    Text {
        id: colorText

        anchors.left: parent.left
        anchors.leftMargin: 0
        horizontalAlignment: Text.AlignHCenter

        height: parent.height / 2
        width: parent.width

        font.pixelSize: height - 10
        color: window.headlineColor
    }

    TextField {
        id: colorTextField

        height: parent.height / 2
        width: parent.width

        anchors.top: colorText.bottom
        anchors.topMargin: 5
        horizontalAlignment: Text.AlignHCenter

        font.pixelSize: height - 10
        color: window.headlineColor

        validator: IntValidator { bottom: 0; top: 255 }

        onTextEdited: {
            vehicle_tracking_configurator_model.color_text_changed(colorText.text, colorTextField.text);
            colorTextContainer.yes()
        }

        background: Rectangle {
            color: window.buttonColor
        }
    }
}