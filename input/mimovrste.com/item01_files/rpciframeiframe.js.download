function addEvent(element, eventName, fn) {
    if (element.addEventListener)
        element.addEventListener(eventName, fn, false);
    else if (element.attachEvent)
        element.attachEvent('on' + eventName, fn);
}


function rpcDispatch(handlers) {
    var backInflightCallbacks = {};
    var backRequestIndex = 0;
    var backLink = null;
    var backRequestPreQueue = [];


    function onRequestEvent(request, event) {
        var iid = request.instanceId;
        var rid = request.requestId;
        var cmd = request.cmd;
        var args = request.args;

        function respond(err, value) {
            var response = {
                messageType: 'response',
                requestId: rid,
                instanceId: iid,
                isError: err,
                value: value
            }
            
            event.source.postMessage(JSON.stringify(response), '*');
        }

        if (cmd == 'backLinkInit') {
            backLink = {
                window: event.source,
                instanceId: iid
            }
            respond(false, {});

            for (var i = 0, l = backRequestPreQueue.length; i < l; i++) {
                var r = backRequestPreQueue[i]
                var preMsg = r.preMsg
                var callback = r.callback

                preMsg.instanceId = backLink.instanceId;
                backInflightCallbacks[preMsg.requestId] = callback;
                backLink.window.postMessage(JSON.stringify(preMsg), '*');
            }

            backRequestPreQueue = [];
            
        } else {
            var handler = handlers[cmd]
            if (handler) {
                handler(args, respond); // XXX: try
            } else {
                respond(true, 'no such method: ' + cmd);
            }
        }
    }

    
    function onBackResponseEvent(response, event) {
        var rid = response.requestId;
        var callback = backInflightCallbacks[rid];

        if (callback) {
            delete backInflightCallbacks[rid]; // null
            callback(response.isError, response.value); // try
        } else {
            // nemam jak logovat
        }
    }

    
    function onMessageEvent(event) {
        var message = JSON.parse(event.data) // XXX

        var messageType = message.messageType;

        if      (messageType == 'request')  { onRequestEvent(message, event) }
        else if (messageType == 'response') { onBackResponseEvent(message, event) }
        else {
            // nemam jak logovat
        }
    }



    function backRpc(cmd, args, callback) {
        var rid = ++backRequestIndex;

        var preMsg = {
            messageType: 'request',
            // instanceId: backLink.instanceId,
            requestId: rid,
            cmd: cmd,
            args: args
        };

        if (backLink) {
            preMsg.instanceId = backLink.instanceId;
            backInflightCallbacks[rid] = callback;
            backLink.window.postMessage(JSON.stringify(preMsg), '*');
        } else {
            backRequestPreQueue.push( { preMsg: preMsg, callback: callback });
        }
    }
    
    
    addEvent(window, 'message', onMessageEvent);

    this.backRpc = backRpc

    return this;
}
