# Math 的詳細處理方法

以下整理了 JavaScript 中 Math 的詳細處理方法。

- [`Math.random()`：返回一個 0 到 1 之間的隨機數，不包含 1](#mathrandom)

- [`Math.round(x)`：將數字四捨五入到最接近的整數](#mathroundx)

- [`Math.floor(x)`：將數字向下取整數，也就是取最接近的、比該數字小的整數](#mathfloorx)

- [`Math.ceil(x)`：將數字向上取整數，也就是取最接近的、比該數字大的整數](#mathceilx)

- [`Math.trunc(x)`：去除數字的小數部分，僅返回整數部分](#mathtruncx)

- [`Math.abs(x)`：返回一個數的絕對值，也就是該數在數線上距離零的距離，無論是正數還是負數](#mathabsx)

- [`Math.sign(x)`：返回一個數字的符號，若是正數返回 1，負數返回 -1，0 返回 0](#mathsignx)

- [`Math.max(...values)`：返回一組數字中的最大值](#mathmaxvalues)

- [`Math.min(...values)`：返回一組數字中的最小值](#mathminvalues)

- [`Math.pow(base, exponent)`：計算 `base` 的 `exponent` 次方，也就是 `base` 的冪次](#mathpowbase-exponent)

- [`Math.sqrt(x)`：計算數字的平方根](#mathsqrtx)

- [`Math.cbrt(x)`：計算數字的立方根](#mathcbrtx)

- [`Math.log(x)`：計算數字的自然對數 (以 e 為底)](#mathlogx)

- [`Math.log10(x)`：計算數字的以 10 為底的對數](#mathlog10x)

- [`Math.log2(x)`：計算數字的以 2 為底的對數](#mathlog2x)

- [`Math.exp(x)`：計算 e 的 `x` 次方](#mathexpx)

- [`Math.sin(x)`：計算數字 (以弧度表示) 的正弦值](#mathsinx)

- [`Math.cos(x)`：計算數字 (以弧度表示) 的餘弦值](#mathcosx)

- [`Math.tan(x)`：計算數字 (以弧度表示) 的正切值](#mathtanx)

- [`Math.asin(x)`：計算數字的反正弦值，結果以弧度表示，輸入的值必須在 -1 到 1 之間](#mathasinx)

- [`Math.acos(x)`：計算數字的反餘弦值，結果以弧度表示，輸入的值必須在 -1 到 1 之間](#mathacosx)

- [`Math.atan(x)`：計算數字的反正切值，結果以弧度表示](#mathatanx)

- [`Math.atan2(y, x)`：計算 `y`/`x` 的反正切值，返回的值以弧度表示](#mathatan2y-x)

- [`Math.hypot(...values)`：計算一組數字的平方和的平方根](#mathhypotvalues)

- [`Math.clz32(x)`：計算 32 位元無符號整數的前導零的數量](#mathclz32x)

- [`Math.imul(a, b)`：進行 32 位元整數相乘，返回結果的低 32 位](#mathimula-b)

- [`Math.fround(x)`：返回最接近的 32 位元單精度浮點數表示](#mathfroundx)

- [`Math.expm1(x)`：計算 e<sup>x</sup> - 1 的值，精度比 `Math.exp(x)` - 1 更高](#mathexpm1x)

- [`Math.log1p(x)`：計算 1 + x 的自然對數，對於 x 接近 0 的值更精確](#mathlog1px)

<br />

## `Math.random()`

`Math.random()` 是 JavaScript 提供的一個內建方法，用來生成一個介於 0 (包含) 到 1 (不包含) 之間的隨機小數。

這個隨機小數通常用來處理一些需要隨機性質的需求，例如：遊戲中的隨機事件、隨機顏色生成、或是從資料中隨機選取某個項目等。

### 基本語法

```javascript
let randomNumber = Math.random();
```

這段程式碼會將 `Math.random()` 產生的隨機數字賦值給變數 `randomNumber`，該隨機數會是一個介於 0 到 1 之間 (開區間) 的浮點數，例如：0.834、0.527 之類的數值。

### 詳細說明

- 應用場景

    - 隨機數字生成

        若想生成一個指定範圍的隨機數，物做法是將隨機數乘以一個範圍，然後進行取整數。

        ```javascript
    	/** 生成 0 到 9 之間的隨機整數 */
    	let randomInt = Math.floor(Math.random() * 10);
    	```

        上面的範例中，`Math.random()` 生成的數字被乘以 10，使結果範圍變成 0 (包含) 到 10 (不包含)。`Math.floor(x)` 用來將浮點數取整數，最終結果是一個 0 到 9 之間的隨機整數。

    - 隨機抽取陣列中的元素

        常用於從一個陣列中隨機選取一個元素

    	```javascript
    	let items = ['aaa', 'bbb', 'ccc'];
    	let randomItem = items[Math.floor(Math.random() * items.length)];
    	console.log(randomItem); // 可能是 "aaa", "bbb" 或 "ccc"
    	```

    - 生成不同範圍的隨機數

        若想生成一個指定範圍的隨機數字 (例如：5 到 15 之間的數字)，可以使用以下方法

    	```javascript
    	function getRandom(min, max) {
    	  return Math.random() * (max - min) + min;
    	}

    	console.log(getRandom(5, 15)); // 生成 5 到 15 之間的隨機數 (不含 15)
    	```

    - 生成隨機整數

        若想在某個範圍內生成整數 (例如：1 到 100)，可以使用下列方法

    	```javascript
    	function getRandomInt(min, max) {
    	  return Math.floor(Math.random() * (max - min + 1)) + min;
    	}

        console.log(getRandomInt(1, 100)); // 生成 1 到 100 之間的隨機整數 (包含 1 和 100)
        ```

-  注意事項

    - 隨機性與可預測性

        `Math.random()` 的隨機性在大多數應用情況下已經足夠，但若需要更高等級的隨機性 (例如：加密、金融交易等領域)，這種隨機數生成方式可能不夠安全，因為 `Math.random()` 是偽隨機數生成器 (Pseudo-Random Number Generator, 簡稱：PRNG)。也就是說，`Math.random()` 是基於一個演算法，雖然看起來隨機，但其實可以預測。

### 常見問題

- 為什麼不能生成 1

    因為 `Math.random()` 的設計原理，所以生成的隨機數總是介於 0 (包含) 到 1 (不包含) 之間。

    這樣的設計確保了無論在什麼情況下，生成的數字永遠不會達到上界 (1)，這在很多情況中可以避免邊界問題。

- 如何生成帶有小數點的隨機數

    `Math.random()` 生成的數字本來就是浮點數，但若想控制小數點後的位數，可以使用 `toFixed()` 方法

    ```javascript
    let randomNum = (Math.random() * 100).toFixed(2);
    console.log(randomNum); // 生成一個有兩位小數的隨機數，例如：43.70
    ```

### 總結

`Math.random()` 是一個非常常用的工具，無論是用來生成隨機整數、浮點數，還是用來從陣列中隨機選取元素，都有廣泛的應用。

雖然 `Math.random()` 的隨機性在一般情況下蠻夠用的，但是在一些需要高安全性的情況可能會有所限制。

<br />

## `Math.round(x)`

`Math.round(x)` 是 JavaScript 中用來四捨五入數字的內建方法，會根據小數點後的數字來決定向上或向下取整數或直接等於該數。

### 基本語法

```javascript
Math.round(x);
```

- `x`：要進行四捨五入的數字。

### 詳細說明

- 四捨五入的規則

    當小數部分小於 0.5 時，會將數字向下取整數，即捨去小數部分。

    當小數部分大於或等於 0.5 時，會將數字向上取整數，即將整數部分加 1。

- 範例

    - 當 `x` 是正數

    	```javascript
    	console.log(Math.round(4.3)); // 4
		console.log(Math.round(4.7)); // 5
		console.log(Math.round(5.5)); // 6
    	```

        在 `Math.round(4.3)` 中，小數點後的 0.3 小於 0.5，會向下取整數為 4。

        在 `Math.round(4.7)` 中，小數點後的 0.7 大於 0.5，會向上取整數為 5。

        在 `Math.round(5.5)` 中，小數點後正好是 0.5，所以會向上取整數為 6。

    - 當 `x` 是負數

        ```javascript
        console.log(Math.round(-4.3)); // -4
		console.log(Math.round(-4.7)); // -5
		console.log(Math.round(-5.5)); // -5
        ```

        在 `Math.round(-4.3)` 中，小數點後的 0.3 小於 0.5，向下取整數為 -4 (更接近 -4 而不是 -5)。

        在 `Math.round(-4.7)` 中，小數點後的 0.7 大於 0.5，向上取整為 -5 (更接近 -5 而不是 -4)。

        在 `Math.round(-5.5)` 中，小數點後是 0.5，結果是 -5 (JavaScript 對負數四捨五入時遵循的是向 0 方向取整數)。

- 應用場景

    - 顯示數值

        `Math.round(x)` 常用在一些需要對顯示的數字進行簡單處理。

        例如：當希望將計算結果四捨五入到最接近的整數

        ```javascript
        let price = 4.56;
        console.log(Math.round(price)); // 5
        ```

    - 計算平均值

        例如：計算多個數字的平均值時，使用 `Math.round(x)` 來四捨五入平均值

        ```javascript
        let avg = (3.5 + 4.8 + 5.1) / 3;
        console.log(Math.round(avg)); // 4
        ```

- 與其他取整數方法的差異

    - `Math.round(x)`：將數字四捨五入，依據小數點後的數值來決定向上或向下取整數。

    - `Math.floor(x)`：將數字向下取整數，不論小數是多少，結果永遠是最接近的較小整數。

    - `Math.ceil(x)`：將數字向上取整數，不論小數是多少，結果永遠是最接近的較大整數。

    - `Math.trunc(x)`：直接捨棄小數部分，不進行四捨五入。

    範例對比

    ```javascript
    console.log(Math.round(4.5)); // 5
    console.log(Math.floor(4.5)); // 4
    console.log(Math.ceil(4.5));  // 5
    console.log(Math.trunc(4.5)); // 4
    ```

### 常見誤區

- 四捨五入負數：有些人可能會誤以為負數的四捨五入與正數相同，但其實在負數的情況下，JavaScript 的四捨五入是向 0 靠攏的。也就是說，`Math.round(-5.5)` 結果是 -5，而不是 -6。

### 總結

`Math.round(x)` 是一個非常常用的四捨五入方法，能夠依據小數部分自動決定向上或向下取整數，無論是正數還是負數都能夠準確返回最接近的整數。

與 `Math.floor(x)` 和 `Math.ceil(x)` 等取整數方法相比，`Math.round(x)` 更具靈活性，特別適合需要進行四捨五入的情境。

<br />

## `Math.floor(x)`

`Math.floor(x)` 是 JavaScript 中用來將數字向下取整數的內建方法，也就是將數字「無條件捨去小數部分」，返回比原數字小或相等的整數。

### 基本語法

```javascript
Math.floor(x);
```

- `x`：要進行向下取整數的數字。

### 詳細說明

- 向下取整數的規則

    不論小數部分是多少，只要存在小數，`Math.floor(x)` 都會將數字向負無窮大到取整數。

    若 `x` 本身已經是整數，結果就會是該數字本身，不會進行任何變化。

    - 若 `x` 是正數，`Math.floor(x)` 的效果類似於「無條件捨去」。

    - 若 `x` 是負數，會返回比 `x` 更小的整數。

- 範例

    - 當 `x` 是正數

		```javascript
		console.log(Math.floor(4.7)); // 4
		console.log(Math.floor(9.1)); // 9
		```

        `Math.floor(4.7)` 將小數點後的 0.7 移除，向下取整數為 4。

        `Math.floor(9.1)` 將小數點後的 0.1 移除，向下取整數為 9。

    - 當 `x` 是負數

		```javascript
		console.log(Math.floor(-3.7)); // -4
		console.log(Math.floor(-2.1)); // -3
		```

        `Math.floor(-3.7)` 將小數點後的 0.7 移除，向下取整數為 -4 (不是 -3，因為 -4 是小於 -3.7 的最大整數)。

        `Math.floor(-2.1)` 將小數點後的 0.1 移除，向下取整數為 -3。

- 應用場景

    - 隨機數生成

        `Math.floor(x)` 常與 `Math.random()` 搭配使用，用來生成一個範圍內的隨機整數。

        例如：生成 0 到 9 之間的隨機整數

        ```javascript
        let randomInt = Math.floor(Math.random() * 10);
        console.log(randomInt); // 結果可能是 0 到 9 之間的隨機整數
        ```

- 與其他取整數方法的差異

    - `Math.round(x)`：將數字四捨五入，依據小數點後的數值來決定向上或向下取整數。

    - `Math.floor(x)`：將數字向下取整數，不論小數是多少，結果永遠是最接近的較小整數。

    - `Math.ceil(x)`：將數字向上取整數，不論小數是多少，結果永遠是最接近的較大整數。

    - `Math.trunc(x)`：直接捨棄小數部分，不進行四捨五入。

    範例對比

    ```javascript
    console.log(Math.round(4.5)); // 5
    console.log(Math.floor(4.5)); // 4
    console.log(Math.ceil(4.5));  // 5
    console.log(Math.trunc(4.5)); // 4
    ```

### 常見誤區

- 負數的處理：有些人可能會誤以為 `Math.floor(x)` 對負數會「無條件捨去」，但其實是向負無窮大取整數。

### 總結

`Math.floor(x)` 的主要功能是將數字向下取整數，適用於很多需要處理整數的情境，例如：隨機數生成、分頁計算等。

與 `Math.ceil(x)` 和 `Math.round(x)` 相比，`Math.floor(x)` 更加注重數值的向下捨去。

<br />

## `Math.ceil(x)`

`Math.ceil(x)` 是 JavaScript 中用來將數字向上取整的內建方法，也就是將數字「無條件捨去小數部分」，返回比原數字大的最小整數或相等的整數。

### 基本語法

```javascript
Math.ceil(x);
```

- `x`：是要進行向上取整數的數字。

### 詳細說明

- 向上取整的規則

    不論小數部分是多少，只要存在小數，`Math.ceil(x)` 都會將數字向無窮大到取整數。

    若 `x` 本身已經是整數，結果就會是該數字本身，不會進行任何變化。

- 範例

    - 當 `x` 是正數

		```javascript
		console.log(Math.ceil(4.3)); // 5
		console.log(Math.ceil(4.7)); // 5
		```

        `Math.ceil(4.3)` 將小數點後的 0.3 移除，向上取整數為 5。

        `Math.ceil(4.7)` 將小數點後的 0.7 移除，向上取整數為 5。

    - 當 `x` 是負數

		```javascript
		console.log(Math.ceil(-4.3)); // -4
		console.log(Math.ceil(-4.7)); // -4
		```

        `Math.ceil(-4.3)` 將小數點後的 0.3 移除，向上取整數為 -4。

        `Math.ceil(-4.7)` 將小數點後的 0.7 移除，向上取整數為 -4。

- 應用場景

    - 計算需要的最小數量

        `Math.ceil(x)` 常用在需要確保結果至少是某個整數的時候。

        例如：假設有 53 個項目，每個盒子可以裝 10 個項目，需要多少個盒子才能裝完所有項目

        ```javascript
        let totalItems = 53;
		let itemsPerBox = 10;
		let boxesNeeded = Math.ceil(totalItems / itemsPerBox);
		console.log(boxesNeeded); // 6
        ```

        在這個範例中，雖然 53 除以 10 等於 5.3，但必須向上取整數以確保有足夠的盒子來裝所有項目。

    - 處理時間進位

        例如：假設需要將時間從分鐘轉換為小時並進行進位，使用 `Math.ceil(x)` 確保不會丟失時間

        ```javascript
        let minutes = 130;
		let hours = Math.ceil(minutes / 60);
		console.log(hours); // 3
        ```

        在這個範例中，30 分鐘約等於 2.17 小時，但因為還有多出的 0.17 小時，結果被向上取整數為 3 小時。

    - 分頁功能

        例如：當處理分頁顯示資料時，可能需要計算總頁數。

		```javascript
		let totalItems = 53;
		let itemsPerPage = 10;

		/** 用 ceil 確保不足一頁也會算一頁 */
		let totalPages = Math.ceil(totalItems / itemsPerPage);

		console.log(totalPages); // 6
		```

        在這個範例中，前 5 頁各放 10 筆資料，第 6 頁放剩下的 3 筆資料，所以在計算分頁總數時可以使用向上取整數。

- 與其他取整數方法的差異

    - `Math.round(x)`：將數字四捨五入，依據小數點後的數值來決定向上或向下取整數。

    - `Math.floor(x)`：將數字向下取整數，不論小數是多少，結果永遠是最接近的較小整數。

    - `Math.ceil(x)`：將數字向上取整數，不論小數是多少，結果永遠是最接近的較大整數。

    - `Math.trunc(x)`：直接捨棄小數部分，不進行四捨五入。

    範例對比

    ```javascript
    console.log(Math.round(4.5)); // 5
    console.log(Math.floor(4.5)); // 4
    console.log(Math.ceil(4.5));  // 5
    console.log(Math.trunc(4.5)); // 4
    ```

### 常見誤區

- 負數的向上取整數：有些人可能會誤以為 `Math.ceil(x)` 對負數也是簡單的「無條件捨去」，但其實是會將負數向無窮大取整數。因此，`Math.ceil(-4.7)` 的結果是 -4，而不是 -5。

### 總結

`Math.ceil(x)` 是用來將數字向上取整數的工具，無論小數部分是多小，只要不是整數，結果都會進位到下一個整數。

`Math.ceil(x)` 的應用範圍很廣，尤其在處理需要進位或確保整數結果的情況。

與 `Math.floor(x)` 和 `Math.round(x)` 等取整數方法相比，`Math.ceil(x)` 的最大特點就是永遠向上取整數，特別是在負數的情況下，能夠精準進行向上取整數。

<br />

## `Math.trunc(x)`

`Math.trunc(x)` 是 JavaScript 中用來去掉數字的小數部分，並只保留整數部分的內建方法。

簡單來說，`Math.trunc(x)` 的作用是直接截取數字小數點之前的整數，不進行任何四捨五入或取整數操作。

### 基本語法

```javascript
Math.trunc(x);
```

- `x`：是要進行截取小數的數字。

### 詳細說明

- 截取小數部分的規則

    `Math.trunc(x)` 會直接捨去小數部分，不管小數是正數還是負數。

    若 `x` 是整數，那結果就是 `x` 本身，沒有任何變化。

- 範例

    - 當 `x` 是正數

    	```javascript
		console.log(Math.trunc(4.9)); // 4
		console.log(Math.trunc(4.1)); // 4
		console.log(Math.trunc(5.0)); // 5
    	```

    - 當 `x` 是負數

        ```javascript
		console.log(Math.trunc(-4.9)); // -4
		console.log(Math.trunc(-4.1)); // -4
		console.log(Math.trunc(-5.0)); // -5
        ```

- 應用場景

    - 截取整數部分

        `Math.trunc(x)` 在需要忽略數字的小數只保留整數時是最直接的方法

    	```javascript
    	let price = 9.99;
		let integerPrice = Math.trunc(price);
		console.log(integerPrice); // 9
    	```

- 與其他取整數方法的差異

    - `Math.round(x)`：將數字四捨五入，依據小數點後的數值來決定向上或向下取整數。

    - `Math.floor(x)`：將數字向下取整數，不論小數是多少，結果永遠是最接近的較小整數。

    - `Math.ceil(x)`：將數字向上取整數，不論小數是多少，結果永遠是最接近的較大整數。

    - `Math.trunc(x)`：直接捨棄小數部分，不進行四捨五入。

    範例對比

    ```javascript
    console.log(Math.round(4.5)); // 5
    console.log(Math.floor(4.5)); // 4
    console.log(Math.ceil(4.5));  // 5
    console.log(Math.trunc(4.5)); // 4
    ```

### 常見誤區

- `Math.trunc(x)` 不會四捨五入：有些人可能會誤以為 `Math.trunc(x)` 會進行某種取整數操作，實際上只是簡單捨去小數部分，而不是根據數字的大小進行向上或向下取整數。

- 負數處理：與 `Math.floor()` 相比，`Math.trunc(x)` 不會將負數向負無窮大方向取整數，而是簡單捨去負數的小數部分。因此，`Math.trunc(-4.7)` 的結果是 -4，而不是 -5。

### 總結

`Math.trunc(x)` 是用來去掉數字小數部分用工具，不進行任何四捨五入或取整數，只是單純截取整數部分。

無論是正數還是負數，都會直接捨去小數點後的數字。

<br />

## `Math.abs(x)`

`Math.abs(x)` 是 JavaScript 中用來取得數字絕對值的內建方法，絕對值就是指不帶正負號的數值。

無論 `x` 是正數還是負數，`Math.abs(x)` 會返回這個數字的非負數。

### 基本語法

```javascript
Math.abs(x);
```

- `x`：想要取得絕對值的數字。

### 詳細說明

- 什麼是絕對值

    絕對值是數字與 0 之間的距離，不考慮方向。因此，無論數字是正數還是負數，結果都是非負數。

    對於任何一個正數或負數 `x`，`Math.abs(x)` 都會將其轉換為正數。

    - `Math.abs(5)` 結果是 5。

    - `Math.abs(-5)` 結果也是 5。

- 範例

    - 當 `x` 是正數

    	```javascript
		console.log(Math.abs(4));   // 4
		console.log(Math.abs(7.5)); // 7.5
    	```

    - 當 `x` 是負數

        ```javascript
		console.log(Math.abs(-4));   // 4
		console.log(Math.abs(-7.5)); // 7.5
        ```

    - 當 `x` 是 0

        ```javascript
        console.log(Math.abs(0)); // 0
        ```

        0 的絕對值還是 0，因為 0 本身就是沒有正負的數值。

    - 當 `x` 是 `NaN`

        ```javascript
        console.log(Math.abs(NaN)); // NaN
        ```
- 應用場景

    - 計算兩個數字的差距

        絕對值常被用在需要計算兩個數字之間的距離。這樣無論順序如何，結果都能表示兩個數字的距離

        ```javascript
        let a = 10;
		let b = 4;
		let difference = Math.abs(a - b);
		console.log(difference); // 6
        ```

        以上範例中，不論是 `a - b` 還是 `b - a`，`Math.abs(x)` 保證結果總是正數，表示兩個數字之間的距離。

    - 在物理或運動中的應用

        絕對值常用於表示實際距離或大小。

        例如：速度、距離等不應該有負數的情境

        ```javascript
        let velocity = -20;
		let speed = Math.abs(velocity);
		console.log(speed); // 20
        ```

        以上範例中，速度的值被轉換為正值，因為速度不應該是負數。

    - 取代條件判斷

        當只關心數字的大小，不在意正負號時，使用 `Math.abs(x)` 可以省去額外的條件判斷。

        例如：判斷一個數字是否超過某個範圍

        ```javascript
        let number = -12;
        if (Math.abs(number) > 10) {
          console.log('超過範圍');
        }
        ```

        以上範例中，不論 `number` 是正數還是負數，只要其絕對值超過 10，都會觸發條件。

- 與其他 Math method 的關聯

    - 與 `Math.sign(x)` 結合使用時，`Math.abs(x)` 可以幫助將數字的符號和大小分離

    	```javascript
    	let num = -9.5;
    	console.log(Math.sign(num) * Math.abs(num)); // -9.5
        ```

        以上範例，可以理解為先取絕對值，再根據原來的符號進行修正。

### 常見誤區

- 絕對值不適用於非數字

    `Math.abs(x)` 只對數字有效，對於其他類型的變數 (例如：字串或物件)，會返回 `NaN`

    ```javascript
    console.log(Math.abs("hello")); // NaN
    ```

### 總結

`Math.abs(x)` 是一個用來取得數字絕對值的簡單工具，會將任何正數或負數轉換為非負數，非常適合用於計算數字之間的差距或處理實際物理量。

`Math.abs(x)` 不會影響數字的小數部分，也不會對 NaN 或非數值資料進行處理。

<br />

## `Math.sign(x)`

`Math.sign(x)` 是 JavaScript 中用來判斷一個數字符號的內建方法，會根據傳入數字不同而返回相對應的結果，具體可以分為以下五種

- 正數 -> `1`

- 負數 -> `-1`

- 正 0 -> `+0`

- 負 0 -> `-0`

- `NaN` -> `NaN`

### 基本語法

```javascript
Math.sign(x);
```

- `x`：想要判斷符號的數字。

### 詳細說明

- 符號判斷的規則

    `Math.sign(x)` 根據數字的符號來返回對應的結果，不改變數字本身的大小或精度，主要是用來快速判斷一個數字是正數還是負數，或是否為 0。

    `Math.sign(x)` 對 `+0` 和 `-0` 做了區分。

- 範例

    - 當 `x` 是正數

		```javascript
		console.log(Math.sign(5));     // 1
		console.log(Math.sign(3.2));   // 1
		console.log(Math.sign('123')); // 1
		```

        正數的符號為 `1`，不論是整數還是小數。

    - 當 x 是負數

		```javascript
		console.log(Math.sign(-5));     // -1
		console.log(Math.sign(-3.2));   // -1
		console.log(Math.sign('-123')); // -1
		```

        負數的符號為 `-1`，不論負數是整數還是小數。

    - 當 `x` 是 `0` 或 `-0`

        ```javascript
        console.log(Math.sign(0));    // 0
        console.log(Math.sign('0'));  // 0
        console.log(Math.sign(-0));   // -0
        console.log(Math.sign('-0')); // -0
        ```

        雖然 `+0` 和 `-0` 看起來相同，但 `Math.sign(x)` 會進行區分。在大多數情況下，`+0` 和 `-0` 的行為幾乎一致，但在某些運算 (例如：除法) 中可能會產生不同的結果。

    - 當 `x` 是 `NaN`

        ```javascript
        console.log(Math.sign(NaN));   // NaN
        console.log(Math.sign('aaa')); // NaN
        ```

- 應用場景

    - 快速判斷數字的符號

        `Math.sign(x)` 常用在需要知道一個數字是正數、負數還是 0 的時候

        ```javascript
        let num = -8;
        if (Math.sign(num) === 1) {
          console.log('這是正數');
        } else if (Math.sign(num) === -1) {
          console.log('這是負數');
        } else {
          console.log('這是 0');
        }
        ```

    - 配合絕對值進行運算

        與 `Math.abs(x)` 一起使用時，可以將一個數字的符號與大小分離

        ```javascript
		let num = -9.5;
		let sign = Math.sign(num);
		let absValue = Math.abs(num);
		console.log(sign * absValue); // -9.5
        ```

        以上方法可以在保留原始符號的情況下，進行其他計算。

### 常見誤區

- 對非數字的處理

    若傳入的是非數值類型，`Math.sign(x)` 會返回 `NaN`，因此需要注意確保傳入的值是數字

    ```javascript
    console.log(Math.sign("text")); // NaN
    ```

### 總結

`Math.sign(x)` 是用來判斷數字符號的實用方法，返回的結果可以幫助快速了解數字是正數、負數還是 0，並且還能區分 `+0` 和 `-0`。

`Math.sign(x)` 的應用範圍廣泛，特別是在需要根據數字符號進行條件判斷時，非常方便。與 `Math.abs(x)` 結合使用時，也能靈活處理數字的大小和符號分離操作。

<br />

## `Math.max(...values)`

`Math.max(...values)` 是 JavaScript 中用來找出一組數字中最大值的內建方法，接受多個數值作為參數，並返回其中最大的那個數字。

若沒有任何參數，則返回 `-Infinity`，表示在空集合中沒有最大值。若傳入的參數包含 `NaN`，則返回 `NaN`。

### 基本語法

```javascript
Math.max(value1, value2, ..., valueN);
```

- `value1, value2, ..., valueN`：要比較的數字。

### 詳細說明

- 多個數值比較

    `Math.max(...values)` 可以接受任意數量的數值，並從中找出最大的數。當傳入多個參數時會逐一比較，並返回其中最大的數字。

- 範例

    - 多個正數

        ```javascript
        console.log(Math.max(1, 3, 5, 7, 9)); // 9
        ```

    - 多個負數

        ```javascript
        console.log(Math.max(-3, -7, -10)); // -3
        ```

    - 混合正數與負數

        ```javascript
        console.log(Math.max(-1, -5, 10, 0, 8)); // 10
        ```

    - 無參數的情況

        ```javascript
        console.log(Math.max()); // -Infinity
        ```

    - NaN 的情況

        ```javascript
        console.log(Math.max(1, 2, NaN, 4)); // NaN
        ```

- 應用場景

    - 比較一組數字的大小

        `Math.max(...values)` 常被用來快速比較一組數字，找到其中的最大值。

        例如：需要找到一組成績中的最高分

        ```javascript
        let scores = [70, 85, 92, 88];
		let highestScore = Math.max(...scores);
		console.log(highestScore); // 92
        ```

        在這個範例中，使用了展開運算符 (`...`)，將陣列轉換成多個參數傳入 `Math.max(...values)`，找到最高的分數。

    - 動態處理資料

        當資料是動態產生時，可以使用 `Math.max(...values)` 找出其中的最大值。

        例如：從一組來自表單輸入的數字中找出最大值

        ```javascript
        let userInputs = [10, -5, 100, 23];
		let maxInput = Math.max(...userInputs);
		console.log(maxInput); // 100
        ```

- 與 `Math.min(...values)` 的比較

    - `Math.max(...values)` 返回一組數字中的最大值，而 `Math.min(...values)` 則返回最小值。

        兩者在功能上是互補的，可以一起使用來同時找到最大值和最小值

        ```javascript
        let numbers = [3, 7, -2, 0, 15];
		console.log(Math.max(...numbers)); // 15
		console.log(Math.min(...numbers)); // -2
        ```

### 常見誤區

- `Math.max(...values)`  不接受陣列作為參數：`Math.max(...values)`  的參數必須是數字，而不是陣列。

    若想從一個陣列中找出最大值，需要使用展開運算符 (`...`) 來將陣列展開成多個數字

    ```javascript
	let arr = [4, 9, 1];
	console.log(Math.max(arr));    // NaN
	console.log(Math.max(...arr)); // 9    
    ```

### 總結

`Math.max(...values)` 是一個用來找出多個數字中最大值的方法，可以比較任意數量的數字，並返回其中的最大值。

常用於數字比較、資料處理等場景。需要注意的是，若參數中有 `NaN`，結果會是 `NaN`，而無參數時則返回 `-Infinity`。

<br />

## `Math.min(...values)`

`Math.min(...values)` 是 JavaScript 中用來找出一組數字中最小值的內建方法，接受多個數值作為參數，並返回其中最小的那個數字。

若沒有任何參數，則返回 `-Infinity`，表示在空集合中沒有最小值。若傳入的參數包含 `NaN`，則返回 `NaN`。

### 基本語法

```javascript
Math.min(value1, value2, ..., valueN);
```

- `value1, value2, ..., valueN`：想要比較的數字。

### 詳細說明

- 多個數值比較

    `Math.max(...values)` 可以接受任意數量的數值，並從中找出最小的數。當傳入多個參數時會逐一比較，並返回其中最小的數字。

- 範例

    - 多個正數

        ```javascript
        console.log(Math.min(3, 7, 1, 9)); // 1
        ```

    - 多個負數

        ```javascript
        console.log(Math.min(-8, -5, -10)); // -10
        ```

    - 混合正數與負數

        ```javascript
        console.log(Math.min(-3, 5, -1, 2)); // -3
        ```

    - 無參數的情況

        ```javascript
        console.log(Math.min()); // -Infinity
        ```

    - NaN 的情況

        ```javascript
        console.log(Math.min(1, 2, NaN, 4)); // NaN
        ```

- 應用場景

    - 比較一組數字的大小

        `Math.min(...values)` 常被用來快速比較一組數字，找到其中的最小值。

        例如：在一組資料中找出最低價格或最小數量

        ```javascript
		let prices = [500, 200, 300, 150];
		let lowestPrice = Math.min(...prices);
		console.log(lowestPrice); // 150
        ```

        在這個範例中，使用了展開運算符 (`...`)，將陣列轉換成多個參數傳入 `Math.min(...values)`，找到最小的價格。

    - 動態處理資料

        當資料是動態產生時，可以使用 `Math.min(...values)` 找出其中的最小值。

        例如：從一組來自表單輸入的數字中找出最小值

        ```javascript
		let userInputs = [20, -10, 30, 5];
		let minInput = Math.min(...userInputs);
		console.log(minInput); // -10
        ```

- 與 `Math.max(...values)` 的比較

    - `Math.min(...values)` 返回一組數字中的最小值，而 `Math.max(...values)` 則返回最大值。

        兩者在功能上是互補的，可以一起使用來同時找到最小值和最大值

        ```javascript
        let numbers = [3, 7, -2, 0, 15];
		console.log(Math.min(...numbers)); // -2
		console.log(Math.max(...numbers)); // 15
        ```

### 常見誤區

- `Math.min(...values)`  不接受陣列作為參數：`Math.min(...values)`  的參數必須是數字，而不是陣列。

    若想從一個陣列中找出最小值，需要使用展開運算符 (`...`) 來將陣列展開成多個數字

    ```javascript
	let arr = [4, 9, 1];
	console.log(Math.min(arr));    // NaN
	console.log(Math.min(...arr)); // 1
    ```

### 總結

`Math.min(...values)` 是一個用來找出多個數字中最小值的方法，可以比較任意數量的數字，並返回其中的最小值。

常用於數字比較、資料處理等場景。需要注意的是，若參數中有 `NaN`，結果會是 `NaN`，而無參數時則返回 `-Infinity`。

<br />

## `Math.pow(base, exponent)`

`Math.pow(base, exponent)` 是 JavaScript 中用來計算次方的內建方法，其中 `base` (底數) 和 `exponent` (指數)，返回底數 `base` 的 `exponent` 次方結果。也就是說，`Math.pow(base, exponent)` 會將底數提升到指數的冪次，並返回該數值。

### 基本語法

```javascript
Math.pow(base, exponent);
```

- `base`：要被提升次方的數字 (底數)。

- `exponent`：提升的次數 (指數)。

### 詳細說明

- 指數運算的基本概念

    `Math.pow(base, exponent)` 是計算 `base` 提升到 `exponent` 次方。

    例如：若想計算 2 的 3 次方 (2<sup>3</sup>)

    ```javascript
    console.log(Math.pow(2, 3)); // 8
    ```

- 範例

    - 正數指數

        當底數和指數都是正數的情況

        ```javascript
        console.log(Math.pow(3, 2)); // 9
        console.log(Math.pow(5, 3)); // 125
        ```
    - 負數指數

        當指數是負數時，`Math.pow(base, exponent)` 計算的是該底數的倒數

        ```javascript
        console.log(Math.pow(2, -3));  // 0.125
        console.log(Math.pow(10, -2)); // 0.01
        ```

    - 指數為零

        根據數學規則，任何數字的 0 次方都是 1

        ```javascript
        console.log(Math.pow(5, 0));   // 1
        console.log(Math.pow(100, 0)); // 1
        ```

    - 負數底數

        若底數是負數，且指數是正整數，`Math.pow(base, exponent)` 會正常計算

        ```javascript
        console.log(Math.pow(-3, 3)); // -27
        console.log(Math.pow(-2, 4)); // 16
        ```

	當底數是負數且指數為奇數時，結果是負數 (例如：-3<sup>3</sup> = -27)。

    當底數是負數且指數為偶數時，結果是正數 (例如：-2<sup>4</sup> = 16)。

    - 小數指數

        `Math.pow(base, exponent)` 也可以處理小數指數。當指數為小數時，計算的結果是底數的根值

        ```javascript
        console.log(Math.pow(9, 0.5));  // 3 (9 的平方根)
        console.log(Math.pow(27, 1/3)); // 3 (27 的立方根)
        ```

    - `NaN` 和 `Infinity`

        若傳入的參數中包含無效值 (例如：非數字)，`Math.pow(base, exponent)` 會返回 `NaN`。

        根據數學規則，某些情況下結果會是 `Infinity` 或 `-Infinity`

        ```javascript
        console.log(Math.pow(0, -1));       // Infinity (0 的負次方是無窮大)
        console.log(Math.pow(Infinity, 2)); // Infinity (無窮大的平方還是無窮大)
        ```

- 應用場景

    - 指數運算：`Math.pow(base, exponent)` 可以用來計算科學或金融中的指數運算，例如：利息、增長率等。

    - 平方和立方：可以用來計算平方 `Math.pow(x, 2)` 或立方 `Math.pow(x, 3)`，也可以計算根號 (例如：平方根 `Math.pow(x, 0.5)`)。

### 替代方法

在 ES6 中，除了 `Math.pow(base, exponent)`，也可以使用指數運算符 (`**`) 來進行相同的運算

```javascript
console.log(2 ** 3); // 8
console.log(5 ** 2); // 25
```

### 範例總結

- 基本次方運算

    ```javascript
    console.log(Math.pow(4, 3)); // 64
    ```

- 負數次方

    ```javascript
    console.log(Math.pow(2, -2)); // 0.25
    ```

- 平方根計算

    ```javascript
    console.log(Math.pow(16, 0.5)); // 4
    ```

- 倒數運算

    ```javascript
    console.log(Math.pow(10, -1)); // 0.1
    ```

### 總結

`Math.pow(base, exponent)` 是用來計算次方的方法，允許將一個數字提升到特定的冪次。

`Math.pow(base, exponent)` 支援正數、負數和小數的指數運算，並能處理各種複雜的數學運算場景。無論是計算平方、立方或根值，`Math.pow(base, exponent)` 都是非常好用的方法。

<br />

## `Math.sqrt(x)`

`Math.sqrt(x)` 是 JavaScript 中用來計算平方根的內建方法。也就是說，當一個數字平方 (乘以自身) 等於 `x` 時，這個數字就是 `x` 的平方根。

若 `x` 是正數，返回其平方根；若 `x` 是負數，則會返回 `NaN`，因為負數在實數範圍內沒有平方根。

### 基本語法

```javascript
Math.sqrt(x);
```

- `x`：想要計算平方根的數字。

### 詳細說明

- 範例

    - 正數的平方根

        `Math.sqrt(x)` 會返回 `x` 的平方根

        ```javascript
        console.log(Math.sqrt(9));  // 3
        console.log(Math.sqrt(16)); // 4
        ```

    - 負數的平方根

        若 `x` 是負數，`Math.sqrt(x)` 會返回 `NaN`，因為在實數範圍內負數沒有平方根

        ```javascript
        console.log(Math.sqrt(-1)); // NaN
        ```

    - 0 的平方根

        若 `x` 是 0，則平方根也是 0

        ```javascript
        console.log(Math.sqrt(0)); // 0
        ```

    - 小數的平方根

        `Math.sqrt(x)` 也可以處理小數，並返回該小數的平方根

        ```javascript
        console.log(Math.sqrt(0.25)); // 0.5
        console.log(Math.sqrt(2.25)); // 1.5
        ```

- 應用場景

    - 數學運算：`Math.sqrt(x)` 常用於數學計算中，例如：幾何問題或物理問題中，需要計算距離或面積時可能會用到平方根。

        - 計算歐幾里得距離

            在計算兩點之間的距離時，`Math.sqrt(x)` 可以用來計算平方和的根值

        	```javascript
        	let x1 = 3, y1 = 4;
			let x2 = 0, y2 = 0;
			let distance = Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
			console.log(distance); // 5
        	```

### 與 `Math.pow(base, exponent)` 的比較

`Math.sqrt(x)` 等同於 `Math.pow(x, 0.5)`，兩者都可以用來計算平方根

```javascript
console.log(Math.sqrt(25));     // 5
console.log(Math.pow(25, 0.5)); // 5
```

### 常見誤區

- 負數的處理：`Math.sqrt(x)` 無法處理負數的平方根。

    若需要處理負數的平方根，就需要進行複數運算，而 JavaScript 的內建 `Math.sqrt(x)` 並不支援複數運算。

### 總結

`Math.sqrt(x)` 是計算數字平方根的方法，常用於數學計算和科學應用中。

對於正數會返回其平方根，對於負數則會返回 `NaN`。

<br />

## `Math.cbrt(x)`

`Math.cbrt(x)` 是 JavaScript 中用來計算立方根的內建方法。也就是說，當一個數字立方等於 `x` 時，這個數字就是 `x` 的立方根。

與平方根不同，立方根可以接受負數，因為負數也有對應的立方根。

### 基本語法

```javascript
Math.cbrt(x);
```

- `x`：想要計算立方根的數字。

### 詳細說明

- 範例

    - 正數的立方根

        若 `x` 是正數，`Math.cbrt(x)` 會返回正的立方根

        ```javascript
		console.log(Math.cbrt(8));  // 2
		console.log(Math.cbrt(27)); // 3
        ```

    - 負數的立方根

        與平方根不同，負數也有立方根。

        `Math.cbrt(x)` 可以計算負數的立方根

        ```javascript
        console.log(Math.cbrt(-8));  // -2
        console.log(Math.cbrt(-27)); // -3
        ```

    - 0 的立方根

        若 `x` 是 0，則立方根也是 0

        ```javascript
        console.log(Math.cbrt(0)); // 0
        ```

    - 小數的立方根

        `Math.cbrt(x)`  也可以處理小數，並返回該小數的立方根

        ```javascript
        console.log(Math.cbrt(0.125)); // 0.5
        console.log(Math.cbrt(1.331)); // 1.1
        ```

- 應用場景

    - 數學運算：`Math.cbrt(x)`  常用於數學計算中，例如：計算三維體積或需要求解立方方程式的情況。

    - 幾何應用：計算立方體的邊長，當已知體積時，可以通過立方根來求出邊長

        ```javascript
		let volume = 64;
		let edgeLength = Math.cbrt(volume);
		console.log(edgeLength); // 4
        ```

### 與 `Math.pow(base, exponent)` 的比較

雖然可以使用 `Math.pow(x, 1/3)` 來計算立方根，但 `Math.cbrt(x)` 是更精確和直接的方法，因為可以避免浮點運算中的誤差，特別是在處理負數時更為精確

```javascript
console.log(Math.cbrt(-1.331));     // -1.1
console.log(Math.pow(-1.331, 1/3)); // NaN
```

- `Math.cbrt(x)` 方法是專門用來計算數字的立方根，並且可以處理負數。

- `Math.pow(base, exponent)` 使用的是乘方計算式，無法處理帶有分數次方的負數。在數學上，對於負數的分數次方會涉及到複數的計算，因為 JavaScript 的 `Math.pow(base, exponent)` 無法直接處理複數，所以返回 `NaN`，表示結果無法計算。


### 總結

`Math.cbrt(x)` 是用來計算立方根的方法，無論是正數、負數、小數還是零，都能給出正確的結果。

與平方根不同，負數也有立方根，因此 `Math.cbrt(x)` 在處理負數時更好用。

<br />

## `Math.log(x)`

`Math.log(x)` 是 JavaScript 中用來計算自然對數的內建方法。

自然對數是以指數函數 (數學常數) e (約等於 2.718) 為底的對數，簡單來說，就是計算當 e 的多少次方等於 `x`。

在數學上，`Math.log(x)` 會返回一個數字，使得 e 的這個次方等於 `x`。

### 基本語法

```javascript
Math.log(x);
```

- `x`：想要計算自然對數的數字，必須大於 0。

### 詳細說明

- 自然對數的基本概念

    `Math.log(x)` 計算的是自然對數，底數為 e (約等於 2.718)。也就是說，`Math.log(x)` 代表 e 的多少次方會等於 `x`。

    例如：`Math.log(1)` 等於 0，因為 e 的 0 次方等於 1

    ```javascript
    console.log(Math.log(1)); // 0
    ```

- 範例

    - 自然對數為正數

        當 `x` 是大於 0 的數字，`Math.log(x)` 會返回對應的自然對數值

        ```javascript
        console.log(Math.log(10)); // 2.302585092994046
        console.log(Math.log(2));  // 0.6931471805599453
        ```

    -  自然對數為 1

        `Math.log(1)` 返回 0，因為 e 的 0 次方等於 1

        ```javascript
        console.log(Math.log(1)); // 0
        ```

    - 自然對數為負數與 0

        `Math.log(x)` 只適用於 `x` > 0 的數字。若 `x` 是 0 或負數，`Math.log(x)` 會返回 `NaN`，因為在實數範圍內沒有定義 0 或負數的自然對數

        ```javascript
        console.log(Math.log(0));  // -Infinity (負無窮大)
        console.log(Math.log(-1)); // NaN
        ```

    - 自然對數為小數

        `Math.log(x)` 也可以處理小於 1 的正數，返回的自然對數會是負數

        ```javascript
        console.log(Math.log(0.5)); // -0.6931471805599453
        ```

- 應用場景

    - 科學與工程：自然對數常用於描述指數增長、衰減的情況，例如：計算放射性衰變、複利利息等。

    - 經濟與統計：在經濟學中，自然對數用於計算投資的複利增長，或處理非線性數據時轉換數據進行線性回歸。


### 常用對數的變換

除了自然對數，若想要計算 10 為底的對數，可以使用 `Math.log10(x)`，也可以通過數學公式轉換。

```javascript
function log10(x) {
  return Math.log(x) / Math.LN10;
}

console.log(log10(100)); // 2
```

### `Math.log(x)` 與 `Math.exp(x)` 的關係

`Math.exp(x)` 是計算 e 的 `x` 次方，而 `Math.log(x)` 則是計算 `x` 的自然對數，兩者互為反函數。

```javascript
console.log(Math.exp(Math.log(5))); // 5
console.log(Math.log(Math.exp(2))); // 2
```

### 總結

`Math.log(x)` 是用來計算自然對數的工具，在數學、科學和經濟等領域有廣泛應用。

`Math.log(x)` 能夠處理大於 0 的正數，返回以 e 為底的對數值。自然對數特別適用在描述指數增長和衰減的問題，但要注意，`x` 必須是正數，否則會返回 `NaN` 或 `-Infinity`。

<br />

## `Math.log10(x)`

`Math.log10(x)` 是 JavaScript 中用來計算以 10 為底數的對數的內建方法。也就是說，`Math.log10(x)` 會返回一個數字，使得 10 的這個次方等於 `x`。

對數運算在科學、工程和數據分析中經常用來處理大範圍的數值，特別是當數據以指數方式增長或衰減時。

### 基本語法

```javascript
Math.log10(x);
```

- `x`：想要計算以 10 為底的對數數字，必須大於 0。

### 詳細說明

- 以 10 為底的對數基本概念

    - `Math.log10(x)` 計算的是以 10 為底的對數，表示的是 10 的多少次方等於 `x`。

- 範例

    - 以 10 為底對數為正數

        當 `x` 是大於 0 的正數時，`Math.log10(x)` 會返回對應的對數值

        ```javascript
        console.log(Math.log10(10));  // 1
        console.log(Math.log10(100)); // 2
        ```

    - 以 10 為底對數為 1

        `Math.log10(1)` 返回 0，因為 10 的 0 次方等於 1

        ```javascript
        console.log(Math.log10(1)); // 0
        ```

    -  以 10 為底對數為負數與 0

        `Math.log10(x)` 只適用於 `x` > 0 的數字。

        若 `x` 是 0 或負數，`Math.log10(x)` 會返回 `NaN` 或 `-Infinity`

        ```javascript
        console.log(Math.log10(0));   // -Infinity
        console.log(Math.log10(-10)); // NaN
        ```

    - 以 10 為底對數為小數

        當 `x` 是介於 0 到 1 之間的小數時，返回的對數值是負數

        ```javascript
        console.log(Math.log10(0.1));  // -1
        console.log(Math.log10(0.01)); // -2
        ```

- 應用場景

    - 數據處理：以 10 為底的對數在數據處理中被廣泛應用，特別是在處理數據範圍很大的時候，對數有助於壓縮數據範圍，便於觀察和分析。

    - 工程與科學計算：在電學、聲學等領域，對數用於表示數值差異，例如：分貝 (dB) 表示音量的差異。

### 與 `Math.log(x)` 的比較

- `Math.log10(x)` 是專門用來計算以 10 為底的對數，而 `Math.log(x)` 則是計算自然對數 (底數是 e)。兩者的底數不同，但都屬於對數運算。

- 使用 `Math.log(x) / Math.LN10` 也可以實現相同效果，因為 `Math.LN10` 是自然對數 `log(10)` 的常數

    ```javascript
    function log10(x) {
      return Math.log(x) / Math.LN10;
    }

    console.log(log10(100)); // 2
    ```

### 總結

`Math.log10(x)` 是用來計算以 10 為底對數的方法，能夠快速計算正數的對數值，並且在處理大範圍數據或指數增長問題時也非常有用。

需要注意的是 `x` 必須是大於 0 的正數，否則會返回 `NaN` 或負無窮大。

<br />

## `Math.log2(x)`

`Math.log2(x)` 是 JavaScript 中用來計算以 2 為底數的對數的內建方法。也就是說，`Math.log2(x)` 會返回一個數字，使得 2 的這個次方等於 `x`。

二進位對數在電腦科學、數據分析和許多計算領域中相當常見，因為二進位制是數位電腦的基礎。

### 基本語法

```javascript
Math.log2(x);
```

- `x`：想要計算以 2 為底的對數數字，必須大於 0。

### 詳細說明

- 以 2 為底的對數基本概念

    - `Math.log2(x)` 計算的是以 2 為底的對數，意思是 2 的多少次方會等於 `x`。

    - 以 2 為底的對數特別常見於電腦科學，因為電腦使用二進位制，計算記憶體大小、處理器運算次數等，都會用到以 2 為底的對數。

- 範例

    - 以 2 為底對數為正數

        當 `x` 是大於 0 的正數時，`Math.log2(x)` 會返回對應的對數值

        ```javascript
		console.log(Math.log2(8));  // 3
		console.log(Math.log2(32)); // 5
        ```

    - 以 2 為底對數為 1

        `Math.log2(1)` 返回 0，因為 2 的 0 次方等於 1

        ```javascript
        console.log(Math.log2(1)); // 0
        ```

    - 以 2 為底對數為負數與 0

        `Math.log2(x)` 只適用於 `x` > 0 的數字。若 `x` 是 0 或負數，`Math.log2(x)` 會返回 `NaN` 或 `-Infinity`

        ```javascript
		console.log(Math.log2(0));  // -Infinity
		console.log(Math.log2(-4)); // NaN
        ```

    - 以 2 為底對數為小數

        當 `x` 是介於 0 到 1 之間的小數時，返回的對數值是負數

        ```javascript
		console.log(Math.log2(0.5));  // -1
		console.log(Math.log2(0.25)); // -2
        ```

- 應用場景

    - 電腦科學：二進位對數用於分析算法的複雜度，特別是二分搜尋、樹狀結構、加密等運算。

    - 數據壓縮與編碼：在處理訊息和數據時，二進位對數可以幫助壓縮數據和計算熵值。

    - 處理大型數據：處理大範圍數據時，使用二進位對數可以使數據範圍更可管理。

### 與 `Math.log(x)` 的比較

- `Math.log2(x)` 是專門用來計算以 2 為底的對數，而 `Math.log(x)` 則是計算自然對數 (底數是 e)。兩者的底數不同，但都屬於對數運算。

- 使用 `Math.log(x) / Math.LN2` 也可以實現相同效果，因為 `Math.LN2` 是自然對數 log(2) 的常數

    ```javascript
	function log2(x) {
	  return Math.log(x) / Math.LN2;
	}

	console.log(log2(8)); // 3
    ```

### 總結

`Math.log2(x)` 是用來計算以 2 為底對數的方法，特別適用於電腦科學和數據處理領域。`Math.log2(x)` 能夠快速計算二進位對數，對於處理指數增長、數據壓縮等問題非常有幫助。

<br />

## `Math.exp(x)`

`Math.exp(x)` 是 JavaScript 中用來計算以指數函數 (數學常數) e (約等於 2.718) 為底的指數的內建方法。e 是自然對數的基礎。`Math.exp(x)` 會返回 e 的 `x` 次方結果，也就是說，計算的是 e<sup>x</sup>。

### 基本語法

```javascript
Math.exp(x);
```

- `x`：要計算的次方指數。

### 詳細說明

- 指數的基本概念

    - `Math.exp(x)` 用來計算數學中的指數運算，底數是自然數 e，這個數字在數學和科學中非常重要。`Math.exp(x)` 就是 e<sup>x</sup>，也就是 e 的 `x` 次方。

- 範例

    - 指數為正數

        當 `x` 是正數時，`Math.exp(x)` 會返回 e 的正數次方

        ```javascript
		console.log(Math.exp(2)); // 7.38905609893065
		console.log(Math.exp(3)); // 20.085536923187668
        ```

    - 指數為 0

        `Math.exp(0)` 返回 1，因為任何數字的 0 次方都是 1，包括 e 也是

        ```javascript
        console.log(Math.exp(0)); // 1
        ```

    - 指數為負數

        當 `x` 是負數時，`Math.exp(x)` 會返回 e 的負數次方，也就是說，計算的是 1 / e<sup>x</sup>

        ```javascript
		console.log(Math.exp(-1)); // 0.36787944117144233
		console.log(Math.exp(-2)); // 0.1353352832366127
        ```

- 應用場景

    - 科學與工程：`Math.exp(x)` 常用於處理自然增長和衰減現象，例如：計算放射性衰變、複利利息、人口增長等。除此之外還在熱力學、電學、經濟學中有著廣泛的應用。

    - 計算自然對數的反函數：`Math.exp(x)` 是自然對數 `Math.log(x)` 的反函數，也就是說，兩者可以互相抵消

        ```javascript
        console.log(Math.exp(Math.log(5))); // 5
        console.log(Math.log(Math.exp(2))); // 2
        ```

### 總結

`Math.exp(x)` 是用來計算自然數 e 的 `x` 次方的方法，特別是在處理指數增長或衰減問題時，常見於科學、經濟學和工程領域。

`Math.exp(x)` 也是自然對數的反函數，因此可以用來還原通過自然對數計算出的結果。可以特別注意的是，當 `x` 是 0 時，結果是 1，而 `x` 是負數時，結果是 e 的倒數。

<br />

## `Math.sin(x)`

`Math.sin(x)` 是 JavaScript 中用來計算一個角度正弦值的內建方法。

正弦函數是三角學中的基本函數之一，用來描述一個直角三角形中對邊與斜邊的比值。

`Math.sin(x)` 輸入的 `x` 是一個弧度 (radians)，而不是角度 (degrees)。

### 基本語法

```javascript
Math.sin(x);
```

- `x`：要計算正弦值的角度 (以弧度為單位)。

### 詳細說明

- 角度與弧度的轉換

    - 在 JavaScript 中，`Math.sin(x)` 接收的是弧度。若想用角度來計算，要先將角度轉換成弧度。

        弧度 = 角度 × (π/180)

    - 例如：30 度等於 `30 × Math.PI / 180`，這樣會轉換成約 0.5236 弧度。

- 正弦函數的基本定義

    - 正弦函數是在一個直角三角形中，對應角的對邊長度與斜邊長度的比值。`Math.sin(x)` 返回的值範圍在 -1 到 1 之間。

    - 例如：`Math.sin(0)` 返回 0，因為 0 度 (或 0 弧度) 的正弦值是 0。

- 常見的正弦值

    - `Math.sin(0)` 返回 0，因為 0 弧度的正弦值是 0。

    - `Math.sin(Math.PI / 2)` 返回 1，因為 90 度 (π/2 弧度) 的正弦值是 1。

    - `Math.sin(Math.PI)` 返回 1.2246467991473532e-16 (因為浮點數精度限制導致)，在數學上 180 度 (π 弧度) 的正弦值是 0。

        解決方法

        - 使用容差範圍 (Epsilon)

            ```javascript
            const result = Math.sin(Math.PI);
            const epsilon = 1e-10; // 容許的誤差範圍

            if (Math.abs(result) < epsilon) {
              console.log(0); // 若結果接近 0，輸出 0
            } else {
              console.log(result); // 否則輸出原始結果
            }
            ```

        - 使用 `toFixed()` 來限制小數位數

            ```javascript
            console.log(Math.sin(Math.PI).toFixed(10)); // 0.0000000000
            ```

- 範例

    - 弧度為正數

        計算 π/2 弧度的正弦值 (90 度)

        ```javascript
        console.log(Math.sin(Math.PI / 2)); // 1
        ```

    - 弧度為 0

        ```javascript
        console.log(Math.sin(0)); // 0
        ```
    - 弧度為負數

        當輸入負數弧度時，`Math.sin(x)` 會返回相應的負數值

    	```javascript
    	console.log(Math.sin(-Math.PI / 2)); // -1
    	```

    - 弧度為小數點

        當輸入小數弧度時，`Math.sin(x)` 會返回該弧度的正弦值

    	```javascript
    	console.log(Math.sin(0.5)); // 0.479425538604203
    	```

    - 轉換角度為弧度並計算正弦值

        ```javascript
        let angle = 60;
		let radian = angle * (Math.PI / 180);
		console.log(Math.sin(radian)); // 0.8660254037844386
        ```

- 範例程式碼

    ```javascript
    /** 計算 30 度的正弦值 */
    let degrees = 30;
    let radians = degrees * (Math.PI / 180);
    console.log(Math.sin(radians)); // 0.49999999999999994   (約等於 0.5)

    /** 計算 90 度的正弦值 */
    console.log(Math.sin(Math.PI / 2)); // 1
    ```

- 應用場景

    - 波動與震盪：正弦函數常被用來描述週期性運動，例如：聲波、光波或電磁波的震盪。

    - 物理學：在力學中，描述簡諧運動或圓周運動的物體時，就會使用到正弦函數。

    - 電學與訊號處理：在分析交變電流或正弦波訊號時，正弦函數非常重要。

### 總結

`Math.sin(x)` 是用來計算角度的正弦值的函數，常用於描述週期運動、波動以及其他相關的物理現象。

計算時需要注意 JavaScript 中的角度必須先轉換為弧度才能進行正弦計算。正弦值的範圍介於 -1 到 1 之間。

<br />

## `Math.cos(x)`

`Math.cos(x)` 是 JavaScript 中用來計算一個角度餘弦值的內建方法。

餘弦函數是三角學中的基本函數之一，用來描述一個直角三角形中鄰邊與斜邊的比值。`Math.cos(x)` 輸入的 `x` 是一個弧度 (Radians)，而不是角度 (Degrees)。

### 基本語法

```javascript
Math.cos(x);
```

- `x`：要計算餘弦值的角度 (以弧度為單位)。

### 詳細說明

- 角度與弧度的轉換

    - 在 JavaScript 中，`Math.cos(x)` 接收的是弧度。若想用角度來計算，要先將角度轉換成弧度。

        弧度 = 角度 × (π/180)

    - 例如：60 度等於 `60 × Math.PI / 180`，這樣會轉換成約 1.047 弧度。

- 餘弦函數的基本定義

    - 餘弦函數是在一個直角三角形中，對應角的鄰邊長度與斜邊長度的比值。`Math.cos(x)` 返回的值範圍在 -1 到 1 之間。

    - 例如：`Math.cos(0)` 返回 1，因為 0 度 (或 0 弧度) 的餘弦值是 1。

- 常見的餘弦值

    - `Math.cos(0)` 返回 1，因為 0 弧度的餘弦值是 1。

    - `Math.cos(Math.PI / 2)` 返回 6.123233995736766e-17 (因為浮點數精度限制導致)，在數學上 90 度 (π/2 弧度) 的餘弦值是 0。

        解決方法

        - 手動近似處理

            ```javascript
            const result = Math.cos(Math.PI / 2);
            const epsilon = 1e-10;

            if (Math.abs(result) < epsilon) {
              console.log(0); // 將非常接近 0 的值視為 0
            } else {
              console.log(result);
            }
            ```

        - 使用 `toFixed()` 來限制小數位數

            ```javascript
            console.log(Math.cos(Math.PI / 2).toFixed(10)); // 0.0000000000
            ```

    - `Math.cos(Math.PI)` 返回 -1，因為 180 度 (π 弧度) 的餘弦值是 -1。

- 範例

    - 弧度為正數

        計算 π 弧度的餘弦值

        ```javascript
        console.log(Math.cos(Math.PI)); // -1
        ```

    - 弧度為 0

        ```javascript
        console.log(Math.cos(0)); // 1
        ```

    - 弧度為負數

        當 `x` 是負數弧度時，`Math.cos(x)` 會返回相應的餘弦值。

        餘弦函數對於正負數弧度是對稱的，也就是說，`Math.cos(-x) = Math.cos(x)`

    	```javascript
    	console.log(Math.cos(-Math.PI)); // -1
    	```

    - 弧度為小數點

        當輸入小數弧度時，`Math.cos(x)` 會返回該弧度的餘弦值

    	```javascript
    	console.log(Math.cos(0.5)); // 0.8775825618903728
    	```

    - 轉換角度為弧度並計算餘弦值

        ```javascript
		let angle = 45;
		let radian = angle * (Math.PI / 180);
		console.log(Math.cos(radian)); // 0.7071067811865476
        ```

- 範例程式碼

    ```javascript
	/** 計算 60 度的餘弦值 */
	let degrees = 60;
	let radians = degrees * (Math.PI / 180);
	console.log(Math.cos(radians)); // 0.5000000000000001   (約等於 0.5)

	/** 計算 π 弧度的餘弦值 */
	console.log(Math.cos(Math.PI)); // -1
    ```

- 應用場景

    - 圓周運動：在描述物體的圓周運動時，餘弦函數經常用來表示物體在水平方向上的位置變化。

    - 波動與振動：餘弦函數廣泛應用於處理正弦波、光波或電磁波的振動和傳播。

    - 物理學與工程學：在描述周期性運動、諧振現象或解析力與方向的問題時，餘弦函數非常重要。

### 與 `Math.sin(x)` 的關係

- `Math.cos(x)` 與 `Math.sin(x)` 是相輔相成的兩個三角函數，在許多情況經常一起使用。這兩個函數在描述圓周運動、振動現象或波形時，能提供完整的運動軌跡。

- 在圓周運動中，`Math.cos(x)` 對應的是水平方向的位移，而 `Math.sin(x)` 對應的是垂直方向的位移。

### 總結

`Math.cos(x)` 是用來計算角度的餘弦值的函數，常用於物理學與工程學中描述週期運動、振動及波動現象。

計算時需要注意 JavaScript 中的角度必須先轉換為弧度才能進行餘弦計算。餘弦值的範圍介於 -1 到 1 之間。

<br />

## `Math.tan(x)`

`Math.tan(x)` 是 JavaScript 中用來計算一個角度正切值的內建方法。

正切函數是三角學中的基本函數之一，用來描述一個直角三角形中對邊與鄰邊的比值。`Math.tan(x)` 輸入的 `x` 是一個弧度 (Radians)，而不是角度 (Degrees)。

### 基本語法

```javascript
Math.tan(x);
```

- `x`：要計算正切值的角度 (以弧度為單位)。

### 詳細說明

- 角度與弧度的轉換

    - 在 JavaScript 中，`Math.tan(x)` 接收的是弧度。若想用角度來計算，要先將角度轉換成弧度。

        弧度 = 角度 × (π/180)

    - 例如：45 度等於 `45 × Math.PI / 180`，這樣會轉換成約 0.7854 弧度。

- 正切函數的基本定義

    - 正切函數描述的是直角三角形中，對應角的對邊長與鄰邊長的比值。當角度趨近於 90 度 (π/2 弧度) 時，正切值會趨向無限大，因為此時鄰邊的長度趨近於 0。

- 常見的正切值

    - `Math.tan(0)` 返回 0，因為0 度 (或 0 弧度) 的正切值是 0。

    - `Math.tan(Math.PI / 4)` 返回 0.9999999999999999 (因為浮點數精度限制導致)，在數學上 45 度 (π/4 弧度) 的正切值是 1。

        解決方法

        - 設置容差範圍來處理浮點數誤差

            ```javascript
            const result = Math.tan(Math.PI / 4);
            const epsilon = 1e-10; // 設置一個小的容差值

            if (Math.abs(result - 1) < epsilon) {
              console.log(1); // 若接近 1，則將結果修正為 1
            } else {
              console.log(result); // 否則輸出原值
            }
            ```

        - 使用 `toFixed()` 或 `toPrecision()` 限制小數位數

            ```javascript
            console.log(Math.tan(Math.PI / 4).toFixed(10)); // 1.0000000000
            ```

        - 檢查常見的理論值

            對於某些特定角度 (例如：π/4、𝜋/2 等)，其正切、正弦、餘弦值是理論上已知的。可以先檢查計算結果是否應該接近這些理論值，並將其修正

            ```javascript
            function fixedTan(angle) {
              if (angle === Math.PI / 4) {
                return 1; // 對於常見的角度，直接返回理論值
              }
            return Math.tan(angle);
            }

            console.log(fixedTan(Math.PI / 4)); // 1
            ```

    - `Math.tan(Math.PI)` 返回 -1，因為 180 度 (π 弧度) 的正切值是 -1。

- 範例

    - 弧度為正數

        計算 π/4 弧度 (45 度) 的正切值

        ```javascript
        console.log(Math.tan(Math.PI / 4)); // 0.9999999999999999
        ```

    - 弧度為 0

        ```javascript
        console.log(Math.tan(0)); // 0
        ```

    - 弧度為負數

        當 `x` 是負數弧度時，`Math.tan(x)` 會返回相應的負數正切值

    	```javascript
    	console.log(Math.tan(-Math.PI / 4)); // -0.9999999999999999
    	```

    - 轉換角度為弧度並計算正切值

        ```javascript
		let angle = 30;
		let radian = angle * (Math.PI / 180);
		console.log(Math.tan(radian)); // 0.5773502691896257
        ```

    - 正切的周期性

        正切函數具有周期性，週期為 π。也就是說，對於任意角度 x，`Math.tan(x)` 等於 `Math.tan(x + nπ)`，其中 `n` 是任意整數

        ```javascript
        console.log(Math.tan(Math.PI)); // -1.2246467991473532e-16   (約等於 0，因為 π 弧度和 0 弧度的正切值相同)
        ```

- 範例程式碼

    ```javascript
    /** 計算 45 度的正切值 */
    let degrees = 45;
    let radians = degrees * (Math.PI / 180);
    console.log(Math.tan(radians)); // 0.9999999999999999

    /** 計算 π/4 弧度的正切值 */
    console.log(Math.tan(Math.PI / 4)); // 0.9999999999999999
    ```

- 應用場景

    - 斜坡與傾斜角度：在幾何學中，正切函數常被用來計算斜坡的傾斜度，可以應用於建築設計、道路工程等。

    - 物理學：正切函數也經常用來描述傾斜物體的力或運動方向。

    - 計算三角形的比例：正切函數經常與其他三角函數 (例如：正弦 `Math.sin(x)` 和餘弦 `-Math.cos()`) 一起使用，來描述三角形的邊長比例。

### 與 `Math.sin(x)` & `Math.cos(x)` 的關係

- `Math.tan(x)` = `Math.sin(x) /  Math.cos(x)`

- `Math.tan(x)` 的值等於 `Math.sin(x)` 與 `Math.cos(x)` 的比值

    ```javascript
    console.log(Math.tan(Math.PI / 4));                         // 0.9999999999999999
    console.log(Math.sin(Math.PI / 4) / Math.cos(Math.PI / 4)); // 0.9999999999999999
    ```

### 總結

`Math.tan(x)` 是用來計算角度的正切值的函數，常用於計算斜坡的傾斜度或描述週期性運動。

正切值是正弦值與餘弦值的比值。

正切函數具有周期性，其結果會根據輸入的弧度周期性重複。

計算時需要注意 JavaScript 中的角度必須先轉換為弧度才能進行正切計算，在 90 度 (π/2 弧度) 時，正切值趨於無限大，在計算上會返回無限大的數值或未定義的結果。

<br />

## `Math.asin(x)`

`Math.asin(x)` 是 JavaScript 中用來計算一個數值的反正弦值 (Arc Sine) 的內建方法。反正弦函數 (Arc Sine) 是正弦函數的反函數，用來計算給定正弦值對應的角度。返回的結果是弧度 (Radians)，而不是角度 (Degrees)，範圍介於 -π/2 到 π/2 之間，也就是 -90 度到 90 度。

### 基本語法

```javascript
Math.asin(x);
```

- `x`：需要計算反正弦值的數值。這個數值必須介於 -1 和 1 之間，因為正弦值的範圍就是在 -1 到 1 之間。

### 詳細說明

- 弧度與角度的轉換

    - 在 JavaScript 中，`Math.asin(x)` 返回的是弧度。若想將結果轉換為角度，要先將弧度轉換成角度。

        角度 = 弧度 × (180/π)

    - 例如：將 `Math.asin(0.5)` 的結果從弧度轉換為角度

    	```javascript
    	let radians = Math.asin(0.5);
    	let degrees = radians * (180 / Math.PI);
    	console.log(degrees); // 30.000000000000004 (約 30 度)
    	```

- 反正弦函數的基本定義

    - 反正弦函數是正弦函數的反向操作，表示已知一個角度的正弦值，想求出這個角度。`Math.asin(x)` 返回的是使得 `Math.sin(θ) = x` 的角度。

    - 例如：`Math.asin(0.5)` 返回約 0.5235987755982989 弧度，對應的角度是 30 度，因為 sin(30°) = 0.5。


- 反正弦函數的範圍

    - `Math.asin(x)` 的輸入值 `x` 必須在範圍 -1 到 1 之間，否則會返回 `NaN` (不是有效數值)。這是因為正弦值的範圍就在這個區間內。

    - 例如

        ```javascript
        console.log(Math.asin(1));  // 1.5707963267948966 弧度 (90 度)
        console.log(Math.asin(-1)); // -1.5707963267948966 (-90 度)
        console.log(Math.asin(2));  // NaN (因為 2 超出範圍)
        ```

- 常見的反正弦值

    - `Math.asin(0)` 返回 0，因為 sin(0°) = 0。

    - `Math.asin(1)` 返回 π/2，也就是 1.5707963267948966 弧度，對應 90 度，因為 sin(90°) = 1。

    - `Math.asin(-1)` 返回 -π/2，也就是 -1.5707963267948966，對應 -90 度，因為 sin(-90°) = -1。

- 範例

    - 反正弦值為正數

        ```javascript
        console.log(Math.asin(1)); // 1.5707963267948966 (弧度) (90 度)
        ```

    - 反正弦值為 0

        ```javascript
        console.log(Math.asin(0)); // 0 (弧度) (0 度)
        ```

    - 反正弦值為負數

        ```javascript
        console.log(Math.asin(-1)); // -1.5707963267948966 (弧度) (-90 度)
        ```

    - 反正弦值為小數

        ```javascript
        console.log(Math.asin(0.5)); // 0.5235987755982989 (弧度) (30 度)
        ```

- 範例程式碼

    ```javascript
	// 計算 0.5 的反正弦值，並將弧度轉換為角度
	let radians = Math.asin(0.5);
	let degrees = radians * (180 / Math.PI);
	console.log(degrees); // 30.000000000000004 (約 30 度)

	// 計算 -0.5 的反正弦值
	console.log(Math.asin(-0.5)); // -0.5235987755982989 (約 -30 度)
    ```

- 應用場景

    - 三角學計算：反正弦函數常用於三角學中，特別是在已知角度的正弦值時，用來反推出角度。

    - 物理學與工程學：在波動、振動、光波或聲波的研究中，反正弦函數用於求解與週期運動相關的角度。

    - 幾何學：在計算三角形的邊長與角度時，反正弦函數可以幫助求出角度。


### 與 `Math.sin()` 的關係

反正弦函數是正弦函數的反函數。

```javascript
let x = Math.sin(Math.PI / 6); // 0.5
let angle = Math.asin(x);      // π/6
console.log(angle);            // 0.5235987755982988 (弧度) (30 度)
```

### 總結

`Math.asin(x)` 是用來計算數值的反正弦值的函數，返回對應的弧度值。

輸入值必須在 -1 到 1 之間。

反正弦函數廣泛應用於三角學、物理學、工程學等領域，特別是在求解已知正弦值對應的角度時。當需要將結果轉換為角度時，可以使用 `弧度 × 180/π` 的公式來轉換。

<br />

## `Math.acos(x)`

`Math.acos(x)` 是 JavaScript 中用來計算一個數值的反餘弦值 (Arc Cosine) 的內建方法。反餘弦函數 (Arc Cosine) 是餘弦函數的反函數，用來計算給定餘弦值對應的角度。返回的結果是以弧度為單位，範圍在 0 到 π (0 到 180 度) 之間。

### 基本語法

```javascript
Math.acos(x);
```

- `x`：需要計算反餘弦值的數值。這個數值必須介於 -1 和 1 之間，因為餘弦值的範圍就是在 -1 到 1 之間。

### 詳細說明

- 弧度與角度的轉換

    - 在 JavaScript 中，`Math.acos(x)` 返回的是弧度。若想將結果轉換為角度，要先將弧度轉換成角度。

        角度 = 弧度 × (180/π)

    - 例如：將 `Math.acos(0.5)` 的結果從弧度轉換為角度

    	```javascript
		let radians = Math.acos(0.5);
		let degrees = radians * (180 / Math.PI);
		console.log(degrees); // 60.00000000000001 (約 60 度)
    	```

- 反餘弦函數的基本定義

    - 反餘弦函數是餘弦函數的反函數，表示已知角度的餘弦值，求出對應的角度。`Math.acos(x)` 返回的是使得 `Math.cos(θ) = x` 的角度。

    - 例如：`Math.acos(0.5)` 返回約 1.0472 弧度，對應的角度是 60 度，因為 cos(60°) = 0.5。


- 反餘弦函數的範圍

    - `Math.acos(x)` 的輸入值 `x` 必須在範圍 -1 到 1 之間，否則會返回 `NaN`。這是因為餘弦值的範圍就在這個區間內。

    - 例如

        ```javascript
		console.log(Math.acos(1));  // 0 (弧度) (0 度)
		console.log(Math.acos(-1)); // 3.141592653589793 (弧度) (180 度)
		console.log(Math.acos(2));  // NaN (因為 2 超出範圍)
        ```

- 常見的反餘弦值

    - `Math.acos(1)` 返回 0 弧度，因為 因為 cos(0°) = 1。

    - `Math.acos(0)` 返回 π/2 弧度，也就是 1.5707963267948966 弧度，對應 90 度，因為 cos(90°) = 0。

    - `Math.acos(-1)` 返回 π 弧度，也就是 3.141592653589793 弧度，對應 180 度，因為 cos(180°) = -1。

- 範例

    - 反餘弦值為正數

        ```javascript
        console.log(Math.acos(1)); // 0 (弧度) (0 度)
        ```

    - 反餘弦值為 0

        ```javascript
        console.log(Math.acos(0)); // 1.5707963267948966 (弧度) (90 度)
        ```

    - 反餘弦值為負數

        ```javascript
        console.log(Math.acos(-1)); // 3.141592653589793 (弧度) (180 度)
        ```

    - 反餘弦值為小數

        ```javascript
        console.log(Math.acos(0.5)); // 1.0471975511965979 (弧度) (60 度)
        ```

- 範例程式碼

    ```javascript
	/** 計算 0.5 的反餘弦值，並將結果轉換為角度 */
	let radians = Math.acos(0.5);
	let degrees = radians * (180 / Math.PI);
	console.log(degrees); // 60.00000000000001 (約 60 度)

	/** 計算 -1 的反餘弦值 */
	console.log(Math.acos(-1)); // 3.141592653589793 (180 度)
    ```

- 應用場景

    - 三角學計算：反餘弦函數主要應用於幾何學中，例如：在已知兩條邊長的情況下，求解三角形的夾角。

    - 物理學與工程學：在計算向量之間的夾角時，反餘弦函數也非常有用，例如：求解力或速度向量的夾角。

    - 計算角度：反餘弦在許多與旋轉、運動有關的應用中十分常見，例如：機器人學、3D 繪圖等領域。


### 與 `Math.cos()` 的關係

反餘弦函數是餘弦函數的反函數

```javascript
let x = Math.cos(Math.PI / 3); // 0.5
let angle = Math.acos(x);      // π/3
console.log(angle);            // 1.0471975511965976 (弧度) (60 度)
```

### 總結

`Math.acos(x)` 是用來計算數值的反餘弦值的函數，返回對應的弧度。輸入值必須在 -1 到 1 之間。

反餘弦函數在許多幾何學、物理學、工程學應用中非常重要，特別是在已知餘弦值時求解角度。當需要將結果轉換為角度時，可以使用 `弧度 × 180/π` 的公式來轉換。

<br />

## `Math.atan(x)`

`Math.atan(x)` 是 JavaScript 中用來計算一個數值的反正切值 (Arc Tangent) 的內建方法。反正切函數 (Arc Tangent) 是正切函數的反函數，用來計算給定正切值對應的角度。

返回的結果是以弧度為單位，範圍在 -π/2 到 π/2 (-90 到 90 度) 之間。

### 基本語法

```javascript
Math.atan(x);
```

- `x`：用來計算反正切值的數值。數值可以是任何實數，不受限制。

### 詳細說明

- 弧度與角度的轉換

    - 在 JavaScript 中，`Math.atan(x)` 返回的是弧度。若想將結果轉換為角度，要先將弧度轉換成角度。

        角度 = 弧度 × (180/π)

    - 例如：將 `Math.atan(1)` 的結果從弧度轉換為角度

    	```javascript
		let radians = Math.atan(1);
		let degrees = radians * (180 / Math.PI);
		console.log(degrees); // 45 (度)
    	```

- 反正切函數的基本定義

    - 反正切函數是正切函數的反向操作，表示已知一個角度的正切值，反推出這個角度。`Math.atan(x)` 返回的是使得 `Math.tan(θ) = x` 的角度。

    - 例如：`Math.atan(1)` 返回的是 π/4 弧度，約等於 0.7853981633974483 弧度，對應 45 度，因為 tan(45°) = 1。

- 反正切函數的範圍

    - `Math.atan(x)` 沒有輸入範圍限制，`x` 可以是任何實數，包括負數、正數甚至 0。

    - 返回的弧度範圍介於 -π/2 到 π/2 之間，即 -1.5708 到 1.5708 弧度，對應的角度範圍為 -90° 到 90°。

- 常見的反正切值

    - `Math.atan(1)` 返回 π/4，約等於 0.7853981633974483，對應 45 度，因為 tan(45°) = 1。

    - `Math.atan(0)` 返回 0 弧度，因為 tan(0°) = 0。

    - `Math.atan(-1)` 返回 -π/4，約等於 -0.7853981633974483 弧度，對應 -45 度，因為 tan(-45°) = -1。

- 範例

    - 反正切值為正數

        ```javascript
        console.log(Math.atan(1)); // 0.7853981633974483 (弧度) (45 度)
        ```

    - 反正切值為 0

        ```javascript
        console.log(Math.atan(0)); // 0 (弧度) (0 度)
        ```

    - 反正切值為負數

        ```javascript
        console.log(Math.atan(-1)); // -0.7853981633974483 (弧度) (-45 度)
        ```

- 應用場景

    - 三角學：反正切函數常用於三角學中，特別是當已知直角三角形中的對邊與鄰邊的比例時，可以用來求角度。

    - 物理學與工程學：在機械領域、電子領域中，反正切函數常被用來計算向量間的角度或坡度。

    - 導航與地理資訊系統 (GIS)：在計算方向與方位時，反正切函數可幫助求解兩點之間的相對角度。


### 與 `Math.tan()` 的關係

反正切函數是正切函數的反函數

```javascript
let x = Math.tan(Math.PI / 4); // 1
let angle = Math.atan(x);      // π/4
console.log(angle);            // 0.7853981633974483 (弧度) (45 度)
```

### 總結

`Math.atan(x)` 是用來計算數值的反正切值的函數，返回對應的弧度。

輸入值可以是任何實數，並且返回的結果範圍介於 -π/2 和 π/2 之間 (即 -90 度到 90 度)。

反正切函數廣泛應用於三角學、物理學、工程學等領域，尤其是在處理向量角度、方位和坡度的計算。

<br />

## `Math.atan2(y, x)`

`Math.atan2(y, x)` 是 JavaScript 中用來計算兩個座標點 (x, y) 的反正切角度的內建方法。

`Math.atan2(y, x)` 與 `Math.atan(x)` 類似，但可以處理完整的四個象限，並根據 (x, y) 的值，返回從原點到這個點的極座標角度 (弧度)。

此方法特別適合用來計算二維平面中兩個點之間的相對角度。

### 基本語法

```javascript
Math.atan2(y, x);
```

- y：點的 y 座標 (對邊)。

- x：點的 x 座標 (鄰邊)。

### 詳細說明

- 弧度與角度的轉換

    - 在 JavaScript 中，`Math.atan2(y, x)` 返回的是弧度。若想將結果轉換為角度，要先將弧度轉換成角度。

        角度 = 弧度 × (180/π)

    - 例如：將 `Math.atan2(1, 1)` 的結果從弧度轉換為角度

    	```javascript
		let radians = Math.atan2(1, 1);
		let degrees = radians * (180 / Math.PI);
		console.log(degrees); // 45 (度)
    	```

- 反正切函數的基本定義

    - `Math.atan2(y, x)` 是計算從座標原點 (0, 0) 到某一點 (x, y) 之間的角度。這個角度是從 x 軸開始，逆時針方向量取。

    - `Math.atan2(y, x)` 會返回一個弧度值，範圍在 -π 到 π 之間 (-180 度到 180 度)。也就是說，能正確處理各個象限中的點。

    - 例如：`Math.atan2(1, 1)` 返回 0.7853981633974483 弧度，對應 45 度，表示從原點到 (1, 1) 的角度是 45 度。

- 範例

    - 計算點 (1, 1) 的角度 (45 度) (第一象限)

        ```javascript
        console.log(Math.atan2(1, 1)); // 0.7853981633974483
        ```

    - 計算點 (1, -1) 的角度 (135 度) (第二象限)

        ```javascript
        console.log(Math.atan2(1, -1)); // 2.356194490192345
        ```

    - 計算點 (-1, -1) 的角度 (-135 度) (第三象限)

        ```javascript
        console.log(Math.atan2(-1, -1)); // -2.356194490192345
        ```

    - 計算點 (-1, 1) 的角度 (-45 度) (第四象限)

        ```javascript
        console.log(Math.atan2(-1, 1)); // -0.7853981633974483
        ```

    - 將反正切結果從弧度轉換為角度

        ```javascript
        let radians = Math.atan2(1, 1);
		let degrees = radians * (180 / Math.PI);
		console.log(degrees); // 45 (度)
        ```

    - 計算點 (0, 1) 的角度 (90 度)

        ```javascript
        console.log(Math.atan2(0, 1)); // 0
        ```

    - 計算點 (-1, 0) 的角度 (180 度)

        ```javascript
        console.log(Math.atan2(-1, 0)); // -1.5707963267948966
        ```

- 應用場景

    - 計算方位角：`Math.atan2(y, x)` 可用來計算從原點到某一點的方向角，例如：地圖、導航或機器人定位等。

    - 計算兩個向量之間的角度：當知道兩個點的座標時，可以使用 `Math.atan2(y, x)` 來計算這兩點的連線與 x 軸之間的角度。

    - 遊戲開發與物理模擬：用來計算角色或物體的旋轉方向，特別是在二維空間中計算物體的運動軌跡或方向。


### 與 `Math.atan()` 的關係

- `Math.atan(x)` 只能處理第一和第四象限，因為只接受單一的正切值作為輸入，而無法得知正切值是來自於哪個象限。

- `Math.atan2(y, x)` 能處理四個象限，因為同時接受 x 和 y 座標，能夠根據這兩個值來確定角度所屬的象限，這樣可以避免由於正負號混淆造成的錯誤。

### 總結

`Math.atan2(y, x)` 是用來計算二維平面中 (x, y) 座標與 x 軸之間角度的函數，返回的角度是以弧度表示，範圍在 -π 到 π 之間。

`Math.atan2(y, x)` 適用於處理四個象限中的所有點，是比 `Math.atan(x)` 更加靈活和完整的選擇，特別適合在地圖導航、遊戲開發以及物理模擬等場景下使用。

當需要將結果轉換為角度時，可以使用弧度與角度的轉換公式來完成。

<br />

## `Math.hypot(...values)`

`Math.hypot(...values)` 是 JavaScript 中用來計算多個數值平方和的平方根的內建方法，用來計算多維空間中一個點到原點的距離，或是用來求解直角三角形的斜邊長度。

在二維空間，可以用來計算兩個座標 (x, y) 到原點的距離；在三維或更高維空間，也同樣適用。

### 基本語法

```javascript
Math.hypot(...values);
```

- `values`：要計算的數值，可以是兩個或多個數字。會先各自平方，再將所有的平方值加總，最後取平方根。

### 詳細說明

- 函數意義

    - `Math.hypot(...values)` 計算的是多個數值的平方和的平方根，也就是說，等同於以下運算的結果

        $$\sqrt{x_1^2 + x_2^2 + x_3^2 + \cdots + x_n^2}$$

    - 在二維情況下，`Math.hypot(...values)` 可以用來計算直角三角形的斜邊長度，符合畢氏定理 (Pythagorean Theorem)。例如：給定直角三角形的兩個直邊長度 a 和 b，斜邊長 c 可以用以下公式計算 $$c = \sqrt{a^2 + b^2}$$

    - 在三維空間中，若要計算點 (x, y, z) 到原點的距離，則公式為 $$d = \sqrt{x^2 + y^2 + z^2}$$

- 範例

    - 計算二維距離

        ```javascript
        console.log(Math.hypot(3, 4)); // 5
        ```

        以上範例中，計算直角三角形的斜邊長

        $$\sqrt{3^2 + 4^2} = 5$$

    - 計算三維距離

        ```javascript
        console.log(Math.hypot(1, 2, 2)); // 3
        ```

        計算點 (1, 2, 2) 到原點的距離

        $$\sqrt{1^2 + 2^2 + 2^2} = 3$$

    - 多個數值的 hypot 計算

        ```javascript
        console.log(Math.hypot(6, 8, 10)); // 14.142135623730951
        ```

        以上範例中，計算三個數值的平方和的平方根。

    - 處理負數

        ```javascript
		console.log(Math.hypot(-3, -4)); // 5
		```

- 應用場景

    - 二維距離計算：當知道一個點的座標 (x, y)，可以使用 `Math.hypot(x, y)` 計算這個點到原點的距離。例如：`Math.hypot(3, 4)` 的結果為 5。

        $$\sqrt{3^2 + 4^2} = 5$$

    - 三維及多維距離計算：`Math.hypot(x, y, z)` 可以用來計算三維空間中點 (x, y, z) 與原點之間的距離。同樣也可以計算多維空間中的距離。

    - 物理學與工程學：在機械、物理學或是其他應用數學領域，常用來計算位移、力的合成或其他涉及多個分量的問題。

    - 避免溢出和下溢問題：`Math.hypot` 具有內建的數學穩定性，能避免直接對非常大的或非常小的數字平方時，因數字溢出或下溢所產生的計算錯誤

### 與手動計算的比較

雖然可以手動使用以下方式計算距離

```javascript
let distance = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
```

但 `Math.hypot(...values)` 提供更簡潔且數學上更穩定的解決方案，特別是在處理非常大的或非常小的數值時，能夠有效避免數值的溢出或下溢。

### 總結

`Math.hypot(...values)` 是一個用來計算多個數值平方和的平方根的函數，特別適合用來計算二維、三維甚至更高維空間中一個點到原點的距離。

`Math.hypot(...values)` 不僅提供簡潔的語法，還能有效避免手動計算時可能出現的數值溢出問題，常用於距離計算、物理模擬、遊戲開發以及工程學中的應用。

<br />

## `Math.clz32(x)`

`Math.clz32(x)` 是 JavaScript 中用來計算一個 32 位元整數的前導零數量的內建方法，特別適合用於處理位元運算和數值的二進制表示，能夠幫助開發人員快速獲得一個數字在二進制表示中前面有多少個零。

### 基本語法

```javascript
Math.clz32(x);
```

- `x`：要計算的數字。這個數字會被轉換成一個 32 位元整數，若 `x` 是一個非整數的值，會先進行向下取整 (即取整至最接近的整數)。

### 詳細說明

- 前導零的基本定義

    - 前導零是指在數字的二進制表示中，最左邊 (高位) 出現的零的數量。例如：數字 8 在二進制中表示為 00000000000000000000000000001000，有 28 個前導零。

- 輸入與輸出

    - `Math.clz32(x)` 的輸入是任意數字，返回的是該數字的 32 位二進制表示中前導零的個數。結果的範圍是 0 到 32。

    - 若 `x` 為 0，返回值為 32，因為 0 的二進制表示為全零。

- 計算過程

    - 當呼叫 `Math.clz32(x)` 時，JavaScript 首先會將 `x` 轉換為一個 32 位元整數。這個過程包括將 `x` 的數值轉換為二進制形式，然後計算在這個二進制形式中最左邊的零的數量。

- 範例

    - 計算數字 8 的前導零數量

		```javascript
		console.log(Math.clz32(8)); // 28
		```

        數字 8 在 32 位元整數中表示為 00000000000000000000000000001000，前面有 28 個零。

    - 計算數字 0 的前導零數量

		```javascript
		console.log(Math.clz32(0)); // 32
		```

        數字 0 的二進制表示為 00000000000000000000000000000000，因此前導零數量為 32。

    - 計算數字 1 的前導零數量

		```javascript
		console.log(Math.clz32(1)); // 31
		```

        數字 1 在 32 位元整數中表示為 00000000000000000000000000000001，前面有 31 個零。

    - 計算數字 15 的前導零數量

		```javascript
		console.log(Math.clz32(15)); // 28
		```

        數字 15 在 32 位元整數中表示為 00000000000000000000000000001111，前面有 28 個零。

- 應用場景

    - 位元運算：在進行位元運算時，計算前導零的數量可以用來確定數字的位元長度或在某些演算法中使用。

    - 數據編碼：在壓縮或編碼數據時，前導零的計算可能會幫助優化儲存方式。

    - 性能優化：在某些情況下，透過計算前導零數量可以加速算法，特別是在需要頻繁處理整數的運算時。

### 常見誤區

由於 `Math.clz32(x)` 僅適用於 32 位元整數，因此對於大於 2^32 - 1 的數字，結果會被截斷，可能不會返回預期的前導零數量。

### 總結

`Math.clz32(x)` 是用於計算一個數字在 32 位元整數表示中前導零數量的函數，在位元運算和數據處理中非常有用，能夠幫助開發人員快速獲得數字的位元特性，並在某些情況下提高性能。

通過提供簡單的語法和穩定的計算方式，`Math.clz32(x)` 成為處理整數時的一個重要工具。

<br />

## `Math.imul(a, b)`

`Math.imul(a, b)` 是 JavaScript 中用來進行兩個 32 位元整數相乘的內建方法，專門用來執行高效能的整數乘法，並返回正確的 32 位元有號整數結果。

`Math.imul(a, b)` 能夠避免 JavaScript 常見的數字溢出或精度問題，特別是在處理大數時特別有用。

### 基本語法

```javascript
Math.imul(a, b);
```

- `a` 和 `b`：兩個要相乘的數字。

### 詳細說明

- 問題背景

    - JavaScript 中的所有數字都以 64 位元浮點數的形式儲存，但在進行整數運算時，特別是當數字非常大時，精度問題容易發生。例如：若進行兩個大整數的乘法運算，可能會導致結果不正確或超出 32 位元整數的範圍。

    - `Math.imul(a, b)` 可以解決這個問題，因為 `Math.imul(a, b)` 能強制將數字轉換為 32 位元整數，然後執行運算，並返回符合 32 位元有號整數範圍內的結果。

- 作用機制

    - `Math.imul(a, b)` 會先將 `a` 和 `b` 轉換為 32 位元整數 (範圍為 -2<sup>31</sup> 到 2<sup>31</sup> - 1)，然後進行相乘運算，最後返回一個 32 位元有號整數結果。

    - 即使輸入的是浮點數，這個方法會先將其向下取整，並只計算取整後的部分。

- 性能優勢

    - `Math.imul(a, b)` 在進行整數運算時具有較高效能，因為直接進行 32 位元整數乘法，而不是使用 JavaScript 的 64 位元浮點數，這使其適合在高效能需求的情況下，例如：遊戲開發或位元運算中使用。

- 範例

    - 基本運算

        ```javascript
		console.log(Math.imul(2, 4)); // 8
		```

    - 處理大數值

        ```javascript
		console.log(Math.imul(0x7FFFFFFF, 2)); // -2
		```

        在這個範例中，0x7FFFFFFF 是 JavaScript 中的最大 32 位元有號整數 (2<sup>31</sup> - 1)，與 2 相乘的結果會溢出，並返回 `-2`。

        這是因為 `Math.imul(a, b)` 處理的是 32 位元有號整數，超過範圍時會自動進行溢出處理。

    - 使用浮點數

		```javascript
		console.log(Math.imul(5.9, 3.2)); // 15
		```

        `Math.imul(a, b)` 會先將浮點數向下取整，然後進行乘法運算，因此結果為 15 (5 乘以 3)。

- 應用場景

    - 位元運算：`Math.imul(a, b)` 適合用於處理位元運算。許多低層次的演算法或圖形運算 (例如：雜湊函數、位元遮罩運算) 都依賴於精確的 32 位元整數乘法。

    - 遊戲開發：在遊戲開發中，進行大量整數運算時，`Math.imul(a, b)` 能夠提供高效的整數乘法，減少計算成本並保持精度。

    - 避免浮點運算精度問題：在處理大整數乘法時，`Math.imul(a, b)` 可以避免浮點數的精度損失，確保運算結果正確。

### 注意事項

- 浮點數取整數：`Math.imul(a, b)` 會將輸入的浮點數轉換為整數來進行運算，因此若輸入的是浮點數，結果可能與預期的不同。

- 溢出處理：`Math.imul(a, b)` 處理的是 32 位元有號整數，因此若乘法結果超過這個範圍，會進行溢出處理並返回相應的結果。

### 總結

`Math.imul(a, b)` 是用來進行 32 位元整數乘法的高效方法，適合在需要進行位元運算或高效整數計算的情況使用。

這個方法不僅能避免 JavaScript 的浮點數精度問題，還能有效處理 32 位元整數的乘法，確保計算結果符合預期。在處理大數值和需高效能的情況下也提供了很好的解決方案。

<br />

## `Math.fround(x)`

`Math.fround(x)` 是 JavaScript 中的一個方法，用來將給定的數字轉換為最接近的 32 位元單精度浮點數 (Single-precision Floating Point Number)。這個方法的主要作用是確保在處理需要精度控制的應用 (例如：圖形運算、科學計算) 時，數字能以更小的記憶體儲存並保持一定的精度。

### 基本語法

```javascript
Math.fround(x);
```

- `x`：要被轉換的數字。

### 詳細說明

- 單精度浮點數 (Single-Precision Floating Point)

    - JavaScript 的數字預設是以 64 位元雙精度浮點數 (Double-precision) 儲存，但在某些情況下，64 位元的精度和記憶體佔用可能過高，因此可以使用 32 位元單精度浮點數 來減少記憶體佔用並提高效能。

    - `Math.fround(x)` 就是用來將數字轉換成這種 32 位元格式的函數，並返回最接近的單精度表示。

- 運作原理

    - 當呼叫 `Math.fround(x)` 時，JavaScript 會將 `x` 轉換成符合 IEEE 754 標準的 32 位元單精度浮點數。這個過程會將過大或過小的數字取近似值，從而保證符合 32 位元範圍。

- 範例

    - 簡單轉換

        ```javascript
        console.log(Math.fround(5.5)); // 5.5
        ```

        5.5 是一個能被精確表示的數字，因此轉換後結果不變。

    - 浮點數轉換

        ```javascript
        console.log(Math.fround(1.337)); // 1.3370000123977661
        ```

        由於單精度浮點數無法精確表示某些小數點後的數字，因此返回值會是最接近的近似值。

    - 大數轉換

        ```javascript
		console.log(Math.fround(123456789)); // 123456792
		```

        由於單精度浮點數的範圍和精度有限，大數在轉換後可能會出現精度損失，因此結果會略有不同。

- 應用場景

    - 精度控制：當需要將數字控制在 32 位元範圍內來節省記憶體，或在某些情況下使用單精度浮點數的情況下，`Math.fround(x)` 是一個很好的工具。

    - WebGL 或其他圖形運算：WebGL 使用大量的單精度浮點數來進行圖形渲染，因此 `Math.fround(x)` 常用於將數字轉換為符合 WebGL 標準的格式。

    - 性能優化：在需要大量數值運算的情況下，使用 32 位元浮點數能有效提升效能，因為會減少處理器的負擔和記憶體的佔用。

### 注意事項

- 精度損失：當使用 `Math.fround(x)` 時，可能會損失一些小數精度，特別是當數字過大或過小時。這是因為 32 位元單精度浮點數無法表示所有的小數點後數字。

- 溢出與下溢：若輸入的數字超出 32 位元單精度浮點數的範圍，結果會是 `Infinity` 或 `-Infinity`。若數字非常小，則可能會被轉換為 0。

### 總結

`Math.fround(x)` 用於將數字轉換為最接近的 32 位元單精度浮點數。在許多需要精度和記憶體控制的情況下，`Math.fround(x)` 提供了一個有效的解決方案。

雖然會有精度損失，但在圖形處理、科學計算和性能要求較高的情況下，都能幫助提升運算效能並減少記憶體使用。

<br />

## `Math.expm1(x)`

`Math.expm1(x)` 是 JavaScript 中的一個內建方法，用來計算數字 `x` 的 exponential 函數減去 1，即 e<sup>x</sup> - 1 的值，e 是自然對數的底數，約等於 2.718。這個方法的主要用途是當 `x` 很接近 0 時，能夠更精確計算 e<sup>x</sup> - 1，因為直接計算 `Math.exp(x) - 1` 可能會因為浮點數精度的限制而導致結果不夠精確。

### 基本語法

```javascript
Math.expm1(x);
```

- `x`：要計算的數字。

### 詳細說明

- 數學背景

    - `Math.expm1(x)` 其實是在計算「指數函數 (Exponential Function)」的變化量，即 e<sup>x</sup> - 1。在數學中，當 `x` 越來越接近 0 時，e<sup>x</sup> - 1 的結果也會越來越接近 0。這時若直接使用 `Math.exp(x) - 1`，由於 JavaScript 浮點數的限制，可能會產生精度誤差。而 `Math.expm1(x)` 就是為了避免這種精度問題而設計的。

- 使用原因

    - 當 `x` 接近 0 時，計算 e<sup>x</sup> - 1 非常常見於數學和工程計算中。例如：在一些金融計算、物理模擬和機率運算裡，指數函數的變化是核心運算之一。

    - 直接計算 `Math.exp(x) - 1` 會在 `x` 非常小的情況下因為浮點運算的精度限制而導致結果不夠準確，特別是在處理接近 0 的數字時會有精度損失。`Math.expm1(x)` 可以更精確計算這類數值。

- 範例

    - 基本範例

	```javascript
    console.log(Math.expm1(1)); // 1.718281828459045
	```

    在這個範例中，計算的是 e<sup>1</sup> - 1，結果接近於 2.718 - 1，也就是 1.718。

    - 接近 0 的範例

	```javascript
    console.log(Math.expm1(0.000001)); // 0.0000010000005000001665
	```

    當 `x` 非常小時，`Math.expm1(x)` 能夠返回比 `Math.exp(x) - 1` 更精確的結果。

    - 負數範例

	```javascript
    console.log(Math.expm1(-1)); // -0.6321205588285577
	```

    當輸入負數時，`Math.expm1(-1)` 計算的是 e<sup>-1</sup> - 1，即 1/e - 1，這是一個負數。

- 應用場景

    - 科學與工程計算：在處理一些增長模型、複利計算，或物理上的熱力學公式時，經常需要計算 e<sup>x</sup> - 1 的值。`Math.expm1(x)` 使得這些計算更加精確，特別是在處理非常小的數字時。

    - 高精度需求：在金融、機器學習或其他需要進行高精度數值計算的領域，這個方法常用來避免浮點數的精度問題。

- 數學推導與比較

    - `Math.exp(x) - 1`：直接使用 `Math.exp(x)` 計算後再減 1，在大部分情況下可以得到正確的結果，但當 x 非常接近 0 時，結果會因為浮點精度問題導致誤差。

    - `Math.expm1(x)`：專門用來避免這個問題，尤其適用於小的 `x`，能確保計算 e<sup>x</sup> - 1 更加精確。

- 注意事項

    - `x` 值的範圍：`Math.expm1(x)` 可以接受任意實數，無論 `x` 是正數、負數或 0 都可以正確計算出結果。

    - 精度差異：當 `x` 很小時，使用 `Math.expm1(x)` 和直接計算 `Math.exp(x) - 1` 之間的精度差異會變得顯著。特別是在處理科學計算或金融分析這類要求高精度的場景下，應優先使用 `Math.expm1(x)`。

### 總結

`Math.expm1(x)` 是用來精確計算 e<sup>x</sup> - 1 的方法，特別是在處理接近 0 的數字時，比直接計算 `Math.exp(x) - 1` 更精確。

`Math.expm1(x)` 特別是用在科學計算、金融分析、以及其他高精度情況下。透過 `Math.expm1(x)`，可以避免由於浮點數精度限制而導致的誤差，使得計算結果更為準確。

<br />

## `Math.log1p(x)`

`Math.log1p(x)` 是 JavaScript 中的一個內建方法，用來計算 1 + x 的自然對數，也就是 ln(1 + x)。這個方法在處理 `x` 非常接近 0 的情況下，能夠更精確計算結果，因為直接使用 `Math.log(1 + x)` 可能會因為浮點數的精度限制而導致計算結果出現誤差。

### 基本語法

```javascript
Math.log1p(x);
```

- `x`：必須是一個實數 (正數、負數或 0)，但必須滿足 `x` > -1，因為若 `x` ≤ -1，則 ln(1 + x) 沒有定義或會導致數學錯誤。

### 詳細說明

- 數學背景

    - `Math.log1p(x)` 所計算的是自然對數 ln(1 + x)。在數學上，自然對數是以數學常數 e (大約等於 2.718) 為底的對數函數，ln(y) 是一個數值 y 的自然對數。

    - 當 `x` 越接近 0，ln(1 + x) 的結果越接近 0。若直接使用 `Math.log(1 + x)`，在 `x` 很小的時候，因為浮點數的限制，可能會產生誤差，而 `Math.log1p(x)` 就是為了解決這個問題，提供更精確的結果。

- 使用原因

    - 在某些科學計算和金融應用中，`x` 可能會非常小 (例如：0.000001 或更小)，這時使用 `Math.log(1 + x)` 可能會有精度問題。為了避免這種情況，`Math.log1p(x)` 可以更精確處理 `x` 接近 0 的情況。

    - 這個函數特別適合處理與增長、複利、熵計算等有關的運算，這些運算通常需要對小數值進行對數計算。

- 範例

    - 基本範例

	```javascript
    console.log(Math.log1p(1)); // 0.6931471805599453
	```

    在這個範例中，計算的是 ln(1 + 1)，也就是 ln(2)，其值大約為 0.693。

    - 小數值範例

	```javascript
    console.log(Math.log1p(0.000001)); // 9.999995000003334e-7
	```

    當 x 非常小時，`Math.log1p(x)` 可以比 `Math.log(1 + x)` 更精確計算結果。

    - 負數範例

	```javascript
    console.log(Math.log1p(-0.5)); // -0.6931471805599453
	```

    當輸入負數時，`Math.log1p(-0.5)` 計算的是 ln(1 - 0.5)，即 ln(0.5)，結果是負值。

- 範例程式碼

    - 小數值的精度優勢

        ```javascript
		console.log(Math.log1p(0.000001));   // 9.999995000003334e-7
		console.log(Math.log(1 + 0.000001)); // 9.999994999180668e-7
        ```

        雖然兩者結果接近，但當 `x` 更小時，`Math.log1p(x)` 的精度優勢會更加明顯。

- 應用場景

    - 金融計算：在計算複利時，`Math.log1p(x)` 可以用來避免精度誤差，特別是當利率很小的時候，這樣能確保結果更為準確。

    - 科學計算：在一些科學應用中，特別是與熵 (entropy) 有關的計算中，對於非常小的值進行對數運算是常見需求，`Math.log1p(x)` 能提供比 `Math.log(1 + x)` 更高的精度。

    - 機率運算：在機率相關的計算中，也經常會用到自然對數，`Math.log1p(x)` 能夠更準確處理小概率的情況。

- 數學推導與比較

    - `Math.log(1 + x)`：在一般情況下，使用 `Math.log(1 + x)` 計算自然對數沒有問題，但當 `x` 非常小時，結果可能會因浮點數精度問題而不夠準確。

    - `Math.log1p(x)`：專門設計來處理 `x` 非常接近 0 的情況，能夠避免精度損失，確保計算更為精確。

### 注意事項

- `x` 值範圍：`Math.log1p(x)` 的有效範圍是 `x` > -1，因為當 `x` ≤ -1 時，1 + x 會變為 0 或負數，而自然對數在這些情況下沒有定義。當輸入 `x` ≤ -1 時，結果會是 `NaN`。

- 精度差異：在處理非常小的 `x` 時，使用 `Math.log1p(x)` 比使用 `Math.log(1 + x)` 的精度更高，尤其在計算小數值對數的場景中

### 總結

`Math.log1p(x)` 是用來精確計算 ln(1 + x) 的方法，特別是在 `x` 非常接近 0 的情況下，能比直接使用 `Math.log(1 + x)` 提供更高的精度。在金融、科學計算、機率運算等需要精確處理小數值對數的情況下，`Math.log1p(x)` 非常實用。通過 `Math.log1p(x)`，可以避免因浮點數精度限制導致的誤差，使得運算結果更加準確。
