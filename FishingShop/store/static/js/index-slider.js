const slider = document.querySelector('.main__slider'), //блок слайдера
    slides = document.querySelectorAll('.main__slide'), //все слайды
    prev = document.querySelector('.main__slider-prev'), //стрелка влево
    next = document.querySelector('.main__slider-next'), //стрелка вправо
    slidesWrapper = document.querySelector('.main__slider-wrapper'),
    slidesField = document.querySelector('.main__slider-inner'), //поле со слайдами
    width = getComputedStyle(slidesWrapper).width, //ширина примененного стиля слайдера
    dots = document.querySelector('.dots'); // индикаторы (точки) на слайдере
    dots_list = []; //массив точек

let offset = 0; //отступ
let slideNumber = 1; //номер текущего слайда

slidesField.style.width = 100 * slides.length + '%';

slides.forEach(slide => {
    slide.style.width = width;
});

//Функция для перелистывания на следующий слайд
function nextSlide() {
    if (offset == +width.slice(0, width.length - 2) * (slides.length - 1)){
        offset = 0;
    } else {
        offset += +width.slice(0, width.length - 2);
    }
    if (slideNumber == slides.length){
        slideNumber = 1;
    } else {
        slideNumber++;
    }
    changeSlideStyles();
}

next.addEventListener('click', nextSlide);

//Функция для перелистывания на предыдущий слайд
function prevSlide() {
    if (offset == 0) {
        offset = +width.slice(0, width.length - 2) * (slides.length - 1);
    } else {
        offset -= +width.slice(0, width.length - 2);
    }
    if (slideNumber == 1) {
        slideNumber = slides.length;
    } else {
        slideNumber--;
    }
    changeSlideStyles();
}

prev.addEventListener('click', prevSlide);

//Функция изменения стилей слайдов
function changeSlideStyles(){
    slidesField.style.transform = `translateX(-${offset}px)`;
    dots_list.forEach(dot => dot.style.opacity = '.4');
    dots_list[slideNumber - 1].style.opacity = 0.7;
}

// Создание индикаторов (точек) на слайдере
for (let i = 0; i < slides.length; i++){
    const dot = document.createElement('li');
    dot.setAttribute('data-slide_to', i + 1);
    if (i == 0) {
        dot.style.opacity = 0.7;
    }
    dots.append(dot);
    dots_list.push(dot);
}

//Добавляем функциональность индикаторам (точкам) на слайдере. 
//При нажатии на точку происходит перелистывание на требуемый слайд
dots_list.forEach(dot => {
    dot.addEventListener('click', (e) => {
        const slideTo = e.target.getAttribute('data-slide_to');
        slideNumber = slideTo;
        offset = +width.slice(0, width.length - 2) * (slideTo - 1); //сдвиг на нужный слайд
        changeSlideStyles();
    });
});

//Таймер. Автоперелистывание

let timerSlide = setInterval(() => nextSlide(), 3000);

slider.addEventListener('mouseover', () => {
    clearInterval(timerSlide)
}); // при наведении на слайдер перелистывание заканчивается

slider.addEventListener('mouseleave', () => {
    timerSlide = setInterval(() => nextSlide(), 3500)
}); // когда курсор со слайдера уходит, перелистывание возобновляется