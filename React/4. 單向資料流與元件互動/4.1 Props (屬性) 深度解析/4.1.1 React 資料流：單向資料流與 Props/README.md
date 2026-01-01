# 4.1.1 React 資料流：單向資料流 (One-way Data Flow) 與 Props

<br />

## 單向資料流概念

### 1. 基本原理

React 採用單向資料流架構，資料只能從父元件流向子元件，不能反向流動。這種設計確保了應用程式狀態的可預測性和除錯的容易性。

```jsx
/** 資料流方向：App → UserProfile → Avatar */
function App() {
  const user = {
    name: 'Charmy',
    avatar: 'avatar.jpg',
    role: 'admin'
  };

  return <UserProfile user={user} />;
}

function UserProfile({ user }) {
  return (
    <div>
      <Avatar src={user.avatar} alt={user.name} />
      <h2>{user.name}</h2>
      <span>{user.role}</span>
    </div>
  );
}

function Avatar({ src, alt }) {
  return <img src={src} alt={alt} />;
}
```

### 2. 資料流向圖解

```text
┌─────────────┐
│     App     │ ← 資料來源 (State)
│   (Parent)  │
└──────┬──────┘
       │ Props 向下傳遞
       ▼
┌─────────────┐
│ UserProfile │ ← 接收 Props
│   (Child)   │
└──────┬──────┘
       │ Props 繼續向下
       ▼
┌─────────────┐
│   Avatar    │ ← 接收 Props
│ (Grandchild)│
└─────────────┘
```

<br />

## Props 基礎概念

### 1. Props 定義與特性

Props (Properties) 是 React 元件間傳遞資料的機制，具有以下特性：

- 唯讀性：子元件不能修改接收到的 `props`

- 單向傳遞：只能從父元件傳遞給子元件

- 任意類型：可以傳遞任何 JavaScript 資料類型

```jsx
function ProductCard({ 
  name,       // 字串
  price,      // 數字
  inStock,    // 布林值
  tags,       // 陣列
  details,    // 物件
  onAddToCart // 函式
}) {
  return (
    <div>
      <h3>{name}</h3>
      <p>NT$ {price}</p>
      <p>庫存：{inStock ? '有' : '無'}</p>
      <div>
        {tags.map(tag => <span key={tag}>{tag}</span>)}
      </div>
      <p>規格：{details.size} / {details.color}</p>
      <button onClick={() => onAddToCart(details.id)}>
        加入購物車
      </button>
    </div>
  );
}
```

### 2. Props 傳遞方式

```jsx
function App() {
  const product = {
    id: 1,
    name: '筆記型電腦',
    price: 30000,
    inStock: true,
    tags: ['電腦', '辦公'],
    details: {
      id: 1,
      size: '15吋',
      color: '銀色'
    }
  };

  const handleAddToCart = (productId) => {
    console.log(`加入購物車：${productId}`);
  };

  return (
    <ProductCard
      name={product.name}
      price={product.price}
      inStock={product.inStock}
      tags={product.tags}
      details={product.details}
      onAddToCart={handleAddToCart}
    />
  );
}
```

<br />

## Props 的不可變性

### 1. Props 唯讀特性

```jsx
function BadExample({ user }) {
  /** ❌ 錯誤：不能修改 props */
  user.name = 'Modified Name';
  user.age = 30;

  return <div>{user.name}</div>;
}

function GoodExample({ user }) {
  /** ✅ 正確：建立新物件進行修改 */
  const modifiedUser = {
    ...user,
    displayName: user.name.toUpperCase()
  };

  return <div>{modifiedUser.displayName}</div>;
}
```

### 2. 陣列與物件的處理

```jsx
function TodoList({ todos, onToggle }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => onToggle(todo.id)} // 透過 Callback Function 通知父元件
          />
          <span>{todo.text}</span>
        </li>
      ))}
    </ul>
  );
}

function App() {
  const [todos, setTodos] = useState([
    { id: 1, text: '學習 React', completed: false },
    { id: 2, text: '完成專案', completed: true }
  ]);

  const handleToggle = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  return <TodoList todos={todos} onToggle={handleToggle} />;
}
```

<br />

## 資料流向與狀態管理

### 1. 狀態提升 (Lifting State Up)

```jsx
function TemperatureInput({ scale, temperature, onTemperatureChange }) {
  return (
    <fieldset>
      <legend>輸入溫度 ({scale === 'c' ? '攝氏' : '華氏'})</legend>
      <input
        value={temperature}
        onChange={(e) => onTemperatureChange(e.target.value)}
      />
    </fieldset>
  );
}

function BoilingVerdict({ celsius }) {
  if (celsius >= 100) {
    return <p>水會沸騰</p>;
  }
  return <p>水不會沸騰</p>;
}

function Calculator() {
  const [temperature, setTemperature] = useState('');
  const [scale, setScale] = useState('c');

  const celsius = scale === 'f' 
    ? (temperature - 32) * 5 / 9 
    : temperature;
  const fahrenheit = scale === 'c' 
    ? (temperature * 9 / 5) + 32 
    : temperature;

  return (
    <div>
      <TemperatureInput
        scale="c"
        temperature={scale === 'c' ? temperature : celsius}
        onTemperatureChange={(temp) => {
          setTemperature(temp);
          setScale('c');
        }}
      />

      <TemperatureInput
        scale="f"
        temperature={scale === 'f' ? temperature : fahrenheit}
        onTemperatureChange={(temp) => {
          setTemperature(temp);
          setScale('f');
        }}
      />

      <BoilingVerdict celsius={parseFloat(celsius)} />
    </div>
  );
}
```

### 2. 深層 Props 傳遞問題

```jsx
/** ❌ Props Drilling 問題 */
function App() {
  const user = { name: 'Charmy', role: 'admin' };

  return <Layout user={user} />;
}

function Layout({ user }) {
  return (
    <div>
      <Header user={user} />
      <Main user={user} />
    </div>
  );
}

function Header({ user }) {
  return <Navigation user={user} />;
}

function Navigation({ user }) {
  return <UserMenu user={user} />;
}

function UserMenu({ user }) {
  return <span>歡迎，{user.name}</span>;
}
```

<br />

## Callback Function 與事件處理

### 1. 基本 Callback 模式

```jsx
function SearchBox({ onSearch, placeholder = '搜尋...' }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
      />
      <button type="submit">搜尋</button>
    </form>
  );
}

function App() {
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async (query) => {
    const results = await searchAPI(query);
    setSearchResults(results);
  };

  return (
    <div>
      <SearchBox onSearch={handleSearch} />
      <SearchResults results={searchResults} />
    </div>
  );
}
```

### 2. 複雜事件處理

```jsx
function DataTable({ data, onSort, onFilter, onSelect }) {
  return (
    <table>
      <thead>
        <tr>
          <th onClick={() => onSort('name')}>姓名</th>
          <th onClick={() => onSort('age')}>年齡</th>
          <th onClick={() => onSort('email')}>Email</th>
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id} onClick={() => onSelect(row)}>
            <td>{row.name}</td>
            <td>{row.age}</td>
            <td>{row.email}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function App() {
  const [data, setData] = useState([]);
  const [sortField, setSortField] = useState('');
  const [selectedRow, setSelectedRow] = useState(null);

  const handleSort = (field) => {
    setSortField(field);
    const sortedData = [...data].sort((a, b) => 
      a[field] > b[field] ? 1 : -1
    );
    setData(sortedData);
  };

  const handleSelect = (row) => {
    setSelectedRow(row);
  };

  return (
    <DataTable
      data={data}
      onSort={handleSort}
      onSelect={handleSelect}
    />
  );
}
```

<br />

## 效能最佳化

### 1. `React.memo` 與 Props 比較

```jsx
const ExpensiveComponent = React.memo(function ExpensiveComponent({ 
  data, 
  onUpdate 
}) {
  console.log('ExpensiveComponent 重新渲染');

  return (
    <div>
      {data.map(item => (
        <div key={item.id}>
          <span>{item.name}</span>
          <button onClick={() => onUpdate(item.id)}>
            更新
          </button>
        </div>
      ))}
    </div>
  );
});

function App() {
  const [data, setData] = useState([]);
  const [count, setCount] = useState(0);

  /** ❌ 每次渲染都建立新函式 */
  const handleUpdate = (id) => {
    setData(data.map(item => 
      item.id === id ? { ...item, updated: true } : item
    ));
  };

  /** ✅ 使用 useCallback 最佳化 */
  const handleUpdateOptimized = useCallback((id) => {
    setData(prevData => prevData.map(item => 
      item.id === id ? { ...item, updated: true } : item
    ));
  }, []);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        計數：{count}
      </button>
      <ExpensiveComponent 
        data={data} 
        onUpdate={handleUpdateOptimized}
      />
    </div>
  );
}
```

### 2. Props 穩定性

```jsx
function ParentComponent() {
  const [count, setCount] = useState(0);

  /** ❌ 每次渲染都建立新物件 */
  const badConfig = {
    theme: 'dark',
    size: 'large'
  };

  /** ✅ 穩定的物件參考 */
  const goodConfig = useMemo(() => ({
    theme: 'dark',
    size: 'large'
  }), []);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        計數：{count}
      </button>
      <ChildComponent config={goodConfig} />
    </div>
  );
}

const ChildComponent = React.memo(function ChildComponent({ config }) {
  console.log('ChildComponent 渲染');
  return <div>主題：{config.theme}</div>;
});
```

<br />

## 實際應用模式

### 1. 表單資料流

```jsx
function ContactForm({ onSubmit, initialData = {} }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
    ...initialData
  });

  const handleChange = (field) => (e) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormField
        label="姓名"
        value={formData.name}
        onChange={handleChange('name')}
      />
      <FormField
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleChange('email')}
      />
      <FormField
        label="訊息"
        as="textarea"
        value={formData.message}
        onChange={handleChange('message')}
      />
      <button type="submit">送出</button>
    </form>
  );
}

function FormField({ label, as = 'input', ...props }) {
  const Component = as;

  return (
    <div>
      <label>{label}</label>
      <Component {...props} />
    </div>
  );
}
```

### 2. 購物車系統

```jsx
function ShoppingCart({ items, onUpdateQuantity, onRemoveItem }) {
  const total = items.reduce((sum, item) => 
    sum + (item.price * item.quantity), 0
  );

  return (
    <div>
      <h2>購物車</h2>
      {items.map(item => (
        <CartItem
          key={item.id}
          item={item}
          onUpdateQuantity={onUpdateQuantity}
          onRemove={onRemoveItem}
        />
      ))}
      <div>總計：NT$ {total.toLocaleString()}</div>
    </div>
  );
}

function CartItem({ item, onUpdateQuantity, onRemove }) {
  return (
    <div>
      <span>{item.name}</span>
      <span>NT$ {item.price}</span>
      <input
        type="number"
        value={item.quantity}
        onChange={(e) => onUpdateQuantity(item.id, parseInt(e.target.value))}
        min="1"
      />
      <button onClick={() => onRemove(item.id)}>
        移除
      </button>
    </div>
  );
}

function App() {
  const [cartItems, setCartItems] = useState([]);

  const updateQuantity = (id, quantity) => {
    setCartItems(items =>
      items.map(item =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  };

  const removeItem = (id) => {
    setCartItems(items => items.filter(item => item.id !== id));
  };

  return (
    <ShoppingCart
      items={cartItems}
      onUpdateQuantity={updateQuantity}
      onRemoveItem={removeItem}
    />
  );
}
```

<br />

## 最佳實務

- 保持 Props 簡潔：避免傳遞過多不必要的資料

- 使用解構賦值：提高程式碼可讀性

- 提供預設值：增加元件的健壯性

- 避免 Props Drilling：考慮使用 Context 或狀態管理庫

- 使用 TypeScript：提供型別檢查和更好的開發體驗

- 最佳化 Callback Function：使用 useCallback 避免不必要的重新渲染

- 保持資料流清晰：狀態應該放在需要的最小共同父元件中

- 文件化 Props 介面：使用 PropTypes 或 TypeScript 定義清楚的介面
