# 立即調用函式表達式 (IIFE)

立即調用函式表達式 (Immediately Invoked Function Expression，簡稱：IIFE) 指的是在宣告的當下就會馬上被執行的函數，通常用於創建一個局部作用域，避免全局污染。

### IIFE 的語法

```javascript
(function () {
  // 函式程式碼
})();
```

<br />

## IIFE 的簡單範例

- 使用 IIFE 創建一個局部作用域，避免變數污染全域

    ```javascript
    let count = 1;

    (function () {
      let count = 2;
      console.log(count); // 2
    })();

    console.log(count); // 1
    ```

- IIFE 為變數創建了一個單獨的命名空間，避免函式名稱和變數名稱衝突

    ```javascript
    let variable = "全域變數";

    (function () {
      let variable = "區域變數";
      console.log(variable); // 區域變數
    })();

    console.log(variable); // 全域變數
    ```

- 使用 IIFE 形成私有作用域

    ```javascript
    for (var i = 1; i <= 5; i++) {
      (function (i) {
        setTimeout(function () {
          console.log(i);
        }, i * 1000);
      })(i);
    }
    ```

    使用 IIFE 後每個迴圈都會形成一個私有作用域，因此 `i` 值可以被正確保留。

    以上程式碼若沒有使用 IIFE，那麼每次迴圈的 i 值都會被覆寫，導致最後輸出的結果都是 `6`。

    若不使用 IIFE 也想做到每隔一秒印出 `1 2 3 4 5`，可以將 `var` 改成 `let` 或使用閉包 (Closure)。

- IIFE 可以將程式碼分為獨立的模組，方便程式碼的管理和維護

    ```javascript
    /** Module 1 */
    (function () {
      var module1Variable = "module 1";

      function module1Function() {
        console.log(module1Variable);
      }
      window.module1 = {
        module1Function: module1Function,
      };
    })();

    /** Module 2 */
    (function () {
      var module2Variable = "module 2";
      function module2Function() {
        console.log(module2Variable);
      }
      window.module2 = {
        module2Function: module2Function,
      };
    })();

    /** Usage */
    module1.module1Function(); // module 1
    module2.module2Function(); // module 2
    ```

    以上程式碼通過兩個 IIFE 分別創建了兩個模組。每個模組內部都有自己的變數和函式，而 IIFE 的作用是創建局部作用域，避免變數污染。接著在 `window` 添加對應的模組物件，實現對模組的公開。使用時可以直接通過 `window` 物件存取模組中的函式實現模組化。

<br />

## IIFE 的優缺點

### 優點

- 創建局部作用域：通過使用 IIFE 創建一個局部作用域，避免變數污染全域。

- 避免命名衝突：IIFE 為變數創建了一個單獨的命名空間，避免函式名稱和變數名稱衝突。

- 形成私有作用域：讓變數可以被正確保留。

- 程式碼模組化：IIFE 可以將程式碼分為獨立的模組，方便程式碼的管理和維護。在前端模組化開始發展、並且還沒有前端模組化工具時，一開始就是使用 IIFE 作為模組化的實踐方式。

- 提高程式碼執行效率：IIFE 可以在定義時立即執行，避免函式的不必要的儲存和呼叫，提高程式碼的執行效率。

### 缺點

- 程式碼不易維護：當程式碼變更加複雜，IIFE 的程式碼容易變大，不易維護和閱讀。

- 不利於重複使用：IIFE 的程式碼通常是一次性的，無法復用，因此在需要多次呼叫時不太方便。

- 增加程式碼複雜度：使用 IIFE 可能會使程式碼變得更加複雜，特別是當程式碼量很大時。

<br />

## 參考資料

- [ES6 中的 class 是什麼？和函式構造函式差別是什麼？](https://www.explainthis.io/zh-hant/swe/what-is-class)
