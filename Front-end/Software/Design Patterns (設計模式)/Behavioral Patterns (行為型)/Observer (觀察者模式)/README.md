# Observer (觀察者模式)

Observer (觀察者模式) 是一種行為型設計模式，定義物件間的一對多依賴關係，當主體物件狀態改變時，所有依賴的觀察者物件會自動收到通知並更新。此模式實現鬆耦合的通訊機制，讓主體與觀察者可獨立變化。

這種模式特別適合用於事件驅動系統，例如：UI 事件處理、資料同步或即時通知系統。

<br />

## 動機

在軟體系統中，物件間常需要根據狀態變化進行同步，例如

- UI 更新：當資料模型改變時，視圖元件需自動更新。

- 即時通知：新聞訂閱系統中，使用者需在新聞發布時收到通知。

- 資料監聽：多個模組需監聽同一資料來源的變化。

若主體直接與觀察者耦合，會導致程式碼難以維護與擴展。

Observer 模式透過將通知機制集中於主體，並讓觀察者訂閱變化，解決這些問題，實現鬆耦合設計。

<br />

## 結構

Observer 模式的結構包含以下元素

- 主體介面 (Subject Interface)：定義註冊、移除和通知觀察者的方法。

- 具體主體 (Concrete Subject)：儲存狀態並在變化時通知觀察者。

- 觀察者介面 (Observer Interface)：定義更新方法，供主體通知時呼叫。

- 具體觀察者 (Concrete Observer)：實現更新方法，響應主體變化。

以下是 Observer 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/hP512i8m44NtWTnXbXLf3r1AARWLNEG4QJhLI4qacGgYtjsM6aiA2eAxcVdCdv-NofDqr9ywphGXTArK2AAlZwW8Rfm1h44IINL8REtHNT3bi7jLgqblyBjkBEdscWpTWpFEL2UzXuqroY5XT2k58GvX3eASDljf57nz3bljgGZkvR_JZPr74cE490eIei-8WabWr9-RZrlnWt_P372AUvOjYN7sTehaCELiYTYcQGcpNA5fXez_0W00" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現一個新聞訂閱系統，主體為新聞來源，觀察者為訂閱者。

    ```java
    public interface Subject {
        void attach(Observer observer);
        void detach(Observer observer);
        void notifyObservers();
    }

    public class NewsAgency implements Subject {
        private List<Observer> observers = new ArrayList<>();
        private String news;

        @Override
        public void attach(Observer observer) {
            observers.add(observer);
        }

        @Override
        public void detach(Observer observer) {
            observers.remove(observer);
        }

        @Override
        public void notifyObservers() {
            for (Observer observer : observers) {
                observer.update(news);
            }
        }

        public void setNews(String news) {
            this.news = news;
            notifyObservers();
        }
    }

    public interface Observer {
        void update(String news);
    }

    public class Subscriber implements Observer {
        private String name;

        public Subscriber(String name) {
            this.name = name;
        }

        @Override
        public void update(String news) {
            System.out.println(name + " 收到新聞: " + news);
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            NewsAgency agency = new NewsAgency();
            Subscriber subscriber1 = new Subscriber("訂閱者 A");
            Subscriber subscriber2 = new Subscriber("訂閱者 B");

            agency.attach(subscriber1);
            agency.attach(subscriber2);

            agency.setNews("重大新聞發布！"); // 訂閱者 A 收到新聞: 重大新聞發布！
            // 訂閱者 B 收到新聞: 重大新聞發布！
        }
    }
    ```

    特點：主體管理觀察者清單，狀態變化時自動通知。

- JavaScript 實現 Observer

    用於前端資料模型與 UI 元件的同步。

    ```javascript
    class Subject {
      constructor() {
        this.observers = [];
      }

      attach(observer) {
        this.observers.push(observer);
      }

      detach(observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
      }

      notify(data) {
        this.observers.forEach(observer => observer.update(data));
      }

      setData(data) {
        this.data = data;
        this.notify(data);
      }
    }

    class View {
      constructor(name) {
        this.name = name;
      }

      update(data) {
        console.log(`${this.name} 更新資料: ${data}`);
      }
    }



    /** 使用範例 */
    const subject = new Subject();
    const view1 = new View('視圖 A');
    const view2 = new View('視圖 B');

    subject.attach(view1);
    subject.attach(view2);

    subject.setData('新資料'); // 視圖 A 更新資料: 新資料
    // 視圖 B 更新資料: 新資料
    ```

    特點：適合前端動態 UI 更新，簡單實現觀察者清單管理。

- TypeScript 實現 Observer

    用於事件監聽系統，確保型別安全。

    ```javascript
    interface Subject {
      attach(observer: Observer): void;
      detach(observer: Observer): void;
      notify(data: string): void;
    }

    interface Observer {
      update(data: string): void;
    }

    class EventSubject implements Subject {
      private observers: Observer[] = [];
      private data: string;

      attach(observer: Observer) {
        this.observers.push(observer);
      }

      detach(observer: Observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
      }

      notify(data: string) {
        this.observers.forEach(observer => observer.update(data));
      }

      setData(data: string) {
        this.data = data;
        this.notify(data);
      }
    }

    class EventListener implements Observer {
      private name: string;

      constructor(name: string) {
        this.name = name;
      }

      update(data: string) {
        console.log(`${this.name} 收到事件: ${data}`);
      }
    }



    /** 使用範例 */
    const subject = new EventSubject();
    const listener1 = new EventListener('監聽者 A');
    const listener2 = new EventListener('監聽者 B');

    subject.attach(listener1);
    subject.attach(listener2);

    subject.setData('新事件觸發'); // 監聽者 A 收到事件: 新事件觸發
    // 監聽者 B 收到事件: 新事件觸發
    ```

    特點：TypeScript 的型別系統確保資料與方法的正確性，適合複雜應用。

- Angular 實現 Observer

    使用 Angular 服務和 RxJS 實現觀察者模式。

    ```javascript
    /** data.service.ts */
    import { Injectable } from '@angular/core';
    import { Subject } from 'rxjs';

    @Injectable({
      providedIn: 'root'
    })
    export class DataService {
      private dataSubject = new Subject<string>();

      data$ = this.dataSubject.asObservable();

      setData(data: string) {
        this.dataSubject.next(data);
      }
    }



    /** component-a.component.ts */
    import { Component, OnInit, OnDestroy } from '@angular/core';
    import { DataService } from './data.service';
    import { Subscription } from 'rxjs';

    @Component({
      selector: 'app-component-a',
      template: `<div>元件A: {{ data }}</div>`
    })
    export class ComponentA implements OnInit, OnDestroy {
      data: string = '';
      private subscription: Subscription;

      constructor(private dataService: DataService) {}

      ngOnInit() {
        this.subscription = this.dataService.data$.subscribe(data => {
          this.data = data;
        });
      }

      ngOnDestroy() {
        this.subscription.unsubscribe();
      }
    }



    /** component-b.component.ts */
    import { Component, OnInit, OnDestroy } from '@angular/core';
    import { DataService } from './data.service';
    import { Subscription } from 'rxjs';

    @Component({
      selector: 'app-component-b',
      template: `
        <div>元件B: {{ data }}</div>
        <button (click)="updateData()">更新資料</button>
      `
    })
    export class ComponentB implements OnInit, OnDestroy {
      data: string = '';
      private subscription: Subscription;

      constructor(private dataService: DataService) {}

      ngOnInit() {
        this.subscription = this.dataService.data$.subscribe(data => {
          this.data = data;
        });
      }

      updateData() {
        this.dataService.setData('來自元件B的新資料');
      }

      ngOnDestroy() {
        this.subscription.unsubscribe();
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

    特點：利用 RxJS 的 Subject，實現高效的事件通知，適合 Angular 應用。

- React 實現 Observer

    使用 React Context 和 Hook 實現觀察者模式。

    ```javascript
    /** DataContext.js */
    import { createContext, useContext, useState } from 'react';

    const DataContext = createContext(null);

    export const useData = () => useContext(DataContext);



    /** DataProvider.js */
    const DataProvider = ({ children }) => {
      const [data, setData] = useState('');

      const updateData = (newData) => {
        setData(newData);
      };

      return (
        <DataContext.Provider value={{ data, updateData }}>
          {children}
        </DataContext.Provider>
      );
    };



    /** ComponentA.jsx */
    import React from 'react';
    import { useData } from './DataContext';

    const ComponentA = () => {
      const { data } = useData();
      return <div>元件A: {data}</div>;
    };

    export default ComponentA;



    /** ComponentB.jsx */
    import React from 'react';
    import { useData } from './DataContext';

    const ComponentB = () => {
      const { data, updateData } = useData();

      return (
        <div>
          <div>元件B: {data}</div>
          <button onClick={() => updateData('來自元件B的新資料')}>
            更新資料
          </button>
        </div>
      );
    };

    export default ComponentB;



    /** App.jsx */
    import React from 'react';
    import ComponentA from './ComponentA';
    import ComponentB from './ComponentB';
    import { DataProvider } from './DataProvider';

    const App = () => {
      return (
        <DataProvider>
          <ComponentA />
          <ComponentB />
        </DataProvider>
      );
    };

    export default App;
    ```

    特點：結合 React Context 和 Hook，實現簡單的狀態同步。

<br />

## 應用場景

Observer 模式適用於以下場景

- 事件通知

    例如：即時新聞訂閱系統，通知訂閱者新內容。

- UI 同步

    例如：資料模型變化時，自動更新多個視圖。

- 資料監聽

    例如：多個模組監聽同一資料來源的變化。

- 分散式系統

    例如：分散式應用中的狀態同步。

例如

- 在前端，Observer 用於 UI 元件與資料模型的同步。

- Java 的 `java.util.Observable` 和 `Observer` 介面是經典實現。

<br />

## 優缺點

### 優點

- 鬆耦合：主體與觀察者僅透過介面互動，降低依賴。

- 動態訂閱：觀察者可隨時加入或退出。

- 廣播通知：支援一對多通訊，高效傳遞變化。

- 符合開閉原則：新增觀察者無需修改主體程式碼。

### 缺點

- 記憶體洩漏：若觀察者未正確移除，可能導致記憶體問題。

- 效能開銷：大量觀察者可能導致通知時間增加。

- 通知管理：複雜系統中，通知順序或優先級難以控制。

<br />

## 注意事項

- 記憶體管理：確保觀察者在不再需要時被移除，避免洩漏。

- 通知順序：在多觀察者場景中，確保通知順序符合需求。

- 異常處理：觀察者的更新方法需妥善處理異常，避免影響主體。

- 非同步通知：在非同步環境中，需確保通知的正確性與一致性。

<br />

## 與其他模式的關係

- 與中介者模式 (Mediator)：Mediator 聚焦多對多協調，Observer 注重一對多通知。

- 與命令模式 (Command)：可結合使用，命令觸發事件並通知觀察者。

- 與發布訂閱模式 (Publish/Subscribe)：Observer 是其簡化形式，發布訂閱通常涉及中間層。

<br />

## 總結

Observer 模式是一種高效的行為型設計模式，透過一對多的通知機制，實現主體與觀察者間的鬆耦合通訊。特別適合用於事件驅動系統與 UI 同步場景，例如：即時通知或資料模型的動態更新。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據專案需求選擇最適合的工具。需注意記憶體管理與通知效能，確保系統穩定性。對於追求高效事件處理與鬆耦合設計的開發人員而言，Observer 模式是一個核心工具，能顯著提升系統的靈活性與可維護性。
