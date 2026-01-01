# `setTimeout` 與 `setInterval` 的差別

在 JavaScript 中，`setTimeout` 與 `setInterval` 都是用來延遲或重複執行程式碼的方法，主要差別在於執行次數與頻率。

<br />

## `setTimeout`

- 用途：在指定的延遲時間後執行一次程式碼。

- 語法：`setTimeout(callback, delay)`

    - `callback`：要執行的函式。

    - `delay`：延遲時間 (毫秒)。

執行完一次後就不會再次觸發。

```javascript
console.log("Start");

setTimeout(function() {
  console.log("Delayed message");
}, 2000);

console.log("End");
```

執行結果：

```console
Start
End
Delayed message (經過 2 秒後才輸出這個訊息)
```

<br />

## `setInterval`

- 用途：在指定的時間間隔內重複執行程式碼。

- 語法：`setInterval(callback, interval)`

    - `callback`：要重複執行的函式。

    - `interval`：間隔時間 (毫秒)。

會持續執行，直到使用 `clearInterval` 停止。

```javascript
let count = 1;

const intervalId = setInterval(function() {
  console.log("Interval message:", count);
  count++;
  if (count > 5) {
    clearInterval(intervalId); // 在計數達到 5 時停止重複執行
  }
}, 1000);
```

執行結果：

```console
Interval message: 1 (第 1 秒結束出現)
Interval message: 2 (第 2 秒結束出現)
Interval message: 3 (第 3 秒結束出現)
Interval message: 4 (第 4 秒結束出現)
Interval message: 5 (第 5 秒結束出現，計數達到 5 時停止)
```

<br />

## 總結

- `setTimeout` 用於延遲一段時間後執行程式碼，只執行一次。

- `setInterval` 用於每隔一段時間重複執行程式碼，持續執行直到使用 `clearInterval` 停止。
