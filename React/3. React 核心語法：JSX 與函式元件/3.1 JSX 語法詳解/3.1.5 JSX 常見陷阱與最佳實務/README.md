# 3.1.5 JSX 常見陷阱與最佳實務 (Fragments、避免過多嵌套)

<br />

## React Fragments

### 1. 問題：不必要的包裝元素

```jsx
/** ❌ 產生多餘的 div 包裝 */
function UserInfo({ user }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

/** 渲染結果會產生額外的 div */
<div>
  <div>
    <h2>Charmy</h2>
    <p>charmy@example.com</p>
  </div>
</div>
```

### 2. 解決方案：使用 React.Fragment

```jsx
/** ✅ 使用 React.Fragment */
function UserInfo({ user }) {
  return (
    <React.Fragment>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </React.Fragment>
  );
}

/** ✅ 使用簡短語法 */
function UserInfo({ user }) {
  return (
    <>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </>
  );
}
```

### 3. Fragment 與 key 屬性

```jsx
function ItemList({ items }) {
  return (
    <div>
      {items.map(item => (
        <React.Fragment key={item.id}>
          <h3>{item.title}</h3>
          <p>{item.description}</p>
          <hr />
        </React.Fragment>
      ))}
    </div>
  );
}
```

<br />

## 常見陷阱與解決方案

### 1. 短路運算的數字陷阱

```jsx
/** ❌ 當 count 為 0 時會顯示 0 */
function BadCounter({ count }) {
  return (
    <div>
      {count && <p>數量：{count}</p>}
    </div>
  );
}

/** ✅ 明確的布林檢查 */
function GoodCounter({ count }) {
  return (
    <div>
      {count > 0 && <p>數量：{count}</p>}
      {Boolean(count) && <p>數量：{count}</p>}
      {!!count && <p>數量：{count}</p>}
    </div>
  );
}
```

### 2. 物件直接渲染錯誤

```jsx
/** ❌ 不能直接渲染物件 */
function BadExample({ user }) {
  return <div>{user}</div>; // 錯誤！
}

/** ✅ 渲染物件屬性 */
function GoodExample({ user }) {
  return (
    <div>
      <p>姓名：{user.name}</p>
      <p>年齡：{user.age}</p>
    </div>
  );
}

/** ✅ 序列化物件用於除錯 */
function DebugExample({ user }) {
  return <pre>{JSON.stringify(user, null, 2)}</pre>;
}
```

### 3. 事件處理函式的陷阱

```jsx
/** ❌ 每次渲染都建立新函式 */
function BadExample({ items, onUpdate }) {
  return (
    <div>
      {items.map(item => (
        <button 
          key={item.id}
          onClick={() => onUpdate(item.id)} // 每次都是新函式
        >
          {item.name}
        </button>
      ))}
    </div>
  );
}

/** ✅ 使用 useCallback 最佳化 */
function GoodExample({ items, onUpdate }) {
  const handleClick = useCallback((id) => {
    onUpdate(id);
  }, [onUpdate]);

  return (
    <div>
      {items.map(item => (
        <button 
          key={item.id}
          onClick={() => handleClick(item.id)}
        >
          {item.name}
        </button>
      ))}
    </div>
  );
}
```

### 4. 條件渲染中的 undefined 問題

```jsx
/** ❌ 可能渲染 undefined */
function BadExample({ user }) {
  return (
    <div>
      <p>{user && user.profile && user.profile.bio}</p>
    </div>
  );
}

/** ✅ 使用可選鏈與預設值 */
function GoodExample({ user }) {
  return (
    <div>
      <p>{user?.profile?.bio || '沒有個人簡介'}</p>
    </div>
  );
}
```

<br />

## 避免過多嵌套

### 1. 提取子元件

```jsx
/** ❌ 過度嵌套的元件 */
function BadDashboard({ user, notifications, tasks }) {
  return (
    <div className="dashboard">
      <header>
        <div className="user-info">
          <img src={user.avatar} alt="頭像" />
          <div className="user-details">
            <h1>{user.name}</h1>
            <p>{user.email}</p>
            <div className="user-stats">
              <span>任務：{tasks.length}</span>
              <span>通知：{notifications.length}</span>
            </div>
          </div>
        </div>
      </header>
      <main>
        <section className="notifications">
          <h2>通知</h2>
          {notifications.map(notification => (
            <div key={notification.id} className="notification">
              <div className="notification-header">
                <span className="type">{notification.type}</span>
                <span className="time">{notification.time}</span>
              </div>
              <div className="notification-body">
                <p>{notification.message}</p>
              </div>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
```

```jsx
/** ✅ 拆分為多個子元件 */
function UserInfo({ user, taskCount, notificationCount }) {
  return (
    <div className="user-info">
      <img src={user.avatar} alt="頭像" />
      <div className="user-details">
        <h1>{user.name}</h1>
        <p>{user.email}</p>
        <UserStats taskCount={taskCount} notificationCount={notificationCount} />
      </div>
    </div>
  );
}

function UserStats({ taskCount, notificationCount }) {
  return (
    <div className="user-stats">
      <span>任務：{taskCount}</span>
      <span>通知：{notificationCount}</span>
    </div>
  );
}

function NotificationItem({ notification }) {
  return (
    <div className="notification">
      <div className="notification-header">
        <span className="type">{notification.type}</span>
        <span className="time">{notification.time}</span>
      </div>
      <div className="notification-body">
        <p>{notification.message}</p>
      </div>
    </div>
  );
}

function GoodDashboard({ user, notifications, tasks }) {
  return (
    <div className="dashboard">
      <header>
        <UserInfo 
          user={user} 
          taskCount={tasks.length}
          notificationCount={notifications.length}
        />
      </header>
      <main>
        <section className="notifications">
          <h2>通知</h2>
          {notifications.map(notification => (
            <NotificationItem key={notification.id} notification={notification} />
          ))}
        </section>
      </main>
    </div>
  );
}
```

### 2. 使用自定義 Hook 簡化

```jsx
/** ✅ 提取業務流程到自定義 Hook */
function useUserDashboard(userId) {
  const [user, setUser] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    /** 載入資料 */
    loadUserData(userId).then(data => {
      setUser(data.user);
      setNotifications(data.notifications);
      setTasks(data.tasks);
      setLoading(false);
    });
  }, [userId]);

  return { user, notifications, tasks, loading };
}

function Dashboard({ userId }) {
  const { user, notifications, tasks, loading } = useUserDashboard(userId);

  if (loading) return <div>載入中...</div>;

  return (
    <div className="dashboard">
      <UserInfo user={user} taskCount={tasks.length} notificationCount={notifications.length} />
      <NotificationList notifications={notifications} />
      <TaskList tasks={tasks} />
    </div>
  );
}
```

<br />

## 效能最佳實務

### 1. 避免在 render 中建立物件

```jsx
/** ❌ 每次渲染都建立新物件 */
function BadExample({ title, content }) {
  return (
    <div style={{ padding: '10px', margin: '5px' }}>
      <h1 style={{ color: 'blue', fontSize: '24px' }}>{title}</h1>
      <p>{content}</p>
    </div>
  );
}

/** ✅ 將樣式提取到外部 */
const containerStyle = { padding: '10px', margin: '5px' };
const titleStyle = { color: 'blue', fontSize: '24px' };

function GoodExample({ title, content }) {
  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>{title}</h1>
      <p>{content}</p>
    </div>
  );
}
```

### 2. 使用 CSS 類別而非內聯樣式

```jsx
/** ✅ 使用 CSS 類別 */
function StyledComponent({ title, content, isHighlighted }) {
  return (
    <div className={`container ${isHighlighted ? 'highlighted' : ''}`}>
      <h1 className="title">{title}</h1>
      <p className="content">{content}</p>
    </div>
  );
}
```

### 3. 條件類別名稱的處理

```jsx
/** ✅ 使用 clsx 或類似工具 */
import clsx from 'clsx';

function Button({ children, variant, size, disabled }) {
  return (
    <button 
      className={clsx(
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        { 'btn-disabled': disabled }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

<br />

## 可讀性最佳實務

### 1. 適當的換行與縮排

```jsx
/** ✅ 清晰的格式化 */
function WellFormattedComponent({ user, onEdit, onDelete }) {
  return (
    <div className="user-card">
      <div className="user-header">
        <img 
          src={user.avatar} 
          alt={`${user.name}的頭像`}
          className="avatar"
        />
        <div className="user-info">
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      </div>

      <div className="user-actions">
        <button 
          onClick={() => onEdit(user.id)}
          className="btn btn-primary"
        >
          編輯
        </button>
        <button 
          onClick={() => onDelete(user.id)}
          className="btn btn-danger"
        >
          刪除
        </button>
      </div>
    </div>
  );
}
```

### 2. 提取複雜的 JSX 到變數

```jsx
function ComplexComponent({ items, filters, sorting }) {
  /** 提取複雜的過濾與排序 */
  const filteredAndSortedItems = useMemo(() => {
    return items
      .filter(item => filters.category ? item.category === filters.category : true)
      .filter(item => filters.search ? item.name.includes(filters.search) : true)
      .sort((a, b) => {
        if (sorting.field === 'name') return a.name.localeCompare(b.name);
        if (sorting.field === 'price') return a.price - b.price;
        return 0;
      });
  }, [items, filters, sorting]);

  /** 提取複雜的 JSX 結構 */
  const emptyState = (
    <div className="empty-state">
      <h3>沒有找到項目</h3>
      <p>請調整篩選條件或新增項目</p>
    </div>
  );

  return (
    <div className="item-list">
      {filteredAndSortedItems.length > 0 ? (
        filteredAndSortedItems.map(item => (
          <ItemCard key={item.id} item={item} />
        ))
      ) : (
        emptyState
      )}
    </div>
  );
}
```

<br />

## 除錯技巧

### 1. 使用 React Developer Tools

```jsx
/** 為元件添加 displayName 便於除錯 */
const UserCard = ({ user }) => {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
    </div>
  );
};

UserCard.displayName = 'UserCard';
```

### 2. 條件渲染的除錯

```jsx
function DebugComponent({ condition, data }) {
  /** 在開發環境中顯示除錯資訊 */
  if (process.env.NODE_ENV === 'development') {
    console.log('Condition:', condition, 'Data:', data);
  }

  return (
    <div>
      {condition ? (
        <div>條件為真</div>
      ) : (
        <div>條件為假</div>
      )}
    </div>
  );
}
```

<br />

## 最佳實務總結

- 使用 Fragments 避免不必要的包裝元素

- 注意短路運算中的 falsy 值

- 不要直接渲染物件

- 提取複雜元件為子元件

- 避免在 render 中建立新物件

- 使用 CSS 類別而非內聯樣式

- 保持 JSX 結構清晰易讀

- 適當使用 `useMemo` 和 `useCallback` 最佳化效能

- 為元件添加 `displayName` 便於除錯

- 遵循一致的程式碼格式化規範
