// Copyright (C) 2023 NGITL

import QtQuick 2.15

Rectangle {
    id: pointsConfig

    property alias configName: configNameText.text

    color: window.accentColor

    function setPoints(points) {
        imagePointXInput.text = points[0];
        imagePointYInput.text = points[1];
        realPointXInput.text = points[2];
        realPointYInput.text = points[3];
    }

    Text {
        id: configNameText

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
        placeholderText: "X"

        anchors.top: imageCoordsText.bottom
        anchors.left: parent.left
    }

    CoordinateTextField {
        id: imagePointYInput

        assingedId: "imagePointYInput"
        placeholderText: "Y"

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
        placeholderText: "X"

        anchors.top: realCoordsText.bottom
        anchors.left: pointsConfig.left
    }

    CoordinateTextField {
        id: realPointYInput

        assingedId: "realPointYInput"
        placeholderText: "Y"

        anchors.top: realCoordsText.bottom
        anchors.left: realPointXInput.right
    }
}
