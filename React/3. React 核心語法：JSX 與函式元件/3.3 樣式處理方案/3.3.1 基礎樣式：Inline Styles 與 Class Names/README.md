# 3.3.1 基礎樣式：Inline Styles 與 Class Names

<br />

## Inline Styles 內聯樣式

### 1. 基本語法

```jsx
function StyledButton() {
  return (
    <button 
      style={{
        backgroundColor: '#007bff',
        color: 'white',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '4px'
      }}
    >
      按鈕
    </button>
  );
}
```

### 2. 樣式物件變數

```jsx
function ProductCard({ product }) {
  const cardStyle = {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '16px',
    margin: '8px',
    backgroundColor: '#fff'
  };

  const titleStyle = {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '8px',
    color: '#333'
  };

  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>{product.name}</h3>
      <p>NT$ {product.price}</p>
    </div>
  );
}
```

### 3. 動態樣式

```jsx
function StatusBadge({ status, isActive }) {
  const badgeStyle = {
    padding: '4px 8px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 'bold',
    backgroundColor: status === 'success' ? '#28a745' : status === 'warning' ? '#ffc107' : '#dc3545',
    color: status === 'warning' ? '#000' : '#fff',
    opacity: isActive ? 1 : 0.6
  };

  return <span style={badgeStyle}>{status}</span>;
}
```

### 4. 條件樣式

```jsx
function ToggleButton({ isToggled, onClick }) {
  const buttonStyle = {
    padding: '10px 20px',
    border: '2px solid #007bff',
    borderRadius: '4px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    backgroundColor: isToggled ? '#007bff' : 'transparent',
    color: isToggled ? 'white' : '#007bff'
  };

  return (
    <button style={buttonStyle} onClick={onClick}>
      {isToggled ? '已啟用' : '未啟用'}
    </button>
  );
}
```

### 5. 響應式樣式處理

```jsx
function ResponsiveContainer() {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const containerStyle = {
    width: '100%',
    maxWidth: windowWidth < 768 ? '100%' : '1200px',
    padding: windowWidth < 768 ? '10px' : '20px',
    margin: '0 auto'
  };

  return (
    <div style={containerStyle}>
      響應式容器
    </div>
  );
}
```

<br />

## Class Names 類別名稱

### 1. 基本 className 使用

```jsx
/** styles.css */
.button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

```jsx
/** Component.jsx */
import './styles.css';

function Button({ children }) {
  return (
    <button className="button">
      {children}
    </button>
  );
}
```

### 2. 多個類別組合

```jsx
/** styles.css */
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
}

.card-highlighted {
  border-color: #007bff;
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
}

.card-large {
  padding: 24px;
  font-size: 18px;
}
```

```jsx
function Card({ children, highlighted, large }) {
  let className = 'card';

  if (highlighted) {
    className += ' card-highlighted';
  }

  if (large) {
    className += ' card-large';
  }

  return (
    <div className={className}>
      {children}
    </div>
  );
}
```

### 3. 條件類別名稱

```jsx
function StatusIndicator({ status, size }) {
  const getClassName = () => {
    let classes = ['status-indicator'];

    if (status === 'success') classes.push('status-success');
    if (status === 'error') classes.push('status-error');
    if (status === 'warning') classes.push('status-warning');

    if (size === 'large') classes.push('status-large');
    if (size === 'small') classes.push('status-small');

    return classes.join(' ');
  };

  return <div className={getClassName()}>狀態指示器</div>;
}
```

### 4. 使用 `clsx` 工具庫

```jsx
import clsx from 'clsx';

function Button({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  disabled = false,
  fullWidth = false 
}) {
  return (
    <button 
      className={clsx(
        'btn',
        `btn-${variant}`,
        `btn-${size}`,
        {
          'btn-disabled': disabled,
          'btn-full-width': fullWidth
        }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

### 5. 動態類別名稱生成

```jsx
function ProductGrid({ products, layout, sortBy }) {
  const gridClassName = clsx(
    'product-grid',
    `layout-${layout}`, // 'layout-grid' 或 'layout-list'
    `sort-${sortBy}`,   // 'sort-price' 或 'sort-name'
    {
      'has-products': products.length > 0,
      'empty-grid': products.length === 0
    }
  );

  return (
    <div className={gridClassName}>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

<br />

## 樣式方法比較

### 1. Inline Styles vs Class Names

```jsx
/** Inline Styles - 適合動態樣式 */
function DynamicButton({ color, size }) {
  const buttonStyle = {
    backgroundColor: color,
    padding: size === 'large' ? '15px 30px' : '10px 20px',
    fontSize: size === 'large' ? '18px' : '14px'
  };

  return <button style={buttonStyle}>動態按鈕</button>;
}

/** Class Names - 適合靜態樣式與偽類 */
function StaticButton({ variant }) {
  return (
    <button className={`btn btn-${variant}`}>
      靜態按鈕
    </button>
  );
}
```

### 2. 混合使用策略

```jsx
function FlexibleCard({ 
  children, 
  backgroundColor, 
  highlighted, 
  customPadding 
}) {
  const dynamicStyle = {
    backgroundColor: backgroundColor,
    padding: customPadding
  };

  return (
    <div 
      className={clsx('card', { 'card-highlighted': highlighted })}
      style={dynamicStyle}
    >
      {children}
    </div>
  );
}
```

<br />

## 實際應用範例

### 1. 主題切換系統

```jsx
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  const themeStyles = {
    light: {
      backgroundColor: '#ffffff',
      color: '#333333'
    },
    dark: {
      backgroundColor: '#333333',
      color: '#ffffff'
    }
  };

  return (
    <div 
      className={`app-container theme-${theme}`}
      style={themeStyles[theme]}
    >
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        切換主題
      </button>
      {children}
    </div>
  );
}
```

### 2. 進度條元件

```jsx
function ProgressBar({ progress, color = '#007bff', height = 20 }) {
  const containerStyle = {
    width: '100%',
    height: `${height}px`,
    backgroundColor: '#e9ecef',
    borderRadius: `${height / 2}px`,
    overflow: 'hidden'
  };

  const barStyle = {
    width: `${Math.min(Math.max(progress, 0), 100)}%`,
    height: '100%',
    backgroundColor: color,
    transition: 'width 0.3s ease'
  };

  return (
    <div className="progress-container" style={containerStyle}>
      <div className="progress-bar" style={barStyle} />
    </div>
  );
}
```

### 3. 響應式網格系統

```jsx
function GridSystem({ children, columns = 3, gap = 16 }) {
  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, 1fr)`,
    gap: `${gap}px`,
    width: '100%'
  };

  return (
    <div 
      className="responsive-grid"
      style={gridStyle}
    >
      {children}
    </div>
  );
}
```

### 4. 動畫按鈕

```jsx
function AnimatedButton({ children, onClick, loading = false }) {
  const [isPressed, setIsPressed] = useState(false);

  const buttonStyle = {
    padding: '12px 24px',
    border: 'none',
    borderRadius: '6px',
    backgroundColor: loading ? '#6c757d' : '#007bff',
    color: 'white',
    cursor: loading ? 'not-allowed' : 'pointer',
    transform: isPressed ? 'scale(0.95)' : 'scale(1)',
    transition: 'all 0.1s ease',
    opacity: loading ? 0.7 : 1
  };

  return (
    <button
      className="animated-button"
      style={buttonStyle}
      onClick={onClick}
      disabled={loading}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
    >
      {loading ? '載入中...' : children}
    </button>
  );
}
```

<br />

## 效能考量

### 1. 避免在 render 中建立樣式物件

```jsx
/** ❌ 每次渲染都建立新物件 */
function BadExample() {
  return (
    <div style={{ padding: '10px', margin: '5px' }}>
      內容
    </div>
  );
}

/** ✅ 將樣式提取到外部 */
const containerStyle = { padding: '10px', margin: '5px' };

function GoodExample() {
  return (
    <div style={containerStyle}>
      內容
    </div>
  );
}
```

### 2. 使用 `useMemo` 快取複雜樣式

```jsx
function ComplexStyledComponent({ data, theme, size }) {
  const computedStyle = useMemo(() => {
    return {
      backgroundColor: theme.primary,
      padding: size === 'large' ? '20px' : '10px',
      borderRadius: data.rounded ? '8px' : '0px',
      boxShadow: data.elevated ? '0 4px 8px rgba(0,0,0,0.1)' : 'none'
    };
  }, [theme.primary, size, data.rounded, data.elevated]);

  return (
    <div style={computedStyle}>
      複雜樣式元件
    </div>
  );
}
```

<br />

## 最佳實務

### 1. 選擇適當的樣式方法

```jsx
/** ✅ 靜態樣式使用 CSS 類別 */
function StaticCard() {
  return <div className="card">靜態卡片</div>;
}

/** ✅ 動態樣式使用 inline styles */
function DynamicCard({ backgroundColor }) {
  return (
    <div 
      className="card"
      style={{ backgroundColor }}
    >
      動態卡片
    </div>
  );
}
```

### 2. 保持樣式的可維護性

```jsx
/** ✅ 將複雜樣式提取到函式 */
function getButtonStyles(variant, size, disabled) {
  const baseStyles = {
    padding: size === 'large' ? '15px 30px' : '10px 20px',
    border: 'none',
    borderRadius: '4px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.6 : 1
  };

  const variantStyles = {
    primary: { backgroundColor: '#007bff', color: 'white' },
    secondary: { backgroundColor: '#6c757d', color: 'white' },
    outline: { backgroundColor: 'transparent', border: '1px solid #007bff', color: '#007bff' }
  };

  return { ...baseStyles, ...variantStyles[variant] };
}

function Button({ children, variant, size, disabled }) {
  return (
    <button style={getButtonStyles(variant, size, disabled)}>
      {children}
    </button>
  );
}
```

<br />

## 最佳實務總結

- 靜態樣式使用 CSS 類別：利用 CSS 的偽類和媒體查詢

- 動態樣式使用 inline styles：根據 `props` 或 `state` 變化

- 避免在 render 中建立樣式物件：提取到外部或使用 `useMemo`

- 使用工具庫簡化類別名稱管理：例如：`clsx` 或 `classnames`

- 保持樣式的可讀性：複雜樣式提取到函式

- 考慮效能影響：避免不必要的重新計算

- 混合使用兩種方法：發揮各自優勢

- 保持一致的命名規範：提高程式碼可維護性
