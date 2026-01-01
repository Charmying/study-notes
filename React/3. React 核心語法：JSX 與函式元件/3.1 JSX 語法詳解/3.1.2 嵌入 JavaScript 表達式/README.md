# 3.1.2 嵌入 JavaScript 表達式：使用 `{}`

<br />

## 基本語法

在 JSX 中使用大括號 `{}` 來嵌入 JavaScript 表達式，讓動態內容能夠渲染到使用者介面上。

```jsx
const name = "React";
const element = <h1>Hello, {name}!</h1>;
```

<br />

## 表達式類型

### 1. 變數與常數

```jsx
const title = "學習 React";
const version = 18;

return (
  <div>
    <h1>{title}</h1>
    <p>版本：{version}</p>
  </div>
);
```

### 2. 數學運算

```jsx
const a = 10;
const b = 5;

return (
  <div>
    <p>加法：{a + b}</p>
    <p>乘法：{a * b}</p>
    <p>餘數：{a % b}</p>
  </div>
);
```

### 3. 字串操作

```jsx
const firstName = "Charmy";
const lastName = "Tseng";

return (
  <div>
    <p>全名：{firstName + " " + lastName}</p>
    <p>長度：{firstName.length}</p>
    <p>大寫：{firstName.toUpperCase()}</p>
  </div>
);
```

### 4. 陣列方法

```jsx
const numbers = [1, 2, 3, 4, 5];

return (
  <div>
    <p>總和：{numbers.reduce((sum, num) => sum + num, 0)}</p>
    <p>最大值：{Math.max(...numbers)}</p>
    <p>長度：{numbers.length}</p>
  </div>
);
```

<br />

## 物件屬性存取

### 1. 點記號存取

```jsx
const user = {
  name: "Charmy",
  age: 28,
  email: "charmy@example.com"
};

return (
  <div>
    <h2>{user.name}</h2>
    <p>年齡：{user.age}</p>
    <p>信箱：{user.email}</p>
  </div>
);
```

### 2. 括號記號存取

```jsx
const user = {
  "first-name": "Charmy",
  "last-name": "Tseng"
};

return (
  <div>
    <p>姓名：{user["first-name"]} {user["last-name"]}</p>
  </div>
);
```

<br />

## 函式呼叫

### 1. 內建函式

```jsx
const currentDate = new Date();

return (
  <div>
    <p>今天：{currentDate.toLocaleDateString()}</p>
    <p>時間：{currentDate.toLocaleTimeString()}</p>
    <p>隨機數：{Math.random().toFixed(2)}</p>
  </div>
);
```

### 2. 自定義函式

```jsx
function formatPrice(price) {
  return `NT$ ${price.toLocaleString()}`;
}

function calculateTax(price, rate = 0.05) {
  return price * rate;
}

const productPrice = 1000;

return (
  <div>
    <p>價格：{formatPrice(productPrice)}</p>
    <p>稅額：{formatPrice(calculateTax(productPrice))}</p>
  </div>
);
```

<br />

## 條件表達式

### 1. 三元運算子

```jsx
const isLoggedIn = true;
const username = "Charmy";

return (
  <div>
    <h1>{isLoggedIn ? `歡迎，${username}` : "請登入"}</h1>
    <p>狀態：{isLoggedIn ? "已登入" : "未登入"}</p>
  </div>
);
```

### 2. 短路運算

```jsx
const user = { name: "Charmy", premium: true };
const notifications = ["訊息1", "訊息2"];

return (
  <div>
    {user.premium && <span>⭐ 高級會員</span>}
    {notifications.length > 0 && (
      <p>未讀訊息：{notifications.length}</p>
    )}
  </div>
);
```

<br />

## 屬性中的表達式

### 1. 動態屬性值

```jsx
const imageUrl = "https://example.com/image.jpg";
const altText = "範例圖片";
const isActive = true;

return (
  <div>
    <img src={imageUrl} alt={altText} />
    <button className={isActive ? "active" : "inactive"}>
      按鈕
    </button>
  </div>
);
```

### 2. 樣式物件

```jsx
const primaryColor = "#007bff";
const fontSize = 16;

const buttonStyle = {
  backgroundColor: primaryColor,
  fontSize: fontSize,
  padding: "10px 20px",
  border: "none",
  borderRadius: "4px"
};

return <button style={buttonStyle}>樣式按鈕</button>;
```

<br />

## 陣列渲染

### 1. 基本列表

```jsx
const fruits = ["蘋果", "香蕉", "橘子"];

return (
  <ul>
    {fruits.map((fruit, index) => (
      <li key={index}>{fruit}</li>
    ))}
  </ul>
);
```

### 2. 物件陣列

```jsx
const products = [
  { id: 1, name: "筆記型電腦", price: 34500 },
  { id: 2, name: "滑鼠", price: 2980 },
  { id: 3, name: "鍵盤", price: 2280 }
];

return (
  <div>
    {products.map(product => (
      <div key={product.id}>
        <h3>{product.name}</h3>
        <p>價格：NT$ {product.price.toLocaleString()}</p>
      </div>
    ))}
  </div>
);
```

<br />

## 複雜表達式範例

### 1. 多層條件判斷

```jsx
const score = 85;

function getGrade(score) {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  return "D";
}

return (
  <div>
    <p>分數：{score}</p>
    <p>等級：{getGrade(score)}</p>
    <p>狀態：{score >= 60 ? "及格" : "不及格"}</p>
  </div>
);
```

### 2. 資料處理與格式化

```jsx
const orders = [
  { id: 1, amount: 1200, status: "completed" },
  { id: 2, amount: 800, status: "pending" },
  { id: 3, amount: 1500, status: "completed" }
];

const completedOrders = orders.filter(order => order.status === "completed");
const totalAmount = completedOrders.reduce((sum, order) => sum + order.amount, 0);

return (
  <div>
    <p>已完成訂單：{completedOrders.length} 筆</p>
    <p>總金額：NT$ {totalAmount.toLocaleString()}</p>
    <p>平均金額：NT$ {Math.round(totalAmount / completedOrders.length).toLocaleString()}</p>
  </div>
);
```

<br />

## 注意事項

### 1. 不可使用的語句

```jsx
/** ❌ 錯誤：不能使用 if 語句 */
return <div>{if (true) { "Hello" }}</div>;

/** ✅ 正確：使用三元運算子 */
return <div>{true ? "Hello" : "Goodbye"}</div>;
```

### 2. 物件直接渲染

```jsx
const user = { name: "Charmy", age: 28 };

/** ❌ 錯誤：不能直接渲染物件 */
return <div>{user}</div>;

/** ✅ 正確：渲染物件屬性 */
return <div>{user.name}</div>;
```

### 3. 函式與表達式的區別

```jsx
/** ❌ 錯誤：函式定義不是表達式 */
return <div>{function() { return "Hello"; }}</div>;

/** ✅ 正確：函式呼叫是表達式 */
return <div>{(() => "Hello")()}</div>;
```

<br />

## 最佳實務

- 保持表達式簡潔：複雜運算應提取到變數或函式中

- 避免副作用：表達式不應修改狀態或產生副作用

- 使用有意義的變數名稱：提高程式碼可讀性

- 適當使用空格：在大括號內外加入適當空格
