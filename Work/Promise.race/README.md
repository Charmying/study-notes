# `Promise.race`

在 JavaScript 中，`Promise` 是處理非同步程式的核心工具之一。除了常見的 `Promise.all` 可以同時處理多個非同步任務外，`Promise.race` 也是非常實用的靜態方法，可以在多個 `Promise` 之間「比賽」，回傳最先完成 (無論成功或失敗) 的結果。

在深入 `Promise.race` 之前，先了解一下什麼是 `Promise`。

<br />

## `Promise` 簡介

在 JavaScript 中，非同步操作 (例如：網路請求、讀取檔案或計時器) 通常不會立即得到結果。傳統方式可能使用回呼函式 (Callback Function) 來處理結果，但當多層回呼疊加時，程式容易變得難以閱讀與維護，這就是俗稱的「回呼地獄 (Callback Hell)」。

`Promise` 是一種用來表示「未來可能完成或失敗的非同步操作結果」的物件。

`Promise` 的三種狀態

- Pending (待定)：初始狀態，尚未完成或失敗。

- Fulfilled (已完成)：非同步操作成功完成，並回傳結果。

- Rejected (已拒絕)：非同步操作失敗，回傳錯誤原因。

生活化舉例：使用訂餐系統時，每張訂單就像是一個 `Promise`

- 當下訂單時，餐點還沒送到 → Pending

- 餐點送到 → Fulfilled

- 店家取消訂單 → Rejected

可以透過 `.then()` 處理成功結果，或用 `.catch()` 處理失敗狀況。

```javascript
const order = new Promise((resolve, reject) => {
  const success = true; // 模擬訂單成功或失敗
  setTimeout(() => {
    if (success) resolve('餐點送到了！');
    else reject('訂單失敗！');
  }, 2000);
});

order
  .then(result => console.log(result))   // 成功：餐點送到了！
  .catch(error => console.error(error)); // 失敗：訂單失敗！
```

<br />

## `Promise.race` 的基本介紹

```javascript
Promise.race(iterable)
```

顧名思義，race 就像「競賽」。當傳入一組 `Promise` (或可轉換為 `Promise` 的值) 時，`Promise.race` 會同時監聽這些非同步任務，並回傳最先被解決 (Fulfilled) 或被拒絕 (Rejected) 的結果。

簡單來說，最先完成的 `Promise` 決定 `Promise.race` 的結果，而其他仍在執行的 `Promise` 結果將被忽略。

<br />

## `Promise.race` 的語法說明

```javascript
Promise.race(iterable)
```

- 參數

    - `iterable`：一個可迭代的物件 (例如：陣列)，裡面包含多個 `Promise` 或可轉換為 `Promise` 的值。

- 回傳值

    - 回傳一個新的 `Promise`。

        - 若最先完成的 `Promise` 為 Fulfilled，回傳該值。

        - 若最先完成的 `Promise` 為 Rejected，回傳錯誤。

<br />

## `Promise.race` 的範例

- 範例 1：最先完成的 `Promise` 決定結果

    ```javascript
    const p1 = new Promise((resolve) => setTimeout(() => resolve('p1 完成'), 3000));
    const p2 = new Promise((resolve) => setTimeout(() => resolve('p2 完成'), 1000));
    const p3 = new Promise((resolve) => setTimeout(() => resolve('p3 完成'), 2000));

    Promise.race([p1, p2, p3])
      .then(result => console.log(result)) // p2 完成
      .catch(error => console.error(error));
    ```

- 範例 2：最先「拒絕」的 `Promise` 也會決定結果

    ```javascript
    const p1 = new Promise((resolve) => setTimeout(() => resolve('成功的結果'), 2000));
    const p2 = new Promise((_, reject) => setTimeout(() => reject('發生錯誤！'), 1000));

    Promise.race([p1, p2])
      .then(result => console.log(result))
      .catch(error => console.error(error)); // 發生錯誤！

    ```

- 範例 3：實務應用 — 請求逾時機制 (Timeout)

    ```javascript
    function fetchWithTimeout(url, timeout) {
      const fetchPromise = fetch(url);
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject('請求逾時'), timeout)
      );

      return Promise.race([fetchPromise, timeoutPromise]);
    }

    fetchWithTimeout('https://example.com/data', 3000)
      .then(response => console.log('取得資料成功', response))
      .catch(error => console.error(error)); // 若超過 3 秒未回應，輸出「請求逾時」
    ```

<br />

## `Promise.race` 與 `Promise.all` 的比較

| 特性 | `Promise.all` | `Promise.race` |
| - | - | - |
| 完成條件 | 所有 `Promise` 都完成後回傳 | 任一 `Promise` 完成或失敗即回傳 |
| 結果內容 | 所有結果組成陣列 | 第一個完成的結果 |
| 常見用途 | 等待所有任務結束 | 設定逾時機制或比對最快結果 |

<br />

## `Promise.race` 的注意事項

- 不會取消其他 `Promise` 的執行

    即使某一個 `Promise` 已先完成，其他仍會繼續執行，只是結果不再被使用。若要中斷執行，需要額外設計取消機制 (例如：`AbortController`)。

- 適合需要「誰先完成就採用」的情境

    例如：多個伺服器節點的備援、影像或資源載入比賽等。

- 空陣列

    若輸入的陣列為空，`Promise.race` 永遠不會結束。

- 非 `Promise` 值

    若傳入的 iterable 包含非 `Promise` 的值 (例如：數字、字串)，會被自動轉為已完成的 `Promise`。

- 所有 `Promise` 都 Pending

    `Promise.race` 會持續等待，直到有一個完成或拒絕。

<br />

## 總結

`Promise.race` 是 JavaScript 中非常靈活的工具，可讓開發人員在多個非同步任務中快速決定結果，適合用於

- 建立逾時保護機制

- 多源資料請求：採用最先回應者策略

- 提供快速回饋的使用者體驗

理解並妥善運用 `Promise` 與 `Promise.race`，不僅能提升程式執行效率，也能讓非同步操作更具彈性與安全性。
