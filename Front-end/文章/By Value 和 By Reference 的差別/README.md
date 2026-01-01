# By Value 與 By Reference

當談到 JavaScript 中的參數傳遞方式時，有兩種不同的方法：「按值傳遞」與「按引用傳遞」。兩者之間的主要差異在於傳遞參數時，參數的值或引用如何被複製和傳遞。

<br />

## By Value (按值傳遞)

當使用按值傳遞時，函式會複製傳遞過來實際參數的值，而不會影響原始值。在函式內部對參數進行修改，不會影響到函式外部的原始值。

```javascript
function modifyValue(value) {
  value = 42;
}

let x = 10;
modifyValue(x);

console.log(x); // 10 (原始值並未受到影響)
```

<br />

## By Reference (按引用傳遞)

當使用按引用傳遞時，函式會傳遞參數的引用 (記憶體位址)，而不是參數的實際值。這表示在函式內部對參數進行修改將直接影響原始值。

```javascript
function modifyArray(array) {
  array.push(100);
}

let newArray = [1, 2, 3];
modifyArray(newArray);

console.log(newArray); // [1, 2, 3, 100](原始陣列被修改)
```

<br />

## 總結

JavaScript 中的基本資料型別 (例如：數字、字串、布林值等) 是 By Value (按值傳遞) 的，而物件、陣列等複雜資料型別則是 By Reference (按引用傳遞) 的。

但嚴格來說，在 JavaScript 中並不存在真正的按引用傳遞。實際上，按引用傳遞是透過共享傳遞 (Pass-by-Sharing) 來實現。也就是說，傳遞給函式的引用 (記憶體位址) 是被複製的，但是函式內部操作的是同一個物件 (或陣列) 的引用，因此對物件或陣列的修改在函式外部也會被反映出來。
