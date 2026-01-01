# Refresh Token

Refresh Token (刷新令牌) 是一種用於管理使用者身份驗證的安全技術，通常與 Access Token (存取令牌) 一起使用，提供更安全的應用程式存取控制。

Refresh Token 是一種令牌，專門用於獲取新的 Access Token。Access Token 是在使用者成功登入後，授予用戶存取應用程式資源的權限令牌，通常具有短期有效性 (例如：1 小時)。當 Access Token 失效時，使用者需要再次登入才能繼續使用應用程式，這是不理想的使用者體驗。

Refresh Token 的引入解決了這個問題。當 Access Token 到期時，應用程式可以使用 Refresh Token 請求新的 Access Token，不需要使用者重新輸入憑證。

<br />

## Refresh Token 的運作流程

1. 使用者登入

    - 使用者輸入帳號和密碼，發送登入請求。

    - 認證伺服器驗證成功後，返回 Access Token 和 Refresh Token。

2. 存取資源

    - 使用者使用 Access Token 訪問受保護的資源，例如：API。

    - 在 Access Token 有效期間，使用者可以正常使用應用程式。

3. Access Token 到期：

    - 當 Access Token 失效時，應用程式會自動檢測到並無法訪問資源。

4. 請求新的 Access Token：

    - 應用程式向認證伺服器發送請求，附上 Refresh Token。

    - 認證伺服器驗證 Refresh Token 是否有效。

5. 返回新的 Access Token

    - 若 Refresh Token 有效，伺服器將返回新的 Access Token。

    - 應用程式可以繼續使用新的 Access Token 訪問資源。

6. 使用新的 Access Token

    - 應用程式使用新的 Access Token 來存取資源，並在下次 Access Token 到期時重複這個過程。

<br />

## Refresh Token 的優缺點

### 優點

- 改善使用者體驗：用戶不需要頻繁登入，能夠在 Access Token 失效後自動獲取新的 Access Token，提供更順暢的使用體驗。

- 提高安全性：Access Token 的有效期設計較短，可以降低被竊取的風險；而 Refresh Token 的有效期較長，能夠保證在用戶持續使用的情況下不必重新驗證。

- 分離權限管理：可以針對 Access Token 和 Refresh Token 設定不同的權限和有效期限，提升安全性與靈活性。

### 缺點

- 安全風險：若 Refresh Token 被竊取，攻擊者可以利用該令牌持續獲取新的 Access Token。因此需要妥善管理 Refresh Token 的儲存與使用。

- 管理複雜性：需要額外處理 Refresh Token 的生成、儲存、更新與過期管理，增加系統的複雜性。

- 失效問題：若 Refresh Token 也設有有效期限，且用戶在過期前未使用，則可能需要重新登入，影響使用者體驗。

<br />

## Refresh Token 的範例

假設有一個簡單的網路應用程式，使用 JWT (JSON Web Token) 作為身份驗證機制。

- 後端 (Node.js Express)

	```javascript
	const express = require('express');
	const jwt = require('jsonwebtoken');
	const bodyParser = require('body-parser');

	const app = express();
	app.use(bodyParser.json());

	const users = {}; // 儲存用戶資料
	const JWT_SECRET = 'your_jwt_secret';
	const REFRESH_TOKEN_SECRET = 'your_refresh_token_secret';
	let refreshTokens = []; // 儲存有效的 Refresh Token

	/** 登入路由 */
	app.post('/login', (req, res) => {
	  const { username, password } = req.body;

	  /** 驗證使用者 (此處省略實際的驗證) */
	  const user = { username };

	  const accessToken = jwt.sign(user, JWT_SECRET, { expiresIn: '1h' });
	  const refreshToken = jwt.sign(user, REFRESH_TOKEN_SECRET);
	  refreshTokens.push(refreshToken); // 儲存 Refresh Token

	  res.json({ accessToken, refreshToken });
	});

	/** 刷新 Access Token 的路由 */
	app.post('/token', (req, res) => {
	  const { token } = req.body;
	  if (!token || !refreshTokens.includes(token)) {
	    return res.sendStatus(403); // 禁止訪問
	  }

	  jwt.verify(token, REFRESH_TOKEN_SECRET, (err, user) => {
	    if (err) return res.sendStatus(403);
	    const accessToken = jwt.sign({ username: user.username }, JWT_SECRET, { 	expiresIn: '1h' });
	    res.json({ accessToken });
	  });
	});

	// 其他路由...

	/** 啟動伺服器 */
	app.listen(3000, () => {
	  console.log('Server is running on port 3000');
	});
	```

- 前端 (JavaScript)

	```javascript
	let accessToken;
	let refreshToken;

	/** 登入函式 */
	async function login(username, password) {
	  const response = await fetch('/login', {
		method: 'POST',
		headers: {
	      'Content-Type': 'application/json',
	    },
	    body: JSON.stringify({ username, password }),
	  });
	  const data = await response.json();
	  accessToken = data.accessToken;
	  refreshToken = data.refreshToken;
	}

	// 使用 Access Token 存取資源
	async function fetchProtectedResource() {
	  const response = await fetch('/protected', {
	    headers: {
	      Authorization: `Bearer ${accessToken}`,
	    },
	  });

	  if (response.status === 403) {
	    /** Access Token 失效，請求新的 Access Token */
	    await refreshAccessToken();
	    return fetchProtectedResource(); // 重試請求
	  }

	  const data = await response.json();
	  console.log(data);
	}

	/** 刷新 Access Token 的函式 */
	async function refreshAccessToken() {
	  const response = await fetch('/token', {
	    method: 'POST',
	    headers: {
	      'Content-Type': 'application/json',
	    },
	    body: JSON.stringify({ token: refreshToken }),
	  });

	  if (response.ok) {
	    const data = await response.json();
	    accessToken = data.accessToken;
	  } else {
	    // Refresh Token 失效，需重新登入
	    console.error('Refresh token is invalid or expired. Please log in again.');
	  }
	}
	```

<br />

## 總結

Refresh Token 是應用程式中身份驗證的重要元件，能有效提升使用者體驗與安全性。透過合理的設計與管理，開發人員可以利用 Refresh Token 實現更加靈活且安全的存取控制方案。在實作過程中，開發人員需要謹慎處理令牌的安全性，確保用戶的資料不受到潛在的威脅。隨著網路安全需求的增加。
