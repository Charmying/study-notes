# 一般函式和箭頭函式的差別

在 JavaScript 中，函式是一個核心的概念，除了能封裝程式碼以及重複使用外，還能透過不同的函式形式達到不同的效果。在 ES6 推出後，JavaScript 引入了箭頭函式 (Arrow Function) 的寫法，'讓開發人員有了更多的選擇來撰寫更具表達力和效率的程式碼。

<br />

##  語法結構的差異

- 一般函式的語法

    `function` 關鍵字是用來定義一個函式的標誌性語法。這種傳統的函式定義方式提供了完整的語法結構，適合用於定義包含多行程式碼的函式。

    ```javascript
    function 函式名稱(參數1, 參數2, ...) {
      // 函式內容
      return 結果;
    }
    ```

    範例

    ```javascript
    function add(a, b) {
      return a + b;
    }
    ```

    在這個範例中，定義了一個名為 `add` 的函式，接受兩個參數後回傳相加的值。這是最傳統的函式寫法。

- 箭頭函式的語法

    箭頭函式讓函式的定義變得更加簡潔，以箭頭 `=>` 作為標誌，不需要使用 `function` 關鍵字。

    ```javascript
    const 函式名稱 = (參數1, 參數2, ...) => {
      // 函式內容
      return 結果;
    }
    ```

    若函式體只有一行，並且這一行是用來回傳結果的，那甚至可以省略 `{}` 和 `return` 關鍵字。

    ```javascript
    const square = x => x * x;
    ```

    這樣簡潔寫法使箭頭函式特別適和在簡單的運算或回呼函式 (Callback Function) 中使用，讓程式碼更加清晰明瞭。

<br />

## `this` 的差異

- 一般函式的 `this` 綁定

    `this` 是一個非常特別的關鍵字，代表函式執行時的上下文。在一般函式中，`this` 是動態綁定的，也就是說，`this` 的值取決於函式是如何被呼叫的。

    ```javascript
    const obj = {
      value: 100,
      getValue: function() {
        return this.value;
      }
    };

    console.log(obj.getValue()); // 100
    ```

    在這個範例中，`getValue` 函式內的 `this` 指向 `obj` 物件，因此 `this.value` 返回的是 `obj` 的 `value` 屬性值。

    若同樣的函式在不同的上下文中呼叫，`this` 可能會指向完全不同的對象。

    ```javascript
    const value = 10; // 全域變數
    const obj = {
      value: 100, // 物件屬性
      getValue: function() {
        return this.value; // this 指向呼叫這個函式的物件
      }
    };

    const getValue = obj.getValue; // 函式分離出來
    console.log(getValue());       // undefined，因為 this 指向全域物件 (window)
    ```

    在這個例子中，`getValue` 函式從 `obj` 中分離出來單獨呼叫時，`this` 指向全域物件 (在瀏覽器中為 window)。因為全域物件 window 中沒有名為 `value` 的屬性，使 `this.value` 返回 `undefined`。即使全域範圍內有一個 `value` 變數，這與 `this` 的綁定無關，因為 `this` 查找的是物件屬性，而不是全域變數。所以 `getValue()` 的輸出是 `undefined` 而不是 `10`。

- 箭頭函式的 `this` 綁定

    與一般函式不同，箭頭函式的 `this` 是詞法綁定 (Lexical Binding) 的。也就是說，箭頭函式的 `this` 值不依賴於函式的呼叫方式，而是取決於在定義時的上下文。

    ```javascript
    const obj = {
      value: 100,
      getValue: () => {
        return this.value;
      }
    };

    console.log(obj.getValue()); // undefined
    ```

    在這個例子中，`getValue` 是一個箭頭函式，因此 `this` 綁定到函式定義時的外部環境，這個環境並不包括 `obj`，通常指向的是全域物件。所以 `this.value` 返回 `undefined`。

    這種特性使箭頭函式在處理回呼函式或嵌套函式時非常有用，因為不需要擔心 `this` 會因為函式的呼叫方式而被意外改變。

<br />

## `arguments` 物件的差異

- 一般函式的 `arguments` 物件

    在一般函式中，`arguments` 是一個隱含的物件，包含了函式被呼叫時傳入的所有參數，無論是否在定義函式時指定了這些參數。

    ```javascript
    function sum() {
      let total = 0;
      for(let i = 0; i < arguments.length; i++) {
        total += arguments[i];
      }
      return total;
    }

    console.log(sum(1, 2, 3)); // 6
    ```

    在這個範例中，利用 `arguments` 物件來取得所有傳入的參數，並計算其總和。

- 箭頭函式的 `arguments` 物件

    箭頭函式中不存在 `arguments` 物件，但是可以使用 ES6 引入的展開運算子 `...` 來取得類似的效果。

    ```javascript
    const sum = (...args) => {
      return args.reduce((total, num) => total + num, 0);
    };

    console.log(sum(1, 2, 3)); // 6
    ```

    在這個範例中，`...args` 將所有傳入的參數組合成一個陣列，然後可以使用陣列的方法來操作這些參數。

<br />

## 作為建構函式的能力

- 一般函式作為建構函式

    一般函式可以作為建構函式使用。也就是說，可以使用 `new` 關鍵字來呼叫這個函式，並創建一個新的物件實例。

    ```javascript
    function Person(name) {
      this.name = name;
    }

    const charmy = new Person("Charmy");
    console.log(charmy.name); // Charmy
    ```

    在這個範例中，`Person` 函式被當作建構函式來使用，並且 `this` 被綁定到新創建的物件 `charmy`，因此 `charmy.name` 可以正確返回。

- 箭頭函式與建構函式

    箭頭函式不能作為建構函式使用。若嘗試使用 `new` 關鍵字來呼叫箭頭函式，JavaScript 會產生報錯。因為箭頭函式沒有自己的 `this`，也沒有 `prototype` 屬性，因此無法用來創建新的物件實例。

    ```javascript
    const Person = (name) => {
      this.name = name;
    };

    const charmy = new Person('Charmy'); // TypeError: Person is not a constructor
    ```

<br />

## 適用場景

- 一般函式：若函式需要動態綁定 `this`、需要使用 `arguments` 物件，或者需要作為建構函式來創建物件實例，那就建議使用一般函式。一般函式在處理複雜功能和大規模程式碼時非常有效。

- 箭頭函式：若需要保持外部 `this` 的綁定，或者想要更簡潔的語法來處理簡單需求，尤其是在回呼函式中，那就建議使用箭頭函式。箭頭函式讓程式碼更易讀、更具表達力，現在使用 JavaScript 開發也被廣泛使用。

<br />

## 總結

總結來說，一般函式和箭頭函式的差別主要體現在以下幾個方面

- 語法結構

    - 一般函式使用 `function` 關鍵字定義，語法相對完整。

    - 箭頭函式使用 `=>` 定義，語法更加簡潔，適合簡單的函式。

- this 綁定

    - 一般函式的 `this` 是動態綁定的，根據函式的呼叫方式決定指向。

    - 箭頭函式沒有自己的 `this`，繼承自定義時的外層作用域，適合在需要保持外部 `this` 的情境下使用。

- `arguments` 物件

    - 一般函式內部自動提供 `arguments` 物件，包含所有傳入的參數。

    - 箭頭函式沒有 `arguments` 物件，需要使用展開運算子 `...` 來取得參數。

- 作為建構函式

    - 一般函式可以作為建構函式，使用 `new` 關鍵字來創建物件實例。

    - 箭頭函式無法作為建構函式使用。

- 應用場景：

    - 一般函式適合在需要動態綁定 `this` 或使用建構函式時使用。

    - 箭頭函式適合用於簡單操作、回呼函式，以及需要保持外部 `this` 綁定的情況。
