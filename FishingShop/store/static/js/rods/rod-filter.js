import ProductFilter from '../product-filter.js';

const rodsListItems = document.querySelectorAll('.rods-list__item'); // элементы продукта
const filterList = ['price', 'weight', 'length', 'manufacturer']; // массив названий фильтров

//фильтр удочек по цене (учитывая остальные фильтры)
const rodsFilterPrice = new ProductFilter(rodsListItems, filterList, {rangeFilterBy: 'price'}, 0, 0, 30000);
rodsFilterPrice.runFilter();

//фильтр удочек по производителю (учитывая остальные фильтры)
const rodsFilterManufacturer = new ProductFilter(rodsListItems, filterList, {checkboxFilterBy: 'manufacturer'});
rodsFilterManufacturer.runFilter();


//фильтр удочек по массе (учитывая остальные фильтры)
const rodsFilterWeight = new ProductFilter(rodsListItems, filterList, {rangeFilterBy: 'weight'}, 0, 0, 800);
rodsFilterWeight.runFilter();


//фильтр удочек по длине (учитывая остальные фильтры)
const rodsFilterLength = new ProductFilter(rodsListItems, filterList, {rangeFilterBy: 'length'}, 0, 50, 1600);
rodsFilterLength.runFilter();