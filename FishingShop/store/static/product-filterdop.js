const rangeInput = document.querySelectorAll('.price-range-input input'),
      priceInput = document.querySelectorAll('.price-input input'),
      progress = document.querySelector('.slider .progress');

let rangeGap = 0; //минимальное расстояние (зазор) между ползунками

priceInput.forEach(input => {
    input.addEventListener('input', event => {
        let minVal = parseInt(priceInput[0].value),
            maxVal = parseInt(priceInput[1].value);
        if ((maxVal - minVal >= rangeGap) && (maxVal <= 30000)){
            if (event.target.className === "input-min"){
                rangeInput[0].value = minVal;
                progress.style.left = (minVal / rangeInput[0].max) * 100 + '%';
            } else {
                rangeInput[1].value = maxVal;
                progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + '%';
            }
        }
    });
});

rangeInput.forEach(input =>{
    input.addEventListener('input', event =>{
        let minVal = parseInt(rangeInput[0].value),
            maxVal = parseInt(rangeInput[1].value);
        if (maxVal - minVal < rangeGap){
            if (event.target.className === "price-range-min range-min"){
                rangeInput[0].value = maxVal - rangeGap;
                progress.style.left = ((maxVal - rangeGap) / rangeInput[0].max) * 100 + '%';  
            } else {
                rangeInput[1].value = minVal + rangeGap; 
                progress.style.right = 100 - ((minVal + rangeGap) / rangeInput[1].max) * 100 + '%';
            }   
        } else {
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            progress.style.left = (minVal / rangeInput[0].max) * 100 + '%';
            console.log('pr1', Number((minVal / rangeInput[0].max).toFixed(1)) * 100 + '%', minVal);
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + '%';
            console.log('pr2', Number((maxVal / rangeInput[1].max).toFixed(1)) * 100 + '%', maxVal);
        }
    });
});
