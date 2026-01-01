# Refactoring

在軟體開發中，Refactoring 的意思代表重構，是一種改善程式碼結構的過程，目的是提高可讀性、可維護性和擴展性，並減少潛在的錯誤風險，而不改變程式的外部行為或功能。重構通常涉及重新整理、整理或重寫程式碼，以便使其更具結構性和一致性。

<br />

## Refactoring 的一些常見目的和方法

-  提高可讀性

    - 命名一致性：確保變數 (Variables)、函式 (Functions)、類別 (Classes) 等命名具有描述性和一致性，以便其他開發人員可以輕鬆理解程式碼的目的。

    - 簡化複雜流程：將複雜的條件或流程拆分成更小、更易理解的部分。

- 提高可維護性

    - 減少重複程式碼：識別並合併重複的程式碼片段，利用函式或類別來封裝重複的處理流程。

    - 優化結構：重新組織程式碼的結構，使其更具模組化和層次性，方便未來的修改和擴展。

- 提高擴展性

    - 解耦合：減少不同模組或元件之間的依賴，以便可以獨立修改和測試。

    - 引入設計模式：利用設計模式來提供解決特定問題的標準化解決方案，提升系統的靈活性和可擴展性。

- 減少錯誤風險

    - 消除程式碼的壞味道 (Code Smells)：壞味道是程式碼中可能導致潛在問題的徵兆，例如：過長的方法、過大的類別等，重構有助於消除這些問題。

- 工具與技術

    - 自動化工具：使用 IDE 提供的重構工具 (例如：重新命名、提取方法等) 來簡化重構過程。

    - 測試：重構前後應進行充分的測試，確保重構不會引入新的錯誤。

<br />

## Refactoring 的簡單範例

以下是一個過長的函式

```javascript
function processOrder(order) {
  if (order.items.length > 0) {
    let total = 0;
    for (let i = 0; i < order.items.length; i++) {
      total += order.items[i].price * order.items[i].quantity;
    }
    if (order.discount) {
      total = total * (1 - order.discount);
    }
    console.log("Order total: " + total);
  } else {
    console.log("No items in the order.");
  }
}
```

這個函式可以重構成

```javascript
function calculateTotal(order) {
  return order.items.reduce((total, item) => total + item.price * item.quantity, 0);
}

function applyDiscount(total, discount) {
  return discount ? total * (1 - discount) : total;
}

function processOrder(order) {
  if (!order.items.length) {
    console.log("No items in the order.");
    return;
  }

  let total = calculateTotal(order);
  total = applyDiscount(total, order.discount);

  console.log("Order total: " + total);
}
```

這樣的重構將流程分解為小函式，使程式碼更清晰、更容易維護。

<br />

## 總結

重構是一個持續的過程，隨著系統的發展，開發人員應該定期檢查和改善程式碼，維持高質量的軟體。這不僅有助於提高團隊合作效率，還能延長軟體的生命週期。
