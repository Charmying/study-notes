# Strategy (策略模式)

Strategy (策略模式) 是一種行為型設計模式，允許在執行時動態選擇演算法或行為，將這些演算法封裝到獨立的策略類別中，使其可互換使用。此模式讓主體物件與具體行為解耦，增強程式碼的靈活性與可維護性。

這種模式特別適合用於需要根據不同情境選擇不同行為的場景，例如：排序演算法選擇、支付方式處理或資料壓縮方式。

<br />

## 動機

在軟體系統中，物件常需根據情境採用不同演算法或行為，例如

- 支付系統：根據使用者選擇，可能需要處理信用卡、電子錢包或銀行轉帳。

- 排序功能：根據資料特性，選擇快速排序、合併排序或氣泡排序。

- 資料傳輸：根據網路條件，選擇不同的壓縮演算法。

若在主體物件中使用條件陳述式 (例如：`if-else`) 選擇行為，會導致程式碼複雜、難以維護，且新增行為需修改既有程式碼。

Strategy 模式透過將行為封裝到獨立策略類別，解決這些問題，讓行為可動態替換，符合開閉原則。

<br />

## 結構

Strategy 模式的結構包含以下元素

- 策略介面 (Strategy Interface)：定義行為的標準方法。

- 具體策略 (Concrete Strategy)：實現策略介面，提供具體行為。

- 上下文 (Context)：持有策略物件，並委派行為給策略物件。

以下是 Strategy 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/fP512i9034NtWTmXonQP7g28r7e05vuWJgCeTGepALJKkolK6PI2Wkv2-7a_-Qc2ijV-r28Sd8hViHNQg6UL_Pak24Gpaa5ihv8rh5pIUdiKgtai46u82BRb46ZLEUj59HAM_oFgdn0gWuw3XiAJLAR3Hc0GZOrigidVN9FmatlARNujYcaMtmGrGjoyCsRnicqbhddyw0u0" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現支付處理系統，支援多種支付方式。

    ```java
    public interface PaymentStrategy {
        void pay(double amount);
    }

    public class CreditCardPayment implements PaymentStrategy {
        @Override
        public void pay(double amount) {
            System.out.println("使用信用卡支付 " + amount + " 元");
        }
    }

    public class DigitalWalletPayment implements PaymentStrategy {
        @Override
        public void pay(double amount) {
            System.out.println("使用電子錢包支付 " + amount + " 元");
        }
    }

    public class PaymentContext {
        private PaymentStrategy strategy;

        public void setStrategy(PaymentStrategy strategy) {
            this.strategy = strategy;
        }

        public void processPayment(double amount) {
            strategy.pay(amount);
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            PaymentContext context = new PaymentContext();

            context.setStrategy(new CreditCardPayment());
            context.processPayment(100.0); // 使用信用卡支付 100.0 元

            context.setStrategy(new DigitalWalletPayment());
            context.processPayment(200.0); // 使用電子錢包支付 200.0 元
        }
    }
    ```

    特點：上下文動態切換策略，無需修改核心程式碼。

- JavaScript 實現 Strategy

    用於選擇不同的排序演算法。

    ```javascript
    class SortStrategy {
      sort(data) {
        throw new Error("Method 'sort()' must be implemented.");
      }
    }

    class QuickSortStrategy extends SortStrategy {
      sort(data) {
        console.log("使用快速排序");
        return [...data].sort((a, b) => a - b);
      }
    }

    class BubbleSortStrategy extends SortStrategy {
      sort(data) {
        console.log("使用氣泡排序");
        let arr = [...data];
        for (let i = 0; i < arr.length; i++) {
          for (let j = 0; j < arr.length - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
              [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
          }
        }
        return arr;
      }
    }

    class SortContext {
      constructor() {
        this.strategy = null;
      }

      setStrategy(strategy) {
        this.strategy = strategy;
      }

      sortData(data) {
        return this.strategy.sort(data);
      }
    }



    /** 使用範例 */
    const context = new SortContext();
    const data = [5, 2, 8, 1, 9];

    context.setStrategy(new QuickSortStrategy());
    console.log(context.sortData(data)); // 使用快速排序, [1, 2, 5, 8, 9]

    context.setStrategy(new BubbleSortStrategy());
    console.log(context.sortData(data)); // 使用氣泡排序, [1, 2, 5, 8, 9]
    ```

    特點：動態選擇排序演算法，適合前端資料處理。

- TypeScript 實現 Strategy

    用於資料壓縮，確保型別安全。

    ```javascript
    interface CompressionStrategy {
      compress(data: string): string;
    }

    class ZipCompression implements CompressionStrategy {
      compress(data: string): string {
        console.log("使用 ZIP 壓縮");
        return `ZIP(${data})`;
      }
    }

    class RarCompression implements CompressionStrategy {
      compress(data: string): string {
        console.log("使用 RAR 壓縮");
        return `RAR(${data})`;
      }
    }

    class CompressionContext {
      private strategy: CompressionStrategy;

      setStrategy(strategy: CompressionStrategy) {
        this.strategy = strategy;
      }

      compressData(data: string): string {
        return this.strategy.compress(data);
      }
    }



    /** 使用範例 */
    const context = new CompressionContext();

    context.setStrategy(new ZipCompression());
    console.log(context.compressData("資料內容")); // 使用 ZIP 壓縮, ZIP(資料內容)

    context.setStrategy(new RarCompression());
    console.log(context.compressData("資料內容")); // 使用 RAR 壓縮, RAR(資料內容)
    ```

    特點：TypeScript 的型別檢查確保策略介面一致。

- Angular 實現 Strategy

    使用 Angular 服務實現支付方式選擇。

    ```javascript
    /** payment.service.ts */
    import { Injectable } from '@angular/core';

    export interface PaymentStrategy {
      pay(amount: number): void;
    }

    @Injectable({
      providedIn: 'root'
    })
    export class CreditCardPayment implements PaymentStrategy {
      pay(amount: number) {
        console.log(`使用信用卡支付 ${amount} 元`);
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class DigitalWalletPayment implements PaymentStrategy {
      pay(amount: number) {
        console.log(`使用電子錢包支付 ${amount} 元`);
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class PaymentContext {
      private strategy: PaymentStrategy;

      setStrategy(strategy: PaymentStrategy) {
        this.strategy = strategy;
      }

      processPayment(amount: number) {
        this.strategy.pay(amount);
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { PaymentContext, CreditCardPayment, DigitalWalletPayment } from './payment.service';

    @Component({
      selector: 'app-root',
      template: `
        <button (click)="payWithCreditCard()">信用卡支付</button>
        <button (click)="payWithWallet()">電子錢包支付</button>
      `
    })
    export class AppComponent {
      constructor(
        private paymentContext: PaymentContext,
        private creditCard: CreditCardPayment,
        private wallet: DigitalWalletPayment
      ) {}

      payWithCreditCard() {
        this.paymentContext.setStrategy(this.creditCard);
        this.paymentContext.processPayment(100);
      }

      payWithWallet() {
        this.paymentContext.setStrategy(this.wallet);
        this.paymentContext.processPayment(200);
      }
    }
    ```

    特點：利用 Angular 依賴注入，動態切換支付策略。

- React 實現 Strategy

    使用 React Hook 實現資料格式化策略。

    ```javascript
    /** FormatStrategy.js */
    class FormatStrategy {
      format(data) {
        throw new Error("Method 'format()' must be implemented.");
      }
    }

    class JsonFormat extends FormatStrategy {
      format(data) {
        console.log("格式化為 JSON");
        return JSON.stringify(data);
      }
    }

    class XmlFormat extends FormatStrategy {
      format(data) {
        console.log("格式化為 XML");
        return `<data>${Object.entries(data).map(([k, v]) => `<${k}>${v}</${k}>`).join('')}</data>`;
      }
    }



    /** FormatContext.js */
    import { createContext, useContext, useState } from 'react';

    const FormatContext = createContext(null);
    export const useFormatContext = () => useContext(FormatContext);



    /** App.jsx */
    import React from 'react';
    import { FormatContext } from './FormatContext';

    const Formatter = () => {
      const { strategy, format } = useFormatContext();
      const data = { name: '使用者A', age: 25 };
      return (
        <div>
          <button onClick={() => format(data)}>格式化</button>
        </div>
      );
    };

    const App = () => {
      const [strategy, setStrategy] = useState(new JsonFormat());

      const format = (data) => {
        console.log(strategy.format(data));
      };

      return (
        <FormatContext.Provider value={{ strategy, format }}>
          <button onClick={() => setStrategy(new JsonFormat())}>使用 JSON</button>
          <button onClick={() => setStrategy(new XmlFormat())}>使用 XML</button>
          <Formatter />
        </FormatContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Hook，實現動態格式化策略切換。

<br />

## 應用場景

Strategy 模式適用於以下場景

- 動態行為選擇

    例如：支付系統根據使用者選擇切換支付方式。

- 演算法替換

    例如：排序或壓縮演算法根據需求動態選擇。

- UI 行為

    例如：根據使用者偏好選擇不同的資料顯示格式。

- 測試性

    例如：單元測試中替換真實行為為模擬行為。

例如

- 在前端，Strategy 用於動態選擇資料格式化或 UI 渲染方式。

- Java 的 `Comparator` 介面是 Strategy 模式的典型應用。

<br />

## 優缺點

### 優點

- 符合開閉原則：新增策略無需修改上下文程式碼。

- 解耦行為：演算法與上下文分離，提升可維護性。

- 靈活性：支援執行時動態切換策略。

- 易於測試：獨立策略類別便於單元測試。

### 缺點

- 類別數量增加：每個策略需一個類別，可能增加程式碼量。

- 客戶端複雜度：客戶端需了解並選擇適當策略。

- 策略初始化：需確保上下文初始化時有有效策略。

<br />

## 注意事項

- 策略選擇：確保客戶端能正確選擇策略，避免無效配置。

- 效能考量：在頻繁切換策略的場景中，需優化策略創建。

- 狀態管理：若策略有狀態，需小心處理共享或獨立狀態。

- 一致性：確保所有策略實現相同的介面，行為一致。

<br />

## 與其他模式的關係

- 與狀態模式 (State)：State 聚焦狀態切換影響行為，Strategy 注重行為替換。

- 與命令模式 (Command)：Strategy 封裝演算法，Command 封裝操作。

- 與工廠模式 (Factory)：工廠可創建策略物件，結合使用。

<br />

## 總結

Strategy 模式是一種靈活的行為型設計模式，透過將演算法或行為封裝到獨立策略類別，實現動態行為切換與解耦。特別適合用於需要根據情境選擇不同行為的場景，例如：支付處理、排序演算法或資料格式化。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據專案需求選擇最適合的工具。需注意策略管理的清晰性與效能，確保程式碼簡潔且高效。對於追求靈活行為選擇與可維護性設計的開發人員而言，Strategy 模式是一個核心工具，能顯著提升系統的彈性與可擴展性
