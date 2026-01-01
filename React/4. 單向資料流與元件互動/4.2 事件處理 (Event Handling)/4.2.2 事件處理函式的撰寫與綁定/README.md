# 4.2.2 事件處理函式的撰寫與綁定

<br />

## 基本事件處理函式

### 1. 函式宣告方式

```jsx
function BasicEventHandling() {
  /** 方式一：函式宣告 */
  function handleClick() {
    console.log('按鈕被點擊');
  }

  /** 方式二：箭頭函式 */
  const handleSubmit = () => {
    console.log('表單送出');
  };

  /** 方式三：函式表達式 */
  const handleChange = function(e) {
    console.log('輸入值改變：', e.target.value);
  };

  return (
    <div>
      <button onClick={handleClick}>點擊按鈕</button>
      <button onClick={handleSubmit}>送出表單</button>
      <input onChange={handleChange} placeholder="輸入文字" />
    </div>
  );
}
```

### 2. 事件物件處理

```jsx
function EventObjectHandling() {
  const handleInputChange = (e) => {
    console.log('事件類型：', e.type);
    console.log('目標元素：', e.target);
    console.log('輸入值：', e.target.value);
    console.log('元素名稱：', e.target.name);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault(); // 阻止預設送出行為
    console.log('表單送出被攔截');

    const formData = new FormData(e.target);
    console.log('表單資料：', Object.fromEntries(formData));
  };

  const handleKeyPress = (e) => {
    console.log('按鍵：', e.key);
    console.log('按鍵代碼：', e.keyCode);
    console.log('是否按住 Ctrl：', e.ctrlKey);
    console.log('是否按住 Shift：', e.shiftKey);
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <input
        name="username"
        onChange={handleInputChange}
        onKeyPress={handleKeyPress}
        placeholder="使用者名稱"
      />
      <input
        name="email"
        type="email"
        onChange={handleInputChange}
        placeholder="電子郵件"
      />
      <button type="submit">送出</button>
    </form>
  );
}
```

<br />

## 帶參數的事件處理

### 1. 使用箭頭函式傳遞參數

```jsx
function ParameterizedEvents() {
  const [selectedItem, setSelectedItem] = useState(null);

  const items = [
    { id: 1, name: '項目 1', category: 'A' },
    { id: 2, name: '項目 2', category: 'B' },
    { id: 3, name: '項目 3', category: 'A' }
  ];

  const handleItemClick = (item) => {
    console.log('選擇項目：', item);
    setSelectedItem(item);
  };

  const handleItemDelete = (itemId, itemName) => {
    console.log(`刪除項目：${itemName} (ID: ${itemId})`);
  };

  const handleCategoryFilter = (category) => {
    console.log('篩選分類：', category);
  };

  return (
    <div>
      <div>
        <button onClick={() => handleCategoryFilter('A')}>
          分類 A
        </button>
        <button onClick={() => handleCategoryFilter('B')}>
          分類 B
        </button>
      </div>

      <ul>
        {items.map(item => (
          <li key={item.id}>
            <span onClick={() => handleItemClick(item)}>
              {item.name}
            </span>
            <button onClick={() => handleItemDelete(item.id, item.name)}>
              刪除
            </button>
          </li>
        ))}
      </ul>

      {selectedItem && (
        <div>
          已選擇：{selectedItem.name}
        </div>
      )}
    </div>
  );
}
```

### 2. 使用 data 屬性傳遞參數

```jsx
function DataAttributeEvents() {
  const handleButtonClick = (e) => {
    const action = e.target.dataset.action;
    const itemId = e.target.dataset.itemId;
    const itemName = e.target.dataset.itemName;

    console.log(`執行動作：${action}`);
    console.log(`項目 ID：${itemId}`);
    console.log(`項目名稱：${itemName}`);

    switch (action) {
      case 'edit':
        console.log(`編輯項目：${itemName}`);
        break;
      case 'delete':
        console.log(`刪除項目：${itemName}`);
        break;
      case 'duplicate':
        console.log(`複製項目：${itemName}`);
        break;
    }
  };

  const products = [
    { id: 1, name: '筆記型電腦' },
    { id: 2, name: '滑鼠' },
    { id: 3, name: '鍵盤' }
  ];

  return (
    <div>
      {products.map(product => (
        <div key={product.id} className="product-item">
          <h3>{product.name}</h3>
          <div>
            <button
              data-action="edit"
              data-item-id={product.id}
              data-item-name={product.name}
              onClick={handleButtonClick}
            >
              編輯
            </button>
            <button
              data-action="delete"
              data-item-id={product.id}
              data-item-name={product.name}
              onClick={handleButtonClick}
            >
              刪除
            </button>
            <button
              data-action="duplicate"
              data-item-id={product.id}
              data-item-name={product.name}
              onClick={handleButtonClick}
            >
              複製
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
```

<br />

## 表單事件處理

### 1. 受控元件事件處理

```jsx
function ControlledFormEvents() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    gender: '',
    interests: [],
    newsletter: false
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: checked
    }));
  };

  const handleMultiSelectChange = (e) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: checked 
        ? [...prev[name], value]
        : prev[name].filter(item => item !== value)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('表單資料：', formData);
  };

  const handleReset = () => {
    setFormData({
      name: '',
      email: '',
      age: '',
      gender: '',
      interests: [],
      newsletter: false
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input
          name="name"
          value={formData.name}
          onChange={handleInputChange}
        />
      </div>

      <div>
        <label>Email：</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleInputChange}
        />
      </div>

      <div>
        <label>年齡：</label>
        <input
          name="age"
          type="number"
          value={formData.age}
          onChange={handleInputChange}
        />
      </div>

      <div>
        <label>性別：</label>
        <select name="gender" value={formData.gender} onChange={handleInputChange}>
          <option value="">請選擇</option>
          <option value="male">男性</option>
          <option value="female">女性</option>
          <option value="other">其他</option>
        </select>
      </div>

      <div>
        <label>興趣：</label>
        <label>
          <input
            type="checkbox"
            name="interests"
            value="reading"
            checked={formData.interests.includes('reading')}
            onChange={handleMultiSelectChange}
          />
          閱讀
        </label>
        <label>
          <input
            type="checkbox"
            name="interests"
            value="sports"
            checked={formData.interests.includes('sports')}
            onChange={handleMultiSelectChange}
          />
          運動
        </label>
        <label>
          <input
            type="checkbox"
            name="interests"
            value="music"
            checked={formData.interests.includes('music')}
            onChange={handleMultiSelectChange}
          />
          音樂
        </label>
      </div>

      <div>
        <label>
          <input
            name="newsletter"
            type="checkbox"
            checked={formData.newsletter}
            onChange={handleCheckboxChange}
          />
          訂閱電子報
        </label>
      </div>

      <div>
        <button type="submit">送出</button>
        <button type="button" onClick={handleReset}>重設</button>
      </div>
    </form>
  );
}
```

### 2. 非受控元件事件處理

```jsx
function UncontrolledFormEvents() {
  const formRef = useRef(null);
  const nameRef = useRef(null);
  const emailRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    /** 方式一：使用 ref 取得值 */
    const name = nameRef.current.value;
    const email = emailRef.current.value;

    console.log('使用 ref 取得的資料：', { name, email });

    /** 方式二：使用 FormData */
    const formData = new FormData(formRef.current);
    const data = Object.fromEntries(formData);

    console.log('使用 FormData 取得的資料：', data);
  };

  const handleInputFocus = (e) => {
    console.log('輸入框獲得焦點：', e.target.name);
    e.target.style.backgroundColor = '#f0f8ff';
  };

  const handleInputBlur = (e) => {
    console.log('輸入框失去焦點：', e.target.name);
    e.target.style.backgroundColor = '';
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input
          ref={nameRef}
          name="name"
          onFocus={handleInputFocus}
          onBlur={handleInputBlur}
        />
      </div>

      <div>
        <label>Email：</label>
        <input
          ref={emailRef}
          name="email"
          type="email"
          onFocus={handleInputFocus}
          onBlur={handleInputBlur}
        />
      </div>

      <button type="submit">送出</button>
    </form>
  );
}
```

<br />

## 事件處理最佳化

### 1. 使用 `useCallback` 避免重新渲染

```jsx
function OptimizedEventHandling() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([
    { id: 1, name: '項目 1' },
    { id: 2, name: '項目 2' },
    { id: 3, name: '項目 3' }
  ]);

  /** ❌ 每次渲染都建立新函式 */
  const handleItemClickBad = (id) => {
    console.log(`點擊項目：${id}`);
  };

  /** ✅ 使用 useCallback 最佳化 */
  const handleItemClick = useCallback((id) => {
    console.log(`點擊項目：${id}`);
  }, []);

  const handleItemDelete = useCallback((id) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  const handleCountIncrement = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);

  return (
    <div>
      <div>
        <p>計數：{count}</p>
        <button onClick={handleCountIncrement}>
          增加計數
        </button>
      </div>

      <div>
        {items.map(item => (
          <OptimizedItem
            key={item.id}
            item={item}
            onItemClick={handleItemClick}
            onItemDelete={handleItemDelete}
          />
        ))}
      </div>
    </div>
  );
}

const OptimizedItem = React.memo(function OptimizedItem({ 
  item, 
  onItemClick, 
  onItemDelete 
}) {
  console.log(`OptimizedItem ${item.id} 重新渲染`);

  return (
    <div>
      <span onClick={() => onItemClick(item.id)}>
        {item.name}
      </span>
      <button onClick={() => onItemDelete(item.id)}>
        刪除
      </button>
    </div>
  );
});
```

### 2. 事件委派模式

```jsx
function EventDelegation() {
  const [todos, setTodos] = useState([
    { id: 1, text: '學習 React', completed: false },
    { id: 2, text: '完成專案', completed: true },
    { id: 3, text: '寫文件', completed: false }
  ]);

  /** 單一事件處理器處理所有操作 */
  const handleTodoAction = (e) => {
    const todoId = parseInt(e.target.closest('[data-todo-id]')?.dataset.todoId);
    const action = e.target.dataset.action;

    if (!todoId || !action) return;

    switch (action) {
      case 'toggle':
        setTodos(prev => prev.map(todo =>
          todo.id === todoId 
            ? { ...todo, completed: !todo.completed }
            : todo
        ));
        break;

      case 'delete':
        setTodos(prev => prev.filter(todo => todo.id !== todoId));
        break;

      case 'edit':
        const newText = prompt('編輯待辦事項：');
        if (newText) {
          setTodos(prev => prev.map(todo =>
            todo.id === todoId 
              ? { ...todo, text: newText }
              : todo
          ));
        }
        break;
    }
  };

  const handleAddTodo = () => {
    const text = prompt('新增待辦事項：');
    if (text) {
      const newTodo = {
        id: Date.now(),
        text,
        completed: false
      };
      setTodos(prev => [...prev, newTodo]);
    }
  };

  return (
    <div>
      <button onClick={handleAddTodo}>新增待辦事項</button>

      <div onClick={handleTodoAction}>
        {todos.map(todo => (
          <div key={todo.id} data-todo-id={todo.id} className="todo-item">
            <span 
              style={{ 
                textDecoration: todo.completed ? 'line-through' : 'none' 
              }}
            >
              {todo.text}
            </span>
            <button data-action="toggle">
              {todo.completed ? '取消完成' : '完成'}
            </button>
            <button data-action="edit">編輯</button>
            <button data-action="delete">刪除</button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

<br />

## 複雜事件處理模式

### 1. 多步驟表單處理

```jsx
function MultiStepForm() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    personal: { name: '', email: '', phone: '' },
    address: { street: '', city: '', zipCode: '' },
    preferences: { newsletter: false, notifications: true }
  });

  const handleStepChange = (step) => {
    setCurrentStep(step);
  };

  const handleFieldChange = (section, field) => (e) => {
    const value = e.target.type === 'checkbox' 
      ? e.target.checked 
      : e.target.value;

    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('完整表單資料：', formData);
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div>
            <h3>個人資訊</h3>
            <input
              placeholder="姓名"
              value={formData.personal.name}
              onChange={handleFieldChange('personal', 'name')}
            />
            <input
              placeholder="Email"
              type="email"
              value={formData.personal.email}
              onChange={handleFieldChange('personal', 'email')}
            />
            <input
              placeholder="電話"
              value={formData.personal.phone}
              onChange={handleFieldChange('personal', 'phone')}
            />
          </div>
        );

      case 2:
        return (
          <div>
            <h3>地址資訊</h3>
            <input
              placeholder="街道地址"
              value={formData.address.street}
              onChange={handleFieldChange('address', 'street')}
            />
            <input
              placeholder="城市"
              value={formData.address.city}
              onChange={handleFieldChange('address', 'city')}
            />
            <input
              placeholder="郵遞區號"
              value={formData.address.zipCode}
              onChange={handleFieldChange('address', 'zipCode')}
            />
          </div>
        );

      case 3:
        return (
          <div>
            <h3>偏好設定</h3>
            <label>
              <input
                type="checkbox"
                checked={formData.preferences.newsletter}
                onChange={handleFieldChange('preferences', 'newsletter')}
              />
              訂閱電子報
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.preferences.notifications}
                onChange={handleFieldChange('preferences', 'notifications')}
              />
              接收通知
            </label>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        步驟 {currentStep} / 3
      </div>

      {renderStep()}

      <div>
        {currentStep > 1 && (
          <button type="button" onClick={handlePrevious}>
            上一步
          </button>
        )}

        {currentStep < 3 ? (
          <button type="button" onClick={handleNext}>
            下一步
          </button>
        ) : (
          <button type="submit">
            送出
          </button>
        )}
      </div>
    </form>
  );
}
```

### 2. 拖放事件處理

```jsx
function DragAndDropEvents() {
  const [draggedItem, setDraggedItem] = useState(null);
  const [items, setItems] = useState([
    { id: 1, text: '項目 1', category: 'todo' },
    { id: 2, text: '項目 2', category: 'todo' },
    { id: 3, text: '項目 3', category: 'done' }
  ]);

  const handleDragStart = (e) => {
    const itemId = parseInt(e.target.dataset.itemId);
    setDraggedItem(itemId);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target);
  };

  const handleDragEnd = () => {
    setDraggedItem(null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const targetCategory = e.currentTarget.dataset.category;

    if (draggedItem && targetCategory) {
      setItems(prev => prev.map(item =>
        item.id === draggedItem
          ? { ...item, category: targetCategory }
          : item
      ));
    }
  };

  const todoItems = items.filter(item => item.category === 'todo');
  const doneItems = items.filter(item => item.category === 'done');

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div
        data-category="todo"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        style={{
          width: '200px',
          minHeight: '300px',
          border: '2px dashed #ccc',
          padding: '10px'
        }}
      >
        <h3>待辦事項</h3>
        {todoItems.map(item => (
          <div
            key={item.id}
            data-item-id={item.id}
            draggable
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            style={{
              padding: '8px',
              margin: '4px 0',
              backgroundColor: draggedItem === item.id ? '#e0e0e0' : '#f0f0f0',
              cursor: 'move'
            }}
          >
            {item.text}
          </div>
        ))}
      </div>

      <div
        data-category="done"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        style={{
          width: '200px',
          minHeight: '300px',
          border: '2px dashed #ccc',
          padding: '10px'
        }}
      >
        <h3>已完成</h3>
        {doneItems.map(item => (
          <div
            key={item.id}
            data-item-id={item.id}
            draggable
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            style={{
              padding: '8px',
              margin: '4px 0',
              backgroundColor: draggedItem === item.id ? '#e0e0e0' : '#e8f5e8',
              cursor: 'move'
            }}
          >
            {item.text}
          </div>
        ))}
      </div>
    </div>
  );
}
```

<br />

## 錯誤處理與除錯

### 1. 事件處理錯誤捕獲

```jsx
function ErrorHandlingEvents() {
  const [error, setError] = useState(null);

  const createSafeHandler = (handler, errorMessage = '事件處理發生錯誤') => {
    return (...args) => {
      try {
        setError(null);
        return handler(...args);
      } catch (err) {
        console.error(errorMessage, err);
        setError(`${errorMessage}: ${err.message}`);
      }
    };
  };

  const riskyOperation = (data) => {
    if (!data) {
      throw new Error('資料不能為空');
    }

    const parsed = JSON.parse(data);
    console.log('解析成功：', parsed);
  };

  const handleRiskyClick = createSafeHandler((e) => {
    const data = e.target.dataset.json;
    riskyOperation(data);
  }, '處理 JSON 資料時發生錯誤');

  const handleAsyncOperation = createSafeHandler(async () => {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    console.log('API 資料：', data);
  }, 'API 呼叫發生錯誤');

  return (
    <div>
      {error && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          錯誤：{error}
        </div>
      )}

      <button
        data-json='{"valid": "json"}'
        onClick={handleRiskyClick}
      >
        有效 JSON 資料
      </button>

      <button
        data-json='invalid json'
        onClick={handleRiskyClick}
      >
        無效 JSON 資料
      </button>

      <button onClick={handleAsyncOperation}>
        非同步操作
      </button>
    </div>
  );
}
```

### 2. 事件處理除錯工具

```jsx
function DebuggingEvents() {
  const [debugMode, setDebugMode] = useState(false);

  const createDebugHandler = (handlerName, handler) => {
    return (e) => {
      if (debugMode) {
        console.group(`🔍 事件處理器: ${handlerName}`);
        console.log('事件類型:', e.type);
        console.log('目標元素:', e.target);
        console.log('事件物件:', e);
        console.log('時間戳:', new Date().toISOString());
        console.groupEnd();
      }

      return handler(e);
    };
  };

  const handleButtonClick = createDebugHandler('handleButtonClick', (e) => {
    console.log('按鈕點擊處理');
  });

  const handleInputChange = createDebugHandler('handleInputChange', (e) => {
    console.log('輸入值變更:', e.target.value);
  });

  const handleFormSubmit = createDebugHandler('handleFormSubmit', (e) => {
    e.preventDefault();
    console.log('表單送出處理');
  });

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={debugMode}
          onChange={(e) => setDebugMode(e.target.checked)}
        />
        啟用除錯模式
      </label>

      <form onSubmit={handleFormSubmit}>
        <input
          onChange={handleInputChange}
          placeholder="輸入文字"
        />
        <button type="button" onClick={handleButtonClick}>
          測試按鈕
        </button>
        <button type="submit">
          送出表單
        </button>
      </form>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 事件處理器命名規範

```jsx
function EventNamingConventions() {
  /** ✅ 清楚的命名規範 */
  const handleUserLogin = () => {};
  const handleFormSubmit = () => {};
  const handleButtonClick = () => {};
  const handleInputChange = () => {};
  const handleModalClose = () => {};

  /** ❌ 模糊的命名 */
  const onClick = () => {};
  const submit = () => {};
  const change = () => {};
  const close = () => {};

  return (
    <div>
      <button onClick={handleUserLogin}>登入</button>
      <button onClick={handleModalClose}>關閉</button>
    </div>
  );
}
```

### 2. 事件處理器組織

```jsx
function OrganizedEventHandlers() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  /** 將相關的事件處理器分組 */
  const userHandlers = {
    login: async (credentials) => {
      setLoading(true);
      try {
        const user = await loginAPI(credentials);
        setUser(user);
      } catch (error) {
        console.error('登入失敗:', error);
      } finally {
        setLoading(false);
      }
    },

    logout: () => {
      setUser(null);
    },

    updateProfile: (updates) => {
      setUser(prev => ({ ...prev, ...updates }));
    }
  };

  const uiHandlers = {
    toggleTheme: () => {
      document.body.classList.toggle('dark-theme');
    },

    showNotification: (message) => {
      console.log('通知:', message);
    }
  };

  return (
    <div>
      <button onClick={() => userHandlers.login({ email: 'test@example.com' })}>
        登入
      </button>
      <button onClick={userHandlers.logout}>
        登出
      </button>
      <button onClick={uiHandlers.toggleTheme}>
        切換主題
      </button>
    </div>
  );
}
```

### 3. 效能最佳化總結

- 使用 `useCallback`：避免不必要的重新渲染

- 事件委派：減少事件監聽器數量

- 避免內聯函式：在 JSX 中避免建立新函式

- 適當的記憶化：使用 `React.memo` 包裝子元件

- 錯誤邊界：捕獲事件處理中的錯誤

- 除錯工具：開發時期的事件追蹤與記錄
