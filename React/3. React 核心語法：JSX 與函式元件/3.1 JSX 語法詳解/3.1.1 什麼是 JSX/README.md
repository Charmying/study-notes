# 3.1.1 什麼是 JSX：JavaScript XML 語法擴充

<br />

## 定義與概念

JSX (JavaScript XML) 是 React 開發的語法擴充，允許在 JavaScript 程式碼中撰寫類似 HTML 的標記語法。JSX 讓開發者能夠以更直觀的方式描述使用者介面的結構。

<br />

## JSX 基本特性

### 1. 語法結構

```jsx
const element = <h1>Hello, World!</h1>;
```

### 2. JavaScript 表達式嵌入

```jsx
const name = "React";
const element = <h1>Hello, {name}!</h1>;
```

### 3. 屬性設定

```jsx
const element = <img src="image.jpg" alt="描述文字" />;
```

<br />

## JSX 與 HTML 的差異

| 特性 | HTML | JSX |
| - | - | - |
| class 屬性 | `class="container"` | `className="container"` |
| for 屬性 | `for="input"` | `htmlFor="input"` |
| 事件處理 | `onclick="handler()"` | `onClick={handler}` |
| 樣式設定 | `style="color: red"` | `style={{color: 'red'}}` |

<br />

## 編譯過程

JSX 程式碼會透過 Babel 編譯器轉換為 JavaScript

- JSX 原始碼

    ```jsx
    const element = <h1 className="greeting">Hello, World!</h1>;
    ```

- 編譯後的 JavaScript

    ```javascript
    const element = React.createElement(
      'h1',
      {className: 'greeting'},
      'Hello, World!'
    );
    ```

<br />

## JSX 規則

### 1. 必須有根元素

```jsx
/** 錯誤寫法 */
return (
  <h1>標題</h1>
  <p>內容</p>
);

/** 正確寫法 */
return (
  <div>
    <h1>標題</h1>
    <p>內容</p>
  </div>
);

/** 或使用 Fragment */
return (
  <>
    <h1>標題</h1>
    <p>內容</p>
  </>
);
```

### 2. 標籤必須正確關閉

```jsx
/** 自閉合標籤 */
<img src="image.jpg" />
<input type="text" />

/** 成對標籤 */
<div>內容</div>
<span>文字</span>
```

### 3. JavaScript 表達式使用大括號

```jsx
const user = { name: "Charmy", age: 28 };

return (
  <div>
    <h1>{user.name}</h1>
    <p>年齡：{user.age}</p>
    <p>成年：{user.age >= 18 ? "是" : "否"}</p>
  </div>
);
```

<br />

## 實際應用範例

### 基本元件結構

```jsx
function Welcome(props) {
  return (
    <div className="welcome-container">
      <h1>歡迎，{props.name}！</h1>
      <p>今天是 {new Date().toLocaleDateString()}</p>
    </div>
  );
}
```

### 條件渲染

```jsx
function UserStatus({ isLoggedIn, username }) {
  return (
    <div>
      {isLoggedIn ? (
        <h1>歡迎回來，{username}！</h1>
      ) : (
        <h1>請先登入</h1>
      )}
    </div>
  );
}
```

### 列表渲染

```jsx
function TodoList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>
          {item.text}
        </li>
      ))}
    </ul>
  );
}
```

<br />

## 優勢與特點

- 直觀性：語法接近 HTML，學習曲線平緩

- 類型檢查：配合 TypeScript 提供更好的開發體驗

- 工具支援：現代編輯器提供語法高亮與自動完成

- 效能最佳化：編譯時期進行最佳化處理

<br />

## 注意事項

- JSX 是可選的，但強烈建議使用

- 需要設定適當的建置工具 (例如：Webpack + Babel)

- 檔案副檔名通常使用 `.jsx` 或 `.js`

- 遵循 JavaScript 命名慣例 (camelCase)
