# JWT (JSON Web Token)

JWT 的全名是 JSON Web Token，是一種基於 JSON 格式開放標準 (RFC 7519) 的安全認證方式，可以把資訊包在 JSON 物件格式中。

JWT 定義了一種簡潔 (Compact) 且自包含 (Self-contained) 的方式，用在雙方安全將訊息作為 JSON 物件傳輸。訊息經過數位簽章 (Digital Signature)，所以可以被驗證和信任。可以透過密碼 (經過 HMAC 演算法) 或用公鑰與私鑰 (經過 RSA 或 ECDSA 演算法) 來對 JWT 進行簽章，生成一連串編碼過後的字串後可以用來進行身份驗證或授權。

<br />

## JWT 的流程

<img src="https://github.com/user-attachments/assets/f799adc2-7cc7-423b-9c93-5186280e2884" width="100%" />

### JWT 流程簡介

1. Client 端發送 HTTP Post 請求到 Server 端，攜帶用戶名稱和密碼。

2. Server 端驗證用戶名稱和密碼，若驗證成功產生 Token。

3. Server 端將資料和 Token 返回 Client 端。

4. Client 端保存 Token。

5. Client 端向 Server 端發送需要認證的 API 請求，在 Authorization 中帶上 Token。

6. Server 端驗證 Token，沒問題就解碼 Token 中的資料。

7. 伺服器端將請求的資料送回客戶端。

<br />

## JWT 的結構

JWT 由三個部分組成，分別是 Header、Payload 和 Signature/Encryption Data，並使用點 `.` 做分隔。

- Header：描述演算法與類型。

- Payload：存放資料與聲明 (Claims)。

- Signature：簽章，用於驗證完整性與來源。

Header 和 Payload 是特定結構的 JSON 物件，Signature 取決於演算法是用來作簽章還是加密，若是未加密的 JWT 則省略。

JWT 可以被編碼成 JWS/JWE 簡潔的表現形式 (Compact Serialization)。JWS 和 JWE 規範中定義了另一種序列化格式，稱為 JSON 序列化，是一種非簡潔的表示形式，允許在同一個 JWT 中使用多個簽章或接收者。

- JWS (JSON Web Signature)：簽章但不加密 (最常見，登入授權幾乎都用這種)。

- JWE (JSON Web Encryption)：加密 JWT，內容不可被解讀，但實務上使用較少。

簡潔的序列化 (The compact serialization) 是對前兩個 UTF-8 字節的 JSON 元素 (Header 和 Payload) 以及進行簽章或加密的 Data (不是 JSON 物件本身) 做 Base64 URL 安全編碼。三部分分別用一個 `.` 隔開，所以結果會像

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                                 # Header
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9. # Payload
TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ                           # Signature
```

<img src="https://github.com/user-attachments/assets/3ad8ea57-3f7a-4676-ae7a-1ea695528ec5" width="100%" />

- Header

    每個 JWT 都有一個 Header (又稱 JOSE Header)，是一種自我聲明，無論 JWT 是簽章的還是加密，這些聲明都表示所使用的演算法，通常也會表示如何解析 JWT 的其餘部分。

    根據 JWT 的類型，Header 中可能包含更多字段。例如：加密的 JWT 攜帶有關用於密鑰加密和內容加密的加密演算法的訊息。對於未加密的 JWT 就沒有這些字段。

    ### Header 內含

    - 必要欄位

        - `alg`：對此 JWT 進行簽章 & 解密的主要演算法，例如：HS256 (HMAC-SHA256)、RS256 (RSA-SHA256)。

            - ⚠️ 若設為 `none` 代表無簽章，在安全上極度危險，實務中絕不可使用。

    - 非必要欄位：

        - `typ`：JWT 本身的媒體類型。此參數僅助於將 JWT 與帶有 JOSE Header 的其他物件混合使用的情況。但是這種情況很少發生。若存在的話此聲明應設置為值 JWT。

        - `cty`：內容類型。大多數 JWT 攜帶特定的聲明以及任意數據作為 Payload 的一部分，在這種情況下，不得設置內容類型聲明。對於 Payload 本身是 JWT 自己 (巢狀 JWT) 的實例，此聲明必須存在並帶有值 JWT，用來表示需要進一步處理巢狀的 JWT。巢狀 JWT 很少見，因此 cty 聲明很少出現在 Header 中。

    若一個未加密的 JWT，Header 會是如下

    ```json
    {
      "alg": "none"
    }
    ```

    經過編碼後為 `eyJhbGciOiJub25lIn0`

- Payload

    Payload 存放 Token 的資料與聲明 (Claims)。

    ```json
    {
      "name": "Charmy",
      "age": "28",
      "title": "Front-end"
    }
    ```

    通常要帶的資料都會被放在 Payload 裡，可以是 `userId`，還可以在這裡指定 Token 到期時間。某些規範中定義的權利要求也可能存在。就像 Header 一樣，Payload 是一個 JSON 物件。儘管特定的權利要求具有明確的含義，但沒有權利要求是強制性的。JWT 規範指出應該忽略在實踐中無法理解的聲明。

    - Registered Claims (註冊聲明)

        具有所附特定含義的權利要求。

        - `iss` (Issuer)：JWT 的簽發者。

            用字串 (Case-sensitive，區分大小寫) 或 URI 表示 JWT 的唯一識別的發行方。

        - `sub` (Subject)：主體 (此 JWT 屬於誰)。

            用字串 (Case-sensitive，區分大小寫) 或 URI 表示 JWT 所夾帶的唯一識別訊息。也就是說，此 JWT 中包含的聲明是關於物件的聲明。JWT 規範規定，此聲明在發行方的上下文中必須是唯一的，或者在不可能的情況下必須是全局唯一。處理此聲明是特定於應用程式。

        - `aud` (Audience)：接收 JWT 的一方。

            用字串 (Case-sensitive，區分大小寫)、URI (Uniform Resource Identifier) 或陣列表示這個 JWT 唯一識別的預期接收者。也就是說，當此聲明存在，則讀取此 JWT 中的數據的一方必須在 `aud` 中找到自己，或者無視 JWT 中包含的數據。與 `iss` 和 `sub` 要求的情況一樣，該權利要求是專用的。

        - `exp` (Expiration Time)：JWT 的過期時間。

            用來表示特定日期和時間的數字，格式為 POSIX 定義自紀元以來的秒數 (UNIX 時間)。此聲明設置了該 JWT 被視為無效的確切時間。一些實踐可能允許時間存在一定的偏差 (考慮此 JWT 在到期日後的幾分鐘內有效)。

        - `nbf` (Not Before Time)：定義擬發放 JWT 之後的某段時間點前該 JWT 仍舊是不可用的。

            `exp` 的相反，格式跟 `exp` 一樣，當前時間和日期必須等於或晚於該日期和時間。一些實踐可能允許一定的偏差。

        - `iat` (Issued At Time)：JWT 簽發時間。

            一個用來表示特定日期和時間的數字 (格式跟 `exp` 和 `nbf`)，即該 JWT 發行的時間。

        - `jti` (JWT ID)：JWT 的身分標示。

            一個字串表示這個唯一識別的 JWT。此聲明可用於區分具有其他相似內容的 JWT (例如：防止重放)。取決於實現以確保唯一性。

    所有的聲明，只要不在 Registered Claims 裡的，不是 Public Claims 就是 Private Claims。

    - Public Claims (公開聲明)

        可以想成是傳遞的欄位必須跟 Registered Claims 欄位不能衝突，可以向官方申請定義公開聲明，會進行審核等步驟，實務開發上不太會用這部分。

    - Private Claims (私有聲明)

        由 JWT 的使用雙方定義，通常用於傳遞用戶相關的訊息。

        發放 JWT 伺服器可以自定義欄位的部分，例如：實務上會放 User Account、User Name、User Role 等不敏感數據。

        使用者密碼等就是敏感數據，因為 Payload 傳遞的訊息最後也是透過 Base64 進行編碼，所以是可以被破解的，因此放使用者密碼會有安全性問題。

- Signature

    根據 Header 與 Payload 再加上私鑰使用特定的算法進行簽章，用來驗證 JWT 是否被篡改過，演算法取決於 Header 的 `alg`。

    Signature 是用來驗證訊息未被竄改的部分。Signature 是將編碼後的 Header、Payload 和一個密鑰進行簽名算法運算得出的結果。

    Signature 是由 Base64UrlEncode (Header)、Base64UrlEncode (Payload)、Secret 三大部分組成

    ```text
    HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
    ```

    - Signature 不是加密，而是 雜湊簽章。

    - Secret 必須安全保存在伺服器端，若外洩，攻擊者即可偽造 Token。

    最後將 Header、Payload、Signature 三者用 `.` 串聯在一起，就是一個合法簽發的 JWT 字串。

<br />

## JWT 常見的儲存地方

- localStorage：由於網站容易使用第三方 JavaScript 程式碼，例如：Vue、React、Angular、jQuery、Google Analytics 等，若駭客有辦法在網站內執行 JavaScript，就有可能竊取在 localStorage 的 JWT，這就是常見的 XSS 攻擊。只要能夠獲取 JWT 就能夠閱讀其內容。 因此並不建議存在 localStorage 中。

- Cookie：透過以下設定可以增加 JWT 放置於 Cookie 的安全性

    - `httpOnly`：駭客不能透過 JavaScript 去取得 Cookie 中的內容。

    - `Secure`：透過 HTTPS 的方式傳送憑證。

    - `Samesite`：防止跨站請求偽造 (CSRF) 攻擊。

<br />

## JWT 的適用範圍

- 授權 (Authorization)

    JWT 是一種憑證，例如：使用者從 Client 端登入後，使用者再次對 Server 端發送請求的時候會帶著 JWT，允許使用者存取該 Token 有權限的資源。單一登錄 (Single Sign On) 是當今廣泛使用 JWT 的功能之一，因為成本較小並且可以在不同的網域 (Domain) 中輕鬆使用。

    #### 憑證：指 JWT 整個字串，可以用來做身份驗證與授權

    - 適用於 單一登入 (SSO) 與分散式系統。

- 訊息交換 (Information Exchange)

    JWT 可以透過公鑰與私鑰做簽章，這樣可以知道是誰發送 JWT，而且由於簽章是使用 Header 和 Payload 計算的，因此還可以驗證內容是否遭到篡改。

    #### 簽章：使用私鑰對 JWT 的 Header 與 Payload 進行簽章，用來驗證訊息的完整性。

<br />

## JWT 的優缺點

### 優點

- 自包含 (Self-contained)

    JWT 包含所有必要的訊息 (例如：用戶身份、過期時間等)，因此不需要在 Server 端儲存資料。降低了伺服器的負擔並提高了性能。

    應用範圍：伺服器可以根據 Token 中的資訊直接進行授權判斷，而不需要進行多次的資料庫查詢。

- 可擴展性 (Scalability)

    由於不需要 Server 端的資料儲存，可以輕易在多個伺服器或微服務架構中使用 JWT，無需考慮會話同步問題。

    應用範圍：非常適合於分佈式系統和需要高擴展性的應用。

- 跨平台性 (Cross-platform Compatibility)

    JWT 使用 JSON 格式，這是一種通用的數據交換格式，因此可以在不同的技術堆棧 (例如：Java、Node.js、Python 等) 中輕鬆使用。

    應用範圍：能夠在前後端不同的技術堆棧中互相傳遞訊息。

- 減少伺服器查詢 (Reduced Server Querying)

    由於 JWT 是自包含的，伺服器不需要每次請求時查詢資料庫來驗證用戶身份，降低了資料庫負載。

    應用範圍：提高了應用的響應速度和效率。

- 無狀態 (Stateless)

    JWT 本質上是無狀態的，也就是說，不需要在 Server 端存儲任何用戶資料。

    應用範圍：對於需要處理大量並發請求的應用而言非常有用。

- 安全性 (Security)

    JWT 可以使用數字簽名來驗證其完整性和來源，確保數據不被竄改。還可以通過加密來保護敏感訊息。

    應用範圍：對於需要確保資料完整性和來源可信的應用來說，這是一個重要的安全層。

### 缺點

- 不可撤銷 (Non-revocable)

    一旦 JWT 發出後，在其有效期內無法撤銷或使其失效，也就是說，若 JWT 被竊取，攻擊者可以持續使用直到過期。

    解決方案：需要設計短期有效的令牌，並使用刷新令牌 (Refresh Token) 來定期更新 JWT。

- 令牌大小 (Token Size)

    相比於傳統的會話 ID，JWT 的大小更大，因為包含了所有的用戶資料，可能會增加網路傳輸的負擔。

    解決方案：儘量縮減 JWT 中的訊息量，僅保留必要的聲明。

- 敏感數據風險 (Sensitive Data Risk)

    JWT 雖然可以加密，但一般使用的是簽名而不是加密，這意味著任何人都可以解碼並查看未加密的內容。

    解決方案：不要在 JWT 中存儲敏感或機密數據，例如：密碼或個人身份訊息。

- 過期處理  (Expiration Handling)

    JWT 的過期時間必須設定得當，過短可能導致用戶體驗不佳，過長則增加了被濫用的風險。

    解決方案：設定合理的過期時間，並使用刷新令牌機制來平衡安全性和用戶體驗。

- 需要妥善管理密鑰 (Key Management)

    JWT 的安全性依賴於簽名密鑰的安全性，若密鑰洩露，整個系統將受到威脅。

    解決方案：確保密鑰的安全存儲和管理，並定期更新密鑰。

<br />

## 參考資料

- [是誰在敲打我窗？什麼是 JWT ？](https://5xcampus.com/posts/what-is-jwt.html)

- [JWT 介紹](https://medium.com/@jesshsieh9/jwt-%E7%B0%A1%E4%BB%8B-f202e0b34099)

- [JWT(JSON Web Token) — 原理介紹](https://medium.com/%E4%BC%81%E9%B5%9D%E4%B9%9F%E6%87%82%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88/jwt-json-web-token-%E5%8E%9F%E7%90%86%E4%BB%8B%E7%B4%B9-74abfafad7ba)

- [What is JWT (JSON Web Token)? How does JWT Authentication work?](https://www.miniorange.com/blog/what-is-jwt-json-web-token-how-does-jwt-authentication-work/)
