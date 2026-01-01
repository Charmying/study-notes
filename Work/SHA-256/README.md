# SHA-256

SHA-256 全名為 Secure Hash Algorithm 256-bit，屬於 SHA-2 家族，核心功能是把一段資料 (例如：文字、檔案或其他訊息) 轉換成一個長度固定為 256 位元 (32 位元組) 的雜湊值。

舉例來說

- 輸入文字：`Hello`

- 輸出雜湊值

    ```text
    185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969
    ```

特點是

- 固定長度：不論輸入內容大小，輸出永遠是 64 個十六進位字元。

- 單向性：無法由輸出反推出原始輸入。

- 高敏感性：輸入只要改變一點點，輸出就會完全不同。

<br />

## SHA-256 的運算流程

SHA-256 的計算並非簡單的加總或壓縮，而是基於一套嚴謹的數學與運算。整體流程可分為以下步驟

1. 前處理 (Preprocessing)

    - 訊息填充 (Padding)

        將原始訊息補齊到長度為 512 位元的倍數。

    - 長度附加

        在訊息最後加上原始訊息的長度 (以 64 位元表示)。

2. 分組處理 (Message Schedule)

    將訊息切分成 512 位元的區塊，每個區塊再被拆成 32 位元的小段，進入後續計算。

3. 初始化 (Initialization)

    定義八個固定的 32 位元初始常數 (這些數值來自數學中的質數平方根)，作為運算的起點。

4. 雜湊迭代 (Compression Function)

    對每個訊息區塊，反覆進行以下運算：

    - 位元運算 (Bitwise Operations)

        包含 AND、OR、XOR、位移 (Shift、Rotate)，確保資料被充分混合。

    - 模 2³² 加法 (Modulo 2³² Addition)

        所有數值都在 32 位元範圍內運算，超過部分會自動捨去，形成「環狀」計算。

    - 非線性函數混合 (Non-linear Functions)

        引入運算公式，讓雜湊值呈現高度隨機性。

    - 常數加法 (Addition of Constants)

        每一輪計算都會加入固定常數 (來自前 64 個質數的立方根小數部分)，避免攻擊者輕易預測運算規律。

    這些步驟能確保執行結果具備高隨機性與不可逆性。

5. 最終輸出

所有區塊處理完成後，將結果拼接，得到最終的 256 位元雜湊值。

<br />

## SHA-256 的特性

- 單向不可逆

    - 無法從雜湊值還原輸入，這讓密碼儲存更加安全。

- 固定長度輸出

    不論輸入是一個字母還是一本書，輸出永遠是 256 位元。

- 抗碰撞性 (Collision Resistance)

    幾乎不可能找到兩個不同輸入卻產生相同輸出。

- 雪崩效應 (Avalanche Effect)

    輸入僅改變一個字元，輸出就會徹底不同，避免被攻擊者預測。

<br />

## SHA-256 的應用

- 密碼儲存與驗證

    系統通常不會儲存使用者密碼，而是儲存密碼的 SHA-256 雜湊值，登入時再進行比對。

- 數位簽章 (Digital Signature)

    文件摘要透過 SHA-256 計算，再使用非對稱加密簽章，能保證文件來源與內容完整性。

- 檔案完整性檢查

    軟體下載頁面常附上 SHA-256 校驗碼，使用者能自行驗證檔案是否遭到竄改。

- 區塊鏈與加密貨幣

    比特幣挖礦、交易驗證與區塊鏈鏈結，核心演算法就是 SHA-256。

- 網路安全協定

    在 HTTPS、VPN 等通訊協定中，SHA-256 被廣泛應用於訊息驗證碼 (MAC) 與憑證簽章。

<br />

## SHA-256 的安全性與挑戰

截至目前，SHA-256 仍被視為安全，尚未有實用性的攻擊能破解其碰撞或逆向運算。

但隨著量子電腦的發展，未來可能需要更新更強的演算法，例如

- SHA-3 (新一代標準)

- 量子抗性演算法

<br />

## 程式範例

- Python 範例

    ```python
    import hashlib

    # 原始訊息
    data = "Hello SHA-256"

    # 計算 SHA-256
    hash_value = hashlib.sha256(data.encode()).hexdigest()

    print("輸入：", data)
    print("SHA-256 輸出：", hash_value)
    ```

    執行結果：

    ```console
    輸入： Hello SHA-256
    SHA-256 輸出： 44d8a6f40a4f8c59a0b51cba940de9fa40c8478690db9c1a7db845c5e54cf6d6
    ```

- Node.js 範例

    Node.js 內建 `crypto` 模組，不需要額外安裝套件即可使用。

    ```javascript
    const crypto = require('crypto');

    /** 原始訊息 */
    const data = "Hello SHA-256";

    /** 使用 SHA-256 演算法 */
    const hash = crypto.createHash('sha256').update(data).digest('hex');

    console.log("輸入：", data);
    console.log("SHA-256 輸出：", hash);
    ```

    執行結果：

    ```console
    輸入： Hello SHA-256
    SHA-256 輸出： 44d8a6f40a4f8c59a0b51cba940de9fa40c8478690db9c1a7db845c5e54cf6d6
    ```

- 瀏覽器端範例 (Web Crypto API)

    現代瀏覽器提供 `crypto.subtle` API，可直接計算 SHA-256。

    ```html
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
      <meta charset="UTF-8">
      <title>SHA-256 範例</title>
    </head>
    <body>
      <h3>SHA-256 計算</h3>
      <input type="text" id="inputText" placeholder="輸入文字">
      <button onclick="hashText()">計算 SHA-256</button>
      <p id="output"></p>

      <script>
        async function hashText() {
          const text = document.getElementById("inputText").value;
          const encoder = new TextEncoder();
          const data = encoder.encode(text);

          /** 計算 SHA-256 */
          const hashBuffer = await crypto.subtle.digest("SHA-256", data);

          /** 轉換為十六進位字串 */
          const hashArray = Array.from(new Uint8Array(hashBuffer));
          const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

          document.getElementById("output").textContent = `SHA-256 輸出：${hashHex}`;
        }
      </script>
    </body>
    </html>
    ```

    操作方式

    1. 在輸入框輸入任何文字

    2. 按下「計算 SHA-256」

    3. 下方會顯示對應的 SHA-256 雜湊值

- 使用第三方套件 (跨環境方便)

    若想同一份程式碼同時在 Node.js 與瀏覽器使用，可以安裝 [crypto-js](https://www.npmjs.com/package/crypto-js)

    ```bash
    npm install crypto-js
    ```

    ```javascript
    const CryptoJS = require("crypto-js");

    /** 原始訊息 */
    const data = "Hello SHA-256";

    /** 計算 SHA-256 */
    const hash = CryptoJS.SHA256(data).toString(CryptoJS.enc.Hex);

    console.log("輸入：", data);
    console.log("SHA-256 輸出：", hash);
    ```

<br />

## 總結

SHA-256 是 SHA-2 家族中最廣泛使用的雜湊演算法，具備單向性、固定長度輸出、雪崩效應與抗碰撞性等特點，至今仍是資訊安全領域的核心基礎。

在實務應用上，SHA-256 不僅用於密碼驗證、檔案完整性檢查，更是區塊鏈與加密貨幣的安全支柱，同時也被廣泛應用於數位簽章、網路通訊協定 (例如：HTTPS、TLS)。

雖然目前尚未出現能有效破解 SHA-256 的攻擊方式，但隨著量子運 的發展，未來可能需要更高強度或抗量子的雜湊演算法 (例如：SHA-3)。

簡單來說

- 安全性：目前仍被認為足夠安全

- 應用面：廣泛存在於現代資訊系統與加密技術

- 未來性：可能隨量子電腦發展而演進

目前 SHA-256 不只是一個數學公式，而是現代網路世界 信任與安全的基石。
