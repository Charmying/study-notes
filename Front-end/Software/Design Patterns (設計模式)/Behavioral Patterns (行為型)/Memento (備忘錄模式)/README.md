# Memento (備忘錄模式)

Memento (備忘錄模式) 是一種行為型設計模式，允許在不破壞物件封裝的情況下，儲存並恢復物件的內部狀態。此模式用於捕捉物件的某個狀態快照，以便在需要時還原，同時確保物件的內部結構不被外部直接存取。

這種模式特別適合用於需要支援「復原」(Undo) 功能或狀態儲存的場景，例如：文字編輯器的復原操作、遊戲的存檔功能或資料庫事務的回滾。

<br />

## 動機

在軟體系統中，物件狀態的儲存與還原常見於以下場景，例如

- 文字編輯器：使用者需要復原之前的編輯操作。

- 遊戲存檔：玩家希望儲存遊戲進度並在之後恢復。

- 表單操作：使用者在表單中修改資料後，可能需要恢復到初始狀態。

若直接暴露物件內部狀態，可能違反封裝原則，導致外部程式碼過度依賴物件實現細節。

Memento 模式透過將狀態儲存於獨立的備忘錄物件，解決這些問題，確保物件狀態的安全存取與還原。

<br />

## 結構

Memento 模式的結構包含以下元素

- 備忘錄 (Memento)：儲存物件狀態的類別，包含狀態資料。

- 發起者 (Originator)：負責創建備忘錄以儲存當前狀態，並能使用備忘錄還原狀態。

- 管理者 (Caretaker)：負責儲存和管理備忘錄，但不操作或檢查備忘錄內容。

以下是 Memento 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/VP0n2iCm34LtW--WCQ7a0XbAe7Ffa1EOHBYcYGsoEfNSlKvZEtK9tSJ_ukjzTPuLyNEUf1WcvJrSSKRB3bvI03GGRCOMUYPZzIgTG2FtgrhLkxv8aG9kPBInYXtzoV0fe_3gpHm8WnX1rYjnt5n27xAncZSnktL1SL64h1wO8NxNCqUwSv0NsnwHV4vzLMsQStvT6njuANQCSk7kfZ7O7Ten_FuD" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現文字編輯器的復原功能。

    ```java
    public class Memento {
        private String state;

        public Memento(String state) {
            this.state = state;
        }

        public String getState() {
            return state;
        }
    }

    public class TextEditor {
        private String content;

        public void setContent(String content) {
            this.content = content;
        }

        public String getContent() {
            return content;
        }

        public Memento save() {
            return new Memento(content);
        }

        public void restore(Memento memento) {
            content = memento.getState();
        }
    }

    public class History {
        private List<Memento> mementos = new ArrayList<>();

        public void addMemento(Memento memento) {
            mementos.add(memento);
        }

        public Memento getMemento(int index) {
            return mementos.get(index);
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            TextEditor editor = new TextEditor();
            History history = new History();

            editor.setContent("第一版內容");
            history.addMemento(editor.save());

            editor.setContent("第二版內容");
            history.addMemento(editor.save());

            editor.setContent("第三版內容");
            System.out.println("當前內容: " + editor.getContent()); // 當前內容: 第三版內容

            editor.restore(history.getMemento(1));
            System.out.println("還原至第二版: " + editor.getContent()); // 還原至第二版: 第二版內容

            editor.restore(history.getMemento(0));
            System.out.println("還原至第一版: " + editor.getContent()); // 還原至第一版: 第一版內容
        }
    }
    ```

    特點：管理者僅儲存備忘錄，不直接操作其內容，確保封裝性。

- JavaScript 實現 Memento

    用於儲存表單輸入狀態。

    ```javascript
    class Memento {
      constructor(state) {
        this.state = state;
      }

      getState() {
        return this.state;
      }
    }

    class Form {
      constructor() {
        this.data = {};
      }

      setData(data) {
        this.data = { ...data };
      }

      getData() {
        return this.data;
      }

      save() {
        return new Memento({ ...this.data });
      }

      restore(memento) {
        this.data = { ...memento.getState() };
      }
    }

    class FormHistory {
      constructor() {
        this.mementos = [];
      }

      addMemento(memento) {
        this.mementos.push(memento);
      }

      getMemento(index) {
        return this.mementos[index];
      }
    }



    /** 使用範例 */
    const form = new Form();
    const history = new FormHistory();

    form.setData({ name: '使用者A', email: 'a@example.com' });
    history.addMemento(form.save());

    form.setData({ name: '使用者B', email: 'b@example.com' });
    history.addMemento(form.save());

    console.log(form.getData()); // { name: '使用者B', email: 'b@example.com' }

    form.restore(history.getMemento(0));
    console.log(form.getData()); // { name: '使用者A', email: 'a@example.com' }
    ```

    特點：使用物件深拷貝，確保狀態獨立，適合前端表單狀態管理。

- TypeScript 實現 Memento

    用於遊戲存檔系統，管理玩家狀態。

    ```javascript
    interface Memento {
      getState(): { level: number; score: number };
    }

    class GameMemento implements Memento {
      private state: { level: number; score: number };

      constructor(state: { level: number; score: number }) {
        this.state = { ...state };
      }

      getState(): { level: number; score: number } {
        return { ...this.state };
      }
    }

    class Game {
      private state: { level: number; score: number } = { level: 1, score: 0 };

      setState(state: { level: number; score: number }) {
        this.state = { ...state };
      }

      getState(): { level: number; score: number } {
        return { ...this.state };
      }

      save(): Memento {
        return new GameMemento(this.state);
      }

      restore(memento: Memento) {
        this.state = { ...memento.getState() };
      }
    }

    class GameHistory {
      private mementos: Memento[] = [];

      addMemento(memento: Memento) {
        this.mementos.push(memento);
      }

      getMemento(index: number): Memento {
        return this.mementos[index];
      }
    }



    /** 使用範例 */
    const game = new Game();
    const history = new GameHistory();

    game.setState({ level: 1, score: 100 });
    history.addMemento(game.save());

    game.setState({ level: 2, score: 200 });
    history.addMemento(game.save());

    console.log(game.getState()); // { level: 2, score: 200 }

    game.restore(history.getMemento(0));
    console.log(game.getState()); // { level: 1, score: 100 }
    ```

    特點：TypeScript 的型別檢查確保狀態結構一致，適合複雜狀態管理。

- Angular 實現 Memento

    使用 Angular 服務管理表單狀態的復原功能。

    ```javascript
    /** memento.service.ts */
    import { Injectable } from '@angular/core';

    export interface Memento {
      getState(): any;
    }

    class FormMemento implements Memento {
      private state: any;

      constructor(state: any) {
        this.state = { ...state };
      }

      getState() {
        return { ...this.state };
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class FormService {
      private data: any = {};

      setData(data: any) {
        this.data = { ...data };
      }

      getData() {
        return { ...this.data };
      }

      save(): Memento {
        return new FormMemento(this.data);
      }

      restore(memento: Memento) {
        this.data = { ...memento.getState() };
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class FormHistoryService {
      private mementos: Memento[] = [];

      addMemento(memento: Memento) {
        this.mementos.push(memento);
      }

      getMemento(index: number): Memento {
        return this.mementos[index];
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { FormService, FormHistoryService } from './memento.service';

    @Component({
      selector: 'app-root',
      template: `
        <input [(ngModel)]="formData.name" placeholder="姓名" />
        <input [(ngModel)]="formData.email" placeholder="電子郵件" />
        <button (click)="save()">儲存</button>
        <button (click)="restore()">復原</button>
      `
    })
    export class AppComponent {
      formData = { name: '', email: '' };

      constructor(
        private formService: FormService,
        private historyService: FormHistoryService
      ) {}

      save() {
        this.formService.setData(this.formData);
        this.historyService.addMemento(this.formService.save());
      }

      restore() {
        const memento = this.historyService.getMemento(0);
        if (memento) {
          this.formService.restore(memento);
          this.formData = this.formService.getData();
        }
      }
    }
    ```

    特點：整合 Angular 的雙向綁定，適合表單狀態的動態管理。

- React 實現 Memento

    使用 React Hook 和 Context 實現表單狀態復原。

    ```javascript
    /** Memento.js */
    class FormMemento {
      #state;

      constructor(state) {
        this.#state = { ...state };
      }

      getState() {
        return { ...this.#state };
      }
    }

    class FormState {
      #data = {};

      setData(data) {
        this.#data = { ...data };
      }

      getData() {
        return { ...this.#data };
      }

      save() {
        return new FormMemento(this.#data);
      }

      restore(memento) {
        this.#data = { ...memento.getState() };
      }
    }



    /** FormContext.js */
    import { createContext, useContext } from 'react';

    const FormContext = createContext(null);
    export const useFormState = () => useContext(FormContext);



    /** App.jsx */
    import React, { useState } from 'react';
    import { FormContext } from './FormContext';

    const App = () => {
      const formState = new FormState();
      const [formData, setFormData] = useState({ name: '', email: '' });
      const [history, setHistory] = useState([]);

      const save = () => {
        formState.setData(formData);
        setHistory([...history, formState.save()]);
      };

      const restore = () => {
        if (history.length > 0) {
          formState.restore(history[0]);
          setFormData(formState.getData());
        }
      };

      return (
        <FormContext.Provider value={formState}>
          <input
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="姓名"
          />
          <input
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            placeholder="電子郵件"
          />
          <button onClick={save}>儲存</button>
          <button onClick={restore}>復原</button>
        </FormContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Hook，實現簡單的狀態復原功能。

<br />

## 應用場景

Memento 模式適用於以下場景

- 復原功能

    例如：文字編輯器的「復原」按鈕。

- 遊戲存檔

    例如：儲存玩家進度並在需要時還原。

- 表單狀態管理

    例如：允許使用者還原表單資料到先前狀態。

- 事務處理

    例如：資料庫操作中的回滾功能。

例如

- 在前端，Memento 用於表單或 UI 狀態的復原。

- Java 的序列化機制可視為 Memento 的簡化應用，儲存物件狀態。

<br />

## 優缺點

### 優點

- 保護封裝：備忘錄僅由發起者存取，外部無法直接修改狀態。

- 簡化復原：提供乾淨的方式實現狀態還原。

- 靈活性：支援多個備忘錄，允許儲存多個狀態快照。

- 易於擴展：可結合其他模式，例如：命令模式，實現複雜操作。

### 缺點

- 記憶體開銷：儲存多個備忘錄可能佔用大量記憶體。

- 狀態管理複雜度：若物件狀態複雜，備忘錄實現可能增加程式碼量。

- 效能問題：頻繁儲存或還原可能影響效能。

<br />

## 注意事項

- 狀態範圍：僅儲存必要的狀態資料，避免記憶體浪費。

- 深拷貝與淺拷貝：在儲存狀態時，確保使用深拷貝以避免意外修改。

- 安全性：限制備忘錄的存取權，防止外部直接修改。

- 歷史管理：管理者需妥善處理備忘錄清單，避免無限增長。

<br />

## 與其他模式的關係

- 與命令模式 (Command)：Memento 常與命令模式結合，實現復原功能。

- 與狀態模式 (State)：Memento 儲存狀態快照，狀態模式管理狀態切換。

- 與觀察者模式 (Observer)：可結合使用，通知狀態變化並儲存備忘錄。

<br />

## 總結

Memento 模式是一種實用的行為型設計模式，透過儲存物件狀態快照，實現復原功能，同時保護物件的封裝性。特別適合用於需要復原操作或狀態管理的場景，例如：文字編輯器、遊戲存檔或表單狀態管理。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據應用需求選擇最適合的工具。需注意記憶體使用與狀態管理的複雜度，確保高效且穩定的實現。對於追求可靠狀態管理的開發人員而言，Memento 模式是一個核心工具，能顯著提升系統的功能性與使用者體驗。
