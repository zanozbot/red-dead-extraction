var cookie = null;

rpcDispatch({
    set: function(args, respond) {
        try {
            localStorage.setItem("ytc", args);
            respond(false, null);
        } catch (e) {
            respond(true, null);
        }
    },
    
    get: function(args, respond) {
        try {
            respond(false, localStorage.getItem("ytc"));
        } catch (e) {
            respond(true, null);
        }
    }
})
