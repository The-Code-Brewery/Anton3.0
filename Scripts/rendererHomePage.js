// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.c

function getReply(){
    let {PythonShell} = require('python-shell')
    var path = require("path")

    var options = {
        scriptPath : path.join(__dirname, './Anton_Engine/'),
    }

    console.log(options.scriptPath,"Listening")

    var anton = new PythonShell('main.py',options);

    anton.on('message',function(message){
        console.log(message)

    })
}