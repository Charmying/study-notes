# Mediator (中介者模式)

Mediator (中介者模式) 是一種行為型設計模式，透過定義一個中介者物件來封裝多個物件間的互動行為，降低物件間的直接耦合，使其能獨立變化。這種模式將複雜的互動關係集中於中介者，促進鬆耦合的系統設計。

這種模式特別適合用於多個物件需要協作，但直接通訊會導致緊耦合的場景，例如：聊天室系統、UI 元件間的互動或事件處理系統。

<br />

## 動機

在軟體開發中，物件間的互動常導致複雜的依賴關係，例如

- UI 元件互動：表單中的按鈕、輸入欄位和下拉選單需要相互影響，但直接引用會增加耦合。

- 多人聊天室：多個使用者間的訊息傳遞，若直接互相發送，會形成網狀依賴。

- 事件驅動系統：多個模組監聽和觸發事件，導致難以維護的關係。

若物件直接通訊，會導致程式碼難以維護、擴展或測試。

Mediator 模式透過將互動集中於中介者，解決這些問題，讓物件僅與中介者互動，降低耦合度。

<br />

## 結構

Mediator 模式的結構包含以下元素

- 中介者介面 (Mediator Interface)：定義物件間通訊的標準介面。

- 具體中介者 (Concrete Mediator)：實現中介者介面，協調物件間的互動。

- 同事類別 (Colleague Class)：與中介者通訊的物件，僅依賴中介者而非其他同事。

以下是 Mediator 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/hP112i9034NtWTmXougs1oWY1TUkFC7GfcLWcf5CAeXwTukjLNJh-ZzU_a-LpAaDVK3mOgojgvaEt7XdKUcAGBGcYURRIvPO6jQIzZ44Tjt06-8pYvLqDFNIhH3k20XrS2cDbDJAnd-IpTHaoQcVhULIThB74wip7oLx2PRxsrjH_BH2UAjZdk_eC_WQyCmN7A4Q9uoVUm00" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現一個簡單聊天室，使用者透過中介者發送訊息。

    ```java
    public interface ChatMediator {
        void sendMessage(String message, User user);
    }

    public class ChatRoom implements ChatMediator {
        @Override
        public void sendMessage(String message, User user) {
            System.out.println(user.getName() + " sends: " + message);
        }
    }

    public abstract class User {
        protected ChatMediator mediator;
        protected String name;

        public User(ChatMediator mediator, String name) {
            this.mediator = mediator;
            this.name = name;
        }

        public String getName() {
            return name;
        }

        public abstract void send(String message);
        public abstract void receive(String message);
    }

    public class ChatUser extends User {
        public ChatUser(ChatMediator mediator, String name) {
            super(mediator, name);
        }

        @Override
        public void send(String message) {
            System.out.println(name + " sending message: " + message);
            mediator.sendMessage(message, this);
        }

        @Override
        public void receive(String message) {
            System.out.println(name + " received message: " + message);
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            ChatMediator mediator = new ChatRoom();
            User user1 = new ChatUser(mediator, "使用者A");
            User user2 = new ChatUser(mediator, "使用者B");

            user1.send("哈囉！"); // 使用者A sending message: 哈囉！
            // 使用者A sends: 哈囉！
            user2.send("嗨！"); // 使用者B sending message: 嗨！
            // 使用者B sends: 嗨！
        }
    }
    ```

    特點：使用者僅與中介者互動，無需直接引用其他使用者。

- JavaScript 實現 Mediator

    用於協調前端 UI 元件間的互動，例如：表單欄位。

    ```javascript
    class FormMediator {
      constructor() {
        this.colleagues = [];
      }

      register(colleague) {
        this.colleagues.push(colleague);
        colleague.setMediator(this);
      }

      notify(sender, event) {
        this.colleagues.forEach(colleague => {
          if (colleague !== sender) {
            colleague.receive(event);
          }
        });
      }
    }

    class FormField {
      constructor(name) {
        this.name = name;
        this.mediator = null;
      }

      setMediator(mediator) {
        this.mediator = mediator;
      }

      send(event) {
        console.log(`${this.name} sends: ${event}`);
        this.mediator.notify(this, event);
      }

      receive(event) {
        console.log(`${this.name} receives: ${event}`);
      }
    }



    /** 使用範例 */
    const mediator = new FormMediator();
    const field1 = new FormField('輸入欄位');
    const field2 = new FormField('下拉選單');

    mediator.register(field1);
    mediator.register(field2);

    field1.send('值已更新'); // 輸入欄位 sends: 值已更新
    // 下拉選單 receives: 值已更新
    ```

    特點：適合前端動態 UI 元件間的協調，減少直接依賴。

- TypeScript 實現 Mediator

    用於管理事件驅動系統中的模組通訊。

    ```javascript
    interface Mediator {
      notify(sender: Colleague, event: string): void;
    }

    class EventMediator implements Mediator {
      private colleagues: Colleague[] = [];

      register(colleague: Colleague) {
        this.colleagues.push(colleague);
        colleague.setMediator(this);
      }

      notify(sender: Colleague, event: string) {
        this.colleagues.forEach(colleague => {
          if (colleague !== sender) {
            colleague.receive(event);
          }
        });
      }
    }

    interface Colleague {
      setMediator(mediator: Mediator): void;
      send(event: string): void;
      receive(event: string): void;
    }

    class EventModule implements Colleague {
      private name: string;
      private mediator: Mediator | null = null;

      constructor(name: string) {
        this.name = name;
      }

      setMediator(mediator: Mediator) {
        this.mediator = mediator;
      }

      send(event: string) {
        console.log(`${this.name} sends: ${event}`);
        this.mediator?.notify(this, event);
      }

      receive(event: string) {
        console.log(`${this.name} receives: ${event}`);
      }
    }



    /** 使用範例 */
    const mediator = new EventMediator();
    const module1 = new EventModule('模組 A');
    const module2 = new EventModule('模組 B');

    mediator.register(module1);
    mediator.register(module2);

    module1.send('事件觸發'); // 模組 A sends: 事件觸發
    // 模組 B receives: 事件觸發
    ```

    特點：TypeScript 的型別檢查確保通訊介面的正確性，適合複雜前端應用。

- Angular 實現 Mediator

    使用 Angular 服務作為中介者，協調元件間的互動。

    ```javascript
    /** mediator.service.ts */
    import { Injectable } from '@angular/core';

    export interface Colleague {
      receive(event: string): void;
    }

    @Injectable({
      providedIn: 'root'
    })
    export class MediatorService {
      private colleagues: { [key: string]: Colleague } = {};

      register(id: string, colleague: Colleague) {
        this.colleagues[id] = colleague;
      }

      notify(senderId: string, event: string) {
        Object.keys(this.colleagues).forEach(id => {
          if (id !== senderId) {
            this.colleagues[id].receive(event);
          }
        });
      }
    }



    /** component-a.component.ts */
    import { Component, OnInit } from '@angular/core';
    import { MediatorService } from './mediator.service';

    @Component({
      selector: 'app-component-a',
      template: `<button (click)="sendEvent()">發送事件</button>`
    })
    export class ComponentA implements OnInit, Colleague {
      constructor(private mediator: MediatorService) {}

      ngOnInit() {
        this.mediator.register('ComponentA', this);
      }

      sendEvent() {
        this.mediator.notify('ComponentA', '來自元件A的事件');
      }

      receive(event: string) {
        console.log('元件A receives: ' + event);
      }
    }



    /** component-b.component.ts */
    import { Component, OnInit } from '@angular/core';
    import { MediatorService } from './mediator.service';

    @Component({
      selector: 'app-component-b',
      template: `<div>元件B</div>`
    })
    export class ComponentB implements OnInit, Colleague {
      constructor(private mediator: MediatorService) {}

      ngOnInit() {
        this.mediator.register('ComponentB', this);
      }

      receive(event: string) {
        console.log('元件B receives: ' + event);
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';

    @Component({
      selector: 'app-root',
      template: `
        <app-component-a></app-component-a>
        <app-component-b></app-component-b>
      `
    })
    export class AppComponent {}
    ```

    特點：利用 Angular 的依賴注入，簡化中介者管理，適合複雜 UI 互動。

- React 實現 Mediator

    使用 React Context 實現中介者，協調多個元件間的事件。

    ```javascript
    /** Mediator.js */
    class EventMediator {
      #colleagues = {};

      register(id, colleague) {
        this.#colleagues[id] = colleague;
      }

      notify(senderId, event) {
        Object.keys(this.#colleagues).forEach(id => {
          if (id !== senderId) {
            this.#colleagues[id].receive(event);
          }
        });
      }
    }



    /** MediatorContext.js */
    import { createContext, useContext } from 'react';

    const MediatorContext = createContext(null);
    export const useMediator = () => useContext(MediatorContext);



    /** ComponentA.jsx */
    import React, { useEffect } from 'react';
    import { useMediator } from './MediatorContext';

    const ComponentA = () => {
      const mediator = useMediator();

      useEffect(() => {
        mediator.register('ComponentA', {
          receive: (event) => console.log('ComponentA receives: ' + event)
        });
      }, [mediator]);

      const sendEvent = () => {
        mediator.notify('ComponentA', '來自元件A的事件');
      };

      return <button onClick={sendEvent}>發送事件</button>;
    };

    export default ComponentA;



    /** ComponentB.jsx */
    import React, { useEffect } from 'react';
    import { useMediator } from './MediatorContext';

    const ComponentB = () => {
      const mediator = useMediator();

      useEffect(() => {
        mediator.register('ComponentB', {
          receive: (event) => console.log('ComponentB receives: ' + event)
        });
      }, [mediator]);

      return <div>元件B</div>;
    };

    export default ComponentB;

    /** App.jsx */
    import React from 'react';
    import ComponentA from './ComponentA';
    import ComponentB from './ComponentB';
    import { MediatorContext } from './MediatorContext';

    const App = () => {
      const mediator = new EventMediator();

      return (
        <MediatorContext.Provider value={mediator}>
          <ComponentA />
          <ComponentB />
        </MediatorContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Context，簡化元件間通訊，適合動態 UI 互動。

<br />

## 應用場景

Mediator 模式適用於以下場景

- 多物件互動

    例如：線上聊天室，使用者間訊息透過中介者傳遞。

- UI 元件協調

    例如：表單中輸入欄位與按鈕的動態互動。

- 事件驅動系統

    例如：模組間的事件觸發與監聽。

- 鬆耦合設計

    例如：需要降低物件間依賴的複雜系統。

例如

- 在前端，Mediator 用於管理表單元件間的互動或事件總線。

- Java 的 `java.util.Timer` 可視為簡單中介者，協調任務執行。

<br />

## 優缺點

### 優點

- 降低耦合：物件僅與中介者通訊，減少直接依賴。

- 集中管理：互動行為集中於中介者，便於維護和修改。

- 靈活性：新增同事物件無需修改現有程式碼。

- 符合開閉原則：易於擴展新行為或新同事。

### 缺點

- 中介者複雜度：隨著互動增加，中介者可能變得過於複雜。

- 效能開銷：集中通訊可能導致中介者成為瓶頸。

- 單點故障：中介者失效可能影響整個系統。

<br />

## 注意事項

- 中介者範圍：避免中介者承擔過多責任，保持單一職責。

- 狀態管理：在無狀態環境中，確保中介者正確處理同事狀態。

- 測試性：中介者需設計為易於單元測試，避免過多依賴。

- 異常處理：確保中介者在異常情況下能正確響應。

<br />

## 與其他模式的關係

- 與觀察者模式 (Observer)：觀察者模式注重一對多通知，Mediator 聚焦多對多協調。

- 與外觀模式 (Facade)：Facade 簡化子系統介面，Mediator 協調物件互動。

- 與命令模式 (Command)：Mediator 可與命令結合，封裝互動行為。

<br />

## 總結

Mediator 模式是一種高效的行為型設計模式，透過將物件間的互動集中於中介者，大幅降低系統耦合度，提升程式碼的可維護性與擴展性。

在前端開發中，管理複雜的 UI 元件互動或事件驅動系統，例如：表單欄位的動態同步或線上聊天室的訊息管理。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據專案需求選擇合適的工具與方法。需特別關注中介者的複雜度和效能，確保設計簡潔且高效。對於追求高品質軟體架構的開發人員而言，Mediator 模式是一個核心工具，能顯著提升系統的靈活性與可維護性。
