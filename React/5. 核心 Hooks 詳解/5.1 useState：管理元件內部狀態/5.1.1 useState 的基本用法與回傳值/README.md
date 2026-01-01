# 5.1.1 `useState` 的基本用法與回傳值

<br />

## 基本概念

`useState` 是 React 最基本的 Hook，用於在函式元件中管理狀態。每次呼叫 `useState` 都會回傳一個陣列，包含目前的狀態值和更新狀態的函式。

### 1. 基本語法

```jsx
import React, { useState } from 'react';

function BasicExample() {
  /** 宣告狀態變數，初始值為 0 */
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>目前計數：{count}</p>
      <button onClick={() => setCount(count + 1)}>
        增加
      </button>
    </div>
  );
}
```

### 2. 回傳值解構

```jsx
function StateDestructuring() {
  /** useState 回傳陣列 [狀態值, 更新函式] */
  const stateArray = useState('初始值');
  const value = stateArray[0];
  const setValue = stateArray[1];

  /** 等同於解構賦值 */
  const [state, setState] = useState('初始值');

  return (
    <div>
      <p>值：{state}</p>
      <button onClick={() => setState('新值')}>
        更新
      </button>
    </div>
  );
}
```

<br />

## 不同資料類型的狀態

### 1. 基本資料類型

```jsx
function PrimitiveTypes() {
  const [text, setText] = useState('');
  const [number, setNumber] = useState(0);
  const [boolean, setBoolean] = useState(false);
  const [nullValue, setNullValue] = useState(null);
  const [undefinedValue, setUndefinedValue] = useState(undefined);

  return (
    <div>
      <div>
        <label>文字：</label>
        <input 
          value={text} 
          onChange={(e) => setText(e.target.value)} 
        />
        <p>目前值：{text}</p>
      </div>

      <div>
        <label>數字：</label>
        <input 
          type="number" 
          value={number} 
          onChange={(e) => setNumber(Number(e.target.value))} 
        />
        <p>目前值：{number}</p>
      </div>

      <div>
        <label>
          <input 
            type="checkbox" 
            checked={boolean} 
            onChange={(e) => setBoolean(e.target.checked)} 
          />
          布林值：{boolean.toString()}
        </label>
      </div>

      <div>
        <button onClick={() => setNullValue('不再是 null')}>
          Null 值：{nullValue === null ? 'null' : nullValue}
        </button>
      </div>

      <div>
        <button onClick={() => setUndefinedValue('已定義')}>
          Undefined 值：{undefinedValue === undefined ? 'undefined' : undefinedValue}
        </button>
      </div>
    </div>
  );
}
```

### 2. 物件狀態

```jsx
function ObjectState() {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0
  });

  const updateName = (newName) => {
    setUser(prevUser => ({
      ...prevUser,
      name: newName
    }));
  };

  const updateEmail = (newEmail) => {
    setUser(prevUser => ({
      ...prevUser,
      email: newEmail
    }));
  };

  const updateAge = (newAge) => {
    setUser(prevUser => ({
      ...prevUser,
      age: newAge
    }));
  };

  return (
    <div>
      <div>
        <input 
          placeholder="姓名"
          value={user.name}
          onChange={(e) => updateName(e.target.value)}
        />
      </div>

      <div>
        <input 
          placeholder="Email"
          value={user.email}
          onChange={(e) => updateEmail(e.target.value)}
        />
      </div>

      <div>
        <input 
          type="number"
          placeholder="年齡"
          value={user.age}
          onChange={(e) => updateAge(Number(e.target.value))}
        />
      </div>

      <div>
        <h3>使用者資訊：</h3>
        <p>姓名：{user.name}</p>
        <p>Email：{user.email}</p>
        <p>年齡：{user.age}</p>
      </div>
    </div>
  );
}
```

### 3. 陣列狀態

```jsx
function ArrayState() {
  const [items, setItems] = useState(['項目 1', '項目 2']);
  const [newItem, setNewItem] = useState('');

  const addItem = () => {
    if (newItem.trim()) {
      setItems(prevItems => [...prevItems, newItem]);
      setNewItem('');
    }
  };

  const removeItem = (index) => {
    setItems(prevItems => prevItems.filter((_, i) => i !== index));
  };

  const updateItem = (index, newValue) => {
    setItems(prevItems => 
      prevItems.map((item, i) => i === index ? newValue : item)
    );
  };

  return (
    <div>
      <div>
        <input 
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="新增項目"
        />
        <button onClick={addItem}>新增</button>
      </div>

      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <input 
              value={item}
              onChange={(e) => updateItem(index, e.target.value)}
            />
            <button onClick={() => removeItem(index)}>刪除</button>
          </li>
        ))}
      </ul>

      <p>總計：{items.length} 個項目</p>
    </div>
  );
}
```

<br />

## 初始值設定

### 1. 靜態初始值

```jsx
function StaticInitialValue() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('歡迎');
  const [user, setUser] = useState({ name: 'Guest', role: 'visitor' });
  const [tags, setTags] = useState(['React', 'JavaScript']);

  return (
    <div>
      <p>計數：{count}</p>
      <p>訊息：{message}</p>
      <p>使用者：{user.name} ({user.role})</p>
      <p>標籤：{tags.join(', ')}</p>
    </div>
  );
}
```

### 2. 動態初始值

```jsx
function DynamicInitialValue() {
  /** 從 localStorage 讀取初始值 */
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });

  /** 從 URL 參數讀取初始值 */
  const [searchQuery, setSearchQuery] = useState(() => {
    const params = new URLSearchParams(window.location.search);
    return params.get('q') || '';
  });

  /** 計算初始值 */
  const [randomId, setRandomId] = useState(() => {
    return Math.random().toString(36).substr(2, 9);
  });

  /** 從 props 計算初始值 */
  const [formData, setFormData] = useState(() => {
    return {
      timestamp: new Date().toISOString(),
      sessionId: randomId
    };
  });

  return (
    <div>
      <p>主題：{theme}</p>
      <p>搜尋查詢：{searchQuery}</p>
      <p>隨機 ID：{randomId}</p>
      <p>表單資料：{JSON.stringify(formData, null, 2)}</p>
    </div>
  );
}
```

### 3. 延遲初始化

```jsx
function LazyInitialization() {
  /** 昂貴的初始化計算 */
  const expensiveCalculation = () => {
    console.log('執行昂貴的計算...');
    let result = 0;
    for (let i = 0; i < 1000000; i++) {
      result += i;
    }
    return result;
  };

  /** ❌ 每次渲染都會執行計算 */
  const [badValue, setBadValue] = useState(expensiveCalculation());

  /** ✅ 只在初始化時執行一次 */
  const [goodValue, setGoodValue] = useState(() => expensiveCalculation());

  /** 從 API 載入初始資料 */
  const [userData, setUserData] = useState(() => {
    const cached = sessionStorage.getItem('userData');
    return cached ? JSON.parse(cached) : null;
  });

  return (
    <div>
      <p>不良初始化：{badValue}</p>
      <p>良好初始化：{goodValue}</p>
      <p>使用者資料：{userData ? userData.name : '載入中...'}</p>
    </div>
  );
}
```

<br />

## 狀態更新函式

### 1. 直接設定值

```jsx
function DirectValueUpdate() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');

  const increment = () => {
    setCount(count + 1);
  };

  const decrement = () => {
    setCount(count - 1);
  };

  const reset = () => {
    setCount(0);
    setMessage('已重設');
  };

  return (
    <div>
      <p>計數：{count}</p>
      <p>訊息：{message}</p>

      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
      <button onClick={reset}>重設</button>
    </div>
  );
}
```

### 2. 函式式更新

```jsx
function FunctionalUpdate() {
  const [count, setCount] = useState(0);

  const increment = () => {
    /** 使用前一個狀態值 */
    setCount(prevCount => prevCount + 1);
  };

  const incrementTwice = () => {
    /** 函式式更新確保正確的狀態 */
    setCount(prevCount => prevCount + 1);
    setCount(prevCount => prevCount + 1);
  };

  const multiplyByTwo = () => {
    setCount(prevCount => prevCount * 2);
  };

  return (
    <div>
      <p>計數：{count}</p>

      <button onClick={increment}>+1</button>
      <button onClick={incrementTwice}>+2 (函式式)</button>
      <button onClick={multiplyByTwo}>×2</button>
    </div>
  );
}
```

### 3. 批次更新

```jsx
function BatchedUpdates() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');

  const handleMultipleUpdates = () => {
    /** React 會自動批次處理這些更新 */
    setCount(count + 1);
    setMessage('計數已更新');

    console.log('更新後的 count:', count); // 仍然是舊值
  };

  const handleAsyncUpdates = () => {
    setTimeout(() => {
      /** 在 React 18 中，這些也會被批次處理 */
      setCount(prevCount => prevCount + 1);
      setMessage('非同步更新');
    }, 1000);
  };

  return (
    <div>
      <p>計數：{count}</p>
      <p>訊息：{message}</p>

      <button onClick={handleMultipleUpdates}>
        多重更新
      </button>
      <button onClick={handleAsyncUpdates}>
        非同步更新
      </button>
    </div>
  );
}
```

<br />

## 實際應用範例

### 1. 表單狀態管理

```jsx
function FormStateManagement() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field) => (e) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value
    }));

    /** 清除該欄位的錯誤 */
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username) newErrors.username = '使用者名稱為必填';
    if (!formData.email) newErrors.email = 'Email 為必填';
    if (!formData.password) newErrors.password = '密碼為必填';
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = '密碼確認不符合';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      /** 模擬 API 呼叫 */
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('表單送出：', formData);

      /** 重設表單 */
      setFormData({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      });
    } catch (error) {
      console.error('送出失敗：', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          placeholder="使用者名稱"
          value={formData.username}
          onChange={handleInputChange('username')}
        />
        {errors.username && <span className="error">{errors.username}</span>}
      </div>

      <div>
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleInputChange('email')}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="密碼"
          value={formData.password}
          onChange={handleInputChange('password')}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="確認密碼"
          value={formData.confirmPassword}
          onChange={handleInputChange('confirmPassword')}
        />
        {errors.confirmPassword && <span className="error">{errors.confirmPassword}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '送出中...' : '送出'}
      </button>
    </form>
  );
}
```

### 2. 計數器與計時器

```jsx
function CounterAndTimer() {
  const [count, setCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    let interval = null;

    if (isRunning) {
      interval = setInterval(() => {
        setElapsedTime(Date.now() - startTime);
      }, 10);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRunning, startTime]);

  const startTimer = () => {
    setStartTime(Date.now() - elapsedTime);
    setIsRunning(true);
  };

  const stopTimer = () => {
    setIsRunning(false);
  };

  const resetTimer = () => {
    setElapsedTime(0);
    setIsRunning(false);
    setStartTime(null);
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60000);
    const seconds = Math.floor((time % 60000) / 1000);
    const milliseconds = Math.floor((time % 1000) / 10);

    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(2, '0')}`;
  };

  return (
    <div>
      <div>
        <h3>計數器</h3>
        <p>計數：{count}</p>
        <button onClick={() => setCount(prev => prev + 1)}>+</button>
        <button onClick={() => setCount(prev => prev - 1)}>-</button>
        <button onClick={() => setCount(0)}>重設</button>
      </div>

      <div>
        <h3>計時器</h3>
        <p>時間：{formatTime(elapsedTime)}</p>
        <button onClick={startTimer} disabled={isRunning}>開始</button>
        <button onClick={stopTimer} disabled={!isRunning}>停止</button>
        <button onClick={resetTimer}>重設</button>
      </div>
    </div>
  );
}
```

<br />

## 常見錯誤與最佳實務

### 1. 狀態更新的非同步性

```jsx
function AsyncStateUpdate() {
  const [count, setCount] = useState(0);

  const handleIncrement = () => {
    console.log('更新前:', count);
    setCount(count + 1);
    console.log('更新後:', count); // 仍然是舊值！
  };

  const handleIncrementCorrect = () => {
    setCount(prevCount => {
      console.log('更新前:', prevCount);
      const newCount = prevCount + 1;
      console.log('更新後:', newCount);
      return newCount;
    });
  };

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={handleIncrement}>錯誤方式</button>
      <button onClick={handleIncrementCorrect}>正確方式</button>
    </div>
  );
}
```

### 2. 物件與陣列的不可變更新

```jsx
function ImmutableUpdates() {
  const [user, setUser] = useState({ name: 'John', age: 30 });
  const [items, setItems] = useState(['a', 'b', 'c']);

  /** ❌ 錯誤：直接修改物件 */
  const updateUserWrong = () => {
    user.age = 31;
    setUser(user); // React 不會重新渲染
  };

  /** ✅ 正確：建立新物件 */
  const updateUserCorrect = () => {
    setUser(prevUser => ({
      ...prevUser,
      age: prevUser.age + 1
    }));
  };

  /** ❌ 錯誤：直接修改陣列 */
  const addItemWrong = () => {
    items.push('d');
    setItems(items); // React 不會重新渲染
  };

  /** ✅ 正確：建立新陣列 */
  const addItemCorrect = () => {
    setItems(prevItems => [...prevItems, 'd']);
  };

  return (
    <div>
      <p>使用者：{user.name}, 年齡：{user.age}</p>
      <button onClick={updateUserCorrect}>增加年齡</button>

      <p>項目：{items.join(', ')}</p>
      <button onClick={addItemCorrect}>新增項目</button>
    </div>
  );
}
```

<br />

## 最佳實務總結

### 1. 狀態設計原則

- 最小化狀態：只儲存必要的狀態

- 單一資料來源：避免重複的狀態

- 正規化結構：複雜資料使用扁平結構

- 分離關注點：不相關的狀態分開管理

### 2. 更新模式

- 函式式更新：依賴前一個狀態時使用

- 不可變更新：物件和陣列使用展開運算子

- 批次更新：React 自動批次處理同步更新

- 延遲初始化：昂貴計算使用函式初始化

### 3. 效能考量

- 避免不必要的重新渲染：使用 `React.memo`

- 狀態結構最佳化：避免過深的嵌套

- 計算值快取：使用 `useMemo` 快取計算結果

- 回調函式最佳化：使用 `useCallback` 避免重新建立
