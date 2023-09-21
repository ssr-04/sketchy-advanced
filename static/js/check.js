import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import {firebaseConfig } from "./firebase.js";

const app = initializeApp(firebaseConfig);

import {getDatabase, set, get, ref, update, remove, child} 
from "https://www.gstatic.com/firebasejs/9.17.1/firebase-database.js";
const db = getDatabase();
var user;

function get_status()
{
    const app = initializeApp(firebaseConfig);
    const dbref = ref(db);
    
    var stat;
    get(child(dbref,"users/"+user))
    .then((snapshot)=>{
        if(snapshot.exists()){
            stat = snapshot.val().status;
            display(stat);
        }
        else{
            console.log("user not found")
        }
    })
    .catch((e)=>{
        console.log("user get error"+e)
    });
}

function display(status)
{
    if(status===0){
        const state1 = document.querySelector('.state1');
        const state2 = document.querySelector('.state2');
        const state3 = document.querySelector('.state3');
        state1.style.display='block';
        state2.style.display='None';
        state3.style.display='None';
        get_status();
    }
    else{
        if(status===1){
            const state1 = document.querySelector('.state1');
            const state2 = document.querySelector('.state2');
            const state3 = document.querySelector('.state3');
            state1.style.display='None';
            state2.style.display='block';
            state3.style.display='None';
            get_status();
        }
        else{
            const state1 = document.querySelector('.state1');
            const state2 = document.querySelector('.state2');
            const state3 = document.querySelector('.state3');
            state1.style.display='None';
            state2.style.display='None';
            state3.style.display='block';
        }
    }
}

$(document).ready(function() {
    user = document.getElementById('user').value;
    get_status();
});

