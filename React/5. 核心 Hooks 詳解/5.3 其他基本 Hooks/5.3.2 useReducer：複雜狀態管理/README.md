# 5.3.2 `useReducer`：複雜狀態管理

<br />

## 基本概念

`useReducer` 是 React Hook，用於管理複雜的狀態更新。當狀態包含多個子值或下一個狀態依賴於前一個狀態時，`useReducer` 比 `useState` 更適合。

### 1. 基本語法

```jsx
import React, { useReducer } from 'react';

/** Reducer 函式 */
function counterReducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return { count: 0 };
    default:
      throw new Error(`未知的 action 類型: ${action.type}`);
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });

  return (
    <div>
      <p>計數：{state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>
        +1
      </button>
      <button onClick={() => dispatch({ type: 'decrement' })}>
        -1
      </button>
      <button onClick={() => dispatch({ type: 'reset' })}>
        重設
      </button>
    </div>
  );
}
```

### 2. 與 `useState` 的比較

```jsx
/** 使用 useState */
function CounterWithState() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(prev => prev + 1);
  const decrement = () => setCount(prev => prev - 1);
  const reset = () => setCount(0);

  return (
    <div>
      <p>計數：{count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
      <button onClick={reset}>重設</button>
    </div>
  );
}

/** 使用 useReducer */
function CounterWithReducer() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });

  return (
    <div>
      <p>計數：{state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>
      <button onClick={() => dispatch({ type: 'reset' })}>重設</button>
    </div>
  );
}
```

<br />

## 複雜狀態管理

### 1. 多欄位表單管理

```jsx
const formReducer = (state, action) => {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        [action.field]: action.value
      };
    case 'SET_ERROR':
      return {
        ...state,
        errors: {
          ...state.errors,
          [action.field]: action.error
        }
      };
    case 'CLEAR_ERRORS':
      return {
        ...state,
        errors: {}
      };
    case 'RESET_FORM':
      return {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        errors: {}
      };
    case 'SET_SUBMITTING':
      return {
        ...state,
        isSubmitting: action.isSubmitting
      };
    default:
      return state;
  }
};

function RegistrationForm() {
  const [state, dispatch] = useReducer(formReducer, {
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    errors: {},
    isSubmitting: false
  });

  const handleFieldChange = (field) => (e) => {
    dispatch({
      type: 'SET_FIELD',
      field,
      value: e.target.value
    });
  };

  const validateForm = () => {
    dispatch({ type: 'CLEAR_ERRORS' });

    if (!state.name.trim()) {
      dispatch({
        type: 'SET_ERROR',
        field: 'name',
        error: '姓名為必填'
      });
      return false;
    }

    if (!state.email.trim()) {
      dispatch({
        type: 'SET_ERROR',
        field: 'email',
        error: 'Email 為必填'
      });
      return false;
    }

    if (state.password.length < 6) {
      dispatch({
        type: 'SET_ERROR',
        field: 'password',
        error: '密碼至少需要 6 個字元'
      });
      return false;
    }

    if (state.password !== state.confirmPassword) {
      dispatch({
        type: 'SET_ERROR',
        field: 'confirmPassword',
        error: '確認密碼不符合'
      });
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    dispatch({ type: 'SET_SUBMITTING', isSubmitting: true });

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('註冊成功:', state);
      dispatch({ type: 'RESET_FORM' });
    } catch (error) {
      console.error('註冊失敗:', error);
    } finally {
      dispatch({ type: 'SET_SUBMITTING', isSubmitting: false });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          placeholder="姓名"
          value={state.name}
          onChange={handleFieldChange('name')}
        />
        {state.errors.name && <span className="error">{state.errors.name}</span>}
      </div>

      <div>
        <input
          type="email"
          placeholder="Email"
          value={state.email}
          onChange={handleFieldChange('email')}
        />
        {state.errors.email && <span className="error">{state.errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="密碼"
          value={state.password}
          onChange={handleFieldChange('password')}
        />
        {state.errors.password && <span className="error">{state.errors.password}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="確認密碼"
          value={state.confirmPassword}
          onChange={handleFieldChange('confirmPassword')}
        />
        {state.errors.confirmPassword && <span className="error">{state.errors.confirmPassword}</span>}
      </div>

      <button type="submit" disabled={state.isSubmitting}>
        {state.isSubmitting ? '註冊中...' : '註冊'}
      </button>
    </form>
  );
}
```

### 2. 購物車狀態管理

```jsx
const cartReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_ITEM':
      const existingItem = state.items.find(item => item.id === action.product.id);

      if (existingItem) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          )
        };
      } else {
        return {
          ...state,
          items: [...state.items, { ...action.product, quantity: 1 }]
        };
      }

    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.productId)
      };

    case 'UPDATE_QUANTITY':
      if (action.quantity <= 0) {
        return {
          ...state,
          items: state.items.filter(item => item.id !== action.productId)
        };
      }

      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.productId
            ? { ...item, quantity: action.quantity }
            : item
        )
      };

    case 'CLEAR_CART':
      return {
        ...state,
        items: []
      };

    case 'APPLY_DISCOUNT':
      return {
        ...state,
        discount: action.discount
      };

    case 'SET_SHIPPING':
      return {
        ...state,
        shipping: action.shipping
      };

    default:
      return state;
  }
};

function ShoppingCart() {
  const [cart, dispatch] = useReducer(cartReducer, {
    items: [],
    discount: 0,
    shipping: 0
  });

  const products = [
    { id: 1, name: '筆記型電腦', price: 30000 },
    { id: 2, name: '滑鼠', price: 500 },
    { id: 3, name: '鍵盤', price: 1500 }
  ];

  const addToCart = (product) => {
    dispatch({ type: 'ADD_ITEM', product });
  };

  const removeFromCart = (productId) => {
    dispatch({ type: 'REMOVE_ITEM', productId });
  };

  const updateQuantity = (productId, quantity) => {
    dispatch({ type: 'UPDATE_QUANTITY', productId, quantity });
  };

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' });
  };

  const applyDiscount = (discount) => {
    dispatch({ type: 'APPLY_DISCOUNT', discount });
  };

  const subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const discountAmount = subtotal * (cart.discount / 100);
  const total = subtotal - discountAmount + cart.shipping;

  return (
    <div>
      <div>
        <h3>商品列表</h3>
        {products.map(product => (
          <div key={product.id}>
            <span>{product.name} - NT$ {product.price}</span>
            <button onClick={() => addToCart(product)}>
              加入購物車
            </button>
          </div>
        ))}
      </div>

      <div>
        <h3>購物車 ({cart.items.length} 種商品)</h3>
        {cart.items.length === 0 ? (
          <p>購物車是空的</p>
        ) : (
          <>
            {cart.items.map(item => (
              <div key={item.id}>
                <span>{item.name}</span>
                <span>NT$ {item.price}</span>
                <input
                  type="number"
                  value={item.quantity}
                  onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                  min="1"
                />
                <span>小計：NT$ {item.price * item.quantity}</span>
                <button onClick={() => removeFromCart(item.id)}>移除</button>
              </div>
            ))}

            <div>
              <p>小計：NT$ {subtotal}</p>
              <p>折扣 ({cart.discount}%)：-NT$ {discountAmount}</p>
              <p>運費：NT$ {cart.shipping}</p>
              <p><strong>總計：NT$ {total}</strong></p>
            </div>

            <div>
              <button onClick={() => applyDiscount(10)}>套用 10% 折扣</button>
              <button onClick={() => dispatch({ type: 'SET_SHIPPING', shipping: 100 })}>
                設定運費 NT$ 100
              </button>
              <button onClick={clearCart}>清空購物車</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
```

### 3. 待辦事項管理

```jsx
const todoReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [
          ...state.todos,
          {
            id: Date.now(),
            text: action.text,
            completed: false,
            priority: action.priority || 'medium',
            createdAt: new Date().toISOString()
          }
        ]
      };

    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.id
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      };

    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.id)
      };

    case 'EDIT_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.id
            ? { ...todo, text: action.text }
            : todo
        )
      };

    case 'SET_FILTER':
      return {
        ...state,
        filter: action.filter
      };

    case 'SET_SORT':
      return {
        ...state,
        sortBy: action.sortBy
      };

    case 'CLEAR_COMPLETED':
      return {
        ...state,
        todos: state.todos.filter(todo => !todo.completed)
      };

    case 'MARK_ALL_COMPLETED':
      return {
        ...state,
        todos: state.todos.map(todo => ({ ...todo, completed: true }))
      };

    default:
      return state;
  }
};

function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, {
    todos: [],
    filter: 'all', // all, active, completed
    sortBy: 'createdAt' // createdAt, priority, alphabetical
  });

  const [newTodo, setNewTodo] = useState('');
  const [newPriority, setNewPriority] = useState('medium');

  const addTodo = () => {
    if (newTodo.trim()) {
      dispatch({
        type: 'ADD_TODO',
        text: newTodo,
        priority: newPriority
      });
      setNewTodo('');
    }
  };

  const getFilteredTodos = () => {
    let filtered = state.todos;

    /** 套用篩選 */
    switch (state.filter) {
      case 'active':
        filtered = filtered.filter(todo => !todo.completed);
        break;
      case 'completed':
        filtered = filtered.filter(todo => todo.completed);
        break;
      default:
        break;
    }

    /** 套用排序 */
    switch (state.sortBy) {
      case 'priority':
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        filtered.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
        break;
      case 'alphabetical':
        filtered.sort((a, b) => a.text.localeCompare(b.text));
        break;
      case 'createdAt':
      default:
        filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        break;
    }

    return filtered;
  };

  const filteredTodos = getFilteredTodos();
  const completedCount = state.todos.filter(todo => todo.completed).length;
  const activeCount = state.todos.length - completedCount;

  return (
    <div>
      <div>
        <h2>待辦事項管理</h2>
        <div>
          <input
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="新增待辦事項"
            onKeyPress={(e) => e.key === 'Enter' && addTodo()}
          />
          <select
            value={newPriority}
            onChange={(e) => setNewPriority(e.target.value)}
          >
            <option value="low">低優先度</option>
            <option value="medium">中優先度</option>
            <option value="high">高優先度</option>
          </select>
          <button onClick={addTodo}>新增</button>
        </div>
      </div>

      <div>
        <div>
          <span>篩選：</span>
          <button
            onClick={() => dispatch({ type: 'SET_FILTER', filter: 'all' })}
            className={state.filter === 'all' ? 'active' : ''}
          >
            全部 ({state.todos.length})
          </button>
          <button
            onClick={() => dispatch({ type: 'SET_FILTER', filter: 'active' })}
            className={state.filter === 'active' ? 'active' : ''}
          >
            進行中 ({activeCount})
          </button>
          <button
            onClick={() => dispatch({ type: 'SET_FILTER', filter: 'completed' })}
            className={state.filter === 'completed' ? 'active' : ''}
          >
            已完成 ({completedCount})
          </button>
        </div>

        <div>
          <span>排序：</span>
          <select
            value={state.sortBy}
            onChange={(e) => dispatch({ type: 'SET_SORT', sortBy: e.target.value })}
          >
            <option value="createdAt">建立時間</option>
            <option value="priority">優先度</option>
            <option value="alphabetical">字母順序</option>
          </select>
        </div>

        <div>
          <button onClick={() => dispatch({ type: 'MARK_ALL_COMPLETED' })}>
            全部標記為完成
          </button>
          <button onClick={() => dispatch({ type: 'CLEAR_COMPLETED' })}>
            清除已完成
          </button>
        </div>
      </div>

      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => dispatch({ type: 'TOGGLE_TODO', id: todo.id })}
            />
            <span
              style={{
                textDecoration: todo.completed ? 'line-through' : 'none',
                color: todo.priority === 'high' ? 'red' : 
                       todo.priority === 'medium' ? 'orange' : 'green'
              }}
            >
              {todo.text}
            </span>
            <span>({todo.priority})</span>
            <button onClick={() => dispatch({ type: 'DELETE_TODO', id: todo.id })}>
              刪除
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

<br />

## 進階模式

### 1. 初始化函式

```jsx
function init(initialCount) {
  return {
    count: initialCount,
    history: [initialCount]
  };
}

function counterReducer(state, action) {
  switch (action.type) {
    case 'increment':
      const newCount = state.count + 1;
      return {
        count: newCount,
        history: [...state.history, newCount]
      };
    case 'decrement':
      const decrementedCount = state.count - 1;
      return {
        count: decrementedCount,
        history: [...state.history, decrementedCount]
      };
    case 'reset':
      return init(action.payload);
    default:
      return state;
  }
}

function CounterWithHistory({ initialCount = 0 }) {
  const [state, dispatch] = useReducer(counterReducer, initialCount, init);

  return (
    <div>
      <p>目前計數：{state.count}</p>
      <p>歷史記錄：{state.history.join(' → ')}</p>

      <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>
      <button onClick={() => dispatch({ type: 'reset', payload: 0 })}>
        重設為 0
      </button>
      <button onClick={() => dispatch({ type: 'reset', payload: 10 })}>
        重設為 10
      </button>
    </div>
  );
}
```

### 2. 中間件模式

```jsx
function withLogging(reducer) {
  return (state, action) => {
    console.group(`Action: ${action.type}`);
    console.log('Previous State:', state);
    console.log('Action:', action);

    const newState = reducer(state, action);

    console.log('New State:', newState);
    console.groupEnd();

    return newState;
  };
}

function withUndo(reducer) {
  return (state, action) => {
    if (action.type === 'UNDO') {
      return {
        ...state,
        present: state.past[state.past.length - 1],
        past: state.past.slice(0, -1),
        future: [state.present, ...state.future]
      };
    }

    if (action.type === 'REDO') {
      return {
        ...state,
        present: state.future[0],
        past: [...state.past, state.present],
        future: state.future.slice(1)
      };
    }

    const newPresent = reducer(state.present, action);

    if (newPresent === state.present) {
      return state;
    }

    return {
      past: [...state.past, state.present],
      present: newPresent,
      future: []
    };
  };
}

const enhancedReducer = withLogging(withUndo(counterReducer));

function UndoableCounter() {
  const [state, dispatch] = useReducer(enhancedReducer, {
    past: [],
    present: { count: 0 },
    future: []
  });

  const canUndo = state.past.length > 0;
  const canRedo = state.future.length > 0;

  return (
    <div>
      <p>計數：{state.present.count}</p>

      <button onClick={() => dispatch({ type: 'increment' })}>+1</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-1</button>

      <button onClick={() => dispatch({ type: 'UNDO' })} disabled={!canUndo}>
        復原
      </button>
      <button onClick={() => dispatch({ type: 'REDO' })} disabled={!canRedo}>
        重做
      </button>

      <p>可復原：{canUndo ? '是' : '否'}</p>
      <p>可重做：{canRedo ? '是' : '否'}</p>
    </div>
  );
}
```

### 3. 組合多個 Reducer

```jsx
function combineReducers(reducers) {
  return (state, action) => {
    const newState = {};
    let hasChanged = false;

    for (const key in reducers) {
      const reducer = reducers[key];
      const previousStateForKey = state[key];
      const nextStateForKey = reducer(previousStateForKey, action);

      newState[key] = nextStateForKey;
      hasChanged = hasChanged || nextStateForKey !== previousStateForKey;
    }

    return hasChanged ? newState : state;
  };
}

const userReducer = (state = { name: '', email: '' }, action) => {
  switch (action.type) {
    case 'SET_USER_NAME':
      return { ...state, name: action.payload };
    case 'SET_USER_EMAIL':
      return { ...state, email: action.payload };
    default:
      return state;
  }
};

const settingsReducer = (state = { theme: 'light', language: 'zh-TW' }, action) => {
  switch (action.type) {
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    case 'SET_LANGUAGE':
      return { ...state, language: action.payload };
    default:
      return state;
  }
};

const rootReducer = combineReducers({
  user: userReducer,
  settings: settingsReducer
});

function App() {
  const [state, dispatch] = useReducer(rootReducer, {
    user: { name: '', email: '' },
    settings: { theme: 'light', language: 'zh-TW' }
  });

  return (
    <div>
      <div>
        <h3>使用者資訊</h3>
        <input
          placeholder="姓名"
          value={state.user.name}
          onChange={(e) => dispatch({ type: 'SET_USER_NAME', payload: e.target.value })}
        />
        <input
          placeholder="Email"
          value={state.user.email}
          onChange={(e) => dispatch({ type: 'SET_USER_EMAIL', payload: e.target.value })}
        />
      </div>

      <div>
        <h3>設定</h3>
        <select
          value={state.settings.theme}
          onChange={(e) => dispatch({ type: 'SET_THEME', payload: e.target.value })}
        >
          <option value="light">淺色</option>
          <option value="dark">深色</option>
        </select>

        <select
          value={state.settings.language}
          onChange={(e) => dispatch({ type: 'SET_LANGUAGE', payload: e.target.value })}
        >
          <option value="zh-TW">繁體中文</option>
          <option value="en-US">English</option>
        </select>
      </div>

      <div>
        <h3>目前狀態</h3>
        <pre>{JSON.stringify(state, null, 2)}</pre>
      </div>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 何時使用 `useReducer`

- 複雜狀態結構：狀態包含多個子值

- 狀態更新較複雜：下一個狀態依賴前一個狀態

- 狀態更新分散：多個元件需要更新同一個狀態

- 需要可預測的狀態更新：集中管理狀態變更流程

### 2. Reducer 設計原則

- 純函式：不產生副作用，相同輸入產生相同輸出

- 不可變更新：返回新的狀態物件

- 可預測性：狀態變更流程清晰明確

- 可測試性：易於單元測試

### 3. Action 設計規範

- 描述性命名：使用動詞描述要執行的動作

- 一致的結構：包含 type 和 payload

- 避免副作用：Action 只描述發生什麼，不包含業務流程

- 可序列化：便於除錯和時間旅行
