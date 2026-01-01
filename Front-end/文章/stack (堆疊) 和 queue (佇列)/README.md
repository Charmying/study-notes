# `stack` (堆疊) 和 `queue` (佇列)

在學習程式設計或資料結構時，`stack` (堆疊) 和 `queue` (佇列) 是兩種最基礎也最常用的線性結構，在記憶體管理、演算法設計、系統排程、日常程式開發，都有非常重要的。

<br />

## `stack` (堆疊)

抽象資料型態 (Abstract data type，簡稱：ADT)：堆疊是一種「先進後出」(Last‑In, First‑Out，簡稱：LIFO) 的資料結構，最後放入的元素最先被取出。

生活類比：一疊盤子，最上方的盤子最先被拿走；書本堆疊，最上面的那本最先拿。

### 核心操作

- `push(x)`：將元素 x 推入堆疊頂端。

- `pop()`：移除並回傳堆疊頂端的元素。

- `peek()` 或 `top()`：查看 (但不移除) 堆疊頂端的元素。

- `isEmpty()`：檢查堆疊是否為空。

<br />

## `queue` (佇列)

抽象資料型態 (Abstract data type，簡稱：ADT)：佇列是一種「先進先出」(First‑In, First‑Out，簡稱：FIFO) 的資料結構，最早放入的元素最先被取出。

生活類比：排隊買東西，先到的顧客先結帳；列印佇列也是同理。

### 核心操作

- `enqueue(x)`：將元素 x 加入尾端

- `dequeue()`：移除並回傳前端的元素

- `front()` 或 `peek()`：讀取前端元素但不移除

- `isEmpty()`：檢查佇列是否為空

<br />

## 時間與空間複雜度

| 操作 | stack (堆疊) | Queue (佇列) |
| - | - | - |
| 插入元素 | O(1) | O(1) |
| 刪除/取出 | O(1) | O(1)* |
| 查看頂端 | O(1) | O(1) |
| 額外空間 | O(n) | O(n) |

- *：若用原生陣列的 `shift()` 實作佇列，`dequeue()` 平均為 O(n)，因為需搬移剩餘元素。可改用雙端陣列、環形緩衝區或「雙堆疊模擬佇列」來優化至 O(1)。

<br />

## 常見實作方式

- 使用陣列 (JavaScript 範例)

    ```javascript
    /** 堆疊 */
	  class Stack {
	    constructor() { this.data = []; }
	    push(x) { this.data.push(x); }
	    pop() { return this.data.pop(); }
	    peek() { return this.data[this.data.length - 1]; }
	    isEmpty() { return this.data.length === 0; }
	  }

	  /** 佇列 (簡易版，shift() 會 O(n)) */
	  class Queue {
	    constructor() { this.data = []; }
	    enqueue(x) { this.data.push(x); }
	    dequeue() { return this.data.shift(); }
	    front() { return this.data[0]; }
	    isEmpty() { return this.data.length === 0; }
	  }
    ```

- 使用鏈結串列 (Linked List)

    - 優點：頭尾插入與刪除都能維持 O(1)。

    - 要點：維護 head (指向頭節點) 與 tail (指向尾節點) 兩個指標。

    - 範例概念

        ```mermaid
		    graph LR
		    head --> A --> B --> C --> null
		    tail --> C
        ```

- 進階優化：雙堆疊模擬佇列

    透過兩個堆疊 (`inStack`, `outStack`) 實作佇列，可將 `enqueue` 與 `dequeue` 平均時間複雜度維持 O(1)。

    - 思路：一個「輸入堆疊」負責 `enqueue`，一個「輸出堆疊」負責 `dequeue`。

    - 流程：

        1. `enqueue`：直接 push 到 `inStack`。

        2. `dequeue`：若 `outStack` 為空，將 `inStack` 的所有元素 pop 出來並 push 到 `outStack`，再從 `outStack` pop；否則直接從 `outStack` pop。

    - 效能：攤還時間平均 O(1)。

<br />

## 應用場景與實例

### 堆疊的常見用途

- 函式呼叫堆疊 (Call Stack)：程式執行過程中，系統用堆疊來追蹤目前正在執行的函式與下一步要回到哪裡。

- 淺層遞迴改寫：可用顯式堆疊取代系統遞迴，以避免過深遞迴造成堆疊溢位 (Stack Overflow)。

- 瀏覽器「上一頁」功能：將歷史路徑 push 到堆疊，按「上一頁」 pop 出來。

- 文字編輯 "Undo"：每次編輯狀態存入堆疊，Undo 時取出上一步狀態。

### 佇列的常見用途

- 作業系統排程：Round Robin 或其他排程演算法常用佇列儲存等待執行的程序。

- 廣度優先搜尋 (BFS)：圖的遍歷使用佇列來依層級逐步展開節點。

<br />

## 演算法範例：BFS vs DFS

在圖 (Graph) 或樹 (Tree) 的遍歷中，BFS 與 DFS 分別對應到佇列與堆疊 (或遞迴呼叫堆疊)：

- 廣度優先搜尋 (BFS，使用佇列)

    特點：逐層擴展，先探訪完一層再往下一層，適合找最短路徑。

    ```javascript
    function bfs(start) {
      const q = new Queue();
      const visited = new Set();

      q.enqueue(start);
      visited.add(start);

	    while (!q.isEmpty()) {
	      const node = q.dequeue();
	      console.log(node.value); // 處理該節點

	      for (const nbr of node.neighbors) {
	        if (!visited.has(nbr)) {
	          visited.add(nbr);
	          q.enqueue(nbr);
	        }
	      }
	    }
	  }
    ```

- 深度優先搜尋 (DFS，使用堆疊或遞迴)

    特點：一路往深處探索，直到到底再回溯；適合檢查連通性與拓撲排序。

    - 遞迴 (系統呼叫堆疊)

        ```javascript
        function dfsRecursive(node, visited = new Set()) {
          visited.add(node);
          console.log(node.value); // 處理該節點

          for (const nbr of node.neighbors) {
            if (!visited.has(nbr)) {
              dfsRecursive(nbr, visited);
            }
          }
        }
        ```

    - 顯式堆疊 (迭代)

        ```javascript
        function dfsIterative(start) {
          const stack = new Stack();
          const visited = new Set();

		  stack.push(start);
		  visited.add(start);

          while (!stack.isEmpty()) {
		    const node = stack.pop();
		    console.log(node.value); // 處理該節點

            /** 注意：若想模擬遞迴順序，可反向推入鄰居 */
            for (let i = node.neighbors.length - 1; i >= 0; i--) {
              const nbr = node.neighbors[i];
              if (!visited.has(nbr)) {
                visited.add(nbr);
                stack.push(nbr);
              }
            }
          }
        }
        ```

<br />

## 實作注意事項與小技巧

- 空結構檢查

    在呼叫 `pop()`、`peek()`、`dequeue()`、`front()` 之前，要先用 `isEmpty()` 確認結構不為空，否則可能回傳 `undefined` 或報錯。

- 避免效能瓶頸

    - 若佇列操作頻繁，避免直接用陣列 `shift()`，可改環形緩衝區或「雙堆疊模擬佇列」。

    - 深度遞迴可能導致系統堆疊溢位 (Stack Overflow)，必要時改用顯式堆疊。

- 選對工具

    - 小規模、低頻操作：直接用陣列最簡潔。

    - 大型、高頻情境：建議用鏈結串列、環形緩衝區或雙堆疊方案。

- 語義清晰

    - 若問題本質是「回溯」或「模擬遞迴」，優先選用堆疊 (或遞迴)。

    - 若關鍵是「層級展開」或「排隊等待」，則使用佇列。

<br />

## 延伸學習

- 優先佇列 (Priority Queue)：依優先級出列的佇列變種，常用於 Dijkstra、A* 演算法。

- 雙端佇列 (Deque)：同時支援頭尾插入與刪除的佇列。

- 其他遍歷演算法：拓撲排序 (Topological Sort)、雙向 BFS、迭代深化 DFS (IDDFS) 等。
