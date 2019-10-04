'use strict';
let a = {};
document.addEventListener('DOMContentLoaded', ()=>{

    document.querySelector('#submit').onclick = () => {
        // Initialize new Ajax request
        const request = new XMLHttpRequest();
        request.open('POST', 'http://127.0.0.1:8000/api/getwords/');
        console.log("Characters submitted");
        request.onload = () =>{
            const data = JSON.parse(JSON.parse(request.responseText));
            a = data;
            console.log(`data: ${data}`)
            console.log(`typeof data: ${typeof(data)}`)
            document.querySelector('#suggested_word').innerHTML = data['suggested_word'];
            console.log(`suggested word: ${data['suggested_word']}`);
            document.querySelector('#points').innerHTML = data['points'];
            console.log(`points: ${data['points']}`);
        }

        // const data = new FormData();
        // data.append('choice', document.querySelector('#choice'));
        let data = JSON.stringify({'characters': document.querySelector('#characters').value})
        request.send(data);
    }
});