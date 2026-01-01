# 4.3.1 受控元件與非受控元件的實務應用

<br />

## 受控元件 (Controlled Components)

### 1. 基本概念

受控元件是指表單元素的值由 React 狀態控制，所有的輸入變更都透過事件處理函式來更新狀態。

```jsx
function ControlledInput() {
  const [value, setValue] = useState('');

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  return (
    <div>
      <input 
        type="text"
        value={value}
        onChange={handleChange}
        placeholder="受控輸入框"
      />
      <p>目前值：{value}</p>
    </div>
  );
}
```

### 2. 完整表單範例

```jsx
function ControlledForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    gender: '',
    interests: [],
    newsletter: false,
    comments: ''
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

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
      </div>

      <div>
        <label>Email：</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>

      <div>
        <label>年齡：</label>
        <input
          name="age"
          type="number"
          value={formData.age}
          onChange={handleInputChange}
          min="1"
          max="120"
        />
      </div>

      <div>
        <label>性別：</label>
        <select 
          name="gender" 
          value={formData.gender} 
          onChange={handleInputChange}
        >
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
        <label>備註：</label>
        <textarea
          name="comments"
          value={formData.comments}
          onChange={handleInputChange}
          rows="4"
          cols="50"
        />
      </div>

      <button type="submit">送出</button>
    </form>
  );
}
```

### 3. 即時驗證

```jsx
function ControlledFormWithValidation() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});

  const validateField = (name, value) => {
    switch (name) {
      case 'username':
        if (value.length < 3) {
          return '使用者名稱至少需要 3 個字元';
        }
        if (!/^[a-zA-Z0-9_]+$/.test(value)) {
          return '使用者名稱只能包含字母、數字和底線';
        }
        break;

      case 'email':
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return 'Email 格式不正確';
        }
        break;

      case 'password':
        if (value.length < 8) {
          return '密碼至少需要 8 個字元';
        }
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          return '密碼需包含大小寫字母和數字';
        }
        break;

      case 'confirmPassword':
        if (value !== formData.password) {
          return '確認密碼不符合';
        }
        break;
    }
    return '';
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    /** 即時驗證 */
    const error = validateField(name, value);
    setErrors(prev => ({
      ...prev,
      [name]: error
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    /** 完整驗證 */
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      const error = validateField(key, formData[key]);
      if (error) newErrors[key] = error;
    });

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      console.log('表單驗證通過：', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>使用者名稱：</label>
        <input
          name="username"
          value={formData.username}
          onChange={handleChange}
          className={errors.username ? 'error' : ''}
        />
        {errors.username && (
          <span className="error-message">{errors.username}</span>
        )}
      </div>

      <div>
        <label>Email：</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
        />
        {errors.email && (
          <span className="error-message">{errors.email}</span>
        )}
      </div>

      <div>
        <label>密碼：</label>
        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          className={errors.password ? 'error' : ''}
        />
        {errors.password && (
          <span className="error-message">{errors.password}</span>
        )}
      </div>

      <div>
        <label>確認密碼：</label>
        <input
          name="confirmPassword"
          type="password"
          value={formData.confirmPassword}
          onChange={handleChange}
          className={errors.confirmPassword ? 'error' : ''}
        />
        {errors.confirmPassword && (
          <span className="error-message">{errors.confirmPassword}</span>
        )}
      </div>

      <button type="submit">註冊</button>
    </form>
  );
}
```

<br />

## 非受控元件 (Uncontrolled Components)

### 1. 基本概念

非受控元件是指表單元素的值由 DOM 本身管理，React 透過 `ref` 來存取元素的值。

```jsx
function UncontrolledInput() {
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('輸入值：', inputRef.current.value);
  };

  const handleFocus = () => {
    inputRef.current.focus();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        ref={inputRef}
        type="text"
        defaultValue="預設值"
        placeholder="非受控輸入框"
      />
      <button type="submit">送出</button>
      <button type="button" onClick={handleFocus}>
        聚焦輸入框
      </button>
    </form>
  );
}
```

### 2. 完整表單範例

```jsx
function UncontrolledForm() {
  const formRef = useRef(null);
  const nameRef = useRef(null);
  const emailRef = useRef(null);
  const ageRef = useRef(null);
  const genderRef = useRef(null);
  const commentsRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    /** 方式一：使用個別 ref */
    const formData = {
      name: nameRef.current.value,
      email: emailRef.current.value,
      age: ageRef.current.value,
      gender: genderRef.current.value,
      comments: commentsRef.current.value
    };

    console.log('使用 ref 取得的資料：', formData);

    /** 方式二：使用 FormData API */
    const formDataAPI = new FormData(formRef.current);
    const data = Object.fromEntries(formDataAPI);

    console.log('使用 FormData 取得的資料：', data);
  };

  const handleReset = () => {
    formRef.current.reset();
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input
          ref={nameRef}
          name="name"
          type="text"
          defaultValue=""
          required
        />
      </div>

      <div>
        <label>Email：</label>
        <input
          ref={emailRef}
          name="email"
          type="email"
          defaultValue=""
          required
        />
      </div>

      <div>
        <label>年齡：</label>
        <input
          ref={ageRef}
          name="age"
          type="number"
          defaultValue=""
          min="1"
          max="120"
        />
      </div>

      <div>
        <label>性別：</label>
        <select ref={genderRef} name="gender" defaultValue="">
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
            defaultChecked={false}
          />
          閱讀
        </label>
        <label>
          <input
            type="checkbox"
            name="interests"
            value="sports"
            defaultChecked={false}
          />
          運動
        </label>
        <label>
          <input
            type="checkbox"
            name="interests"
            value="music"
            defaultChecked={true}
          />
          音樂
        </label>
      </div>

      <div>
        <label>
          <input
            name="newsletter"
            type="checkbox"
            defaultChecked={false}
          />
          訂閱電子報
        </label>
      </div>

      <div>
        <label>備註：</label>
        <textarea
          ref={commentsRef}
          name="comments"
          defaultValue=""
          rows="4"
          cols="50"
        />
      </div>

      <button type="submit">送出</button>
      <button type="button" onClick={handleReset}>重設</button>
    </form>
  );
}
```

### 3. 檔案上傳處理

```jsx
function FileUploadForm() {
  const fileInputRef = useRef(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);

    console.log('選擇的檔案：', files.map(f => ({
      name: f.name,
      size: f.size,
      type: f.type
    })));
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    const files = fileInputRef.current.files;
    if (files.length === 0) {
      alert('請選擇檔案');
      return;
    }

    setUploadStatus('上傳中...');

    try {
      const formData = new FormData();
      Array.from(files).forEach(file => {
        formData.append('files', file);
      });

      /** 模擬上傳 */
      await new Promise(resolve => setTimeout(resolve, 2000));

      setUploadStatus('上傳成功！');
      fileInputRef.current.value = '';
      setSelectedFiles([]);
    } catch (error) {
      setUploadStatus('上傳失敗：' + error.message);
    }
  };

  const handleClearFiles = () => {
    fileInputRef.current.value = '';
    setSelectedFiles([]);
    setUploadStatus('');
  };

  return (
    <form onSubmit={handleUpload}>
      <div>
        <label>選擇檔案：</label>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".jpg,.jpeg,.png,.pdf,.doc,.docx"
          onChange={handleFileSelect}
        />
      </div>

      {selectedFiles.length > 0 && (
        <div>
          <h4>已選擇的檔案：</h4>
          <ul>
            {selectedFiles.map((file, index) => (
              <li key={index}>
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </li>
            ))}
          </ul>
        </div>
      )}

      {uploadStatus && (
        <div className={uploadStatus.includes('成功') ? 'success' : 'info'}>
          {uploadStatus}
        </div>
      )}

      <div>
        <button type="submit" disabled={selectedFiles.length === 0}>
          上傳檔案
        </button>
        <button type="button" onClick={handleClearFiles}>
          清除選擇
        </button>
      </div>
    </form>
  );
}
```

<br />

## 混合使用策略

### 1. 部分受控元件

```jsx
function HybridForm() {
  /** 受控的重要欄位 */
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');

  /** 非受控的次要欄位 */
  const nameRef = useRef(null);
  const phoneRef = useRef(null);
  const addressRef = useRef(null);

  const validateEmail = (value) => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      setEmailError('Email 格式不正確');
    } else {
      setEmailError('');
    }
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    validateEmail(value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (emailError) {
      alert('請修正錯誤後再送出');
      return;
    }

    const formData = {
      /** 受控欄位 */
      email,
      password,
      /** 非受控欄位 */
      name: nameRef.current.value,
      phone: phoneRef.current.value,
      address: addressRef.current.value
    };

    console.log('混合表單資料：', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>姓名：</label>
        <input
          ref={nameRef}
          type="text"
          defaultValue=""
        />
      </div>

      <div>
        <label>Email：</label>
        <input
          type="email"
          value={email}
          onChange={handleEmailChange}
          className={emailError ? 'error' : ''}
        />
        {emailError && (
          <span className="error-message">{emailError}</span>
        )}
      </div>

      <div>
        <label>密碼：</label>
        <input
          type="password"
          value={password}
          onChange={handlePasswordChange}
        />
      </div>

      <div>
        <label>電話：</label>
        <input
          ref={phoneRef}
          type="tel"
          defaultValue=""
        />
      </div>

      <div>
        <label>地址：</label>
        <textarea
          ref={addressRef}
          defaultValue=""
          rows="3"
        />
      </div>

      <button type="submit">送出</button>
    </form>
  );
}
```

### 2. 動態表單處理

```jsx
function DynamicForm() {
  const [fields, setFields] = useState([
    { id: 1, name: 'field1', label: '欄位 1', type: 'text', controlled: true, value: '' },
    { id: 2, name: 'field2', label: '欄位 2', type: 'text', controlled: false, defaultValue: '' }
  ]);

  const refs = useRef({});

  const handleControlledChange = (fieldId, value) => {
    setFields(prev => prev.map(field =>
      field.id === fieldId ? { ...field, value } : field
    ));
  };

  const addField = () => {
    const newField = {
      id: Date.now(),
      name: `field${Date.now()}`,
      label: `欄位 ${fields.length + 1}`,
      type: 'text',
      controlled: Math.random() > 0.5, // 隨機決定是否受控
      value: '',
      defaultValue: ''
    };

    setFields(prev => [...prev, newField]);
  };

  const removeField = (fieldId) => {
    setFields(prev => prev.filter(field => field.id !== fieldId));
    delete refs.current[fieldId];
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {};

    fields.forEach(field => {
      if (field.controlled) {
        formData[field.name] = field.value;
      } else {
        formData[field.name] = refs.current[field.id]?.value || '';
      }
    });

    console.log('動態表單資料：', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {fields.map(field => (
        <div key={field.id}>
          <label>{field.label}：</label>
          {field.controlled ? (
            <input
              type={field.type}
              value={field.value}
              onChange={(e) => handleControlledChange(field.id, e.target.value)}
            />
          ) : (
            <input
              ref={el => refs.current[field.id] = el}
              type={field.type}
              defaultValue={field.defaultValue}
            />
          )}
          <span>({field.controlled ? '受控' : '非受控'})</span>
          <button 
            type="button" 
            onClick={() => removeField(field.id)}
          >
            移除
          </button>
        </div>
      ))}

      <div>
        <button type="button" onClick={addField}>
          新增欄位
        </button>
        <button type="submit">送出</button>
      </div>
    </form>
  );
}
```

<br />

## 效能考量

### 1. 受控元件效能最佳化

```jsx
function OptimizedControlledForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    description: ''
  });

  /** 使用 useCallback 避免子元件重新渲染 */
  const handleFieldChange = useCallback((fieldName) => (e) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: e.target.value
    }));
  }, []);

  /** 防抖處理，避免過於頻繁的狀態更新 */
  const [debouncedDescription, setDebouncedDescription] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedDescription(formData.description);
    }, 500);

    return () => clearTimeout(timer);
  }, [formData.description]);

  return (
    <form>
      <OptimizedField
        label="姓名"
        value={formData.name}
        onChange={handleFieldChange('name')}
      />

      <OptimizedField
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleFieldChange('email')}
      />

      <div>
        <label>描述：</label>
        <textarea
          value={formData.description}
          onChange={handleFieldChange('description')}
          rows="4"
        />
        <p>字數：{debouncedDescription.length}</p>
      </div>
    </form>
  );
}

const OptimizedField = React.memo(function OptimizedField({ 
  label, 
  type = 'text', 
  value, 
  onChange 
}) {
  console.log(`OptimizedField ${label} 重新渲染`);

  return (
    <div>
      <label>{label}：</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
      />
    </div>
  );
});
```

### 2. 大型表單處理

```jsx
function LargeFormOptimization() {
  const [formData, setFormData] = useState({});
  const [changedFields, setChangedFields] = useState(new Set());

  /** 只更新變更的欄位 */
  const handleFieldChange = useCallback((fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));

    setChangedFields(prev => new Set([...prev, fieldName]));
  }, []);

  /** 批次更新多個欄位 */
  const handleBatchUpdate = useCallback((updates) => {
    setFormData(prev => ({ ...prev, ...updates }));
    setChangedFields(prev => new Set([...prev, ...Object.keys(updates)]));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    /** 只送出變更的欄位 */
    const changedData = {};
    changedFields.forEach(field => {
      changedData[field] = formData[field];
    });

    console.log('變更的欄位：', changedData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* 大量表單欄位 */}
      {Array.from({ length: 50 }, (_, i) => (
        <div key={i}>
          <label>欄位 {i + 1}：</label>
          <input
            value={formData[`field${i}`] || ''}
            onChange={(e) => handleFieldChange(`field${i}`, e.target.value)}
          />
          {changedFields.has(`field${i}`) && <span>*</span>}
        </div>
      ))}

      <button type="submit">
        送出 ({changedFields.size} 個變更)
      </button>
    </form>
  );
}
```

<br />

## 選擇指南

### 1. 使用受控元件的情況

- 需要即時驗證

- 需要格式化輸入

- 需要條件式顯示/隱藏

- 需要同步多個欄位

- 需要複雜的表單狀態管理

### 2. 使用非受控元件的情況

- 簡單的表單送出

- 檔案上傳

- 與第三方 DOM 庫整合

- 效能要求較高的大型表單

- 一次性資料收集

### 3. 混合使用策略

- 重要欄位使用受控 (例如：email、password)

- 次要欄位使用非受控 (例如：備註、地址)

- 根據使用者互動動態切換控制方式

- 效能敏感的部分使用非受控

<br />

## 最佳實務

- 選擇適當的控制方式：根據需求選擇受控或非受控

- 保持一致性：同一表單中盡量使用相同的控制方式

- 效能最佳化：大型表單考慮使用非受控或混合方式

- 錯誤處理：提供清楚的錯誤訊息和驗證回饋

- 使用者體驗：提供即時回饋和適當的預設值

- 可存取性：確保表單元素有適當的標籤和鍵盤導航
