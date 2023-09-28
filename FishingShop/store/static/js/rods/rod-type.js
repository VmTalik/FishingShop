'use strict';

const rodTypeList = document.querySelector('.rod-type-list');



//  актуальный способ общения с сервером

async function getResource(url) {
    let result = await fetch(url);
    if (!result.ok) {
        throw new Error(`Не удалось получить ${url}, статус: ${result.status} `);
    }
    return await result.json();
}

getResource('http://127.0.0.1:8000/api/rod_type').
    then(data => {
        data.forEach(({ id, rod_type_name, rod_type_image }) => {
            rodTypeList.innerHTML += `<a class="rod-type__item" href="/catalog-summer/rod_type/${id}"><img class="image-rod-type" src="${rod_type_image }">
            <div class="rod-type-name">${rod_type_name}</div></a>`;

        });
    });


//`<a class="rod-type__item" href="/ggggggg">${rod_type_name}</a>`