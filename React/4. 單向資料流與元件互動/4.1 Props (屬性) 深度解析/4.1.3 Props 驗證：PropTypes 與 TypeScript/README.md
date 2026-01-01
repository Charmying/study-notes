# 4.1.3 Props 驗證：PropTypes 與 TypeScript

<br />

## PropTypes 基礎

### 1. 安裝與設定

```bash
npm install prop-types
```

```jsx
import PropTypes from 'prop-types';

function Button({ children, variant, size, disabled, onClick }) {
  return (
    <button 
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'outline']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  disabled: PropTypes.bool,
  onClick: PropTypes.func
};

Button.defaultProps = {
  variant: 'primary',
  size: 'medium',
  disabled: false,
  onClick: () => {}
};
```

### 2. 基本型別驗證

```jsx
import PropTypes from 'prop-types';

function UserProfile({ 
  name, 
  age, 
  email, 
  isActive, 
  tags, 
  profile, 
  onUpdate 
}) {
  return (
    <div className="user-profile">
      <h2>{name}</h2>
      <p>年齡：{age}</p>
      <p>Email：{email}</p>
      <p>狀態：{isActive ? '啟用' : '停用'}</p>
      <div>
        標籤：{tags.join(', ')}
      </div>
      <p>簡介：{profile.bio}</p>
      <button onClick={() => onUpdate(profile.id)}>
        更新資料
      </button>
    </div>
  );
}

UserProfile.propTypes = {
  name: PropTypes.string.isRequired, // 必填字串
  age: PropTypes.number.isRequired,  // 必填數字
  email: PropTypes.string,           // 選填字串
  isActive: PropTypes.bool,          // 布林值
  tags: PropTypes.array,             // 陣列
  profile: PropTypes.object,         // 物件
  onUpdate: PropTypes.func           // 函式
};
```

### 3. 進階型別驗證

```jsx
function ProductCard({ 
  product, 
  categories, 
  onAddToCart, 
  renderActions 
}) {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>
      <div>
        分類：
        {categories.map(category => (
          <span key={category.id}>{category.name}</span>
        ))}
      </div>
      {renderActions && renderActions(product)}
      <button onClick={() => onAddToCart(product.id)}>
        加入購物車
      </button>
    </div>
  );
}

ProductCard.propTypes = {
  /** 物件形狀驗證 */
  product: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    name: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired,
    description: PropTypes.string
  }).isRequired,

  /** 陣列元素型別驗證 */
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired
    })
  ),

  /** 函式簽名驗證 */
  onAddToCart: PropTypes.func.isRequired,

  /** 渲染函式驗證 */
  renderActions: PropTypes.func
};

ProductCard.defaultProps = {
  categories: [],
  renderActions: null
};
```

### 4. 自定義驗證器

```jsx
function validateEmail(props, propName, componentName) {
  const email = props[propName];

  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Error(
      `Invalid prop \`${propName}\` of value \`${email}\` supplied to \`${componentName}\`, expected a valid email address.`
    );
  }
}

function validateAge(props, propName, componentName) {
  const age = props[propName];

  if (age !== undefined && (typeof age !== 'number' || age < 0 || age > 150)) {
    return new Error(
      `Invalid prop \`${propName}\` of value \`${age}\` supplied to \`${componentName}\`, expected a number between 0 and 150.`
    );
  }
}

function UserForm({ name, email, age, onSubmit }) {
  return (
    <form onSubmit={onSubmit}>
      <input value={name} placeholder="姓名" />
      <input value={email} placeholder="Email" />
      <input value={age} placeholder="年齡" type="number" />
      <button type="submit">送出</button>
    </form>
  );
}

UserForm.propTypes = {
  name: PropTypes.string.isRequired,
  email: validateEmail,
  age: validateAge,
  onSubmit: PropTypes.func.isRequired
};
```

### 5. 複雜資料結構驗證

```jsx
function DataTable({ columns, data, pagination, onSort }) {
  return (
    <div>
      <table>
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column.key} onClick={() => onSort(column.key)}>
                {column.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.id}>
              {columns.map(column => (
                <td key={column.key}>
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {pagination && (
        <div>
          第 {pagination.current} 頁，共 {pagination.total} 頁
        </div>
      )}
    </div>
  );
}

DataTable.propTypes = {
  columns: PropTypes.arrayOf(
    PropTypes.shape({
      key: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      sortable: PropTypes.bool,
      width: PropTypes.oneOfType([PropTypes.string, PropTypes.number])
    })
  ).isRequired,

  data: PropTypes.arrayOf(PropTypes.object).isRequired,

  pagination: PropTypes.shape({
    current: PropTypes.number.isRequired,
    total: PropTypes.number.isRequired,
    pageSize: PropTypes.number
  }),

  onSort: PropTypes.func
};

DataTable.defaultProps = {
  pagination: null,
  onSort: () => {}
};
```

<br />

## TypeScript 型別定義

### 1. 基本介面定義

```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
}

function Button({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  disabled = false, 
  onClick 
}: ButtonProps) {
  return (
    <button 
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### 2. 複雜型別定義

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  profile: {
    avatar?: string;
    bio?: string;
    preferences: {
      theme: 'light' | 'dark';
      language: string;
    };
  };
}

interface UserProfileProps {
  user: User;
  editable?: boolean;
  onUpdate?: (userId: number, updates: Partial<User>) => void;
  onDelete?: (userId: number) => void;
}

function UserProfile({ 
  user, 
  editable = false, 
  onUpdate, 
  onDelete 
}: UserProfileProps) {
  const handleUpdate = () => {
    if (onUpdate) {
      onUpdate(user.id, { 
        profile: { 
          ...user.profile, 
          bio: '更新的簡介' 
        } 
      });
    }
  };

  return (
    <div className="user-profile">
      <img src={user.profile.avatar} alt={user.name} />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <p>角色：{user.role}</p>
      <p>主題：{user.profile.preferences.theme}</p>

      {editable && (
        <div>
          <button onClick={handleUpdate}>更新</button>
          <button onClick={() => onDelete?.(user.id)}>刪除</button>
        </div>
      )}
    </div>
  );
}
```

### 3. 泛型元件

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string | number;
  emptyMessage?: string;
}

function List<T>({ 
  items, 
  renderItem, 
  keyExtractor, 
  emptyMessage = '沒有資料' 
}: ListProps<T>) {
  if (items.length === 0) {
    return <div className="empty-state">{emptyMessage}</div>;
  }

  return (
    <div className="list">
      {items.map((item, index) => (
        <div key={keyExtractor(item)} className="list-item">
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}

/** 使用範例 */
interface Product {
  id: number;
  name: string;
  price: number;
}

function ProductList({ products }: { products: Product[] }) {
  return (
    <List<Product>
      items={products}
      keyExtractor={(product) => product.id}
      renderItem={(product) => (
        <div>
          <h3>{product.name}</h3>
          <p>NT$ {product.price}</p>
        </div>
      )}
      emptyMessage="沒有產品"
    />
  );
}
```

### 4. 事件處理型別

```typescript
interface FormProps {
  initialData?: {
    name: string;
    email: string;
  };
  onSubmit: (data: { name: string; email: string }) => void;
  onCancel?: () => void;
}

function ContactForm({ initialData, onSubmit, onCancel }: FormProps) {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    email: initialData?.email || ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleInputChange}
        placeholder="姓名"
      />
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleInputChange}
        placeholder="Email"
      />
      <button type="submit">送出</button>
      {onCancel && (
        <button type="button" onClick={onCancel}>
          取消
        </button>
      )}
    </form>
  );
}
```

### 5. 進階型別技巧

```typescript
/** 聯合型別 */
type Status = 'loading' | 'success' | 'error';

/** 條件型別 */
type ApiResponse<T> = {
  status: Status;
  data: Status extends 'success' ? T : null;
  error: Status extends 'error' ? string : null;
};

/** 工具型別 */
interface BaseUser {
  id: number;
  name: string;
  email: string;
}

type CreateUserData = Omit<BaseUser, 'id'>;
type UpdateUserData = Partial<BaseUser>;
type UserKeys = keyof BaseUser;

interface DataComponentProps<T> {
  data: T[];
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
  onItemSelect: (item: T) => void;
}

function DataComponent<T extends { id: number }>({ 
  data, 
  loading, 
  error, 
  onRefresh, 
  onItemSelect 
}: DataComponentProps<T>) {
  if (loading) {
    return <div>載入中...</div>;
  }

  if (error) {
    return (
      <div>
        <p>錯誤：{error}</p>
        <button onClick={onRefresh}>重新載入</button>
      </div>
    );
  }

  return (
    <div>
      {data.map(item => (
        <div key={item.id} onClick={() => onItemSelect(item)}>
          {JSON.stringify(item)}
        </div>
      ))}
    </div>
  );
}
```

<br />

## 實際應用比較

### 1. PropTypes vs TypeScript 比較

```jsx
/** PropTypes 版本 */
import PropTypes from 'prop-types';

function ProductCard({ product, onAddToCart }) {
  return (
    <div>
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>
      <button onClick={() => onAddToCart(product.id)}>
        加入購物車
      </button>
    </div>
  );
}

ProductCard.propTypes = {
  product: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired
  }).isRequired,
  onAddToCart: PropTypes.func.isRequired
};
```

```typescript
/** TypeScript 版本 */
interface Product {
  id: number;
  name: string;
  price: number;
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: number) => void;
}

function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <div>
      <h3>{product.name}</h3>
      <p>NT$ {product.price}</p>
      <button onClick={() => onAddToCart(product.id)}>
        加入購物車
      </button>
    </div>
  );
}
```

### 2. 混合使用策略

```typescript
/** TypeScript 專案中仍可使用 PropTypes 進行執行時驗證 */
import PropTypes from 'prop-types';

interface ValidatedComponentProps {
  data: unknown;
  onProcess: (data: any) => void;
}

function ValidatedComponent({ data, onProcess }: ValidatedComponentProps) {
  return (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <button onClick={() => onProcess(data)}>
        處理資料
      </button>
    </div>
  );
}

/* 執行時驗證 */
ValidatedComponent.propTypes = {
  data: PropTypes.object.isRequired,
  onProcess: PropTypes.func.isRequired
};
```

<br />

## 開發工具整合

### 1. ESLint 規則設定

```json
/** .eslintrc.json */
{
  "extends": [
    "react-app",
    "@typescript-eslint/recommended"
  ],
  "rules": {
    "react/prop-types": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

### 2. TypeScript 設定

```json
/** tsconfig.json */
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noImplicitThis": true
  },
  "include": [
    "src/**/*"
  ]
}
```

### 3. 型別定義檔案組織

```typescript
/** types/user.ts */
export interface User {
  id: number;
  name: string;
  email: string;
}

export interface UserFormData {
  name: string;
  email: string;
}

/** types/api.ts */
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

/** types/components.ts */
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

/** components/UserProfile.tsx */
import { User } from '../types/user';
import { BaseComponentProps } from '../types/components';

interface UserProfileProps extends BaseComponentProps {
  user: User;
  onEdit: (user: User) => void;
}
```

<br />

## 最佳實務

### 1. PropTypes 最佳實務

- 為所有 `props` 定義型別

- 使用 isRequired 標記必填屬性

- 提供合理的 `defaultProps`

- 使用自定義驗證器處理複雜驗證

### 2. TypeScript 最佳實務

- 定義清楚的介面和型別

- 使用泛型提高程式碼重用性

- 適當使用工具型別 (Partial, Omit, Pick)

- 分離型別定義到獨立檔案

### 3. 選擇建議

- 小型專案：PropTypes 足夠使用

- 大型專案：TypeScript 提供更好的開發體驗

- 團隊協作：TypeScript 提供更好的程式碼文件化

- 效能考量：TypeScript 編譯時檢查，PropTypes 執行時檢查

### 4. 遷移策略

- 逐步將 PropTypes 轉換為 TypeScript

- 保留關鍵元件的執行時驗證

- 使用 TypeScript 的嚴格模式

- 建立團隊的型別定義規範
