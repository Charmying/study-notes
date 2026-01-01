# 3.1.3 條件渲染：`if`、`&&`、三元運算子實務

<br />

## 基本概念

條件渲染允許根據不同條件顯示不同的 UI 元素，是 React 應用程式中控制介面顯示的核心技術。

<br />

## 方法一：`if` 語句 (函式內部)

### 1. 基本 `if` 語句

```jsx
function Greeting({ isLoggedIn, username }) {
  if (isLoggedIn) {
    return <h1>歡迎回來，{username}！</h1>;
  }
  return <h1>請先登入</h1>;
}
```

### 2. 複雜條件判斷

```jsx
function UserStatus({ user }) {
  if (!user) {
    return <div>載入中...</div>;
  }

  if (user.role === 'admin') {
    return (
      <div>
        <h2>管理員面板</h2>
        <p>歡迎，{user.name}</p>
      </div>
    );
  }

  if (user.role === 'user') {
    return (
      <div>
        <h2>使用者面板</h2>
        <p>哈囉，{user.name}</p>
      </div>
    );
  }

  return <div>權限不足</div>;
}
```

### 3. 提前返回模式

```jsx
function ProductCard({ product }) {
  /** 提前處理錯誤狀態 */
  if (!product) {
    return <div>產品不存在</div>;
  }

  if (product.status === 'discontinued') {
    return <div>此產品已停產</div>;
  }

  /** 正常渲染 */
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>價格：NT$ {product.price}</p>
    </div>
  );
}
```

<br />

## 方法二：短路運算 (`&&`)

### 1. 基本短路運算

```jsx
function Notification({ hasNotification, message }) {
  return (
    <div>
      <h1>首頁</h1>
      {hasNotification && (
        <div className="notification">
          {message}
        </div>
      )}
    </div>
  );
}
```

### 2. 多重條件

```jsx
function Dashboard({ user, permissions }) {
  return (
    <div>
      <h1>控制台</h1>

      {user && user.isActive && (
        <div>歡迎，{user.name}</div>
      )}

      {permissions.canEdit && (
        <button>編輯</button>
      )}

      {permissions.canDelete && (
        <button>刪除</button>
      )}
    </div>
  );
}
```

### 3. 陣列長度檢查

```jsx
function TodoList({ todos }) {
  return (
    <div>
      <h2>待辦事項</h2>

      {todos.length > 0 && (
        <ul>
          {todos.map(todo => (
            <li key={todo.id}>{todo.text}</li>
          ))}
        </ul>
      )}

      {todos.length === 0 && (
        <p>沒有待辦事項</p>
      )}
    </div>
  );
}
```

<br />

## 方法三：三元運算子 (`value` `?` `true 時執行` `:` `false 時執行`)

### 1. 基本三元運算

```jsx
function LoginButton({ isLoggedIn, onLogin, onLogout }) {
  return (
    <button onClick={isLoggedIn ? onLogout : onLogin}>
      {isLoggedIn ? '登出' : '登入'}
    </button>
  );
}
```

### 2. 複雜元素切換

```jsx
function UserProfile({ user, isEditing }) {
  return (
    <div className="user-profile">
      {isEditing ? (
        <form>
          <input defaultValue={user.name} />
          <input defaultValue={user.email} />
          <button type="submit">儲存</button>
        </form>
      ) : (
        <div>
          <h2>{user.name}</h2>
          <p>{user.email}</p>
          <button>編輯</button>
        </div>
      )}
    </div>
  );
}
```

### 3. 巢狀三元運算

```jsx
function StatusBadge({ status }) {
  return (
    <span className={
      status === 'active' ? 'badge-success' :
      status === 'pending' ? 'badge-warning' :
      'badge-error'
    }>
      {status === 'active' ? '啟用' :
       status === 'pending' ? '待審核' :
       '停用'}
    </span>
  );
}
```

<br />

## 實務應用範例

### 1. 載入狀態處理

```jsx
function DataComponent({ data, loading, error }) {
  if (loading) {
    return <div className="spinner">載入中...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>發生錯誤：{error.message}</p>
        <button onClick={() => window.location.reload()}>
          重新載入
        </button>
      </div>
    );
  }

  return (
    <div>
      {data && data.length > 0 ? (
        <ul>
          {data.map(item => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      ) : (
        <p>沒有資料</p>
      )}
    </div>
  );
}
```

### 2. 權限控制

```jsx
function AdminPanel({ user, children }) {
  /** 檢查使用者權限 */
  if (!user) {
    return <div>請先登入</div>;
  }

  if (user.role !== 'admin') {
    return <div>權限不足</div>;
  }

  return (
    <div className="admin-panel">
      <header>
        <h1>管理面板</h1>
        <p>管理員：{user.name}</p>
      </header>
      {children}
    </div>
  );
}
```

### 3. 表單驗證顯示

```jsx
function FormField({ label, value, error, required }) {
  return (
    <div className="form-field">
      <label>
        {label}
        {required && <span className="required">*</span>}
      </label>

      <input 
        value={value}
        className={error ? 'error' : ''}
      />

      {error && (
        <span className="error-message">{error}</span>
      )}
    </div>
  );
}
```

### 4. 響應式顯示

```jsx
function ResponsiveMenu({ isMobile, isMenuOpen }) {
  return (
    <nav>
      {isMobile ? (
        <div>
          <button className="menu-toggle">
            選單
          </button>
          {isMenuOpen && (
            <div className="mobile-menu">
              <a href="/home">首頁</a>
              <a href="/about">關於</a>
              <a href="/contact">聯絡</a>
            </div>
          )}
        </div>
      ) : (
        <div className="desktop-menu">
          <a href="/home">首頁</a>
          <a href="/about">關於</a>
          <a href="/contact">聯絡</a>
        </div>
      )}
    </nav>
  );
}
```

<br />

## 效能考量

### 1. 避免不必要的重新渲染

```jsx
/** ❌ 每次都會建立新物件 */
function BadExample({ showDetails }) {
  return (
    <div>
      {showDetails && (
        <div style={{ padding: '10px', margin: '5px' }}>
          詳細資訊
        </div>
      )}
    </div>
  );
}

/** ✅ 將樣式提取到外部 */
const detailsStyle = { padding: '10px', margin: '5px' };

function GoodExample({ showDetails }) {
  return (
    <div>
      {showDetails && (
        <div style={detailsStyle}>
          詳細資訊
        </div>
      )}
    </div>
  );
}
```

### 2. 使用 React.memo 最佳化

```jsx
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  return (
    <div>
      {/* 複雜的渲染內容 */}
    </div>
  );
});

function ParentComponent({ shouldShow, data }) {
  return (
    <div>
      {shouldShow && <ExpensiveComponent data={data} />}
    </div>
  );
}
```

<br />

## 常見錯誤與解決方案

### 1. 短路運算的陷阱

```jsx
/** ❌ 當 count 為 0 時會顯示 0 */
function BadCounter({ count }) {
  return (
    <div>
      {count && <p>數量：{count}</p>}
    </div>
  );
}

/** ✅ 明確檢查條件 */
function GoodCounter({ count }) {
  return (
    <div>
      {count > 0 && <p>數量：{count}</p>}
    </div>
  );
}
```

### 2. 複雜條件的可讀性

```jsx
/** ❌ 難以閱讀的巢狀條件 */
function BadExample({ user, permissions, settings }) {
  return (
    <div>
      {user && user.isActive && permissions && permissions.canView && 
       settings && settings.showContent && (
        <Content />
      )}
    </div>
  );
}

/** ✅ 提取條件到變數 */
function GoodExample({ user, permissions, settings }) {
  const canShowContent = user?.isActive &&  permissions?.canView &&  settings?.showContent;

  return (
    <div>
      {canShowContent && <Content />}
    </div>
  );
}
```

<br />

## 最佳實務

- 優先使用短路運算：簡單的顯示/隱藏條件

- 三元運算子用於二選一：在兩個不同元素間切換

- `if` 語句處理複雜條件：多重條件或提前返回

- 提取複雜條件到變數：提高程式碼可讀性

- 避免過深的巢狀：使用提前返回或元件分割

- 考慮效能影響：避免在條件中建立新物件
