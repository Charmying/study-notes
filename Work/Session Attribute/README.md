# Session Attribute

Session Attribute (會話屬性) 簡單來說是指在網站或應用程式中，當一個用戶與 Server 建立 session (會話) 時，Server 用來儲存與該用戶相關資訊的屬性或變數。

若想了解 Session Attribute，會需要先了解 session 是什麼。

<br />

## Session

Session 是一種用於用戶與 Server 之間維持狀態的機制。因為 HTTP 協議是無狀態的，每次請求都是獨立的，Server 不會記得之前的請求，所以需要使用 Session 來跟蹤用戶的活動。

- ### Session 的實現

    - Session ID：每個 Session 都有一個唯一的識別符，稱為 Session ID。當用戶首次訪問網站時，Server 會創建一個 Session 並生成一個 Session ID，然後通過 Cookie、URL 重寫或其他方法將這個 ID 傳給用戶。

    - Session 儲存：Session 可以儲存在 Server、database 或檔案系統中。Server 需要一種機制來追蹤 Session ID 與其儲存的數據之間的映射。

- ### Session 的特點

    - 狀態保持：Session 用在多個 HTTP 請求之間保存用戶的狀態和資料。對於需要狀態持久性的情況 (例如：登入系統、購物車) 非常重要。

    - Server 端儲存：Session 通常儲存在 Server 端，而只在 Server 端儲存一個唯一的識別符 (Session ID)，這樣可以提高安全性，因為敏感資料不會暴露在 Client 端。

    - 唯一識別：每個用戶 Session 由一個唯一的 Session ID 標識，該 ID 通常是通過 Cookie、URL 重寫或其他方法傳遞。

    - 有限的生存週期：Session 通常有一個預定的生存時間，在用戶不活動一段時間後會自動過期。過期的 Session 不再有效，Server 會清除相關資料。

- ### Session 的工作原理

    1. 創建 Session：當用戶第一次訪問應用程式時，Server 創建一個新的 Session 並生成一個唯一的 Session ID。這個 ID 通常會在 HTTP 響應中以 Cookie 的形式發送到用戶的瀏覽器。

    2. 維護 Session：在後續的每次請求中，瀏覽器會自動將 Session ID 發送回 Server (通常是通過 Cookie)，Server 使用該 ID 獲取相關的 Session 數據，從而識別用戶並執行相應的操作。

    3. 存取和更新 Session：在 Session 期間，用戶的每個請求都會附帶這個 Session ID，Server 通過這個 ID 來存取和更新相應的 Session 屬性。這使用戶的狀態和資料能夠在 Session 期間保持一致。

    4. 終止 Session：當用戶登出或 Session 過期時，Server 會刪除相應的 Session 數據，並使該 Session ID 無效。

- ### Session 的應用

    - 用戶身份驗證：在登入系統中，Session 可以用於保存用戶的身份訊息，這樣用戶在網站的不同頁面之間切換時不需要重新登入，也可以識別和授權用戶的請求。

    - 購物車功能：在電商網站中，Session 可以用來保存用戶的購物車資料，使用戶在瀏覽網站的過程中不丟失購物車內容。

    - 數據儲存：可以在 Session 中儲存臨時數據，例如：用戶偏好設定或表單數據，以便用戶在 Session 期間存取。

- ### Session 在不同技術中的簡單範例

    - Java (Servlet 和 JSP)：使用 `HttpSession` 來管理 Session

        ```java
        /** 創建或獲取會話 */
        HttpSession session = request.getSession();

        /** 設定 Session Attribute */
        session.setAttribute("user", "Charmy");

        /** 獲取 Session Attribute */
        String user = (String) session.getAttribute("user");
        ```

    - Node.js Express：使用 `express-session` 來管理 Session

        ```javascript
        const session = require('express-session');

        app.use(session({
          secret: 'mySecret',
          resave: false,
          saveUninitialized: true,
          cookie: { secure: true }
        }));

        /** 設定 Session Attribute */
        req.session.username = 'Charmy';

        /** 獲取 Session Attribute */
        const username = req.session.username;
        ```

    - Python/Flask：使用 Flask 的 `session` 功能

        ```python
        from flask import Flask, session

        app = Flask(__name__)
        app.secret_key = 'mySecret'

        @app.route('/')
        def index():
            # 設定 Session Attribute
            session['username'] = 'Charmy'
            return 'session set'

        @app.route('/get')
        def get_session():
            # 獲取 Session Attribute
            username = session.get('username', 'Guest')
            return f'Hello, {username}!'
        ```

    - PHP：使用 `$_SESSION`

        ```php
        session_start();

        /** 設定 Session Attribute */
        $_SESSION['username'] = 'Charmy';

        /** 獲取 Session Attribute */
        $username = $_SESSION['username'];
        ```

- ### Session 與 Cookie 的差別

    - Session 是儲存在 Server 端的，Cookie 是儲存在 Client 端 (用戶的瀏覽器) 上的。

    - Cookie 通常用於儲存一些簡單的或長期有效的資料，而 Session 更適合用在儲存臨時且敏感的資料。

- ### Session 的好處

    - 安全性：由於 Session 儲存在 Server 上，敏感訊息不會直接暴露給 Client 端，提高了安全性。

    - 靈活性：Session 可以很容易更新或刪除，並且可以儲存比 Cookie 更多的數據。

- ### Session 的常見問題

    - Session 失效：Session 通常有一定的有效期，若用戶在 Session 到期後繼續操作，可能會導致重新登錄或數據丟失。

    - 性能問題：大量的 Session 可能會增加 Server 的負擔，因此需要合理管理和清理過期的 Session。

<br />

## Session 和 sessionStorage 的差別

Session 和 sessionStorage 是兩種不同的技術，一開始在聽說的時候容易搞混，但是在用法、儲存位置和生命周期等有很大的差異。

- ### sessionStorage 的特點

    - Client 端儲存：sessionStorage 是一種 Web 儲存 API，資料儲存在 Client 端的瀏覽器中。

    - 生命周期：sessionStorage 的資料僅在同一瀏覽器窗口或標籤頁的持續期間有效。當窗口或標籤頁關閉時，資料會被刪除。

    - 隔離性：sessionStorage 資料是特定於每個窗口或標籤頁的，即便是同一網站，不同的標籤頁也無法共享 sessionStorage 資料。

    - 不適合儲存敏感資料：由於資料儲存在 Client 端，sessionStorage 不適合儲存敏感的用戶訊息。

- ### sessionStorage 的應用場景

    - 臨時資料：適合儲存需要在用戶瀏覽過程中保持的臨時數據，例如：表單填寫進度。

    - 用戶交互狀態：保存用戶在某一頁面的交互狀態，比如展開/折疊狀態。

- ### 對比總結

    | 特點 | Session | sessionStorage |
    | - | - | - |
    | 儲存位置 | Server 端 | Client 端 (瀏覽器) |
    | 儲存範圍 | 整個 Session 中的所有頁面 | 單個窗口或標籤頁 |
    | 儲存持久性 | 在 Session 結束或過期時清除 | 在窗口或標籤頁關閉時清除 |
    | 安全性 | 更加安全，適合儲存敏感訊息 | 不適合儲存敏感訊息 |
    | 典型用例 | 用戶登入狀態、購物車資料、個性化設置 | 臨時資料、用戶交互狀態 |
    | 資料共享 | 同一 Session 中可跨頁面共享 | 不同窗口或標籤頁間不共享 |

<br />

## 總結

在選擇使用 Session 還是 sessionStorage 時，可以根據需求、資料安全性和持久性來決定。若需要在 Server 端安全儲存並管理用戶的 Session 狀態，可以使用 Session。若需要在用戶單次瀏覽期間在 Client 端臨時儲存資料，則可以使用 sessionStorage。
