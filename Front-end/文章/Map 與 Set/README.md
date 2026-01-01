# `Map` 與 `Set`

在 JavaScript 中，除了基本的物件 (Object) 和陣列 (Array)，ES6 之後引入了兩個非常實用的資料結構：`Map` 與 `Set`。

`Map` 與 `Set` 分別解決了物件與陣列的一些限制，在處理關聯資料與集合運算時特別方便。

<br />

## `Map`

### 概念

`Map` 是一種鍵值對 (Key-value Pairs) 的資料結構，類似於物件 (Object)。

相較於物件，`Map` 有幾個明顯的優勢

- 任何型別都能當作 key (包含物件、函式、`NaN` 等)。

- 保持插入順序 (遍歷時會依照插入的順序)。

- 內建方法更完整，方便操作。

### 建立 `Map`

```javascript
const map = new Map();

// 新增資料
map.set('name', 'Charmy');
map.set(123, '數字 key');
map.set(true, '布林值 key');

// 取值
console.log(map.get('name')); // Charmy
console.log(map.get(123));    // 數字 key
console.log(map.get(true));   // 布林值 key
```

### 常用方法

| 方法 | 說明 |
| - | - |
| `set(key, value)` | 新增或更新一筆資料 |
| `get(key)` | 取得對應的值 |
| `has(key)` | 判斷是否存在某個 key |
| `delete(key)` | 刪除一筆資料 |
| `clear()` | 清空所有資料 |
| `size` | 回傳 `Map` 的大小 |

### 範例

```javascript
const map = new Map([
  ['a', 1],
  ['b', 2]
]);

map.set('c', 3);
console.log(map.size); // 3

console.log(map.has('a')); // true
map.delete('b');
console.log(map.has('b')); // false

map.clear();
console.log(map.size); // 0
```

### 遍歷 `Map`

```javascript
const map = new Map([
  ['name', 'Charmy'],
  ['age', 28]
]);

// for...of
for (const [key, value] of map) {
  console.log(key, value);
}

// forEach
map.forEach((value, key) => {
  console.log(key, value);
});
```

執行結果：

```console
name Charmy
age 28
name Charmy
age 28
```

<br />

## `Set`

### 概念

`Set` 是一種 不重複的值集合。

`Set` 的特色

- 只能存放唯一值，自動去除重複項目。

- 可以存放任何型別的資料。

- 插入順序保留，可被遍歷。

### 建立 `Set`

```javascript
const set = new Set([1, 2, 3, 3, 4]);

console.log(set); // Set { 1, 2, 3, 4 }
```

### 常用方法

| 方法 | 說明 |
| - | - |
| `add(value)` | 新增資料 |
| `has(value)` | 判斷是否存在某個值 |
| `delete(value)` | 刪除某個值 |
| `clear()` | 清空所有資料 |
| `size` | 回傳集合大小 |

### 範例

```javascript
const set = new Set();

set.add(1);
set.add(2);
set.add(2); // 重複的值不會加入

console.log(set.size);   // 2
console.log(set.has(1)); // true

set.delete(2);
console.log(set.has(2)); // false

set.clear();
console.log(set.size); // 0
```

### 遍歷 `Set`

```javascript
const set = new Set(['蘋果', '香蕉', '葡萄']);

for (const value of set) {
  console.log(value);
}

// forEach
set.forEach(value => {
  console.log(value);
});
```

<br />

## `Map` 與 `Set` 的差異比較

| 特性 | `Map` | `Set` |
| - | - | - |
| 資料結構 | 鍵值對 | 單一值集合 |
| Key | 可以是任何型別 | 不存在 key，只有值 |
| Value | 任何型別 | 任何型別 |
| 是否允許重複 | key 唯一，值可重複 | 值必須唯一 |
| 插入順序 | 保留 | 保留 |
| 常見用途 | 關聯資料、快取、查表 | 去重、集合運算 |

<br />

## 實際應用場景

### `Map` 的應用

- 快取結果 (避免重複計算)

- 儲存物件與資訊的對應關係

```javascript
const cache = new Map();

function fibonacci(n) {
  if (cache.has(n)) return cache.get(n);
  if (n <= 1) return n;
  const result = fibonacci(n - 1) + fibonacci(n - 2);
  cache.set(n, result);
  return result;
}

console.log(fibonacci(10)); // 55
```

### `Set` 的應用

- 去除陣列重複值

	```javascript
	const arr = [1, 2, 2, 3, 4, 4, 5];
	const uniqueArr = [...new Set(arr)];
	console.log(uniqueArr); // [1, 2, 3, 4, 5]
	```

- 集合運算 (交集、聯集、差集)

	```javascript
	const setA = new Set([1, 2, 3]);
	const setB = new Set([2, 3, 4]);

	// 聯集
	const union = new Set([...setA, ...setB]); 
	console.log(union); // {1, 2, 3, 4}

	// 交集
	const intersection = new Set([...setA].filter(x => setB.has(x)));
	console.log(intersection); // {2, 3}

	// 差集
	const difference = new Set([...setA].filter(x => !setB.has(x)));
	console.log(difference); // {1}
	```

<br />

## 總結

- `Map` 適合用來處理關聯資料 (像字典或快取)。

- `Set` 適合用來處理唯一值集合 (像去重或集合運算)。

- 兩者都保留插入順序，且都提供了比傳統物件、陣列更方便的操作方法。

簡單來說，在實務專案中，需要快速查詢、儲存關聯時選擇 `Map`，需要去掉重複資料或集合操作時，選擇 `Set`。
