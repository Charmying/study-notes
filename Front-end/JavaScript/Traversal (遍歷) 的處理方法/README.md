# Traversal (遍歷) 的處理方法

在 JavaScript 中，遍歷 (Traversal) 指的是依序訪問資料結構中的每一個元素，通常是用來讀取、檢查、處理或修改其值。

### 遍歷的主要目的

- 讀取所有資料 (例如：印出陣列的每個元素)

- 找特定條件的資料 (例如：找第一個大於 100 的數字)

- 轉換或修改資料 (例如：把每個數字都乘以 2)

- 累加或彙總 (例如：計算總和或平均值)

### 常見的遍歷對象

- 陣列 (Array)：最常見，因為陣列的元素有固定順序，可以從第一個到最後一個依序處理。

- 字串 (String)：字串其實就是一個個字元的序列，也能一個一個遍歷。

- 物件 (Object)：物件沒有順序，但可以遍歷屬性名稱與對應的值。

- `Map`/`Set`：ES6 引入的新資料結構，也有自己的遍歷方法。

「遍歷陣列」是日常操作中最常見的任務之一。除了傳統的 `for` Loop 外，ES6 以後更提供許多語法糖與高階函數，能更優雅、簡潔操作陣列。

以下整理了 JavaScript 中 Traversal (遍歷) 的處理方法。

- [`for` Loop](#for-loop-傳統索引遍歷)

- [`for...of` Loop](#forof-loop-es6-可疊代值)

- [`forEach()`](#foreach-es5)

- [`map()`](#map)

- [`filter()`](#filter)

- [`reduce()`](#reduce)

- [`find()`/`findIndex()`](#findfindindex)

- [`some()`/`every()`](#someevery)

- [`entries()`/`keys()`/`values()`](#entrieskeysvalues-es6-iterator)

- [不建議的遍歷方法 `for...in`](#不建議的遍歷方法-forin)

- [進階方法補充](#進階方法補充)

- [總結](#總結)

<br />

## 主流遍歷方法

| 方法 | 是否可取索引 | 是否可中斷 | 是否回傳新值 | 適用情境 |
|-|-|-|-|-|
| `for` | ✅ | ✅ | ❌ | 需要索引或控制流程 |
| `for...of` | ❌ (可搭配 `entries()`) | ✅ | ❌ | 簡單取值 |
| `forEach()` | ✅ | ❌ | ❌ | 每個元素執行副作用 |
| `map()` | ✅ | ❌ | ✅ 新陣列 | 對每個值轉換 |
| `filter()` | ✅ | ❌ | ✅ 子陣列 | 篩選條件符合者 |
| `reduce()` | ✅ | ❌ | ✅ 聚合值 | 總和、計算、合併 |
| `find()`/`findIndex()` | ✅ | ✅ | ✅ 符合條件第一項 | 搜尋首項 |
| `some()`/`every()` | ✅ | ✅ | ✅ Boolean | 是否符合條件 |
| `entries()`/`keys()`/`values()` | ✅ (entries) | ✅ | ❌ | 可讀性高、迭代索引或值 |

<br />

## `for` Loop (傳統索引遍歷)

最基礎的迴圈方式，透過索引從陣列頭到尾遍歷每一個元素。完全控制流程。

### 語法結構

```javascript
for (初始化; 條件; 更新) {
  // 每次迴圈執行區塊
}
```

### 語法範例

```javascript
const arr = ['a', 'b', 'c'];
for (let i = 0; i < arr.length; i++) {
  console.log(i, arr[i]);
}
```

### 試用情境

- 需要索引來處理元素或搭配條件判斷

- 需要跳出迴圈 (`break`)、跳過 (`continue`)

### 補充建議

- 冗長但具備最高自由度

- 適用於複雜情況與條件流程控制

<br />

## `for...of` Loop (ES6 可疊代值)

針對「可疊代物件」的遍歷方式，最常用於陣列與字串。

### 語法結構

```javascript
for (const value of array) {
  // 處理每一個值
}
```

### 語法範例

```javascript
const arr = ['a', 'b', 'c'];
for (const value of arr) {
  console.log(value);
}
```

### 試用情境

- 不需要索引，只需處理值

- 語法簡潔、可讀性佳

### 補充建議：

- 若需要索引，使用 `array.entries()` 搭配解構

```javascript
for (const [index, value] of arr.entries()) {
  console.log(index, value);
}
```

<br />

## `forEach()` (ES5)

對陣列每個元素執行一次回呼函式，無回傳值。

### 語法結構

```javascript
array.forEach((value, index, array) => {
  // 處理每一個元素
});
```

### 語法範例

```javascript
const arr = [1, 2, 3];
arr.forEach((value, index) => {
  console.log(`第 ${index + 1} 個是 ${value}`);
});
```

### 試用情境

- 顯示資料、渲染 DOM、`console.log` 等副作用操作

- 資料不需轉換或回傳

### 補充建議：

- 無法使用 `break`/`continue` 跳出

- 不會回傳新陣列 (不同於 `map()`)

<br />

## `map()`

對每個元素執行處理並「建立一個新的陣列」回傳。

### 語法結構

```javascript
const newArray = array.map((value, index, array) => {
  return 處理後的新值;
});
```

### 語法範例

```javascript
const nums = [1, 2, 3];
const squared = nums.map(n => n * n); // [1, 4, 9]
```

### 試用情境

- 將原始資料轉換為新格式

- 保持資料純粹性與不可變性

### 補充建議：

- 一定要有 `return`，否則新陣列會是 undefined

<br />

## `filter()`

篩選陣列中符合條件的元素，並建立新的陣列。

### 語法結構

```javascript
const filteredArray = array.filter((value, index, array) => {
  return 條件判斷式 (true/false);
});
```

### 語法範例

```javascript
const nums = [1, 2, 3, 4];
const even = nums.filter(n => n % 2 === 0); // [2, 4]
```

### 試用情境

- 從陣列中挑出特定條件資料 (若找出未完成任務)

### 補充建議：

- 保留原始陣列不變

- 回傳的是一個新陣列

<br />

## `reduce()`

將陣列所有值「累加或聚合」成一個結果 (數字、字串、物件 等)。

### 語法結構

```javascript
const result = array.reduce((accumulator, currentValue, index, array) => {
  return 累加後結果;
}, 初始值);
```

### 語法範例

```javascript
const nums = [1, 2, 3];
const total = nums.reduce((sum, n) => sum + n, 0); // 6
```

### 試用情境

- 計算總和、轉成物件、統計資料等

### 補充建議：

- 強大但需較熟練，初學者可先用 `map()` + `filter()` 組合

<br />

## `find()`/`findIndex()`

- `find()`：回傳第一個符合條件的值。

- `findIndex()`：回傳第一個符合條件的索引。

### 語法結構

```javascript
array.find(item => 條件)
array.findIndex(item => 條件)
```

### 語法範例

```javascript
const users = [{id: 1}, {id: 2}];
const found = users.find(u => u.id === 2); // {id: 2}
```

### 試用情境

- 搜尋資料庫中是否有某筆資料符合條件

### 補充建議：

- 找不到時分別回傳 undefined 和 -1

<br />

## `some()`/`every()`

- `some()`：判斷是否「至少有一個」符合條件。

- `every()`：判斷是否「全部」符合條件。

### 語法結構

```javascript
array.some(item => 條件)
array.every(item => 條件)
```

### 語法範例

```javascript
const nums = [1, 3, 5];
console.log(nums.some(n => n > 4));        // true
console.log(nums.every(n => n % 2 === 1)); // true
```

### 試用情境

- 表單驗證 (所有欄位是否都填寫)、列表中是否有某種狀態

### 補充建議：

- 回傳布林值，常與程式運算結合

<br />

## `entries()`/`keys()`/`values()` (ES6 Iterator)

- `entries()`：同時取得索引和值的 iterable。

- `keys()`：只取索引。

- `values()`：只取值。

### 語法結構

```javascript
for (const [i, v] of array.entries()) { }
for (const i of array.keys()) { }
for (const v of array.values()) { }
```

### 語法範例

```javascript
const arr = ['x', 'y'];
for (const [i, v] of arr.entries()) {
  console.log(i, v);
}
```

### 試用情境

- 需要「索引和值」但又希望語法簡潔

### 補充建議：

- 搭配 `for...of` 使用最方便

<br />

##  不建議的遍歷方法 `for...in`

用來列舉物件屬性，但也可遍歷陣列的「索引字串」(不建議)。

### 錯誤使用範例

```javascript
const arr = [1, 2];
arr.foo = 'extra';
for (const key in arr) {
  console.log(key); // 0, 1, foo
}
```

### 補充建議：

- `for...in` 會遍歷原型鏈上的屬性與自訂屬性，容易出錯

<br />

## 進階方法補充

| 方法 | 功能 | 範例 |
|-|-|-|
| `Array.from()` | 將類陣列物件轉為陣列，並可遍歷 | `Array.from([1,2], x => x * 2)` |
| `flatMap()` | `map()` 並扁平化一層 | `[1,2].flatMap(n => [n, n]) // [1,1,2,2]` |
| `for await...of` | 用於 async iterable (例如：fetch stream) | `for await (const item of asyncGen()) {}` |

<br />

## 總結

| 使用目的 | 建議使用方法 |
|:-:|:-:|
| 有索引需求 | `for`、`entries()` |
| 只需取值 | `for...of`、`forEach()` |
| 建立新陣列 | `map()` |
| 篩選特定元素 | `filter()` |
| 資料累加 | `reduce()` |
| 搜尋特定值 | `find()`/`findIndex()` |
| 驗證條件 | `some()`/`every()` |
| 處理非同步串流| `for await...of` (進階) |
