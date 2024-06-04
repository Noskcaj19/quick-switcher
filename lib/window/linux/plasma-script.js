let connections = {};

function sendActivated(client) {
    callDBus(
        "com.noskcaj.Switcher",
        "/com/noskcaj/Switcher",
        "com.noskcaj.Switcher",
        "NotifyActiveWindow",
        "internalId" in client ? String(client.internalId) : "",
        "caption" in client ? client.caption : "",
        "resourceClass" in client ? String(client.resourceClass) : "",
        "resourceName" in client ? String(client.resourceName) : "",
        "desktopFileName" in client ? client.desktopFileName : "",
        // how to get it out of kscript?
        // String(client.icon)
    );
}

function sendCaptionChange(client) {
    callDBus(
        "com.noskcaj.Switcher",
        "/com/noskcaj/Switcher",
        "com.noskcaj.Switcher",
        "NotifyCaptionChanged",
        "internalId" in client ? String(client.internalId) : "",
        "caption" in client ? client.caption : "",
        "resourceClass" in client ? String(client.resourceClass) : "",
        "resourceName" in client ? String(client.resourceName) : "",
        "desktopFileName" in client ? client.desktopFileName : "",
    );
}

function sendAdded(client) {
    callDBus(
        "com.noskcaj.Switcher",
        "/com/noskcaj/Switcher",
        "com.noskcaj.Switcher",
        "NotifyAddedWindow",
        "internalId" in client ? String(client.internalId) : "",
        "caption" in client ? client.caption : "",
        "resourceClass" in client ? String(client.resourceClass) : "",
        "resourceName" in client ? String(client.resourceName) : "",
        "desktopFileName" in client ? client.desktopFileName : "",
    );
}

function sendRemoved(client) {
    callDBus(
        "com.noskcaj.Switcher",
        "/com/noskcaj/Switcher",
        "com.noskcaj.Switcher",
        "NotifyRemovedWindow",
        "internalId" in client ? String(client.internalId) : ""
    );
}

function pollActivate() {
    callDBus(
        "com.noskcaj.Switcher",
        "/com/noskcaj/Switcher",
        "com.noskcaj.Switcher",
        "PollActivate",
        (v) => {
            target = workspace.windowList().find(w => String(w.internalId) === v)
            workspace.activeWindow = target;
            // workspace.raiseWindow(window);

            pollActivate()
        }
    )
}

pollActivate()

function attachCaptionListener(client) {
    if (!(client.internalId in connections)) {
        connections[client.internalId] = true;
        client.captionChanged.connect(function() {
            if (client.active) {
                sendCaptionChange(client);
            }
        });
    }
}

let handleActivated = function(client) {
    if (client === null) {
        return;
    }

    if (!client.normalWindow) return

    attachCaptionListener(client);

    sendActivated(client);
};

let handleAdded = function(client) {
    if (client === null) {
        return;
    }

    if (!client.normalWindow) return

    attachCaptionListener(client);

    sendAdded(client);
};

let handleRemoved = function(client) {
    if (client === null) {
        return;
    }

    if (!client.normalWindow) return

    attachCaptionListener(client);

    sendRemoved(client);
};


const clients = workspace.windowList();
for (var i = 0; i < clients.length; i++) {
    if (!clients[i].normalWindow) continue
    sendAdded(clients[i]);
}


// let activationEvent = workspace.windowActivated ? workspace.windowActivated : workspace.clientActivated;
if (workspace.windowActivated) {
    workspace.windowActivated.connect(handleActivated);
} else {
    // KDE version < 6
    workspace.clientActivated.connect(handleActivated);
}

workspace.windowAdded.connect(handleAdded)
workspace.windowRemoved.connect(handleRemoved)
