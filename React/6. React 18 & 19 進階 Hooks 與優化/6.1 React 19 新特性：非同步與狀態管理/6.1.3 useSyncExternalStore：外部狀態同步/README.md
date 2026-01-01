# 6.1.3 `useSyncExternalStore`：外部狀態同步

<br />

## 概述

`useSyncExternalStore` 是 React 18 引入的 Hook，用於與外部狀態管理庫同步。這個 Hook 解決了在並行渲染環境下外部狀態可能導致的不一致性問題，確保元件能夠安全訂閱外部資料來源。

<br />

## 基本語法

```jsx
const snapshot = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)
```

### 參數說明

- `subscribe`: 訂閱函式，接收一個回調函式並回傳取消訂閱函式

- `getSnapshot`: 取得當前狀態快照的函式

- `getServerSnapshot`: (可選) 伺服器端渲染時使用的快照函式

<br />

## 基本範例

### 簡單的外部 Store

```jsx
/** 外部狀態 store */
class CounterStore {
  constructor() {
    this.count = 0;
    this.listeners = new Set();
  }

  getSnapshot = () => {
    return this.count;
  };

  subscribe = (listener) => {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  };

  increment = () => {
    this.count++;
    this.emitChange();
  };

  decrement = () => {
    this.count--;
    this.emitChange();
  };

  emitChange = () => {
    this.listeners.forEach(listener => listener());
  };
}

const counterStore = new CounterStore();
```

### React 元件使用

```jsx
import { useSyncExternalStore } from 'react';

function Counter() {
  const count = useSyncExternalStore(
    counterStore.subscribe,
    counterStore.getSnapshot
  );

  return (
    <div>
      <p>計數: {count}</p>
      <button onClick={counterStore.increment}>+1</button>
      <button onClick={counterStore.decrement}>-1</button>
    </div>
  );
}
```

<br />

## 實際應用範例

### 瀏覽器 API 整合

```jsx
/** 視窗尺寸 hook */
function useWindowSize() {
  const subscribe = (callback) => {
    window.addEventListener('resize', callback);
    return () => window.removeEventListener('resize', callback);
  };

  const getSnapshot = () => {
    return {
      width: window.innerWidth,
      height: window.innerHeight
    };
  };

  const getServerSnapshot = () => {
    return {
      width: 1024,
      height: 768
    };
  };

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

function ResponsiveComponent() {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>視窗尺寸: {width} x {height}</p>
      {width < 768 ? <MobileView /> : <DesktopView />}
    </div>
  );
}
```

### 網路狀態監控

```jsx
function useOnlineStatus() {
  const subscribe = (callback) => {
    window.addEventListener('online', callback);
    window.addEventListener('offline', callback);

    return () => {
      window.removeEventListener('online', callback);
      window.removeEventListener('offline', callback);
    };
  };

  const getSnapshot = () => navigator.onLine;
  const getServerSnapshot = () => true;

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}

function NetworkStatus() {
  const isOnline = useOnlineStatus();

  return (
    <div>
      <p>網路狀態: {isOnline ? '已連線' : '離線'}</p>
      {!isOnline && <div>請檢查網路連線</div>}
    </div>
  );
}
```

### localStorage 同步

```jsx
function useLocalStorage(key, defaultValue) {
  const subscribe = (callback) => {
    const handleStorageChange = (e) => {
      if (e.key === key) {
        callback();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  };

  const getSnapshot = () => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  };

  const getServerSnapshot = () => defaultValue;

  const value = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  const setValue = (newValue) => {
    try {
      localStorage.setItem(key, JSON.stringify(newValue));
      /** 手動觸發 storage 事件 */
      window.dispatchEvent(new StorageEvent('storage', {
        key,
        newValue: JSON.stringify(newValue)
      }));
    } catch (error) {
      console.error('無法儲存到 localStorage:', error);
    }
  };

  return [value, setValue];
}

function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'zh-TW');

  return (
    <div>
      <h2>設定</h2>
      <div>
        <label>
          主題: 
          <select value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option value="light">明亮</option>
            <option value="dark">暗黑</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          語言: 
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="zh-TW">繁體中文</option>
            <option value="en">English</option>
          </select>
        </label>
      </div>
    </div>
  );
}
```

<br />

## 與狀態管理庫整合

### Redux 整合

```jsx
import { createStore } from 'redux';

/** Redux store */
const initialState = { count: 0 };

function counterReducer(state = initialState, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

const store = createStore(counterReducer);

/** React Hook */
function useReduxStore(selector) {
  const subscribe = (callback) => {
    return store.subscribe(callback);
  };

  const getSnapshot = () => {
    return selector(store.getState());
  };

  return useSyncExternalStore(subscribe, getSnapshot);
}

function ReduxCounter() {
  const count = useReduxStore(state => state.count);

  return (
    <div>
      <p>計數: {count}</p>
      <button onClick={() => store.dispatch({ type: 'INCREMENT' })}>+1</button>
      <button onClick={() => store.dispatch({ type: 'DECREMENT' })}>-1</button>
    </div>
  );
}
```

### Zustand 整合

```jsx
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 }))
}));

/** 使用 useSyncExternalStore 與 Zustand 整合 */
function useZustandSync(selector) {
  const subscribe = (callback) => {
    return useStore.subscribe(callback);
  };

  const getSnapshot = () => {
    return selector(useStore.getState());
  };

  return useSyncExternalStore(subscribe, getSnapshot);
}

function ZustandCounter() {
  const count = useZustandSync(state => state.count);
  const { increment, decrement } = useStore();

  return (
    <div>
      <p>計數: {count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
    </div>
  );
}
```

<br />

## 進階範例

### 複雜狀態管理

```jsx
class TodoStore {
  constructor() {
    this.todos = [];
    this.filter = 'all';
    this.listeners = new Set();
  }

  subscribe = (listener) => {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  };

  getSnapshot = () => {
    return {
      todos: this.todos,
      filter: this.filter,
      filteredTodos: this.getFilteredTodos()
    };
  };

  addTodo = (text) => {
    this.todos.push({
      id: Date.now(),
      text,
      completed: false
    });
    this.emitChange();
  };

  toggleTodo = (id) => {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      this.emitChange();
    }
  };

  setFilter = (filter) => {
    this.filter = filter;
    this.emitChange();
  };

  getFilteredTodos = () => {
    switch (this.filter) {
      case 'active':
        return this.todos.filter(todo => !todo.completed);
      case 'completed':
        return this.todos.filter(todo => todo.completed);
      default:
        return this.todos;
    }
  };

  emitChange = () => {
    this.listeners.forEach(listener => listener());
  };
}

const todoStore = new TodoStore();

function TodoApp() {
  const { filteredTodos, filter } = useSyncExternalStore(
    todoStore.subscribe,
    todoStore.getSnapshot
  );

  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      todoStore.addTodo(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="新增任務"
        />
        <button type="submit">新增</button>
      </form>

      <div>
        <button 
          onClick={() => todoStore.setFilter('all')}
          className={filter === 'all' ? 'active' : ''}
        >
          全部
        </button>
        <button 
          onClick={() => todoStore.setFilter('active')}
          className={filter === 'active' ? 'active' : ''}
        >
          進行中
        </button>
        <button 
          onClick={() => todoStore.setFilter('completed')}
          className={filter === 'completed' ? 'active' : ''}
        >
          已完成
        </button>
      </div>

      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => todoStore.toggleTodo(todo.id)}
            />
            <span className={todo.completed ? 'completed' : ''}>
              {todo.text}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 即時資料同步

```jsx
class WebSocketStore {
  constructor(url) {
    this.url = url;
    this.data = null;
    this.status = 'disconnected';
    this.listeners = new Set();
    this.ws = null;
  }

  connect = () => {
    if (this.ws) return;

    this.ws = new WebSocket(this.url);
    this.status = 'connecting';
    this.emitChange();

    this.ws.onopen = () => {
      this.status = 'connected';
      this.emitChange();
    };

    this.ws.onmessage = (event) => {
      this.data = JSON.parse(event.data);
      this.emitChange();
    };

    this.ws.onclose = () => {
      this.status = 'disconnected';
      this.ws = null;
      this.emitChange();
    };
  };

  disconnect = () => {
    if (this.ws) {
      this.ws.close();
    }
  };

  subscribe = (listener) => {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  };

  getSnapshot = () => {
    return {
      data: this.data,
      status: this.status
    };
  };

  emitChange = () => {
    this.listeners.forEach(listener => listener());
  };
}

function useWebSocket(url) {
  const [store] = useState(() => new WebSocketStore(url));

  const { data, status } = useSyncExternalStore(
    store.subscribe,
    store.getSnapshot
  );

  useEffect(() => {
    store.connect();
    return () => store.disconnect();
  }, [store]);

  return { data, status };
}

function LiveData() {
  const { data, status } = useWebSocket('ws://localhost:8080');

  return (
    <div>
      <p>連線狀態: {status}</p>
      {status === 'connected' && data && (
        <div>
          <h3>即時資料:</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

<br />

## 最佳實踐

### 1. 穩定的快照

```jsx
/** ❌ 不穩定：每次都建立新物件 */
function BadExample() {
  const data = useSyncExternalStore(
    store.subscribe,
    () => ({ value: store.getValue() }) // 每次都是新物件
  );
  return <div>{data.value}</div>;
}

/** ✅ 穩定：使用緩存或穩定的參考 */
function GoodExample() {
  const value = useSyncExternalStore(
    store.subscribe,
    store.getValue // 穩定的函式參考
  );
  return <div>{value}</div>;
}
```

### 2. 錯誤處理

```jsx
function SafeExternalStore() {
  const subscribe = (callback) => {
    try {
      return externalStore.subscribe(callback);
    } catch (error) {
      console.error('訂閱失敗:', error);
      return () => {}; // 回傳空的取消函式
    }
  };

  const getSnapshot = () => {
    try {
      return externalStore.getState();
    } catch (error) {
      console.error('取得狀態失敗:', error);
      return null; // 回傳預設值
    }
  };

  return useSyncExternalStore(subscribe, getSnapshot);
}
```

### 3. 效能優化

```jsx
/** 使用 selector 避免不必要的重新渲染 */
function useStoreSelector(selector) {
  const subscribe = useCallback((callback) => {
    return store.subscribe(callback);
  }, []);

  const getSnapshot = useCallback(() => {
    return selector(store.getState());
  }, [selector]);

  return useSyncExternalStore(subscribe, getSnapshot);
}

function OptimizedComponent() {
  /** 只當 count 改變時才重新渲染 */
  const count = useStoreSelector(state => state.count);

  return <div>{count}</div>;
}
```

<br />

## 注意事項

### 1. 伺服器端渲染

```jsx
/** 必須提供 getServerSnapshot 以支援 SSR */
function useClientOnlyStore() {
  const subscribe = (callback) => {
    /** 在伺服器端不執行 */
    if (typeof window === 'undefined') {
      return () => {};
    }
    return clientStore.subscribe(callback);
  };

  const getSnapshot = () => {
    if (typeof window === 'undefined') {
      return null;
    }
    return clientStore.getState();
  };

  const getServerSnapshot = () => null;

  return useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
}
```

### 2. 記憶體洩漏預防

```jsx
function useExternalStoreWithCleanup() {
  const subscribe = useCallback((callback) => {
    const unsubscribe = externalStore.subscribe(callback);

    /** 確保清理資源 */
    return () => {
      if (typeof unsubscribe === 'function') {
        unsubscribe();
      }
    };
  }, []);

  const getSnapshot = useCallback(() => {
    return externalStore.getState();
  }, []);

  return useSyncExternalStore(subscribe, getSnapshot);
}
```

<br />

## 總結

### 主要優勢

- 並行渲染安全：避免狀態不一致性問題

- 外部整合：與任何外部狀態管理庫整合

- SSR 支援：提供伺服器端渲染支援

- 效能優化：只在狀態改變時重新渲染

### 適用場景

- 與 Redux、Zustand 等狀態管理庫整合

- 瀏覽器 API (例如：localStorage、視窗尺寸)

- WebSocket 或其他即時資料來源

- 第三方庫的狀態同步

### 使用建議

- 確保 `getSnapshot` 回傳穩定的參考

- 提供適當的 `getServerSnapshot` 以支援 SSR

- 正確處理訂閱和取消訂閱

- 使用 `selector` 優化效能

- 注意錯誤處理和資源清理

`useSyncExternalStore` 是 React 與外部狀態系統整合的標準方式，特別適合在並行渲染環境下使用。
