# 6.1.4 React 19 Compiler (React Forget)：自動記憶化簡介

<br />

## 概述

React 19 Compiler (原名 React Forget) 是 React 團隊開發的編譯時優化工具，能夠自動為 React 元件添加記憶化 (memoization) 優化。這個編譯器分析程式碼並自動插入 `useMemo`、`useCallback` 和 `React.memo`，減少開發者手動優化的負擔。

<br />

## 主要特性

### 1. 自動記憶化

```jsx
/** 原始程式碼 */
function ExpensiveComponent({ items, filter }) {
  const filteredItems = items.filter(item => 
    item.category === filter
  );

  const total = filteredItems.reduce((sum, item) => 
    sum + item.price, 0
  );

  return (
    <div>
      <p>總計: ${total}</p>
      <ul>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}

/** React Compiler 自動優化後 */
function ExpensiveComponent({ items, filter }) {
  const filteredItems = useMemo(() => 
    items.filter(item => item.category === filter),
    [items, filter]
  );

  const total = useMemo(() => 
    filteredItems.reduce((sum, item) => sum + item.price, 0),
    [filteredItems]
  );

  return (
    <div>
      <p>總計: ${total}</p>
      <ul>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### 2. 自動函式記憶化

```jsx
/** 原始程式碼 */
function TodoList({ todos, onToggle, onDelete }) {
  const handleToggle = (id) => {
    onToggle(id);
  };

  const handleDelete = (id) => {
    onDelete(id);
  };

  return (
    <ul>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
}

/** React Compiler 自動優化後 */
function TodoList({ todos, onToggle, onDelete }) {
  const handleToggle = useCallback((id) => {
    onToggle(id);
  }, [onToggle]);

  const handleDelete = useCallback((id) => {
    onDelete(id);
  }, [onDelete]);

  return (
    <ul>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
}
```

### 3. 元件記憶化

```jsx
/** 原始程式碼 */
function UserCard({ user, theme }) {
  return (
    <div className={`card ${theme}`}>
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

/** React Compiler 自動優化後 */
const UserCard = React.memo(function UserCard({ user, theme }) {
  return (
    <div className={`card ${theme}`}>
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});
```

<br />

## 實際應用範例

### 複雜計算優化

```jsx
/** 原始程式碼 */
function DataAnalytics({ data, filters }) {
  const processedData = data
    .filter(item => filters.categories.includes(item.category))
    .filter(item => item.date >= filters.startDate && item.date <= filters.endDate)
    .map(item => ({
      ...item,
      normalizedValue: item.value / 100
    }));

  const statistics = {
    total: processedData.length,
    sum: processedData.reduce((acc, item) => acc + item.normalizedValue, 0),
    average: processedData.length > 0 
      ? processedData.reduce((acc, item) => acc + item.normalizedValue, 0) / processedData.length 
      : 0
  };

  const chartData = processedData.map(item => ({
    x: item.date,
    y: item.normalizedValue
  }));

  return (
    <div>
      <StatsPanel stats={statistics} />
      <Chart data={chartData} />
    </div>
  );
}

/** React Compiler 自動優化後 */
function DataAnalytics({ data, filters }) {
  const processedData = useMemo(() => 
    data
      .filter(item => filters.categories.includes(item.category))
      .filter(item => item.date >= filters.startDate && item.date <= filters.endDate)
      .map(item => ({
        ...item,
        normalizedValue: item.value / 100
      })),
    [data, filters.categories, filters.startDate, filters.endDate]
  );

  const statistics = useMemo(() => ({
    total: processedData.length,
    sum: processedData.reduce((acc, item) => acc + item.normalizedValue, 0),
    average: processedData.length > 0 
      ? processedData.reduce((acc, item) => acc + item.normalizedValue, 0) / processedData.length 
      : 0
  }), [processedData]);

  const chartData = useMemo(() => 
    processedData.map(item => ({
      x: item.date,
      y: item.normalizedValue
    })),
    [processedData]
  );

  return (
    <div>
      <StatsPanel stats={statistics} />
      <Chart data={chartData} />
    </div>
  );
}
```

### 事件處理優化

```jsx
/** 原始程式碼 */
function SearchableList({ items, onItemClick, onItemSelect }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItems, setSelectedItems] = useState([]);

  const filteredItems = items.filter(item => 
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleItemClick = (item) => {
    onItemClick(item);
  };

  const handleItemSelect = (item) => {
    const newSelection = selectedItems.includes(item.id)
      ? selectedItems.filter(id => id !== item.id)
      : [...selectedItems, item.id];
    setSelectedItems(newSelection);
    onItemSelect(newSelection);
  };

  const handleSelectAll = () => {
    const allIds = filteredItems.map(item => item.id);
    setSelectedItems(allIds);
    onItemSelect(allIds);
  };

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="搜尋..."
      />
      <button onClick={handleSelectAll}>全選</button>
      <ul>
        {filteredItems.map(item => (
          <ListItem
            key={item.id}
            item={item}
            isSelected={selectedItems.includes(item.id)}
            onClick={handleItemClick}
            onSelect={handleItemSelect}
          />
        ))}
      </ul>
    </div>
  );
}

/** React Compiler 自動優化後 */
function SearchableList({ items, onItemClick, onItemSelect }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItems, setSelectedItems] = useState([]);

  const filteredItems = useMemo(() => 
    items.filter(item => 
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    ),
    [items, searchTerm]
  );

  const handleItemClick = useCallback((item) => {
    onItemClick(item);
  }, [onItemClick]);

  const handleItemSelect = useCallback((item) => {
    const newSelection = selectedItems.includes(item.id)
      ? selectedItems.filter(id => id !== item.id)
      : [...selectedItems, item.id];
    setSelectedItems(newSelection);
    onItemSelect(newSelection);
  }, [selectedItems, onItemSelect]);

  const handleSelectAll = useCallback(() => {
    const allIds = filteredItems.map(item => item.id);
    setSelectedItems(allIds);
    onItemSelect(allIds);
  }, [filteredItems, onItemSelect]);

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="搜尋..."
      />
      <button onClick={handleSelectAll}>全選</button>
      <ul>
        {filteredItems.map(item => (
          <ListItem
            key={item.id}
            item={item}
            isSelected={selectedItems.includes(item.id)}
            onClick={handleItemClick}
            onSelect={handleItemSelect}
          />
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 編譯器設定

### Babel 配置

```json
{
  "presets": ["@babel/preset-react"],
  "plugins": [
    ["babel-plugin-react-compiler", {
      "runtimeModule": "react-compiler-runtime"
    }]
  ]
}
```

### Webpack 配置

```jsx
module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react'],
            plugins: [
              ['babel-plugin-react-compiler', {
                sources: (filename) => {
                  return filename.indexOf('node_modules') === -1;
                }
              }]
            ]
          }
        }
      }
    ]
  }
};
```

### Vite 配置

```jsx
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      babel: {
        plugins: [
          ['babel-plugin-react-compiler', {
            runtimeModule: 'react-compiler-runtime'
          }]
        ]
      }
    })
  ]
});
```

<br />

## 優化策略

### 1. 依賴分析

```jsx
/** 編譯器能夠正確分析依賴 */
function SmartComponent({ a, b, c }) {
  /** 只依賴 a 和 b */
  const result1 = a + b;

  /** 只依賴 b 和 c */
  const result2 = b * c;

  /** 依賴 result1 和 result2 */
  const finalResult = result1 + result2;

  return <div>{finalResult}</div>;
}

/** 編譯器自動優化 */
function SmartComponent({ a, b, c }) {
  const result1 = useMemo(() => a + b, [a, b]);
  const result2 = useMemo(() => b * c, [b, c]);
  const finalResult = useMemo(() => result1 + result2, [result1, result2]);

  return <div>{finalResult}</div>;
}
```

### 2. 條件式渲染優化

```jsx
/** 原始程式碼 */
function ConditionalComponent({ showDetails, user, stats }) {
  const userInfo = {
    name: user.name,
    email: user.email,
    joinDate: new Date(user.createdAt).toLocaleDateString()
  };

  const processedStats = stats.map(stat => ({
    ...stat,
    percentage: (stat.value / stat.total) * 100
  }));

  return (
    <div>
      <UserBasicInfo info={userInfo} />
      {showDetails && (
        <UserDetailedStats stats={processedStats} />
      )}
    </div>
  );
}

/** React Compiler 優化 */
function ConditionalComponent({ showDetails, user, stats }) {
  const userInfo = useMemo(() => ({
    name: user.name,
    email: user.email,
    joinDate: new Date(user.createdAt).toLocaleDateString()
  }), [user.name, user.email, user.createdAt]);

  /** 只在 showDetails 為 true 時才計算 */
  const processedStats = useMemo(() => {
    if (!showDetails) return null;
    return stats.map(stat => ({
      ...stat,
      percentage: (stat.value / stat.total) * 100
    }));
  }, [showDetails, stats]);

  return (
    <div>
      <UserBasicInfo info={userInfo} />
      {showDetails && processedStats && (
        <UserDetailedStats stats={processedStats} />
      )}
    </div>
  );
}
```

<br />

## 效能影響

### 測試結果比較

```jsx
/** 效能測試範例 */
function PerformanceTest() {
  const [count, setCount] = useState(0);
  const [items] = useState(() => 
    Array.from({ length: 10000 }, (_, i) => ({ id: i, value: Math.random() }))
  );

  /** 沒有 React Compiler */
  /** 每次重新渲染時都會重新計算 */
  const expensiveCalculation = items
    .filter(item => item.value > 0.5)
    .reduce((sum, item) => sum + item.value, 0);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
      <p>結果: {expensiveCalculation}</p>
    </div>
  );
}

/** 使用 React Compiler 後 */
/** 只有當 items 改變時才會重新計算 */
function PerformanceTest() {
  const [count, setCount] = useState(0);
  const [items] = useState(() => 
    Array.from({ length: 10000 }, (_, i) => ({ id: i, value: Math.random() }))
  );

  const expensiveCalculation = useMemo(() => 
    items
      .filter(item => item.value > 0.5)
      .reduce((sum, item) => sum + item.value, 0),
    [items]
  );

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
      <p>結果: {expensiveCalculation}</p>
    </div>
  );
}
```

<br />

## 限制與注意事項

### 1. 不支援的模式

```jsx
/** ❌ 動態屬性存取 */
function UnsupportedPattern({ data }) {
  const key = 'dynamicKey';
  const value = data[key]; // 編譯器無法優化

  return <div>{value}</div>;
}

/** ❌ eval 或動態程式碼執行 */
function UnsupportedEval({ code }) {
  const result = eval(code); // 不支援
  return <div>{result}</div>;
}

/** ✅ 支援的模式 */
function SupportedPattern({ data }) {
  const value = data.staticKey; // 可以優化
  return <div>{value}</div>;
}
```

### 2. 副作用處理

```jsx
/** ❌ 副作用無法被正確追蹤 */
function ComponentWithSideEffect({ onMount }) {
  const data = processData(); // 如果有副作用，可能不會被優化

  useEffect(() => {
    onMount();
  }, []);

  return <div>{data}</div>;
}

/** ✅ 明確的純函式 */
function PureComponent({ input }) {
  const result = pureFunction(input); // 可以被優化
  return <div>{result}</div>;
}
```

### 3. 編譯時警告

```jsx
/** 編譯器會發出警告 */
function ComponentWithWarning({ items }) {
  /** 警告：無法優化的計算 */
  const result = items.map(item => {
    // 複雜的副作用
    console.log(item); // 副作用
    return item.value * Math.random(); // 非純函式
  });

  return <div>{result.join(', ')}</div>;
}
```

<br />

## 最佳實踐

### 1. 編寫純函式元件

```jsx
/** ✅ 純函式元件更容易被優化 */
function PureCalculation({ numbers }) {
  const sum = numbers.reduce((a, b) => a + b, 0);
  const average = sum / numbers.length;

  return (
    <div>
      <p>總和: {sum}</p>
      <p>平均: {average}</p>
    </div>
  );
}

/** ❌ 避免不必要的副作用 */
function ImpureCalculation({ numbers }) {
  console.log('Calculating...'); // 副作用
  const sum = numbers.reduce((a, b) => a + b, 0);

  return <div>{sum}</div>;
}
```

### 2. 使用穩定的參考

```jsx
/** ✅ 穩定的物件參考 */
const DEFAULT_OPTIONS = { sort: 'asc', limit: 10 };

function DataList({ items, options = DEFAULT_OPTIONS }) {
  const processedItems = items
    .sort((a, b) => options.sort === 'asc' ? a.id - b.id : b.id - a.id)
    .slice(0, options.limit);

  return (
    <ul>
      {processedItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

/** ❌ 不穩定的物件參考 */
function DataList({ items, options }) {
  /** 每次都建立新物件 */
  const defaultOptions = { sort: 'asc', limit: 10 };
  const finalOptions = { ...defaultOptions, ...options };

  return <div>{/* ... */}</div>;
}
```

<br />

## 總結

### 主要優勢

- 自動優化：無需手動添加 `useMemo` 和 `useCallback`

- 減少程式碼量：簡化元件程式碼結構

- 效能提升：自動識別和優化性能瓶頸

- 減少錯誤：避免手動優化的常見錯誤

### 使用建議

- 編寫純函式元件以獲得最佳優化

- 避免不必要的副作用和動態程式碼

- 使用穩定的物件參考和預設值

- 關注編譯器警告和建議

- 在開發環境中測試效能影響

### 未來展望

- React 19 正式版本將內建編譯器支援

- 更智能的依賴分析和優化策略

- 更好的開發工具和除錯支援

- 與其他 React 特性的深度整合

React 19 Compiler 代表了 React 效能優化的重大進步，將大幅減少開發者的優化負擔，同時提供更一致的效能表現。
