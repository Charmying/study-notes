# Javascript 的作用域 (Scope) 與作用域鏈 (Scope Chain)

在 JavaScript 中，作用域 (Scope) 和作用域鏈 (Scope Chain) 是理解 JavaScript 如何管理變數存取的關鍵，對於寫出穩定且高效的程式碼至關重要。

<br />

## 作用域 (Scope)

作用域是指變數或函式在程式碼中的有效範圍，也就是說，在程式的哪些部分可以存取或使用這些變數或函式。作用域可以分為以下幾種類型。

- 全域作用域 (Global Scope)

    當一個變數或函式在任何函式、區塊之外宣告時，就會屬於全域作用域。全域作用域中的變數或函式可以在整個程式中被存取，這些變數通常是全域物件 (例如：window 或 global) 的屬性。

    ```javascript
    var globalVar = "全域變數";

    function showGlobalVar() {
      console.log(globalVar); // 可以在函式內存取全域變數
    }

    showGlobalVar(); // 全域變數
    ```

    在這個範例中，`globalVar` 是一個全域變數，可以在 `showGlobalVar` 函式中被存取和使用，這是因為 `showGlobalVar` 在全域作用域中運行。

- 區域作用域 (Local Scope)

    區域作用域是指變數或函式只在某個特定的函式或區塊內部有效。當在函式內部宣告一個變數時，就屬於該函式的區域作用域。也就是說，該變數只能在函式內部被存取，無法在函式外部使用。

    ```javascript
    function showLocalVar() {
      var localVar = "區域變數";
      console.log(localVar); // 可以在函式內存取區域變數
    }

    showLocalVar();        // 區域變數
    console.log(localVar); // 無法在函式外部存取，會報錯。ReferenceError: localVar is not defined
    ```

    在這個範例中，`localVar` 是一個區域變數，只在 `showLocalVar` 函式內部有效。若嘗試在函式外部存取 `localVar` 就會報錯，因為 `localVar` 不屬於全域作用域。

- 區塊作用域 (Block Scope)

    隨著 ES6 的引入，JavaScript 新增了 `let` 和 `const` 來關鍵字，`let` 和 `const` 允許開發人員在區塊級別 (Block-level) 宣告變數。區塊作用域是指變數只在特定區塊 (由 `{}` 包圍的程式碼塊) 內部有效。

    ```javascript
    if (true) {
      let blockVar = "區塊變數";
      console.log(blockVar); // 可以在區塊內存取區塊變數，這邊直接輸出：區塊變數
    }

    console.log(blockVar); // 無法在區塊外部存取，會報錯。ReferenceError: blockVar is not defined
    ```

    在這個範例中，`blockVar` 是一個區塊變數，只有在 `if` 區塊內部有效。若在區塊外部存取 `blockVar` 就會報錯，因為這個變數在區塊外部無效。

- 函式作用域 (Function Scope)

    函式作用域是一種特殊的區域作用域 (Local Scope)，特點是變數或函式在宣告時，只在當前函式內有效，無法在函式外部存取。也就是說，當一個變數或函式在一個函式內部宣告時，這個變數或函式的作用域僅限於該函式內部。

    在 ES6 之前，JavaScript 只支持函式作用域，而不支持區塊作用域。也就是說，在函式內部用 `var` 宣告的變數，不管是在任何區塊 (例如：`if` 或 `for` 迴圈) 內，該變數在整個函式內部都是有效的。

    - 函式作用域中的 `var` 行為

    	```javascript
    	function testVar() {
    	  if (true) {
    	    var x = 10;
    	  }
    	  console.log(x); // 仍然可以存取到 x
    	}

    	testVar(); // 10
    	```

        在這個範例中，即使 `x` 是在 `if` 區塊內宣告，因為使用的是 `var`，所以 `x` 的作用域擴展到了整個 `testVar` 函式內部，這就是函式作用域的特性。

    - 函式作用域中的 `let` 行為

    	```javascript
    	function testLet() {
    	  if (true) {
    	    let y = 20;
    	  }
    	  console.log(y);
    	}

    	testLet(); // 會報錯，因為 y 不在作用域內。ReferenceError: y is not defined
    	```

        在這個範例中，`y` 是用 `let` 宣告的，使得作用域僅限於 `if` 區塊內部，因此在區塊外部存取 `y` 會出現報錯。

<br />

## 作用域鏈 (Scope Chain)

在 JavaScript 中，當執行一個函式時，會建立一個作用域鏈，這個鏈是由多個作用域組成的鏈條，通常包括

- 函式的區域作用域 (Local Scope)：函式內部的變數和函式宣告。

- 外層函式的作用域 (Outer Scope)：若函式被嵌套，則會包含外層函式的作用域。

- 全域作用域 (Global Scope)：若在所有外層作用域中都找不到變數，最終會查找全域作用域。

作用域鏈的概念與函式的嵌套有很大關係。當 JavaScript 引擎在查找變數的時候，會從函式的區域作用域開始，逐層向外查找，直到找到變數或達到全域作用域。

```javascript
var globalVar = "全域變數";

function outerFunction() {
  var outerVar = "外層變數";

  function innerFunction() {
    var innerVar = "內層變數";
    console.log(innerVar);  // 可以存取內層變數
    console.log(outerVar);  // 可以存取外層變數 (外層作用域)
    console.log(globalVar); // 可以存取全域變數
  }

  innerFunction();
}

outerFunction();
```

在這個範例中，`innerFunction` 的作用域鏈如下

- `innerFunction` 的區域作用域：包含 `innerVar` 變數。

- `outerFunction` 的作用域：包含 `outerVar` 變數。

- 全域作用域：包含 `globalVar` 變數。

當 `innerFunction` 嘗試存取一個變數時，JavaScript 引擎首先會在 `innerFunction` 的區域作用域內查找變數。若沒有找到，會繼續向外查找 `outerFunction` 的作用域。若還是找不到，則最終會查找全域作用域。這個逐層查找的過程就是作用域鏈。

<br />

## 提升 (Hoisting)

在理解作用域和作用域鏈時，還必須提到 JavaScript 中的一個重要概念：提升 (Hoisting)。在 JavaScript 中，變數和函式的宣告會被 Hoisting 到其所在作用域的頂端。也就是說，即使變數或函式在其所在作用域的後面才出現，JavaScript 引擎仍然會將這些被宣告變數或函式 Hoisting 到作用域的最前面，但 Hoisting 的僅是宣告，賦值不會被 Hoisting。

```javascript
console.log(hoistedVar); // undefined
var hoistedVar = "已提升的變數";
```

在這個範例中，`hoistedVar` 被提升到全域作用域的頂端，但其值 `已提升的變數` 並未提升，因此第一次 `console.log` 會輸出 `undefined`，而非 `已提升的變數`。

<br />

## 總結

JavaScript 的作用域和作用域鏈是變數管理的基礎，了解這些概念可以幫助避免變數命名衝突、瞭解變數的生命週期，並撰寫出更具結構性且不容易出錯的程式碼。
