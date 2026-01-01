# 3.2.2 元件命名規範與檔案結構最佳實務

<br />

## 元件命名規範

### 1. PascalCase 命名法

```jsx
/** ✅ 正確：使用 PascalCase */
function UserProfile() {
  return <div>使用者資料</div>;
}

function ShoppingCart() {
  return <div>購物車</div>;
}

function ProductDetailModal() {
  return <div>產品詳情彈窗</div>;
}

/** ❌ 錯誤：其他命名方式 */
function userProfile() { }  // camelCase
function user_profile() { } // snake_case
function user-profile() { } // kebab-case
```

### 2. 描述性命名

```jsx
/** ✅ 清楚表達元件用途 */
function LoginForm() {
  return <form>登入表單</form>;
}

function NavigationBar() {
  return <nav>導航列</nav>;
}

function ProductCard() {
  return <div>產品卡片</div>;
}

/** ❌ 模糊不清的命名 */
function Component1() { }
function MyComponent() { }
function Thing() { }
```

### 3. 避免縮寫與簡稱

```jsx
/** ✅ 完整且清楚的名稱 */
function UserAuthentication() {
  return <div>使用者驗證</div>;
}

function NavigationMenu() {
  return <nav>導航選單</nav>;
}

/** ❌ 過度縮寫 */
function UserAuth() { }
function NavMenu() { }
function Btn() { }
```

### 4. 元件類型後綴

```jsx
/** 表單相關元件 */
function ContactForm() {
  return <form>聯絡表單</form>;
}

function SearchForm() {
  return <form>搜尋表單</form>;
}

/** 模態框元件 */
function ConfirmModal() {
  return <div>確認彈窗</div>;
}

function ImageModal() {
  return <div>圖片彈窗</div>;
}

/** 列表元件 */
function ProductList() {
  return <ul>產品列表</ul>;
}

function UserList() {
  return <ul>使用者列表</ul>;
}
```

<br />

## 檔案命名規範

### 1. 檔案名稱與元件名稱一致

```text
/** ✅ 正確的檔案命名 */
UserProfile.jsx             對應 UserProfile 元件
ShoppingCart.jsx            對應 ShoppingCart 元件
ProductDetailModal.jsx      對應 ProductDetailModal 元件

/** ❌ 不一致的命名 */
user.jsx                    元件名稱是 UserProfile
cart.jsx                    元件名稱是 ShoppingCart
```

### 2. 檔案副檔名選擇

```text
/** React 元件檔案 */
Component.jsx               包含 JSX 的 React 元件
Component.js                純 JavaScript 的 React 元件

/** TypeScript 專案 */
Component.tsx               TypeScript + JSX
Component.ts                純 TypeScript

/** 樣式檔案 */
Component.module.css        CSS Modules
Component.styled.js         Styled Components
```

<br />

## 目錄結構最佳實務

### 1. 基本專案結構

```text
src/
├── components/                 共用元件
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.module.css
│   │   └── index.js
│   ├── Modal/
│   │   ├── Modal.jsx
│   │   ├── Modal.module.css
│   │   └── index.js
│   └── index.js
├── pages/                      頁面元件
│   ├── Home/
│   │   ├── Home.jsx
│   │   └── Home.module.css
│   ├── About/
│   │   ├── About.jsx
│   │   └── About.module.css
│   └── index.js
├── hooks/                      自定義 Hooks
├── utils/                      工具函式
├── services/                   API 服務
└── App.jsx
```

### 2. 功能導向結構

```text
src/
├── features/
│   ├── authentication/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── SignupForm.jsx
│   │   │   └── index.js
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── index.js
│   │   ├── services/
│   │   │   ├── authAPI.js
│   │   │   └── index.js
│   │   └── index.js
│   ├── products/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ProductList.jsx
│   │   │   └── index.js
│   │   ├── hooks/
│   │   └── services/
│   └── shopping-cart/
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── App.jsx
```

### 3. 原子設計結構

```text
src/
├── components/
│   ├── atoms/              最小單位元件
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Label/
│   │   └── index.js
│   ├── molecules/          組合原子的元件
│   │   ├── SearchBox/
│   │   ├── FormField/
│   │   └── index.js
│   ├── organisms/          複雜的元件組合
│   │   ├── Header/
│   │   ├── ProductGrid/
│   │   └── index.js
│   ├── templates/          頁面模板
│   │   ├── PageLayout/
│   │   └── index.js
│   └── pages/              完整頁面
│       ├── HomePage/
│       ├── ProductPage/
│       └── index.js
```

<br />

## 元件檔案內部結構

### 1. 標準元件檔案結構

```jsx
/** 1. 匯入區域 */
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';

/** 2. 樣式匯入 */
import styles from './ProductCard.module.css';

/** 3. 子元件匯入 */
import Button from '../Button';
import Badge from '../Badge';

/** 4. 常數定義 */
const PRODUCT_STATUS = {
  IN_STOCK: 'in-stock',
  OUT_OF_STOCK: 'out-of-stock',
  DISCONTINUED: 'discontinued'
};

/** 5. 主要元件 */
function ProductCard({ 
  product, 
  onAddToCart, 
  onViewDetails,
  className 
}) {
  const [isLoading, setIsLoading] = useState(false);

  const handleAddToCart = async () => {
    setIsLoading(true);
    await onAddToCart(product.id);
    setIsLoading(false);
  };

  return (
    <div className={clsx(styles.card, className)}>
      <img 
        src={product.image} 
        alt={product.name}
        className={styles.image}
      />

      <div className={styles.content}>
        <h3 className={styles.title}>{product.name}</h3>
        <p className={styles.price}>NT$ {product.price}</p>

        <Badge status={product.status} />

        <div className={styles.actions}>
          <Button 
            onClick={handleAddToCart}
            disabled={isLoading || product.status === PRODUCT_STATUS.OUT_OF_STOCK}
          >
            {isLoading ? '加入中...' : '加入購物車'}
          </Button>

          <Button 
            variant="secondary"
            onClick={() => onViewDetails(product.id)}
          >
            查看詳情
          </Button>
        </div>
      </div>
    </div>
  );
}

/** 6. PropTypes 定義 */
ProductCard.propTypes = {
  product: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired,
    image: PropTypes.string.isRequired,
    status: PropTypes.oneOf(Object.values(PRODUCT_STATUS)).isRequired
  }).isRequired,
  onAddToCart: PropTypes.func.isRequired,
  onViewDetails: PropTypes.func.isRequired,
  className: PropTypes.string
};

/** 7. 預設 Props */
ProductCard.defaultProps = {
  className: ''
};

/** 8. 匯出 */
export default ProductCard;
```

### 2. index.js 檔案模式

```javascript
/** components/Button/index.js */
export { default } from './Button';

/** components/index.js */
export { default as Button } from './Button';
export { default as Modal } from './Modal';
export { default as ProductCard } from './ProductCard';

/** 使用方式 */
import { Button, Modal, ProductCard } from '../components';
```

<br />

## 匯入匯出最佳實務

### 1. 具名匯出 vs 預設匯出

```jsx
/** ✅ 預設匯出：主要元件 */
function Button({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>;
}

export default Button;

/** ✅ 具名匯出：工具函式、常數 */
export const BUTTON_VARIANTS = {
  PRIMARY: 'primary',
  SECONDARY: 'secondary'
};

export function validateProps(props) {
  /** 驗證功能 */
}
```

### 2. 匯入順序規範

```jsx
/** 1. React 相關 */
import React, { useState, useEffect } from 'react';

/** 2. 第三方套件 */
import clsx from 'clsx';
import { format } from 'date-fns';

/** 3. 內部模組 (絕對路徑) */
import { api } from 'services/api';
import { formatCurrency } from 'utils/format';

/** 4. 相對路徑匯入 */
import Button from '../Button';
import Modal from './Modal';

/** 5. 樣式檔案 */
import styles from './Component.module.css';
```

<br />

## 元件分類與組織

### 1. 按功能分類

```text
components/
├── layout/             版面配置元件
│   ├── Header/
│   ├── Footer/
│   ├── Sidebar/
│   └── Layout/
├── forms/              表單相關元件
│   ├── Input/
│   ├── Select/
│   ├── Checkbox/
│   └── FormField/
├── navigation/         導航元件
│   ├── NavBar/
│   ├── Breadcrumb/
│   └── Pagination/
└── feedback/           回饋元件
    ├── Alert/
    ├── Toast/
    └── Loading/
```

### 2. 按複雜度分類

```text
components/
├── basic/              基礎元件
│   ├── Button/
│   ├── Input/
│   └── Icon/
├── composite/          複合元件
│   ├── SearchBox/
│   ├── DataTable/
│   └── ImageGallery/
└── complex/            複雜元件
    ├── Dashboard/
    ├── Calendar/
    └── Editor/
```

<br />

## 命名空間與前綴

### 1. 專案前綴

```jsx
/** 大型專案可使用前綴避免命名衝突 */
function ECommerceProductCard() {
  return <div>電商產品卡片</div>;
}

function ECommerceShoppingCart() {
  return <div>電商購物車</div>;
}
```

### 2. 功能前綴

```jsx
/** 表單元件前綴 */
function FormInput() {
  return <input />;
}

function FormSelect() {
  return <select />;
}

/** 模態框元件前綴 */
function ModalHeader() {
  return <header />;
}

function ModalBody() {
  return <div />;
}
```

<br />

## Props

| 屬性 | 類型 | 必填 | 預設值 | 描述 |
| - | - | - | - | - |
| product | Object | 是 | - | 產品資料物件 |
| onAddToCart | Function | 是 | - | 加入購物車 Callback |

<br />

## 最佳實務總結

- 使用 PascalCase 命名元件

- 檔案名稱與元件名稱保持一致

- 選擇合適的目錄結構模式

- 保持匯入順序的一致性

- 適當使用命名空間避免衝突

- 為複雜元件撰寫文件

- 使用 index.js 簡化匯入路徑

- 按功能或複雜度組織元件

- 遵循團隊的編碼規範

- 定期重構和整理檔案結構
