# 解構賦值 (Destructuring Assignment)

解構賦值 (Destructuring Assignment) 是 JavaScript 在 ES6 (ECMAScript 2015) 引入的語法，允許從陣列或物件中提取值，並將這些值直接賦給對應的變數。這種語法讓程式碼更簡潔、可讀性更高，並在處理結構化資料時非常實用。

解構賦值可用於

- 陣列

- 物件

- 函式參數

- 結合預設值與重新命名

- rest 運算子

- 巢狀結構

<br />

## 解構賦值的概念

傳統寫法需要透過索引或屬性名稱逐一取值

```javascript
const arr = [1, 2, 3];
const a = arr[0];
const b = arr[1];

const obj = { name: "Charmy", age: 28 };
const name = obj.name;
```

使用解構賦值後可大幅簡化

```javascript
const [a, b] = [1, 2];
const { name, age } = { name: "Charmy", age: 28 };
```

<br />

## 解構賦值的範例

- 陣列解構賦值

    ```javascript
    const numbers = [1, 2, 3];
    const [a, b, c] = numbers;

    console.log(a); // 1
    console.log(b); // 2
    console.log(c); // 3

    ```

- 物件解構賦值

    ```javascript
	const person = { name: "Charmy", age: 28, gender: "Male" };
	const { name, age, gender } = person;

	console.log(name);   // Charmy
	console.log(age);    // 28
	console.log(gender); // Male
    ```

- 解構賦值支持預設值，防止物件或陣列中沒有對應的屬性或元素

	```javascript
	const numbers = [1, 2];
	const [a, b, c = 3] = numbers;
	console.log(a); // 1
	console.log(b); // 2
	console.log(c); // 3 (使用預設值)

	const person = { name: "Charmy", age: 28 };
	const { name, age, gender = "Male" } = person;
	console.log(name);   // Charmy
	console.log(age);    // 28
	console.log(gender); // Male (使用預設值)
	```

- 巢狀解構賦值 (Nested Destructuring)

    解構支援巢狀結構，可直接取得物件中的物件或陣列值

    ```javascript
    const user = {
      name: "Charmy",
      contact: {
        email: "charmy@example.com",
        phone: "0987878787"
      }
    };

    const {
      name,
      contact: { email, phone }
    } = user;

    console.log(name);  // Charmy
    console.log(email); // charmy@example.com
    console.log(phone); // 0987878787
    ```

- 使用 Rest 參數取得剩餘資料

    可以使用 `...rest` 取得其餘元素或屬性

    - 陣列

	    ```javascript
	    const [first, ...others] = [1, 2, 3, 4];
	    console.log(first);  // 1
	    console.log(others); // [2, 3, 4]
	    ```

    - 物件

	    ```javascript
	    const { a, b, ...rest } = { a: 1, b: 2, c: 3, d: 4 };
	    console.log(a);    // 1
	    console.log(b);    // 2
	    console.log(rest); // { c: 3, d: 4 }
	    ```

- 函式參數解構 (常見於框架中)

    可以直接在函式參數中解構，使得參數更清楚、更易讀

	```javascript
	function greet({ name, age }) {
	  console.log(`Hello ${name}, you are ${age} years old.`);
	}

	greet({ name: "Charmy", age: 28 }); // Hello Charmy, you are 28 years old.
	```

- 已宣告變數的解構 (注意加括號)

    對已宣告的變數進行物件解構賦值時，需使用小括號 `()` 包起來，否則 `{}` 會被解析成區塊語法，導致錯誤

	```javascript
	let name, age;
	({ name, age } = { name: "Charmy", age: 28 });

	console.log(name); // Charmy
	console.log(age);  // 28
	```

- 無效的解構情況 (防呆提醒)

    - 陣列解構會依照順序取值，因此順序要對應

    - 物件解構是根據「屬性名稱」而非順序

    - 未定義的屬性不會報錯，但會得到 `undefined`

	```javascript
	const [a, b] = [1]; // b 為 undefined
	const { x } = {};   // x 為 undefined
	```

<br />

## 解構賦值的常見用途

- 從 API 回傳資料快速取值

- React/Vue 的 `props` 解構

- 處理函式的多個參數

- 簡化對巢狀物件的存取

- 撰寫更具可讀性的程式碼

<br />

## 總結

解構賦值是 JavaScript 中一個非常實用的語法，在處理複雜的資料結構時也非常有用，可以簡單從陣列或物件中提取資料，並將其賦給適當的變數。無論是在變數賦值、函數參數或是預設值中，解構賦值都提升程式碼的可讀性和簡潔性。
