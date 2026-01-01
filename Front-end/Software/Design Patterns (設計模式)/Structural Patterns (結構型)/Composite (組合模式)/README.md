# Composite (組合模式)

Composite (組合模式) 是一種結構型設計模式，將物件組織成樹狀結構，以統一處理單個物件與組合物件。

這種模式允許客戶端以一致方式操作單一部件與複合結構，簡化複雜層次結構的管理。

<br />

## 動機

軟體開發中，常需處理具有層次兼具容器的物件，例如

- 檔案系統中，檔案與資料夾需統一操作。

- 圖形編輯器中，單一形狀與形狀群組需一致處理。

- 前端 UI 元件樹，例如：表單包含輸入框與按鈕群組。

若分別處理單一物件與組合物件，程式碼會變得複雜且難以擴展。

Composite 模式透過統一介面，解決此問題。

<br />

## 結構

Composite 模式的結構包含以下元素

- 元件介面 (Component Interface)：定義葉子與組合物件的共同操作。

- 葉子 (Leaf)：樹狀結構中的單一物件，無子節點。

- 組合物件 (Composite)：包含子元件的容器，可遞迴包含其他組合物件或葉子。

- 客戶端 (Client)：透過元件介面操作樹狀結構。

以下是 Composite 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLulhNboUvjJtPtlvox22J0ovMPLv9Qb9QOdAhWd9zRa9-NcbUYKCtBfQ2WhP1Va5gKM9APdwUXoSjLoyi5C-J5nCwdQoT0j2Vd91ONA_Ya9gOHqWMq-kc4ZkUTAu4EGDOBjhOuioGLOe2kGd96PavAKMgUWXN2IT6n4CCJKr8qak7kH5AW2P4lIitDBql5gmIN-rvEd_DaVnF4POYWiAdHqmDx3qCGxcwe3DWB-RgwTWfAkObvbKf8uMcba9oVLvAOcLVCo-MGcfS2Z100" width="100%" />

<br />

## 實現方式

- 基本實現

    假設表示檔案系統中的檔案與資料夾。

    ```java
    /** 元件介面 */
    public interface FileSystemComponent {
        void display();
    }

    /** 葉子：檔案 */
    public class File implements FileSystemComponent {
        private String name;

        public File(String name) {
            this.name = name;
        }

        @Override
        public void display() {
            System.out.println("File: " + name);
        }
    }

    /** 組合物件：資料夾 */
    public class Folder implements FileSystemComponent {
        private String name;
        private java.util.List<FileSystemComponent> children = new java.util.ArrayList<>();

        public Folder(String name) {
            this.name = name;
        }

        public void add(FileSystemComponent component) {
            children.add(component);
        }

        public void remove(FileSystemComponent component) {
            children.remove(component);
        }

        @Override
        public void display() {
            System.out.println("Folder: " + name);
            for (FileSystemComponent component : children) {
                component.display();
            }
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Folder root = new Folder("root");
            Folder subFolder = new Folder("docs");
            File file1 = new File("file1.txt");
            File file2 = new File("file2.txt");

            subFolder.add(file1);
            root.add(subFolder);
            root.add(file2);
            root.display();
            // Folder: root
            // Folder: docs
            // File: file1.txt
            // File: file2.txt
        }
    }
    ```

    特點：檔案與資料夾透過統一介面操作，簡化樹狀結構管理。

- JavaScript 實現 Composite

    表示 DOM 樹中的元素與容器。

    ```javascript
    /** 元件介面 */
    class DOMElement {
      constructor(name) {
        this.name = name;
      }

      display() {
        throw new Error("Method 'display()' must be implemented.");
      }
    }

    /** 葉子：單一元素 */
    class SingleElement extends DOMElement {
      display() {
        return `<${this.name}>${this.name}</${this.name}>`;
      }
    }

    /** 組合物件：容器元素 */
    class ContainerElement extends DOMElement {
      constructor(name) {
        super(name);
        this.children = [];
      }

	  add(element) {
	    this.children.push(element);
	  }

      remove(element) {
        this.children = this.children.filter(child => child !== element);
      }

      display() {
        const childrenContent = this.children.map(child => child.display()).join('');
        return `<${this.name}>${childrenContent}</${this.name}>`;
      }
    }



    /** 使用範例 */
    const root = new ContainerElement('div');
    const subContainer = new ContainerElement('section');
    const element1 = new SingleElement('p');
    const element2 = new SingleElement('span');

    subContainer.add(element1);
    root.add(subContainer);
    root.add(element2);
    console.log(root.display()); // <div><section><p>p</p></section><span>span</span></div>
    ```

    特點：統一處理 DOM 元素與容器，適合前端樹狀結構。

- TypeScript 實現 Composite

    表示 UI 元件樹。

    ```typescript
    /** 元件介面 */
    interface UIComponent {
      render(): string;
    }

    /** 葉子：單一元件 */
    class SingleComponent implements UIComponent {
      constructor(private name: string) {}

      render(): string {
        return `<${this.name}>${this.name}</${this.name}>`;
      }
    }

    /** 組合物件：容器元件 */
    class ContainerComponent implements UIComponent {
      private children: UIComponent[] = [];

      constructor(private name: string) {}

      add(component: UIComponent) {
        this.children.push(component);
      }

      remove(component: UIComponent) {
        this.children = this.children.filter(child => child !== component);
      }

      render(): string {
        const childrenContent = this.children.map(child => child.render()).join('');
        return `<${this.name}>${childrenContent}</${this.name}>`;
      }
    }



	/** 使用範例 */
	const root = new ContainerComponent('div');
	const subContainer = new ContainerComponent('section');
	const component1 = new SingleComponent('p');
	const component2 = new SingleComponent('span');

    subContainer.add(component1);
    root.add(subContainer);
    root.add(component2);
    console.log(root.render()); // <div><section><p>p</p></section><span>span</span></div>
    ```

    特點：TypeScript 確保型別安全，適合 UI 元件層次結構。

- Angular 實現 Composite

    建構動態表單元件樹。

    ```typescript
    /** form.service.ts */
    import { Injectable } from '@angular/core';

    export interface FormComponent {
      render(): string;
    }

    @Injectable()
    export class InputField implements FormComponent {
      constructor(private id: string) {}

      render(): string {
        return `<input id="${this.id}" type="text" />`;
      }
    }

	@Injectable()
	export class FormContainer implements FormComponent {
	  private children: FormComponent[] = [];

      constructor(private id: string) {}

      add(component: FormComponent) {
        this.children.push(component);
      }

      remove(component: FormComponent) {
        this.children = this.children.filter(child => child !== component);
      }

      render(): string {
        const childrenContent = this.children.map(child => child.render()).join('');
        return `<form id="${this.id}">${childrenContent}</form>`;
      }
    }

    @Injectable()
    export class FormService {
      createForm(id: string) {
        return new FormContainer(id);
      }

      createInput(id: string) {
        return new InputField(id);
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { FormService } from './form.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [FormService],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { FormService } from './form.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="buildForm()">建構表單</button>`
    })
    export class AppComponent {
      constructor(private formService: FormService) {}

      buildForm() {
        const form = this.formService.createForm('form1');
        const input1 = this.formService.createInput('input1');
        const input2 = this.formService.createInput('input2');
        form.add(input1);
        form.add(input2);
        console.log(form.render()); // <form id="form1"><input id="input1" type="text" /><input id="input2" type="text" /></form>
      }
    }
    ```

    特點：Angular 服務管理表單層次結構，支援動態建構。

- React 實現 Composite

    建構 UI 元件樹。

    ```javascript
    /** ComponentTree.js */
    class UIComponent {
      constructor(name) {
        this.name = name;
      }

      render() {
        throw new Error("Method 'render()' must be implemented.");
      }
    }

    class SingleComponent extends UIComponent {
      render() {
        return <div>{this.name}</div>;
      }
    }

    class ContainerComponent extends UIComponent {
      constructor(name) {
        super(name);
        this.children = [];
      }

	  add(component) {
	    this.children.push(component);
	  }

      remove(component) {
        this.children = this.children.filter(child => child !== component);
      }

      render() {
        return <div>{this.children.map(child => child.render())}</div>;
      }
    }

    /** App.jsx */
    import React from 'react';

    const App = () => {
      const root = new ContainerComponent('root');
      const subContainer = new ContainerComponent('section');
      const component1 = new SingleComponent('p');
      const component2 = new SingleComponent('span');

	  subContainer.add(component1);
	  root.add(subContainer);
	  root.add(component2);

      return root.render();
    };

    export default App;
    ```

    特點：統一處理 React 元件樹，簡化層次結構。

<br />

## 應用場景

Composite 模式適用於以下場景

- 管理樹狀結構，例如：檔案系統或 DOM 樹。

- 統一處理單一物件與組合物件。

- 前端中動態建構 UI 元件樹。

例如：Java 的 `java.awt.Component` 與 `Container` 使用 Composite 模式。

<br />

## 優缺點

### 優點

- 統一操作：單一物件與組合物件使用一致介面。

- 簡化客戶端：無需區分葉子與容器。

- 靈活性：易於新增元件。

- 符合開閉原則：新增元件無需修改既有程式碼。

### 缺點

- 程式碼複雜度：樹狀結構管理較複雜。

- 效能開銷：遞迴操作可能增加開銷。

- 通用性限制：葉子與容器行為需高度一致。

<br />

## 注意事項

- 介面一致性：確保葉子與容器有統一操作。

- 遞迴管理：小心處理深層樹結構。

- 深拷貝 vs 淺拷貝：Clone 元件時選擇合適拷貝方式。

- 避免濫用：簡單結構可使用其他模式。

<br />

## 與其他模式的關係

- 與 Bridge：Composite 聚焦樹狀結構，Bridge 分離抽象與實現。

- 與 Decorator：Composite 管理層次，Decorator 增強功能。

- 與 Iterator：Composite 常與 Iterator 結合遍歷樹。

- 與 Flyweight：Composite 可與 Flyweight 結合優化記憶體。

<br />

## 總結

Composite 模式透過統一介面管理樹狀結構，適合複雜層次系統。

在前端中，此模式適用於動態 UI 元件樹建構。

理解 Composite 有助於設計可擴展架構，提升程式碼可維護性。
