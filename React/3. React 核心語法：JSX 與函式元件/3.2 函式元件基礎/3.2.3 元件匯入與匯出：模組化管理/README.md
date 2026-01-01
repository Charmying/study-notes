# 3.2.3 元件匯入與匯出：模組化管理

<br />

## 基本匯出方式

### 1. 預設匯出 (Default Export)

```jsx
/** Button.jsx */
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

export default Button;
```

### 2. 具名匯出 (Named Export)

```javascript
/** utils.js */
export function formatPrice(price) {
  return `NT$ ${price.toLocaleString()}`;
}

export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export const API_ENDPOINTS = {
  USERS: '/api/users',
  PRODUCTS: '/api/products'
};
```

### 3. 混合匯出

```jsx
/** ProductCard.jsx */
function ProductCard({ product }) {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>{formatPrice(product.price)}</p>
    </div>
  );
}

export const PRODUCT_STATUS = {
  AVAILABLE: 'available',
  OUT_OF_STOCK: 'out_of_stock'
};

export function calculateDiscount(price, discountRate) {
  return price * (1 - discountRate);
}

export default ProductCard;
```

<br />

## 基本匯入方式

### 1. 預設匯入

```jsx
// App.jsx
import Button from './components/Button';
import ProductCard from './components/ProductCard';

function App() {
  return (
    <div>
      <Button onClick={() => console.log('clicked')}>
        點擊按鈕
      </Button>
      <ProductCard product={{ name: '商品', price: 1000 }} />
    </div>
  );
}
```

### 2. 具名匯入

```jsx
/** App.jsx */
import { formatPrice, validateEmail, API_ENDPOINTS } from './utils';

function App() {
  const price = formatPrice(1000);
  const isValid = validateEmail('test@example.com');

  return <div>{price}</div>;
}
```

### 3. 混合匯入

```jsx
/** App.jsx */
import ProductCard, { PRODUCT_STATUS, calculateDiscount } from './components/ProductCard';

function App() {
  const discountedPrice = calculateDiscount(1000, 0.1);

  return (
    <ProductCard 
      product={{ 
        name: '商品', 
        price: discountedPrice,
        status: PRODUCT_STATUS.AVAILABLE 
      }} 
    />
  );
}
```

### 4. 重新命名匯入

```jsx
/** App.jsx */
import { formatPrice as formatCurrency } from './utils/price';
import { Button as PrimaryButton } from './components/Button';

function App() {
  const price = formatCurrency(1000);

  return (
    <PrimaryButton>
      價格：{price}
    </PrimaryButton>
  );
}
```

### 5. 全部匯入

```jsx
/** App.jsx */
import * as Utils from './utils';
import * as Components from './components';

function App() {
  const price = Utils.formatPrice(1000);

  return (
    <Components.Button>
      {price}
    </Components.Button>
  );
}
```

<br />

## 模組化管理策略

### 1. index.js 檔案模式

```javascript
/** components/Button/index.js */
export { default } from './Button';

/** components/Modal/index.js */
export { default } from './Modal';

/** components/index.js */
export { default as Button } from './Button';
export { default as Modal } from './Modal';
export { default as ProductCard } from './ProductCard';
export { default as UserProfile } from './UserProfile';
```

```jsx
/** 使用方式 */
import { Button, Modal, ProductCard } from './components';

function App() {
  return (
    <div>
      <Button>按鈕</Button>
      <Modal>彈窗內容</Modal>
      <ProductCard />
    </div>
  );
}
```

### 2. 分類匯出

```javascript
/** components/forms/index.js */
export { default as Input } from './Input';
export { default as Select } from './Select';
export { default as Checkbox } from './Checkbox';
export { default as FormField } from './FormField';

/** components/layout/index.js */
export { default as Header } from './Header';
export { default as Footer } from './Footer';
export { default as Sidebar } from './Sidebar';

/** components/index.js */
export * from './forms';
export * from './layout';
export { default as Button } from './Button';
```

### 3. 功能模組匯出

```javascript
/** features/authentication/index.js */
export { default as LoginForm } from './components/LoginForm';
export { default as SignupForm } from './components/SignupForm';
export { useAuth } from './hooks/useAuth';
export { authAPI } from './services/authAPI';

/** features/products/index.js */
export { default as ProductList } from './components/ProductList';
export { default as ProductCard } from './components/ProductCard';
export { useProducts } from './hooks/useProducts';
export { productsAPI } from './services/productsAPI';
```

<br />

## 路徑管理

### 1. 相對路徑

```jsx
/** 當前目錄 */
import Button from './Button';

/** 上層目錄 */
import Utils from '../utils';

/** 上兩層目錄 */
import API from '../../services/api';
```

### 2. 絕對路徑 (使用 jsconfig.json 或 tsconfig.json)

```json
/** jsconfig.json */
{
  "compilerOptions": {
    "baseUrl": "src",
    "paths": {
      "@components/*": ["components/*"],
      "@utils/*": ["utils/*"],
      "@services/*": ["services/*"],
      "@hooks/*": ["hooks/*"]
    }
  }
}
```

```jsx
/** 使用絕對路徑 */
import Button from '@components/Button';
import { formatPrice } from '@utils/format';
import { api } from '@services/api';
import { useAuth } from '@hooks/useAuth';
```

### 3. 環境變數路徑

```javascript
/** webpack.config.js 或 vite.config.js */
export default {
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
      '@utils': path.resolve(__dirname, 'src/utils')
    }
  }
};
```

<br />

## 動態匯入

### 1. 基本動態匯入

```jsx
/** 動態載入元件 */
function App() {
  const [Component, setComponent] = useState(null);

  const loadComponent = async () => {
    const { default: DynamicComponent } = await import('./components/HeavyComponent');
    setComponent(() => DynamicComponent);
  };

  return (
    <div>
      <button onClick={loadComponent}>載入元件</button>
      {Component && <Component />}
    </div>
  );
}
```

### 2. React.lazy 與 Suspense

```jsx
/** Lazy Loading Component 元件 */
const LazyComponent = React.lazy(() => import('./components/LazyComponent'));
const AnotherLazyComponent = React.lazy(() => import('./components/AnotherLazyComponent'));

function App() {
  return (
    <div>
      <Suspense fallback={<div>載入中...</div>}>
        <LazyComponent />
        <AnotherLazyComponent />
      </Suspense>
    </div>
  );
}
```

### 3. 條件動態匯入

```jsx
function FeatureComponent({ featureEnabled }) {
  const [FeatureModule, setFeatureModule] = useState(null);

  useEffect(() => {
    if (featureEnabled) {
      import('./features/AdvancedFeature').then(module => {
        setFeatureModule(() => module.default);
      });
    }
  }, [featureEnabled]);

  if (!featureEnabled) {
    return <div>功能未啟用</div>;
  }

  return FeatureModule ? <FeatureModule /> : <div>載入中...</div>;
}
```

<br />

## 循環依賴處理

### 1. 避免循環依賴

```jsx
/** ❌ 錯誤：循環依賴 */
/** ComponentA.jsx */
import ComponentB from './ComponentB';

function ComponentA() {
  return <ComponentB />;
}

/** ComponentB.jsx */
import ComponentA from './ComponentA'; // 循環依賴

function ComponentB() {
  return <ComponentA />;
}
```

### 2. 解決方案：提取共用功能

```jsx
/** ✅ 正確：提取共用功能到第三個檔案 */
/** shared.js */
export const sharedLogic = () => {
  // 共用功能
};

/** ComponentA.jsx */
import { sharedLogic } from './shared';

function ComponentA() {
  sharedLogic();
  return <div>Component A</div>;
}

/** ComponentB.jsx */
import { sharedLogic } from './shared';

function ComponentB() {
  sharedLogic();
  return <div>Component B</div>;
}
```

<br />

## 型別定義匯出 (TypeScript)

### 1. 介面匯出

```typescript
/** types/User.ts */
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

export interface UserProps {
  user: User;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}
```

### 2. 型別匯出

```typescript
/** types/Product.ts */
export type ProductStatus = 'available' | 'out_of_stock' | 'discontinued';

export type Product = {
  id: string;
  name: string;
  price: number;
  status: ProductStatus;
};

export type ProductCardProps = {
  product: Product;
  onAddToCart: (productId: string) => void;
};
```

### 3. 元件與型別一起匯出

```typescript
/** ProductCard.tsx */
import { ProductCardProps } from './types';

function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => onAddToCart(product.id)}>
        加入購物車
      </button>
    </div>
  );
}

export default ProductCard;
export type { ProductCardProps };
```

<br />

## 實際專案範例

### 1. 大型專案結構

```javascript
/** src/components/index.js */
export { default as Button } from './Button';
export { default as Input } from './Input';
export { default as Modal } from './Modal';

/** src/features/index.js */
export * from './authentication';
export * from './products';
export * from './orders';

/** src/utils/index.js */
export * from './format';
export * from './validation';
export * from './api';

/** src/index.js */
export * from './components';
export * from './features';
export * from './utils';
```

### 2. 主應用程式匯入

```jsx
/** App.jsx */
import React from 'react';
import { 
  Button, 
  Modal,
  LoginForm,
  ProductList,
  formatPrice,
  validateEmail 
} from './src';

function App() {
  return (
    <div className="app">
      <LoginForm />
      <ProductList />
      <Modal>
        <Button>關閉</Button>
      </Modal>
    </div>
  );
}

export default App;
```

<br />

## 效能最佳化

### 1. Tree Shaking 友善的匯出

```javascript
/** ✅ 支援 Tree Shaking */
export function formatPrice(price) {
  return `NT$ ${price.toLocaleString()}`;
}

export function formatDate(date) {
  return date.toLocaleDateString();
}

/** ❌ 不支援 Tree Shaking */
export default {
  formatPrice: (price) => `NT$ ${price.toLocaleString()}`,
  formatDate: (date) => date.toLocaleDateString()
};
```

### 2. 按需載入

```jsx
/** 只匯入需要的函式 */
import { formatPrice } from './utils'; // 只載入 formatPrice

/** 避免匯入整個模組 */
import * as Utils from './utils'; // 載入所有函式
```

<br />

## 最佳實務

- 優先使用具名匯出：提高 Tree Shaking 效果

- 保持匯入順序一致：React → 第三方 → 內部模組 → 樣式

- 使用 index.js 簡化匯入路徑

- 避免循環依賴：重構共用功能

- 適當使用動態匯入：提升應用程式效能

- 設定路徑別名：簡化長路徑匯入

- 分類組織匯出：按功能或類型分組

- 文件化匯出介面：提供清楚的 API 說明
