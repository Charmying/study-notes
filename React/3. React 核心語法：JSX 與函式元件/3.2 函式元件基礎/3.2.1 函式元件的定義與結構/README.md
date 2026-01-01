# 3.2.1 函式元件的定義與結構

<br />

## 基本概念

函式元件是 React 中最簡單且最常用的元件類型，使用 JavaScript 函式來定義 UI 元件。函式元件接收 `props` 作為參數，並返回 JSX 元素。

## 函式元件的定義方式

### 1. 函式宣告 (Function Declaration)

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}!</h1>;
}
```

### 2. 函式表達式 (Function Expression)

```jsx
const Welcome = function(props) {
  return <h1>Hello, {props.name}!</h1>;
};
```

### 3. 箭頭函式 (Arrow Function)

```jsx
const Welcome = (props) => {
  return <h1>Hello, {props.name}!</h1>;
};

/** 簡化版本 */
const Welcome = props => <h1>Hello, {props.name}!</h1>;
```

<br />

## 基本結構

### 1. 最簡單的函式元件

```jsx
function SimpleComponent() {
  return <div>Hello World</div>;
}
```

### 2. 接收 `props` 的元件

```jsx
function Greeting({ name, age }) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
    </div>
  );
}
```

### 3. 包含多個元素的元件

```jsx
function UserCard({ user }) {
  return (
    <>
      <img src={user.avatar} alt="Avatar" />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <span>{user.role}</span>
    </>
  );
}
```

<br />

## `props` 解構

### 1. 參數解構

```jsx
/** 直接在參數中解構 */
function ProductCard({ name, price, image, inStock }) {
  return (
    <div className="product-card">
      <img src={image} alt={name} />
      <h3>{name}</h3>
      <p>NT$ {price}</p>
      {inStock ? <span>有庫存</span> : <span>缺貨</span>}
    </div>
  );
}
```

### 2. 函式內解構

```jsx
function ProductCard(props) {
  const { name, price, image, inStock } = props;

  return (
    <div className="product-card">
      <img src={image} alt={name} />
      <h3>{name}</h3>
      <p>NT$ {price}</p>
      {inStock ? <span>有庫存</span> : <span>缺貨</span>}
    </div>
  );
}
```

### 3. 預設值設定

```jsx
function Button({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  disabled = false 
}) {
  return (
    <button 
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

<br />

## 返回值類型

### 1. 單一 JSX 元素

```jsx
function Title({ text }) {
  return <h1>{text}</h1>;
}
```

### 2. Fragment

```jsx
function UserInfo({ user }) {
  return (
    <>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </>
  );
}
```

### 3. 陣列

```jsx
function Navigation({ items }) {
  return items.map(item => (
    <a key={item.id} href={item.url}>
      {item.label}
    </a>
  ));
}
```

### 4. 條件返回

```jsx
function ErrorMessage({ error }) {
  if (!error) return null;

  return (
    <div className="error">
      {error.message}
    </div>
  );
}
```

<br />

## 元件命名規範

### 1. PascalCase 命名

```jsx
/** ✅ 正確：使用 PascalCase */
function UserProfile() {
  return <div>User Profile</div>;
}

function ShoppingCart() {
  return <div>Shopping Cart</div>;
}

/** ❌ 錯誤：小寫開頭 */
function userProfile() {
  return <div>User Profile</div>;
}
```

### 2. 有意義的名稱

```jsx
/** ✅ 清楚表達元件用途 */
function LoginForm() {
  return <form>Login Form</form>;
}

function ProductList() {
  return <ul>Product List</ul>;
}

/** ❌ 模糊不清的名稱 */
function Component1() {
  return <div>Something</div>;
}
```

<br />

## 實際應用範例

### 1. 簡單的展示元件

```jsx
function Avatar({ src, alt, size = 'medium' }) {
  const sizeClass = `avatar-${size}`;

  return (
    <img 
      src={src} 
      alt={alt} 
      className={`avatar ${sizeClass}`}
    />
  );
}
```

### 2. 複合元件

```jsx
function Card({ title, children, footer }) {
  return (
    <div className="card">
      {title && (
        <div className="card-header">
          <h3>{title}</h3>
        </div>
      )}

      <div className="card-body">
        {children}
      </div>

      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
}
```

### 3. 列表渲染元件

```jsx
function TodoList({ todos, onToggle, onDelete }) {
  return (
    <ul className="todo-list">
      {todos.map(todo => (
        <li key={todo.id} className={todo.completed ? 'completed' : ''}>
          <input 
            type="checkbox"
            checked={todo.completed}
            onChange={() => onToggle(todo.id)}
          />
          <span>{todo.text}</span>
          <button onClick={() => onDelete(todo.id)}>
            刪除
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### 4. 表單元件

```jsx
function ContactForm({ onSubmit }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="contact-form">
      <div className="form-group">
        <label htmlFor="name">姓名</label>
        <input 
          type="text" 
          id="name" 
          name="name" 
          required 
        />
      </div>

      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input 
          type="email" 
          id="email" 
          name="email" 
          required 
        />
      </div>

      <div className="form-group">
        <label htmlFor="message">訊息</label>
        <textarea 
          id="message" 
          name="message" 
          rows="4" 
          required
        />
      </div>

      <button type="submit">送出</button>
    </form>
  );
}
```

## 元件組合

### 1. 基本組合

```jsx
function Header({ title, subtitle }) {
  return (
    <header>
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </header>
  );
}

function Footer({ copyright }) {
  return (
    <footer>
      <p>&copy; {copyright}</p>
    </footer>
  );
}

function Layout({ title, subtitle, children, copyright }) {
  return (
    <div className="layout">
      <Header title={title} subtitle={subtitle} />
      <main>{children}</main>
      <Footer copyright={copyright} />
    </div>
  );
}
```

### 2. 條件組合

```jsx
function Dashboard({ user, isAdmin }) {
  return (
    <div className="dashboard">
      <h1>歡迎，{user.name}</h1>

      {isAdmin && (
        <AdminPanel />
      )}

      <UserStats user={user} />
      <RecentActivity user={user} />
    </div>
  );
}

function AdminPanel() {
  return (
    <div className="admin-panel">
      <h2>管理面板</h2>
      <button>管理使用者</button>
      <button>系統設定</button>
    </div>
  );
}
```

<br />

## 效能考量

### 1. 避免在渲染中建立函式

```jsx
/** ❌ 每次渲染都建立新函式 */
function BadExample({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          <button onClick={() => console.log(item.id)}>
            {item.name}
          </button>
        </li>
      ))}
    </ul>
  );
}

/** ✅ 使用 useCallback 或提取到外部 */
function GoodExample({ items, onItemClick }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          <button onClick={() => onItemClick(item.id)}>
            {item.name}
          </button>
        </li>
      ))}
    </ul>
  );
}
```

### 2. 使用 React.memo 最佳化

```jsx
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  /** 複雜的計算或渲染 */
  return (
    <div>
      {data.map(item => (
        <ComplexItem key={item.id} item={item} />
      ))}
    </div>
  );
});
```

<br />

## 最佳實務

- 使用 PascalCase 命名元件

- 保持元件功能單一且專注

- 適當使用 `props` 解構提高可讀性

- 為 `props` 設定合理的預設值

- 使用有意義的元件和變數名稱

- 避免過度嵌套，適時拆分子元件

- 考慮效能影響，適當使用 `React.memo`

- 保持一致的程式碼風格和格式
