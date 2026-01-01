# 6.1.1 `use()` API：渲染中讀取 Promise 或 Context

<br />

## 概述

`use()` 是 React 19 引入的新 API，允許在元件渲染過程中直接讀取 Promise 或 Context 的值。這個 API 簡化了非同步資料處理和 Context 消費的方式，提供更直觀的程式碼結構。

<br />

## 基本語法

```jsx
const value = use(resource)
```

### 參數說明

- `resource`: Promise 物件或 Context 物件

- 回傳值: Promise 的解析值或 Context 的當前值

<br />

## 使用 Promise

### 基本範例

```jsx
import { use } from 'react';

function UserProfile({ userPromise }) {
  const user = use(userPromise);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}

/** 使用方式 */
function App() {
  const userPromise = fetch('/api/user').then(res => res.json());

  return (
    <Suspense fallback={<div>載入中...</div>}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

### 錯誤處理

```jsx
import { use } from 'react';

function DataComponent({ dataPromise }) {
  try {
    const data = use(dataPromise);
    return <div>{data.content}</div>;
  } catch (error) {
    return <div>載入失敗: {error.message}</div>;
  }
}

/** 使用 Error Boundary */
function App() {
  const dataPromise = fetchData();

  return (
    <ErrorBoundary fallback={<div>發生錯誤</div>}>
      <Suspense fallback={<div>載入中...</div>}>
        <DataComponent dataPromise={dataPromise} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

### 條件式使用

```jsx
function ConditionalData({ shouldLoad, dataPromise }) {
  if (!shouldLoad) {
    return <div>未載入資料</div>;
  }

  const data = use(dataPromise);
  return <div>{data.title}</div>;
}
```

<br />

## 使用 Context

### 基本 Context 使用

```jsx
import { use, createContext } from 'react';

const ThemeContext = createContext();

function Button() {
  const theme = use(ThemeContext);

  return (
    <button 
      style={{ 
        backgroundColor: theme.primary,
        color: theme.text 
      }}
    >
      按鈕
    </button>
  );
}

function App() {
  const theme = {
    primary: '#007bff',
    text: '#ffffff'
  };

  return (
    <ThemeContext.Provider value={theme}>
      <Button />
    </ThemeContext.Provider>
  );
}
```

### 多層 Context

```jsx
const UserContext = createContext();
const SettingsContext = createContext();

function Profile() {
  const user = use(UserContext);
  const settings = use(SettingsContext);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>語言: {settings.language}</p>
      <p>主題: {settings.theme}</p>
    </div>
  );
}
```

<br />

## 實際應用範例

### 資料載入元件

```jsx
function PostList({ postsPromise }) {
  const posts = use(postsPromise);

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.excerpt}</p>
        </li>
      ))}
    </ul>
  );
}

function BlogPage() {
  const postsPromise = fetch('/api/posts').then(res => res.json());

  return (
    <div>
      <h1>部落格文章</h1>
      <Suspense fallback={<div>載入文章中...</div>}>
        <PostList postsPromise={postsPromise} />
      </Suspense>
    </div>
  );
}
```

### 使用者認證

```jsx
const AuthContext = createContext();

function ProtectedContent() {
  const auth = use(AuthContext);

  if (!auth.isAuthenticated) {
    return <div>請先登入</div>;
  }

  return (
    <div>
      <h2>歡迎, {auth.user.name}</h2>
      <p>這是受保護的內容</p>
    </div>
  );
}

function App() {
  const [auth, setAuth] = useState({
    isAuthenticated: false,
    user: null
  });

  return (
    <AuthContext.Provider value={auth}>
      <ProtectedContent />
    </AuthContext.Provider>
  );
}
```

### 組合 Promise 和 Context

```jsx
const ApiContext = createContext();

function UserDashboard({ userPromise }) {
  const api = use(ApiContext);
  const user = use(userPromise);

  const handleUpdate = async () => {
    await api.updateUser(user.id, { lastLogin: new Date() });
  };

  return (
    <div>
      <h1>{user.name} 的儀表板</h1>
      <button onClick={handleUpdate}>更新登入時間</button>
    </div>
  );
}
```

<br />

## 與傳統方法的比較

### 使用 `useEffect` 和 `useState`

```jsx
/** 傳統方法 */
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div>載入中...</div>;
  if (error) return <div>錯誤: {error.message}</div>;

  return <div>{user.name}</div>;
}

/** 使用 use() API */
function UserProfile({ userPromise }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}
```

### 使用 `useContext`

```jsx
/** 傳統方法 */
function Button() {
  const theme = useContext(ThemeContext);
  return <button style={{ color: theme.primary }}>按鈕</button>;
}

/** 使用 use() API */
function Button() {
  const theme = use(ThemeContext);
  return <button style={{ color: theme.primary }}>按鈕</button>;
}
```

<br />

## 注意事項

### 1. 必須在 `Suspense` 邊界內使用

```jsx
/** ❌ 錯誤：沒有 Suspense */
function App() {
  const dataPromise = fetchData();
  return <DataComponent dataPromise={dataPromise} />;
}

/** ✅ 正確：包裹在 Suspense 中 */
function App() {
  const dataPromise = fetchData();
  return (
    <Suspense fallback={<div>載入中...</div>}>
      <DataComponent dataPromise={dataPromise} />
    </Suspense>
  );
}
```

### 2. Promise 應該穩定

```jsx
/** ❌ 錯誤：每次渲染都建立新的 Promise */
function Component() {
  const dataPromise = fetch('/api/data'); // 每次都是新的
  const data = use(dataPromise);
  return <div>{data.content}</div>;
}

/** ✅ 正確：使用穩定的 Promise */
function Component({ dataPromise }) {
  const data = use(dataPromise);
  return <div>{data.content}</div>;
}
```

### 3. 錯誤邊界處理

```jsx
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>發生錯誤</div>;
    }
    return this.props.children;
  }
}
```

<br />

## 最佳實踐

### 1. Promise 快取

```jsx
const promiseCache = new Map();

function getCachedPromise(url) {
  if (!promiseCache.has(url)) {
    promiseCache.set(url, fetch(url).then(res => res.json()));
  }
  return promiseCache.get(url);
}

function DataComponent({ url }) {
  const data = use(getCachedPromise(url));
  return <div>{data.content}</div>;
}
```

### 2. 條件式載入

```jsx
function OptionalData({ shouldLoad, dataPromise }) {
  if (!shouldLoad) {
    return <div>資料未載入</div>;
  }

  const data = use(dataPromise);
  return <div>{data.content}</div>;
}
```

### 3. 組合多個資源

```jsx
function CombinedData({ userPromise, postsPromise }) {
  const user = use(userPromise);
  const posts = use(postsPromise);

  return (
    <div>
      <h1>{user.name} 的文章</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
        </article>
      ))}
    </div>
  );
}
```

<br />

## 效能考量

### Promise 重複使用

```jsx
/** 在父元件中建立 Promise */
function App() {
  const userPromise = useMemo(
    () => fetch('/api/user').then(res => res.json()),
    []
  );

  return (
    <Suspense fallback={<div>載入中...</div>}>
      <UserProfile userPromise={userPromise} />
      <UserSettings userPromise={userPromise} />
    </Suspense>
  );
}
```

### 條件式渲染優化

```jsx
function ConditionalLoader({ condition, dataPromise }) {
  /** 先檢查條件，避免不必要的 Promise 解析 */
  if (!condition) {
    return <div>條件不符合</div>;
  }

  const data = use(dataPromise);
  return <div>{data.content}</div>;
}
```

<br />

## 總結

`use()` API 的主要優勢：

- 簡化程式碼：減少狀態管理的複雜性

- 更好的可讀性：直接在渲染中使用非同步資料

- 統一介面：Promise 和 Context 使用相同的 API

- 自動 `Suspense` 整合：無需手動處理載入狀態

- 條件式使用：可以在條件語句中使用

適用場景：

- 簡單的資料載入

- Context 值的讀取

- 需要條件式載入的情況

- 與 `Suspense` 和 Error Boundary 整合的應用

注意 `use()` API 目前仍在實驗階段，在生產環境中使用前請確認其穩定性和瀏覽器支援度。
