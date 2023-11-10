// Copyright (C) 2023 NGITL
import QtQuick 2.15

import "../items"

Rectangle {
    id: pointsConfig

    property string configName

    color: window.accentColor

    Text {
        id: configNameText

        text: configName

        anchors.top: pointsConfig.top
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 40
    }

    Text {
        id: imageCoordsText

        text: "Image Coordinates"

        anchors.top: configNameText.bottom
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 30
    }

    CoordinateTextField {
        id: imagePointXInput

        assingedId: "imagePointXInput"
        placeholderTextText: "X"

        anchors.top: imageCoordsText.bottom
        anchors.left: parent.left
    }

    CoordinateTextField {
        id: imagePointYInput

        assingedId: "imagePointYInput"
        placeholderTextText: "Y"

        anchors.top: imageCoordsText.bottom
        anchors.left: imagePointXInput.right
    }

    Text {
        id: realCoordsText

        text: "Real World Coordinates"

        anchors.top: imagePointYInput.bottom
        anchors.topMargin: 5
        anchors.left: pointsConfig.left
        anchors.leftMargin: 5

        color: window.headlineColor
        fontSizeMode: Text.Fit
        minimumPixelSize: 10
        font.pixelSize: 30
    }

    CoordinateTextField {
        id: realPointXInput

        assingedId: "realPointXInput"
        placeholderTextText: "X"

        anchors.top: realCoordsText.bottom
        anchors.left: pointsConfig.left
    }

    CoordinateTextField {
        id: realPointYInput

        assingedId: "realPointYInput"
        placeholderTextText: "Y"

        anchors.top: realCoordsText.bottom
        anchors.left: realPointXInput.right
    }
}
