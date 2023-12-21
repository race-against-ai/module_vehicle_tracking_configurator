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

    text: "0"

    font.pixelSize: 25
    color: window.headlineColor

    // FIXME: Fix this so it limits it to 1332 and not 9999 (could be bug in Qt)
    validator: IntValidator { bottom: 0; top: 1332 }

    onTextEdited: {
        vehicle_tracking_configurator_model.coordinate_text_changed(assingedId, pointsConfig.configName, text);
    }

    background: Rectangle {
        id: coordInputBackground

        color: window.buttonColor
    }
}
