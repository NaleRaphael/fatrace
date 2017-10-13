// renderer.js
"use strict"
client.connect("tcp://127.0.0.1:4242")

document.ondragover = document.ondrop = (ev) => {
    ev.preventDefault();
}

document.body.ondrop = (ev) => {
    console.log(ev.dataTransfer.files[0].path);
    ev.preventDefault();
}
