# 5.3.4 `useId`：生成唯一 ID (React 18+，適用無障礙與表單)

## 基本概念

`useId` 是 React 18 新增的 Hook，用於生成在客戶端和伺服器端都穩定的唯一 ID。主要用於無障礙屬性和表單元素的關聯。

### 1. 基本語法

```jsx
import React, { useId } from 'react';

function BasicIdExample() {
  const id = useId();

  return (
    <div>
      <label htmlFor={id}>使用者名稱：</label>
      <input id={id} type="text" />
      <p>生成的 ID：{id}</p>
    </div>
  );
}
```

### 2. 與傳統 ID 生成方式比較

```jsx
/** ❌ 傳統方式：可能在 SSR 中不一致 */
function TraditionalIdExample() {
  const [id] = useState(() => Math.random().toString(36));

  return (
    <div>
      <label htmlFor={id}>傳統方式：</label>
      <input id={id} type="text" />
    </div>
  );
}

/** ✅ 使用 useId：SSR 安全 */
function ModernIdExample() {
  const id = useId();

  return (
    <div>
      <label htmlFor={id}>現代方式：</label>
      <input id={id} type="text" />
    </div>
  );
}
```

<br />

## 表單應用

### 1. 基本表單欄位

```jsx
function FormField({ label, type = 'text', required = false, ...props }) {
  const id = useId();

  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        {required && <span className="required">*</span>}
      </label>
      <input 
        id={id}
        type={type}
        required={required}
        {...props}
      />
    </div>
  );
}

function ContactForm() {
  return (
    <form>
      <FormField 
        label="姓名" 
        required 
        placeholder="請輸入姓名"
      />
      <FormField 
        label="Email" 
        type="email" 
        required 
        placeholder="請輸入 Email"
      />
      <FormField 
        label="電話" 
        type="tel" 
        placeholder="請輸入電話"
      />
      <button type="submit">送出</button>
    </form>
  );
}
```

### 2. 複雜表單元件

```jsx
function RadioGroup({ name, options, value, onChange, label }) {
  const groupId = useId();

  return (
    <fieldset>
      <legend>{label}</legend>
      {options.map((option, index) => {
        const optionId = `${groupId}-${index}`;

        return (
          <div key={option.value} className="radio-option">
            <input
              id={optionId}
              type="radio"
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={(e) => onChange(e.target.value)}
            />
            <label htmlFor={optionId}>
              {option.label}
            </label>
          </div>
        );
      })}
    </fieldset>
  );
}

function CheckboxGroup({ options, values, onChange, label }) {
  const groupId = useId();

  const handleChange = (optionValue, checked) => {
    if (checked) {
      onChange([...values, optionValue]);
    } else {
      onChange(values.filter(v => v !== optionValue));
    }
  };

  return (
    <fieldset>
      <legend>{label}</legend>
      {options.map((option, index) => {
        const optionId = `${groupId}-${index}`;

        return (
          <div key={option.value} className="checkbox-option">
            <input
              id={optionId}
              type="checkbox"
              value={option.value}
              checked={values.includes(option.value)}
              onChange={(e) => handleChange(option.value, e.target.checked)}
            />
            <label htmlFor={optionId}>
              {option.label}
            </label>
          </div>
        );
      })}
    </fieldset>
  );
}

function PreferencesForm() {
  const [gender, setGender] = useState('');
  const [interests, setInterests] = useState([]);

  const genderOptions = [
    { value: 'male', label: '男性' },
    { value: 'female', label: '女性' },
    { value: 'other', label: '其他' }
  ];

  const interestOptions = [
    { value: 'reading', label: '閱讀' },
    { value: 'sports', label: '運動' },
    { value: 'music', label: '音樂' },
    { value: 'travel', label: '旅遊' }
  ];

  return (
    <form>
      <RadioGroup
        name="gender"
        label="性別"
        options={genderOptions}
        value={gender}
        onChange={setGender}
      />

      <CheckboxGroup
        label="興趣"
        options={interestOptions}
        values={interests}
        onChange={setInterests}
      />

      <div>
        <p>選擇的性別：{gender}</p>
        <p>選擇的興趣：{interests.join(', ')}</p>
      </div>
    </form>
  );
}
```

### 3. 表單驗證與錯誤訊息

```jsx
function ValidatedField({ 
  label, 
  type = 'text', 
  value, 
  onChange, 
  error, 
  required = false,
  ...props 
}) {
  const fieldId = useId();
  const errorId = useId();

  return (
    <div className="validated-field">
      <label htmlFor={fieldId}>
        {label}
        {required && <span className="required">*</span>}
      </label>

      <input
        id={fieldId}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        className={error ? 'error' : ''}
        {...props}
      />

      {error && (
        <div id={errorId} className="error-message" role="alert">
          {error}
        </div>
      )}
    </div>
  );
}

function RegistrationForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});

  const handleChange = (field) => (e) => {
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

    if (!formData.username.trim()) {
      newErrors.username = '使用者名稱為必填';
    } else if (formData.username.length < 3) {
      newErrors.username = '使用者名稱至少需要 3 個字元';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email 為必填';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Email 格式不正確';
    }

    if (!formData.password) {
      newErrors.password = '密碼為必填';
    } else if (formData.password.length < 6) {
      newErrors.password = '密碼至少需要 6 個字元';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = '確認密碼不符合';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      console.log('表單驗證通過:', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <ValidatedField
        label="使用者名稱"
        value={formData.username}
        onChange={handleChange('username')}
        error={errors.username}
        required
      />

      <ValidatedField
        label="Email"
        type="email"
        value={formData.email}
        onChange={handleChange('email')}
        error={errors.email}
        required
      />

      <ValidatedField
        label="密碼"
        type="password"
        value={formData.password}
        onChange={handleChange('password')}
        error={errors.password}
        required
      />

      <ValidatedField
        label="確認密碼"
        type="password"
        value={formData.confirmPassword}
        onChange={handleChange('confirmPassword')}
        error={errors.confirmPassword}
        required
      />

      <button type="submit">註冊</button>
    </form>
  );
}
```

<br />

## 無障礙應用

### 1. ARIA 屬性關聯

```jsx
function AccessibleTooltip({ children, tooltip }) {
  const tooltipId = useId();
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="tooltip-container">
      <button
        aria-describedby={isVisible ? tooltipId : undefined}
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
      >
        {children}
      </button>

      {isVisible && (
        <div
          id={tooltipId}
          role="tooltip"
          className="tooltip"
        >
          {tooltip}
        </div>
      )}
    </div>
  );
}

function AccessibleModal({ isOpen, onClose, title, children }) {
  const titleId = useId();
  const descriptionId = useId();

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div 
      className="modal-overlay"
      onClick={onClose}
    >
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
        onClick={(e) => e.stopPropagation()}
      >
        <header className="modal-header">
          <h2 id={titleId}>{title}</h2>
          <button 
            onClick={onClose}
            aria-label="關閉對話框"
          >
            ×
          </button>
        </header>

        <div id={descriptionId} className="modal-content">
          {children}
        </div>
      </div>
    </div>
  );
}

function AccessibilityDemo() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div>
      <AccessibleTooltip tooltip="這是一個提示訊息">
        滑鼠懸停或聚焦查看提示
      </AccessibleTooltip>

      <button onClick={() => setIsModalOpen(true)}>
        開啟對話框
      </button>

      <AccessibleModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="範例對話框"
      >
        <p>這是對話框的內容。</p>
        <p>使用 useId 確保 ARIA 屬性正確關聯。</p>
      </AccessibleModal>
    </div>
  );
}
```

### 2. 複雜互動元件

```jsx
function AccessibleAccordion({ items }) {
  const [openItems, setOpenItems] = useState(new Set());

  const toggleItem = (index) => {
    setOpenItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  return (
    <div className="accordion">
      {items.map((item, index) => {
        const headerId = useId();
        const panelId = useId();
        const isOpen = openItems.has(index);

        return (
          <div key={index} className="accordion-item">
            <h3>
              <button
                id={headerId}
                className="accordion-header"
                aria-expanded={isOpen}
                aria-controls={panelId}
                onClick={() => toggleItem(index)}
              >
                {item.title}
                <span className="accordion-icon">
                  {isOpen ? '−' : '+'}
                </span>
              </button>
            </h3>

            <div
              id={panelId}
              className={`accordion-panel ${isOpen ? 'open' : 'closed'}`}
              role="region"
              aria-labelledby={headerId}
              hidden={!isOpen}
            >
              <div className="accordion-content">
                {item.content}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function TabPanel({ tabs }) {
  const [activeTab, setActiveTab] = useState(0);
  const tabListId = useId();

  return (
    <div className="tab-container">
      <div 
        role="tablist" 
        aria-labelledby={tabListId}
        className="tab-list"
      >
        <h2 id={tabListId} className="sr-only">頁籤導航</h2>
        {tabs.map((tab, index) => {
          const tabId = useId();
          const panelId = useId();

          return (
            <button
              key={index}
              id={tabId}
              role="tab"
              aria-selected={activeTab === index}
              aria-controls={panelId}
              className={`tab ${activeTab === index ? 'active' : ''}`}
              onClick={() => setActiveTab(index)}
            >
              {tab.title}
            </button>
          );
        })}
      </div>

      {tabs.map((tab, index) => {
        const tabId = `tab-${index}`;
        const panelId = useId();

        return (
          <div
            key={index}
            id={panelId}
            role="tabpanel"
            aria-labelledby={tabId}
            className={`tab-panel ${activeTab === index ? 'active' : 'hidden'}`}
            hidden={activeTab !== index}
          >
            {tab.content}
          </div>
        );
      })}
    </div>
  );
}

function InteractiveDemo() {
  const accordionItems = [
    {
      title: '什麼是 React？',
      content: 'React 是一個用於建立使用者介面的 JavaScript 函式庫。'
    },
    {
      title: '什麼是 useId？',
      content: 'useId 是 React 18 新增的 Hook，用於生成唯一 ID。'
    },
    {
      title: '為什麼需要無障礙？',
      content: '無障礙設計確保所有使用者都能使用網站功能。'
    }
  ];

  const tabData = [
    {
      title: '基本資訊',
      content: <div>這是基本資訊的內容</div>
    },
    {
      title: '進階設定',
      content: <div>這是進階設定的內容</div>
    },
    {
      title: '說明文件',
      content: <div>這是說明文件的內容</div>
    }
  ];

  return (
    <div>
      <h2>手風琴元件</h2>
      <AccessibleAccordion items={accordionItems} />

      <h2>頁籤元件</h2>
      <TabPanel tabs={tabData} />
    </div>
  );
}
```

<br />

## 進階應用

### 1. 自定義 Hook 結合 `useId`

```jsx
function useFormField(initialValue = '', validation = null) {
  const [value, setValue] = useState(initialValue);
  const [error, setError] = useState('');
  const [touched, setTouched] = useState(false);
  const id = useId();
  const errorId = useId();

  const validate = useCallback(() => {
    if (validation && touched) {
      const errorMessage = validation(value);
      setError(errorMessage || '');
      return !errorMessage;
    }
    return true;
  }, [value, touched, validation]);

  useEffect(() => {
    validate();
  }, [validate]);

  const fieldProps = {
    id,
    value,
    onChange: (e) => setValue(e.target.value),
    onBlur: () => setTouched(true),
    'aria-invalid': !!error,
    'aria-describedby': error ? errorId : undefined
  };

  const labelProps = {
    htmlFor: id
  };

  const errorProps = {
    id: errorId,
    role: 'alert'
  };

  return {
    value,
    setValue,
    error,
    touched,
    isValid: !error,
    fieldProps,
    labelProps,
    errorProps,
    validate: () => {
      setTouched(true);
      return validate();
    }
  };
}

function SmartForm() {
  const nameField = useFormField('', (value) => {
    if (!value.trim()) return '姓名為必填';
    if (value.length < 2) return '姓名至少需要 2 個字元';
    return null;
  });

  const emailField = useFormField('', (value) => {
    if (!value.trim()) return 'Email 為必填';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Email 格式不正確';
    return null;
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const isNameValid = nameField.validate();
    const isEmailValid = emailField.validate();

    if (isNameValid && isEmailValid) {
      console.log('表單資料:', {
        name: nameField.value,
        email: emailField.value
      });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-field">
        <label {...nameField.labelProps}>姓名：</label>
        <input {...nameField.fieldProps} />
        {nameField.error && (
          <div {...nameField.errorProps} className="error-message">
            {nameField.error}
          </div>
        )}
      </div>

      <div className="form-field">
        <label {...emailField.labelProps}>Email：</label>
        <input {...emailField.fieldProps} type="email" />
        {emailField.error && (
          <div {...emailField.errorProps} className="error-message">
            {emailField.error}
          </div>
        )}
      </div>

      <button type="submit">送出</button>
    </form>
  );
}
```

### 2. 動態表單生成

```jsx
function DynamicForm({ schema }) {
  const [formData, setFormData] = useState({});

  const handleFieldChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const renderField = (field) => {
    const fieldId = useId();
    const errorId = useId();
    const value = formData[field.name] || '';

    const commonProps = {
      id: fieldId,
      name: field.name,
      value,
      onChange: (e) => handleFieldChange(field.name, e.target.value),
      required: field.required
    };

    switch (field.type) {
      case 'text':
      case 'email':
      case 'tel':
        return (
          <div key={field.name} className="form-field">
            <label htmlFor={fieldId}>
              {field.label}
              {field.required && <span className="required">*</span>}
            </label>
            <input {...commonProps} type={field.type} />
          </div>
        );

      case 'textarea':
        return (
          <div key={field.name} className="form-field">
            <label htmlFor={fieldId}>
              {field.label}
              {field.required && <span className="required">*</span>}
            </label>
            <textarea {...commonProps} rows={field.rows || 4} />
          </div>
        );

      case 'select':
        return (
          <div key={field.name} className="form-field">
            <label htmlFor={fieldId}>
              {field.label}
              {field.required && <span className="required">*</span>}
            </label>
            <select {...commonProps}>
              <option value="">請選擇</option>
              {field.options.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        );

      case 'radio':
        return (
          <fieldset key={field.name} className="form-field">
            <legend>
              {field.label}
              {field.required && <span className="required">*</span>}
            </legend>
            {field.options.map((option, index) => {
              const optionId = `${fieldId}-${index}`;
              return (
                <div key={option.value} className="radio-option">
                  <input
                    id={optionId}
                    type="radio"
                    name={field.name}
                    value={option.value}
                    checked={value === option.value}
                    onChange={(e) => handleFieldChange(field.name, e.target.value)}
                  />
                  <label htmlFor={optionId}>{option.label}</label>
                </div>
              );
            })}
          </fieldset>
        );

      default:
        return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('動態表單資料:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {schema.fields.map(renderField)}
      <button type="submit">送出</button>
    </form>
  );
}

function DynamicFormDemo() {
  const formSchema = {
    fields: [
      {
        name: 'name',
        type: 'text',
        label: '姓名',
        required: true
      },
      {
        name: 'email',
        type: 'email',
        label: 'Email',
        required: true
      },
      {
        name: 'gender',
        type: 'radio',
        label: '性別',
        options: [
          { value: 'male', label: '男性' },
          { value: 'female', label: '女性' },
          { value: 'other', label: '其他' }
        ]
      },
      {
        name: 'country',
        type: 'select',
        label: '國家',
        options: [
          { value: 'tw', label: '台灣' },
          { value: 'jp', label: '日本' },
          { value: 'kr', label: '韓國' }
        ]
      },
      {
        name: 'message',
        type: 'textarea',
        label: '訊息',
        rows: 5
      }
    ]
  };

  return <DynamicForm schema={formSchema} />;
}
```

<br />

## 最佳實務

### 1. 何時使用 `useId`

- 表單標籤關聯：label 與 input 的 htmlFor/id 關聯

- ARIA 屬性：aria-describedby、aria-labelledby 等

- 無障礙元件：模態框、工具提示、手風琴等

- SSR 應用：需要客戶端與伺服器端 ID 一致性

### 2. 使用注意事項

- 不要用於 key 屬性：useId 不適合作為列表項目的 key

- 不要用於 CSS 選擇器：ID 格式可能變化

- 避免條件性使用：每次渲染都應該呼叫 `useId`

- 伺服器端渲染：確保 hydration 過程中 ID 保持一致

### 3. 與其他方案比較

- Math.random()：在 SSR 中不一致

- Date.now()：可能產生重複 ID

- 自定義計數器：在多個元件實例中可能衝突

- useId：React 保證唯一性和 SSR 安全性

### 4. 效能考量

- 輕量級：useId 的效能開銷極小

- 穩定性：同一元件實例的 ID 在重新渲染間保持穩定

- 唯一性：React 確保應用程式中所有 ID 的唯一性
