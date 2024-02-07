class ProductFilter {
    constructor(productItems, filterList = [], FilterBy, rangeGap = 0, minRangeVal = 0, maxRangeVal = 10 ** 5) {
        this.productItems = productItems; // элементы продукта
        if (filterList != []) {
            this.filterList = filterList; // массив названий фильтров
            this.otherFilterList = filterList.filter((el) => el != this.rangeFilterBy); //массив названий фильтров, кроме текущего 
            this.otherFilterList = filterList.filter((el) => el != this.checkboxFilterBy);
        }
        this.rangeFilterBy = FilterBy.rangeFilterBy; // строка, название текущего фильтра диапазона (price, weight и т.д.)
        if (typeof this.rangeFilterBy !== 'undefined') {
            this.range = document.querySelectorAll(`.${this.rangeFilterBy}-range-input input`); // ползунок
            this.label = document.querySelectorAll(`.${this.rangeFilterBy}-input input`);  // лэбэйл ввода и вывода
            this.progress = document.querySelector(`.${this.rangeFilterBy}-progress`); // строка прогресса
            this.rangeGap = rangeGap; // минимальное расстояние(зазор) между ползунками
            this.minRangeVal = minRangeVal; // минимальное значение диапазона фильтра
            this.maxRangeVal = maxRangeVal; // максимальное значение диапазона фильтра
            this.currentMinRangeVal = minRangeVal; // текущее минимальное значение диапазона фильтра
            this.currentMaxRangeVal = maxRangeVal; // текущее максимальное значение диапазона фильтра
        }
        this.checkboxFilterBy = FilterBy.checkboxFilterBy; // строка, название текущего фильтра чекбокса (manufacture и т.д.)
        if (typeof this.checkboxFilterBy !== 'undefined') {
            this.checkboxes = document.querySelectorAll(`.${this.checkboxFilterBy}-label input[type=checkbox]`); //чекбоксы
            this.activeCheckboxName = ''; // название активного чекбокса
            this.hideCheckboxName = ''; // название скрытого чекбокса
        }
    }

    runFilter() {
        if (typeof this.checkboxFilterBy !== 'undefined') {
            this.checkboxInput();
        }
        if (typeof this.rangeFilterBy !== 'undefined') {
            this.labelOfRangeInput();
            this.rangeInput();
        }
    }

    labelOfRangeInput() {
        this.label.forEach(input => {
            input.addEventListener('input', event => {
                //this.currentMinRangeVal_int = parseInt(this.label[0].value);
                this.currentMinRangeVal_float = parseFloat(this.label[0].value);
                //this.currentMaxRangeVal_int = parseInt(this.label[1].value);
                this.currentMaxRangeVal_float = parseFloat(this.label[1].value);
                if (typeof this.currentMinRangeVal_float !== 'undefined') {
                    this.currentMinRangeVal = this.currentMinRangeVal_float
                }
                if (typeof this.currentMaxRangeVal_float !== 'undefined') {
                    this.currentMaxRangeVal = this.currentMaxRangeVal_float
                }
                if (isNaN(this.currentMinRangeVal) || (this.label[0].value[0] == this.minRangeVal)){
                    this.currentMinRangeVal = this.minRangeVal;
                    this.range[0].value = this.minRangeVal;
                    this.label[0].value = '';
                }
                if (isNaN(this.currentMaxRangeVal) || (this.label[1].value[0] == this.maxRangeVal)){
                    this.currentMaxRangeVal = this.maxRangeVal;
                    this.range[1].value = this.maxRangeVal;
                    this.label[1].value = '';
                }
                //Если текущее вводимое значение левое (min) больше чем верхняя граница диапазона 
                if (this.currentMinRangeVal > this.maxRangeVal) {
                    this.currentMinRangeVal = this.minRangeVal;
                    this.range[0].value = this.minRangeVal;
                    this.label[0].value = '';
                }
                //Если текущее вводимое значение левое (min) меньше чем нижняя граница диапазона 
                if (this.currentMinRangeVal < this.minRangeVal) {
                    this.currentMinRangeVal = this.minRangeVal;
                    this.range[0].value = this.minRangeVal;
                    
                }
                if ((this.currentMaxRangeVal - this.currentMinRangeVal >= this.rangeGap)) {
                    if (this.currentMaxRangeVal > this.maxRangeVal) {
                        this.currentMaxRangeVal = this.maxRangeVal;
                        this.label[1].value = '';
                    }
                    
                    this.range[0].value = this.currentMinRangeVal;
                    this.progress.style.left = ((this.currentMinRangeVal - this.range[0].min) / (this.range[0].max - this.range[0].min)) * 100 + '%';
                    this.progress.style.right = 100 - ((this.currentMaxRangeVal - this.range[1].min) / (this.range[1].max - this.range[1].min)) * 100 + '%';
                    this.range[1].value = this.currentMaxRangeVal;
                    this.checkRange();
                }
                else if (this.currentMinRangeVal > this.currentMaxRangeVal){
                    if (event.target.className === 'input-min') {
                        if (this.currentMaxRangeVal === this.maxRangeVal){
                            this.progress.style.left = '100%';
                            this.progress.style.right = '0%';
                        }
                        
                        this.progress.style.left = 100 - parseFloat(this.progress.style.right) + '%';
                        this.range[0].value = this.range[1].value;
                       
                    } else{
                        this.progress.style.right = 100 - parseFloat(this.progress.style.left) + '%';
                        this.range[1].value = this.range[0].value;
                    }
                    this.checkRange();
                }
            });
        });
    }

    rangeInput() {
        this.range.forEach(input => {
            input.addEventListener('input', event => {
                this.currentMinRangeVal_float= parseFloat(this.range[0].value);
                this.currentMaxRangeVal_float= parseFloat(this.range[1].value);

                if (typeof this.currentMinRangeVal_float !== 'undefined') {
                    this.currentMinRangeVal = this.currentMinRangeVal_float;
                }

                if (typeof this.currentMaxRangeVal_float !== 'undefined') {
                    this.currentMaxRangeVal = this.currentMaxRangeVal_float;
                }

                if (event.target.className === `${this.rangeFilterBy}-range-min range-min`) {
                    this.range[0].style = 'z-index: 1;'; // активен левый ползунок 
                    this.range[1].style = 'z-index: 0;';
                } else {
                    this.range[1].style = 'z-index: 1;'; // активен правый ползунок 
                    this.range[0].style = 'z-index: 0;';
                }
                if (this.currentMaxRangeVal - this.currentMinRangeVal < this.rangeGap) {
                    if (event.target.className === `${this.rangeFilterBy}-range-min range-min`) {
                        this.range[0].value = this.currentMaxRangeVal - this.rangeGap;
                        this.currentMinRangeVal = this.currentMaxRangeVal - this.rangeGap;
                        this.progress.style.left = ((this.currentMaxRangeVal - this.range[0].min - this.rangeGap) / (this.range[0].max - this.range[0].min)) * 100 + '%';
                        this.label[0].value = this.currentMinRangeVal;
                    } else {
                        this.range[1].value = this.currentMinRangeVal + this.rangeGap;
                        this.currentMaxRangeVal = this.currentMinRangeVal + this.rangeGap;
                        this.progress.style.right = 100 - ((this.currentMinRangeVal - this.range[1].min + this.rangeGap) / (this.range[1].max - this.range[1].min)) * 100 + '%';
                        this.label[1].value = this.currentMaxRangeVal;
                    }
                } else {
                    this.progress.style.left = ((this.currentMinRangeVal - this.range[0].min) / (this.range[0].max - this.range[0].min)) * 100 + '%';
                    this.progress.style.right = 100 - ((this.currentMaxRangeVal - this.range[1].min) / (this.range[1].max - this.range[1].min)) * 100 + '%';
                    this.label[0].value = this.currentMinRangeVal;
                    this.label[1].value = this.currentMaxRangeVal;
                    if (this.currentMinRangeVal == this.minRangeVal) { this.label[0].value = ''; } 
                    if (this.currentMaxRangeVal == this.maxRangeVal) { this.label[1].value = ''; }
                }
                this.checkRange();
            });
        });
    }

    checkRange() {
        this.productItems.forEach(item => {
            const productValSpan = item.querySelector(`.product__item-${this.rangeFilterBy} > span`);
            let productVal = -1
            if (productValSpan !== null) {
                productVal = productValSpan.textContent;
            } else if ((this.currentMinRangeVal == this.minRangeVal) && (this.currentMaxRangeVal == this.maxRangeVal)) {
                productVal = this.minRangeVal; //на случай, если не у всех товаров указаны параметры для фильтрации
            }
            if ((+productVal >= this.currentMinRangeVal) && (+productVal <= this.currentMaxRangeVal)) {
                item.classList.add(`active-${this.rangeFilterBy}`);
                item.classList.remove(`hide-${this.rangeFilterBy}`);
            } else {
                item.classList.add(`hide-${this.rangeFilterBy}`);
                item.classList.remove(`active-${this.rangeFilterBy}`);
            }
            this.applyFilter(item);
        });
    }

    checkboxInput() {
        this.checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', (event) => {
                if (event.target.checked) {
                    this.activeCheckboxName = checkbox.parentElement.textContent;
                    this.hideCheckboxName = null;
                    this.checkCheckbox();

                } else {
                    this.hideCheckboxName = checkbox.parentElement.textContent;
                    this.activeCheckboxName = null;
                    this.checkCheckbox();
                }
            });
        });
    }

    checkCheckbox() {
        let countProducts = 0; // количество продуктов
        let countProductsHide = 0; //количество скрытых продуктов
        this.productItems.forEach(item => {
            countProducts += 1;
            let productCheckboxNameSpan = item.querySelector(`.product__item-${this.checkboxFilterBy} > span`);
            let productCheckboxName  = '';
            if (productCheckboxNameSpan !== null){
                productCheckboxName = productCheckboxNameSpan.textContent;
            } 
            if ((this.activeCheckboxName === productCheckboxName)) {
                item.classList.add(`active-${this.checkboxFilterBy}`);
                item.classList.remove(`hide-${this.checkboxFilterBy}`);
            }
            else if ((this.hideCheckboxName === productCheckboxName)) {
                item.classList.add(`hide-${this.checkboxFilterBy}`);
                item.classList.remove(`active-${this.checkboxFilterBy}`);
                countProductsHide += 1;
            }
            else if ((this.hideCheckboxName !== productCheckboxName) && !item.classList.contains(`active-${this.checkboxFilterBy}`)) {
                item.classList.add(`hide-${this.checkboxFilterBy}`);
                item.classList.remove(`active-${this.checkboxFilterBy}`);
                countProductsHide += 1;
            }
            this.applyFilter(item);
        });
        // Если все чекбоксы неактивны, то будем показывать все товары изначальные
        if (countProductsHide === countProducts) {
            this.productItems.forEach(item => {
                item.classList.remove(`active-${this.checkboxFilterBy}`);
                item.classList.remove(`hide-${this.checkboxFilterBy}`);
                this.applyFilter(item);
            });
        }
    }

    applyFilter(item) {
        let hideFlagByOtherFilters = false; //флаг скрытия элементов нетекущими фильтрами
        this.otherFilterList.forEach(nameOtherFilter => {
            if (item.classList.contains(`hide-${nameOtherFilter}`)) {
                hideFlagByOtherFilters = true;
            }
        });
        if (!item.classList.contains(`hide-${this.rangeFilterBy}`) && !item.classList.contains(`hide-${this.checkboxFilterBy}`) &&
            !hideFlagByOtherFilters) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    }
}


const productListItems = document.querySelectorAll('.products-list__item'); // элементы продукта
const filterList = ['price', 'manufacturer']; // массив названий фильтров

const paramsCheckboxListItems = document.querySelectorAll('.checkboxName'); // названия чекбосов
const paramsRangeListItems = document.querySelectorAll('.rangeName'); // названия фильтров диапазонов


//объект дополнительных фильтров диапазона
let paramsRangeItemObjects = {}

//массив дополнительных фильтров чекбокса
let paramsCheckboxItemList = []

paramsRangeListItems.forEach(elem => {
    //Добавляем названия дополнительных фильтров диапазона в массив
    filterList.push(elem.dataset.paramrange);
    //Получаем объект дополнительных фильтров диапазона (названия фильтров и соответствующие массивы с min и max параметрами диапазона)
    paramsRangeItemObjects[elem.dataset.paramrange] = document.querySelector(`.${elem.dataset.paramrange}-range-input`).dataset.rangeminmax.split(' ');
});

paramsCheckboxListItems.forEach(elem => {
    //Добавляем названия дополнительных фильтров чекбокса в общий массив фильтров
    filterList.push(elem.dataset.paramcheckbox);
    //Добавляем названия дополнительных фильтров чекбокса в массив чекбоксов
    paramsCheckboxItemList.push(elem.dataset.paramcheckbox);
});

//минимальная и максимальная цена товара для фильтра
const min_price = document.querySelector('.price-range-min').value;
const max_price = document.querySelector('.price-range-max').value;

//фильтр товаров по цене (учитывая остальные фильтры)
const productFilterPrice = new ProductFilter(productListItems, filterList, { rangeFilterBy: 'price' }, 0, min_price, max_price);
productFilterPrice.runFilter();

//фильтр товаров по производителю (учитывая остальные фильтры)
const productFilterManufacturer = new ProductFilter(productListItems, filterList, { checkboxFilterBy: 'manufacturer' });
productFilterManufacturer.runFilter();


//дополнительные фильтры диапазона для товаров (учитывая остальные фильтры)
for (let param in paramsRangeItemObjects) {
    const productFilter = new ProductFilter(
        productListItems,
        filterList,
        { rangeFilterBy: param },
        0,
        paramsRangeItemObjects[param][0],
        paramsRangeItemObjects[param][1]);
    productFilter.runFilter();
}

// дополнительные чекбокс фильтры товаров (учитывая остальные фильтры)
paramsCheckboxItemList.forEach(param => {
    const productFilter = new ProductFilter(
        productListItems,
        filterList,
        { checkboxFilterBy: param });
    productFilter.runFilter();

});

//сделаем невидимыми некоторые параметры товаров
const productsParameters = document.querySelectorAll('.products-list__item-parameters');
productsParameters.forEach(elem => {
    for (let i = 4; i < elem.children.length - 1; i++){ //с 5-го по предпоследний, пар-ры на карточках товаров скрываем
        elem.children[i].style.display = 'none';
    }
});


//Сортировка товаров

const productsSortSelect = document.getElementById('sort');
const productList = document.querySelector('.product-list');

productsSortSelect.addEventListener('change', () => {
    const arrayProductItems = [...productListItems];
    let sortedArrayProductItems = [];
    if (productsSortSelect.value == 'price'){
        sortedArrayProductItems = arrayProductItems.sort((a, b) => +a.dataset.price - +b.dataset.price);
    }
    else if (productsSortSelect.value == '-price') {
        sortedArrayProductItems = arrayProductItems.sort((a, b) => +b.dataset.price - +a.dataset.price);
    }
    else if (productsSortSelect.value == 'popular') {
        sortedArrayProductItems = arrayProductItems.sort((a, b) => +b.dataset.count_buyproduct - +a.dataset.count_buyproduct);
    }
    else if (productsSortSelect.value == 'discussed') {
        sortedArrayProductItems = arrayProductItems.sort((a, b) => +b.dataset.count_comments - +a.dataset.count_comments);
    }
    else if (productsSortSelect.value == 'rating') {
        sortedArrayProductItems = arrayProductItems.sort((a, b) => +b.dataset.rating - +a.dataset.rating);
    }
    else if (productsSortSelect.value == 'new') {
        sortedArrayProductItems = arrayProductItems.sort((a, b) => new Date(b.dataset.supply_date) - new Date(a.dataset.supply_date));
    }
    else {
        sortedArrayProductItems = arrayProductItems
    }
    productList.innerHTML = '';
    sortedArrayProductItems.forEach(element => {
        productList.appendChild(element);
    });
});
