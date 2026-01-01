# 5.2.2 依賴陣列的作用與陷阱 (Closure Problem)

<br />

## 依賴陣列基本概念

依賴陣列決定 `useEffect` 何時重新執行。React 會比較依賴陣列中的每個值，只有當值發生變化時才會重新執行 Effect。

### 1. 依賴陣列的比較機制

```jsx
function DependencyComparison() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('Charmy');
  const [user, setUser] = useState({ id: 1, name: 'Charmy' });

  /** 基本類型比較 - 值比較 */
  useEffect(() => {
    console.log('count 變化:', count);
  }, [count]);

  /** 字串比較 - 值比較 */
  useEffect(() => {
    console.log('name 變化:', name);
  }, [name]);

  /** 物件比較 - 參考比較 */
  useEffect(() => {
    console.log('user 變化:', user);
  }, [user]);

  const updateUserName = () => {
    /** 建立新物件，會觸發 Effect */
    setUser(prev => ({ ...prev, name: 'Tina' }));
  };

  const updateUserSameReference = () => {
    /** 修改同一個物件，不會觸發 Effect */
    user.name = 'Charlie';
    setUser(user); // 相同參考，Effect 不會執行
  };

  return (
    <div>
      <p>計數：{count}</p>
      <p>姓名：{name}</p>
      <p>使用者：{user.name}</p>

      <button onClick={() => setCount(count + 1)}>增加計數</button>
      <button onClick={() => setName(name === 'Charmy' ? 'Tina' : 'Charmy')}>
        切換姓名
      </button>
      <button onClick={updateUserName}>更新使用者 (新物件)</button>
      <button onClick={updateUserSameReference}>更新使用者 (同參考)</button>
    </div>
  );
}
```

### 2. 依賴陣列的不同形式

```jsx
function DependencyArrayForms() {
  const [count, setCount] = useState(0);
  const [multiplier, setMultiplier] = useState(2);

  /** 1. 無依賴陣列 - 每次渲染都執行 */
  useEffect(() => {
    console.log('1. 每次渲染都執行');
  });

  /** 2. 空依賴陣列 - 只執行一次 */
  useEffect(() => {
    console.log('2. 只在掛載時執行');
  }, []);

  /** 3. 單一依賴 */
  useEffect(() => {
    console.log('3. count 變化時執行:', count);
  }, [count]);

  /** 4. 多個依賴 */
  useEffect(() => {
    console.log('4. count 或 multiplier 變化時執行');
  }, [count, multiplier]);

  /** 5. 計算值作為依賴 */
  const result = count * multiplier;
  useEffect(() => {
    console.log('5. 計算結果變化時執行:', result);
  }, [result]);

  return (
    <div>
      <p>計數：{count}</p>
      <p>乘數：{multiplier}</p>
      <p>結果：{result}</p>

      <button onClick={() => setCount(count + 1)}>增加計數</button>
      <button onClick={() => setMultiplier(multiplier + 1)}>增加乘數</button>
    </div>
  );
}
```

<br />

## 閉包問題 (Closure Problem)

閉包問題是指 Effect 中的變數可能會「困住」舊的值，導致行為不如預期。

### 1. 基本閉包問題

```jsx
function BasicClosureProblem() {
  const [count, setCount] = useState(0);

  /** ❌ 問題：閉包困住舊的 count 值 */
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('定時器中的 count:', count); // 永遠是 0
      setCount(count + 1); // 永遠是 0 + 1 = 1
    }, 1000);

    return () => clearInterval(timer);
  }, []); // 空依賴陣列導致閉包問題

  return (
    <div>
      <p>計數：{count}</p>
      <p>這個計數器只會從 0 增加到 1，然後停止</p>
    </div>
  );
}
```

### 2. 解決閉包問題的方法

```jsx
function ClosureSolutions() {
  const [count, setCount] = useState(0);

  /** 解決方案 1：添加依賴 */
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('方案 1 - count:', count);
      setCount(count + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [count]); // 添加 count 作為依賴

  /** 解決方案 2：使用函式式更新 */
  useEffect(() => {
    const timer = setInterval(() => {
      setCount(prevCount => {
        console.log('方案 2 - prevCount:', prevCount);
        return prevCount + 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []); // 可以保持空依賴陣列

  /** 解決方案 3：使用 useRef 保存最新值 */
  const countRef = useRef(count);
  countRef.current = count;

  useEffect(() => {
    const timer = setInterval(() => {
      console.log('方案 3 - countRef.current:', countRef.current);
      setCount(countRef.current + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []); // 空依賴陣列，但透過 ref 獲取最新值

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={() => setCount(0)}>重設</button>
    </div>
  );
}
```

### 3. 複雜閉包問題範例

```jsx
function ComplexClosureProblem() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  /** ❌ 問題：多個狀態的閉包問題 */
  useEffect(() => {
    const processItems = () => {
      console.log('處理項目，當前狀態:');
      console.log('items:', items.length);
      console.log('filter:', filter);
      console.log('searchTerm:', searchTerm);

      /** 這些值可能是過時的 */
      let filtered = items;

      if (filter !== 'all') {
        filtered = items.filter(item => item.category === filter);
      }

      if (searchTerm) {
        filtered = filtered.filter(item => 
          item.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      console.log('過濾後的項目數量:', filtered.length);
    };

    const timer = setInterval(processItems, 2000);
    return () => clearInterval(timer);
  }, []); // 空依賴陣列導致閉包問題

  /** ✅ 解決方案：包含所有依賴 */
  useEffect(() => {
    const processItems = () => {
      console.log('正確處理項目，當前狀態:');
      console.log('items:', items.length);
      console.log('filter:', filter);
      console.log('searchTerm:', searchTerm);

      let filtered = items;

      if (filter !== 'all') {
        filtered = items.filter(item => item.category === filter);
      }

      if (searchTerm) {
        filtered = filtered.filter(item => 
          item.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      console.log('正確過濾後的項目數量:', filtered.length);
    };

    const timer = setInterval(processItems, 2000);
    return () => clearInterval(timer);
  }, [items, filter, searchTerm]); // 包含所有依賴

  const addItem = () => {
    const newItem = {
      id: Date.now(),
      name: `項目 ${items.length + 1}`,
      category: Math.random() > 0.5 ? 'A' : 'B'
    };
    setItems(prev => [...prev, newItem]);
  };

  return (
    <div>
      <div>
        <button onClick={addItem}>新增項目</button>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">全部</option>
          <option value="A">分類 A</option>
          <option value="B">分類 B</option>
        </select>
        <input 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="搜尋項目"
        />
      </div>

      <p>項目總數：{items.length}</p>
      <p>目前篩選：{filter}</p>
      <p>搜尋詞：{searchTerm}</p>

      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} (分類: {item.category})
          </li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 函式作為依賴的問題

### 1. 函式依賴導致的無限迴圈

```jsx
function FunctionDependencyProblem() {
  const [count, setCount] = useState(0);
  const [data, setData] = useState(null);

  /** ❌ 問題：每次渲染都建立新函式 */
  const fetchData = async () => {
    console.log('獲取資料，count:', count);
    const response = await fetch(`/api/data?count=${count}`);
    const result = await response.json();
    setData(result);
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]); // fetchData 每次都是新函式，導致無限迴圈

  return (
    <div>
      <p>計數：{count}</p>
      <p>資料：{data ? JSON.stringify(data) : '無'}</p>
      <button onClick={() => setCount(count + 1)}>增加計數</button>
    </div>
  );
}
```

### 2. 使用 `useCallback` 解決函式依賴問題

```jsx
function FunctionDependencySolution() {
  const [count, setCount] = useState(0);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  /** ✅ 解決方案：使用 useCallback 穩定函式參考 */
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      console.log('獲取資料，count:', count);
      /** 模擬 API 呼叫 */
      await new Promise(resolve => setTimeout(resolve, 1000));
      const mockData = { count, timestamp: Date.now() };
      setData(mockData);
    } catch (error) {
      console.error('獲取資料失敗:', error);
    } finally {
      setLoading(false);
    }
  }, [count]); // 只有 count 變化時才建立新函式

  useEffect(() => {
    fetchData();
  }, [fetchData]); // 現在 fetchData 是穩定的

  return (
    <div>
      <p>計數：{count}</p>
      <p>載入中：{loading ? '是' : '否'}</p>
      <p>資料：{data ? JSON.stringify(data) : '無'}</p>
      <button onClick={() => setCount(count + 1)}>增加計數</button>
    </div>
  );
}
```

### 3. 將函式移到 Effect 內部

```jsx
function FunctionInsideEffect() {
  const [userId, setUserId] = useState(1);
  const [userData, setUserData] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    /** ✅ 將函式定義在 Effect 內部 */
    const fetchUserData = async () => {
      try {
        const userResponse = await fetch(`/api/users/${userId}`);
        const user = await userResponse.json();
        setUserData(user);

        const postsResponse = await fetch(`/api/users/${userId}/posts`);
        const userPosts = await postsResponse.json();
        setPosts(userPosts);
      } catch (error) {
        console.error('獲取使用者資料失敗:', error);
      }
    };

    fetchUserData();
  }, [userId]); // 只需要依賴 userId

  return (
    <div>
      <div>
        <label>使用者 ID：</label>
        <input 
          type="number"
          value={userId}
          onChange={(e) => setUserId(Number(e.target.value))}
          min="1"
        />
      </div>

      {userData && (
        <div>
          <h3>使用者：{userData.name}</h3>
          <p>Email：{userData.email}</p>
        </div>
      )}

      <div>
        <h4>文章 ({posts.length})</h4>
        <ul>
          {posts.map(post => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

<br />

## 物件和陣列依賴的陷阱

### 1. 物件依賴問題

```jsx
function ObjectDependencyTrap() {
  const [user, setUser] = useState({ name: 'Charmy', age: 25 });
  const [settings, setSettings] = useState({ theme: 'light', lang: 'zh-TW' });

  /** ❌ 問題：每次渲染都建立新物件 */
  const config = {
    user: user.name,
    theme: settings.theme,
    timestamp: Date.now() // 每次都不同！
  };

  useEffect(() => {
    console.log('配置變化:', config);
  }, [config]); // config 每次都是新物件，導致每次都執行

  /** ✅ 解決方案 1：使用 useMemo */
  const stableConfig = useMemo(() => ({
    user: user.name,
    theme: settings.theme
    // 移除 timestamp 或使其穩定
  }), [user.name, settings.theme]);

  useEffect(() => {
    console.log('穩定配置變化:', stableConfig);
  }, [stableConfig]);

  /** ✅ 解決方案 2：直接依賴原始值 */
  useEffect(() => {
    const config = {
      user: user.name,
      theme: settings.theme
    };
    console.log('直接依賴原始值:', config);
  }, [user.name, settings.theme]);

  return (
    <div>
      <div>
        <input 
          value={user.name}
          onChange={(e) => setUser(prev => ({ ...prev, name: e.target.value }))}
          placeholder="使用者名稱"
        />
      </div>

      <div>
        <select 
          value={settings.theme}
          onChange={(e) => setSettings(prev => ({ ...prev, theme: e.target.value }))}
        >
          <option value="light">淺色</option>
          <option value="dark">深色</option>
        </select>
      </div>
    </div>
  );
}
```

### 2. 陣列依賴問題

```jsx
function ArrayDependencyTrap() {
  const [items, setItems] = useState(['a', 'b', 'c']);
  const [filter, setFilter] = useState('');

  /** ❌ 問題：每次渲染都建立新陣列 */
  const filteredItems = items.filter(item => 
    item.toLowerCase().includes(filter.toLowerCase())
  );

  useEffect(() => {
    console.log('過濾項目變化:', filteredItems);
  }, [filteredItems]); // 每次都是新陣列

  /** ✅ 解決方案：使用 useMemo */
  const stableFilteredItems = useMemo(() => 
    items.filter(item => 
      item.toLowerCase().includes(filter.toLowerCase())
    ), [items, filter]
  );

  useEffect(() => {
    console.log('穩定過濾項目變化:', stableFilteredItems);
  }, [stableFilteredItems]);

  const addItem = () => {
    const newItem = String.fromCharCode(97 + items.length); // a, b, c, d...
    setItems(prev => [...prev, newItem]);
  };

  const removeLastItem = () => {
    setItems(prev => prev.slice(0, -1));
  };

  return (
    <div>
      <div>
        <input 
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="過濾項目"
        />
        <button onClick={addItem}>新增項目</button>
        <button onClick={removeLastItem}>移除最後項目</button>
      </div>

      <div>
        <p>所有項目：{items.join(', ')}</p>
        <p>過濾項目：{stableFilteredItems.join(', ')}</p>
      </div>
    </div>
  );
}
```

<br />

## 實際應用中的依賴管理

### 1. API 呼叫的依賴管理

```jsx
function APICallDependencies() {
  const [userId, setUserId] = useState(1);
  const [postId, setPostId] = useState(null);
  const [userData, setUserData] = useState(null);
  const [postData, setPostData] = useState(null);
  const [loading, setLoading] = useState(false);

  /** 獲取使用者資料 */
  useEffect(() => {
    if (!userId) return;

    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await fetch(`/api/users/${userId}`);
        const user = await response.json();
        setUserData(user);
      } catch (error) {
        console.error('獲取使用者失敗:', error);
        setUserData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]); // 只依賴 userId

  /** 獲取文章資料 */
  useEffect(() => {
    if (!postId) {
      setPostData(null);
      return;
    }

    const fetchPost = async () => {
      setLoading(true);
      try {
        const response = await fetch(`/api/posts/${postId}`);
        const post = await response.json();
        setPostData(post);
      } catch (error) {
        console.error('獲取文章失敗:', error);
        setPostData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [postId]); // 只依賴 postId

  return (
    <div>
      <div>
        <label>使用者 ID：</label>
        <input 
          type="number"
          value={userId}
          onChange={(e) => setUserId(Number(e.target.value))}
          min="1"
        />
      </div>

      <div>
        <label>文章 ID：</label>
        <input 
          type="number"
          value={postId || ''}
          onChange={(e) => setPostId(e.target.value ? Number(e.target.value) : null)}
          min="1"
        />
      </div>

      {loading && <p>載入中...</p>}

      {userData && (
        <div>
          <h3>使用者資料</h3>
          <p>姓名：{userData.name}</p>
          <p>Email：{userData.email}</p>
        </div>
      )}

      {postData && (
        <div>
          <h3>文章資料</h3>
          <p>標題：{postData.title}</p>
          <p>內容：{postData.content}</p>
        </div>
      )}
    </div>
  );
}
```

### 2. 複雜表單的依賴管理

```jsx
function ComplexFormDependencies() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    country: '',
    city: ''
  });

  const [countries, setCountries] = useState([]);
  const [cities, setCities] = useState([]);
  const [validation, setValidation] = useState({});

  /** 載入國家列表 */
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch('/api/countries');
        const data = await response.json();
        setCountries(data);
      } catch (error) {
        console.error('載入國家失敗:', error);
      }
    };

    fetchCountries();
  }, []); // 只執行一次

  /** 當國家變化時載入城市列表 */
  useEffect(() => {
    if (!formData.country) {
      setCities([]);
      return;
    }

    const fetchCities = async () => {
      try {
        const response = await fetch(`/api/countries/${formData.country}/cities`);
        const data = await response.json();
        setCities(data);
      } catch (error) {
        console.error('載入城市失敗:', error);
        setCities([]);
      }
    };

    fetchCities();
  }, [formData.country]); // 只依賴國家

  /** 當國家變化時清除城市選擇 */
  useEffect(() => {
    if (formData.city && !cities.some(city => city.id === formData.city)) {
      setFormData(prev => ({ ...prev, city: '' }));
    }
  }, [cities, formData.city]); // 依賴城市列表和目前選擇的城市

  /** 表單驗證 */
  useEffect(() => {
    const newValidation = {};

    if (!formData.name.trim()) {
      newValidation.name = '姓名為必填';
    }

    if (!formData.email.trim()) {
      newValidation.email = 'Email 為必填';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newValidation.email = 'Email 格式不正確';
    }

    if (!formData.country) {
      newValidation.country = '請選擇國家';
    }

    if (!formData.city) {
      newValidation.city = '請選擇城市';
    }

    setValidation(newValidation);
  }, [formData]); // 依賴整個表單資料

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const isFormValid = Object.keys(validation).length === 0;

  return (
    <div>
      <div>
        <input 
          value={formData.name}
          onChange={(e) => updateFormData('name', e.target.value)}
          placeholder="姓名"
        />
        {validation.name && <span className="error">{validation.name}</span>}
      </div>

      <div>
        <input 
          type="email"
          value={formData.email}
          onChange={(e) => updateFormData('email', e.target.value)}
          placeholder="Email"
        />
        {validation.email && <span className="error">{validation.email}</span>}
      </div>

      <div>
        <select 
          value={formData.country}
          onChange={(e) => updateFormData('country', e.target.value)}
        >
          <option value="">選擇國家</option>
          {countries.map(country => (
            <option key={country.id} value={country.id}>
              {country.name}
            </option>
          ))}
        </select>
        {validation.country && <span className="error">{validation.country}</span>}
      </div>

      <div>
        <select 
          value={formData.city}
          onChange={(e) => updateFormData('city', e.target.value)}
          disabled={!formData.country}
        >
          <option value="">選擇城市</option>
          {cities.map(city => (
            <option key={city.id} value={city.id}>
              {city.name}
            </option>
          ))}
        </select>
        {validation.city && <span className="error">{validation.city}</span>}
      </div>

      <button disabled={!isFormValid}>
        送出表單
      </button>

      <div>
        <h4>表單狀態：</h4>
        <p>有效：{isFormValid ? '是' : '否'}</p>
        <p>錯誤數量：{Object.keys(validation).length}</p>
      </div>
    </div>
  );
}
```

<br />

## 最佳實務與工具

### 1. ESLint 規則

```jsx
/** .eslintrc.js */
module.exports = {
  extends: [
    'react-app',
    'react-app/jest'
  ],
  rules: {
    /** 強制檢查 useEffect 依賴 */
    'react-hooks/exhaustive-deps': 'error'
  }
};

function ESLintExample() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  /** ESLint 會警告缺少 name 依賴 */
  useEffect(() => {
    console.log(`${name}: ${count}`);
  }, [count]); // 缺少 name 依賴

  /** 正確的依賴 */
  useEffect(() => {
    console.log(`${name}: ${count}`);
  }, [count, name]); // 包含所有依賴

  return (
    <div>
      <input 
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="姓名"
      />
      <p>計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>增加</button>
    </div>
  );
}
```

### 2. 自定義 Hook 簡化依賴管理

```jsx
/** 自定義 Hook 封裝複雜的依賴處理 */
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]); // 清楚的依賴關係

  return debouncedValue;
}

function useAPI(url, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    const abortController = new AbortController();

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url, {
          signal: abortController.signal
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => {
      abortController.abort();
    };
  }, [url, ...dependencies]); // 動態依賴

  return { data, loading, error };
}

/** 使用自定義 Hook */
function CustomHookExample() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('all');

  const debouncedQuery = useDebounce(query, 500);

  const { data, loading, error } = useAPI(
    debouncedQuery ? `/api/search?q=${debouncedQuery}&category=${category}` : null,
    [debouncedQuery, category]
  );

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜尋..."
      />

      <select 
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      >
        <option value="all">全部</option>
        <option value="posts">文章</option>
        <option value="users">使用者</option>
      </select>

      {loading && <p>搜尋中...</p>}
      {error && <p>錯誤：{error}</p>}
      {data && (
        <div>
          <p>找到 {data.length} 個結果</p>
          <ul>
            {data.map(item => (
              <li key={item.id}>{item.title}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

<br />

## 總結

### 依賴陣列原則

- 包含所有依賴：Effect 中使用的所有變數都應該在依賴陣列中

- 避免過度依賴：不要包含不必要的依賴

- 使用 ESLint 規則：自動檢查依賴完整性

- 理解比較機制：React 使用 `Object.is` 比較依賴

### 閉包問題解決方案

- 函式式更新：使用 `setState(prev => ...)` 避免依賴舊狀態

- `useCallback`：穩定函式參考

- `useMemo`：穩定物件和陣列參考

- `useRef`：保存最新值的參考

### 最佳實務

- 分離關注點：不同的副作用使用不同的 `useEffect`

- 自定義 Hook：封裝複雜的依賴處理

- 工具輔助：使用 ESLint 規則檢查依賴

- 測試驗證：編寫測試確保依賴正確性
