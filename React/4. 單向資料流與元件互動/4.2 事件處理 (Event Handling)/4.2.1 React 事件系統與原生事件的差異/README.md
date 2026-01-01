# 4.2.1 React 事件系統與原生事件的差異

<br />

## React 合成事件 (SyntheticEvent)

### 1. 基本概念

React 使用合成事件系統來包裝原生 DOM 事件，提供跨瀏覽器的一致性體驗。合成事件是原生事件的包裝器，具有相同的介面但行為更加統一。

```jsx
function EventExample() {
  const handleClick = (e) => {
    console.log('React 合成事件：', e);
    console.log('事件類型：', e.type);
    console.log('目標元素：', e.target);
    console.log('原生事件：', e.nativeEvent);
  };

  return (
    <button onClick={handleClick}>
      點擊按鈕
    </button>
  );
}
```

### 2. 合成事件 vs 原生事件

```jsx
function EventComparison() {
  const handleReactEvent = (e) => {
    console.log('=== React 合成事件 ===');
    console.log('事件物件：', e);
    console.log('事件類型：', e.type);
    console.log('是否為合成事件：', e instanceof SyntheticEvent);
    console.log('原生事件：', e.nativeEvent);
  };

  const handleNativeEvent = () => {
    const button = document.getElementById('native-button');
    button.addEventListener('click', (e) => {
      console.log('=== 原生事件 ===');
      console.log('事件物件：', e);
      console.log('事件類型：', e.type);
      console.log('是否為原生事件：', e instanceof Event);
    });
  };

  useEffect(() => {
    handleNativeEvent();
  }, []);

  return (
    <div>
      <button onClick={handleReactEvent}>
        React 事件
      </button>
      <button id="native-button">
        原生事件
      </button>
    </div>
  );
}
```

<br />

## 事件委派 (Event Delegation)

### 1. React 事件委派機制

```jsx
function EventDelegation() {
  const handleButtonClick = (e) => {
    console.log('按鈕被點擊：', e.target.textContent);
    console.log('實際監聽器位置：', e.currentTarget); // 通常是 document
  };

  const handleDivClick = (e) => {
    console.log('容器被點擊');
    console.log('事件階段：', e.eventPhase);
  };

  return (
    <div onClick={handleDivClick}>
      <button onClick={handleButtonClick}>按鈕 1</button>
      <button onClick={handleButtonClick}>按鈕 2</button>
      <button onClick={handleButtonClick}>按鈕 3</button>
    </div>
  );
}
```

### 2. 事件委派的優勢

```jsx
function DynamicList() {
  const [items, setItems] = useState([
    { id: 1, name: '項目 1' },
    { id: 2, name: '項目 2' }
  ]);

  /** React 自動處理事件委派，即使動態添加元素也能正常工作 */
  const handleItemClick = (e) => {
    const itemId = e.target.dataset.itemId;
    console.log(`點擊項目：${itemId}`);
  };

  const addItem = () => {
    const newId = items.length + 1;
    setItems(prev => [...prev, { id: newId, name: `項目 ${newId}` }]);
  };

  return (
    <div>
      <button onClick={addItem}>新增項目</button>
      <ul>
        {items.map(item => (
          <li 
            key={item.id}
            data-item-id={item.id}
            onClick={handleItemClick}
            style={{ cursor: 'pointer' }}
          >
            {item.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 事件物件屬性差異

### 1. 常用屬性比較

```jsx
function EventProperties() {
  const handleEvent = (e) => {
    console.log('=== 事件屬性比較 ===');

    /** 共同屬性 */
    console.log('type:', e.type);
    console.log('target:', e.target);
    console.log('currentTarget:', e.currentTarget);
    console.log('timeStamp:', e.timeStamp);

    /** React 特有屬性 */
    console.log('nativeEvent:', e.nativeEvent);
    console.log('isDefaultPrevented:', e.isDefaultPrevented());
    console.log('isPropagationStopped:', e.isPropagationStopped());

    /** 滑鼠事件屬性 */
    if (e.type === 'click') {
      console.log('clientX:', e.clientX);
      console.log('clientY:', e.clientY);
      console.log('button:', e.button);
      console.log('buttons:', e.buttons);
    }

    /** 鍵盤事件屬性 */
    if (e.type === 'keydown') {
      console.log('key:', e.key);
      console.log('keyCode:', e.keyCode);
      console.log('ctrlKey:', e.ctrlKey);
      console.log('shiftKey:', e.shiftKey);
    }
  };

  return (
    <div>
      <button onClick={handleEvent}>
        點擊測試
      </button>
      <input 
        onKeyDown={handleEvent}
        placeholder="按鍵測試"
      />
    </div>
  );
}
```

### 2. 表單事件處理

```jsx
function FormEvents() {
  const [formData, setFormData] = useState({
    text: '',
    select: '',
    checkbox: false
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;

    console.log('表單事件屬性：');
    console.log('name:', name);
    console.log('value:', value);
    console.log('type:', type);
    console.log('checked:', checked);

    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault(); // React 合成事件的 preventDefault
    console.log('表單資料：', formData);
    console.log('預設行為已阻止：', e.isDefaultPrevented());
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="text"
        value={formData.text}
        onChange={handleInputChange}
        placeholder="文字輸入"
      />

      <select
        name="select"
        value={formData.select}
        onChange={handleInputChange}
      >
        <option value="">請選擇</option>
        <option value="option1">選項 1</option>
        <option value="option2">選項 2</option>
      </select>

      <label>
        <input
          name="checkbox"
          type="checkbox"
          checked={formData.checkbox}
          onChange={handleInputChange}
        />
        核取方塊
      </label>

      <button type="submit">送出</button>
    </form>
  );
}
```

<br />

## 事件傳播與阻止

### 1. 事件傳播階段

```jsx
function EventPropagation() {
  const handleCapture = (e) => {
    console.log('捕獲階段：', e.currentTarget.className);
  };

  const handleBubble = (e) => {
    console.log('冒泡階段：', e.currentTarget.className);
  };

  const handleStopPropagation = (e) => {
    console.log('阻止事件傳播');
    e.stopPropagation();
  };

  return (
    <div 
      className="outer"
      onClick={handleBubble}
      onClickCapture={handleCapture}
    >
      外層容器
      <div 
        className="middle"
        onClick={handleBubble}
        onClickCapture={handleCapture}
      >
        中層容器
        <button 
          className="inner"
          onClick={handleStopPropagation}
          onClickCapture={handleCapture}
        >
          內層按鈕 (阻止傳播)
        </button>
        <button 
          className="inner-normal"
          onClick={handleBubble}
          onClickCapture={handleCapture}
        >
          內層按鈕 (正常傳播)
        </button>
      </div>
    </div>
  );
}
```

### 2. 阻止預設行為

```jsx
function PreventDefault() {
  const handleLinkClick = (e) => {
    e.preventDefault();
    console.log('連結點擊被攔截');
    console.log('預設行為已阻止：', e.isDefaultPrevented());

    /** 自定義導流程 */
    window.history.pushState({}, '', e.target.href);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    console.log('表單送出被攔截');

    /** 自定義送出流程 */
    const formData = new FormData(e.target);
    console.log('表單資料：', Object.fromEntries(formData));
  };

  const handleContextMenu = (e) => {
    e.preventDefault();
    console.log('右鍵選單被阻止');
  };

  return (
    <div>
      <a 
        href="/example" 
        onClick={handleLinkClick}
      >
        自定義導航連結
      </a>

      <form onSubmit={handleFormSubmit}>
        <input name="username" placeholder="使用者名稱" />
        <button type="submit">送出</button>
      </form>

      <div 
        onContextMenu={handleContextMenu}
        style={{ 
          padding: '20px', 
          border: '1px solid #ccc',
          marginTop: '10px'
        }}
      >
        右鍵點擊此區域 (右鍵選單被阻止)
      </div>
    </div>
  );
}
```

<br />

## 原生事件與 React 事件混用

### 1. 混用注意事項

```jsx
function MixedEvents() {
  const buttonRef = useRef(null);

  useEffect(() => {
    const button = buttonRef.current;

    /** 原生事件監聽器 */
    const nativeHandler = (e) => {
      console.log('原生事件處理器');
      e.stopPropagation(); // 這不會影響 React 事件
    };

    button.addEventListener('click', nativeHandler);

    return () => {
      button.removeEventListener('click', nativeHandler);
    };
  }, []);

  const handleReactClick = (e) => {
    console.log('React 事件處理器');
    // React 事件的 stopPropagation 不會影響原生事件
  };

  const handleParentClick = () => {
    console.log('父元件點擊');
  };

  return (
    <div onClick={handleParentClick}>
      <button 
        ref={buttonRef}
        onClick={handleReactClick}
      >
        混合事件按鈕
      </button>
    </div>
  );
}
```

### 2. 事件執行順序

```jsx
function EventOrder() {
  const buttonRef = useRef(null);

  useEffect(() => {
    const button = buttonRef.current;

    /** 原生事件 - 捕獲階段 */
    button.addEventListener('click', () => {
      console.log('1. 原生事件 - 捕獲階段');
    }, true);

    /** 原生事件 - 冒泡階段 */
    button.addEventListener('click', () => {
      console.log('3. 原生事件 - 冒泡階段');
    }, false);

    return () => {
      /** 清理事件監聽器 */
    };
  }, []);

  const handleReactClick = () => {
    console.log('2. React 合成事件');
  };

  return (
    <button 
      ref={buttonRef}
      onClick={handleReactClick}
    >
      事件執行順序測試
    </button>
  );
}
```

<br />

## 效能考量

### 1. 事件處理器最佳化

```jsx
function PerformanceOptimization() {
  const [items, setItems] = useState(
    Array.from({ length: 1000 }, (_, i) => ({ id: i, name: `項目 ${i}` }))
  );

  /** ❌ 每次渲染都建立新函式 */
  const badHandler = (id) => {
    console.log(`點擊項目：${id}`);
  };

  /** ✅ 使用 useCallback 最佳化 */
  const goodHandler = useCallback((e) => {
    const id = e.target.dataset.id;
    console.log(`點擊項目：${id}`);
  }, []);

  /** ✅ 事件委派模式 */
  const delegatedHandler = (e) => {
    if (e.target.dataset.id) {
      console.log(`點擊項目：${e.target.dataset.id}`);
    }
  };

  return (
    <div>
      {/* ❌ 效能較差的方式 */}
      <div>
        {items.slice(0, 10).map(item => (
          <button 
            key={item.id}
            onClick={() => badHandler(item.id)}
          >
            {item.name}
          </button>
        ))}
      </div>

      {/* ✅ 最佳化的方式 */}
      <div onClick={delegatedHandler}>
        {items.slice(10, 20).map(item => (
          <button 
            key={item.id}
            data-id={item.id}
          >
            {item.name}
          </button>
        ))}
      </div>
    </div>
  );
}
```

### 2. 被動事件監聽器

```jsx
function PassiveEvents() {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;

    /** 被動事件監聽器 - 提升滾動效能 */
    const handleScroll = (e) => {
      /** 不能呼叫 preventDefault() */
      console.log('滾動位置：', e.target.scrollTop);
    };

    const handleTouch = (e) => {
      /** 被動觸控事件 */
      console.log('觸控事件');
    };

    container.addEventListener('scroll', handleScroll, { passive: true });
    container.addEventListener('touchstart', handleTouch, { passive: true });

    return () => {
      container.removeEventListener('scroll', handleScroll);
      container.removeEventListener('touchstart', handleTouch);
    };
  }, []);

  return (
    <div 
      ref={containerRef}
      style={{ 
        height: '200px', 
        overflow: 'auto',
        border: '1px solid #ccc'
      }}
    >
      <div style={{ height: '1000px', padding: '20px' }}>
        <p>滾動此區域測試被動事件</p>
        <p>內容很長...</p>
        {Array.from({ length: 50 }, (_, i) => (
          <p key={i}>第 {i + 1} 行內容</p>
        ))}
      </div>
    </div>
  );
}
```

<br />

## 跨瀏覽器相容性

### 1. 事件名稱標準化

```jsx
function CrossBrowserEvents() {
  const handleAnimationEvent = (e) => {
    console.log('動畫事件：', e.type);
    // React 自動處理瀏覽器前綴
    // 例如：animationend, webkitAnimationEnd, etc.
  };

  const handleTransitionEvent = (e) => {
    console.log('過渡事件：', e.type);
    // React 統一處理 transitionend 事件
  };

  const handleWheelEvent = (e) => {
    console.log('滾輪事件：', e.deltaY);
    // React 統一處理 wheel 事件 (不是 mousewheel)
  };

  return (
    <div>
      <div 
        style={{ 
          width: '100px', 
          height: '100px', 
          backgroundColor: 'blue',
          transition: 'all 0.3s ease'
        }}
        onTransitionEnd={handleTransitionEvent}
        onAnimationEnd={handleAnimationEvent}
        onWheel={handleWheelEvent}
        onClick={(e) => {
          e.target.style.backgroundColor = 
            e.target.style.backgroundColor === 'red' ? 'blue' : 'red';
        }}
      >
        點擊改變顏色
      </div>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 事件處理器命名

```jsx
function EventNaming() {
  /** ✅ 清楚的命名規範 */
  const handleButtonClick = () => {};
  const handleFormSubmit = () => {};
  const handleInputChange = () => {};
  const handleMouseEnter = () => {};

  /** ❌ 模糊的命名 */
  const onClick = () => {};
  const submit = () => {};
  const change = () => {};

  return (
    <form onSubmit={handleFormSubmit}>
      <input onChange={handleInputChange} />
      <button 
        onClick={handleButtonClick}
        onMouseEnter={handleMouseEnter}
      >
        送出
      </button>
    </form>
  );
}
```

### 2. 錯誤處理

```jsx
function ErrorHandling() {
  const handleClickWithErrorHandling = (e) => {
    try {
      /** 可能出錯的操作 */
      const data = JSON.parse(e.target.dataset.json);
      console.log(data);
    } catch (error) {
      console.error('事件處理錯誤：', error);
      // 錯誤回報或使用者提示
    }
  };

  const safeEventHandler = (callback) => (e) => {
    try {
      callback(e);
    } catch (error) {
      console.error('事件處理器錯誤：', error);
    }
  };

  return (
    <div>
      <button 
        data-json='{"valid": "json"}'
        onClick={handleClickWithErrorHandling}
      >
        有效 JSON
      </button>

      <button 
        data-json='invalid json'
        onClick={safeEventHandler(handleClickWithErrorHandling)}
      >
        無效 JSON (安全處理)
      </button>
    </div>
  );
}
```

<br />

## 總結

### React 事件系統特點

- 合成事件：跨瀏覽器一致性

- 事件委派：自動最佳化效能

- 統一介面：標準化的事件屬性

- 記憶體管理：自動清理事件監聽器

### 與原生事件的主要差異

- 事件物件：SyntheticEvent vs Event

- 事件委派：自動 vs 手動

- 記憶體管理：自動 vs 手動

- 跨瀏覽器：統一 vs 需要處理差異

### 使用建議

- 優先使用 React 事件：除非有特殊需求

- 注意事件執行順序：原生事件先於 React 事件

- 效能最佳化：使用事件委派和 `useCallback`

- 錯誤處理：包裝事件處理器進行錯誤捕獲
