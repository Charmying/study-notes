# `==`、`===`、`Object.is` 的差異與用法

在寫程式的過程中，很常遇到需要判別比較的情況，這時候可以先了解 JavaScript 的比較運算子，這也是在提到 `==`、`===`、`Object.is` 的差異與用法之前需要知道的。

<br />

## 什麼是比較運算子

在 JavaScript 中，比較運算子是用來比較兩個值是否相等，或者比較兩個值的大小關係。常見的比較運算子包括

- `==` (鬆散等於)

- `===` (嚴格等於)

- `!=` (不等於)

- `!==` (嚴格不等於)

- `>` (大於)

- `<` (小於)

- `>=` (大於等於)

- `<=` (小於等於)

<br />

## `==`：鬆散等於 (Loose Equality)

`==` 運算子是「鬆散等於」的意思，會先進行型別轉換，然後再比較值是否相等。這種比較方式被稱為「鬆散比較」或「抽象比較」。

### 特點

- 若兩個值的型別不同，JavaScript 會嘗試轉換成相同的型別，然後再比較。

- 這種做法是為了方便，但也容易造成混淆，因為型別轉換的規則複雜，寫程式時若不小心，可能會得到意想不到的結果。

### 範例

```javascript
console.log(5 == "5");          // true (因為 "5" 被轉換成 5)
console.log(0 == false);        // true (因為 false 被轉換成 0)
console.log(null == undefined); // true (因為 null 和 undefined 在 JavaScript 中被視為相等)
console.log("" == false);       // true (因為空字串被轉換成 0，而 0 == false)
```

### 注意事項

- 使用 `==` 時，需要特別注意型別轉換的規則。

    例如：`"" == false` 是 `true`，因為空字串被轉換成 0，而 `0 == false` 也是 `true`。

- 雖然 `==` 很方便，但因為其不確定性，通常不建議在重要程式中使用。根據 MDN Web Docs，大多數情況下應避免使用鬆散比較。

<br />

## `===`：嚴格等於 (Strict Equality)

`===` 運算子是「嚴格等於」，不會進行型別轉換，直接比較兩個值的型別和值是否完全相同。

### 特點

- 若兩個值的型別不同，`===` 會直接返回 `false`，不會進行任何型別轉換。

- 這種方式更安全，因此在現代 JavaScript 中，建議盡量使用 `===`。

### 範例

```javascript
console.log(5 === "5");             // false (因為型別不同 -> number vs string)
console.log(0 === false);           // false (因為型別不同 -> number vs boolean)
console.log(null === undefined);    // false (因為型別不同)
console.log(123 === Number("123")); // true (因為型別和值都相同)
```

### 注意事項

- `===` 是最常用的相等比較運算子，因為避免了型別轉換帶來的問題。

- 特殊情況。

    `+0` 和 `-0` 的比較：`+0 === -0` 是 `true`，這是語言設計者刻意設計的，因為在大多數情境下，`+0` 和 `-0` 是等價的。

    `NaN` 和 `NaN` 的比較：`NaN === NaN` 是 `false`，因為 `NaN` 在 JavaScript 中是一個「非數值」，與任何值都不相等，包括 `NaN` 本身。

- 根據 MDN Web Docs，嚴格比較的結果更可預測，且因無型別轉換，執行效率更高。

<br />

## `Object.is`：同值相等 (Same-value Equality)

`Object.is` 是 ES6 中新增的靜態方法，用來比較兩個值是否為「同值相等」。`Object.is` 比較方式與 `===` 相似，但因算法不同對特殊情況有不同的結果。

### 特點

- `Object.is` 不進行型別轉換，直接比較值。

- 與 `===` 的主要差異

    - `Object.is(+0, -0)` 是 `false`，而 `0 === -0` 是 `true`。

    - `Object.is(NaN, NaN)` 是 `true`，而 `NaN === NaN` 是 `false`。

    這些差異是因為 `Object.is` 使用「同值相等」算法，特別處理 `NaN` 和 `0` 的區別。

### 範例

```javascript
console.log(Object.is(5, "5"));   // false (因為型別不同)
console.log(Object.is(0, -0));    // false (因為 Object.is 區分 +0 和 -0)
console.log(Object.is(NaN, NaN)); // true (因為 Object.is 認為 NaN 和 NaN 相等)
console.log(Object.is(25, 25));   // true (因為值和型別相同)
```

### 注意事項

- `Object.is` 通常用在需要區分 `+0` 和 `-0`，或者需要比較 `NaN` 是否相等的特殊情況。在一般情況下，`===` 已經足以應付，大多數開發人員不需要頻繁使用 `Object.is`。

<br />

## `==`、`===`、`Object.is` 的差異

| Value 1 | Value 2 | `==` | `===` | `Object.is` |
| - | - | - | - | - |
| `5` | `"5"` | `true` | `false` | `false` |
| `0` | `false` | `true` | `false` | `false` |
| `null` | `undefined` | `true` | `false` | `false` |
| `+0` | `-0` | `true` | `true` | `false` |
| `NaN` | `NaN` | `false` | `false` | `true` |
| `true` | `1` | `true` | `false` | `false` |
| `"foo"` | `"foo"` | `true` | `true` | `true` |
| `{ foo: "bar" }` | `{ foo: "bar" }` | `false` | `false` | `false` |

- `==` 會進行型別轉換，值相等即可為 `true`。

- `===` 不會進行型別轉換，值與型別皆相同才為 `true`。

- `Object.is` 與 `===` 幾乎相同，但可以區分 `+0` 和 `-0` 以及比較 `NaN` 是否相等。

<br />

## 其他比較運算子

除了等於運算子之外，JavaScript 還有其他比較運算子，這些運算子會先進行型別轉換，然後再比較值。

### 範例

```javascript
console.log(5 > "3");           // true (因為 "3" 被轉換成 3)
console.log("10" < 5);          // false (因為 "10" 被轉換成 10)
console.log("hello" > "world"); // false (因為 string 比較依據 Unicode 順序)
console.log("hello" > 1);       // false (因為 "hello" 無法轉換成 number)
```

### 注意事項

- 若比較的值無法轉換成 number，則會返回 `false`。

- string 比較是依據字典順序 (Unicode 編碼)，而非數值大小。例如：`"apple" < "banana"` 是 `true`，因為 `a` 的 Unicode 值小於 `b`。

<br />

## 深入了解比較算法

- `==` (鬆散比較)：定義於 ECMAScript 5.1 規範的 11.9.3 節，會根據值的型別執行一系列轉換規則，例如：將 string 轉為 number，或將 boolean 轉為 `0` 或 `1`。

- `===` (嚴格比較)：定義於 ECMAScript 5.1 規範的 11.9.6 節，會直接比較型別和值，無需轉換。

- `Object.is` (同值相等)：定義於 ECMAScript 2026 規範，使用「同值相等」算法，特別處理 `NaN` 和 `0` 的區別。

<br />

## 參考資料

- [MDN Web Docs: 運算式與運算子](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Guide/Expressions_and_operators)

- [MDN Web Docs: Object.is()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is)

- [MDN Web Docs: 相等比較](https://developer.mozilla.org/zh-TW/docs/MDN/Community/Translated_content#%E6%B4%BB%E8%BA%8D%E7%9A%84%E8%AA%9E%E8%A8%80)
