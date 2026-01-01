# 5.3.1 `useContext`：Context API 共享資料

<br />

## 基本概念

`useContext` 是 React Hook，用於在元件樹中共享資料，避免 Props Drilling 問題。Context 提供一種在元件間傳遞資料的方式，不需要逐層傳遞 props。

### 1. 建立與使用 Context

```jsx
import React, { createContext, useContext, useState } from 'react';

/** 建立 Context */
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  /** 使用 useContext 取得 Context 值 */
  const { theme, setTheme } = useContext(ThemeContext);

  return (
    <button 
      style={{
        backgroundColor: theme === 'light' ? '#fff' : '#333',
        color: theme === 'light' ? '#333' : '#fff'
      }}
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
    >
      切換主題 ({theme})
    </button>
  );
}

function App() {
  return (
    <ThemeProvider>
      <div>
        <h1>主題切換範例</h1>
        <ThemedButton />
      </div>
    </ThemeProvider>
  );
}
```

### 2. 預設值與錯誤處理

```jsx
const UserContext = createContext();

/** 自定義 Hook 提供錯誤處理 */
function useUser() {
  const context = useContext(UserContext);

  if (!context) {
    throw new Error('useUser 必須在 UserProvider 內使用');
  }

  return context;
}

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const login = async (credentials) => {
    setLoading(true);
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      const userData = await response.json();
      setUser(userData);
    } catch (error) {
      console.error('登入失敗:', error);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

function LoginButton() {
  const { user, loading, login, logout } = useUser();

  if (loading) return <button disabled>載入中...</button>;

  if (user) {
    return (
      <div>
        <span>歡迎，{user.name}</span>
        <button onClick={logout}>登出</button>
      </div>
    );
  }

  return (
    <button onClick={() => login({ username: 'demo', password: 'demo' })}>
      登入
    </button>
  );
}
```

<br />

## 多層 Context 使用

### 1. 巢狀 Context Providers

```jsx
const ThemeContext = createContext();
const LanguageContext = createContext();
const UserContext = createContext();

function AppProviders({ children }) {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <UserProvider>
          {children}
        </UserProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('zh-TW');
  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

function Header() {
  const { theme, setTheme } = useContext(ThemeContext);
  const { language, setLanguage } = useContext(LanguageContext);
  const { user } = useContext(UserContext);

  return (
    <header style={{ 
      backgroundColor: theme === 'light' ? '#f0f0f0' : '#333',
      color: theme === 'light' ? '#333' : '#fff'
    }}>
      <h1>應用程式標題</h1>

      <div>
        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="zh-TW">繁體中文</option>
          <option value="en-US">English</option>
        </select>

        <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
          {theme === 'light' ? '深色' : '淺色'}主題
        </button>

        {user && <span>使用者：{user.name}</span>}
      </div>
    </header>
  );
}
```

### 2. 組合多個 Context

```jsx
function useAppContext() {
  const theme = useContext(ThemeContext);
  const language = useContext(LanguageContext);
  const user = useContext(UserContext);

  return { theme, language, user };
}

function Dashboard() {
  const { theme, language, user } = useAppContext();

  const getText = (key) => {
    const texts = {
      'zh-TW': {
        welcome: '歡迎',
        dashboard: '控制台'
      },
      'en-US': {
        welcome: 'Welcome',
        dashboard: 'Dashboard'
      }
    };
    return texts[language.language][key];
  };

  return (
    <div style={{
      backgroundColor: theme.theme === 'light' ? '#fff' : '#222',
      color: theme.theme === 'light' ? '#333' : '#fff',
      padding: '20px'
    }}>
      <h2>{getText('dashboard')}</h2>
      {user.user && <p>{getText('welcome')}, {user.user.name}!</p>}
    </div>
  );
}
```

<br />

## 實際應用範例

### 1. 購物車 Context

```jsx
const CartContext = createContext();

function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart 必須在 CartProvider 內使用');
  }
  return context;
}

function CartProvider({ children }) {
  const [items, setItems] = useState([]);

  const addItem = (product) => {
    setItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);

      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevItems, { ...product, quantity: 1 }];
      }
    });
  };

  const removeItem = (productId) => {
    setItems(prevItems => prevItems.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId, quantity) => {
    if (quantity <= 0) {
      removeItem(productId);
      return;
    }

    setItems(prevItems =>
      prevItems.map(item =>
        item.id === productId
          ? { ...item, quantity }
          : item
      )
    );
  };

  const clearCart = () => {
    setItems([]);
  };

  const getTotalPrice = () => {
    return items.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getTotalItems = () => {
    return items.reduce((total, item) => total + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      items,
      addItem,
      removeItem,
      updateQuantity,
      clearCart,
      getTotalPrice,
      getTotalItems
    }}>
      {children}
    </CartContext.Provider>
  );
}

function ProductCard({ product }) {
  const { addItem } = useCart();

  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>
      <button onClick={() => addItem(product)}>
        加入購物車
      </button>
    </div>
  );
}

function CartSummary() {
  const { items, getTotalPrice, getTotalItems } = useCart();

  return (
    <div className="cart-summary">
      <h3>購物車</h3>
      <p>商品數量：{getTotalItems()}</p>
      <p>總價：NT$ {getTotalPrice()}</p>

      {items.length === 0 ? (
        <p>購物車是空的</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.name} x {item.quantity}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### 2. 通知系統 Context

```jsx
const NotificationContext = createContext();

function useNotification() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification 必須在 NotificationProvider 內使用');
  }
  return context;
}

function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  const addNotification = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    const notification = { id, message, type, duration };

    setNotifications(prev => [...prev, notification]);

    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }
  };

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  return (
    <NotificationContext.Provider value={{
      notifications,
      addNotification,
      removeNotification,
      clearAll
    }}>
      {children}
    </NotificationContext.Provider>
  );
}

function NotificationContainer() {
  const { notifications, removeNotification } = useNotification();

  return (
    <div className="notification-container">
      {notifications.map(notification => (
        <div
          key={notification.id}
          className={`notification notification-${notification.type}`}
        >
          <span>{notification.message}</span>
          <button onClick={() => removeNotification(notification.id)}>
            ×
          </button>
        </div>
      ))}
    </div>
  );
}

function ActionButtons() {
  const { addNotification } = useNotification();

  return (
    <div>
      <button onClick={() => addNotification('成功訊息', 'success')}>
        成功通知
      </button>
      <button onClick={() => addNotification('錯誤訊息', 'error')}>
        錯誤通知
      </button>
      <button onClick={() => addNotification('警告訊息', 'warning')}>
        警告通知
      </button>
      <button onClick={() => addNotification('資訊訊息', 'info')}>
        資訊通知
      </button>
    </div>
  );
}
```

### 3. 表單狀態管理 Context

```jsx
const FormContext = createContext();

function useForm() {
  const context = useContext(FormContext);
  if (!context) {
    throw new Error('useForm 必須在 FormProvider 內使用');
  }
  return context;
}

function FormProvider({ children, initialValues = {}, validationRules = {} }) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const setValue = (name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));

    /** 清除錯誤 */
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const setFieldTouched = (name) => {
    setTouched(prev => ({ ...prev, [name]: true }));
  };

  const validateField = (name, value) => {
    const rules = validationRules[name];
    if (!rules) return '';

    for (const rule of rules) {
      const error = rule(value, values);
      if (error) return error;
    }

    return '';
  };

  const validateForm = () => {
    const newErrors = {};

    Object.keys(validationRules).forEach(name => {
      const error = validateField(name, values[name]);
      if (error) newErrors[name] = error;
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (onSubmit) => {
    setIsSubmitting(true);

    /** 標記所有欄位為已觸碰 */
    const allTouched = {};
    Object.keys(validationRules).forEach(name => {
      allTouched[name] = true;
    });
    setTouched(allTouched);

    if (validateForm()) {
      try {
        await onSubmit(values);
      } catch (error) {
        console.error('表單送出失敗:', error);
      }
    }

    setIsSubmitting(false);
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  };

  return (
    <FormContext.Provider value={{
      values,
      errors,
      touched,
      isSubmitting,
      setValue,
      setFieldTouched,
      validateField,
      validateForm,
      handleSubmit,
      reset
    }}>
      {children}
    </FormContext.Provider>
  );
}

function FormField({ name, label, type = 'text', required = false }) {
  const { values, errors, touched, setValue, setFieldTouched, validateField } = useForm();

  const handleChange = (e) => {
    setValue(name, e.target.value);
  };

  const handleBlur = () => {
    setFieldTouched(name);
    const error = validateField(name, values[name]);
    if (error) {
      // 錯誤會在 validateField 中設定
    }
  };

  return (
    <div className="form-field">
      <label>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <input
        type={type}
        value={values[name] || ''}
        onChange={handleChange}
        onBlur={handleBlur}
        className={errors[name] && touched[name] ? 'error' : ''}
      />
      {errors[name] && touched[name] && (
        <span className="error-message">{errors[name]}</span>
      )}
    </div>
  );
}

function ContactForm() {
  const { handleSubmit, reset, isSubmitting } = useForm();

  const onSubmit = async (values) => {
    console.log('送出表單:', values);
    /** 模擬 API 呼叫 */
    await new Promise(resolve => setTimeout(resolve, 1000));
    alert('表單送出成功！');
    reset();
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      handleSubmit(onSubmit);
    }}>
      <FormField name="name" label="姓名" required />
      <FormField name="email" label="Email" type="email" required />
      <FormField name="message" label="訊息" />

      <div>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? '送出中...' : '送出'}
        </button>
        <button type="button" onClick={reset}>
          重設
        </button>
      </div>
    </form>
  );
}

/** 使用表單 */
function App() {
  const validationRules = {
    name: [
      (value) => !value?.trim() ? '姓名為必填' : '',
      (value) => value?.length < 2 ? '姓名至少需要 2 個字元' : ''
    ],
    email: [
      (value) => !value?.trim() ? 'Email 為必填' : '',
      (value) => !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? 'Email 格式不正確' : ''
    ]
  };

  return (
    <FormProvider
      initialValues={{ name: '', email: '', message: '' }}
      validationRules={validationRules}
    >
      <ContactForm />
    </FormProvider>
  );
}
```

<br />

## 效能最佳化

### 1. 分離 Context 避免不必要的重新渲染

```jsx
/** ❌ 單一 Context 包含所有狀態 */
const AppContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('zh-TW');

  /** 每次任何狀態變化都會重新渲染所有使用者 */
  const value = { user, setUser, theme, setTheme, language, setLanguage };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

/** ✅ 分離 Context */
const UserContext = createContext();
const ThemeContext = createContext();
const LanguageContext = createContext();

function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('zh-TW');
  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}
```

### 2. 使用 `useMemo` 最佳化 Context 值

```jsx
function OptimizedProvider({ children }) {
  const [user, setUser] = useState(null);
  const [preferences, setPreferences] = useState({});

  /** 使用 useMemo 避免每次渲染都建立新物件 */
  const contextValue = useMemo(() => ({
    user,
    setUser,
    preferences,
    setPreferences,
    /** 計算值也可以快取 */
    isLoggedIn: !!user,
    userDisplayName: user?.name || 'Guest'
  }), [user, preferences]);

  return (
    <UserContext.Provider value={contextValue}>
      {children}
    </UserContext.Provider>
  );
}
```

### 3. 使用 `React.memo` 避免不必要的重新渲染

```jsx
const ExpensiveComponent = React.memo(function ExpensiveComponent() {
  const { theme } = useContext(ThemeContext);

  console.log('ExpensiveComponent 重新渲染');

  return (
    <div style={{ backgroundColor: theme === 'light' ? '#fff' : '#333' }}>
      昂貴的元件
    </div>
  );
});

// 只有 theme 變化時才會重新渲染
```

<br />

## 最佳實務

### 1. Context 設計原則

- 單一職責：每個 Context 只管理相關的狀態

- 適當粒度：避免過度細分或過度集中

- 提供預設值：為 Context 提供合理的預設值

- 錯誤處理：檢查 Context 是否在正確的 Provider 內使用

### 2. 效能考量

- 分離關注點：將不相關的狀態分到不同的 Context

- 使用 useMemo：快取 Context 值避免不必要的重新渲染

- React.memo：包裝消費 Context 的元件

- 避免過度使用：不是所有狀態都需要放在 Context 中

### 3. 組織結構

- 自定義 Hook：為每個 Context 提供自定義 Hook

- Provider 組合：使用組合模式管理多個 Provider

- 型別定義：使用 TypeScript 定義 Context 型別

- 測試友善：設計易於測試的 Context 結構
