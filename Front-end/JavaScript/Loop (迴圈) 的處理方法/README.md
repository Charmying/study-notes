# Loop (迴圈) 的處理方法

在 JavaScript 中處理重複性任務時，迴圈 (Loop) 是非常重要的控制流程工具。JavaScript 提供了多種迴圈類型，各自有不同的語法特性與適用情境。

以下整理了 JavaScript 中 Loop (迴圈) 的處理方法。

- [`for` Loop](#for-loop)

- [`while` Loop](#while-loop-條件迴圈)

- [`do...while` Loop](#dowhile-loop-先做再判斷)

- [`for...of` Loop](#forof-loop-es6)

- [`for...in` Loop](#forin-loop)

- [`Array.prototype.forEach()`](#arrayprototypeforeach-陣列迭代函式)

- [其他函數式方法](#其他函數式方法-非傳統迴圈)

- [各迴圈使用建議總整理](#各迴圈使用建議總整理)

- [總結](#總結)

<br />

## `for` Loop

`for` 是最基本的迴圈語法，用於已知要重複執行幾次的情況，透過計數器變數控制。

### 語法結構

```javascript
for (初始化; 條件; 遞增) {
  // 執行區塊
}
```

### 範例

```javascript
for (let i = 0; i < 5; i++) {
  console.log(`第 ${i + 1} 次`);
}
```

### 試用情境

- 遍歷固定次數 (例如：迴圈執行 10 次)。

- 需要使用索引值時 (例如：讀取陣列元素)。

### 補充

- `for` 是同步執行。

- 常與 `break` (中止) 和 `continue` (跳過本次) 搭配使用。

<br />

## `while` Loop (條件迴圈)

在條件為 `true` 時持續執行。用於「不確定重複次數，但有條件停止」的場景。

### 語法結構

```javascript
while (條件) {
  // 執行區塊
}
```

### 範例

```javascript
let i = 0;
while (i < 3) {
  console.log(`目前 i = ${i}`);
  i++;
}
```

### 試用情境

- 使用者輸入驗證 (直到輸入正確)。

- 遊戲回合控制 (直到某個條件結束)。

### 補充

- 若條件永遠為 `true` 會變成無限迴圈。

- 建議條件內部要有變數更新機制。

<br />

## `do...while` Loop (先做再判斷)

會先執行一次再進行條件判斷，保證區塊內至少執行一次。

### 語法結構

```javascript
do {
  // 執行區塊
} while (條件);
```

### 範例

```javascript
let password;
do {
  password = prompt("請輸入密碼：");
} while (password !== "1234");
```

### 試用情境

- 必須至少進行一次的任務 (例如：用戶提示)。

- 表單輸入與驗證流程。

### 補充

- 不論條件是否成立，區塊會先執行一次。

<br />

## `for...of` Loop (ES6)

用來遍歷「可疊代 (iterable)」的物件，例如：陣列、字串、`Map`、`Set`。

### 語法結構

```javascript
for (const item of 可迭代物件) {
  // 使用 item
}
```

### 範例

```javascript
const fruits = ["apple", "banana", "cherry"];
for (const fruit of fruits) {
  console.log(fruit);
}
```

### 試用情境

- 遍歷陣列或字串內容。

- 簡潔方式處理迭代。

### 補充

- 無法取得索引 (使用 `for...in` 或傳統 `for`)

- 可搭配 `entries()` 同時取得索引與值

<br />

## `for...in` Loop

用於列舉物件的可列舉屬性名稱 (Key)，也可用於陣列 (不推薦)。

### 語法結構

```javascript
for (const key in 物件) {
  // 使用 key 和 物件[key]
}
```

### 範例

```javascript
const user = { name: "Charmy", age: 28 };
for (const key in user) {
  console.log(`${key}：${user[key]}`);
}
```

### 試用情境

- 列出物件的所有屬性。

- 動態列印 JSON 結構。

### 補充

- 若用於陣列，會取得索引值字串 (不推薦)

- 會列出原型鏈上的屬性，需加上 `hasOwnProperty` 過濾

<br />

## `Array.prototype.forEach()` (陣列迭代函式)

是一個陣列方法，接受 Callback Function，對陣列每一個元素執行該函式。

### 語法結構

```javascript
array.forEach((value, index, array) => {
  // 執行動作
});
```

### 範例

```javascript
const scores = [90, 80, 100];
scores.forEach((score, index) => {
  console.log(`第 ${index + 1} 個分數是 ${score}`);
});
```

### 試用情境

- 陣列處理，像是顯示資料、統計等。

- 常與 DOM 操作、渲染列表搭配使用。

### 補充

- 無法使用 `break` 或 `continue`。

- 無回傳值 (不同於 `map()`)。

<br />

## 其他函數式方法 (非傳統迴圈)

這些不是「語法上的迴圈」，但也是執行重複操作的方式

| 方法 | 功能 | 回傳 |
|-|-|-|
| `map()` | 對每個元素運算並回傳新陣列 | 新陣列 |
| `filter()` | 篩選符合條件的元素 | 新陣列 |
| `reduce()` | 累加或累計計算 | 累加結果 |
| `some()`/`every()` | 驗證是否有某些或所有元素符合條件 | Boolean |

<br />

## 各迴圈使用建議總整理

| 目的 | 建議使用 |
|:-:|:-:|
| 固定次數、索引控制 | `for` |
| 直到條件不成立 | `while` |
| 至少執行一次 | `do...while` |
| 針對「值」遍歷 | `for...of` |
| 針對「鍵」遍歷 | `for...in` (物件) |
| 陣列資料迭代處理 | `forEach()`、`map()` |
| 高階函式使用 (過濾、計算) | `filter()`、`reduce()` |

<br />

## 總結

- `for` 與 `while` 是基本的迴圈控制工具，靈活但稍繁瑣。

- `for...of` 與 `for...in` 是語法糖，針對物件與陣列有專用用途。

- `forEach()` 與 `map()` 更符合現代 JavaScript 的寫法。
