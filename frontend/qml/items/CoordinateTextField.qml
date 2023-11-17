// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
    id: coordInput

    width: 82
    height: 40

    property string assingedId

    anchors.topMargin: 5
    anchors.leftMargin: 5
    horizontalAlignment: Text.AlignHCenter

    font.pixelSize: 25
    color: window.headlineColor

    onTextEdited: {
        window.onCoordinateTextChanged(assingedId, pointsConfig.configName, coordInput.text);
    }

    background: Rectangle {
        color: window.buttonColor
    }
}
