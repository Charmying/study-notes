# `var`、`let` 和 `const` 的差別

在 JavaScript 中，`var`、`let` 和 `const` 是用於宣告變數的保留字，早期的 JavaScript 只有 `var`，直到 ES2015 (ES6) 才加入 `let` 和 `const`。

<br />

## `var`、`let` 和 `const` 的主要差別

- 作用域

    - `var`：全域作用域或函式作用域 (Function Scope)

    - `let` 和 `const`：區塊作用域 (Block Scope)

- 重複宣告

    - `var` 可以被重複宣告

    - `let` 和 `const` 不可重複宣告

- 重新賦值

    - `let` 和 `const` 可以重新賦值

    - `const` 不能重新賦值，但若是物件或陣列，可以修改內部的屬性或元素

- Hoisting (提升)

    - `var` 宣告的變數會被 Hoisting 並初始化為 `undefined`，在宣告前使用不會報錯

    - `let` 和 `const` 也會被 Hoisting，但存在暫時死區 (TDZ)，在宣告前使用會報錯

    - `let` 和 `const` 以及 `var` 一樣都有被 Hoisting，但是 `let` 和 `const` 卻會進入暫時死區，原因在於 JavaScript 的變數生命週期

        ### 變數生命週期

        1. 建立 (Creation Phase)

            - 執行上下文 (Execution Context) 建立時，JavaScript 會先掃描所有變數宣告

            - 對 `var`、`let` 和 `const` 都會做綁定 (Binding)，綁定的這個行為就算是 Hoisting

        2. 初始化 (Initialization Phase)

            - `var` 在建立階段就會自動初始化成 `undefined`

            - `let` 和 `const` 不會自動初始化，而是進入暫時死區

        3. 賦值 (Assignment Phase)

            - 變數宣告語句執行到時，才會被賦值

            - 對 `const` 來說，必須同時宣告與賦值

<br />

## `var` 是全域或函式作用域，`let` 和 `const` 是區塊作用域

在 ES6 前，JavaScript 沒有區塊作用域 (Block Scope) 的概念，只有全域 (Global Scope) 和函式作用域 (Function Scope)。

`var` 宣告的變數屬於函式作用域，但不會受限於區塊。

ES6 之後，`let` 和 `const` 引入了區塊作用域的概念，變數只會存在於 `{}` 包住的區塊內。

- `var`：函式作用域，不具備區塊作用域。

- `let` 和 `const`：具有區塊作用域，變數只存在於區塊中。

```javascript
/** var 不受區塊限制，區塊外變數存取成功 */

{
  var variable = "Charmy";
}

console.log(variable); // Charmy
```

```javascript
/** let 會受區塊限制，區塊外變數存取失敗 */

{
  let variable = "Charmy";
}

console.log(variable); // ReferenceError: variable is not defined
```

```javascript
/** 雖然 var 不受區塊限制，但會受到函式範圍限制 */

function callName() {
  var variable = "Charmy";
}

console.log(variable); // ReferenceError: variable is not defined
```

```javascript
/** 相同變數名稱不會衝突，因為各自存在於不同函式作用域 */

function callName() {
  var variable = "Charmy";
  console.log(variable);
}

function callNum() {
  var variable = 123;
  console.log(variable);
}

callName(); // Charmy
callNum();  // 123
```

### 限定作用域範圍的好處

- 避免同名變數的衝突。

- 維持最小權限的原則，避免變數資料被不當存取。

<br />

## `var` 與 `let` 在 for 迴圈的差別

用 for 迴圈執行三次，每隔 0.1 秒會印出 i

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(function () {
    console.log(i);
  }, 100);
}
```

執行結果：

```console
3
3
3
```

為什麼結果不是 `0 1 2` 而是 `3 3 3`，這與 `var` 和 `let` 有關。要理解這個問題，要分成兩點討論

- `setTimeout()` 的時間延遲，與 function 中 `console.log(i)` 的執行時間點。

- function 中 `console.log(i)` 的值怎麼來。

首先第一點，當進入 for 迴圈時，宣告變數 `var i = 0` ，並開始條件判斷，當 `i < 3` 時，`i + 1` 執行完後需要等待 0.1 秒，才會執行 `setTimeout()` 內 `function() {}` 裡的 `console.log(i)`。

而 JavaScript 是非同步語言，因此在等待執行 `console.log(i)` 前的這 0.1 秒內，會先執行完已經能執行的 `for` 迴圈。

所以第一點的結論：function 中 `console.log(i)` 的執行時間點會在 `for` 迴圈執行完畢之後。

```javascript
/** 因為非同步與延遲時間，所以會先執行完 for 迴圈後，才執行 function */

for (var i = 0; i < 3; i++) {
  /** for 迴圈直接執行，不會等待 setTimeout 的 0.1 秒 */
  setTimeout(function () {
    console.log(i);
  }, 100);
}
```

執行結果：

```console
3
3
3
```

目前所提的第一點其實與 `var` 和 `let` 的差別沒啥關係，只是說明非同步和時間點的狀況。第二點 `console.log(i)` 的值是怎麼來的就與 `var` 和 `let` 的差別有關了。

`var` 是函式作用域，這段 `for` 迴圈外沒有任何包覆，所以 `var` 所宣告的 `i` 會存在全域 window (瀏覽器) 裡，而且只會被綁定 (Binding) 一次，也可以說是共用一個 instance。

加上 `for` 迴圈會先跑完才跑 `console.log(i)`，所以最後 `console.log(i)` 的值會才會是 `3`。

`let` 則是區塊作用域，每次 `i` 都會被紀錄在創造出來的區域中，更精確來說，是每次迭代都會建立一個新的環境 (Context)，這個環境會紀錄當下的變數 `i` 值，不會覆蓋掉上一個環境裡面的變數值，因此可以產生多個 `i` 值。

<img src="https://github.com/user-attachments/assets/4a0140b9-22d7-4a68-b2dd-66c88a7ace96" width="100%" />

- `var` 的情況只會綁定一次，而且不具區塊作用域，最終會只有一個值存在全域中 (依此例而言)，也可以說只有一個 instance。

- `let` 的情況會發生重複綁定，而且具有區塊作用域，或者說多個紀錄變數的環境，最終會有多的值存在於 `for` 迴圈區塊中，也可以說會有多個 instance。

實作而言，雖然 `var` 的情況下可以用「立即呼叫執行函式 (IIFE)」處理這樣的狀況，但較複雜而且不直覺，改用 `let` 後，就能簡單處理。

```javascript
/** 將 var 改為 let 可以輕易解決問題 */

for (let i = 0; i < 3; i++) {
  setTimeout(function () {
    console.log(i);
  }, 100);
}
```

執行結果：

```console
0
1
2
```

```javascript
/** 不改 var i 的情況下，以 IIFE 相對複雜且不直覺 */

for (var i = 0; i < 3; i++) {
  (function (x) {
    setTimeout(function () {
      console.log(x);
    }, 100 * x);
  })(i);
}
```

執行結果：

```console
0
1
2
```

<br />

## `var` 的 Hoisting 與 `let` 和 `const` 不同

```javascript
console.log(i); // undefined
var i = 5;
```

`undefined` 代表雖然看不見，但在 `console.log(i)` 之前 `i` 就已經被宣告，只是還沒賦值。

由於 `var` 直接把變數 `Hoisting`，所以下面兩段程式碼其實是相同意思

```javascript
console.log(i); // undefined
var i = 5;
```

```javascript
var i;
console.log(i); // undefined
i = 5;
```

function 其實也有 Hoisting 的特性。而 Hoisting 簡單來說就是在執行任何程式碼前，會把變數放進記憶體中，這樣的特點是可以在程式碼宣告變數前就直接使用。

```javascript
/** 因為 Hoisting，所以可以在宣告變數前，就預先使用變數，這樣可以寫完後一起宣告 */

i = 2;
n = 3;
console.log(i + n); // 5
var i;
var n;
```

這樣的情況下，只要有賦值就不會報錯，即使沒有宣告變數也不會報錯。

但是若養成了後宣告的習慣，這樣最後忘了用 `var` 宣告的話變數就會變成全域變數。

```javascript
/** 函式中沒有用 var 宣告，導致污染到全域 */

var x = 1;
function addFunc(y) {
  x = 100;
  x = x + y;
}

addFunc(50);
console.log(x); // 150，預期應該要是 1，但函式中的 x 跑出來了
```

在 `let` 中 Hoisting 比較安全 (`let` 也有 Hoisting，只是情況不同)，所以習慣用 `let` 的開發通常會先宣告變數，而不會習慣先運算變數後宣告的情況，降低出錯的機率。

```javascript
console.log(i); // ReferenceError: Cannot access 'i' before initialization
let i = 5;
```

```javascript
i = 5;
console.log(i); // ReferenceError: Cannot access 'i' before initialization
let i;
```

這樣的使用方式除了降低錯誤外，也相對直覺。

<br />

## `var` 允許重複宣告，`let` 和 `const` 不行

```javascript
var str = "Charmy";
var str = "Charmying";
console.log(str); // Charmying
```

```javascript
let str = "Charmy";
let str = "Charmying";
console.log(str); // SyntaxError: Identifier 'str' has already been declared
```

```javascript
const str = "Charmy";
const str = "Charmying";
console.log(str); // SyntaxError: Identifier 'str' has already been declared
```

<br />

## 總結 `var`、`let` 和 `const` 的差別

- `var` 屬於函式作用域，`let` 和 `const` 屬於區域作用域，後者能避免更多情況下的同名變數與提取變數衝突、區塊內變數污染到全域的情況，而且讓 `for` 迴圈使用更直覺方便。

- `var` 會自動 Hoisting 變數，`let` 和 `const` 較為嚴謹，後者能避免忘記宣告變數或因無宣告讓變數污染到全域的情況。`let` 和 `const` 也是有 Hoisting 的特性。

- `var` 能重複宣告同名變數，`let` 和 `const` 不能重複宣告同名變數，後者能避免開發上的錯誤情況。

簡單來說就是 `let` 和 `const` 將宣告變數變得更嚴謹，藉此增加易讀性、防止出錯。

<br />

## 參考資料

- [JS 宣告變數， var 與 let / const 差異](https://www.programfarmer.com/articles/2020/javascript-var-let-const-for-loop)

- [重新認識 JavaScript: Day 18 Callback Function 與 IIFE](https://ithelp.ithome.com.tw/articles/10192739)

- [鐵人賽：ES6 開始的新生活 let, const](https://www.casper.tw/javascript/2017/12/20/javascript-es6-let-const/)

- [Day 05: ES6篇 - let與const](https://ithelp.ithome.com.tw/articles/10185142)

- [[JavaScript] 你應該使用 let 而不是 var 的 3 個重要理由](https://realdennis.medium.com/%E6%87%B6%E4%BA%BA%E5%8C%85-javascript%E4%B8%AD-%E4%BD%BF%E7%94%A8let%E5%8F%96%E4%BB%A3var%E7%9A%843%E5%80%8B%E7%90%86%E7%94%B1-f11429793fcc)

- [let keyword in the for loop](https://stackoverflow.com/questions/16473350/let-keyword-in-the-for-loop)

- [JavaScript 入門 - 學徒的試煉](https://www.hexschool.com/courses/javascript.html)
