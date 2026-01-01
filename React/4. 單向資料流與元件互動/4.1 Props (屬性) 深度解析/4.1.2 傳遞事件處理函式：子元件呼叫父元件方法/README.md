# 4.1.2 傳遞事件處理函式：子元件呼叫父元件方法

<br />

## 基本概念

在 React 的單向資料流中，子元件無法直接修改父元件的狀態。當子元件需要通知父元件發生某些事件時，父元件會將事件處理函式作為 props 傳遞給子元件。

<br />

## 基本事件處理模式

### 1. 簡單事件 Callback

```jsx
function Button({ children, onClick, variant = 'primary' }) {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

function App() {
  const handleClick = () => {
    alert('按鈕被點擊了！');
  };

  return (
    <div>
      <Button onClick={handleClick}>
        點擊按鈕
      </Button>
    </div>
  );
}
```

### 2. 帶參數的事件處理

```jsx
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <div className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span className={todo.completed ? 'completed' : ''}>
        {todo.text}
      </span>
      <button onClick={() => onDelete(todo.id)}>
        刪除
      </button>
    </div>
  );
}

function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: '學習 React', completed: false },
    { id: 2, text: '完成專案', completed: true }
  ]);

  const handleToggle = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const handleDelete = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}
```

### 3. 事件物件傳遞

```jsx
function FormInput({ label, value, onChange, type = 'text' }) {
  return (
    <div className="form-field">
      <label>{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange} // 直接傳遞事件物件
      />
    </div>
  );
}

function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleInputChange = (field) => (e) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };

  return (
    <form>
      <FormInput
        label="姓名"
        value={formData.name}
        onChange={handleInputChange('name')}
      />
      <FormInput
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleInputChange('email')}
      />
    </form>
  );
}
```

<br />

## 複雜事件處理模式

### 1. 多重 Callback Function

```jsx
function ProductCard({ 
  product, 
  onAddToCart, 
  onAddToWishlist, 
  onViewDetails 
}) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>

      <div className="actions">
        <button onClick={() => onAddToCart(product)}>
          加入購物車
        </button>
        <button onClick={() => onAddToWishlist(product.id)}>
          加入願望清單
        </button>
        <button onClick={() => onViewDetails(product.id)}>
          查看詳情
        </button>
      </div>
    </div>
  );
}

function ProductGrid({ products }) {
  const [cart, setCart] = useState([]);
  const [wishlist, setWishlist] = useState([]);

  const handleAddToCart = (product) => {
    setCart(prev => [...prev, product]);
    console.log(`${product.name} 已加入購物車`);
  };

  const handleAddToWishlist = (productId) => {
    setWishlist(prev => [...prev, productId]);
    console.log(`產品 ${productId} 已加入願望清單`);
  };

  const handleViewDetails = (productId) => {
    console.log(`查看產品 ${productId} 詳情`);
  };

  return (
    <div className="product-grid">
      {products.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={handleAddToCart}
          onAddToWishlist={handleAddToWishlist}
          onViewDetails={handleViewDetails}
        />
      ))}
    </div>
  );
}
```

### 2. 條件事件處理

```jsx
function EditableText({ 
  text, 
  isEditing, 
  onEdit, 
  onSave, 
  onCancel 
}) {
  const [editValue, setEditValue] = useState(text);

  const handleSave = () => {
    onSave(editValue);
    setEditValue(text);
  };

  const handleCancel = () => {
    onCancel();
    setEditValue(text);
  };

  if (isEditing) {
    return (
      <div className="editing-mode">
        <input
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
          autoFocus
        />
        <button onClick={handleSave}>儲存</button>
        <button onClick={handleCancel}>取消</button>
      </div>
    );
  }

  return (
    <div className="display-mode">
      <span>{text}</span>
      <button onClick={onEdit}>編輯</button>
    </div>
  );
}

function TextManager() {
  const [text, setText] = useState('點擊編輯此文字');
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = (newText) => {
    setText(newText);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  return (
    <EditableText
      text={text}
      isEditing={isEditing}
      onEdit={handleEdit}
      onSave={handleSave}
      onCancel={handleCancel}
    />
  );
}
```

### 3. 非同步事件處理

```jsx
function FileUpload({ onUploadStart, onUploadSuccess, onUploadError }) {
  const [uploading, setUploading] = useState(false);

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    onUploadStart(file.name);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        onUploadSuccess(result);
      } else {
        throw new Error('上傳失敗');
      }
    } catch (error) {
      onUploadError(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={handleFileSelect}
        disabled={uploading}
      />
      {uploading && <p>上傳中...</p>}
    </div>
  );
}

function App() {
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUploadStart = (filename) => {
    setUploadStatus(`開始上傳：${filename}`);
  };

  const handleUploadSuccess = (result) => {
    setUploadStatus(`上傳成功：${result.filename}`);
  };

  const handleUploadError = (error) => {
    setUploadStatus(`上傳失敗：${error}`);
  };

  return (
    <div>
      <FileUpload
        onUploadStart={handleUploadStart}
        onUploadSuccess={handleUploadSuccess}
        onUploadError={handleUploadError}
      />
      <p>{uploadStatus}</p>
    </div>
  );
}
```

<br />

## 事件處理最佳化

### 1. 使用 `useCallback` 避免重新渲染

```jsx
function ExpensiveList({ items, onItemClick }) {
  console.log('ExpensiveList 重新渲染');

  return (
    <div>
      {items.map(item => (
        <ExpensiveItem
          key={item.id}
          item={item}
          onClick={onItemClick}
        />
      ))}
    </div>
  );
}

const ExpensiveItem = React.memo(function ExpensiveItem({ item, onClick }) {
  console.log(`ExpensiveItem ${item.id} 重新渲染`);

  return (
    <div onClick={() => onClick(item.id)}>
      {item.name}
    </div>
  );
});

function App() {
  const [items, setItems] = useState([
    { id: 1, name: '項目 1' },
    { id: 2, name: '項目 2' }
  ]);
  const [count, setCount] = useState(0);

  /** ❌ 每次渲染都建立新函式 */
  const handleItemClickBad = (id) => {
    console.log(`點擊項目：${id}`);
  };

  /** ✅ 使用 useCallback 最佳化 */
  const handleItemClick = useCallback((id) => {
    console.log(`點擊項目：${id}`);
  }, []);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        計數：{count}
      </button>
      <ExpensiveList 
        items={items} 
        onItemClick={handleItemClick}
      />
    </div>
  );
}
```

### 2. 事件委派模式

```jsx
function ListContainer({ items, onItemAction }) {
  const handleClick = (e) => {
    const itemId = e.target.closest('[data-item-id]')?.dataset.itemId;
    const action = e.target.dataset.action;

    if (itemId && action) {
      onItemAction(itemId, action);
    }
  };

  return (
    <div onClick={handleClick}>
      {items.map(item => (
        <div key={item.id} data-item-id={item.id}>
          <span>{item.name}</span>
          <button data-action="edit">編輯</button>
          <button data-action="delete">刪除</button>
          <button data-action="duplicate">複製</button>
        </div>
      ))}
    </div>
  );
}

function App() {
  const [items, setItems] = useState([
    { id: 1, name: '項目 1' },
    { id: 2, name: '項目 2' }
  ]);

  const handleItemAction = (itemId, action) => {
    switch (action) {
      case 'edit':
        console.log(`編輯項目：${itemId}`);
        break;
      case 'delete':
        setItems(items.filter(item => item.id !== parseInt(itemId)));
        break;
      case 'duplicate':
        const item = items.find(item => item.id === parseInt(itemId));
        if (item) {
          setItems([...items, { ...item, id: Date.now() }]);
        }
        break;
    }
  };

  return (
    <ListContainer 
      items={items} 
      onItemAction={handleItemAction}
    />
  );
}
```

<br />

## 表單事件處理

### 1. 統一表單處理

```jsx
function FormField({ 
  name, 
  label, 
  type = 'text', 
  value, 
  onChange, 
  error,
  required = false 
}) {
  return (
    <div className="form-field">
      <label>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        className={error ? 'error' : ''}
      />
      {error && <span className="error-message">{error}</span>}
    </div>
  );
}

function UserForm({ onSubmit, initialData = {} }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    ...initialData
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    /** 清除該欄位的錯誤 */
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = '姓名為必填欄位';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email 為必填欄位';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email 格式不正確';
    }

    if (!formData.age || formData.age < 1) {
      newErrors.age = '請輸入有效年齡';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormField
        name="name"
        label="姓名"
        value={formData.name}
        onChange={handleChange}
        error={errors.name}
        required
      />

      <FormField
        name="email"
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        error={errors.email}
        required
      />

      <FormField
        name="age"
        label="年齡"
        type="number"
        value={formData.age}
        onChange={handleChange}
        error={errors.age}
        required
      />

      <button type="submit">送出</button>
    </form>
  );
}

function App() {
  const handleFormSubmit = (data) => {
    console.log('表單資料：', data);
    // 處理表單送出
  };

  return (
    <UserForm onSubmit={handleFormSubmit} />
  );
}
```

### 2. 動態表單處理

```jsx
function DynamicForm({ fields, onSubmit }) {
  const [formData, setFormData] = useState({});

  const handleFieldChange = (fieldName) => (e) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map(field => (
        <div key={field.name} className="form-field">
          <label>{field.label}</label>
          {field.type === 'select' ? (
            <select
              value={formData[field.name] || ''}
              onChange={handleFieldChange(field.name)}
            >
              <option value="">請選擇</option>
              {field.options.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          ) : (
            <input
              type={field.type || 'text'}
              value={formData[field.name] || ''}
              onChange={handleFieldChange(field.name)}
            />
          )}
        </div>
      ))}
      <button type="submit">送出</button>
    </form>
  );
}

function App() {
  const formFields = [
    { name: 'name', label: '姓名', type: 'text' },
    { name: 'email', label: 'Email', type: 'email' },
    { 
      name: 'category', 
      label: '分類', 
      type: 'select',
      options: [
        { value: 'tech', label: '科技' },
        { value: 'business', label: '商業' },
        { value: 'design', label: '設計' }
      ]
    }
  ];

  const handleSubmit = (data) => {
    console.log('動態表單資料：', data);
  };

  return (
    <DynamicForm 
      fields={formFields} 
      onSubmit={handleSubmit}
    />
  );
}
```

<br />

## 錯誤處理與邊界情況

### 1. 安全的事件處理

```jsx
function SafeButton({ onClick, children, ...props }) {
  const handleClick = (e) => {
    try {
      /** 確保 onClick 是函式 */
      if (typeof onClick === 'function') {
        onClick(e);
      }
    } catch (error) {
      console.error('按鈕點擊處理發生錯誤：', error);
    }
  };

  return (
    <button onClick={handleClick} {...props}>
      {children}
    </button>
  );
}

function RobustComponent({ onAction }) {
  const handleAction = (data) => {
    /** 驗證資料 */
    if (!data || typeof data !== 'object') {
      console.warn('無效的資料格式');
      return;
    }

    /** 安全呼叫 Callback Function */
    try {
      onAction?.(data);
    } catch (error) {
      console.error('Callback Function 執行錯誤：', error);
    }
  };

  return (
    <SafeButton onClick={() => handleAction({ id: 1, name: '測試' })}>
      執行動作
    </SafeButton>
  );
}
```

<br />

## 最佳實務

- 使用描述性的 Callback Function 名稱

- 保持事件處理函式簡潔：把複雜部分拆分到獨立函式中

- 使用 useCallback 最佳化效能：避免不必要的重新渲染

- 提供預設的空函式：防止未傳遞 Callback Function 時的錯誤

- 適當的錯誤處理：捕獲並處理可能的異常

- 避免在 JSX 中定義函式：影響效能且難以除錯

- 使用事件委派：處理大量相似元素的事件

- 保持 Callback Function 介面穩定：避免頻繁更改參數結構
