# 5.3.5 `useImperativeHandle`：控制父元件 ref 操作

<br />

## 概述

`useImperativeHandle` 是一個進階 Hook，允許子元件自定義暴露給父元件的 ref 值。通常與 `forwardRef` 搭配使用，讓父元件能夠呼叫子元件的特定方法或存取特定屬性。

<br />

## 基本語法

```jsx
useImperativeHandle(ref, createHandle, [deps])
```

### 參數說明

- `ref`: 從父元件傳遞的 ref 物件

- `createHandle`: 回傳要暴露給父元件的物件的函式

- `deps`: 依賴陣列 (可選)

<br />

## 基本使用範例

### 子元件定義

```jsx
import React, { useImperativeHandle, forwardRef, useRef } from 'react';

const CustomInput = forwardRef((props, ref) => {
  const inputRef = useRef();

  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current.focus();
    },
    clear: () => {
      inputRef.current.value = '';
    },
    getValue: () => {
      return inputRef.current.value;
    }
  }));

  return <input ref={inputRef} type="text" {...props} />;
});

export default CustomInput;
```

### 父元件使用

```jsx
import React, { useRef } from 'react';
import CustomInput from './CustomInput';

function ParentComponent() {
  const inputRef = useRef();

  const handleFocus = () => {
    inputRef.current.focus();
  };

  const handleClear = () => {
    inputRef.current.clear();
  };

  const handleGetValue = () => {
    const value = inputRef.current.getValue();
    console.log('輸入值:', value);
  };

  return (
    <div>
      <CustomInput ref={inputRef} placeholder="請輸入文字" />
      <button onClick={handleFocus}>聚焦</button>
      <button onClick={handleClear}>清除</button>
      <button onClick={handleGetValue}>取得值</button>
    </div>
  );
}
```

<br />

## 進階範例：Modal 元件

### Modal 子元件

```jsx
import React, { useState, useImperativeHandle, forwardRef } from 'react';

const Modal = forwardRef(({ children }, ref) => {
  const [isOpen, setIsOpen] = useState(false);

  useImperativeHandle(ref, () => ({
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen(prev => !prev),
    isOpen: () => isOpen
  }));

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button 
          className="close-btn" 
          onClick={() => setIsOpen(false)}
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
});

export default Modal;
```

### 父元件使用 Modal

```jsx
import React, { useRef } from 'react';
import Modal from './Modal';

function App() {
  const modalRef = useRef();

  const openModal = () => {
    modalRef.current.open();
  };

  const closeModal = () => {
    modalRef.current.close();
  };

  const toggleModal = () => {
    modalRef.current.toggle();
  };

  const checkModalStatus = () => {
    const isOpen = modalRef.current.isOpen();
    alert(`Modal 狀態: ${isOpen ? '開啟' : '關閉'}`);
  };

  return (
    <div>
      <h1>Modal 範例</h1>
      <button onClick={openModal}>開啟 Modal</button>
      <button onClick={closeModal}>關閉 Modal</button>
      <button onClick={toggleModal}>切換 Modal</button>
      <button onClick={checkModalStatus}>檢查狀態</button>

      <Modal ref={modalRef}>
        <h2>這是 Modal 內容</h2>
        <p>這裡可以放置任何內容</p>
      </Modal>
    </div>
  );
}
```

<br />

## 與依賴陣列的使用

```jsx
import React, { useImperativeHandle, forwardRef, useState } from 'react';

const Counter = forwardRef(({ step = 1 }, ref) => {
  const [count, setCount] = useState(0);

  useImperativeHandle(ref, () => ({
    increment: () => setCount(prev => prev + step),
    decrement: () => setCount(prev => prev - step),
    reset: () => setCount(0),
    getCount: () => count
  }), [step, count]); // 依賴 step 和 count

  return (
    <div>
      <p>計數: {count}</p>
    </div>
  );
});
```

<br />

## 使用場景

### 1. 表單驗證

```jsx
const FormField = forwardRef(({ name, validation }, ref) => {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  useImperativeHandle(ref, () => ({
    validate: () => {
      const isValid = validation(value);
      if (!isValid) {
        setError('驗證失敗');
        return false;
      }
      setError('');
      return true;
    },
    getValue: () => value,
    reset: () => {
      setValue('');
      setError('');
    }
  }));

  return (
    <div>
      <input 
        value={value} 
        onChange={(e) => setValue(e.target.value)}
        placeholder={name}
      />
      {error && <span className="error">{error}</span>}
    </div>
  );
});
```

### 2. 動畫控制

```jsx
const AnimatedBox = forwardRef((props, ref) => {
  const [isAnimating, setIsAnimating] = useState(false);

  useImperativeHandle(ref, () => ({
    startAnimation: () => {
      setIsAnimating(true);
      setTimeout(() => setIsAnimating(false), 1000);
    },
    stopAnimation: () => setIsAnimating(false),
    isAnimating: () => isAnimating
  }));

  return (
    <div 
      className={`box ${isAnimating ? 'animate' : ''}`}
      style={{
        width: 100,
        height: 100,
        backgroundColor: 'blue',
        transition: 'transform 1s'
      }}
    />
  );
});
```

<br />

## 注意事項

### 1. 避免過度使用

```jsx
/** ❌ 不建議：暴露太多內部狀態 */
useImperativeHandle(ref, () => ({
  state,
  setState,
  internalMethod1,
  internalMethod2,
  // ... 太多方法
}));

/** ✅ 建議：只暴露必要的介面 */
useImperativeHandle(ref, () => ({
  focus,
  clear,
  validate
}));
```

### 2. 搭配 `forwardRef` 使用

```jsx
/** ❌ 錯誤：沒有使用 forwardRef */
const MyComponent = (props) => {
  useImperativeHandle(/* 這裡會出錯 */);
  return <div />;
};

/** ✅ 正確：使用 forwardRef */
const MyComponent = forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({
    // 方法定義
  }));
  return <div />;
});
```

### 3. 依賴陣列的重要性

```jsx
/** ❌ 可能導致過時的閉包 */
useImperativeHandle(ref, () => ({
  getValue: () => value // value 可能是過時的
}));

/** ✅ 正確使用依賴陣列 */
useImperativeHandle(ref, () => ({
  getValue: () => value
}), [value]);
```

<br />

## 最佳實踐

### 1. 明確的介面設計

```jsx
/** 定義清楚的介面 */
const VideoPlayer = forwardRef((props, ref) => {
  const videoRef = useRef();

  useImperativeHandle(ref, () => ({
    /** 播放控制 */
    play: () => videoRef.current.play(),
    pause: () => videoRef.current.pause(),
    stop: () => {
      videoRef.current.pause();
      videoRef.current.currentTime = 0;
    },

    /** 狀態查詢 */
    isPlaying: () => !videoRef.current.paused,
    getCurrentTime: () => videoRef.current.currentTime,
    getDuration: () => videoRef.current.duration,

    /** 設定方法 */
    setVolume: (volume) => {
      videoRef.current.volume = Math.max(0, Math.min(1, volume));
    },
    setCurrentTime: (time) => {
      videoRef.current.currentTime = time;
    }
  }));

  return <video ref={videoRef} {...props} />;
});
```

### 2. 錯誤處理

```jsx
const SafeComponent = forwardRef((props, ref) => {
  const [isReady, setIsReady] = useState(false);

  useImperativeHandle(ref, () => ({
    performAction: () => {
      if (!isReady) {
        console.warn('元件尚未準備就緒');
        return false;
      }
      /** 執行動作 */
      return true;
    }
  }));

  return <div />;
});
```

<br />

## 與其他 Hooks 的比較

| Hook | 用途 | 使用時機 |
| - | - | - |
| `useRef` | 存取 DOM 元素或保存可變值 | 需要直接操作 DOM 或保存不觸發重新渲染的值 |
| `forwardRef` | 轉發 ref 到子元件 | 父元件需要存取子元件的 DOM 節點 |
| `useImperativeHandle` | 自定義 ref 暴露的值 | 需要控制父元件能夠存取的子元件方法或屬性 |

<br />

## 總結

`useImperativeHandle` 是一個強大但需要謹慎使用的 Hook：

- 優點：提供精確的介面控制，封裝內部實作細節

- 缺點：打破了 React 的資料流原則，可能增加程式碼複雜度

- 適用場景：函式庫元件、複雜的表單控制、動畫控制等

- 最佳實踐：保持介面簡潔、搭配 `forwardRef` 使用、適當使用依賴陣列

在大多數情況下，透過 `props` 和 `state` 來管理元件間的互動是更好的選擇。只有在確實需要命令式 API 時，才考慮使用 `useImperativeHandle`。
