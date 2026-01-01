# 5.2.3 資料撈取、事件訂閱與手動 DOM 操作

<br />

## 資料撈取 (Data Fetching)

### 1. 基本 API 資料撈取

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const userData = await response.json();
        setUser(userData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUser();
    }
  }, [userId]);

  if (loading) return <div>載入中...</div>;
  if (error) return <div>錯誤：{error}</div>;
  if (!user) return <div>找不到使用者</div>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>Email：{user.email}</p>
      <p>註冊日期：{user.createdAt}</p>
    </div>
  );
}
```

### 2. 取消請求避免記憶體洩漏

```jsx
function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchPosts = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch('/api/posts', {
          signal: abortController.signal
        });

        if (!response.ok) {
          throw new Error('獲取文章失敗');
        }

        const data = await response.json();
        setPosts(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();

    return () => {
      abortController.abort();
    };
  }, []);

  return (
    <div>
      {loading && <p>載入文章中...</p>}
      {error && <p>錯誤：{error}</p>}
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

### 3. 分頁資料撈取

```jsx
function PaginatedPosts() {
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/posts?page=${currentPage}&limit=10`);
        const data = await response.json();

        setPosts(data.posts);
        setTotalPages(data.totalPages);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [currentPage]);

  const goToPage = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  return (
    <div>
      {loading && <p>載入中...</p>}
      {error && <p>錯誤：{error}</p>}

      <ul>
        {posts.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>

      <div>
        <button 
          onClick={() => goToPage(currentPage - 1)}
          disabled={currentPage <= 1}
        >
          上一頁
        </button>

        <span>第 {currentPage} 頁，共 {totalPages} 頁</span>

        <button 
          onClick={() => goToPage(currentPage + 1)}
          disabled={currentPage >= totalPages}
        >
          下一頁
        </button>
      </div>
    </div>
  );
}
```

### 4. 搜尋與過濾

```jsx
function SearchablePosts() {
  const [posts, setPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const abortController = new AbortController();

    const searchPosts = async () => {
      if (!searchTerm.trim() && category === 'all') {
        setPosts([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const params = new URLSearchParams();
        if (searchTerm.trim()) params.append('search', searchTerm);
        if (category !== 'all') params.append('category', category);

        const response = await fetch(`/api/posts/search?${params}`, {
          signal: abortController.signal
        });

        const data = await response.json();
        setPosts(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    const timeoutId = setTimeout(searchPosts, 300); // 防抖

    return () => {
      clearTimeout(timeoutId);
      abortController.abort();
    };
  }, [searchTerm, category]);

  return (
    <div>
      <div>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="搜尋文章..."
        />

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="all">所有分類</option>
          <option value="tech">技術</option>
          <option value="design">設計</option>
          <option value="business">商業</option>
        </select>
      </div>

      {loading && <p>搜尋中...</p>}
      {error && <p>錯誤：{error}</p>}

      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <span>分類：{post.category}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 事件訂閱 (Event Subscription)

### 1. 視窗事件監聽

```jsx
function WindowEvents() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });
  const [scrollY, setScrollY] = useState(window.scrollY);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('resize', handleResize);
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return (
    <div>
      <p>視窗大小：{windowSize.width} x {windowSize.height}</p>
      <p>捲動位置：{scrollY}px</p>
      <p>網路狀態：{isOnline ? '線上' : '離線'}</p>
    </div>
  );
}
```

### 2. 鍵盤事件處理

```jsx
function KeyboardShortcuts() {
  const [pressedKeys, setPressedKeys] = useState(new Set());
  const [lastKeyPressed, setLastKeyPressed] = useState('');

  useEffect(() => {
    const handleKeyDown = (e) => {
      setPressedKeys(prev => new Set([...prev, e.key]));
      setLastKeyPressed(e.key);

      /** 快捷鍵處理 */
      if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        console.log('儲存快捷鍵觸發');
      }

      if (e.key === 'Escape') {
        console.log('ESC 鍵按下');
      }
    };

    const handleKeyUp = (e) => {
      setPressedKeys(prev => {
        const newSet = new Set(prev);
        newSet.delete(e.key);
        return newSet;
      });
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  return (
    <div>
      <p>最後按下的鍵：{lastKeyPressed}</p>
      <p>目前按住的鍵：{Array.from(pressedKeys).join(', ')}</p>
      <p>提示：按 Ctrl+S 或 ESC 試試看</p>
    </div>
  );
}
```

### 3. WebSocket 連接

```jsx
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [newMessage, setNewMessage] = useState('');
  const wsRef = useRef(null);

  useEffect(() => {
    if (!roomId) return;

    const ws = new WebSocket(`ws://localhost:8080/chat/${roomId}`);
    wsRef.current = ws;

    setConnectionStatus('connecting');

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

    return () => {
      ws.close();
    };
  }, [roomId]);

  const sendMessage = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN && newMessage.trim()) {
      const message = {
        text: newMessage,
        timestamp: new Date().toISOString(),
        user: 'current-user'
      };

      wsRef.current.send(JSON.stringify(message));
      setNewMessage('');
    }
  };

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
            <small> ({new Date(message.timestamp).toLocaleTimeString()})</small>
          </div>
        ))}
      </div>

      <div>
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="輸入訊息..."
          disabled={connectionStatus !== 'connected'}
        />
        <button 
          onClick={sendMessage}
          disabled={connectionStatus !== 'connected'}
        >
          送出
        </button>
      </div>
    </div>
  );
}
```

### 4. 自定義事件系統

```jsx
/** 事件發射器 */
class EventEmitter {
  constructor() {
    this.events = {};
  }

  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  }

  off(event, callback) {
    if (this.events[event]) {
      this.events[event] = this.events[event].filter(cb => cb !== callback);
    }
  }

  emit(event, data) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
  }
}

const eventBus = new EventEmitter();

function NotificationPublisher() {
  const [message, setMessage] = useState('');

  const publishNotification = () => {
    if (message.trim()) {
      eventBus.emit('notification', {
        id: Date.now(),
        message,
        type: 'info',
        timestamp: new Date().toISOString()
      });
      setMessage('');
    }
  };

  return (
    <div>
      <h3>發布通知</h3>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="輸入通知訊息"
      />
      <button onClick={publishNotification}>發布</button>
    </div>
  );
}

function NotificationSubscriber() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const handleNotification = (notification) => {
      setNotifications(prev => [...prev, notification]);

      /** 3 秒後自動移除 */
      setTimeout(() => {
        setNotifications(prev => prev.filter(n => n.id !== notification.id));
      }, 3000);
    };

    eventBus.on('notification', handleNotification);

    return () => {
      eventBus.off('notification', handleNotification);
    };
  }, []);

  return (
    <div>
      <h3>通知列表</h3>
      {notifications.map(notification => (
        <div key={notification.id} style={{ 
          padding: '10px', 
          margin: '5px', 
          backgroundColor: '#f0f0f0' 
        }}>
          {notification.message}
          <small> ({new Date(notification.timestamp).toLocaleTimeString()})</small>
        </div>
      ))}
    </div>
  );
}
```

<br />

## 手動 DOM 操作

### 1. 焦點管理

```jsx
function FocusManagement() {
  const inputRef = useRef(null);
  const buttonRef = useRef(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const modalRef = useRef(null);

  /** 元件掛載時聚焦到輸入框 */
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  /** 模態框開啟時管理焦點 */
  useEffect(() => {
    if (isModalOpen && modalRef.current) {
      const focusableElements = modalRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      }

      const handleKeyDown = (e) => {
        if (e.key === 'Escape') {
          setIsModalOpen(false);
        }

        /** Tab 鍵循環焦點 */
        if (e.key === 'Tab') {
          const firstElement = focusableElements[0];
          const lastElement = focusableElements[focusableElements.length - 1];

          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      };

      document.addEventListener('keydown', handleKeyDown);

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isModalOpen]);

  return (
    <div>
      <input 
        ref={inputRef}
        placeholder="自動聚焦的輸入框"
      />

      <button onClick={() => setIsModalOpen(true)}>
        開啟模態框
      </button>

      {isModalOpen && (
        <div 
          ref={modalRef}
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: 'white',
            padding: '20px',
            border: '1px solid #ccc',
            zIndex: 1000
          }}
        >
          <h3>模態框</h3>
          <input placeholder="模態框內的輸入" />
          <div>
            <button onClick={() => setIsModalOpen(false)}>關閉</button>
            <button>確認</button>
          </div>
        </div>
      )}

      {isModalOpen && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            zIndex: 999
          }}
          onClick={() => setIsModalOpen(false)}
        />
      )}
    </div>
  );
}
```

### 2. 滾動控制

```jsx
function ScrollControl() {
  const [isScrollLocked, setIsScrollLocked] = useState(false);
  const scrollPositionRef = useRef(0);
  const contentRef = useRef(null);

  /** 鎖定/解鎖頁面滾動 */
  useEffect(() => {
    if (isScrollLocked) {
      scrollPositionRef.current = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.top = `-${scrollPositionRef.current}px`;
      document.body.style.width = '100%';
    } else {
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, scrollPositionRef.current);
    }

    return () => {
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
    };
  }, [isScrollLocked]);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToElement = () => {
    if (contentRef.current) {
      contentRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'center'
      });
    }
  };

  return (
    <div>
      <div style={{ height: '200vh', padding: '20px' }}>
        <h2>滾動控制範例</h2>

        <div>
          <button onClick={() => setIsScrollLocked(!isScrollLocked)}>
            {isScrollLocked ? '解鎖滾動' : '鎖定滾動'}
          </button>
          <button onClick={scrollToTop}>回到頂部</button>
          <button onClick={scrollToElement}>滾動到內容</button>
        </div>

        <div style={{ marginTop: '100vh' }} ref={contentRef}>
          <h3>目標內容區域</h3>
          <p>這是要滾動到的內容</p>
        </div>

        <div style={{ marginTop: '50vh' }}>
          <p>頁面底部內容</p>
        </div>
      </div>
    </div>
  );
}
```

### 3. 動態樣式操作

```jsx
function DynamicStyling() {
  const elementRef = useRef(null);
  const [animationState, setAnimationState] = useState('idle');

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    switch (animationState) {
      case 'fadeIn':
        element.style.opacity = '0';
        element.style.transition = 'opacity 0.5s ease';

        requestAnimationFrame(() => {
          element.style.opacity = '1';
        });

        const fadeInTimer = setTimeout(() => {
          setAnimationState('idle');
        }, 500);

        return () => clearTimeout(fadeInTimer);

      case 'slideIn':
        element.style.transform = 'translateX(-100%)';
        element.style.transition = 'transform 0.3s ease';

        requestAnimationFrame(() => {
          element.style.transform = 'translateX(0)';
        });

        const slideInTimer = setTimeout(() => {
          setAnimationState('idle');
        }, 300);

        return () => clearTimeout(slideInTimer);

      case 'bounce':
        element.style.animation = 'bounce 0.6s ease';

        const bounceTimer = setTimeout(() => {
          element.style.animation = '';
          setAnimationState('idle');
        }, 600);

        return () => clearTimeout(bounceTimer);

      default:
        element.style.opacity = '';
        element.style.transform = '';
        element.style.transition = '';
        element.style.animation = '';
    }
  }, [animationState]);

  /** 添加 CSS 動畫 */
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes bounce {
        0%, 20%, 53%, 80%, 100% {
          transform: translate3d(0,0,0);
        }
        40%, 43% {
          transform: translate3d(0,-30px,0);
        }
        70% {
          transform: translate3d(0,-15px,0);
        }
        90% {
          transform: translate3d(0,-4px,0);
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div>
      <div>
        <button onClick={() => setAnimationState('fadeIn')}>
          淡入動畫
        </button>
        <button onClick={() => setAnimationState('slideIn')}>
          滑入動畫
        </button>
        <button onClick={() => setAnimationState('bounce')}>
          彈跳動畫
        </button>
      </div>

      <div 
        ref={elementRef}
        style={{
          width: '200px',
          height: '100px',
          backgroundColor: '#007bff',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '20px 0',
          borderRadius: '8px'
        }}
      >
        動畫元素
      </div>

      <p>目前狀態：{animationState}</p>
    </div>
  );
}
```

### 4. 第三方庫整合

```jsx
function ThirdPartyIntegration() {
  const chartRef = useRef(null);
  const mapRef = useRef(null);
  const chartInstanceRef = useRef(null);

  /** 圖表庫整合 (例如：Chart.js) */
  useEffect(() => {
    if (chartRef.current) {
      /** 模擬圖表庫初始化 */
      const initChart = () => {
        console.log('初始化圖表');
        // const chart = new Chart(chartRef.current, config);
        // chartInstanceRef.current = chart;
      };

      initChart();

      return () => {
        if (chartInstanceRef.current) {
          console.log('銷毀圖表');
          // chartInstanceRef.current.destroy();
        }
      };
    }
  }, []);

  /** 地圖庫整合 (例如：Google Maps) */
  useEffect(() => {
    if (mapRef.current) {
      const initMap = () => {
        console.log('初始化地圖');
        // const map = new google.maps.Map(mapRef.current, options);
      };

      /** 檢查第三方庫是否已載入 */
      if (window.google && window.google.maps) {
        initMap();
      } else {
        /** 動態載入第三方庫 */
        const script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY';
        script.onload = initMap;
        document.head.appendChild(script);

        return () => {
          document.head.removeChild(script);
        };
      }
    }
  }, []);

  return (
    <div>
      <h3>第三方庫整合範例</h3>

      <div>
        <h4>圖表區域</h4>
        <canvas 
          ref={chartRef}
          width="400" 
          height="200"
          style={{ border: '1px solid #ccc' }}
        />
      </div>

      <div>
        <h4>地圖區域</h4>
        <div 
          ref={mapRef}
          style={{ 
            width: '400px', 
            height: '300px', 
            backgroundColor: '#f0f0f0',
            border: '1px solid #ccc'
          }}
        />
      </div>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 資料撈取最佳實務

- 使用 `AbortController`：取消不需要的請求

- 錯誤處理：提供清楚的錯誤訊息

- 載入狀態：顯示適當的載入指示器

- 快取策略：避免重複請求相同資料

### 2. 事件訂閱最佳實務

- 清理監聽器：避免記憶體洩漏

- 防抖與節流：控制事件觸發頻率

- 事件委派：減少監聽器數量

- 被動監聽器：提升滾動效能

### 3. DOM 操作最佳實務

- 最小化 DOM 操作：批次處理變更

- 使用 `ref` 而非 `querySelector`：更好的效能

- 清理副作用：重設樣式和移除監聽器

- 可存取性考量：維護焦點管理和鍵盤導航
