# Chain of Responsibility (責任鏈模式)

Chain of Responsibility (責任鏈模式) 是一種行為型設計模式，將請求沿著處理者鏈傳遞，每個處理者決定是否處理或傳遞給下一個。

這種模式解耦發送者與接收者，適合多條件處理的場景。

<br />

## 動機

軟體開發中，常需處理請求但不確定哪個物件負責，例如

- 日誌系統中，依據層級決定是否記錄訊息。

- 事件處理中，沿著 UI 元件鏈傳遞事件。

- 前端表單驗證，依序檢查多個規則。

直接指定處理者導致程式碼耦合度高且難以擴展。

Chain of Responsibility 模式透過鏈狀結構動態處理請求，解決此問題。

<br />

## 結構

Chain of Responsibility 模式的結構包含以下元素

- 處理者介面 (Handler Interface)：定義處理請求的方法與設定下一個處理者。

- 具體處理者 (Concrete Handler)：實作處理者介面，決定是否處理或傳遞請求。

- 客戶端 (Client)：建立處理者鏈並發送請求。

以下是 Chain of Responsibility 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuCNFgymbjBnfQd-pkVZbt4KYCboiphoIrA2qnELN18p4l9IUrIA6Qbqj1GLkXEBN4BxMYH2C3Acm5Kw09aOU8QnIb5fQc5fS01MjvkM0sFMtT_dBr5BXz49kISnABYnMSy_EIYr9BKg66ESAimsuSLZrE-FL0dF1o-fmd-viWDiDyPbEZfuVX0FpIJhnS62xMrRM31vQLGXuma30KEM5Lv92QbmAC3m00" width="100%" />

<br />

## 實現方式

- 基本實現

    假設處理不同層級的日誌請求。

    ```java
    /** 處理者介面 */
    public interface LoggerHandler {
        void setNext(LoggerHandler next);
        void handle(String message, int level);
    }

    /** 具體處理者：錯誤層級 */
    public class ErrorLogger implements LoggerHandler {
        private LoggerHandler next;

        @Override
        public void setNext(LoggerHandler next) {
            this.next = next;
        }

        @Override
        public void handle(String message, int level) {
            if (level >= 3) {
                System.out.println("Error: " + message);
            } else if (next != null) {
                next.handle(message, level);
            }
        }
    }

    /** 具體處理者：警告層級 */
    public class WarningLogger implements LoggerHandler {
        private LoggerHandler next;

        @Override
        public void setNext(LoggerHandler next) {
            this.next = next;
        }

        @Override
        public void handle(String message, int level) {
            if (level == 2) {
                System.out.println("Warning: " + message);
            } else if (next != null) {
                next.handle(message, level);
            }
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            LoggerHandler errorLogger = new ErrorLogger();
            LoggerHandler warningLogger = new WarningLogger();
            warningLogger.setNext(errorLogger);

            warningLogger.handle("This is a warning", 2); // Warning: This is a warning
            warningLogger.handle("This is an error", 3);  // Error: This is an error
        }
    }
    ```

    特點：鏈狀處理日誌層級，易於擴展。

- JavaScript 實現 Chain of Responsibility

    處理 UI 事件冒泡。

    ```javascript
    /** 處理者介面 */
    class EventHandler {
      constructor() {
        this.next = null;
      }

      setNext(handler) {
        this.next = handler;
      }

      handle(event) {
        throw new Error("Method 'handle()' must be implemented.");
      }
    }

    /** 具體處理者：按鈕處理者 */
    class ButtonHandler extends EventHandler {
      handle(event) {
        if (event.type === 'click') {
          console.log("Button clicked");
        } else if (this.next) {
          this.next.handle(event);
        }
      }
    }

    /** 具體處理者：容器處理者 */
    class ContainerHandler extends EventHandler {
      handle(event) {
        if (event.type === 'hover') {
          console.log("Container hovered");
        } else if (this.next) {
          this.next.handle(event);
        }
      }
    }



    /** 使用範例 */
    const containerHandler = new ContainerHandler();
    const buttonHandler = new ButtonHandler();
    containerHandler.setNext(buttonHandler);

    containerHandler.handle({ type: 'click' }); // Button clicked
    containerHandler.handle({ type: 'hover' }); // Container hovered
    ```

    特點：模擬事件傳遞，適合前端 UI 交互。

- TypeScript 實現 Chain of Responsibility

    處理請求驗證鏈。

    ```typescript
    /** 處理者介面 */
    interface RequestHandler {
      setNext(handler: RequestHandler): void;
      handle(request: string): boolean;
    }

    /** 具體處理者：權限驗證 */
    class AuthHandler implements RequestHandler {
      private next: RequestHandler | null = null;

      setNext(handler: RequestHandler) {
        this.next = handler;
      }

      handle(request: string): boolean {
        if (request.includes('auth')) {
          console.log("Authenticated");
          return true;
        } else if (this.next) {
          return this.next.handle(request);
        }
        return false;
      }
    }

    /** 具體處理者：資料驗證 */
    class DataHandler implements RequestHandler {
      private next: RequestHandler | null = null;

      setNext(handler: RequestHandler) {
        this.next = handler;
      }

      handle(request: string): boolean {
        if (request.includes('data')) {
          console.log("Data validated");
          return true;
        } else if (this.next) {
          return this.next.handle(request);
        }
        return false;
      }
    }



    /** 使用範例 */
    const authHandler = new AuthHandler();
    const dataHandler = new DataHandler();
    authHandler.setNext(dataHandler);

    console.log(authHandler.handle('auth request')); // Authenticated
                                                     // true
    console.log(authHandler.handle('data request')); // Data validated
                                                     // true
    ```

    特點：TypeScript 確保型別安全，適合請求處理鏈。

- Angular 實現 Chain of Responsibility

    處理路由守衛鏈。

    ```typescript
    /** guard.service.ts */
    import { Injectable } from '@angular/core';

    export interface Guard {
      setNext(guard: Guard): void;
      canActivate(): boolean;
    }

    @Injectable()
    export class AuthGuard implements Guard {
      private next: Guard | null = null;

      setNext(guard: Guard) {
        this.next = guard;
      }

      canActivate(): boolean {
        console.log("Checking auth");
        if (true) {
          /** 模擬通過 */
          return this.next ? this.next.canActivate() : true;
        }
        return false;
      }
    }

    @Injectable()
    export class RoleGuard implements Guard {
      private next: Guard | null = null;

      setNext(guard: Guard) {
        this.next = guard;
      }

      canActivate(): boolean {
        console.log("Checking role");
        if (true) {
          /** 模擬通過 */
          return this.next ? this.next.canActivate() : true;
        }
        return false;
      }
    }

    @Injectable()
    export class GuardChain {
      constructor(private authGuard: AuthGuard, private roleGuard: RoleGuard) {
        authGuard.setNext(roleGuard);
      }

      check(): boolean {
        return this.authGuard.canActivate();
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { AuthGuard, RoleGuard, GuardChain } from './guard.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [AuthGuard, RoleGuard, GuardChain],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { GuardChain } from './guard.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="checkGuard()">檢查守衛</button>`
    })
    export class AppComponent {
      constructor(private guardChain: GuardChain) {}

      checkGuard() {
        console.log(this.guardChain.check());
        // Checking auth
        // Checking role
        // true
      }
    }
    ```

    特點：Angular 服務實現路由守衛鏈。

- React 實現 Chain of Responsibility

    處理表單驗證鏈。

    ```javascript
    /** ValidationChain.js */
    class Validator {
      constructor() {
        this.next = null;
      }

      setNext(validator) {
        this.next = validator;
      }

      validate(data) {
        throw new Error("Method 'validate()' must be implemented.");
      }
    }

    class RequiredValidator extends Validator {
      validate(data) {
        if (data) {
          return this.next ? this.next.validate(data) : true;
        }
        console.log("Required field");
        return false;
      }
    }

    class LengthValidator extends Validator {
      validate(data) {
        if (data.length > 5) {
          return this.next ? this.next.validate(data) : true;
        }
        console.log("Length too short");
        return false;
      }
    }



    /** App.jsx */
    import React, { useState } from 'react';

    const App = () => {
      const requiredValidator = new RequiredValidator();
      const lengthValidator = new LengthValidator();
      requiredValidator.setNext(lengthValidator);

      const [input, setInput] = useState('');

      const handleSubmit = () => {
        const valid = requiredValidator.validate(input);
        console.log(valid ? "Valid" : "Invalid");
      };

      return (
        <div>
          <input value={input} onChange={e => setInput(e.target.value)} />
          <button onClick={handleSubmit}>驗證</button>
        </div>
      );
    };

    export default App;
    ```

    特點：鏈狀驗證表單輸入，簡化 React 表單處理。

<br />

## 應用場景

Chain of Responsibility 模式適用於以下場景

- 多條件處理請求，例如：日誌層級或事件冒泡。

- 動態調整處理順序。

- 前端中事件傳遞或驗證鏈。

例如：Java 的 `java.util.logging` 使用責任鏈處理日誌。

<br />

## 優缺點

### 優點

- 解耦：發送者與接收者無直接依賴。

- 靈活性：易於新增或調整處理者。

- 符合單一職責原則：每個處理者專注單一任務。

- 鏈狀擴展：支援動態鏈結構。

### 缺點

- 請求未保證處理：可能無處理者負責。

- 效能開銷：長鏈可能增加調用深度。

- 調試難度：鏈狀執行不易追蹤。

<br />

## 注意事項

- 鏈終止：確保鏈末端處理或預設行為。

- 處理順序：正確設定處理者順序。

- 深拷貝 vs 淺拷貝：Clone 鏈時選擇合適拷貝方式。

- 避免濫用：簡單條件可使用 `if-else`。

<br />

## 與其他模式的關係

- 與 Command：Chain of Responsibility 可與 Command 結合處理命令。

- 與 Mediator：Chain of Responsibility 聚焦鏈狀處理，Mediator 協調交互。

- 與 Observer：可與 Observer 結合事件傳遞。

- 與 Strategy：處理者可使用策略模式實現行為。

<br />

## 總結

Chain of Responsibility 模式透過鏈狀結構動態處理請求，適合多條件場景。

在前端中，此模式適用於事件冒泡或驗證鏈。

理解 Chain of Responsibility 有助於設計靈活系統，提升程式碼可維護性。
