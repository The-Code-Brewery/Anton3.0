// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
function getReply(){
    let {PythonShell} = require('python-shell')
    var path = require("path")

    var options = {
        scriptPath : path.join(__dirname, './Engine/'),
    }

    console.log(options.scriptPath,"Greetings")

    var anton = new PythonShell('greetings.py',options);

    anton.on('message',function(message){
        console.log(message)
    })
}