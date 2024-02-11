//Скрипт для прокрутки страницы к сохранённому положению после её перезагрузки.

const initTime = localStorage.getItem('initTime'); //время (в миллисекундах) инициализации элементов в localStorage
const limitTime = 500; // лимит времени (в миллисекундах) на существование элементов в localStorage
const addToBasket = document.querySelectorAll('.add_to_basket'); //элементы добавления товара в корзину


if (initTime !== null) {
    if (+new Date() - initTime <= limitTime) {
        window.scroll(0, localStorage.getItem('scrollY'));
    }else {
        localStorage.removeItem('initTime');
        localStorage.removeItem('scrollY');
    }
}

window.addEventListener('unload', () => {
    localStorage.setItem('initTime', +new Date());
    localStorage.setItem('scrollY', window['scrollY']);
});
