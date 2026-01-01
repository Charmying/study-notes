# 4.1.4 Props Drilling 的問題與初步解決方案

<br />

## Props Drilling 問題說明

### 1. 什麼是 Props Drilling

Props Drilling 指的是在 React 元件樹中，為了將資料從頂層元件傳遞到深層子元件，必須透過中間的每一層元件逐層傳遞 `props` 的現象。

```jsx
/** 問題範例：資料需要從 App 傳遞到 UserMenu */
function App() {
  const user = { 
    id: 1, 
    name: 'Charmy', 
    role: 'admin',
    avatar: 'avatar.jpg'
  };

  return <Layout user={user} />;
}

function Layout({ user }) {
  return (
    <div className="layout">
      <Header user={user} />
      <Main />
      <Footer />
    </div>
  );
}

function Header({ user }) {
  return (
    <header>
      <Logo />
      <Navigation user={user} />
    </header>
  );
}

function Navigation({ user }) {
  return (
    <nav>
      <NavLinks />
      <UserMenu user={user} />
    </nav>
  );
}

function UserMenu({ user }) {
  return (
    <div className="user-menu">
      <img src={user.avatar} alt={user.name} />
      <span>{user.name}</span>
      <span>{user.role}</span>
    </div>
  );
}
```

### 2. Props Drilling 的問題

```jsx
/** 複雜的 Props Drilling 範例 */
function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('zh-TW');
  const [notifications, setNotifications] = useState([]);

  return (
    <Dashboard
      user={user}
      theme={theme}
      language={language}
      notifications={notifications}
      onUserUpdate={setUser}
      onThemeChange={setTheme}
      onLanguageChange={setLanguage}
      onNotificationDismiss={(id) => 
        setNotifications(prev => prev.filter(n => n.id !== id))
      }
    />
  );
}

function Dashboard({ 
  user, 
  theme, 
  language, 
  notifications,
  onUserUpdate,
  onThemeChange,
  onLanguageChange,
  onNotificationDismiss
}) {
  return (
    <div className={`dashboard theme-${theme}`}>
      <Sidebar
        user={user}
        theme={theme}
        language={language}
        onThemeChange={onThemeChange}
        onLanguageChange={onLanguageChange}
      />
      <MainContent
        user={user}
        notifications={notifications}
        onUserUpdate={onUserUpdate}
        onNotificationDismiss={onNotificationDismiss}
      />
    </div>
  );
}

function Sidebar({ 
  user, 
  theme, 
  language, 
  onThemeChange, 
  onLanguageChange 
}) {
  return (
    <aside>
      <UserProfile user={user} />
      <Settings
        theme={theme}
        language={language}
        onThemeChange={onThemeChange}
        onLanguageChange={onLanguageChange}
      />
    </aside>
  );
}

function Settings({ theme, language, onThemeChange, onLanguageChange }) {
  return (
    <div className="settings">
      <ThemeSelector theme={theme} onChange={onThemeChange} />
      <LanguageSelector language={language} onChange={onLanguageChange} />
    </div>
  );
}
```

<br />

## 解決方案一：元件組合 (Component Composition)

### 1. 使用 children prop

```jsx

/** 重構前：Props Drilling */
function App() {
  const user = { name: 'Charmy', role: 'admin' };

  return <Layout user={user} />;
}

function Layout({ user }) {
  return (
    <div>
      <Header user={user} />
    </div>
  );
}

function Header({ user }) {
  return (
    <header>
      <UserInfo user={user} />
    </header>
  );
}

/** 重構後：元件組合 */
function App() {
  const user = { name: 'Charmy', role: 'admin' };

  return (
    <Layout>
      <Header>
        <UserInfo user={user} />
      </Header>
    </Layout>
  );
}

function Layout({ children }) {
  return <div className="layout">{children}</div>;
}

function Header({ children }) {
  return <header className="header">{children}</header>;
}

function UserInfo({ user }) {
  return (
    <div>
      <span>{user.name}</span>
      <span>{user.role}</span>
    </div>
  );
}
```

### 2. 使用具名插槽 (Named Slots)

```jsx
function Layout({ header, sidebar, main, footer }) {
  return (
    <div className="layout">
      <div className="header">{header}</div>
      <div className="content">
        <div className="sidebar">{sidebar}</div>
        <div className="main">{main}</div>
      </div>
      <div className="footer">{footer}</div>
    </div>
  );
}

function App() {
  const user = { name: 'Charmy', role: 'admin' };
  const products = [
    { id: 1, name: '產品 1' },
    { id: 2, name: '產品 2' }
  ];

  return (
    <Layout
      header={<UserHeader user={user} />}
      sidebar={<Navigation user={user} />}
      main={<ProductList products={products} />}
      footer={<Footer />}
    />
  );
}

function UserHeader({ user }) {
  return (
    <header>
      <h1>歡迎，{user.name}</h1>
    </header>
  );
}

function Navigation({ user }) {
  return (
    <nav>
      <p>角色：{user.role}</p>
    </nav>
  );
}
```

### 3. 渲染函式模式 (Render Props)

```jsx
function DataProvider({ children, endpoint }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(endpoint)
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, [endpoint]);

  return children({ data, loading, error });
}

function App() {
  return (
    <div>
      <DataProvider endpoint="/api/users">
        {({ data: users, loading, error }) => (
          <Layout>
            <Header>
              {loading ? (
                <div>載入中...</div>
              ) : error ? (
                <div>錯誤：{error}</div>
              ) : (
                <UserCount count={users?.length || 0} />
              )}
            </Header>
            <Main>
              {users && <UserList users={users} />}
            </Main>
          </Layout>
        )}
      </DataProvider>
    </div>
  );
}

function Layout({ children }) {
  return <div className="layout">{children}</div>;
}

function Header({ children }) {
  return <header>{children}</header>;
}

function Main({ children }) {
  return <main>{children}</main>;
}

function UserCount({ count }) {
  return <div>使用者數量：{count}</div>;
}

function UserList({ users }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

<br />

## 解決方案二：自定義 Hook

### 1. 狀態管理 Hook

```jsx
/** 自定義 Hook 管理使用者狀態 */
function useUser() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    /** 模擬 API 呼叫 */
    setTimeout(() => {
      setUser({ 
        id: 1, 
        name: 'Charmy', 
        role: 'admin',
        avatar: 'avatar.jpg'
      });
      setLoading(false);
    }, 1000);
  }, []);

  const updateUser = (updates) => {
    setUser(prev => ({ ...prev, ...updates }));
  };

  return { user, loading, updateUser };
}

/** 使用自定義 Hook 的元件 */
function App() {
  return (
    <Layout>
      <Header />
      <Main />
    </Layout>
  );
}

function Layout({ children }) {
  return <div className="layout">{children}</div>;
}

function Header() {
  return (
    <header>
      <Navigation />
    </header>
  );
}

function Navigation() {
  return (
    <nav>
      <UserMenu />
    </nav>
  );
}

function UserMenu() {
  const { user, loading } = useUser();

  if (loading) return <div>載入中...</div>;

  return (
    <div className="user-menu">
      <img src={user.avatar} alt={user.name} />
      <span>{user.name}</span>
      <span>{user.role}</span>
    </div>
  );
}

function Main() {
  const { user, updateUser } = useUser();

  return (
    <main>
      <UserProfile user={user} onUpdate={updateUser} />
    </main>
  );
}

function UserProfile({ user, onUpdate }) {
  if (!user) return null;

  return (
    <div>
      <h2>{user.name}</h2>
      <button onClick={() => onUpdate({ name: '更新的名稱' })}>
        更新名稱
      </button>
    </div>
  );
}
```

### 2. 複雜狀態管理 Hook

```jsx
function useAppState() {
  const [state, setState] = useState({
    user: null,
    theme: 'light',
    language: 'zh-TW',
    notifications: []
  });

  const actions = {
    setUser: (user) => setState(prev => ({ ...prev, user })),
    setTheme: (theme) => setState(prev => ({ ...prev, theme })),
    setLanguage: (language) => setState(prev => ({ ...prev, language })),
    addNotification: (notification) => 
      setState(prev => ({ 
        ...prev, 
        notifications: [...prev.notifications, notification] 
      })),
    removeNotification: (id) =>
      setState(prev => ({
        ...prev,
        notifications: prev.notifications.filter(n => n.id !== id)
      }))
  };

  return { state, actions };
}

/** 在任何深層元件中使用 */
function DeepComponent() {
  const { state, actions } = useAppState();

  return (
    <div>
      <p>目前主題：{state.theme}</p>
      <button onClick={() => actions.setTheme('dark')}>
        切換到深色主題
      </button>
      <p>通知數量：{state.notifications.length}</p>
    </div>
  );
}
```

<br />

## 解決方案三：狀態提升與集中管理

### 1. 狀態提升到共同父元件

```jsx
function App() {
  /** 將狀態提升到最小共同父元件 */
  const [cartItems, setCartItems] = useState([]);
  const [user, setUser] = useState({ name: 'Charmy' });

  const addToCart = (product) => {
    setCartItems(prev => [...prev, product]);
  };

  const removeFromCart = (productId) => {
    setCartItems(prev => prev.filter(item => item.id !== productId));
  };

  return (
    <div>
      {/* 直接傳遞給需要的元件 */}
      <Header cartCount={cartItems.length} user={user} />
      <ProductGrid onAddToCart={addToCart} />
      <Cart 
        items={cartItems} 
        onRemoveItem={removeFromCart}
      />
    </div>
  );
}

function Header({ cartCount, user }) {
  return (
    <header>
      <div>歡迎，{user.name}</div>
      <CartIcon count={cartCount} />
    </header>
  );
}

function CartIcon({ count }) {
  return (
    <div className="cart-icon">
      🛒 {count}
    </div>
  );
}

function ProductGrid({ onAddToCart }) {
  const products = [
    { id: 1, name: '產品 1', price: 100 },
    { id: 2, name: '產品 2', price: 200 }
  ];

  return (
    <div>
      {products.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onAddToCart={onAddToCart}
        />
      ))}
    </div>
  );
}

function ProductCard({ product, onAddToCart }) {
  return (
    <div>
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>
      <button onClick={() => onAddToCart(product)}>
        加入購物車
      </button>
    </div>
  );
}
```

### 2. 使用 Reducer 模式

```jsx
const initialState = {
  user: null,
  cart: [],
  theme: 'light'
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'ADD_TO_CART':
      return { 
        ...state, 
        cart: [...state.cart, action.payload] 
      };
    case 'REMOVE_FROM_CART':
      return {
        ...state,
        cart: state.cart.filter(item => item.id !== action.payload)
      };
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    default:
      return state;
  }
}

function App() {
  const [state, dispatch] = useReducer(appReducer, initialState);

  useEffect(() => {
    /** 初始化使用者資料 */
    dispatch({ 
      type: 'SET_USER', 
      payload: { id: 1, name: 'Charmy' } 
    });
  }, []);

  return (
    <div className={`app theme-${state.theme}`}>
      <Header 
        user={state.user}
        cartCount={state.cart.length}
        onThemeChange={(theme) => 
          dispatch({ type: 'SET_THEME', payload: theme })
        }
      />
      <ProductList 
        onAddToCart={(product) =>
          dispatch({ type: 'ADD_TO_CART', payload: product })
        }
      />
      <Cart 
        items={state.cart}
        onRemoveItem={(id) =>
          dispatch({ type: 'REMOVE_FROM_CART', payload: id })
        }
      />
    </div>
  );
}
```

<br />

## 解決方案四：React Context (預告)

### 1. 基本 Context 使用

```jsx
/** 建立 Context */
const UserContext = createContext();

/** Provider 元件 */
function UserProvider({ children }) {
  const [user, setUser] = useState({ 
    name: 'Charmy', 
    role: 'admin' 
  });

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

/** 使用 Context 的 Hook */
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}

/** 應用程式結構 */
function App() {
  return (
    <UserProvider>
      <Layout />
    </UserProvider>
  );
}

function Layout() {
  return (
    <div>
      <Header />
      <Main />
    </div>
  );
}

function Header() {
  return (
    <header>
      <Navigation />
    </header>
  );
}

function Navigation() {
  return (
    <nav>
      <UserMenu />
    </nav>
  );
}

/** 深層元件直接使用 Context */
function UserMenu() {
  const { user } = useUser();

  return (
    <div>
      <span>{user.name}</span>
      <span>{user.role}</span>
    </div>
  );
}
```

<br />

## 方案比較與選擇

### 1. 各方案適用場景

```jsx
/** 場景 1：簡單的資料傳遞 - 使用元件組合 */
function SimpleCase() {
  const user = { name: 'Charmy' };

  return (
    <Layout>
      <Header>
        <UserInfo user={user} />
      </Header>
    </Layout>
  );
}

/** 場景 2：中等複雜度 - 使用自定義 Hook */
function MediumCase() {
  return (
    <div>
      <ComponentA />
      <ComponentB />
    </div>
  );
}

function ComponentA() {
  const { data } = useSharedData();
  return <div>{data.title}</div>;
}

function ComponentB() {
  const { data, updateData } = useSharedData();
  return (
    <button onClick={() => updateData({ title: '新標題' })}>
      更新
    </button>
  );
}

/** 場景 3：複雜應用 - 使用 Context 或狀態管理庫 */
function ComplexCase() {
  return (
    <AppProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </Router>
    </AppProvider>
  );
}
```

### 2. 決策樹

```
Props Drilling 問題
├── 傳遞層級 ≤ 3 層
│   ├── 資料簡單 → 保持 Props 傳遞
│   └── 資料複雜 → 元件組合
├── 傳遞層級 4-6 層
│   ├── 狀態局部使用 → 自定義 Hook
│   └── 狀態全域使用 → Context API
└── 傳遞層級 > 6 層
    ├── 簡單全域狀態 → Context API
    └── 複雜狀態管理 → Redux/Zustand
```

<br />

## 最佳實務

### 1. 避免過度工程化

```jsx
/** ❌ 過度使用 Context */
function OverEngineered() {
  return (
    <ThemeProvider>
      <UserProvider>
        <LanguageProvider>
          <NotificationProvider>
            <SimpleComponent />
          </NotificationProvider>
        </LanguageProvider>
      </UserProvider>
    </ThemeProvider>
  );
}

/** ✅ 適度使用，合併相關狀態 */
function WellEngineered() {
  return (
    <AppProvider> {/* 合併相關狀態 */}
      <SimpleComponent />
    </AppProvider>
  );
}
```

### 2. 漸進式重構

```jsx
// 步驟 1：識別 Props Drilling
// 步驟 2：評估傳遞深度和複雜度
// 步驟 3：選擇適當的解決方案
// 步驟 4：逐步重構，不要一次性大改
// 步驟 5：測試和驗證重構結果
```

### 3. 效能考量

- 元件組合：無額外效能開銷

- 自定義 Hook：輕微的 Hook 呼叫開銷

- Context：可能導致不必要的重新渲染

- 狀態管理庫：額外的 bundle 大小

### 4. 維護性考量

- 可讀性：程式碼是否容易理解

- 可測試性：是否容易進行單元測試

- 可擴展性：未來需求變更時的適應性

- 團隊熟悉度：團隊對解決方案的熟悉程度
