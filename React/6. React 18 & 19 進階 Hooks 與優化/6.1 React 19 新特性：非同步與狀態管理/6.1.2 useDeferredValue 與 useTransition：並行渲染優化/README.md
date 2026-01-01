# 6.1.2 `useDeferredValue` 與 `useTransition`：並行渲染優化

<br />

## 概述

`useDeferredValue` 和 `useTransition` 是 React 18 引入的並行渲染 Hooks，用於優化使用者體驗。這兩個 Hook 允許開發者控制更新的優先級，讓緊急更新 (例如：使用者輸入) 優先於非緊急更新 (例如：搜尋結果)，避免介面卡頓。

<br />

## `useDeferredValue`

### 基本語法

```jsx
const deferredValue = useDeferredValue(value)
```

### 參數說明

- `value`: 要延遲的值

- 回傳值: 延遲版本的值

### 基本範例

```jsx
import { useDeferredValue, useState } from 'react';

function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);

  /** 使用延遲的查詢進行搜尋 */
  const results = useSearch(deferredQuery);

  return (
    <div>
      {results.map(item => (
        <div key={item.id}>{item.title}</div>
      ))}
    </div>
  );
}

function App() {
  const [query, setQuery] = useState('');

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜尋..."
      />
      <SearchResults query={query} />
    </div>
  );
}
```

### 實際應用：搜尋功能

```jsx
function SearchApp() {
  const [searchTerm, setSearchTerm] = useState('');
  const deferredSearchTerm = useDeferredValue(searchTerm);

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="輸入搜尋關鍵字"
      />
      <SearchResults query={deferredSearchTerm} />
    </div>
  );
}

function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }

    setLoading(true);
    searchAPI(query)
      .then(setResults)
      .finally(() => setLoading(false));
  }, [query]);

  if (loading) return <div>搜尋中...</div>;

  return (
    <ul>
      {results.map(result => (
        <li key={result.id}>{result.title}</li>
      ))}
    </ul>
  );
}
```

<br />

## `useTransition`

### 基本語法

```jsx
const [isPending, startTransition] = useTransition()
```

### 回傳值說明

- `isPending`: 布林值，表示是否有轉換正在進行

- `startTransition`: 函式，用於標記狀態更新為非緊急

### 基本範例

```jsx
import { useTransition, useState } from 'react';

function TabContainer() {
  const [activeTab, setActiveTab] = useState('tab1');
  const [isPending, startTransition] = useTransition();

  const handleTabClick = (tab) => {
    startTransition(() => {
      setActiveTab(tab);
    });
  };

  return (
    <div>
      <div className="tabs">
        <button 
          onClick={() => handleTabClick('tab1')}
          className={activeTab === 'tab1' ? 'active' : ''}
        >
          標籤 1
        </button>
        <button 
          onClick={() => handleTabClick('tab2')}
          className={activeTab === 'tab2' ? 'active' : ''}
        >
          標籤 2
        </button>
      </div>

      {isPending && <div>載入中...</div>}

      <div className="tab-content">
        {activeTab === 'tab1' && <ExpensiveComponent1 />}
        {activeTab === 'tab2' && <ExpensiveComponent2 />}
      </div>
    </div>
  );
}
```

### 實際應用：列表過濾

```jsx
function FilterableList({ items }) {
  const [filter, setFilter] = useState('');
  const [filteredItems, setFilteredItems] = useState(items);
  const [isPending, startTransition] = useTransition();

  const handleFilterChange = (value) => {
    setFilter(value);

    startTransition(() => {
      const filtered = items.filter(item => 
        item.name.toLowerCase().includes(value.toLowerCase())
      );
      setFilteredItems(filtered);
    });
  };

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => handleFilterChange(e.target.value)}
        placeholder="過濾項目"
      />

      {isPending && <div>更新中...</div>}

      <ul style={{ opacity: isPending ? 0.7 : 1 }}>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 組合使用

### 搜尋與過濾組合

```jsx
function AdvancedSearch() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('all');
  const [results, setResults] = useState([]);

  const deferredQuery = useDeferredValue(query);
  const [isPending, startTransition] = useTransition();

  const handleCategoryChange = (newCategory) => {
    startTransition(() => {
      setCategory(newCategory);
    });
  };

  useEffect(() => {
    if (deferredQuery) {
      searchAPI(deferredQuery, category).then(setResults);
    }
  }, [deferredQuery, category]);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜尋..."
      />

      <select 
        value={category} 
        onChange={(e) => handleCategoryChange(e.target.value)}
      >
        <option value="all">全部</option>
        <option value="articles">文章</option>
        <option value="videos">影片</option>
      </select>

      {isPending && <div>更新分類中...</div>}

      <div style={{ opacity: isPending ? 0.7 : 1 }}>
        {results.map(result => (
          <div key={result.id}>{result.title}</div>
        ))}
      </div>
    </div>
  );
}
```

### 資料表格優化

```jsx
function DataTable({ data }) {
  const [sortField, setSortField] = useState('name');
  const [sortDirection, setSortDirection] = useState('asc');
  const [searchTerm, setSearchTerm] = useState('');

  const deferredSearchTerm = useDeferredValue(searchTerm);
  const [isPending, startTransition] = useTransition();

  const handleSort = (field) => {
    startTransition(() => {
      if (sortField === field) {
        setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
      } else {
        setSortField(field);
        setSortDirection('asc');
      }
    });
  };

  const processedData = useMemo(() => {
    let filtered = data;

    if (deferredSearchTerm) {
      filtered = data.filter(item => 
        item.name.toLowerCase().includes(deferredSearchTerm.toLowerCase())
      );
    }

    return filtered.sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (sortDirection === 'asc') {
        return aVal > bVal ? 1 : -1;
      }
      return aVal < bVal ? 1 : -1;
    });
  }, [data, deferredSearchTerm, sortField, sortDirection]);

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="搜尋資料"
      />

      {isPending && <div>排序中...</div>}

      <table style={{ opacity: isPending ? 0.7 : 1 }}>
        <thead>
          <tr>
            <th onClick={() => handleSort('name')}>名稱</th>
            <th onClick={() => handleSort('age')}>年齡</th>
            <th onClick={() => handleSort('email')}>電子郵件</th>
          </tr>
        </thead>
        <tbody>
          {processedData.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.age}</td>
              <td>{item.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

<br />

## 效能比較

### 沒有優化的版本

```jsx
function SlowSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    /** 每次輸入都會立即觸發搜尋 */
    if (query) {
      expensiveSearch(query).then(setResults);
    }
  }, [query]);

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <div>{results.length} 個結果</div>
    </div>
  );
}
```

### 使用 `useDeferredValue` 優化

```jsx
function OptimizedSearch() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const [results, setResults] = useState([]);

  useEffect(() => {
    /** 只有當延遲的查詢改變時才搜尋 */
    if (deferredQuery) {
      expensiveSearch(deferredQuery).then(setResults);
    }
  }, [deferredQuery]);

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <div>{results.length} 個結果</div>
    </div>
  );
}
```

<br />

## 最佳實踐

### 1. 適當的使用場景

```jsx
/** ✅ 適合使用 useDeferredValue */
function SearchComponent() {
  const [input, setInput] = useState('');
  const deferredInput = useDeferredValue(input);

  /** 搜尋結果不需要立即更新 */
  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <ExpensiveSearchResults query={deferredInput} />
    </div>
  );
}

/** ✅ 適合使用 useTransition */
function NavigationComponent() {
  const [currentPage, setCurrentPage] = useState('home');
  const [isPending, startTransition] = useTransition();

  const navigate = (page) => {
    startTransition(() => {
      setCurrentPage(page); // 頁面切換可以延遲
    });
  };

  return (
    <div>
      <button onClick={() => navigate('profile')}>個人資料</button>
      {isPending && <div>載入中...</div>}
      <PageContent page={currentPage} />
    </div>
  );
}
```

### 2. 避免過度使用

```jsx
/** ❌ 不適合：簡單的狀態更新 */
function Counter() {
  const [count, setCount] = useState(0);
  const [isPending, startTransition] = useTransition();

  const increment = () => {
    startTransition(() => {
      setCount(c => c + 1); // 不需要延遲
    });
  };

  return <button onClick={increment}>{count}</button>;
}

/** ✅ 正確：直接更新 */
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      {count}
    </button>
  );
}
```

### 3. 提供視覺回饋

```jsx
function LoadingStateExample() {
  const [data, setData] = useState([]);
  const [isPending, startTransition] = useTransition();

  const loadData = () => {
    startTransition(() => {
      fetchData().then(setData);
    });
  };

  return (
    <div>
      <button onClick={loadData} disabled={isPending}>
        {isPending ? '載入中...' : '載入資料'}
      </button>

      <div style={{ 
        opacity: isPending ? 0.5 : 1,
        transition: 'opacity 0.2s'
      }}>
        {data.map(item => <div key={item.id}>{item.name}</div>)}
      </div>
    </div>
  );
}
```

<br />

## 注意事項

### 1. 瀏覽器支援

```jsx
/** 檢查是否支援並行功能 */
function FeatureCheck() {
  const isSupported = typeof startTransition === 'function';

  if (!isSupported) {
    return <div>瀏覽器不支援並行渲染功能</div>;
  }

  return <OptimizedComponent />;
}
```

### 2. 記憶體使用

```jsx
/** 避免在 useDeferredValue 中使用大型物件 */
function MemoryOptimized({ largeData }) {
  const [filter, setFilter] = useState('');

  /** ✅ 只延遲簡單的值 */
  const deferredFilter = useDeferredValue(filter);

  /** ❌ 避免延遲大型物件 */
  // const deferredLargeData = useDeferredValue(largeData);

  const filteredData = useMemo(() => {
    return largeData.filter(item => 
      item.name.includes(deferredFilter)
    );
  }, [largeData, deferredFilter]);

  return (
    <div>
      <input 
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      {filteredData.map(item => <div key={item.id}>{item.name}</div>)}
    </div>
  );
}
```

<br />

## 總結

### `useDeferredValue` vs `useTransition`

| 特性 | `useDeferredValue` | `useTransition` |
| - | - | - |
| 用途 | 延遲值的更新 | 標記狀態更新為非緊急 |
| 回傳值 | 延遲的值 | `[isPending, startTransition]` |
| 適用場景 | 搜尋、過濾 | 導航、標籤切換 |
| 控制方式 | 自動延遲 | 手動包裝更新 |

### 主要優勢

- 改善使用者體驗：避免介面卡頓

- 優先級控制：緊急更新優先處理

- 視覺回饋：提供載入狀態指示

- 效能優化：減少不必要的重新渲染

### 使用建議

- 在搜尋功能中使用 `useDeferredValue`

- 在頁面導航中使用 `useTransition`

- 提供適當的載入狀態指示

- 避免在簡單操作中過度使用

- 考慮瀏覽器支援度和效能影響

這兩個 Hook 是 React 並行渲染的核心工具，正確使用可以顯著提升應用程式的使用者體驗。
