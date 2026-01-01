# 箭頭函式 (Arrow Function)

JavaScript 的箭頭函式 (Arrow Function) 是 ES6 (ECMAScript 2015) 引入的一個功能，目的在簡化函式的語法結構，使程式碼更精簡、可讀性更高。箭頭函式特別適用於需要撰寫短小函式的情況，例如：回呼函式 (Callback Function) 或是一些單純進行運算的函式。

<br />

## 箭頭函式的基本語法

一般情況下是使用 `function` 關鍵字來定義函式

```javascript
function add(a, b) {
  return a + b;
}
```

或

```javascript
const add = function(x, y) {
  return x + y;
};
```

使用箭頭函式可以將上面的程式碼簡化

```javascript
const add = (x, y) => {
  return x + y;
};
```

在這個範例中，`add` 是一個接收兩個參數 `x` 和 `y` 的函式，並回傳兩者的和。這種語法不僅更加簡潔，而且在某些情況下更易於理解。

<br />

## 箭頭函式的語法簡化

除了基本語法外，箭頭函式還有更多語法簡化的方法，可以再使程式碼更加精簡。

- 若函式只有一個參數，可以省略參數的括號 `()`

    ```javascript
    const square = x => {
      return x * x;
    };
    ```

    在這個範例中，`square` 函式接受一個參數 `x`，並回傳 `x` 的平方。

- 省略大括號 `{}` 與 `return`

    若函式內部的程式碼區塊只有一個表達式，並且此表達式需要回傳值，則可以省略大括號 `{}` 和 `return` 關鍵字。

    ```javascript
    const square = x => x * x;
    ```

    在這個範例中，`square` 函式與之前範例的功能完全相同，但更簡潔。省略 `return` 關鍵字後，箭頭函式會自動返回此表達式的計算結果。

- 無參數和多參數的箭頭函式

    在無參數的情況下，必須使用空括號來表示沒有參數。

    ```javascript
    const greet = () => 'Hello!';
    ```

    當有多個參數時，就需要用括號包起來

    ```javascript
    const multiply = (x, y, z) => x * y * z;
    ```

    這樣的語法使箭頭函式在各種情況下都能保持簡潔。

<br />

## 箭頭函式與 `this` 綁定的特性

箭頭函式相較於傳統函式的一個特點是沒有自己的 `this` 綁定。也就是說，箭頭函式中的 `this` 會繼承自其定義位置的外層作用域，而不是函式調用時的上下文。

```javascript
function Person() {
  this.age = 0;

  setInterval(() => {
    this.age++; // this 繼承自 Person 函式
    console.log(this.age);
  }, 1000);
}

const p = new Person();
```

在這個範例中，`setInterval` 內的箭頭函式沒有自己的 `this`，所以會繼承 `Person` 物件的 `this`，從而能正常存取並修改 `age` 屬性。

使用傳統函式的話 `this` 會在 `setInterval` 的執行上下文中指向 `window` (或 `undefined`)，導致無法正確存取 `Person` 物件的 `this`。這時可能需要使用 `bind`、`call` 或 `apply` 方法來綁定 `this`。

```javascript
function Person() {
  this.age = 0;

  setInterval(function() {
    this.age++;
    console.log(this.age);
  }.bind(this), 1000);
}

const p = new Person();
```

這就是為什麼在某些情境下，箭頭函式比傳統函式更加方便，特別是在需要正確綁定 `this` 的情況。

<br />

## 箭頭函式的限制與不適用情況

- 不能作為建構子函式

    箭頭函式不能作為建構子函式使用，因為沒有自己的 `this`。若嘗試使用箭頭函式來創建物件實例會產生報錯。

    ```javascript
    const Person = (name) => {
      this.name = name;
    };

    const p = new Person('Charmy'); // TypeError: Person is not a constructor
    ```

- 不支援 `arguments` 物件

    箭頭函式沒有 `arguments` 物件，也就是說，無法直接使用 `arguments` 來存取傳遞給函式的參數。若需要存取所有傳入參數，可以使用展開運算符 `...` 來解決這個問題。

    ```javascript
    const sum = (...args) => args.reduce((acc, val) => acc + val, 0);
    ```

- 不適用動態 `this` 需求的情況

    在一些需要動態綁定 `this` 的情況下，例如：事件處理器或某些特定的回呼函式，使用傳統函式可能更適合。

<br />

## 總結

箭頭函式的引入為 JavaScript 開發人員提供一種簡潔的函式定義方式，特別是在需要撰寫短小且簡單的函式時非常有用。箭頭函式的語法簡化了程式碼結構，同時避免了常見的 `this` 綁定問題。但是在涉及建構子函式或需要 `arguments` 物件的情況中下需要特別注意。
