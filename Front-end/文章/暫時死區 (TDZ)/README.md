# 暫時死區 (TDZ)

暫時死區 (Temporary Dead Zone，簡稱：TDZ) 在 JavaScript 中是指在使用 `let` 和 `const` 宣告變數時，從變數宣告開始到變數初始化之間的範圍。這段範圍內，變數不能被存取，即使這個變數在程式碼中已經被宣告。

<br />

## 為什麼會有暫時死區

暫時死區的設計是為了解決變數提升 (Hoisting) 所帶來的混淆問題。在 JavaScript 中，使用 `var` 宣告的變數會被 Hoisting 到其所在作用域的頂部，但不會同時初始化。因此，在變數初始化前存取變數時，會得到 `undefined`。但是這樣可能會導致程式碼出現潛在的錯誤或意外行為。

`let` 和 `const` 的引入是為了提供一個更具預測性和安全性的變數宣告方式，防止開發人員意外在變數初始化之前存取。

<br />

## 暫時死區的定義

在一段程式碼中使用 `let` 或 `const` 宣告變數時，這些變數會被 Hoisting 到作用域的頂部 (與 `var` 類似)，但是這些變數並不會立即初始化。從變數 Hoisting 開始到變數初始化這段時間，就是所謂的暫時死區。在這個區域中，若嘗試存取這些變數，JavaScript 會拋出一個 `ReferenceError`。

<br />

## 暫時死區的定義

```javascript
console.log(a); // ReferenceError: Cannot access 'a' before initialization
let a = 3;
```

```javascript
function testTDZ() {
  console.log(b); // ReferenceError: Cannot access 'b' before initialization
  let b = 5;
}

testTDZ();
```

以上範例中，對 `a` 和 `b` 的存取都會報錯 `ReferenceError`，因為用 `let` 宣告的變數在初始化之前就已經要使用了。

<br />

## 總結

- `let` 和 `const` 的 Hoisting：雖然 `let` 和 `const` 宣告的變數也會被 Hoisting 到作用域的頂部，但在初始化之前無法被存取，這就是暫時死區存在的原因。

- `var` 與暫時死區：`var` 宣告的變數不會有暫時死區，因為在 Hoisting 時會初始化為 `undefined`，因此在初始化之前可以被存取，但通常這樣做會導致非預期的行為。

- 區塊作用域：暫時死區只在用 `let` 和 `const` 宣告的變數所屬區塊作用域內有效。

暫時死區的概念強調在使用 `let` 和 `const` 時，開發人員應該在變數宣告之前不要進行存取。這樣可以減少潛在的錯誤和程式行為不一致的風險。
