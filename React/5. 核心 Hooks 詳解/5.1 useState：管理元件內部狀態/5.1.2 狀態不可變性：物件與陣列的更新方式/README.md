# 5.1.2 狀態不可變性：物件與陣列的更新方式

<br />

## 不可變性基本概念

React 狀態更新必須遵循不可變性原則，即不能直接修改現有的狀態物件或陣列，而是要建立新的物件或陣列來觸發重新渲染。

### 1. 為什麼需要不可變性

```jsx
function ImmutabilityExample() {
  const [user, setUser] = useState({ name: 'John', age: 30 });

  /** ❌ 錯誤：直接修改物件 */
  const updateAgeWrong = () => {
    user.age = 31;
    setUser(user); // React 不會重新渲染，因為參考相同
    console.log('不會觸發重新渲染');
  };

  /** ✅ 正確：建立新物件 */
  const updateAgeCorrect = () => {
    setUser(prevUser => ({
      ...prevUser,
      age: 31
    }));
    console.log('會觸發重新渲染');
  };

  return (
    <div>
      <p>姓名：{user.name}</p>
      <p>年齡：{user.age}</p>
      <button onClick={updateAgeWrong}>錯誤更新</button>
      <button onClick={updateAgeCorrect}>正確更新</button>
    </div>
  );
}
```

### 2. 物件參考比較

```jsx
function ReferenceComparison() {
  const [data, setData] = useState({ count: 0 });
  const [renderCount, setRenderCount] = useState(0);

  useEffect(() => {
    setRenderCount(prev => prev + 1);
  });

  const mutateObject = () => {
    data.count += 1;
    setData(data); // 相同參考，不會重新渲染
  };

  const createNewObject = () => {
    setData(prevData => ({
      ...prevData,
      count: prevData.count + 1
    })); // 新參考，會重新渲染
  };

  return (
    <div>
      <p>計數：{data.count}</p>
      <p>渲染次數：{renderCount}</p>
      <button onClick={mutateObject}>修改物件 (不會重新渲染)</button>
      <button onClick={createNewObject}>建立新物件 (會重新渲染)</button>
    </div>
  );
}
```

<br />

## 物件狀態更新

### 1. 淺層物件更新

```jsx
function ShallowObjectUpdate() {
  const [user, setUser] = useState({
    name: 'Charmy',
    email: 'charmy@example.com',
    age: 25,
    isActive: true
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

  const toggleActive = () => {
    setUser(prevUser => ({
      ...prevUser,
      isActive: !prevUser.isActive
    }));
  };

  const incrementAge = () => {
    setUser(prevUser => ({
      ...prevUser,
      age: prevUser.age + 1
    }));
  };

  return (
    <div>
      <div>
        <input 
          value={user.name}
          onChange={(e) => updateName(e.target.value)}
          placeholder="姓名"
        />
      </div>

      <div>
        <input 
          value={user.email}
          onChange={(e) => updateEmail(e.target.value)}
          placeholder="Email"
        />
      </div>

      <div>
        <button onClick={incrementAge}>
          年齡：{user.age} (+1)
        </button>
      </div>

      <div>
        <button onClick={toggleActive}>
          狀態：{user.isActive ? '啟用' : '停用'}
        </button>
      </div>

      <div>
        <h3>使用者資訊：</h3>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>
    </div>
  );
}
```

### 2. 深層物件更新

```jsx
function DeepObjectUpdate() {
  const [profile, setProfile] = useState({
    personal: {
      name: 'John',
      age: 30,
      contact: {
        email: 'john@example.com',
        phone: '123-456-7890'
      }
    },
    preferences: {
      theme: 'light',
      language: 'zh-TW',
      notifications: {
        email: true,
        sms: false,
        push: true
      }
    }
  });

  const updateName = (newName) => {
    setProfile(prevProfile => ({
      ...prevProfile,
      personal: {
        ...prevProfile.personal,
        name: newName
      }
    }));
  };

  const updateEmail = (newEmail) => {
    setProfile(prevProfile => ({
      ...prevProfile,
      personal: {
        ...prevProfile.personal,
        contact: {
          ...prevProfile.personal.contact,
          email: newEmail
        }
      }
    }));
  };

  const updateTheme = (newTheme) => {
    setProfile(prevProfile => ({
      ...prevProfile,
      preferences: {
        ...prevProfile.preferences,
        theme: newTheme
      }
    }));
  };

  const toggleEmailNotification = () => {
    setProfile(prevProfile => ({
      ...prevProfile,
      preferences: {
        ...prevProfile.preferences,
        notifications: {
          ...prevProfile.preferences.notifications,
          email: !prevProfile.preferences.notifications.email
        }
      }
    }));
  };

  return (
    <div>
      <div>
        <input 
          value={profile.personal.name}
          onChange={(e) => updateName(e.target.value)}
          placeholder="姓名"
        />
      </div>

      <div>
        <input 
          value={profile.personal.contact.email}
          onChange={(e) => updateEmail(e.target.value)}
          placeholder="Email"
        />
      </div>

      <div>
        <select 
          value={profile.preferences.theme}
          onChange={(e) => updateTheme(e.target.value)}
        >
          <option value="light">淺色主題</option>
          <option value="dark">深色主題</option>
        </select>
      </div>

      <div>
        <label>
          <input 
            type="checkbox"
            checked={profile.preferences.notifications.email}
            onChange={toggleEmailNotification}
          />
          Email 通知
        </label>
      </div>

      <div>
        <h3>個人檔案：</h3>
        <pre>{JSON.stringify(profile, null, 2)}</pre>
      </div>
    </div>
  );
}
```

### 3. 使用 `immer` 簡化深層更新

```jsx
import { produce } from 'immer';

function ImmerExample() {
  const [state, setState] = useState({
    user: {
      profile: {
        name: 'Charmy',
        settings: {
          theme: 'light',
          notifications: {
            email: true,
            push: false
          }
        }
      }
    }
  });

  const updateWithImmer = (newName) => {
    setState(produce(draft => {
      draft.user.profile.name = newName;
    }));
  };

  const toggleEmailNotification = () => {
    setState(produce(draft => {
      draft.user.profile.settings.notifications.email = 
        !draft.user.profile.settings.notifications.email;
    }));
  };

  return (
    <div>
      <input 
        value={state.user.profile.name}
        onChange={(e) => updateWithImmer(e.target.value)}
        placeholder="姓名"
      />

      <label>
        <input 
          type="checkbox"
          checked={state.user.profile.settings.notifications.email}
          onChange={toggleEmailNotification}
        />
        Email 通知
      </label>

      <pre>{JSON.stringify(state, null, 2)}</pre>
    </div>
  );
}
```

<br />

## 陣列狀態更新

### 1. 基本陣列操作

```jsx
function BasicArrayOperations() {
  const [items, setItems] = useState(['蘋果', '香蕉', '橘子']);
  const [newItem, setNewItem] = useState('');

  /** 新增項目 */
  const addItem = () => {
    if (newItem.trim()) {
      setItems(prevItems => [...prevItems, newItem]);
      setNewItem('');
    }
  };

  /** 在開頭新增 */
  const addToBeginning = () => {
    if (newItem.trim()) {
      setItems(prevItems => [newItem, ...prevItems]);
      setNewItem('');
    }
  };

  /** 在指定位置插入 */
  const insertAt = (index) => {
    if (newItem.trim()) {
      setItems(prevItems => [
        ...prevItems.slice(0, index),
        newItem,
        ...prevItems.slice(index)
      ]);
      setNewItem('');
    }
  };

  /** 刪除項目 */
  const removeItem = (index) => {
    setItems(prevItems => prevItems.filter((_, i) => i !== index));
  };

  /** 更新項目 */
  const updateItem = (index, newValue) => {
    setItems(prevItems => 
      prevItems.map((item, i) => i === index ? newValue : item)
    );
  };

  /** 移動項目 */
  const moveItem = (fromIndex, toIndex) => {
    setItems(prevItems => {
      const newItems = [...prevItems];
      const [movedItem] = newItems.splice(fromIndex, 1);
      newItems.splice(toIndex, 0, movedItem);
      return newItems;
    });
  };

  return (
    <div>
      <div>
        <input 
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          placeholder="新項目"
        />
        <button onClick={addItem}>新增到結尾</button>
        <button onClick={addToBeginning}>新增到開頭</button>
        <button onClick={() => insertAt(1)}>插入到位置 1</button>
      </div>

      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <input 
              value={item}
              onChange={(e) => updateItem(index, e.target.value)}
            />
            <button onClick={() => removeItem(index)}>刪除</button>
            {index > 0 && (
              <button onClick={() => moveItem(index, index - 1)}>↑</button>
            )}
            {index < items.length - 1 && (
              <button onClick={() => moveItem(index, index + 1)}>↓</button>
            )}
          </li>
        ))}
      </ul>

      <p>總計：{items.length} 個項目</p>
    </div>
  );
}
```

### 2. 物件陣列操作

```jsx
function ObjectArrayOperations() {
  const [todos, setTodos] = useState([
    { id: 1, text: '學習 React', completed: false, priority: 'high' },
    { id: 2, text: '完成專案', completed: true, priority: 'medium' },
    { id: 3, text: '寫文件', completed: false, priority: 'low' }
  ]);

  const [newTodo, setNewTodo] = useState('');

  /** 新增待辦事項 */
  const addTodo = () => {
    if (newTodo.trim()) {
      const todo = {
        id: Date.now(),
        text: newTodo,
        completed: false,
        priority: 'medium'
      };
      setTodos(prevTodos => [...prevTodos, todo]);
      setNewTodo('');
    }
  };

  /** 切換完成狀態 */
  const toggleTodo = (id) => {
    setTodos(prevTodos => 
      prevTodos.map(todo =>
        todo.id === id 
          ? { ...todo, completed: !todo.completed }
          : todo
      )
    );
  };

  /** 更新文字 */
  const updateTodoText = (id, newText) => {
    setTodos(prevTodos => 
      prevTodos.map(todo =>
        todo.id === id 
          ? { ...todo, text: newText }
          : todo
      )
    );
  };

  /** 更新優先度 */
  const updatePriority = (id, newPriority) => {
    setTodos(prevTodos => 
      prevTodos.map(todo =>
        todo.id === id 
          ? { ...todo, priority: newPriority }
          : todo
      )
    );
  };

  /** 刪除待辦事項 */
  const deleteTodo = (id) => {
    setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
  };

  /** 批次操作 */
  const markAllCompleted = () => {
    setTodos(prevTodos => 
      prevTodos.map(todo => ({ ...todo, completed: true }))
    );
  };

  const clearCompleted = () => {
    setTodos(prevTodos => prevTodos.filter(todo => !todo.completed));
  };

  const completedCount = todos.filter(todo => todo.completed).length;

  return (
    <div>
      <div>
        <input 
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="新增待辦事項"
          onKeyPress={(e) => e.key === 'Enter' && addTodo()}
        />
        <button onClick={addTodo}>新增</button>
      </div>

      <div>
        <button onClick={markAllCompleted}>全部標記為完成</button>
        <button onClick={clearCompleted}>清除已完成</button>
        <span>已完成：{completedCount}/{todos.length}</span>
      </div>

      <ul>
        {todos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'completed' : ''}>
            <input 
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />

            <input 
              value={todo.text}
              onChange={(e) => updateTodoText(todo.id, e.target.value)}
              style={{ 
                textDecoration: todo.completed ? 'line-through' : 'none' 
              }}
            />

            <select 
              value={todo.priority}
              onChange={(e) => updatePriority(todo.id, e.target.value)}
            >
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
            </select>

            <button onClick={() => deleteTodo(todo.id)}>刪除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 3. 巢狀陣列操作

```jsx
function NestedArrayOperations() {
  const [categories, setCategories] = useState([
    {
      id: 1,
      name: '工作',
      items: [
        { id: 101, text: '開會', completed: false },
        { id: 102, text: '寫報告', completed: true }
      ]
    },
    {
      id: 2,
      name: '個人',
      items: [
        { id: 201, text: '運動', completed: false },
        { id: 202, text: '讀書', completed: false }
      ]
    }
  ]);

  /** 新增分類 */
  const addCategory = (name) => {
    const newCategory = {
      id: Date.now(),
      name,
      items: []
    };
    setCategories(prev => [...prev, newCategory]);
  };

  /** 新增項目到指定分類 */
  const addItemToCategory = (categoryId, text) => {
    const newItem = {
      id: Date.now(),
      text,
      completed: false
    };

    setCategories(prevCategories =>
      prevCategories.map(category =>
        category.id === categoryId
          ? { ...category, items: [...category.items, newItem] }
          : category
      )
    );
  };

  /** 切換項目完成狀態 */
  const toggleItem = (categoryId, itemId) => {
    setCategories(prevCategories =>
      prevCategories.map(category =>
        category.id === categoryId
          ? {
              ...category,
              items: category.items.map(item =>
                item.id === itemId
                  ? { ...item, completed: !item.completed }
                  : item
              )
            }
          : category
      )
    );
  };

  /** 刪除項目 */
  const deleteItem = (categoryId, itemId) => {
    setCategories(prevCategories =>
      prevCategories.map(category =>
        category.id === categoryId
          ? {
              ...category,
              items: category.items.filter(item => item.id !== itemId)
            }
          : category
      )
    );
  };

  /** 刪除分類 */
  const deleteCategory = (categoryId) => {
    setCategories(prev => prev.filter(category => category.id !== categoryId));
  };

  return (
    <div>
      <button onClick={() => addCategory(prompt('分類名稱：'))}>
        新增分類
      </button>

      {categories.map(category => (
        <div key={category.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
          <div>
            <h3>{category.name}</h3>
            <button onClick={() => deleteCategory(category.id)}>
              刪除分類
            </button>
            <button onClick={() => {
              const text = prompt('項目內容：');
              if (text) addItemToCategory(category.id, text);
            }}>
              新增項目
            </button>
          </div>

          <ul>
            {category.items.map(item => (
              <li key={item.id}>
                <input 
                  type="checkbox"
                  checked={item.completed}
                  onChange={() => toggleItem(category.id, item.id)}
                />
                <span style={{ 
                  textDecoration: item.completed ? 'line-through' : 'none' 
                }}>
                  {item.text}
                </span>
                <button onClick={() => deleteItem(category.id, item.id)}>
                  刪除
                </button>
              </li>
            ))}
          </ul>

          <p>
            完成度：{category.items.filter(item => item.completed).length}/{category.items.length}
          </p>
        </div>
      ))}
    </div>
  );
}
```

<br />

## 效能最佳化技巧

### 1. 避免不必要的物件建立

```jsx
function PerformanceOptimization() {
  const [user, setUser] = useState({
    name: 'John',
    email: 'john@example.com',
    preferences: {
      theme: 'light',
      language: 'zh-TW'
    }
  });

  /** ❌ 每次都建立新物件，即使值沒變 */
  const updateNameBad = (newName) => {
    setUser(prevUser => ({
      ...prevUser,
      name: newName,
      preferences: {
        ...prevUser.preferences // 不必要的複製
      }
    }));
  };

  /** ✅ 只更新需要變更的部分 */
  const updateNameGood = (newName) => {
    setUser(prevUser => ({
      ...prevUser,
      name: newName
    }));
  };

  /** ✅ 檢查值是否真的改變 */
  const updateNameOptimal = (newName) => {
    setUser(prevUser => {
      if (prevUser.name === newName) {
        return prevUser; // 返回相同參考，避免重新渲染
      }
      return {
        ...prevUser,
        name: newName
      };
    });
  };

  return (
    <div>
      <input 
        value={user.name}
        onChange={(e) => updateNameOptimal(e.target.value)}
        placeholder="姓名"
      />
      <p>姓名：{user.name}</p>
      <p>Email：{user.email}</p>
    </div>
  );
}
```

### 2. 使用 useCallback 最佳化陣列操作

```jsx
function OptimizedArrayOperations() {
  const [items, setItems] = useState([
    { id: 1, name: '項目 1', completed: false },
    { id: 2, name: '項目 2', completed: true }
  ]);

  const toggleItem = useCallback((id) => {
    setItems(prevItems =>
      prevItems.map(item =>
        item.id === id
          ? { ...item, completed: !item.completed }
          : item
      )
    );
  }, []);

  const deleteItem = useCallback((id) => {
    setItems(prevItems => prevItems.filter(item => item.id !== id));
  }, []);

  const updateItemName = useCallback((id, newName) => {
    setItems(prevItems =>
      prevItems.map(item =>
        item.id === id
          ? { ...item, name: newName }
          : item
      )
    );
  }, []);

  return (
    <div>
      {items.map(item => (
        <OptimizedItem
          key={item.id}
          item={item}
          onToggle={toggleItem}
          onDelete={deleteItem}
          onUpdateName={updateItemName}
        />
      ))}
    </div>
  );
}

const OptimizedItem = React.memo(function OptimizedItem({ 
  item, 
  onToggle, 
  onDelete, 
  onUpdateName 
}) {
  return (
    <div>
      <input 
        type="checkbox"
        checked={item.completed}
        onChange={() => onToggle(item.id)}
      />
      <input 
        value={item.name}
        onChange={(e) => onUpdateName(item.id, e.target.value)}
      />
      <button onClick={() => onDelete(item.id)}>刪除</button>
    </div>
  );
});
```

<br />

## 常見錯誤與解決方案

### 1. 直接修改狀態

```jsx
function CommonMistakes() {
  const [user, setUser] = useState({ name: 'John', hobbies: ['reading'] });

  /** ❌ 錯誤：直接修改物件屬性 */
  const addHobbyWrong = () => {
    user.hobbies.push('swimming');
    setUser(user); // 不會觸發重新渲染
  };

  /** ❌ 錯誤：修改後再設定 */
  const addHobbyStillWrong = () => {
    const updatedUser = user;
    updatedUser.hobbies.push('swimming');
    setUser(updatedUser); // 仍然是相同參考
  };

  /** ✅ 正確：建立新物件和新陣列 */
  const addHobbyCorrect = () => {
    setUser(prevUser => ({
      ...prevUser,
      hobbies: [...prevUser.hobbies, 'swimming']
    }));
  };

  return (
    <div>
      <p>姓名：{user.name}</p>
      <p>興趣：{user.hobbies.join(', ')}</p>
      <button onClick={addHobbyCorrect}>新增興趣</button>
    </div>
  );
}
```

### 2. 狀態更新時機問題

```jsx
function TimingIssues() {
  const [items, setItems] = useState([]);

  /** ❌ 錯誤：依賴可能過時的狀態 */
  const addMultipleItemsWrong = () => {
    setItems([...items, 'item1']);
    setItems([...items, 'item2']); // items 仍然是舊值
  };

  /** ✅ 正確：使用函式式更新 */
  const addMultipleItemsCorrect = () => {
    setItems(prev => [...prev, 'item1']);
    setItems(prev => [...prev, 'item2']);
  };

  /** ✅ 更好：一次更新多個項目 */
  const addMultipleItemsBest = () => {
    setItems(prev => [...prev, 'item1', 'item2']);
  };

  return (
    <div>
      <p>項目：{items.join(', ')}</p>
      <button onClick={addMultipleItemsBest}>新增多個項目</button>
    </div>
  );
}
```

<br />

## 最佳實務總結

### 1. 物件更新原則

- 使用展開運算子：建立新物件時複製現有屬性

- 避免深層複製：只複製需要變更的層級

- 檢查值是否改變：避免不必要的狀態更新

- 考慮使用 Immer：簡化複雜的深層更新

### 2. 陣列更新原則

- 使用陣列方法：`filter`、`map`、`concat` 等不會修改原陣列

- 避免 mutating 方法：`push`、`pop`、`splice`、`sort` 等

- 保持項目唯一性：使用穩定的 key 值

- 批次更新：一次更新多個變更而非分別更新

### 3. 效能考量

- `React.memo`：避免不必要的重新渲染

- `useCallback`：穩定的 Callback Function 參考

- `useMemo`：快取計算結果

- 狀態結構最佳化：避免過度巢狀的狀態結構
