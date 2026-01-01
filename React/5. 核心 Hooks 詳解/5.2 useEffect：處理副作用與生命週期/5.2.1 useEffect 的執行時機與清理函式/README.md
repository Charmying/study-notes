# 5.2.1 `useEffect` 的執行時機與清理函式

<br />

## 基本概念

`useEffect` 是 React 中處理副作用的 Hook，用於執行資料獲取、訂閱、手動 DOM 操作等操作。副作用會在元件渲染完成後執行。

### 1. 基本語法

```jsx
import React, { useState, useEffect } from 'react';

function BasicEffect() {
  const [count, setCount] = useState(0);

  /** 每次渲染後都會執行 */
  useEffect(() => {
    console.log('Effect 執行了');
    document.title = `計數：${count}`;
  });

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  );
}
```

### 2. 執行時機示範

```jsx
function ExecutionTiming() {
  const [count, setCount] = useState(0);

  console.log('1. 元件渲染中');

  useEffect(() => {
    console.log('3. useEffect 執行');
  });

  console.log('2. 元件渲染完成，即將返回 JSX');

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => {
        console.log('4. 按鈕點擊');
        setCount(count + 1);
      }}>
        增加計數
      </button>
    </div>
  );
}
```

<br />

## 依賴陣列控制執行時機

### 1. 無依賴陣列 - 每次渲染都執行

```jsx
function NoDepArray() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  useEffect(() => {
    console.log('每次渲染都執行');
  }); // 沒有依賴陣列

  return (
    <div>
      <p>計數：{count}</p>
      <p>姓名：{name}</p>
      <button onClick={() => setCount(count + 1)}>增加計數</button>
      <input 
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="輸入姓名"
      />
    </div>
  );
}
```

### 2. 空依賴陣列 - 只在掛載時執行一次

```jsx
function EmptyDepArray() {
  const [count, setCount] = useState(0);
  const [data, setData] = useState(null);

  useEffect(() => {
    console.log('只在元件掛載時執行一次');

    /** 模擬 API 呼叫 */
    setTimeout(() => {
      setData('從 API 獲取的資料');
    }, 1000);
  }, []); // 空依賴陣列

  return (
    <div>
      <p>計數：{count}</p>
      <p>資料：{data || '載入中...'}</p>
      <button onClick={() => setCount(count + 1)}>
        增加計數 (不會觸發 effect)
      </button>
    </div>
  );
}
```

### 3. 有依賴的陣列 - 依賴變化時執行

```jsx
function WithDependencies() {
  const [count, setCount] = useState(0);
  const [multiplier, setMultiplier] = useState(1);
  const [result, setResult] = useState(0);

  useEffect(() => {
    console.log('count 或 multiplier 變化時執行');
    setResult(count * multiplier);
  }, [count, multiplier]); // 依賴 count 和 multiplier

  return (
    <div>
      <p>計數：{count}</p>
      <p>乘數：{multiplier}</p>
      <p>結果：{result}</p>

      <button onClick={() => setCount(count + 1)}>
        增加計數
      </button>
      <button onClick={() => setMultiplier(multiplier + 1)}>
        增加乘數
      </button>
    </div>
  );
}
```

<br />

## 清理函式 (Cleanup Function)

### 1. 基本清理函式

```jsx
function BasicCleanup() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log('Effect 設定');

    /** 返回清理函式 */
    return () => {
      console.log('Effect 清理');
    };
  }, [count]);

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加 (會觸發清理和重新設定)
      </button>
    </div>
  );
}
```

### 2. 定時器清理

```jsx
function TimerCleanup() {
  const [count, setCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let interval = null;

    if (isRunning) {
      console.log('啟動定時器');
      interval = setInterval(() => {
        setCount(prevCount => prevCount + 1);
      }, 1000);
    }

    /** 清理函式 */
    return () => {
      if (interval) {
        console.log('清理定時器');
        clearInterval(interval);
      }
    };
  }, [isRunning]);

  return (
    <div>
      <p>計數：{count}</p>
      <p>狀態：{isRunning ? '運行中' : '已停止'}</p>

      <button onClick={() => setIsRunning(!isRunning)}>
        {isRunning ? '停止' : '開始'}
      </button>
      <button onClick={() => setCount(0)}>
        重設計數
      </button>
    </div>
  );
}
```

### 3. 事件監聽器清理

```jsx
function EventListenerCleanup() {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    console.log('添加事件監聽器');
    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);

    /** 清理事件監聽器 */
    return () => {
      console.log('移除事件監聽器');
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []); // 只在掛載和卸載時執行

  return (
    <div>
      <p>視窗寬度：{windowWidth}px</p>
      <p>滑鼠位置：({mousePosition.x}, {mousePosition.y})</p>
    </div>
  );
}
```

### 4. API 請求取消

```jsx
function APIRequestCleanup() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userId, setUserId] = useState(1);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchUserData = async () => {
      setLoading(true);
      setError(null);

      try {
        console.log(`開始獲取使用者 ${userId} 的資料`);

        const response = await fetch(`/api/users/${userId}`, {
          signal: abortController.signal
        });

        if (!response.ok) {
          throw new Error('獲取資料失敗');
        }

        const userData = await response.json();
        setData(userData);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();

    /** 清理函式：取消請求 */
    return () => {
      console.log(`取消使用者 ${userId} 的請求`);
      abortController.abort();
    };
  }, [userId]);

  return (
    <div>
      <div>
        <label>使用者 ID：</label>
        <input 
          type="number"
          value={userId}
          onChange={(e) => setUserId(Number(e.target.value))}
          min="1"
        />
      </div>

      {loading && <p>載入中...</p>}
      {error && <p>錯誤：{error}</p>}
      {data && (
        <div>
          <h3>使用者資料：</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

<br />

## 多個 `useEffect` 的執行順序

### 1. 多個 Effect 的執行順序

```jsx
function MultipleEffects() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log('Effect 1: 每次渲染');
  });

  useEffect(() => {
    console.log('Effect 2: 只在掛載時');
  }, []);

  useEffect(() => {
    console.log('Effect 3: count 變化時');

    return () => {
      console.log('Effect 3 清理');
    };
  }, [count]);

  useEffect(() => {
    console.log('Effect 4: 每次渲染');

    return () => {
      console.log('Effect 4 清理');
    };
  });

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加計數
      </button>
    </div>
  );
}
```

### 2. 條件式 Effect

```jsx
function ConditionalEffects() {
  const [isVisible, setIsVisible] = useState(true);
  const [count, setCount] = useState(0);

  /** 條件式 Effect */
  useEffect(() => {
    if (isVisible) {
      console.log('元件可見時的 Effect');

      return () => {
        console.log('元件隱藏時的清理');
      };
    }
  }, [isVisible]);

  /** 另一個 Effect */
  useEffect(() => {
    console.log('計數變化:', count);
  }, [count]);

  if (!isVisible) {
    return (
      <div>
        <button onClick={() => setIsVisible(true)}>
          顯示元件
        </button>
      </div>
    );
  }

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加計數
      </button>
      <button onClick={() => setIsVisible(false)}>
        隱藏元件
      </button>
    </div>
  );
}
```

<br />

## 實際應用範例

### 1. 資料獲取與載入狀態

```jsx
function DataFetching() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/posts?page=${page}`);
        if (!response.ok) {
          throw new Error('獲取文章失敗');
        }

        const data = await response.json();
        setPosts(data.posts);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [page]);

  if (loading) return <div>載入中...</div>;
  if (error) return <div>錯誤：{error}</div>;

  return (
    <div>
      <h2>文章列表 (第 {page} 頁)</h2>

      <div>
        <button 
          onClick={() => setPage(page - 1)}
          disabled={page <= 1}
        >
          上一頁
        </button>
        <span> 第 {page} 頁 </span>
        <button onClick={() => setPage(page + 1)}>
          下一頁
        </button>
      </div>

      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 2. 即時聊天功能

```jsx
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  useEffect(() => {
    if (!roomId) return;

    console.log(`連接到聊天室：${roomId}`);
    setConnectionStatus('connecting');

    /** 模擬 WebSocket 連接 */
    const ws = new WebSocket(`ws://localhost:8080/chat/${roomId}`);

    ws.onopen = () => {
      console.log('WebSocket 連接已建立');
      setConnectionStatus('connected');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    ws.onclose = () => {
      console.log('WebSocket 連接已關閉');
      setConnectionStatus('disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket 錯誤:', error);
      setConnectionStatus('error');
    };

    /** 清理函式：關閉 WebSocket 連接 */
    return () => {
      console.log(`斷開聊天室連接：${roomId}`);
      ws.close();
    };
  }, [roomId]);

  return (
    <div>
      <div>
        <h3>聊天室：{roomId}</h3>
        <p>連接狀態：{connectionStatus}</p>
      </div>

      <div style={{ height: '300px', overflow: 'auto', border: '1px solid #ccc' }}>
        {messages.map((message, index) => (
          <div key={index}>
            <strong>{message.user}:</strong> {message.text}
          </div>
        ))}
      </div>
    </div>
  );
}

function ChatApp() {
  const [currentRoom, setCurrentRoom] = useState('general');

  return (
    <div>
      <div>
        <button onClick={() => setCurrentRoom('general')}>
          一般聊天室
        </button>
        <button onClick={() => setCurrentRoom('tech')}>
          技術聊天室
        </button>
        <button onClick={() => setCurrentRoom('random')}>
          隨機聊天室
        </button>
      </div>

      <ChatRoom roomId={currentRoom} />
    </div>
  );
}
```

### 3. 本地儲存同步

```jsx
function LocalStorageSync() {
  const [settings, setSettings] = useState({
    theme: 'light',
    language: 'zh-TW',
    notifications: true
  });

  /** 從 localStorage 載入設定 */
  useEffect(() => {
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings);
        setSettings(parsed);
        console.log('從 localStorage 載入設定');
      } catch (error) {
        console.error('解析儲存的設定失敗:', error);
      }
    }
  }, []);

  /** 儲存設定到 localStorage */
  useEffect(() => {
    localStorage.setItem('userSettings', JSON.stringify(settings));
    console.log('設定已儲存到 localStorage');
  }, [settings]);

  const updateSetting = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div>
      <h3>使用者設定</h3>

      <div>
        <label>主題：</label>
        <select 
          value={settings.theme}
          onChange={(e) => updateSetting('theme', e.target.value)}
        >
          <option value="light">淺色</option>
          <option value="dark">深色</option>
        </select>
      </div>

      <div>
        <label>語言：</label>
        <select 
          value={settings.language}
          onChange={(e) => updateSetting('language', e.target.value)}
        >
          <option value="zh-TW">繁體中文</option>
          <option value="en-US">English</option>
          <option value="ja-JP">日本語</option>
        </select>
      </div>

      <div>
        <label>
          <input 
            type="checkbox"
            checked={settings.notifications}
            onChange={(e) => updateSetting('notifications', e.target.checked)}
          />
          啟用通知
        </label>
      </div>

      <div>
        <h4>目前設定：</h4>
        <pre>{JSON.stringify(settings, null, 2)}</pre>
      </div>
    </div>
  );
}
```

<br />

## 常見錯誤與最佳實務

### 1. 忘記清理副作用

```jsx
function MemoryLeakExample() {
  const [data, setData] = useState(null);

  useEffect(() => {
    /** ❌ 錯誤：沒有清理定時器 */
    const timer = setInterval(() => {
      console.log('定時器執行中...');
    }, 1000);

    // 忘記返回清理函式會導致記憶體洩漏
  }, []);

  /** // ✅ 正確的做法 */
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('定時器執行中...');
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  return <div>檢查控制台的定時器輸出</div>;
}
```

### 2. 依賴陣列遺漏

```jsx
function MissingDependency() {
  const [count, setCount] = useState(0);
  const [multiplier, setMultiplier] = useState(2);

  /** ❌ 錯誤：遺漏 multiplier 依賴 */
  useEffect(() => {
    const result = count * multiplier;
    console.log('結果:', result);
  }, [count]); // 應該包含 multiplier

  /** ✅ 正確：包含所有依賴 */
  useEffect(() => {
    const result = count * multiplier;
    console.log('結果:', result);
  }, [count, multiplier]);

  return (
    <div>
      <p>計數：{count}</p>
      <p>乘數：{multiplier}</p>
      <button onClick={() => setCount(count + 1)}>增加計數</button>
      <button onClick={() => setMultiplier(multiplier + 1)}>增加乘數</button>
    </div>
  );
}
```

<br />

## 最佳實務總結

### 1. 執行時機控制

- 無依賴陣列：每次渲染後執行

- 空依賴陣列：只在掛載時執行一次

- 有依賴陣列：依賴變化時執行

### 2. 清理函式使用

- 定時器：使用 `clearInterval` 或 `clearTimeout`

- 事件監聽器：使用 `removeEventListener`

- API 請求：使用 `AbortController` 取消請求

- 訂閱：取消訂閱以避免記憶體洩漏

### 3. 依賴陣列管理

- 包含所有依賴：避免過時的閉包問題

- 使用 ESLint 規則：`react-hooks/exhaustive-deps`

- 函式依賴：使用 `useCallback` 穩定函式參考

### 4. 效能考量

- 避免不必要的執行：正確設定依賴陣列

- 分離關注點：不同的副作用使用不同的 `useEffect`

- 條件執行：在 Effect 內部使用條件判斷
