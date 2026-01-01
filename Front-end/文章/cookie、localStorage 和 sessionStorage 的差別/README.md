# `cookie`、`localStorage` 和 `sessionStorage` 的差別

`cookie`、`sessionStorage` 和 `localStorage` 都是用來在使用者瀏覽器中儲存資料的技術，但在使用方式、儲存的資料量、存取範圍和存活時間等方面有明顯的差異。

<br />

## `cookie`

### 可設定失效時間。 預設是關閉瀏覽器後失效

`cookie` 是網頁儲存技術中歷史最悠久的一種，最初是為了在客戶端和伺服器之間傳遞小量資料而設計的。

`cookie` 有著較多的應用限制，但在某些情境下仍然是不可或缺的工具。

- 儲存範圍

    `cookie` 與特定的網站域名綁定，並且可以設定適用的路徑，也就是說，`cookie` 可以在網站中的某些特定頁面間共享或限制在某些頁面使用。`cookie` 可以被客戶端 (瀏覽器) 和伺服器端同時存取，這讓 `cookie` 成為在客戶端和伺服器間交換資料的重要工具。

- 資料存活時間

    `cookie` 可以設定明確的過期時間 (Expiration Time)。當設定了過期時間後，`cookie` 會在該時間點之前一直保留，即使瀏覽器被關閉也不會消失。若未設定過期時間，`cookie` 會在當前瀏覽器會話結束 (關閉瀏覽器) 時自動刪除。

- 儲存容量

    `cookie` 的儲存容量相對較小，通常每個 `cookie` 的大小限制在 4KB 以內，而且每個域名下最多只能儲存約 20 個 `cookie`。這使 `cookie` 更適合用來儲存小型的資料，例如：用戶 ID、登入憑證等。

- 使用範例

    `cookie` 最常見的用途之一是儲存用戶的登入狀態。當使用者登入後，伺服器可以將登入憑證存儲在 `cookie` 中，瀏覽器每次向伺服器發送請求時，都會自動附帶該 `cookie`，使伺服器能夠識別用戶的身份。

	```javascript
	// 設定 cookie
	document.cookie = "username=Charmy; expires=Fri, 31 Dec 2024 12:00:00 UTC; path=/";

	// 讀取 cookie
	const cookies = document.cookie.split('; ').reduce((prev, current) => {
	  const [name, value] = current.split('=');
	  prev[name] = value;
	  return prev;
	}, {});

	// 刪除 cookie (通過設定過期時間來刪除)
	document.cookie = "username=Charmy; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
	```

<br />

## `localStorage`

### 不會過期，除非手動清除

`localStorage` 是一種瀏覽器內建的儲存方式，專門用來儲存大量的、需要持久化的資料。

- 儲存範圍

    `localStorage` 與網站域名 (domain) 綁定，因此在同一個瀏覽器中，只要是來自同一個域名的網頁，不論是不同的分頁還是重新載入，均可存取相同的 `localStorage` 資料。這讓 `localStorage` 特別適合儲存需要跨多個頁面共用的資料，例如：使用者的偏好設定、購物車資料等。

- 資料存活時間

    `localStorage` 的資料是持久性的。也就是說，儲存在 `localStorage` 裡的資料即使在瀏覽器關閉後也會持續保存，除非使用者手動清除瀏覽器資料或開發人員在程式碼中明確刪除這些資料。這使得 `localStorage` 非常適合用來儲存需要長時間保留的資料。

- 儲存容量

    `localStorage` 通常有較大的儲存空間，依據不同的瀏覽器，儲存容量約在 5MB 至 10MB 之間。這相比於其他兩種儲存方式，提供了更大的儲存空間，適合用來儲存更大量的資料。

- 使用範例

    `localStorage` 最常見的使用情境之一是儲存使用者的偏好設定，例如：主題顏色、語言選擇等。這些資料在使用者再次瀏覽網站時可以被快速載入，提供一致且個性化的使用體驗。

	```javascript
	// 儲存資料至 localStorage
	localStorage.setItem('theme', 'dark');

	// 從 localStorage 讀取資料
	const theme = localStorage.getItem('theme');

	// 刪除 localStorage 中的資料
	localStorage.removeItem('theme');
	```

<br />

## `sessionStorage`

### 每次分頁或瀏覽器關掉後就會清除

`sessionStorage` 是與 `localStorage` 相似的瀏覽器儲存技術，但設計目的是用來儲存臨時性的資料，只會在特定的瀏覽期間有效。

- 儲存範圍

    `sessionStorage` 與 `localStorage` 一樣，與網站域名綁定。但與 `localStorage` 不同的是，`sessionStorage` 的資料只在同一個瀏覽器分頁或視窗共享。也就是說，即使開啟多個分頁或視窗瀏覽同一個網站，這些分頁或視窗的 `sessionStorage` 是互相獨立的。

- 資料存活時間

    `sessionStorage` 的資料僅在當前的瀏覽器會話中有效。一旦關閉該分頁或視窗，儲存在 `sessionStorage` 中的資料就會被自動清除。因此 `sessionStorage` 特別適合儲存臨時性的資料，例如：表單輸入內容或瀏覽歷史等。

- 儲存容量

    `sessionStorage` 的儲存容量與 `localStorage` 相近，通常也是 5MB 至 10MB。儘管儲存空間較大，但由於其資料存活時間較短，通常是用來儲存較少且短期使用的資料。

- 使用範例

    `sessionStorage` 最常見的使用情境是臨時保存表單資料。假設使用者在填寫表單過程中意外重新整理頁面，使用 `sessionStorage` 可以讓表單內容在重新載入後恢復。

	```javascript
	// 儲存資料至 sessionStorage
	sessionStorage.setItem('formData', JSON.stringify({ name: 'Charmy', age: 28 }));

	// 從 sessionStorage 讀取資料
	const formData = JSON.parse(sessionStorage.getItem('formData'));

	// 刪除 sessionStorage 中的資料
	sessionStorage.removeItem('formData');
	```

<br />

## 總結

| 項目 | Cookie | localStorage | sessionStorage |
| - | - | - | - |
| 儲存範圍 | 與網站的網域與指定路徑綁定，可與伺服器共享 | 與網站網域綁定，在同一瀏覽器內的所有分頁共享 | 與網站網域綁定，但僅在同一瀏覽器分頁中有效 |
| 資料存活時間 | 可設定過期時間，未設定時為瀏覽器關閉即失效 | 除非主動清除，否則永久保存 | 當分頁或瀏覽器關閉後即被清除 |
| 與伺服器溝通 | 每次請求都會自動攜帶，可能造成效能負擔 | 僅儲存在瀏覽器，不會傳送至伺服器 | 僅儲存在瀏覽器，不會傳送至伺服器 |
| 儲存容量限制 | 每個約 4KB，單一網域最多約 20 個 | 約 5MB～10MB | 約 5MB～10MB |
| 資料存取方式 | 可由客戶端與伺服器雙向存取 | 僅能由客戶端 (JavaScript) 存取 | 僅能由客戶端 (JavaScript) 存取 |
| 常見用途 | 儲存登入憑證、用戶 ID 等需伺服器驗證的小型資料 | 儲存使用者偏好、購物車資料、長期快取等 | 儲存表單資料、一次性狀態等暫時性資訊 |
| 設定方式 | `document.cookie` | `localStorage.setItem()`/`getItem()` | `sessionStorage.setItem()`/`getItem()` |
| 安全性 | 可被伺服器與客戶端存取，易受 XSS、CSRF 攻擊 | 僅在瀏覽器中可存取，安全性較高 | 僅在瀏覽器中可存取，安全性較高 |
| 適用場景 | 適合需要與伺服器共享的小量資料 | 適合需長期保存的大量客戶端資料 | 適合儲存短期、會話期間使用的資料 |
