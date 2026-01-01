# Array (陣列) 的處理方法

以下整理了 JavaScript 中對 Array (陣列) 的處理方法。

### 基本屬性和方法

- [`length` property：獲取陣列長度。](#length-property-length-屬性)

- [`push()`：將元素添加到陣列的末尾。](#push)

- [`pop()`：移除並返回陣列的最後一個元素。](#pop)

- [`shift()`：移除並返回陣列的第一個元素。](#shift)

- [`unshift()`：將元素添加到陣列的開頭。](#unshift)

### 修改陣列的方法

- [`splice()`：添加、移除或替換陣列中的元素。](#splice)

- [`fill()`：用靜態值填充陣列中的元素。](#fill)

- [`reverse()`：反轉陣列中元素的順序。](#reverse)

- [`sort()`：對陣列中的元素進行排序。](#sort)

- [`copyWithin()`：在陣列內部複製元素到其他位置。](#copywithin)

### 返回新陣列的方法

- [`slice()`：返回一個新的陣列，包含從開始索引到結束索引 (不包含結束索引) 的部分元素。](#slice)

- [`concat()`：合併數個陣列，返回一個新陣列。](#concat)

- [`flat()`：將多維陣列展平成一維陣列。](#flat)

- [`flatMap()`：先對陣列進行 `map()` 操作，再將結果展平成一維陣列。](#flatmap)

- [`toSorted()`：返回一個已排序的新陣列，不改變原本的陣列。](#tosorted-es2023)

- [`toReversed()`：返回一個倒序的新陣列，不改變原本的陣列。](#toreversed-es2023)

- [`toSpliced()`：返回一個已修改的新陣列，用法類似 `splice()`，但不改變原本的陣列。](#tospliced-es2023)

- [`with()`：返回一個指定索引值被替換的新陣列，不改變原本的陣列。](#with-es2023)

### 轉換和迭代方法

- [`toString()`：將陣列轉換為字串，元素之間以逗號分隔。](#tostring)

- [`join()`：將陣列轉換為字串，可以指定分隔符號。](#join)

- [`forEach()`：為陣列中的每個元素執行一次提供的函式。](#foreach)

- [`map()`：創建一個新陣列，其元素是調用函式處理每個元素後的結果。](#map)

- [`filter()`：創建一個新陣列，其結果是滿足條件的所有元素。](#filter)

- [`reduce()`：將陣列中的每個元素依次累積，最終為單一值。](#reduce)

- [`reduceRight()`：從右到左對陣列中的元素進行累積，最終為單一值。](#reduceright)

### 搜尋和判斷方法

- [`includes()`：判斷陣列是否包含某個值，返回布林值。](#includes)

- [`indexOf()`：返回指定元素在陣列中的第一個索引，若沒有找到則返回 `-1`。](#indexof)

- [`lastIndexOf()`：返回指定元素在陣列中的最後一個索引，若沒有找到則返回 `-1`。](#lastindexof)

- [`find()`：返回符合條件的第一個元素，否則返回 `undefined`。](#find)

- [`findIndex()`：返回符合條件的第一個元素的索引，否則返回 `-1`。](#findindex)

- [`some()`：判斷陣列中是否至少有一個元素滿足條件，返回布林值。](#some)

- [`every()`：判斷陣列中的所有元素是否都滿足條件，返回布林值。](#every)

### 迭代器和靜態方法

- [`entries()`：返回一個新的陣列迭代器物件，包含鍵值對。](#entries)

- [`keys()`：返回一個新的陣列迭代器物件，包含每個索引。](#keys)

- [`values()`：回傳一個陣列值的迭代器，可用 `for...of` 取出每個值。](#values)

- [`from()`：將類陣列物件或可迭代物件轉換為陣列。](#from)

- [`isArray()`：檢查給定的值是否為陣列，返回布林值。](#isarray)

### 其他方法

- [`valueOf()`：返回陣列的原始值。](#valueof)

- [`at()`：取得指定索引的值。](#at-es2022)

- [`group()`：根據 Callback Function 的回傳值分組陣列元素，回傳一個物件。](#group-es2023)

- [`groupToMap()`：和 `group()` 類似，但回傳 `Map` 物件，更適合需要鍵值為非字串的情境。](#grouptomap-es2023)

- [`delete` 運算符：刪除陣列中的某個元素，但不會改變陣列的長度，會留下 `empty`。](#delete-運算符)

<br />

## `length` property (`length` 屬性)

獲取陣列長度。

```javascript
const arr = [1, 2, 3];

console.log(arr.length); // 3
```

<br />

## `push()`

將元素添加到陣列的末尾。

```javascript
const arr = [1, 2, 3];
arr.push(5);

console.log(arr); // [1, 2, 3, 5]
```

<br />

## `pop()`

移除並返回陣列的最後一個元素。

```javascript
const arr = [1, 2, 3];
const last = arr.pop();

console.log(last); // 3
console.log(arr);  // [1, 2]
```

<br />

## `shift()`

移除並返回陣列的第一個元素。

```javascript
const arr = [1, 2, 3];
const first = arr.shift();

console.log(first); // 1
console.log(arr);   // [2, 3]
```

<br />

## `unshift()`

將元素添加到陣列的開頭。

```javascript
const arr = [2, 3];
arr.unshift(1);

console.log(arr); // [1, 2, 3]
```

<br />

## `splice()`

添加、移除或替換陣列中的元素。

```javascript
array.splice(start, deleteCount, item1, item2, ...)
```

- `start`：開始操作的索引位置。

- `deleteCount`：要移除的元素數量 (可以為 0，若只想添加元素)。

- `item1, item2, ...`：要添加到陣列中的新元素 (可選)。

```javascript
const arr = [1, 2, 3, 4, 5];

/** 添加：不移除任何元素 */
arr.splice(2, 0, 'x', 'y');
console.log(arr); // [1, 2, 'x', 'y', 3, 4, 5]

/** 移除：移除 2 個元素 */
arr.splice(1, 2);
console.log(arr); // [1, 'y', 3, 4, 5]

/** 替換：移除 1 個元素並添加新元素 */
arr.splice(2, 1, 'z');
console.log(arr); // [1, 'y', 'z', 4, 5]
```

<br />

## `fill()`

用靜態值填充陣列中的元素。

```javascript
const arr = [1, 2, 3];
arr.fill(0);

console.log(arr); // [0, 0, 0]
```

<br />

## `reverse()`

反轉陣列中元素的順序。

```javascript
const arr = [1, 2, 3];
arr.reverse();

console.log(arr); // [3, 2, 1]
```

<br />

## `sort()`

對陣列中的元素進行排序。

```javascript
const arr = [3, 1, 2];
arr.sort();

console.log(arr); // [1, 2, 3]
```

<br />

## `copyWithin()`

在陣列內部複製元素到其他位置 (會修改原陣列)。

```javascript
const arr = [1, 2, 3, 4, 5];
arr.copyWithin(0, 3, 5);

console.log(arr); // [4, 5, 3, 4, 5]
```

<br />

## `slice()`

返回一個新的陣列，包含從開始索引到結束索引 (不包含結束索引) 的部分元素。

```javascript
const arr = [1, 2, 3, 4];
const newArr = arr.slice(1, 3);

console.log(newArr); // [2, 3]
```

<br />

## `concat()`

合併數個陣列，返回一個新陣列。

```javascript
const arr1 = [1, 2];
const arr2 = [3, 4];
const arr = arr1.concat(arr2);

console.log(arr); // [1, 2, 3, 4]
```

<br />

## `flat()`

將多維陣列展平成一維陣列。

```javascript
const arr = [1, [2, 3], [4, [5]]];
const flatArr = arr.flat(2);

console.log(flatArr); // [1, 2, 3, 4, 5]
```

<br />

## `flatMap()`

先對陣列進行 `map()` 操作，再將結果展平成一維陣列。

```javascript
const arr = [1, 2, 3];
const flatMappedArr = arr.flatMap(x => [x, x * 2]);

console.log(flatMappedArr); // [1, 2, 2, 4, 3, 6]
```

<br />

## `toSorted()` (ES2023)

返回一個已排序的新陣列，不改變原本的陣列。

```javascript
const arr = [3, 1, 4, 2];
const sorted = arr.toSorted((a, b) => a - b);

console.log(sorted); // [1, 2, 3, 4]
console.log(arr);    // [3, 1, 4, 2](原陣列不變)
```

<br />

## `toReversed()` (ES2023)

返回一個倒序的新陣列，不改變原本的陣列。

```javascript
const arr = [1, 2, 3];
const reversed = arr.toReversed();

console.log(reversed); // [3, 2, 1]
console.log(arr);      // [1, 2, 3](原陣列不變)
```

<br />

## `toSpliced()` (ES2023)

返回一個已修改的新陣列，用法類似 `splice()`，但不改變原本的陣列。

```javascript
const arr = [1, 2, 3, 4];
const newArr = arr.toSpliced(1, 2, 9, 10);

console.log(newArr); // [1, 9, 10, 4]
console.log(arr);    // [1, 2, 3, 4](原陣列不變)
```

<br />

## `with()` (ES2023)

返回一個指定索引值被替換的新陣列，不改變原本的陣列。

```javascript
const arr = [1, 2, 3];
const newArr = arr.with(1, 9);

console.log(newArr); // [1, 9, 3]
console.log(arr);    // [1, 2, 3](原陣列不變)
```

<br />

## `toString()`

將陣列轉換為字串，元素之間以逗號分隔。

```javascript
const arr = [1, 2, 3];
const str = arr.toString();

console.log(str); // 1,2,3
```

<br />

## `join()`

將陣列轉換為字串，可以指定分隔符號。

```javascript
const arr = [1, 2, 3];
const str = arr.join('-');

console.log(str); // 1-2-3
```

<br />

## `forEach()`

為陣列中的每個元素執行一次提供的函式。

```javascript
const arr = [1, 2, 3];
arr.forEach(element => {
  console.log(element);
});
```

執行結果：

```console
1
2
3
```

<br />

## `map()`

創建一個新陣列，其元素是調用函式處理每個元素後的結果。

```javascript
const arr = [1, 2, 3];
const newArr = arr.map(x => x * 2);

console.log(newArr); // [2, 4, 6]
```

<br />

## `filter()`

創建一個新陣列，其結果是滿足條件的所有元素。

```javascript
const arr = [1, 2, 3, 4];
const filteredArr = arr.filter(x => x > 2);

console.log(filteredArr); // [3, 4]
```

<br />

## `reduce()`

將陣列中的每個元素依次累積，最終為單一值。

```javascript
const arr = [1, 2, 3, 4];
const sum = arr.reduce((acc, curr) => acc + curr, 0);

console.log(sum); // 10
```

<br />

## `reduceRight()`

從右到左對陣列中的元素進行累積，最終為單一值。

```javascript
const arr = [1, 2, 3, 4];
const product = arr.reduceRight((acc, curr) => acc * curr, 1);

console.log(product); // 24
```

<br />

## `includes()`

判斷陣列是否包含某個值，返回布林值。

```javascript
const arr = [1, 2, 3];

console.log(arr.includes(2)); // true
console.log(arr.includes(4)); // false
```

<br />

## `indexOf()`

返回指定元素在陣列中的第一個索引，若沒有找到則返回 `-1`。

```javascript
const arr = [1, 2, 3, 2];

console.log(arr.indexOf(2)); // 1
console.log(arr.indexOf(4)); // -1
```

<br />

## `lastIndexOf()`

返回指定元素在陣列中的最後一個索引，若沒有找到則返回 `-1`。

```javascript
const arr = [1, 2, 3, 2];

console.log(arr.lastIndexOf(2)); // 3
console.log(arr.lastIndexOf(4)); // -1
```

<br />

## `find()`

返回符合條件的第一個元素，否則返回 `undefined`。

```javascript
const arr = [1, 2, 3, 4];
const found = arr.find(x => x > 2);

console.log(found); // 3
```

<br />

## `findIndex()`

返回符合條件的第一個元素的索引，否則返回 `-1`。

```javascript
const arr = [1, 2, 3, 4];
const index = arr.findIndex(x => x > 2);

console.log(index); // 2
```

<br />

## `some()`

判斷陣列中是否至少有一個元素滿足條件，返回布林值。

```javascript
const arr = [1, 2, 3];
const hasEven = arr.some(x => x % 2 === 0);

console.log(hasEven); // true
```

<br />

## `every()`

判斷陣列中的所有元素是否都滿足條件，返回布林值。

```javascript
const arr = [1, 2, 3];
const allPositive = arr.every(x => x > 0);

console.log(allPositive); // true
```

<br />

## `entries()`

返回一個新的陣列迭代器物件，包含鍵值對 (Key-value Pairs)。

```javascript
const arr = ['a', 'b', 'c'];
const iterator = arr.entries();
for (let [index, value] of iterator) {
  console.log(index, value);
}
```

執行結果：

```console
0 'a'
0 'a'
2 'c'
```

<br />

## `keys()`

返回一個新的陣列迭代器物件，包含每個索引。

```javascript
const arr = ['a', 'b', 'c'];
const iterator = arr.keys();
for (let key of iterator) {
  console.log(key);
}
```

執行結果：

```console
0
1
2
```

<br />

## `values()`

回傳一個陣列值 (values) 的迭代器，可用 `for...of` 取出每個值。

```javascript
const arr = ['a', 'b', 'c'];
const iterator = arr.values();

for (const value of iterator) {
  console.log(value);
}
```

執行結果：

```console
a
b
c
```

<br />

## `from()`

將類陣列物件或可迭代物件轉換為陣列。

```javascript
const str = 'Hello';
const arr = Array.from(str);

console.log(arr); // ['H', 'e', 'l', 'l', 'o']
```

<br />

## `isArray()`

檢查給定的值是否為陣列，返回布林值。

```javascript
console.log(Array.isArray([1, 2, 3])); // true
console.log(Array.isArray('Hello'));   // false
```

<br />

## `valueOf()`

返回陣列的原始值 (通常與陣列本身相同)。

```javascript
const arr = [1, 2, 3];

console.log(arr.valueOf()); // [1, 2, 3]
```

<br />

## `at()` (ES2022)

取得指定索引的值 (支援負索引，從陣列尾端開始算)。

```javascript
const arr = [10, 20, 30, 40];

console.log(arr.at(1));  // 20
console.log(arr.at(-1)); // 40 (最後一個元素)
```

<br />

## `group()` (ES2023)

根據 Callback Function 的回傳值分組陣列元素，回傳一個物件 (Object)。

```javascript
const arr = [1, 2, 3, 4, 5];
const grouped = arr.group(num => num % 2 === 0 ? 'even' : 'odd');

console.log(grouped); // { odd: [1, 3, 5], even: [2, 4] }
```

<br />

## `groupToMap()` (ES2023)

和 `group()` 類似，但回傳 `Map` 物件，更適合需要鍵值為非字串的情境。

```javascript
const arr = [1, 2, 3, 4, 5];
const groupedMap = arr.groupToMap(num => num % 2 === 0 ? 'even' : 'odd');

console.log(groupedMap); // Map(2) { 'odd' => [1, 3, 5], 'even' => [2, 4] }
```

<br />

## `delete` 運算符

刪除陣列中的某個元素，但不會改變陣列的長度，會留下 `empty`。

```javascript
const arr = [1, 2, 3];
delete arr[1];

console.log(arr); // [1, empty, 3]
```
