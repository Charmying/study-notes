# 淺拷貝 (Shallow Copy) 和 深拷貝 (Deep Copy)

在 JavaScript 中，淺拷貝 (Shallow Copy) 和深拷貝 (Deep Copy) 是處理物件 (Object) 或陣列 (Array) 時的概念。

<img src="https://github.com/user-attachments/assets/c86d3c8d-435a-41ea-a30d-7037202c27e0" width="100%" />

- 淺拷貝：共用同一個記憶體空間

- 深拷貝：兩個不同的記憶體空間

<br />

## 淺拷貝 (Shallow Copy)

淺拷貝是指只複製物件或陣列的最外層屬性或元素，但不會遞迴複製內部的巢狀結構。若物件的屬性是基本型別 (例如：字串、數字、布林值等) 會被直接複製，但是若屬性是參考型別 (例如：物件或陣列)，淺拷貝只會複製這個參考，不是物件或陣列本身。也就是說，拷貝後的物件與原物件共用相同的內部物件或陣列。

```javascript
let object1 = {a: 1};
let object2 = object1;
object1.a = 2;
console.log(object2.a); // 2
```

不以 JavaScript 的角度來看，依正常程式運作原理應該會輸出 `1` 才對，因為運作的原理是 Call By Value，但 JavaScript 對於物件的操作是 Call By Reference，所以上面程式碼中的 `object1` 以及 `object2` 其實是共用同一個記憶體，所以只要有一方的值改變了另一方也會跟著改變，這就叫淺拷貝。

```javascript
let object1 = {a: 1};
let object2 = {a: object1.a};
object1.a = 2;
console.log(object2.a); // 1
```

乍看之下好像真的是兩個不同的物件，的確在這種情況下是一種深拷貝，但在某些情況下其實還是屬於一種淺拷貝。

稍微改變一下 `object1` 的架構

```javascript
let object1 = {a: {a: 1}};
let object2 = {a: object1.a};
object1.a.a = 2;
console.log(object2.a); // {a: 2} (不是 {a: 1})
```

這時候 `object2` 內的值也變了，所以只要物件超過一層，這種作法只會複製表層而已，深層的內容還是共用同一個記憶體，因此兩者還是會互相影響。

<img src="https://github.com/user-attachments/assets/563518bf-e54c-4974-8792-11fd6019b3e2" width="100%" />

### 淺拷貝的應用與常見陷阱

淺拷貝適用於處理結構較為簡單的物件，特別是物件內屬性大部分都是基本型別的情況。若物件或陣列的巢狀層級不深，且開發人員不介意部分參考型別的共用，淺拷貝可以是一個簡單高效的選擇。

- `...operator`

    ES6 有一個新的 `operator`，利用 `...array` 或 `...object` 的方式達到展開 (Spread) 的效果，可以把剛剛的例子用這個 `operator` 來達到更簡單的寫法。

    ```javascript
    let object1 = {a: 1};
    let object2 = {...object1};
    object1.a = 2;
    console.log(object2.a); // 1
    ```

    看起來又是一種深拷貝，但其實這也不算是深拷貝，是跟剛剛的例子一樣，稍微變化一下又變成淺拷貝。

    ```javascript
    let obj1 = {a: {a: 1}};
    let obj2 = {...obj1};
    obj1.a.a = 2;
    console.log(obj2.a); // {a: 2}
    ```

- `Object.assign(target, source)`

    簡單來說就是將來源的 `Object` 分派給指定的物件。

    ```javascript
    let object1 = {a: 1};
    let object2 = Object.assign({}, object1);
    object1.a = 2;
    console.log(object2.a); // 1
    ```

    這也是 ES6 推出的物件操作方法，這稍微變化一下又是淺拷貝。

    ```javascript
    let object1 = {a: {a: 1}};
    let object2 = Object.assign({}, object1);
    object1.a.a = 2;
    console.log(object2.a); // {a: 2}
    ```

<br />

## 深拷貝 (Deep Copy)

深拷貝是遞迴複製物件或陣列的每一層結構，包含內部的巢狀物件或陣列。也就是說，深拷貝後的新物件與原物件完全獨立，彼此之間不會共享任何記憶體。對深拷貝後物件的修改不會影響原物件，反之亦然。


### 深拷貝的應用

深拷貝適用於處理結構較為複雜的物件，特別是當物件或陣列內部包含其他物件或陣列，且開發人員希望確保拷貝後的物件完全獨立於原物件。

- `JSON.stringify(object)` 以及 `JSON.parse(JSONString)`

    若想要真的進行深拷貝的話，就回歸最基本的 JSON 操作。

    將物件轉成字串再轉成物件，這樣就真的可以確保出來的會是一個新的物件而且是使用不同的記憶體。

    ```javascript
    let object1 = {a: {a: 1}};
    let object2 = JSON.parse(JSON.stringify(object1));
    object1.a.a = 2;
    console.log(object2.a); // {a: 1}
    ```

- lodash 內的 `cloneDeep`

    lodash 是 JS 中一套非常強大的 utility library，裡面有一個 API 叫 `_.cloneDeep(object)`，會回傳一個利用深拷貝而得到的新物件，也是比較簡單而且看起來也比較乾淨的作法。

    ```javascript
    let object1 = {a: {a: 1}};
    let object2 = _.cloneDeep(object1);
    object1.a.a = 2;
    console.log(object2.a); // {a: 1}
    ```

    需要先在專案中使用 `npm install lodash` 後再加入 `const _ = require("lodash");`

<br />

## 總結

- 淺拷貝

    只拷貝資料的第一層，當資料中包含複合型物件或陣列時，只會複製這些物件或陣列的引用。

    適用於簡單的物件或陣列，這些資料結構通常只包含基本型別的資料。若物件不包含其他內嵌的物件或陣列，淺拷貝是一個快速且有效的選擇。

- 深拷貝

    遞迴拷貝每一層屬性和元素的方式，確保拷貝後的資料與原資料完全獨立，任何一方的修改都不會影響另一方。

    適用於處理複雜的資料結構，尤其當希望確保拷貝出來的物件與原始物件完全獨立時。對於防止意外修改原始資料非常有幫助，特別是在處理多層嵌套的資料。

| 特性 | 淺拷貝 | 深拷貝 |
| - | - | - |
| 拷貝層級 | 只拷貝第一層 | 遞迴拷貝所有層級 |
| 拷貝效率 | 高效，因為只拷貝第一層資料 | 較慢，因為需要遍歷所有層級 |
| 資料獨立性 | 拷貝的資料與原資料不完全獨立 | 拷貝的資料與原資料完全獨立 |
| 適用場景 | 單層資料結構 | 多層嵌套的複雜資料結構 |
| 典型實作方法 | `Object.assign()` 或展開運算子 | `JSON.stringify()` + `JSON.parse()` 或 `_.cloneDeep()` |

<br />

## 參考資料

- [關於JS中的淺拷貝(shallow copy)以及深拷貝(deep copy)](https://medium.com/andy-blog/%E9%97%9C%E6%96%BCjs%E4%B8%AD%E7%9A%84%E6%B7%BA%E6%8B%B7%E8%B2%9D-shallow-copy-%E4%BB%A5%E5%8F%8A%E6%B7%B1%E6%8B%B7%E8%B2%9D-deep-copy-5f5bbe96c122)
