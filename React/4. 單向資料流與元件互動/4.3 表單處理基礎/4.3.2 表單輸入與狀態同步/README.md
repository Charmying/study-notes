# 4.3.2 表單輸入與狀態同步

<br />

## 基本狀態同步

### 1. 單一輸入框同步

```jsx
function SingleInputSync() {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="輸入文字"
      />
      <p>目前值：{inputValue}</p>
      <p>字元數：{inputValue.length}</p>
    </div>
  );
}
```

### 2. 多個輸入框同步

```jsx
function MultipleInputSync() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const fullName = `${formData.firstName} ${formData.lastName}`.trim();

  return (
    <div>
      <div>
        <input
          name="firstName"
          value={formData.firstName}
          onChange={handleInputChange}
          placeholder="名字"
        />
        <input
          name="lastName"
          value={formData.lastName}
          onChange={handleInputChange}
          placeholder="姓氏"
        />
      </div>

      <div>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleInputChange}
          placeholder="電子郵件"
        />
        <input
          name="phone"
          type="tel"
          value={formData.phone}
          onChange={handleInputChange}
          placeholder="電話號碼"
        />
      </div>

      <div>
        <h3>即時預覽：</h3>
        <p>全名：{fullName}</p>
        <p>Email：{formData.email}</p>
        <p>電話：{formData.phone}</p>
      </div>
    </div>
  );
}
```

<br />

## 不同輸入類型的同步

### 1. 文字輸入與格式化

```jsx
function FormattedInputSync() {
  const [formData, setFormData] = useState({
    creditCard: '',
    phone: '',
    currency: '',
    percentage: ''
  });

  const formatCreditCard = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = matches && matches[0] || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    if (parts.length) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const formatPhone = (value) => {
    const phoneNumber = value.replace(/[^\d]/g, '');
    const phoneNumberLength = phoneNumber.length;

    if (phoneNumberLength < 4) return phoneNumber;
    if (phoneNumberLength < 7) {
      return `${phoneNumber.slice(0, 3)}-${phoneNumber.slice(3)}`;
    }
    return `${phoneNumber.slice(0, 3)}-${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 10)}`;
  };

  const formatCurrency = (value) => {
    const numericValue = value.replace(/[^0-9.]/g, '');
    const number = parseFloat(numericValue);
    return isNaN(number) ? '' : number.toLocaleString();
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let formattedValue = value;

    switch (name) {
      case 'creditCard':
        formattedValue = formatCreditCard(value);
        break;
      case 'phone':
        formattedValue = formatPhone(value);
        break;
      case 'currency':
        formattedValue = formatCurrency(value);
        break;
      case 'percentage':
        const numValue = parseFloat(value);
        formattedValue = isNaN(numValue) ? '' : Math.min(100, Math.max(0, numValue)).toString();
        break;
    }

    setFormData(prev => ({
      ...prev,
      [name]: formattedValue
    }));
  };

  return (
    <div>
      <div>
        <label>信用卡號碼：</label>
        <input
          name="creditCard"
          value={formData.creditCard}
          onChange={handleInputChange}
          placeholder="1234 5678 9012 3456"
          maxLength="19"
        />
      </div>

      <div>
        <label>電話號碼：</label>
        <input
          name="phone"
          value={formData.phone}
          onChange={handleInputChange}
          placeholder="123-456-7890"
          maxLength="12"
        />
      </div>

      <div>
        <label>金額：</label>
        <input
          name="currency"
          value={formData.currency}
          onChange={handleInputChange}
          placeholder="1,000"
        />
      </div>

      <div>
        <label>百分比：</label>
        <input
          name="percentage"
          type="number"
          value={formData.percentage}
          onChange={handleInputChange}
          min="0"
          max="100"
          placeholder="0-100"
        />
        %
      </div>
    </div>
  );
}
```

### 2. 選擇類型輸入同步

```jsx
function SelectInputSync() {
  const [formData, setFormData] = useState({
    country: '',
    city: '',
    category: '',
    subcategory: '',
    skills: [],
    preferences: {
      newsletter: false,
      notifications: true,
      darkMode: false
    }
  });

  const countryData = {
    taiwan: ['台北', '台中', '台南', '高雄'],
    japan: ['東京', '大阪', '京都', '名古屋'],
    korea: ['首爾', '釜山', '大邱', '仁川']
  };

  const categoryData = {
    technology: ['前端開發', '後端開發', '資料科學', '人工智慧'],
    design: ['UI設計', 'UX設計', '平面設計', '產品設計'],
    business: ['行銷', '業務', '專案管理', '營運']
  };

  const handleSelectChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
      // 清除相依欄位
      ...(name === 'country' && { city: '' }),
      ...(name === 'category' && { subcategory: '' })
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, value, checked } = e.target;

    if (name === 'skills') {
      setFormData(prev => ({
        ...prev,
        skills: checked
          ? [...prev.skills, value]
          : prev.skills.filter(skill => skill !== value)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        preferences: {
          ...prev.preferences,
          [name]: checked
        }
      }));
    }
  };

  return (
    <div>
      <div>
        <label>國家：</label>
        <select name="country" value={formData.country} onChange={handleSelectChange}>
          <option value="">請選擇國家</option>
          <option value="taiwan">台灣</option>
          <option value="japan">日本</option>
          <option value="korea">韓國</option>
        </select>
      </div>

      <div>
        <label>城市：</label>
        <select 
          name="city" 
          value={formData.city} 
          onChange={handleSelectChange}
          disabled={!formData.country}
        >
          <option value="">請選擇城市</option>
          {formData.country && countryData[formData.country].map(city => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>
      </div>

      <div>
        <label>主要分類：</label>
        <select name="category" value={formData.category} onChange={handleSelectChange}>
          <option value="">請選擇分類</option>
          <option value="technology">科技</option>
          <option value="design">設計</option>
          <option value="business">商業</option>
        </select>
      </div>

      <div>
        <label>子分類：</label>
        <select 
          name="subcategory" 
          value={formData.subcategory} 
          onChange={handleSelectChange}
          disabled={!formData.category}
        >
          <option value="">請選擇子分類</option>
          {formData.category && categoryData[formData.category].map(sub => (
            <option key={sub} value={sub}>{sub}</option>
          ))}
        </select>
      </div>

      <div>
        <label>技能：</label>
        {['JavaScript', 'React', 'Node.js', 'Python', 'Design'].map(skill => (
          <label key={skill}>
            <input
              type="checkbox"
              name="skills"
              value={skill}
              checked={formData.skills.includes(skill)}
              onChange={handleCheckboxChange}
            />
            {skill}
          </label>
        ))}
      </div>

      <div>
        <label>偏好設定：</label>
        <label>
          <input
            type="checkbox"
            name="newsletter"
            checked={formData.preferences.newsletter}
            onChange={handleCheckboxChange}
          />
          訂閱電子報
        </label>
        <label>
          <input
            type="checkbox"
            name="notifications"
            checked={formData.preferences.notifications}
            onChange={handleCheckboxChange}
          />
          接收通知
        </label>
        <label>
          <input
            type="checkbox"
            name="darkMode"
            checked={formData.preferences.darkMode}
            onChange={handleCheckboxChange}
          />
          深色模式
        </label>
      </div>

      <div>
        <h3>選擇結果：</h3>
        <p>地點：{formData.country && formData.city ? `${formData.city}, ${formData.country}` : '未選擇'}</p>
        <p>分類：{formData.subcategory || formData.category || '未選擇'}</p>
        <p>技能：{formData.skills.join(', ') || '未選擇'}</p>
        <p>偏好：{Object.entries(formData.preferences)
          .filter(([key, value]) => value)
          .map(([key]) => key)
          .join(', ') || '無'}</p>
      </div>
    </div>
  );
}
```

<br />

## 即時驗證與狀態同步

### 1. 即時驗證回饋

```jsx
function RealTimeValidation() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [validation, setValidation] = useState({
    username: { isValid: false, message: '' },
    email: { isValid: false, message: '' },
    password: { isValid: false, message: '' },
    confirmPassword: { isValid: false, message: '' }
  });

  const validateField = (name, value, allData = formData) => {
    switch (name) {
      case 'username':
        if (value.length < 3) {
          return { isValid: false, message: '使用者名稱至少需要 3 個字元' };
        }
        if (!/^[a-zA-Z0-9_]+$/.test(value)) {
          return { isValid: false, message: '只能包含字母、數字和底線' };
        }
        return { isValid: true, message: '使用者名稱可用' };

      case 'email':
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return { isValid: false, message: 'Email 格式不正確' };
        }
        return { isValid: true, message: 'Email 格式正確' };

      case 'password':
        if (value.length < 8) {
          return { isValid: false, message: '密碼至少需要 8 個字元' };
        }
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          return { isValid: false, message: '密碼需包含大小寫字母和數字' };
        }
        return { isValid: true, message: '密碼強度良好' };

      case 'confirmPassword':
        if (value !== allData.password) {
          return { isValid: false, message: '確認密碼不符合' };
        }
        return { isValid: true, message: '密碼確認正確' };

      default:
        return { isValid: true, message: '' };
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    const newFormData = {
      ...formData,
      [name]: value
    };

    setFormData(newFormData);

    /** 即時驗證當前欄位 */
    const fieldValidation = validateField(name, value, newFormData);

    setValidation(prev => ({
      ...prev,
      [name]: fieldValidation,
      // 如果是密碼變更，也要重新驗證確認密碼
      ...(name === 'password' && {
        confirmPassword: validateField('confirmPassword', newFormData.confirmPassword, newFormData)
      })
    }));
  };

  const isFormValid = Object.values(validation).every(field => field.isValid);

  return (
    <div>
      <div>
        <label>使用者名稱：</label>
        <input
          name="username"
          value={formData.username}
          onChange={handleInputChange}
          className={validation.username.isValid ? 'valid' : 'invalid'}
        />
        <span className={validation.username.isValid ? 'success' : 'error'}>
          {validation.username.message}
        </span>
      </div>

      <div>
        <label>Email：</label>
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleInputChange}
          className={validation.email.isValid ? 'valid' : 'invalid'}
        />
        <span className={validation.email.isValid ? 'success' : 'error'}>
          {validation.email.message}
        </span>
      </div>

      <div>
        <label>密碼：</label>
        <input
          name="password"
          type="password"
          value={formData.password}
          onChange={handleInputChange}
          className={validation.password.isValid ? 'valid' : 'invalid'}
        />
        <span className={validation.password.isValid ? 'success' : 'error'}>
          {validation.password.message}
        </span>
      </div>

      <div>
        <label>確認密碼：</label>
        <input
          name="confirmPassword"
          type="password"
          value={formData.confirmPassword}
          onChange={handleInputChange}
          className={validation.confirmPassword.isValid ? 'valid' : 'invalid'}
        />
        <span className={validation.confirmPassword.isValid ? 'success' : 'error'}>
          {validation.confirmPassword.message}
        </span>
      </div>

      <div>
        <button disabled={!isFormValid}>
          註冊 {isFormValid ? '✓' : '✗'}
        </button>
      </div>

      <div>
        <h4>表單狀態：</h4>
        <p>整體有效性：{isFormValid ? '有效' : '無效'}</p>
        <p>已填寫欄位：{Object.values(formData).filter(v => v).length}/4</p>
      </div>
    </div>
  );
}
```

### 2. 防抖驗證

```jsx
function DebouncedValidation() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [validationStatus, setValidationStatus] = useState({
    username: { checking: false, available: null, message: '' },
    email: { checking: false, valid: null, message: '' }
  });

  /** 模擬 API 檢查使用者名稱是否可用 */
  const checkUsernameAvailability = async (username) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const unavailableUsernames = ['admin', 'user', 'test', 'demo'];
    return !unavailableUsernames.includes(username.toLowerCase());
  };

  /** 模擬 API 檢查 Email 是否已註冊 */
  const checkEmailExists = async (email) => {
    await new Promise(resolve => setTimeout(resolve, 800));
    const existingEmails = ['test@example.com', 'admin@example.com'];
    return !existingEmails.includes(email.toLowerCase());
  };

  /** 防抖 Hook */
  const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
      const handler = setTimeout(() => {
        setDebouncedValue(value);
      }, delay);

      return () => {
        clearTimeout(handler);
      };
    }, [value, delay]);

    return debouncedValue;
  };

  const debouncedUsername = useDebounce(username, 500);
  const debouncedEmail = useDebounce(email, 500);

  /** 使用者名稱驗證 */
  useEffect(() => {
    if (debouncedUsername && debouncedUsername.length >= 3) {
      setValidationStatus(prev => ({
        ...prev,
        username: { checking: true, available: null, message: '檢查中...' }
      }));

      checkUsernameAvailability(debouncedUsername).then(available => {
        setValidationStatus(prev => ({
          ...prev,
          username: {
            checking: false,
            available,
            message: available ? '使用者名稱可用' : '使用者名稱已被使用'
          }
        }));
      });
    } else if (debouncedUsername) {
      setValidationStatus(prev => ({
        ...prev,
        username: { checking: false, available: false, message: '使用者名稱至少需要 3 個字元' }
      }));
    }
  }, [debouncedUsername]);

  /** Email 驗證 */
  useEffect(() => {
    if (debouncedEmail && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(debouncedEmail)) {
      setValidationStatus(prev => ({
        ...prev,
        email: { checking: true, valid: null, message: '檢查中...' }
      }));

      checkEmailExists(debouncedEmail).then(available => {
        setValidationStatus(prev => ({
          ...prev,
          email: {
            checking: false,
            valid: available,
            message: available ? 'Email 可用' : 'Email 已被註冊'
          }
        }));
      });
    } else if (debouncedEmail) {
      setValidationStatus(prev => ({
        ...prev,
        email: { checking: false, valid: false, message: 'Email 格式不正確' }
      }));
    }
  }, [debouncedEmail]);

  return (
    <div>
      <div>
        <label>使用者名稱：</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="輸入使用者名稱"
        />
        <span className={
          validationStatus.username.checking ? 'checking' :
          validationStatus.username.available === true ? 'success' :
          validationStatus.username.available === false ? 'error' : ''
        }>
          {validationStatus.username.checking && '⏳ '}
          {validationStatus.username.available === true && '✓ '}
          {validationStatus.username.available === false && '✗ '}
          {validationStatus.username.message}
        </span>
      </div>

      <div>
        <label>Email：</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="輸入 Email"
        />
        <span className={
          validationStatus.email.checking ? 'checking' :
          validationStatus.email.valid === true ? 'success' :
          validationStatus.email.valid === false ? 'error' : ''
        }>
          {validationStatus.email.checking && '⏳ '}
          {validationStatus.email.valid === true && '✓ '}
          {validationStatus.email.valid === false && '✗ '}
          {validationStatus.email.message}
        </span>
      </div>

      <div>
        <p>輸入狀態：</p>
        <p>使用者名稱：{username} (防抖後：{debouncedUsername})</p>
        <p>Email：{email} (防抖後：{debouncedEmail})</p>
      </div>
    </div>
  );
}
```

<br />

## 複雜狀態同步

### 1. 巢狀物件狀態同步

```jsx
function NestedObjectSync() {
  const [userProfile, setUserProfile] = useState({
    personal: {
      firstName: '',
      lastName: '',
      birthDate: '',
      gender: ''
    },
    contact: {
      email: '',
      phone: '',
      address: {
        street: '',
        city: '',
        zipCode: '',
        country: ''
      }
    },
    preferences: {
      language: 'zh-TW',
      timezone: 'Asia/Taipei',
      notifications: {
        email: true,
        sms: false,
        push: true
      }
    }
  });

  /** 深層更新函式 */
  const updateNestedState = (path, value) => {
    setUserProfile(prev => {
      const newState = { ...prev };
      const keys = path.split('.');
      let current = newState;

      /** 建立深層複製路徑 */
      for (let i = 0; i < keys.length - 1; i++) {
        current[keys[i]] = { ...current[keys[i]] };
        current = current[keys[i]];
      }

      /** 設定最終值 */
      current[keys[keys.length - 1]] = value;
      return newState;
    });
  };

  const handleInputChange = (path) => (e) => {
    const { type, checked, value } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    updateNestedState(path, newValue);
  };

  return (
    <div>
      <section>
        <h3>個人資訊</h3>
        <input
          placeholder="名字"
          value={userProfile.personal.firstName}
          onChange={handleInputChange('personal.firstName')}
        />
        <input
          placeholder="姓氏"
          value={userProfile.personal.lastName}
          onChange={handleInputChange('personal.lastName')}
        />
        <input
          type="date"
          value={userProfile.personal.birthDate}
          onChange={handleInputChange('personal.birthDate')}
        />
        <select
          value={userProfile.personal.gender}
          onChange={handleInputChange('personal.gender')}
        >
          <option value="">選擇性別</option>
          <option value="male">男性</option>
          <option value="female">女性</option>
          <option value="other">其他</option>
        </select>
      </section>

      <section>
        <h3>聯絡資訊</h3>
        <input
          type="email"
          placeholder="Email"
          value={userProfile.contact.email}
          onChange={handleInputChange('contact.email')}
        />
        <input
          type="tel"
          placeholder="電話"
          value={userProfile.contact.phone}
          onChange={handleInputChange('contact.phone')}
        />

        <h4>地址</h4>
        <input
          placeholder="街道地址"
          value={userProfile.contact.address.street}
          onChange={handleInputChange('contact.address.street')}
        />
        <input
          placeholder="城市"
          value={userProfile.contact.address.city}
          onChange={handleInputChange('contact.address.city')}
        />
        <input
          placeholder="郵遞區號"
          value={userProfile.contact.address.zipCode}
          onChange={handleInputChange('contact.address.zipCode')}
        />
        <input
          placeholder="國家"
          value={userProfile.contact.address.country}
          onChange={handleInputChange('contact.address.country')}
        />
      </section>

      <section>
        <h3>偏好設定</h3>
        <select
          value={userProfile.preferences.language}
          onChange={handleInputChange('preferences.language')}
        >
          <option value="zh-TW">繁體中文</option>
          <option value="en-US">English</option>
          <option value="ja-JP">日本語</option>
        </select>

        <select
          value={userProfile.preferences.timezone}
          onChange={handleInputChange('preferences.timezone')}
        >
          <option value="Asia/Taipei">台北時間</option>
          <option value="America/New_York">紐約時間</option>
          <option value="Europe/London">倫敦時間</option>
        </select>

        <h4>通知設定</h4>
        <label>
          <input
            type="checkbox"
            checked={userProfile.preferences.notifications.email}
            onChange={handleInputChange('preferences.notifications.email')}
          />
          Email 通知
        </label>
        <label>
          <input
            type="checkbox"
            checked={userProfile.preferences.notifications.sms}
            onChange={handleInputChange('preferences.notifications.sms')}
          />
          簡訊通知
        </label>
        <label>
          <input
            type="checkbox"
            checked={userProfile.preferences.notifications.push}
            onChange={handleInputChange('preferences.notifications.push')}
          />
          推播通知
        </label>
      </section>

      <section>
        <h3>資料預覽</h3>
        <pre>{JSON.stringify(userProfile, null, 2)}</pre>
      </section>
    </div>
  );
}
```

### 2. 陣列狀態同步

```jsx
function ArrayStateSync() {
  const [todoList, setTodoList] = useState([
    { id: 1, text: '學習 React', completed: false, priority: 'high' },
    { id: 2, text: '完成專案', completed: true, priority: 'medium' }
  ]);

  const [newTodo, setNewTodo] = useState({ text: '', priority: 'medium' });

  const addTodo = () => {
    if (newTodo.text.trim()) {
      setTodoList(prev => [...prev, {
        id: Date.now(),
        text: newTodo.text,
        completed: false,
        priority: newTodo.priority
      }]);
      setNewTodo({ text: '', priority: 'medium' });
    }
  };

  const updateTodo = (id, updates) => {
    setTodoList(prev => prev.map(todo =>
      todo.id === id ? { ...todo, ...updates } : todo
    ));
  };

  const deleteTodo = (id) => {
    setTodoList(prev => prev.filter(todo => todo.id !== id));
  };

  const moveTodo = (id, direction) => {
    setTodoList(prev => {
      const index = prev.findIndex(todo => todo.id === id);
      if (index === -1) return prev;

      const newIndex = direction === 'up' ? index - 1 : index + 1;
      if (newIndex < 0 || newIndex >= prev.length) return prev;

      const newList = [...prev];
      [newList[index], newList[newIndex]] = [newList[newIndex], newList[index]];
      return newList;
    });
  };

  const completedCount = todoList.filter(todo => todo.completed).length;
  const totalCount = todoList.length;

  return (
    <div>
      <div>
        <h3>新增待辦事項</h3>
        <input
          value={newTodo.text}
          onChange={(e) => setNewTodo(prev => ({ ...prev, text: e.target.value }))}
          placeholder="輸入待辦事項"
          onKeyPress={(e) => e.key === 'Enter' && addTodo()}
        />
        <select
          value={newTodo.priority}
          onChange={(e) => setNewTodo(prev => ({ ...prev, priority: e.target.value }))}
        >
          <option value="low">低優先度</option>
          <option value="medium">中優先度</option>
          <option value="high">高優先度</option>
        </select>
        <button onClick={addTodo}>新增</button>
      </div>

      <div>
        <h3>待辦清單 ({completedCount}/{totalCount})</h3>
        {todoList.map((todo, index) => (
          <div key={todo.id} className={`todo-item priority-${todo.priority}`}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={(e) => updateTodo(todo.id, { completed: e.target.checked })}
            />

            <input
              value={todo.text}
              onChange={(e) => updateTodo(todo.id, { text: e.target.value })}
              className={todo.completed ? 'completed' : ''}
            />

            <select
              value={todo.priority}
              onChange={(e) => updateTodo(todo.id, { priority: e.target.value })}
            >
              <option value="low">低</option>
              <option value="medium">中</option>
              <option value="high">高</option>
            </select>

            <button 
              onClick={() => moveTodo(todo.id, 'up')}
              disabled={index === 0}
            >
              ↑
            </button>
            <button 
              onClick={() => moveTodo(todo.id, 'down')}
              disabled={index === todoList.length - 1}
            >
              ↓
            </button>
            <button onClick={() => deleteTodo(todo.id)}>刪除</button>
          </div>
        ))}
      </div>

      <div>
        <h4>統計資訊</h4>
        <p>總計：{totalCount} 項</p>
        <p>已完成：{completedCount} 項</p>
        <p>進度：{totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0}%</p>
        <p>各優先度分布：</p>
        <ul>
          <li>高：{todoList.filter(t => t.priority === 'high').length} 項</li>
          <li>中：{todoList.filter(t => t.priority === 'medium').length} 項</li>
          <li>低：{todoList.filter(t => t.priority === 'low').length} 項</li>
        </ul>
      </div>
    </div>
  );
}
```

<br />

## 效能最佳化

### 1. 減少不必要的重新渲染

```jsx
function OptimizedFormSync() {
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

  /** 分離頻繁變更的欄位 */
  const [description, setDescription] = useState('');
  const [debouncedDescription, setDebouncedDescription] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedDescription(description);
    }, 300);

    return () => clearTimeout(timer);
  }, [description]);

  return (
    <div>
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
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="4"
        />
        <p>字數：{debouncedDescription.length}</p>
      </div>

      <div>
        <h4>表單資料：</h4>
        <p>姓名：{formData.name}</p>
        <p>Email：{formData.email}</p>
        <p>描述：{debouncedDescription}</p>
      </div>
    </div>
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

### 2. 批次狀態更新

```jsx
function BatchedUpdates() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: ''
  });

  const [updateQueue, setUpdateQueue] = useState([]);

  /** 批次更新機制 */
  useEffect(() => {
    if (updateQueue.length > 0) {
      const timer = setTimeout(() => {
        setFormData(prev => {
          const newData = { ...prev };
          updateQueue.forEach(({ field, value }) => {
            newData[field] = value;
          });
          return newData;
        });
        setUpdateQueue([]);
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [updateQueue]);

  const queueUpdate = (field, value) => {
    setUpdateQueue(prev => [
      ...prev.filter(update => update.field !== field),
      { field, value }
    ]);
  };

  const handleBulkImport = () => {
    const importData = {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      phone: '123-456-7890'
    };

    /** 批次更新所有欄位 */
    setFormData(importData);
  };

  const handleReset = () => {
    setFormData({
      firstName: '',
      lastName: '',
      email: '',
      phone: ''
    });
    setUpdateQueue([]);
  };

  return (
    <div>
      <div>
        <input
          placeholder="名字"
          value={formData.firstName}
          onChange={(e) => queueUpdate('firstName', e.target.value)}
        />
        <input
          placeholder="姓氏"
          value={formData.lastName}
          onChange={(e) => queueUpdate('lastName', e.target.value)}
        />
        <input
          placeholder="Email"
          value={formData.email}
          onChange={(e) => queueUpdate('email', e.target.value)}
        />
        <input
          placeholder="電話"
          value={formData.phone}
          onChange={(e) => queueUpdate('phone', e.target.value)}
        />
      </div>

      <div>
        <button onClick={handleBulkImport}>匯入範例資料</button>
        <button onClick={handleReset}>重設</button>
      </div>

      <div>
        <h4>目前資料：</h4>
        <pre>{JSON.stringify(formData, null, 2)}</pre>
        <p>待更新佇列：{updateQueue.length} 項</p>
      </div>
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 狀態結構設計

- 扁平化結構：避免過深的巢狀物件

- 正規化資料：複雜資料使用 ID 參照

- 分離關注點：將不相關的狀態分開管理

- 最小化狀態：只儲存必要的狀態，其他透過計算得出

### 2. 效能最佳化

- 使用 `useCallback`：避免不必要的重新渲染

- 防抖處理：減少頻繁的狀態更新

- 批次更新：合併多個狀態變更

- 記憶化計算：使用 `useMemo` 快取計算結果

### 3. 使用者體驗

- 即時回饋：提供即時的驗證和狀態回饋

- 錯誤處理：清楚的錯誤訊息和恢復機制

- 載入狀態：顯示處理中的狀態

- 自動儲存：定期儲存使用者輸入

### 4. 程式碼組織

- 單一職責：每個函式只處理一種類型的更新

- 可重用性：建立通用的狀態更新函式

- 型別安全：使用 TypeScript 確保型別正確性

- 測試友善：設計易於測試的狀態更新流程
