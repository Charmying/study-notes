# 遞迴 (Recursion)

遞迴 (Recursion) 是在程式設計中常見的技術，指的是函數 (Function) 在定義或執行過程中，直接或間接呼叫自身。通常用於解決可以被分解為相同子問題的複雜問題，透過不斷將問題簡化，直到達到一個基本情況 (Base Case)，從而解決整個問題。

<br />

## 遞迴的基本概念

遞迴的核心思想是分治法 (Divide and Conquer)，也就是將一個大問題拆解成多個相似的小問題，並透過解決小問題來逐步解決大問題。

遞迴函數通常包含兩個部分

- 遞迴條件 (Recursive Case)：函數在執行過程中呼叫自身，將問題進一步分解。

- 終止條件 (Base Case)：當問題被簡化到一定程度時，遞迴停止，避免無限迴圈。

<br />

## 遞迴的運作方式

以計算階乘 (Factorial) 為例，階乘的定義為：

n! = n × (n − 1) × (n − 2) × ⋯ × 1

這個問題可以用遞迴來解決：

1. 遞迴條件：n! = n × (n−1)!

2. 終止條件：當 n = 1 時，1! = 1

在程式碼中，遞迴函數會不斷呼叫自身，直到 n = 1 時停止，然後逐步返回結果。

```javascript
function factorial(n) {
  /** 終止條件 (Base Case)：當 n 為 1 時，直接返回 1 */
  if (n === 1) {
    return 1;
  }
  /** 遞迴條件 (Recursive Case)：呼叫自身並返回 n * factorial(n - 1) */
  else {
    return n * factorial(n - 1);
  }
}

let number = 5;
let result = factorial(number);
console.log(`${number} 的階乘是：${result}`); // 5 的階乘是：120
```

1. 終止條件：當 n = 1 時，函數直接返回 1，這是遞迴的終止條件，避免無限遞迴。

2. 遞迴條件：當 n × factorial(n − 1)，將問題不斷簡化。

3. 執行過程：

    1. 以 n = 5 為例，遞迴的執行過程如下：

        - factorial(5) = 5 * factorial(4)

		- factorial(4) = 4 * factorial(3)

        - factorial(3) = 3 * factorial(2)

        - factorial(2) = 2 * factorial(1)

        - factorial(1) = 1

    2. 最終結果為 5 × 4 × 3 × 2 × 1 = 120


### 注意事項

- 堆疊溢出 (Stack Overflow)：若遞迴的深度過大 (n 很大)，可能會導致堆疊溢出錯誤，因為每次遞迴呼叫都會佔用一定的記憶體空間。

- 效率問題：遞迴的效率通常較低，因為每次呼叫都需要額外的時間和空間來處理。對於某些問題，可以使用迴圈來替代遞迴，以提高效率。

```javascript
function factorial(n) {
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}

let number = 5;
let result = factorial(number);
console.log(`${number} 的階乘是：${result}`); // 5 的階乘是：120
```

<br />

## 遞迴的優缺點

### 優點

- 程式碼簡潔易懂，特別適合處理具有遞迴性質的問題，例如：樹狀結構 (Tree Structure) 或分治法 (Divide and Conquer) 的應用。

- 能夠將複雜問題簡化為多個相同的小問題，降低問題的複雜度。

### 缺點

- 遞迴可能會導致大量的函數呼叫，增加記憶體的消耗，尤其是在深度遞迴時，可能引發堆疊溢出 (Stack Overflow) 的錯誤。

- 遞迴的效率通常較低，因為每次函數呼叫都需要額外的時間和空間來處理。

<br />

## 遞迴的應用場景

- 數學計算：階乘、費波那契數列 (Fibonacci Sequence) 等。

- 資料結構：樹 (Tree) 的遍歷 (Traversal)、圖 (Graph)的搜尋等。

- 演算法：快速排序 (Quick Sort)、合併排序 (Merge Sort) 等。

<br />

## 遞迴與迴圈的比較

- 遞迴是透過函數呼叫自身來實現重複，適合處理具有遞迴性質的問題。

- 迴圈則是透過條件判斷來控制重複的次數，通常效率較高，但程式碼可能較為冗長。

<br />

## 總結

遞迴是一種強大的技巧，能夠將複雜問題簡化為多個相同的小問題，並透過不斷分解問題來找到解決方案。但是使用遞迴時需要注意終止條件和效率問題，以避免無限迴圈或堆疊溢出的情況。在實際應用中，遞迴與迴圈可以根據問題的特性選擇使用，達到最佳的程式設計效果。
