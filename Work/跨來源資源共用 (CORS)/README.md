# 跨來源資源共用 (CORS)

跨來源資源共用 (Cross-Origin Resource Sharing，簡稱：CORS) 是一種瀏覽器的安全性機制，用於控制網頁應用程式在不同來源之間共享資源的方式。在網頁開發中，當一個網頁應用程式 (Domain A) 嘗試從另一個來源 (Domain B) 的網頁請求資源 (例如：API 請求或嵌入的內容等) 時，瀏覽器會實施 CORS 政策來確保安全性，防止惡意攻擊和跨站請求偽造 (CSRF) 等風險。

CORS 政策主要依賴於 HTTP 標頭來實施，允許伺服器告訴瀏覽器哪些來源的請求是被允許的。這是一種對同源政策的補充，讓開發人員能在安全的前提下實現跨域資源共享。

<br />

## 同源政策與跨域問題

在理解 CORS 之前，需要先了解瀏覽器的同源政策 (Same-Origin Policy)。

同源政策是一種重要的安全機制，用來防止不同來源之間的互相干擾。根據同源政策，網頁只能向與其相同來源的伺服器發送請求。所謂的同源，指的是以下三者相同

- 網域 (Domain)

- 協議 (Protocol)

- 端口 (Port)

舉例來說，對於 `https://www.example.com:443` 的網頁來說，以下的 URL 都被視為不同來源

- `http://www.example.com:443` (協議不同)

- `https://api.example.com:443` (網域不同)

- `https://www.example.com:8080` (端口不同)

而同源政策的主要目的是保護用戶的數據安全，防止惡意網站在用戶不知情的情況下發送請求來竊取或操控用戶的敏感資料。這有效阻止了許多潛在的安全漏洞，例如：XSS、CSRF 等。

現在許多應用程式需要在不同的域名之間共享資源。例如：單頁應用 (Single Page Applications，簡稱：SPA) 常常需要向不同的 API 發送請求來獲取資料，這就需要 CORS 的應用。

<br />

## CORS 的基本原理

CORS 的工作原理是通過伺服器設置特定的 HTTP 標頭來控制哪些來源可以存取資源。當瀏覽器發現一個跨域請求時，會檢查伺服器返回的 CORS 標頭來決定是否允許該請求。

<br />

## CORS 的運作機制

- 簡單請求

    簡單請求 (Simple Request) 是指請求滿足以下條件之一

    - 請求方法是 `GET`、`POST` 或 `HEAD`。

    - 請求的 HTTP 標頭限於 `Accept`、`Accept-Language`、`Content-Language`、`Content-Type` (僅限於 `text/plain`、`multipart/form-data`、`application/x-www-form-urlencoded`)。

    對於簡單請求，瀏覽器會自動處理 CORS，並在請求中添加 `Origin` 標頭，指出請求的來源。伺服器根據這個標頭返回適當的 CORS 標頭。

    簡單請求的流程：

    1. 瀏覽器發送簡單請求：

        ```http
        GET /api/data HTTP/1.1
        Host: api.example.com
        Origin: https://www.client.com
        ```

    2. 伺服器返回簡單響應

        ```http
        HTTP/1.1 200 OK
        Access-Control-Allow-Origin: https://www.client.com
        ```

    3. 瀏覽器檢查簡單響應

        若 `Access-Control-Allow-Origin` 標頭的值與請求的 `Origin` 相匹配，則允許存取資源，否則阻止存取資源。

- 預檢請求

    預檢請求 (Preflight Request) 是針對非簡單請求的一種安全檢查。當請求使用了非簡單方法 (例如：`PUT`、`DELETE`) 或自定義標頭時，瀏覽器會首先發送一個 `OPTIONS` 請求以確認伺服器是否允許該請求。

    1. 瀏覽器發送預檢請求：

        ```http
        OPTIONS /api/data HTTP/1.1
        Host: api.example.com
        Origin: https://www.client.com
        Access-Control-Request-Method: PUT
        Access-Control-Request-Headers: X-Custom-Header
        ```

    2. 伺服器返回預檢響應：

        ```http
        HTTP/1.1 204 No Content
        Access-Control-Allow-Origin: https://www.client.com
        Access-Control-Allow-Methods: GET, POST, PUT
        Access-Control-Allow-Headers: X-Custom-Header
        ```

    3. 瀏覽器發送實際請求：

        若預檢響應允許，瀏覽器會發送實際的請求，否則請求會被阻止。

- 回應請求

    伺服器對於跨域請求的回應應包含適當的 CORS 標頭

    - `Access-Control-Allow-Origin`：指定允許的來源。

    - `Access-Control-Allow-Methods`：指定允許的 HTTP 方法。

    - `Access-Control-Allow-Headers`：指定允許的自定義標頭。

    - `Access-Control-Allow-Credentials`：是否允許憑證 (例如：Cookie)。

    - `Access-Control-Expose-Headers`：指定哪些標頭可以在響應中被客戶端存取。

- 憑證與安全

    CORS 允許伺服器決定是否允許請求攜帶憑證 (例如：Cookie)。這是通過 `Access-Control-Allow-Credentials` 標頭控制的。需要注意的是，當啟用憑證時，`Access-Control-Allow-Origin` 不能設置為 `*`，必須是明確的來源。

<br />

## CORS 的實際應用

- API 服務

    許多 API 服務需要允許來自不同網域的請求。通過配置 CORS，API 提供者可以控制哪些網域可以存取。

- 微服務架構

    在微服務架構中，服務之間經常需要進行跨域通訊。CORS 能夠為這些跨域請求提供必要的安全保障。

- 第三方整合

    許多網站使用第三方服務 (例如：地圖、支付、身份驗證等)，這些服務通常需要跨域存取。CORS 使這些整合能夠在安全的前提下順利進行。

<br />

## CORS 的配置

不同的伺服器環境中，CORS 的配置可能略有不同。

### Node.js

在 Node.js 中，可以使用中介軟體 (Middleware) 來設置 CORS 標頭。例如：使用 Express 框架時，可以安裝 CORS 中介軟體：

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

// 配置 CORS
const corsOptions = {
  origin: 'https://www.client.com',
  methods: 'GET,POST,PUT,DELETE',
  allowedHeaders: 'Content-Type,Authorization',
  credentials: true
};

app.use(cors(corsOptions));

app.get('/api/data', (req, res) => {
  res.json({ message: 'Hello, CORS!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### Apache

在 Apache 伺服器中，可以在 `.htaccess` 中或伺服器配置文件中添加以下配置

```apache
<IfModule mod_headers.c>
  Header set Access-Control-Allow-Origin "https://www.client.com"
  Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE"
  Header set Access-Control-Allow-Headers "Content-Type, Authorization"
  Header set Access-Control-Allow-Credentials "true"
</IfModule>
```

### Nginx

在 Nginx 中可以在伺服器塊 (Server Block) 中添加以下配置

```nginx
location /api/ {
  add_header 'Access-Control-Allow-Origin' 'https://www.client.com';
  add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE';
  add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
  add_header 'Access-Control-Allow-Credentials' 'true';
}
```

<br />

## 常見的 CORS 問題與解決方案

- No 'Access-Control-Allow-Origin' header is present

    解決方法：確保伺服器設置了正確的 `Access-Control-Allow-Origin` 標頭，並且該標頭的值與請求來源匹配。

- CORS 預檢請求被阻止

    解決方法：檢查伺服器是否正確處理 `OPTIONS` 預檢請求，並返回正確的 CORS 標頭。

- Credentials mode is 'include' but the 'Access-Control-Allow-Credentials' header is ''

    解決方法：確保伺服器返回 `Access-Control-Allow-Credentials: true`，並且 `Access-Control-Allow-Origin` 不能為 `*`。

<br />

## 總結

CORS 是現代 Web 安全中不可或缺的一部分。通過理解和正確配置 CORS，開發人員能夠在保證安全的前提下，實現豐富的跨域資源共享功能。掌握 CORS 有助於開發人員設計和構建更加安全和高效的專案。
