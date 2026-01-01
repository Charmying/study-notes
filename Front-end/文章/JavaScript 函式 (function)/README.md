# JavaScript 函式 (function)

在 JavaScript 中，函式是一個基本的構建塊，用來封裝可重複使用的程式碼。函式允許將程式碼組織成易於管理和重用的模組。

<br />

## 函式定義方法

- 函式聲明 (Function Declaration)

    使用 `function` 關鍵字來定義函式。函式聲明會被提升 (Hoisting)，所以可以在定義之前呼叫。

    ```javascript
    function sayHello(name) {
      return `Hello, ${name}!`;
    }

    console.log(sayHello('Charmy')); // Hello, Charmy!
    ```

- 函式表達式 (Function Expression)

    將函式賦值給變數。與函式聲明不同，函式表達式不會被提升 (Hoisting)，必須在定義之後才能呼叫。

    ```javascript
    const sayHello = function(name) {
      return `Hello, ${name}!`;
    };

    console.log(sayHello('Charmy')); // Hello, Charmy!
    ```

- 箭頭函式 (Arrow Function)

    更簡潔的函式寫法，並且不會綁定自己的 `this`，適合回呼函式 (Callback Function)。

    ```javascript
    const sayHello = (name) => `Hello, ${name}!`;

    console.log(sayHello('Charmy')); // Hello, Charmy!
    ```

    當函式只有一行時，可以省略大括號 `{}` 和 `return`。

    ```javascript
    const square = x => x * x;

    console.log(square(5)); // 25
    ```

- 立即調用函式表達式 (IIFE)

    定義後立即執行，用於建立局部作用域，避免變數污染。

    ```javascript
    (function() {
      let message = "This is an IIFE.";
      console.log(message); // This is an IIFE.
    })();
    ```

- 匿名函式 (Anonymous Function)

    沒有名稱的函式，常用於回呼 (Callback)。

	```javascript
	setTimeout(function() {
	  console.log("This runs later.");
	}, 1000);
	```

<br />

## 函式回傳值 (Return Value)

- 使用 `return` 返回值。

- `return` 會結束函式的執行。

- 沒有返回值的函式會返回 `undefined`。

```javascript
function multiply(a, b) {
  return a * b;
}

console.log(multiply(2, 3)); // 6

function noReturn() {}
console.log(noReturn()); // undefined
```

<br />

## 函式參數

- 基本參數

    函式可以接受任意數量的參數，並可以在函式內部使用這些參數進行操作。

	```javascript
	function add(a, b) {
	  return a + b;
	}

	console.log(add(3, 5)); // 8
	```

- 預設參數

    JavaScript 函式允許設置預設參數值。若函式呼叫時未提供這些參數，則會使用預設值。

    ```javascript
    function sayHello(name = 'Charmy') {
      return `Hello, ${name}!`;
    }

    console.log(sayHello());            // Hello, Charmy!
    console.log(sayHello('Charmying')); // Hello, Charmying!
    ```

- 剩餘參數 (Rest Parameters)

    剩餘參數使用 `...` 語法，可以接收任意數量的參數，並全部收集到一個陣列中。

    ```javascript
    function sum(...numbers) {
      return numbers.reduce((total, num) => total + num, 0);
    }

    console.log(sum(1, 2, 3, 4)); // 10
    ```

    在這個例子中，`...numbers` 會將所有傳遞給函式的參數收集到 `numbers` 陣列中。

- 函式參數解構 (Destructuring Parameters)

    JavaScript 允許在函式參數中使用解構賦值來直接提取物件或陣列中的值。

    ```javascript
    /** 物件解構 */
    function printPerson({ name, age }) {
      console.log(`Name: ${name}, Age: ${age}`);
    }

    printPerson({ name: 'Charmy', age: 27 }); // Name: Charmy, Age: 27

    /** 陣列解構 */
    function printCoordinates([x, y]) {
      console.log(`X: ${x}, Y: ${y}`);
    }

    printCoordinates([10, 20]);  // X: 10, Y: 20
    ```

    這樣可以在函式內部直接使用解構後的變數。

<br />

## 函式提升 (Hoisting)

- 函式聲明：會被提升，可以在定義前呼叫。

- 函式表達式和箭頭函式：不會被提升。

```javascript
sayHello(); // 可以執行

function sayHello() {
  console.log("Hello!");
}

greet(); // ❌ TypeError: greet is not a function

const greet = function() {
  console.log("Hi!");
};
```

<br />

## 函式變數與作用域

- 變數作用域 (Variable Scope)

    - 全域作用域 (Global Scope)：在函式外部定義的變數，所有函式都可以使用。

        ```javascript
        let globalVar = 'I am global';

        function showGlobal() {
          console.log(globalVar); // 可以存取全域變數
        }

        showGlobal(); // I am global
        ```

    - 局部作用域 (Local Scope)：在函式內部定義的變數，只能在函式內部使用。

        ```javascript
        function showLocal() {
          let localVar = 'I am local';
          console.log(localVar); // 可以存取局部變數
        }

        showLocal();           // I am local
        console.log(localVar); // ReferenceError: localVar is not defined
        ```

- 函式作用域 (Function Scope)

    每個函式都有自己的作用域。函式內部定義的變數在函式外部不可存取，但外部變數在函式內部是可以存取的。

    ```javascript
    function outerFunction() {
      let outerVariable = 'I am from outer function';

      function innerFunction() {
        console.log(outerVariable); // 可以存取外部變數
      }

      innerFunction();
    }

    outerFunction(); // I am from outer function
    ```

<br />

## 函式中的 `this`

- 一般函式呼叫：`this` 指向全域物件 (`window`/`globalThis`)

	```javascript
	function showThis() {
	  console.log(this);
	}

	showThis(); // window (瀏覽器)
	```

- 物件方法：`this` 指向呼叫的物件

	```javascript
	const person = {
	  name: 'Charmy',
	  greet: function() {
	    console.log(this.name);
	  }
	};

	person.greet(); // Charmy
    ```

- 箭頭函式：繼承外部作用域的 `this`

	```javascript
	const person = {
	  name: 'Charmy',
	  greet: function() {
	    const innerGreet = () => {
	      console.log(this.name);
	    };
	    innerGreet();
	  }
	};

	person.greet(); // Charmy
	```

<br />

## 高階函式 (Higher-Order Functions)

函式可以作為參數或返回值。

```javascript
function createMultiplier(factor) {
  return function(x) {
    return x * factor;
  };
}

const double = createMultiplier(2);
console.log(double(5)); // 10
```

<br />

## 函式屬性與方法

函式本質上是物件，具有屬性。

```javascript
function add(a, b) {}

console.log(add.name);   // "add"
console.log(add.length); // 2
```

<br />

## 閉包 (Closure)

閉包是指「函式可以存取其外部作用域的變數」，即使外部函式已經執行完畢。閉包常用於資料封裝、模組化程式設計。

```javascript
function makeCounter() {
  let count = 0;
  return function() {
    count++;
    return count;
  };
}

const counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```
