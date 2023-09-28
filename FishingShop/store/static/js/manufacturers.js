'use strict';

const manufacturersList = document.querySelector('.manufacturers-list');

// старый способ общения с сервером
/*
const request = new XMLHttpRequest();
request.open('GET', 'http://127.0.0.1:8000/api/manufacturers');
request.setRequestHeader('Content-Type', 'application/json; charset=utf8');
request.send();
request.addEventListener('load', () => 
{
    if (request.status === 200) {
        console.log(request.response);
        const data = JSON.parse(request.response);
        data.forEach(el => {
            manufacturersList.innerHTML += `<li>${el.manufacturer_name}</li>`;
        });
    } else {
        console.log('Что-то пошло не так!');
    }
});
*/

//  актуальный способ общения с сервером

async function getResource(url) {
    let result = await fetch(url);
    if (!result.ok) {
        throw new Error(`Не удалось получить ${url}, статус: ${result.status} `);
    }
    return await result.json();
}

getResource('http://127.0.0.1:8000/api/manufacturers').
    then(data => {
        data.forEach(({ manufacturer_name }) => {
            manufacturersList.innerHTML += `<div class="manufacturers__item">${manufacturer_name}</div>`;
        });
    });