# 5.3.3 `useRef`：存取 DOM 與儲存渲染間值

## 基本概念

`useRef` 是 React Hook，用於存取 DOM 元素或在渲染之間保存可變值。與 `useState` 不同，更新 `useRef` 的值不會觸發重新渲染。

### 1. 基本語法

```jsx
import React, { useRef, useEffect } from 'react';

function BasicRefExample() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} placeholder="點擊按鈕聚焦" />
      <button onClick={focusInput}>聚焦輸入框</button>
    </div>
  );
}
```

### 2. `useRef` vs `useState`

```jsx
function RefVsState() {
  const [stateCount, setStateCount] = useState(0);
  const refCount = useRef(0);
  const renderCount = useRef(0);

  /** 每次渲染時增加渲染計數 */
  renderCount.current += 1;

  const incrementState = () => {
    setStateCount(prev => prev + 1); // 觸發重新渲染
  };

  const incrementRef = () => {
    refCount.current += 1; // 不觸發重新渲染
    console.log('Ref count:', refCount.current);
  };

  return (
    <div>
      <p>State 計數：{stateCount}</p>
      <p>Ref 計數：{refCount.current}</p>
      <p>渲染次數：{renderCount.current}</p>

      <button onClick={incrementState}>增加 State (會重新渲染)</button>
      <button onClick={incrementRef}>增加 Ref (不會重新渲染)</button>
    </div>
  );
}
```

<br />

## DOM 元素存取

### 1. 基本 DOM 操作

```jsx
function DOMAccess() {
  const inputRef = useRef(null);
  const divRef = useRef(null);

  const handleFocus = () => {
    inputRef.current.focus();
  };

  const handleSelect = () => {
    inputRef.current.select();
  };

  const changeBackgroundColor = () => {
    divRef.current.style.backgroundColor = 
      divRef.current.style.backgroundColor === 'lightblue' ? 'lightcoral' : 'lightblue';
  };

  const getDimensions = () => {
    const rect = divRef.current.getBoundingClientRect();
    alert(`寬度: ${rect.width}, 高度: ${rect.height}`);
  };

  return (
    <div>
      <input 
        ref={inputRef}
        defaultValue="測試文字"
        placeholder="輸入文字"
      />

      <div>
        <button onClick={handleFocus}>聚焦</button>
        <button onClick={handleSelect}>選取文字</button>
      </div>

      <div 
        ref={divRef}
        style={{
          width: '200px',
          height: '100px',
          border: '1px solid #ccc',
          margin: '10px 0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        點擊按鈕改變背景色
      </div>

      <div>
        <button onClick={changeBackgroundColor}>改變背景色</button>
        <button onClick={getDimensions}>取得尺寸</button>
      </div>
    </div>
  );
}
```

### 2. 表單處理

```jsx
function FormWithRefs() {
  const nameRef = useRef(null);
  const emailRef = useRef(null);
  const messageRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {
      name: nameRef.current.value,
      email: emailRef.current.value,
      message: messageRef.current.value
    };

    console.log('表單資料:', formData);

    /** 驗證 */
    if (!formData.name.trim()) {
      nameRef.current.focus();
      alert('請輸入姓名');
      return;
    }

    if (!formData.email.trim()) {
      emailRef.current.focus();
      alert('請輸入 Email');
      return;
    }

    alert('表單送出成功！');
  };

  const handleReset = () => {
    nameRef.current.value = '';
    emailRef.current.value = '';
    messageRef.current.value = '';
    nameRef.current.focus();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input ref={nameRef} type="text" />
      </div>

      <div>
        <label>Email：</label>
        <input ref={emailRef} type="email" />
      </div>

      <div>
        <label>訊息：</label>
        <textarea ref={messageRef} rows="4" />
      </div>

      <div>
        <button type="submit">送出</button>
        <button type="button" onClick={handleReset}>重設</button>
      </div>
    </form>
  );
}
```

### 3. 滾動控制

```jsx
function ScrollControl() {
  const topRef = useRef(null);
  const middleRef = useRef(null);
  const bottomRef = useRef(null);
  const containerRef = useRef(null);

  const scrollToElement = (elementRef) => {
    elementRef.current.scrollIntoView({ 
      behavior: 'smooth',
      block: 'center'
    });
  };

  const scrollToTop = () => {
    containerRef.current.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  const scrollToBottom = () => {
    containerRef.current.scrollTo({
      top: containerRef.current.scrollHeight,
      behavior: 'smooth'
    });
  };

  return (
    <div>
      <div>
        <button onClick={() => scrollToElement(topRef)}>滾動到頂部</button>
        <button onClick={() => scrollToElement(middleRef)}>滾動到中間</button>
        <button onClick={() => scrollToElement(bottomRef)}>滾動到底部</button>
        <button onClick={scrollToTop}>回到最頂端</button>
        <button onClick={scrollToBottom}>到最底端</button>
      </div>

      <div 
        ref={containerRef}
        style={{
          height: '300px',
          overflow: 'auto',
          border: '1px solid #ccc',
          margin: '10px 0'
        }}
      >
        <div ref={topRef} style={{ height: '200px', backgroundColor: 'lightblue' }}>
          <h3>頂部區域</h3>
          <p>這是頂部的內容</p>
        </div>

        <div style={{ height: '400px', backgroundColor: 'lightgreen' }}>
          <h3>中間區域 (上半部)</h3>
          <p>這是中間區域的上半部內容</p>
        </div>

        <div ref={middleRef} style={{ height: '200px', backgroundColor: 'lightyellow' }}>
          <h3>中間區域 (中心)</h3>
          <p>這是中間區域的中心內容</p>
        </div>

        <div style={{ height: '400px', backgroundColor: 'lightpink' }}>
          <h3>中間區域 (下半部)</h3>
          <p>這是中間區域的下半部內容</p>
        </div>

        <div ref={bottomRef} style={{ height: '200px', backgroundColor: 'lightcoral' }}>
          <h3>底部區域</h3>
          <p>這是底部的內容</p>
        </div>
      </div>
    </div>
  );
}
```

<br />

## 儲存渲染間的值

### 1. 保存前一個值

```jsx
function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  });

  return ref.current;
}

function PreviousValueExample() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('Charmy');

  const prevCount = usePrevious(count);
  const prevName = usePrevious(name);

  return (
    <div>
      <div>
        <p>目前計數：{count}</p>
        <p>前一個計數：{prevCount}</p>
        <button onClick={() => setCount(count + 1)}>增加計數</button>
      </div>

      <div>
        <p>目前姓名：{name}</p>
        <p>前一個姓名：{prevName}</p>
        <input 
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="輸入姓名"
        />
      </div>
    </div>
  );
}
```

### 2. 計時器與間隔

```jsx
function TimerWithRef() {
  const [count, setCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef(null);
  const countRef = useRef(count);

  /** 保持 countRef 與 count 同步 */
  useEffect(() => {
    countRef.current = count;
  }, [count]);

  const startTimer = () => {
    if (!isRunning) {
      setIsRunning(true);
      intervalRef.current = setInterval(() => {
        setCount(prevCount => prevCount + 1);
      }, 1000);
    }
  };

  const stopTimer = () => {
    if (isRunning) {
      setIsRunning(false);
      clearInterval(intervalRef.current);
    }
  };

  const resetTimer = () => {
    setCount(0);
    setIsRunning(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  const logCurrentCount = () => {
    /** 使用 ref 取得最新的 count 值 */
    console.log('目前計數 (來自 ref):', countRef.current);
    console.log('目前計數 (來自 state):', count);
  };

  /** 清理計時器 */
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div>
      <h3>計時器：{count} 秒</h3>
      <p>狀態：{isRunning ? '運行中' : '已停止'}</p>

      <div>
        <button onClick={startTimer} disabled={isRunning}>
          開始
        </button>
        <button onClick={stopTimer} disabled={!isRunning}>
          停止
        </button>
        <button onClick={resetTimer}>
          重設
        </button>
        <button onClick={logCurrentCount}>
          記錄目前計數
        </button>
      </div>
    </div>
  );
}
```

### 3. 避免過時閉包問題

```jsx
function ChatRoom() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const messagesRef = useRef(messages);

  /** 保持 ref 與 state 同步 */
  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  useEffect(() => {
    const interval = setInterval(() => {
      /** 模擬接收新訊息 */
      const randomMessage = `系統訊息 ${Date.now()}`;

      /** 使用 ref 避免閉包問題 */
      setMessages(prevMessages => [...prevMessages, {
        id: Date.now(),
        text: randomMessage,
        timestamp: new Date().toLocaleTimeString()
      }]);

      console.log('目前訊息數量:', messagesRef.current.length);
    }, 5000);

    return () => clearInterval(interval);
  }, []); // 空依賴陣列，但透過 ref 存取最新狀態

  const sendMessage = () => {
    if (newMessage.trim()) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: newMessage,
        timestamp: new Date().toLocaleTimeString(),
        sender: 'user'
      }]);
      setNewMessage('');
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return (
    <div>
      <div style={{ 
        height: '200px', 
        overflow: 'auto', 
        border: '1px solid #ccc',
        padding: '10px',
        marginBottom: '10px'
      }}>
        {messages.map(message => (
          <div key={message.id}>
            <strong>{message.sender || 'system'}:</strong> {message.text}
            <small> ({message.timestamp})</small>
          </div>
        ))}
      </div>

      <div>
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="輸入訊息..."
        />
        <button onClick={sendMessage}>送出</button>
        <button onClick={clearMessages}>清除</button>
      </div>

      <p>訊息數量：{messages.length}</p>
    </div>
  );
}
```

<br />

## 進階應用

### 1. 自定義 Hook 結合 `useRef`

```jsx
function useClickOutside(callback) {
  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        callback();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [callback]);

  return ref;
}

function useHover() {
  const ref = useRef(null);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);

    element.addEventListener('mouseenter', handleMouseEnter);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter);
      element.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return [ref, isHovered];
}

function DropdownMenu() {
  const [isOpen, setIsOpen] = useState(false);

  const dropdownRef = useClickOutside(() => {
    setIsOpen(false);
  });

  const [buttonRef, isButtonHovered] = useHover();

  return (
    <div ref={dropdownRef} style={{ position: 'relative', display: 'inline-block' }}>
      <button 
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        style={{
          backgroundColor: isButtonHovered ? '#e0e0e0' : '#f0f0f0',
          padding: '10px 20px',
          border: '1px solid #ccc',
          cursor: 'pointer'
        }}
      >
        選單 {isOpen ? '▲' : '▼'}
      </button>

      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          backgroundColor: 'white',
          border: '1px solid #ccc',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          zIndex: 1000,
          minWidth: '150px'
        }}>
          <div style={{ padding: '10px', cursor: 'pointer' }}>選項 1</div>
          <div style={{ padding: '10px', cursor: 'pointer' }}>選項 2</div>
          <div style={{ padding: '10px', cursor: 'pointer' }}>選項 3</div>
        </div>
      )}
    </div>
  );
}
```

### 2. 效能最佳化

```jsx
function ExpensiveComponent({ data, onProcess }) {
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const processingRef = useRef(false);
  const abortControllerRef = useRef(null);

  const processData = useCallback(async () => {
    /** 防止重複處理 */
    if (processingRef.current) {
      console.log('已在處理中，忽略重複請求');
      return;
    }

    processingRef.current = true;
    setIsProcessing(true);

    /** 取消前一個請求 */
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();

    try {
      /** 模擬昂貴的非同步操作 */
      await new Promise((resolve, reject) => {
        const timeoutId = setTimeout(resolve, 2000);

        abortControllerRef.current.signal.addEventListener('abort', () => {
          clearTimeout(timeoutId);
          reject(new Error('操作被取消'));
        });
      });

      if (!abortControllerRef.current.signal.aborted) {
        const processedResult = `處理結果: ${data.length} 項資料`;
        setResult(processedResult);
        onProcess(processedResult);
      }
    } catch (error) {
      if (error.message !== '操作被取消') {
        console.error('處理失敗:', error);
      }
    } finally {
      processingRef.current = false;
      setIsProcessing(false);
    }
  }, [data, onProcess]);

  /** 清理函式 */
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return (
    <div>
      <button onClick={processData} disabled={isProcessing}>
        {isProcessing ? '處理中...' : '開始處理'}
      </button>

      {result && (
        <div>
          <h4>處理結果：</h4>
          <p>{result}</p>
        </div>
      )}

      <p>資料項目數：{data.length}</p>
    </div>
  );
}
```

### 3. 動畫與過渡效果

```jsx
function AnimatedComponent() {
  const [isVisible, setIsVisible] = useState(false);
  const elementRef = useRef(null);
  const animationRef = useRef(null);

  const fadeIn = () => {
    const element = elementRef.current;
    if (!element) return;

    element.style.opacity = '0';
    element.style.display = 'block';

    let opacity = 0;
    const fadeInAnimation = () => {
      opacity += 0.05;
      element.style.opacity = opacity;

      if (opacity < 1) {
        animationRef.current = requestAnimationFrame(fadeInAnimation);
      }
    };

    animationRef.current = requestAnimationFrame(fadeInAnimation);
  };

  const fadeOut = () => {
    const element = elementRef.current;
    if (!element) return;

    let opacity = 1;
    const fadeOutAnimation = () => {
      opacity -= 0.05;
      element.style.opacity = opacity;

      if (opacity > 0) {
        animationRef.current = requestAnimationFrame(fadeOutAnimation);
      } else {
        element.style.display = 'none';
      }
    };

    animationRef.current = requestAnimationFrame(fadeOutAnimation);
  };

  const toggleVisibility = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    if (isVisible) {
      fadeOut();
    } else {
      fadeIn();
    }

    setIsVisible(!isVisible);
  };

  /** 清理動畫 */
  useEffect(() => {
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return (
    <div>
      <button onClick={toggleVisibility}>
        {isVisible ? '隱藏' : '顯示'}
      </button>

      <div 
        ref={elementRef}
        style={{
          width: '200px',
          height: '100px',
          backgroundColor: 'lightblue',
          margin: '20px 0',
          display: 'none',
          alignItems: 'center',
          justifyContent: 'center',
          border: '1px solid #ccc'
        }}
      >
        動畫元素
      </div>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 何時使用 `useRef`

- DOM 操作：聚焦、滾動、測量尺寸

- 儲存可變值：不需要觸發重新渲染的值

- 避免閉包問題：在 `useEffect` 中存取最新狀態

- 效能最佳化：避免重複計算或操作

### 2. 使用注意事項

- 不要過度使用：優先考慮 React 的聲明式方式

- 避免在渲染期間讀取：ref.current 在渲染期間可能不穩定

- 清理副作用：記得清理計時器、事件監聽器等

- 類型安全：TypeScript 中正確定義 ref 類型

### 3. 常見錯誤

- 在渲染期間修改 ref：應該在 `useEffect` 或事件處理器中修改

- 依賴 ref 觸發重新渲染：ref 變更不會觸發重新渲染

- 忘記初始值：`useRef` 需要提供初始值

- 記憶體洩漏：忘記清理 ref 相關的副作用
