# State (狀態模式)

State (狀態模式) 是一種行為型設計模式，允許物件在內部狀態改變時改變其行為，使物件看起來像是改變了其類別。此模式將狀態相關的行為封裝到獨立的狀態類別中，讓主體物件委派行為給當前狀態。

這種模式特別適合用於物件行為隨狀態改變的場景，例如：訂單處理流程、遊戲角色狀態或 UI 元件的動態行為。

<br />

## 動機

在軟體系統中，物件行為常隨狀態變化，例如

- 訂單管理：訂單可能處於「待處理」、「已出貨」或「已完成」等狀態，每種狀態有不同操作。

- 遊戲角色：角色可能處於「正常」、「受傷」或「增強」狀態，影響其行動能力。

- UI 元件：按鈕根據「啟用」、「禁用」或「點擊中」狀態展現不同行為。

若使用條件陳述式 (例如：`if-else`) 管理狀態，會導致程式碼複雜、難以維護，且新增狀態需要修改主體程式碼。

State 模式透過將狀態行為封裝到獨立類別，解決這些問題，提升程式碼可維護性與擴展性。

<br />

## 結構

State 模式的結構包含以下元素

- 狀態介面 (State Interface)：定義狀態相關行為的標準方法。

- 具體狀態 (Concrete State)：實現狀態介面，定義特定狀態的行為。

- 上下文 (Context)：持有當前狀態物件，並委派行為給狀態物件。

以下是 State 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/dL112i903Bm7zWyvRf7s0KMarYVuWcKRKLYtk4cXeFxTRiE221xqbimmavbqB2x9T0q6Bb4edPmdF8eJmhi1n0sUNHm2MJykz2mj7dIe33mD6F31CMVG9n9QbVl_fVslqWogfaRE3gscLnScMJVxJbNA9RfDn6ABfPRUFfhceyrtgZTG8enrlIkNEuh3yj4N0" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現訂單狀態管理。

    ```java
    public interface OrderState {
        void handle(OrderContext context);
    }

    public class PendingState implements OrderState {
        @Override
        public void handle(OrderContext context) {
            System.out.println("訂單狀態：待處理 - 準備出貨");
            context.setState(new ShippedState());
        }
    }

    public class ShippedState implements OrderState {
        @Override
        public void handle(OrderContext context) {
            System.out.println("訂單狀態：已出貨 - 等待送達");
            context.setState(new DeliveredState());
        }
    }

    public class DeliveredState implements OrderState {
        @Override
        public void handle(OrderContext context) {
            System.out.println("訂單狀態：已送達 - 訂單完成");
        }
    }

    public class OrderContext {
        private OrderState state;

        public OrderContext() {
            this.state = new PendingState();
        }

        public void setState(OrderState state) {
            this.state = state;
        }

        public void process() {
            state.handle(this);
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            OrderContext order = new OrderContext();
            order.process(); // 訂單狀態：待處理 - 準備出貨
            order.process(); // 訂單狀態：已出貨 - 等待送達
            order.process(); // 訂單狀態：已送達 - 訂單完成
        }
    }
    ```

    特點：上下文委派行為給當前狀態，狀態轉換由狀態類別管理。

- JavaScript 實現 State

    用於管理 UI 按鈕的狀態。

    ```javascript
    class ButtonState {
      handle(context) {
        throw new Error("Method 'handle()' must be implemented.");
      }
    }

    class EnabledState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：啟用 - 可點擊");
        context.setState(new ClickedState());
      }
    }

    class ClickedState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：點擊中 - 處理中");
        context.setState(new DisabledState());
      }
    }

    class DisabledState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：禁用 - 不可點擊");
      }
    }

    class ButtonContext {
      constructor() {
        this.state = new EnabledState();
      }

      setState(state) {
        this.state = state;
      }

      click() {
        this.state.handle(this);
      }
    }



    /** 使用範例 */
    const button = new ButtonContext();
    button.click(); // 按鈕狀態：啟用 - 可點擊
    button.click(); // 按鈕狀態：點擊中 - 處理中
    button.click(); // 按鈕狀態：禁用 - 不可點擊
    ```

    特點：簡化 UI 元件狀態管理，適合前端動態行為。

- TypeScript 實現 State

    用於遊戲角色狀態管理，確保型別安全。

    ```javascript
    interface State {
      handle(context: GameContext): void;
    }

    class NormalState implements State {
      handle(context: GameContext) {
        console.log("角色狀態：正常 - 普通攻擊力");
        context.setState(new PoweredState());
      }
    }

    class PoweredState implements State {
      handle(context: GameContext) {
        console.log("角色狀態：增強 - 攻擊力加倍");
        context.setState(new InjuredState());
      }
    }

    class InjuredState implements State {
      handle(context: GameContext) {
        console.log("角色狀態：受傷 - 攻擊力減半");
        context.setState(new NormalState());
      }
    }

    class GameContext {
      private state: State;

      constructor() {
        this.state = new NormalState();
      }

      setState(state: State) {
        this.state = state;
      }

      action() {
        this.state.handle(this);
      }
    }



    /** 使用範例 */
    const game = new GameContext();
    game.action(); // 角色狀態：正常 - 普通攻擊力
    game.action(); // 角色狀態：增強 - 攻擊力加倍
    game.action(); // 角色狀態：受傷 - 攻擊力減半
    ```

    特點：TypeScript 的型別檢查確保狀態與行為一致。

- Angular 實現 State

    使用 Angular 服務管理表單提交狀態。

    ```javascript
    /** state.service.ts */
    import { Injectable } from '@angular/core';

    export interface FormState {
      handle(context: FormContext): void;
    }

    @Injectable({
      providedIn: 'root'
    })
    export class IdleState implements FormState {
      handle(context: FormContext) {
        console.log("表單狀態：待機 - 可提交");
        context.setState(new SubmittingState());
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class SubmittingState implements FormState {
      handle(context: FormContext) {
        console.log("表單狀態：提交中 - 請稍候");
        context.setState(new SubmittedState());
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class SubmittedState implements FormState {
      handle(context: FormContext) {
        console.log("表單狀態：已提交 - 完成");
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class FormContext {
      private state: FormState;

      constructor(private idleState: IdleState) {
        this.state = idleState;
      }

      setState(state: FormState) {
        this.state = state;
      }

      submit() {
        this.state.handle(this);
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { FormContext } from './state.service';

    @Component({
      selector: 'app-root',
      template: `
        <button (click)="submitForm()">提交表單</button>
      `
    })
    export class AppComponent {
      constructor(private formContext: FormContext) {}

      submitForm() {
        this.formContext.submit();
      }
    }
    ```

    特點：利用 Angular 依賴注入，實現表單狀態的動態切換。

- React 實現 State

    使用 React Hook 實現按鈕狀態管理。

    ```javascript
    /** ButtonState.js */
    class ButtonState {
      handle(context) {
        throw new Error("Method 'handle()' must be implemented.");
      }
    }

    class EnabledState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：啟用 - 可點擊");
        context.setState(new ClickedState());
      }
    }

    class ClickedState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：點擊中 - 處理中");
        context.setState(new DisabledState());
      }
    }

    class DisabledState extends ButtonState {
      handle(context) {
        console.log("按鈕狀態：禁用 - 不可點擊");
      }
    }



    /** ButtonContext.js */
    import { createContext, useContext, useState } from 'react';

    const ButtonContext = createContext(null);
    export const useButtonContext = () => useContext(ButtonContext);



    /** App.jsx */
    import React from 'react';
    import { ButtonContext } from './ButtonContext';

    const Button = () => {
      const { state, click } = useButtonContext();

      return <button onClick={click}>點擊按鈕</button>;
    };

    const App = () => {
      const [state, setState] = useState(new EnabledState());

      const click = () => {
        state.handle({ setState });
      };

      return (
        <ButtonContext.Provider value={{ state, click }}>
          <Button />
        </ButtonContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Hook，實現簡單的狀態切換與 UI 更新。

<br />

## 應用場景

State 模式適用於以下場景

- 狀態依賴行為

    例如：訂單系統中不同狀態的處理規則。

- 遊戲角色管理

    例如：角色根據狀態改變攻擊或移動行為。

- UI 元件動態行為

    例如：按鈕或表單根據狀態改變外觀或功能。

- 流程控制

    例如：工作流程中的階段切換。

例如

- 在前端，State 用於管理 UI 元件的動態行為。

- Java 的有限狀態機 (Finite State Machine) 常使用 State 模式實現。

<br />

## 優缺點

### 優點

- 符合開閉原則：新增狀態僅需新增狀態類別，不修改上下文。

- 簡化程式碼：消除複雜的條件陳述式，提高可讀性。

- 狀態封裝：每個狀態的行為獨立封裝，便於維護。

- 靈活性：支援動態切換狀態，適應不同場景。

### 缺點

- 類別數量增加：每個狀態需一個類別，可能增加程式碼量。

- 狀態轉換管理：複雜系統中，狀態轉換可能難以追蹤。

- 初始設置：需要初始化上下文與初始狀態，增加設計成本。

<br />

## 注意事項

- 狀態轉換：確保狀態切換規則清晰，避免無限循環。

- 狀態共享：若多個上下文共享狀態，需小心管理狀態實例。

- 效能考量：在頻繁切換狀態的場景中，需優化狀態創建。

- 測試性：每個狀態類別需獨立測試，確保行為正確。

<br />

## 與其他模式的關係

- 與策略模式 (Strategy)：策略模式注重行為替換，State 聚焦狀態切換。

- 與狀態機 (Finite State Machine)：State 模式是狀態機的物件導向實現。

- 與命令模式 (Command)：可結合使用，命令觸發狀態變化。

<br />

## 總結

State 模式是一種強大的行為型設計模式，透過將狀態行為封裝到獨立類別，實現物件行為隨狀態動態變化。特別適合用於狀態驅動的場景，例如：訂單處理、遊戲角色管理或 UI 元件的動態行為。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據應用需求選擇最適合的工具。需注意狀態轉換的清晰性與程式碼的可維護性，確保高效實現。對於追求乾淨程式碼與靈活狀態管理的開發人員而言，State 模式是一個核心工具，能顯著提升系統的可擴展性與可讀性。
