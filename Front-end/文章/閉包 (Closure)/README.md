# 閉包 (Closure)

在 JavaScript 中，閉包 (Closure) 是一種非常重要的概念，指的是當一個函式被創建時，會記住其所在的作用域 (Scope)，即使該作用域已經結束執行，函式依然能夠存取該作用域中的變數。

<br />

## 閉包的基本概念

### 定義：

閉包是一種函式，該函式能夠記住並存取在定義時的作用域 (即使這個函式在定義作用域之外執行)。

### 閉包通常在以下情況下產生：

- 一個函式在另一個函式內部被定義。

- 內部函式存取外部函式中的變數。

- 外部函式執行完畢後，內部函式仍然存在並被使用。

<br />

## 為什麼會有閉包

閉包的存在是因為 JavaScript 使用了詞法作用域 (Lexical Scope)，也叫做靜態作用域。也就是說，函式的作用域在定義時就確定了，而不是在執行時。

<br />

## 閉包的範例與解釋

- 範例：基本閉包

	```javascript
	function outerFunction() {
	  let outerVariable = "外部變數";

	  function innerFunction() {
	    console.log(outerVariable); // 可以存取 outerFunction 的變數
	  }

	  return innerFunction;
	}

	const closure = outerFunction(); // 呼叫 outerFunction，返回 innerFunction
	closure();                       // 外部變數
	```

    - 當 `outerFunction` 執行時，創建了一個變數 `outerVariable` 和一個內部函式 `innerFunction`。

    - `innerFunction` 被作為閉包返回，並記住 `outerVariable`。

    - 即使 `outerFunction` 的執行結束，`innerFunction` 依然可以存取 `outerVariable`。

- 範例：閉包的應用 - 建立私有變數

	```javascript
	function createCounter() {
	  let count = 0;

	  return {
	    increment: function () {
	      count++;
	      return count;
	    },

	    decrement: function () {
	      count--;
	      return count;
	    },

	    getCount: function () {
	      return count;
	    }
	  };
	}

	const counter = createCounter();
	console.log(counter.increment()); // 1
	console.log(counter.increment()); // 2
	console.log(counter.decrement()); // 1
	console.log(counter.getCount());  // 1
	```

    - `createCounter` 是一個函式，內部定義了一個私有變數 `count` 和多個操作方法。

    - `createCounter` 返回的物件中的方法組成了閉包，這些方法可以存取 `count`。

    - 外部無法直接修改 `count`，只能透過 `increment`、`decrement` 和 `getCount` 操作。

<br />

## 閉包的優缺點

### 優點

- 數據封裝： 使用閉包創建私有變數，避免全域變數污染。

- 模組化： 提供了一種模組化設計模式，讓程式碼更容易維護。

- 狀態保持： 閉包可以記住外部函式中的變數狀態，進行靈活運用。

### 缺點

- 記憶體占用：閉包可能導致不必要的變數長期駐留於記憶體，容易引發記憶體洩漏 (Memory Leak) 問題。

- 調試困難： 由於閉包存取外部作用域的變數，可能會增加程式的調試複雜性。

<br />

## 閉包常見的應用場景

- 事件處理：

	```javascript
	function setupEventListener(element, message) {
	  element.addEventListener('click', function () {
	    console.log(message); // 閉包記住了 message
	  });
	}

	const button = document.querySelector('#myButton');
	setupEventListener(button, "按鈕被點擊了！");
	```

- 延遲執行 (setTimeout)：

	```javascript
	function delayLog(message, delay) {
	  setTimeout(function () {
	    console.log(message); // 閉包記住了 message
	  }, delay);
	}

	delayLog("這是延遲訊息", 1000);
	```

- 模擬私有變數： 使用閉包模擬類似其語言中的私有變數，增加程式的安全性與可控性。

<br />

## 總結

閉包是 JavaScript 中強大的特性，讓函式能夠記住和操作其定義時的作用域，並在多種情境中提供極大的彈性與功能性。然而，在使用閉包時需要注意記憶體管理與效能問題，以免造成不必要的資源消耗。
