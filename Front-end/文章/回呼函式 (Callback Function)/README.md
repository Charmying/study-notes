# 回呼函式 (Callback Function)

Callback Function 就是「把一個函式當作參數傳給另一個函式，讓那個函式在適當時候回呼 (執行)」。

```javascript
function greet(name, cb) {
  const msg = `Hello, ${name}!`;
  cb(msg); // 在這裡呼叫被傳入的 Callback Function
}

greet('Charmy', function(message) {
  console.log(message); // Hello, Charmy!
});
```

<br />

## 同步 vs 非同步 回呼

- 同步回呼 (Synchronous Callback)：在呼叫的函式內立刻被執行、在同一個呼叫堆疊 (Call Stack) 中完成。例如：`Array.prototype.map`, `forEach`, `sort` 的比較函式等。

    ```javascript
    [1,2,3].forEach(x => console.log(x)); // 回呼立即同步執行
    ```

- 非同步回呼 (Asynchronous Callback)：在未來某個時間點或事件發生時執行，通常會經由事件迴圈 (Event Loop) 排程。例如：`setTimeout`、網路請求、DOM 事件監聽器、Node.js 的 I/O 回呼。

	```javascript
	setTimeout(() => {
	  console.log('兩秒後執行');
	}, 2000);
	```

<br />

## 常見情況與範例

- 高階函式 (接受回呼)

	```javascript
	function repeat(n, action) {
	  for (let i = 0; i < n; i++) action(i);
	}
	repeat(3, i => console.log('迴圈', i));
	```

- 陣列操作 (同步回呼)

	```javascript
	const squares = [1,2,3].map(x => x * x); // map 的回呼是同步
	```

- 事件處理 (非同步)

	```javascript
	button.addEventListener('click', event => {
	  console.log('按鈕被按下', event);
	});
	```

- Node.js 的 Error-first Callback (慣例)

	```javascript
	const fs = require('fs');
	fs.readFile('file.txt', 'utf8', (err, data) => {
	  if (err) {
	    console.error('讀檔錯誤', err);
	    return;
	  }
	  console.log('檔案內容：', data);
	});
	```

    - Node 慣例是第一個參數放 `err`，讓呼叫者先處理錯誤。

<br />

## 常見問題與陷阱

- Callback Hell (回呼地獄/嵌套金字塔)

    當多個非同步任務必須依序執行且每個裡面又有回呼，會造成可讀性差的情況

	```javascript
	doA(arg, aResult => {
	  doB(aResult, bResult => {
	    doC(bResult, cResult => {
	      // 很難維護
	    });
	  });
	});
	```

- `this` 失綁 (Context 丟失)

    把物件方法當回呼傳入時，`this` 可能會丟失

	```javascript
	const obj = {
	  x: 10,
	  print() { console.log(this.x); }
	};
	setTimeout(obj.print, 1000); // undefined 或錯誤，this 不再是 obj
	// 解法：綁定
	setTimeout(obj.print.bind(obj), 1000);
	```

- 同步/非同步行為不一致

    API 有時會在某些情境同步呼叫 Callback，有時非同步呼叫，使用者很難預期。設計 API 時應標註並盡量一致。

- 錯誤處理

    非同步回呼若沒妥善處理錯誤 (例如：忘記檢查 `err`)，會導致 Silent Failure。遵循 Error-first Pattern 有助於一致處理。

<br />

## 改善方式：`Promise` 與 `async`/`await` (現代替代方法)

Callback Hell 的常見解法是改用 `Promise` 或 `async`/`await`。把 Callback 包成 `Promise` 可以讓程式改寫成線性、較易讀的風格。

範例：把一個 Callback-style 的函式包成 `Promise`

```javascript
// 假設 readFile 是 Error-first Callback
function readFilePromise(path) {
  return new Promise((resolve, reject) => {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

// 使用
readFilePromise('file.txt')
  .then(data => console.log(data))
  .catch(err => console.error(err));

// 或 async/await
async function main() {
  try {
    const content = await readFilePromise('file.txt');
    console.log(content);
  } catch (e) {
    console.error(e);
  }
}
```

<br />

## 總結

- Callback 是 JavaScript 常見的控制流程工具，將函式當參數傳遞給另一個函式，在稍後再被呼叫。

- Callback 是直接傳函式並由呼叫方執行；`Promise` 提供更可組合、可鏈結的錯誤處理與狀態 (Fulfilled/Rejected)，通常可解決巢狀問題。

- 遇到多層依賴性非同步任務導致巢狀回呼等複雜非同步流程時，可以拆成命名函式，使用 Promise 或 async/await 改寫。

- 寫回呼要注意錯誤處理、`this` 綁定與可讀性
