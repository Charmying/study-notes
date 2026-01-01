# 3.1.4 列表渲染：`map()` 與 `key` 屬性的重要性

<br />

## 基本概念

列表渲染是將陣列資料轉換為 JSX 元素的過程，主要使用 JavaScript 的 `map()` 方法來實現動態內容顯示。

<br />

## 基本 `map()` 語法

### 1. 簡單陣列渲染

```jsx
function FruitList() {
  const fruits = ['蘋果', '香蕉', '橘子', '葡萄'];

  return (
    <ul>
      {fruits.map((fruit, index) => (
        <li key={index}>{fruit}</li>
      ))}
    </ul>
  );
}
```

### 2. 數字陣列處理

```jsx
function NumberList() {
  const numbers = [1, 2, 3, 4, 5];

  return (
    <div>
      {numbers.map(number => (
        <span key={number} className="number-badge">
          {number}
        </span>
      ))}
    </div>
  );
}
```

<br />

## 物件陣列渲染

### 1. 基本物件列表

```jsx
function UserList() {
  const users = [
    { id: 1, name: 'Charmy', email: 'charmy@example.com' },
    { id: 2, name: 'Tina', email: 'tina@example.com' },
  ];

  return (
    <div>
      {users.map(user => (
        <div key={user.id} className="user-card">
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      ))}
    </div>
  );
}
```

### 2. 複雜物件結構

```jsx
function ProductGrid() {
  const products = [
    {
      id: 1,
      name: '筆記型電腦',
      price: 34500,
      category: '電腦',
      inStock: true,
      image: 'laptop.jpg'
    },
    {
      id: 2,
      name: '無線滑鼠',
      price: 2980,
      category: '配件',
      inStock: false,
      image: 'mouse.jpg'
    }
  ];

  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>
          <p className="category">{product.category}</p>
          <p className="price">NT$ {product.price.toLocaleString()}</p>
          <span className={`stock ${product.inStock ? 'in-stock' : 'out-stock'}`}>
            {product.inStock ? '有庫存' : '缺貨'}
          </span>
        </div>
      ))}
    </div>
  );
}
```

<br />

## `key` 屬性的重要性

### 1. 為什麼需要 `key`

```jsx
/** React 使用 key 來識別哪些項目已更改、新增或移除 */
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input type="checkbox" checked={todo.completed} />
          <span>{todo.text}</span>
        </li>
      ))}
    </ul>
  );
}
```

### 2. 正確的 `key` 選擇

```jsx
function MessageList({ messages }) {
  return (
    <div>
      {messages.map(message => (
        /** ✅ 使用唯一且穩定的 ID */
        <div key={message.id} className="message">
          <strong>{message.sender}:</strong>
          <p>{message.content}</p>
          <small>{message.timestamp}</small>
        </div>
      ))}
    </div>
  );
}
```

### 3. 避免使用 index 作為 `key`

```jsx
/** ❌ 不建議：當列表順序改變時會有問題 */
function BadExample({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item.name}</li>
      ))}
    </ul>
  );
}

/** ✅ 建議：使用穩定的唯一識別符 */
function GoodExample({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

<br />

## 進階列表渲染技巧

### 1. 條件式列表項目

```jsx
function FilteredList({ items, showCompleted }) {
  return (
    <ul>
      {items
        .filter(item => showCompleted || !item.completed)
        .map(item => (
          <li key={item.id} className={item.completed ? 'completed' : ''}>
            {item.text}
          </li>
        ))}
    </ul>
  );
}
```

### 2. 排序與分組

```jsx
function SortedProductList({ products, sortBy }) {
  const sortedProducts = [...products].sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });

  return (
    <div>
      {sortedProducts.map(product => (
        <div key={product.id} className="product-item">
          <h4>{product.name}</h4>
          <p>NT$ {product.price}</p>
        </div>
      ))}
    </div>
  );
}
```

### 3. 巢狀列表渲染

```jsx
function CategoryList({ categories }) {
  return (
    <div>
      {categories.map(category => (
        <div key={category.id} className="category">
          <h2>{category.name}</h2>
          <ul>
            {category.items.map(item => (
              <li key={item.id}>
                <span>{item.name}</span>
                <span>NT$ {item.price}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
```

<br />

## 實務應用範例

### 1. 表格渲染

```jsx
function DataTable({ data, columns }) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map(column => (
            <th key={column.key}>{column.title}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id}>
            {columns.map(column => (
              <td key={`${row.id}-${column.key}`}>
                {row[column.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### 2. 卡片網格

```jsx
function CardGrid({ cards }) {
  return (
    <div className="card-grid">
      {cards.map(card => (
        <div key={card.id} className="card">
          <div className="card-header">
            <h3>{card.title}</h3>
            <span className="card-date">{card.date}</span>
          </div>
          <div className="card-body">
            <p>{card.description}</p>
          </div>
          <div className="card-footer">
            {card.tags.map(tag => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 3. 導航選單

```jsx
function Navigation({ menuItems }) {
  return (
    <nav>
      <ul className="nav-menu">
        {menuItems.map(item => (
          <li key={item.id} className="nav-item">
            <a href={item.url} className="nav-link">
              {item.icon && <span className="nav-icon">{item.icon}</span>}
              {item.label}
            </a>
            {item.children && (
              <ul className="sub-menu">
                {item.children.map(child => (
                  <li key={child.id}>
                    <a href={child.url}>{child.label}</a>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

<br />

## 效能最佳化

### 1. 使用 React.memo 避免不必要的重新渲染

```jsx
const ListItem = React.memo(function ListItem({ item, onUpdate }) {
  return (
    <div className="list-item">
      <span>{item.name}</span>
      <button onClick={() => onUpdate(item.id)}>
        更新
      </button>
    </div>
  );
});

function OptimizedList({ items, onUpdateItem }) {
  return (
    <div>
      {items.map(item => (
        <ListItem 
          key={item.id} 
          item={item} 
          onUpdate={onUpdateItem}
        />
      ))}
    </div>
  );
}
```

### 2. 虛擬化長列表

```jsx
function VirtualizedList({ items, itemHeight = 50, containerHeight = 400 }) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );

  const visibleItems = items.slice(startIndex, endIndex);

  return (
    <div 
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        {visibleItems.map((item, index) => (
          <div
            key={item.id}
            style={{
              position: 'absolute',
              top: (startIndex + index) * itemHeight,
              height: itemHeight,
              width: '100%'
            }}
          >
            {item.name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

<br />

## 常見錯誤與解決方案

### 1. 缺少 `key` 屬性

```jsx
/** ❌ 錯誤：缺少 key 屬性 */
function BadList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li>{item.name}</li> // 缺少 key
      ))}
    </ul>
  );
}

/** ✅ 正確：添加 key 屬性 */
function GoodList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### 2. 直接修改原陣列

```jsx
/** ❌ 錯誤：直接修改原陣列 */
function BadSort({ items }) {
  return (
    <ul>
      {items.sort().map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

/** ✅ 正確：建立新陣列 */
function GoodSort({ items }) {
  return (
    <ul>
      {[...items].sort().map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### 3. 在 map 中使用 index 作為 `key` 的問題

```jsx
/** 當列表項目順序改變時，React 無法正確追蹤元素 */
function ProblematicList({ items, onRemove }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>
          <input type="text" defaultValue={item.name} />
          <button onClick={() => onRemove(index)}>移除</button>
        </li>
      ))}
    </ul>
  );
}
```

<br />

## 最佳實務

-  總是提供 `key` 屬性：確保列表項目能被正確追蹤

-  使用穩定且唯一的 key：避免使用陣列索引

-  保持 `key` 的一致性：同一項目的 `key` 不應改變

-  避免在 render 中進行複雜運算：將排序、過濾提取到 `useMemo`

-  考慮效能影響：長列表使用虛擬化技術

-  不要直接修改原陣列：使用展開運算子或其他方法建立新陣列
