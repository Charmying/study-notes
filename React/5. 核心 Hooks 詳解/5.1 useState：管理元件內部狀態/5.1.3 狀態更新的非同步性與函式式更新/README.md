# 5.1.3 狀態更新的非同步性與函式式更新

## 狀態更新的非同步性

React 狀態更新是非同步的，這意味著呼叫 `setState` 後，狀態值不會立即改變。React 會批次處理狀態更新以提升效能。

### 1. 基本非同步行為

```jsx
function AsyncStateExample() {
  const [count, setCount] = useState(0);

  const handleIncrement = () => {
    console.log('更新前:', count);
    setCount(count + 1);
    console.log('更新後:', count); // 仍然是舊值！
  };

  const handleMultipleUpdates = () => {
    console.log('初始值:', count);
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
    console.log('三次更新後:', count); // 仍然是舊值
    // 實際上只會增加 1，因為都是基於相同的舊值
  };

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={handleIncrement}>增加 1</button>
      <button onClick={handleMultipleUpdates}>增加 3 (錯誤方式)</button>
    </div>
  );
}
```

### 2. 狀態更新時機

```jsx
function UpdateTimingExample() {
  const [value, setValue] = useState(0);
  const [log, setLog] = useState([]);

  const addLog = (message) => {
    setLog(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const handleUpdate = () => {
    addLog(`更新前 value: ${value}`);

    setValue(value + 1);
    addLog(`setState 呼叫後 value: ${value}`); // 仍然是舊值

    /** 使用 setTimeout 查看更新後的值 */
    setTimeout(() => {
      addLog(`setTimeout 中 value: ${value}`); // 仍然是舊值 (閉包)
    }, 0);
  };

  /** 使用 useEffect 觀察狀態變化 */
  useEffect(() => {
    addLog(`useEffect 中 value: ${value}`);
  }, [value]);

  return (
    <div>
      <p>目前值：{value}</p>
      <button onClick={handleUpdate}>更新值</button>
      <button onClick={() => setLog([])}>清除記錄</button>

      <div>
        <h4>執行記錄：</h4>
        <ul>
          {log.map((entry, index) => (
            <li key={index}>{entry}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

### 3. 批次更新行為

```jsx
function BatchingExample() {
  const [count, setCount] = useState(0);
  const [flag, setFlag] = useState(false);
  const [renderCount, setRenderCount] = useState(0);

  /** 追蹤渲染次數 */
  useEffect(() => {
    setRenderCount(prev => prev + 1);
  });

  const handleSyncUpdates = () => {
    console.log('同步更新開始');
    setCount(count + 1);
    setFlag(!flag);
    console.log('同步更新結束');
    // React 會批次處理這兩個更新，只觸發一次重新渲染
  };

  const handleAsyncUpdates = () => {
    console.log('非同步更新開始');
    setTimeout(() => {
      setCount(count + 1);
      setFlag(!flag);
      // 在 React 18 中，這些也會被批次處理
    }, 0);
    console.log('非同步更新結束');
  };

  const handlePromiseUpdates = () => {
    Promise.resolve().then(() => {
      setCount(count + 1);
      setFlag(!flag);
      // 在 React 18 中，Promise 中的更新也會被批次處理
    });
  };

  return (
    <div>
      <p>計數：{count}</p>
      <p>旗標：{flag.toString()}</p>
      <p>渲染次數：{renderCount}</p>

      <button onClick={handleSyncUpdates}>同步更新</button>
      <button onClick={handleAsyncUpdates}>非同步更新</button>
      <button onClick={handlePromiseUpdates}>Promise 更新</button>
      <button onClick={() => setRenderCount(0)}>重設渲染計數</button>
    </div>
  );
}
```

<br />

## 函式式更新

函式式更新允許基於前一個狀態值來計算新的狀態值，解決了非同步更新帶來的問題。

### 1. 基本函式式更新

```jsx
function FunctionalUpdateBasics() {
  const [count, setCount] = useState(0);

  const incrementCorrect = () => {
    /** 使用函式式更新，基於前一個狀態值 */
    setCount(prevCount => prevCount + 1);
  };

  const incrementMultiple = () => {
    /** 多次函式式更新會正確累加 */
    setCount(prevCount => prevCount + 1);
    setCount(prevCount => prevCount + 1);
    setCount(prevCount => prevCount + 1);
  };

  const incrementByAmount = (amount) => {
    setCount(prevCount => prevCount + amount);
  };

  const doubleValue = () => {
    setCount(prevCount => prevCount * 2);
  };

  const resetToZero = () => {
    setCount(0); // 直接設定值也是可以的
  };

  return (
    <div>
      <p>計數：{count}</p>

      <button onClick={incrementCorrect}>+1</button>
      <button onClick={incrementMultiple}>+3 (正確方式)</button>
      <button onClick={() => incrementByAmount(5)}>+5</button>
      <button onClick={doubleValue}>×2</button>
      <button onClick={resetToZero}>重設</button>
    </div>
  );
}
```

### 2. 複雜狀態的函式式更新

```jsx
function ComplexFunctionalUpdate() {
  const [user, setUser] = useState({
    name: 'John',
    age: 30,
    score: 0,
    achievements: []
  });

  const incrementAge = () => {
    setUser(prevUser => ({
      ...prevUser,
      age: prevUser.age + 1
    }));
  };

  const addScore = (points) => {
    setUser(prevUser => ({
      ...prevUser,
      score: prevUser.score + points
    }));
  };

  const addAchievement = (achievement) => {
    setUser(prevUser => ({
      ...prevUser,
      achievements: [...prevUser.achievements, achievement]
    }));
  };

  const levelUp = () => {
    setUser(prevUser => {
      const newLevel = Math.floor(prevUser.score / 100) + 1;
      return {
        ...prevUser,
        score: prevUser.score + 50,
        achievements: [...prevUser.achievements, `達到等級 ${newLevel}`]
      };
    });
  };

  const resetProgress = () => {
    setUser(prevUser => ({
      ...prevUser,
      score: 0,
      achievements: []
    }));
  };

  return (
    <div>
      <h3>使用者資訊</h3>
      <p>姓名：{user.name}</p>
      <p>年齡：{user.age}</p>
      <p>分數：{user.score}</p>
      <p>成就：{user.achievements.length} 個</p>

      <div>
        <button onClick={incrementAge}>增加年齡</button>
        <button onClick={() => addScore(10)}>+10 分</button>
        <button onClick={() => addAchievement('新成就')}>新增成就</button>
        <button onClick={levelUp}>升級</button>
        <button onClick={resetProgress}>重設進度</button>
      </div>

      <div>
        <h4>成就列表：</h4>
        <ul>
          {user.achievements.map((achievement, index) => (
            <li key={index}>{achievement}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

### 3. 陣列的函式式更新

```jsx
function ArrayFunctionalUpdate() {
  const [items, setItems] = useState(['項目 1', '項目 2']);
  const [history, setHistory] = useState([]);

  const addItem = () => {
    const newItem = `項目 ${items.length + 1}`;

    setItems(prevItems => [...prevItems, newItem]);
    setHistory(prevHistory => [...prevHistory, `新增: ${newItem}`]);
  };

  const removeLastItem = () => {
    setItems(prevItems => {
      if (prevItems.length === 0) return prevItems;

      const removedItem = prevItems[prevItems.length - 1];
      setHistory(prevHistory => [...prevHistory, `移除: ${removedItem}`]);

      return prevItems.slice(0, -1);
    });
  };

  const shuffleItems = () => {
    setItems(prevItems => {
      const shuffled = [...prevItems].sort(() => Math.random() - 0.5);
      setHistory(prevHistory => [...prevHistory, '重新排序']);
      return shuffled;
    });
  };

  const reverseItems = () => {
    setItems(prevItems => {
      const reversed = [...prevItems].reverse();
      setHistory(prevHistory => [...prevHistory, '反轉順序']);
      return reversed;
    });
  };

  const clearAll = () => {
    setItems([]);
    setHistory(prevHistory => [...prevHistory, '清除所有項目']);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div>
      <div>
        <h3>項目列表 ({items.length})</h3>
        <ul>
          {items.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>

      <div>
        <button onClick={addItem}>新增項目</button>
        <button onClick={removeLastItem}>移除最後項目</button>
        <button onClick={shuffleItems}>隨機排序</button>
        <button onClick={reverseItems}>反轉順序</button>
        <button onClick={clearAll}>清除全部</button>
      </div>

      <div>
        <h4>操作歷史</h4>
        <button onClick={clearHistory}>清除歷史</button>
        <ul>
          {history.map((action, index) => (
            <li key={index}>{action}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

<br />

## 實際應用場景

### 1. 計數器與累加器

```jsx
function CounterAccumulator() {
  const [count, setCount] = useState(0);
  const [total, setTotal] = useState(0);
  const [operations, setOperations] = useState([]);

  const addOperation = (operation, value) => {
    setOperations(prev => [...prev, { operation, value, timestamp: Date.now() }]);
  };

  const increment = () => {
    setCount(prev => prev + 1);
    setTotal(prev => prev + 1);
    addOperation('增加', 1);
  };

  const decrement = () => {
    setCount(prev => prev - 1);
    setTotal(prev => prev - 1);
    addOperation('減少', 1);
  };

  const multiplyBy = (factor) => {
    setCount(prev => {
      const newValue = prev * factor;
      setTotal(prevTotal => prevTotal + (newValue - prev));
      addOperation('乘以', factor);
      return newValue;
    });
  };

  const reset = () => {
    setCount(0);
    setTotal(0);
    setOperations([]);
  };

  return (
    <div>
      <p>目前計數：{count}</p>
      <p>累計總和：{total}</p>
      <p>操作次數：{operations.length}</p>

      <div>
        <button onClick={increment}>+1</button>
        <button onClick={decrement}>-1</button>
        <button onClick={() => multiplyBy(2)}>×2</button>
        <button onClick={() => multiplyBy(0)}>×0</button>
        <button onClick={reset}>重設</button>
      </div>

      <div>
        <h4>最近操作：</h4>
        <ul>
          {operations.slice(-5).map((op, index) => (
            <li key={index}>
              {op.operation} {op.value} (時間: {new Date(op.timestamp).toLocaleTimeString()})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

### 2. 購物車管理

```jsx
function ShoppingCart() {
  const [cart, setCart] = useState([]);
  const [total, setTotal] = useState(0);

  const products = [
    { id: 1, name: '筆記型電腦', price: 30000 },
    { id: 2, name: '滑鼠', price: 500 },
    { id: 3, name: '鍵盤', price: 1500 }
  ];

  const addToCart = (product) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id);

      if (existingItem) {
        return prevCart.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevCart, { ...product, quantity: 1 }];
      }
    });
  };

  const removeFromCart = (productId) => {
    setCart(prevCart => prevCart.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
      return;
    }

    setCart(prevCart =>
      prevCart.map(item =>
        item.id === productId
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  };

  const clearCart = () => {
    setCart([]);
  };

  /** 計算總價 */
  useEffect(() => {
    setTotal(cart.reduce((sum, item) => sum + (item.price * item.quantity), 0));
  }, [cart]);

  return (
    <div>
      <div>
        <h3>商品列表</h3>
        {products.map(product => (
          <div key={product.id} style={{ border: '1px solid #ccc', margin: '5px', padding: '10px' }}>
            <h4>{product.name}</h4>
            <p>價格：NT$ {product.price.toLocaleString()}</p>
            <button onClick={() => addToCart(product)}>
              加入購物車
            </button>
          </div>
        ))}
      </div>

      <div>
        <h3>購物車 ({cart.length} 種商品)</h3>
        {cart.length === 0 ? (
          <p>購物車是空的</p>
        ) : (
          <>
            {cart.map(item => (
              <div key={item.id} style={{ border: '1px solid #ddd', margin: '5px', padding: '10px' }}>
                <h4>{item.name}</h4>
                <p>單價：NT$ {item.price.toLocaleString()}</p>
                <div>
                  數量：
                  <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>-</button>
                  <span style={{ margin: '0 10px' }}>{item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
                </div>
                <p>小計：NT$ {(item.price * item.quantity).toLocaleString()}</p>
                <button onClick={() => removeFromCart(item.id)}>移除</button>
              </div>
            ))}

            <div style={{ marginTop: '20px', fontSize: '18px', fontWeight: 'bold' }}>
              總計：NT$ {total.toLocaleString()}
            </div>

            <button onClick={clearCart} style={{ marginTop: '10px' }}>
              清空購物車
            </button>
          </>
        )}
      </div>
    </div>
  );
}
```

### 3. 表單驗證與狀態管理

```jsx
function FormValidation() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});
  const [touchedFields, setTouchedFields] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateField = (name, value) => {
    switch (name) {
      case 'username':
        return value.length < 3 ? '使用者名稱至少需要 3 個字元' : '';
      case 'email':
        return !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? 'Email 格式不正確' : '';
      case 'password':
        return value.length < 6 ? '密碼至少需要 6 個字元' : '';
      case 'confirmPassword':
        return value !== formData.password ? '確認密碼不符合' : '';
      default:
        return '';
    }
  };

  const handleInputChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    /** 即時驗證 */
    if (touchedFields[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: validateField(name, value)
      }));
    }
  };

  const handleBlur = (name) => {
    setTouchedFields(prev => ({
      ...prev,
      [name]: true
    }));

    setErrors(prev => ({
      ...prev,
      [name]: validateField(name, formData[name])
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    /** 驗證所有欄位 */
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      const error = validateField(key, formData[key]);
      if (error) newErrors[key] = error;
    });

    setErrors(newErrors);
    setTouchedFields({
      username: true,
      email: true,
      password: true,
      confirmPassword: true
    });

    if (Object.keys(newErrors).length === 0) {
      setIsSubmitting(true);

      try {
        /** 模擬 API 呼叫 */
        await new Promise(resolve => setTimeout(resolve, 2000));
        console.log('表單送出成功:', formData);

        /** 重設表單 */
        setFormData({
          username: '',
          email: '',
          password: '',
          confirmPassword: ''
        });
        setTouchedFields({});
        setErrors({});
      } catch (error) {
        console.error('送出失敗:', error);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          placeholder="使用者名稱"
          value={formData.username}
          onChange={(e) => handleInputChange('username', e.target.value)}
          onBlur={() => handleBlur('username')}
          className={errors.username ? 'error' : ''}
        />
        {errors.username && <span className="error-message">{errors.username}</span>}
      </div>

      <div>
        <input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => handleInputChange('email', e.target.value)}
          onBlur={() => handleBlur('email')}
          className={errors.email ? 'error' : ''}
        />
        {errors.email && <span className="error-message">{errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="密碼"
          value={formData.password}
          onChange={(e) => handleInputChange('password', e.target.value)}
          onBlur={() => handleBlur('password')}
          className={errors.password ? 'error' : ''}
        />
        {errors.password && <span className="error-message">{errors.password}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="確認密碼"
          value={formData.confirmPassword}
          onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
          onBlur={() => handleBlur('confirmPassword')}
          className={errors.confirmPassword ? 'error' : ''}
        />
        {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '送出中...' : '送出'}
      </button>
    </form>
  );
}
```

<br />

## 最佳實務與注意事項

### 1. 何時使用函式式更新

```jsx
function WhenToUseFunctionalUpdate() {
  const [count, setCount] = useState(0);

  /** ✅ 需要基於前一個狀態值時，使用函式式更新 */
  const incrementBasedOnPrevious = () => {
    setCount(prev => prev + 1);
  };

  /** ✅ 多次更新時，使用函式式更新 */
  const incrementMultiple = () => {
    setCount(prev => prev + 1);
    setCount(prev => prev + 1);
    setCount(prev => prev + 1);
  };

  /** ✅ 在事件處理器中多次呼叫時 */
  const handleComplexUpdate = () => {
    setCount(prev => prev + 1);
    // 其他處理...
    setCount(prev => prev * 2);
  };

  /** ✅ 直接設定固定值時，不需要函式式更新 */
  const resetToZero = () => {
    setCount(0); // 簡單直接
  };

  const setToSpecificValue = () => {
    setCount(100); // 不依賴前一個值
  };

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={incrementBasedOnPrevious}>+1</button>
      <button onClick={incrementMultiple}>+3</button>
      <button onClick={handleComplexUpdate}>複雜更新</button>
      <button onClick={resetToZero}>重設為 0</button>
      <button onClick={setToSpecificValue}>設為 100</button>
    </div>
  );
}
```

### 2. 避免常見錯誤

```jsx
function AvoidCommonMistakes() {
  const [items, setItems] = useState([]);

  /** ❌ 錯誤：在函式式更新中使用外部變數 */
  const addItemWrong = () => {
    const newItem = `項目 ${items.length + 1}`; // 可能是過時的值
    setItems(prev => [...prev, newItem]);
  };

  /** ✅ 正確：在函式式更新中使用參數 */
  const addItemCorrect = () => {
    setItems(prev => {
      const newItem = `項目 ${prev.length + 1}`;
      return [...prev, newItem];
    });
  };

  /** ❌ 錯誤：在函式式更新中修改參數 */
  const modifyItemsWrong = () => {
    setItems(prev => {
      prev.push('新項目'); // 直接修改參數
      return prev;
    });
  };

  /** ✅ 正確：返回新陣列 */
  const modifyItemsCorrect = () => {
    setItems(prev => [...prev, '新項目']);
  };

  return (
    <div>
      <p>項目數量：{items.length}</p>
      <button onClick={addItemCorrect}>正確新增項目</button>
      <button onClick={modifyItemsCorrect}>正確修改項目</button>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 總結

### 狀態更新特性

- 非同步性：狀態更新不會立即反映在變數中

- 批次處理：React 會自動批次處理多個狀態更新

- 閉包問題：事件處理器中的狀態值可能是過時的

### 函式式更新優勢

- 基於最新狀態：總是基於最新的狀態值進行更新

- 避免競態條件：多次更新會正確累積

- 更好的可預測性：不依賴外部變數的值

### 使用建議

- 依賴前一個狀態時：使用函式式更新

- 多次更新時：使用函式式更新

- 設定固定值時：直接傳遞值

- 複雜更新處理：在函式式更新中完成所有相關計算與更新
