# Decorator (裝飾者模式)

Decorator (裝飾者模式) 是一種結構型設計模式，動態為物件附加功能，無需修改原始類別。

這種模式提供繼承的靈活替代方案，適合需要擴展功能的場景。

<br />

## 動機

軟體開發中，常需為物件增加新功能，例如

- UI 元件需動態添加樣式或行為，例如：邊框、陰影。

- 日誌系統需附加時間戳記或格式化功能。

- 前端表單元件需動態增加驗證或提示功能。

直接修改類別可能違反開閉原則，或導致子類別數量爆炸。

Decorator 模式透過組合方式動態擴展功能，解決此問題。

<br />

## 結構

Decorator 模式的結構包含以下元素

- 元件介面 (Component Interface)：定義基礎操作。

- 具體元件 (Concrete Component)：實作元件介面的核心類別。

- 裝飾者 (Decorator)：實作元件介面，包含對具體元件的引用，並提供擴展功能。

- 具體裝飾者 (Concrete Decorator)：實現具體的附加功能。

以下是 Decorator 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/ZT5F3W4n50RmVPFUuUqGgGE84S55glF49BJIAHia8gni9JPiM5fZ8U4o8ymjpAHXcDdOzi_l-rvRymtNPj3hKf83nt7WSPm7brDmMORRNRn0YISDwZON20tLwok9qi284e0Yg3vgRZmbymLA9fIyaVlY71vMbhA8w7BVZm0fD1hy6thkj-7--fmkhC9Rlj5S6B1S4uMAhYbj6GRYuvQJilzKJUNyjat5fAnuWRikkdNiyA6dT2eWN6-2syowoToLSQcKVOxCYKyq9KaBnLZrUxnafp9cB5kRaXfAD_hZ5m00" width="100%" />

<br />

## 實現方式

- 基本實現

    假設為咖啡訂單添加額外配料。

    ```java
    /** 元件介面 */
    public interface Coffee {
        String getDescription();
        double getCost();
    }

    /** 具體元件 */
    public class SimpleCoffee implements Coffee {
        @Override
        public String getDescription() {
            return "Simple Coffee";
        }

        @Override
        public double getCost() {
            return 5.0;
        }
    }

    /** 裝飾者 */
    public abstract class CoffeeDecorator implements Coffee {
        protected Coffee coffee;

        public CoffeeDecorator(Coffee coffee) {
            this.coffee = coffee;
        }

        @Override
        public String getDescription() {
            return coffee.getDescription();
        }

        @Override
        public double getCost() {
            return coffee.getCost();
        }
    }

    /** 具體裝飾者：牛奶 */
    public class MilkDecorator extends CoffeeDecorator {
        public MilkDecorator(Coffee coffee) {
            super(coffee);
        }

        @Override
        public String getDescription() {
            return coffee.getDescription() + ", Milk";
        }

        @Override
        public double getCost() {
            return coffee.getCost() + 1.5;
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Coffee coffee = new SimpleCoffee();
            coffee = new MilkDecorator(coffee);
            System.out.println(coffee.getDescription() + " $" + coffee.getCost());
            // Simple Coffee, Milk $6.5
        }
    }
    ```

    特點：動態為咖啡添加配料，無需修改原始類別。

- JavaScript 實現 Decorator

    為 UI 元件添加樣式。

    ```javascript
    /** 元件介面 */
    class UIComponent {
      render() {
        throw new Error("Method 'render()' must be implemented.");
      }
    }

    /** 具體元件 */
    class Button extends UIComponent {
      render() {
        return `<button>Click me</button>`;
      }
    }

    /** 裝飾者 */
    class UIDecorator extends UIComponent {
      constructor(component) {
        super();
        this.component = component;
      }

      render() {
        return this.component.render();
      }
    }

    /** 具體裝飾者：邊框 */
    class BorderDecorator extends UIDecorator {
      render() {
        return `<div style="border: 1px solid black;">${this.component.render()}</div>`;
      }
    }

    /** 使用範例 */
    const button = new Button();
    const decoratedButton = new BorderDecorator(button);
    console.log(decoratedButton.render()); // <div style="border: 1px solid black;"><button>Click me</button></div>
    ```

    特點：動態為按鈕添加邊框樣式，保持原始元件不變。

- TypeScript 實現 Decorator

    為表單輸入框添加驗證功能。

    ```typescript
    /** 元件介面 */
    interface FormField {
      render(): string;
      validate(): boolean;
    }

    /** 具體元件 */
    class TextInput implements FormField {
      render(): string {
        return `<input type="text" />`;
      }

      validate(): boolean {
        return true;
      }
    }

    /** 裝飾者 */
    abstract class FormFieldDecorator implements FormField {
      protected field: FormField;

      constructor(field: FormField) {
        this.field = field;
      }

      render(): string {
        return this.field.render();
      }

      validate(): boolean {
        return this.field.validate();
      }
    }

    /** 具體裝飾者：必填驗證 */
    class RequiredValidator extends FormFieldDecorator {
      render(): string {
        return `${this.field.render()} <span>*必填</span>`;
      }

      validate(): boolean {
        return false; // 模擬驗證失敗
      }
    }



    /** 使用範例 */
    const input = new TextInput();
    const decoratedInput = new RequiredValidator(input);
    console.log(decoratedInput.render());   // <input type="text" /> <span>*必填</span>
    console.log(decoratedInput.validate()); // false
    ```

    特點：TypeScript 確保型別安全，動態添加驗證功能。

- Angular 實現 Decorator

    為元件添加動態樣式。

    ```typescript
    /** style.service.ts */
    import { Injectable } from '@angular/core';

    export interface Component {
      render(): string;
    }

    @Injectable()
    export class BaseComponent implements Component {
      render(): string {
        return `<div>Base Component</div>`;
      }
    }

    @Injectable()
    export abstract class ComponentDecorator implements Component {
      protected component: Component;

	  constructor(component: Component) {
	    this.component = component;
	  }

      render(): string {
        return this.component.render();
      }
    }

    @Injectable()
    export class ShadowDecorator extends ComponentDecorator {
      render(): string {
        return `<div style="box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">${this.component.render()}</div>`;
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { BaseComponent, ShadowDecorator } from './style.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [BaseComponent, ShadowDecorator],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { BaseComponent, ShadowDecorator } from './style.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="renderComponent()">渲染元件</button>`
    })
    export class AppComponent {
      constructor(private baseComponent: BaseComponent, private shadowDecorator: ShadowDecorator) {
        this.shadowDecorator = new ShadowDecorator(baseComponent);
      }

      renderComponent() {
        console.log(this.shadowDecorator.render());
        /** <div style="box-shadow: 2px 2px 5px rgba(0,0,0,0.3);"><div>Base Component</div></div> */
      }
    }
    ```

    特點：Angular 服務支援動態樣式擴展。

- React 實現 Decorator

    為按鈕添加點擊追蹤功能。

    ```javascript
    /** ButtonDecorator.js */
    class ButtonComponent {
      render() {
        return <button>Click me</button>;
      }
    }

    class ButtonDecorator {
      constructor(component) {
        this.component = component;
      }

      render() {
        return this.component.render();
      }
    }

    class TrackClickDecorator extends ButtonDecorator {
      render() {
        return (
          <div onClick={() => console.log('Button clicked')}>
            {this.component.render()}
          </div>
        );
      }
    }



    /** App.jsx */
    import React from 'react';

    const App = () => {
      const button = new ButtonComponent();
      const decoratedButton = new TrackClickDecorator(button);

      return decoratedButton.render();
    };

    export default App;
    ```

    特點：動態為 React 元件添加行為，保持原始結構。

<br />

## 應用場景

Decorator 模式適用於以下場景

- 動態為物件添加功能，例如：UI 樣式或行為。

- 需要擴展功能但不想修改原始類別。

- 前端中為元件添加樣式、驗證或事件處理。

例如：Java 的 `java.io` 包使用 Decorator，像是 `BufferedInputStream` 裝飾 `InputStream`。

<br />

## 優缺點

### 優點

- 靈活性：動態添加或移除功能。

- 符合開閉原則：無需修改原始類別。

- 可組合性：多個裝飾者可層層疊加。

- 重用性：功能模組化，易於重用。

### 缺點

- 程式碼複雜度：多個裝飾者增加管理成本。

- 調試難度：層層裝飾可能難以追蹤。

- 效能開銷：多層包裝可能略增開銷。

<br />

## 注意事項

- 介面一致性：確保裝飾者與元件相容。

- 裝飾順序：不同裝飾者順序可能影響結果。

- 深拷貝 vs 淺拷貝：Clone 裝飾者時選擇合適拷貝方式。

- 避免濫用：簡單功能可直接實現。

<br />

## 與其他模式的關係

- 與 Adapter：Decorator 增強功能，Adapter 轉換介面。

- 與 Composite：Decorator 可用於 Composite 的葉子或容器。

- 與 Strategy：Decorator 改變行為結構，Strategy 改變演算法。

- 與 Proxy：Decorator 聚焦功能擴展，Proxy 聚焦控制訪問。

<br />

## 總結

Decorator 模式透過動態組合提供靈活方式擴展物件功能，適合需要增強行為的場景。

在前端中，此模式適用於 UI 元件樣式或行為擴展。

理解 Decorator 有助於設計模組化架構，提升程式碼可維護性。
