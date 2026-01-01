# 3.3.2 現代方案：CSS Modules、Tailwind CSS、CSS-in-JS (Styled-Components/Emotion)

<br />

## CSS Modules

### 1. 基本設定與使用

```css
/* Button.module.css */
.button {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.primary {
  background-color: #007bff;
  color: white;
}

.primary:hover {
  background-color: #0056b3;
}

.secondary {
  background-color: #6c757d;
  color: white;
}

.large {
  padding: 16px 32px;
  font-size: 18px;
}

.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

```jsx
/** Button.jsx */
import styles from './Button.module.css';

function Button({ children, variant = 'primary', size, disabled }) {
  const buttonClasses = [
    styles.button,
    styles[variant],
    size === 'large' && styles.large,
    disabled && styles.disabled
  ].filter(Boolean).join(' ');

  return (
    <button className={buttonClasses} disabled={disabled}>
      {children}
    </button>
  );
}
```

### 2. 組合類別名稱

```css
/* ProductCard.module.css */
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.highlighted {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
}

.image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  margin: 12px 0 8px 0;
  color: #333;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #007bff;
}
```

```jsx
/** ProductCard.jsx */
import styles from './ProductCard.module.css';
import clsx from 'clsx';

function ProductCard({ product, highlighted }) {
  return (
    <div className={clsx(styles.card, highlighted && styles.highlighted)}>
      <img 
        src={product.image} 
        alt={product.name}
        className={styles.image}
      />
      <h3 className={styles.title}>{product.name}</h3>
      <p className={styles.price}>NT$ {product.price}</p>
    </div>
  );
}
```

### 3. 全域與區域樣式混合

```css
/* Layout.module.css */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* 使用 :global() 定義全域樣式 */
:global(.app-header) {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.header {
  composes: app-header from global;
  padding: 16px 0;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

<br />

## Tailwind CSS

### 1. 基本使用

```jsx
function Button({ children, variant = 'primary', size = 'medium', disabled }) {
  const baseClasses = 'font-medium rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500',
    outline: 'border border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500'
  };

  const sizeClasses = {
    small: 'px-3 py-1.5 text-sm',
    medium: 'px-4 py-2 text-base',
    large: 'px-6 py-3 text-lg'
  };

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer';

  return (
    <button 
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

### 2. 響應式設計

```jsx
function ResponsiveGrid({ children }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
      {children}
    </div>
  );
}

function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <img 
        src={product.image} 
        alt={product.name}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">
          {product.name}
        </h3>
        <p className="text-xl font-bold text-blue-600">
          NT$ {product.price.toLocaleString()}
        </p>
        <button className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
          加入購物車
        </button>
      </div>
    </div>
  );
}
```

### 3. 自定義工具類別

```jsx
/** 使用 @apply 指令建立自定義類別 */
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6 border border-gray-200;
  }

  .form-input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent;
  }
}
```

```jsx
function CustomStyledComponents() {
  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-4">表單</h2>
      <input 
        type="text" 
        placeholder="輸入文字"
        className="form-input mb-4"
      />
      <button className="btn-primary">
        送出
      </button>
    </div>
  );
}
```

### 4. 條件樣式與動態類別

```jsx
import clsx from 'clsx';

function StatusBadge({ status, size = 'medium' }) {
  return (
    <span className={clsx(
      'inline-flex items-center font-medium rounded-full',
      {
        'px-2 py-1 text-xs': size === 'small',
        'px-3 py-1 text-sm': size === 'medium',
        'px-4 py-2 text-base': size === 'large'
      },
      {
        'bg-green-100 text-green-800': status === 'success',
        'bg-yellow-100 text-yellow-800': status === 'warning',
        'bg-red-100 text-red-800': status === 'error',
        'bg-gray-100 text-gray-800': status === 'neutral'
      }
    )}>
      {status}
    </span>
  );
}
```

<br />

## Styled-Components

### 1. 基本使用

```jsx
import styled from 'styled-components';

const StyledButton = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  background-color: ${props => 
    props.variant === 'primary' ? '#007bff' : 
    props.variant === 'secondary' ? '#6c757d' : 
    'transparent'
  };

  color: ${props => 
    props.variant === 'outline' ? '#007bff' : 'white'
  };

  border: ${props => 
    props.variant === 'outline' ? '1px solid #007bff' : 'none'
  };

  &:hover {
    background-color: ${props => 
      props.variant === 'primary' ? '#0056b3' : 
      props.variant === 'secondary' ? '#545b62' : 
      '#f8f9fa'
    };
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

function Button({ children, variant = 'primary', ...props }) {
  return (
    <StyledButton variant={variant} {...props}>
      {children}
    </StyledButton>
  );
}
```

### 2. 主題系統

```jsx
import styled, { ThemeProvider } from 'styled-components';

const theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    light: '#f8f9fa',
    dark: '#343a40'
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  breakpoints: {
    sm: '576px',
    md: '768px',
    lg: '992px',
    xl: '1200px'
  }
};

const Card = styled.div`
  background: white;
  border-radius: 8px;
  padding: ${props => props.theme.spacing.md};
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;

  ${props => props.highlighted && `
    border-color: ${props.theme.colors.primary};
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
  `}
`;

const Title = styled.h3`
  color: ${props => props.theme.colors.dark};
  font-size: 18px;
  font-weight: 600;
  margin-bottom: ${props => props.theme.spacing.sm};
`;

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Card highlighted>
        <Title>卡片標題</Title>
        <p>卡片內容</p>
      </Card>
    </ThemeProvider>
  );
}
```

### 3. 繼承與擴展

```jsx
const BaseButton = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
`;

const PrimaryButton = styled(BaseButton)`
  background-color: #007bff;
  color: white;

  &:hover {
    background-color: #0056b3;
  }
`;

const OutlineButton = styled(BaseButton)`
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;

  &:hover {
    background-color: #007bff;
    color: white;
  }
`;

/** 擴展現有元件 */
const LargeButton = styled(PrimaryButton)`
  padding: 16px 32px;
  font-size: 18px;
`;
```

### 4. 動態樣式與動畫

```jsx
import styled, { keyframes, css } from 'styled-components';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

const AnimatedCard = styled.div`
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  animation: ${fadeIn} 0.3s ease-out;

  ${props => props.loading && css`
    animation: ${pulse} 1.5s ease-in-out infinite;
  `}

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
  }
`;
```

<br />

## Emotion

### 1. CSS Prop 使用

```jsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

const buttonStyle = css`
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: #007bff;
  color: white;

  &:hover {
    background-color: #0056b3;
  }
`;

function Button({ children }) {
  return (
    <button css={buttonStyle}>
      {children}
    </button>
  );
}
```

### 2. Styled Components 語法

```jsx
import styled from '@emotion/styled';

const Card = styled.div`
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  ${props => props.highlighted && `
    border: 2px solid #007bff;
  `}
`;

const Title = styled.h3`
  color: #333;
  font-size: 18px;
  margin-bottom: 12px;
`;

function ProductCard({ product, highlighted }) {
  return (
    <Card highlighted={highlighted}>
      <Title>{product.name}</Title>
      <p>NT$ {product.price}</p>
    </Card>
  );
}
```

### 3. 動態樣式函式

```jsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

const getButtonStyles = (variant, size) => css`
  padding: ${size === 'large' ? '16px 32px' : '12px 24px'};
  font-size: ${size === 'large' ? '18px' : '14px'};
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;

  ${variant === 'primary' && `
    background-color: #007bff;
    color: white;
    &:hover {
      background-color: #0056b3;
    }
  `}

  ${variant === 'secondary' && `
    background-color: #6c757d;
    color: white;
    &:hover {
      background-color: #545b62;
    }
  `}
`;

function Button({ children, variant = 'primary', size = 'medium' }) {
  return (
    <button css={getButtonStyles(variant, size)}>
      {children}
    </button>
  );
}
```

<br />

## 方案比較

### 1. 功能特性比較

```jsx
/** CSS Modules - 作用域隔離 */
import styles from './Component.module.css';
<div className={styles.container} />

/** Tailwind CSS - 工具類別 */
<div className="bg-white p-4 rounded-lg shadow-md" />

/** Styled-Components - CSS-in-JS */
const Container = styled.div`
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

/** Emotion - 靈活的 CSS-in-JS */
<div css={css`
  background: white;
  padding: 16px;
  border-radius: 8px;
`} />
```

### 2. 效能考量

```jsx
/** CSS Modules - 編譯時處理，執行時效能最佳 */
const styles = {
  container: 'Component_container__abc123'
};

/** Tailwind CSS - 預建置類別，檔案大小需要 purge */
// 生產環境自動移除未使用的類別

/** Styled-Components - 執行時生成樣式 */
// 使用 babel plugin 可改善效能

/** Emotion - 支援編譯時最佳化 */
// 可選擇執行時或編譯時處理
```

<br />

## 實際專案整合

### 1. 混合使用策略

```jsx
/** 全域樣式使用 CSS */
/* globals.css */
* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/** 元件樣式使用 CSS Modules */
import styles from './Layout.module.css';

/** 工具類別使用 Tailwind */
import clsx from 'clsx';

function Layout({ children }) {
  return (
    <div className={clsx(styles.layout, 'min-h-screen bg-gray-50')}>
      <header className={styles.header}>
        <nav className="flex justify-between items-center">
          導航內容
        </nav>
      </header>
      <main className={styles.main}>
        {children}
      </main>
    </div>
  );
}
```

### 2. 設計系統建立

```jsx
/** 使用 Styled-Components 建立設計系統 */
const theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d'
  },
  spacing: [0, 4, 8, 16, 24, 32, 48, 64],
  fontSizes: [12, 14, 16, 18, 20, 24, 32]
};

const Box = styled.div`
  padding: ${props => theme.spacing[props.p] || 0}px;
  margin: ${props => theme.spacing[props.m] || 0}px;
  background-color: ${props => props.bg || 'transparent'};
`;

const Text = styled.p`
  font-size: ${props => theme.fontSizes[props.size] || 16}px;
  color: ${props => theme.colors[props.color] || 'inherit'};
`;

function DesignSystemExample() {
  return (
    <Box p={4} bg="white">
      <Text size={5} color="primary">
        設計系統標題
      </Text>
      <Text size={2}>
        內容文字
      </Text>
    </Box>
  );
}
```

<br />

## 最佳實務建議

- CSS Modules：適合傳統 CSS 開發者，提供作用域隔離

- Tailwind CSS：快速原型開發，一致的設計系統

- Styled-Components：動態樣式需求，完整的主題系統

- Emotion：靈活性最高，支援多種寫法

- 混合使用：根據需求選擇最適合的方案

- 效能考量：生產環境注意 bundle 大小

- 團隊協作：選擇團隊熟悉且易維護的方案

- 設計系統：建立一致的樣式規範與元件庫
