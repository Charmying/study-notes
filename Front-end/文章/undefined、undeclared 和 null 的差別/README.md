# `undefined`、`undeclared` 和 `null` 的差別

在 JavaScript 中，`undefined` 、`undeclared` 和 `null` 是三個與變數相關的概念。這些概念代表了不同的情況和值。

<br />

## `undefined` (未定義)

- 代表變數已經被宣告，但目前尚未賦予任何值，或者表示物件屬性不存在的情況。

- 當宣告一個變數，但尚未賦值時，該變數的值就是 `undefined`。

- 當嘗試訪問一個物件的不存在屬性時，返回的值也是 `undefined`。

```javascript
let x;          // 宣告變數 x，但沒有賦值，此時 x 的值為 undefined
console.log(x); // undefined

const obj = { name: "Charmy", age: 27 };
console.log(obj.gender); // undefined，因為 obj 沒有 gender 屬性
```

<br />

## `undeclared` (未宣告)

- 代表變數還沒被宣告，也就是說嘗試使用一個未宣告的變數。

- 使用未宣告的變數會引發 `ReferenceError` (參考錯誤)。

```javascript
console.log(y); // ReferenceError: y is not defined
```

<br />

## `null` (空值)

- 代表變數已經被宣告，但被賦值為 `null`，表示值為空或不存在。

- `null` 是一個表示空值的特殊值。

```javascript
let QQQ = null;   // 將變數 QQQ 賦值為 null，表示 QQQ 為空值
console.log(QQQ); // null
```

<br />

## 總結

- `undefined` (未定義) 表示變數已經被宣告，但尚未賦值，或者物件屬性不存在。

- `undeclared` (未宣告) 表示變數尚未被宣告，嘗試訪問會引發 `ReferenceError` (參考錯誤)。

- `null` (空值) 表示變數已經被宣告且賦值為 `null`，表示該變數是一個空值。
