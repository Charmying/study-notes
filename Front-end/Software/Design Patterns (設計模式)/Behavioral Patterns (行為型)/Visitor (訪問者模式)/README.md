# Visitor (訪問者模式)

Visitor (訪問者模式) 是一種行為型設計模式，允許在不修改物件結構的情況下，為物件結構中的元素新增新的操作。透過將操作封裝到獨立的訪問者類別，實現結構與行為的分離，提升程式碼的靈活性與可維護性。

這種模式特別適合用於處理複雜物件結構，例如：樹狀結構或異構物件集合，當需要新增操作但不希望改變原有類別時。

<br />

## 動機

在軟體系統中，經常需要對複雜物件結構執行不同操作，例如

- 報表生成：對文件結構中的不同元素 (例如：段落、表格) 生成不同格式的報表。

- 樹狀結構處理：對樹節點執行遍歷、計算或格式化操作。

- 異構物件集合：對不同類型的物件執行統一操作，例如：驗證或匯出。

若將所有操作直接寫在物件類別中，會導致類別職責過重，且新增操作需修改原有程式碼，違反開閉原則。

Visitor 模式透過將操作封裝到訪問者類別，讓物件結構保持穩定，同時支援動態新增操作。

<br />

## 結構

Visitor 模式的結構包含以下元素

- 訪問者介面 (Visitor Interface)：定義對每種元素類型的訪問方法。

- 具體訪問者 (Concrete Visitor)：實現訪問者介面，提供具體操作。

- 元素介面 (Element Interface)：定義接受訪問者的方法。

- 具體元素 (Concrete Element)：實現元素介面，接受訪問者並調用相應方法。

- 物件結構 (Object Structure)：管理元素集合，允許訪問者遍歷。

以下是 Visitor 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/lL9D2y8m3BqN-Xzwt93j1umnPiMRu47mNhi8bNr8c-sY_dStrZgsgIY2joOloNjvQMfGQAoBd19L8kYZaC3soYYiDBjGmjY2DLsupg604fSUz8-8hQfIQa1mY3-lvY-hULjzeuGIcGjZ7kW_cOTzBU9OXPHmHg_fjKJEZkUAdOPVclbNpTl32IJkKDSIQmrzRy3ilYPY6sKmjgCJEpZBR6BmnIRyZwZTOU9h64wlHOapS8GwPzx3d9BfGbKG94uT9JEZE_J1F7DoXAPGPktVlWC0" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現文件結構的報表生成。

    ```java
    public interface DocumentVisitor {
        void visitParagraph(Paragraph paragraph);
        void visitTable(Table table);
    }

    public class HtmlReportVisitor implements DocumentVisitor {
        @Override
        public void visitParagraph(Paragraph paragraph) {
            System.out.println("生成 HTML 段落: " + paragraph.getContent());
        }

        @Override
        public void visitTable(Table table) {
            System.out.println("生成 HTML 表格: " + table.getRows() + " 行");
        }
    }

    public class PdfReportVisitor implements DocumentVisitor {
        @Override
        public void visitParagraph(Paragraph paragraph) {
            System.out.println("生成 PDF 段落: " + paragraph.getContent());
        }

        @Override
        public void visitTable(Table table) {
            System.out.println("生成 PDF 表格: " + table.getRows() + " 行");
        }
    }

    public interface DocumentElement {
        void accept(DocumentVisitor visitor);
    }

    public class Paragraph implements DocumentElement {
        private String content;

        public Paragraph(String content) {
            this.content = content;
        }

        public String getContent() {
            return content;
        }

        @Override
        public void accept(DocumentVisitor visitor) {
            visitor.visitParagraph(this);
        }
    }

    public class Table implements DocumentElement {
        private int rows;

        public Table(int rows) {
            this.rows = rows;
        }

        public int getRows() {
            return rows;
        }

        @Override
        public void accept(DocumentVisitor visitor) {
            visitor.visitTable(this);
        }
    }

    public class Document {
        private List<DocumentElement> elements = new ArrayList<>();

        public void addElement(DocumentElement element) {
            elements.add(element);
        }

        public void accept(DocumentVisitor visitor) {
            for (DocumentElement element : elements) {
                element.accept(visitor);
            }
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            Document doc = new Document();
            doc.addElement(new Paragraph("介紹內容"));
            doc.addElement(new Table(3));

            DocumentVisitor htmlVisitor = new HtmlReportVisitor();
            doc.accept(htmlVisitor);
            // 生成 HTML 段落: 介紹內容
            // 生成 HTML 表格: 3 行

            DocumentVisitor pdfVisitor = new PdfReportVisitor();
            doc.accept(pdfVisitor);
            // 生成 PDF 段落: 介紹內容
            // 生成 PDF 表格: 3 行
        }
    }
    ```

    特點：文件元素接受訪問者，操作由訪問者實現，結構不變。

- JavaScript 實現 Visitor

    用於處理樹狀結構的節點計算。

    ```javascript
    class TreeVisitor {
      visitLeaf(leaf) {
        throw new Error("Method 'visitLeaf()' must be implemented.");
      }

      visitNode(node) {
        throw new Error("Method 'visitNode()' must be implemented.");
      }
    }

    class SumVisitor extends TreeVisitor {
      visitLeaf(leaf) {
        console.log(`計算葉節點值: ${leaf.value}`);
      }

      visitNode(node) {
        console.log(`計算子節點總和: ${node.children.length} 個子節點`);
      }
    }

    class CountVisitor extends TreeVisitor {
      visitLeaf(leaf) {
        console.log(`計數葉節點: 1`);
      }

      visitNode(node) {
        console.log(`計數子節點: ${node.children.length}`);
      }
    }

    class TreeElement {
      accept(visitor) {
        throw new Error("Method 'accept()' must be implemented.");
      }
    }

    class Leaf extends TreeElement {
      constructor(value) {
        super();
        this.value = value;
      }

      accept(visitor) {
        visitor.visitLeaf(this);
      }
    }

    class Node extends TreeElement {
      constructor(children) {
        super();
        this.children = children;
      }

      accept(visitor) {
        visitor.visitNode(this);
        this.children.forEach(child => child.accept(visitor));
      }
    }



    /** 使用範例 */
    const tree = new Node([
      new Leaf(5),
      new Node([new Leaf(3), new Leaf(7)])
    ]);

    const sumVisitor = new SumVisitor();
    tree.accept(sumVisitor);
    // 計算子節點總和: 2 個子節點
    // 計算葉節點值: 5
    // 計算子節點總和: 2 個子節點
    // 計算葉節點值: 3
    // 計算葉節點值: 7

    const countVisitor = new CountVisitor();
    tree.accept(countVisitor);
    // 計數子節點: 2
    // 計數葉節點: 1
    // 計數子節點: 2
    // 計數葉節點: 1
    // 計數葉節點: 1
    ```

    特點：適合前端處理樹狀結構，動態新增操作。

- TypeScript 實現 Visitor

    用於檔案系統的內容檢查，確保型別安全。

    ```javascript
    interface FileSystemVisitor {
      visitFile(file: File): void;
      visitDirectory(directory: Directory): void;
    }

    class SizeVisitor implements FileSystemVisitor {
      visitFile(file: File) {
        console.log(`計算檔案大小: ${file.size} 位元組`);
      }

      visitDirectory(directory: Directory) {
        console.log(`計算目錄內檔案數: ${directory.files.length}`);
      }
    }

    class ListVisitor implements FileSystemVisitor {
      visitFile(file: File) {
        console.log(`列出檔案: ${file.name}`);
      }

      visitDirectory(directory: Directory) {
        console.log(`列出目錄: ${directory.name}`);
      }
    }

    interface FileSystemElement {
      accept(visitor: FileSystemVisitor): void;
    }

    class File implements FileSystemElement {
      name: string;
      size: number;

      constructor(name: string, size: number) {
        this.name = name;
        this.size = size;
      }

      accept(visitor: FileSystemVisitor) {
        visitor.visitFile(this);
      }
    }

    class Directory implements FileSystemElement {
      name: string;
      files: FileSystemElement[];

      constructor(name: string, files: FileSystemElement[]) {
        this.name = name;
        this.files = files;
      }

      accept(visitor: FileSystemVisitor) {
        visitor.visitDirectory(this);
        this.files.forEach(file => file.accept(visitor));
      }
    }



    /** 使用範例 */
    const fileSystem = new Directory("root", [
      new File("doc.txt", 100),
      new Directory("subfolder", [new File("image.png", 200)])
    ]);

    const sizeVisitor = new SizeVisitor();
    fileSystem.accept(sizeVisitor);
    // 計算目錄內檔案數: 2
    // 計算檔案大小: 100 位元組
    // 計算目錄內檔案數: 1
    // 計算檔案大小: 200 位元組

    const listVisitor = new ListVisitor();
    fileSystem.accept(listVisitor);
    // 列出目錄: root
    // 列出檔案: doc.txt
    // 列出目錄: subfolder
    // 列出檔案: image.png
    ```

    特點：TypeScript 確保訪問者與元素的型別一致。

- Angular 實現 Visitor

    使用 Angular 服務處理 UI 元件結構。

    ```javascript
    /** visitor.service.ts */
    import { Injectable } from '@angular/core';

    export interface UiVisitor {
      visitButton(button: ButtonElement): void;
      visitInput(input: InputElement): void;
    }

    @Injectable({
      providedIn: 'root'
    })
    export class RenderVisitor implements UiVisitor {
      visitButton(button: ButtonElement) {
        console.log(`渲染按鈕: ${button.label}`);
      }

      visitInput(input: InputElement) {
        console.log(`渲染輸入框: ${input.placeholder}`);
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class ValidateVisitor implements UiVisitor {
      visitButton(button: ButtonElement) {
        console.log(`驗證按鈕: ${button.label} 可點擊`);
      }

      visitInput(input: InputElement) {
        console.log(`驗證輸入框: ${input.placeholder} 內容有效`);
      }
    }

    export interface UiElement {
      accept(visitor: UiVisitor): void;
    }

    @Injectable({
      providedIn: 'root'
    })
    export class ButtonElement implements UiElement {
      label: string;

      constructor(label: string) {
        this.label = label;
      }

      accept(visitor: UiVisitor) {
        visitor.visitButton(this);
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class InputElement implements UiElement {
      placeholder: string;

      constructor(placeholder: string) {
        this.placeholder = placeholder;
      }

      accept(visitor: UiVisitor) {
        visitor.visitInput(this);
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class UiStructure {
      private elements: UiElement[] = [];

      addElement(element: UiElement) {
        this.elements.push(element);
      }

      accept(visitor: UiVisitor) {
        this.elements.forEach(element => element.accept(visitor));
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { UiStructure, RenderVisitor, ValidateVisitor, ButtonElement, InputElement } from './visitor.service';

    @Component({
      selector: 'app-root',
      template: `
        <button (click)="render()">渲染 UI</button>
        <button (click)="validate()">驗證 UI</button>
      `
    })
    export class AppComponent {
      constructor(
        private uiStructure: UiStructure,
        private renderVisitor: RenderVisitor,
        private validateVisitor: ValidateVisitor
      ) {
        this.uiStructure.addElement(new ButtonElement("提交"));
        this.uiStructure.addElement(new InputElement("輸入姓名"));
      }

      render() {
        this.uiStructure.accept(this.renderVisitor);
      }

      validate() {
        this.uiStructure.accept(this.validateVisitor);
      }
    }
    ```

    特點：利用 Angular 依賴注入，動態處理 UI 元件。

- React 實現 Visitor

    使用 React Hook 處理元件結構。

    ```javascript
    /** UiVisitor.js */
    class UiVisitor {
      visitButton(button) {
        throw new Error("Method 'visitButton()' must be implemented.");
      }

      visitInput(input) {
        throw new Error("Method 'visitInput()' must be implemented.");
      }
    }

    class RenderVisitor extends UiVisitor {
      visitButton(button) {
        console.log(`渲染按鈕: ${button.label}`);
      }

      visitInput(input) {
        console.log(`渲染輸入框: ${input.placeholder}`);
      }
    }

    class ValidateVisitor extends UiVisitor {
      visitButton(button) {
        console.log(`驗證按鈕: ${button.label} 可點擊`);
      }

      visitInput(input) {
        console.log(`驗證輸入框: ${input.placeholder} 內容有效`);
      }
    }



    /** UiElement.js */
    class UiElement {
      accept(visitor) {
        throw new Error("Method 'accept()' must be implemented.");
      }
    }

    class ButtonElement extends UiElement {
      constructor(label) {
        super();
        this.label = label;
      }

      accept(visitor) {
        visitor.visitButton(this);
      }
    }

    class InputElement extends UiElement {
      constructor(placeholder) {
        super();
        this.placeholder = placeholder;
      }

      accept(visitor) {
        visitor.visitInput(this);
      }
    }

    class UiStructure {
      constructor() {
        this.elements = [];
      }

      addElement(element) {
        this.elements.push(element);
      }

      accept(visitor) {
        this.elements.forEach(element => element.accept(visitor));
      }
    }



    /** UiContext.js */
    import { createContext, useContext } from 'react';

    const UiContext = createContext(null);
    export const useUiContext = () => useContext(UiContext);



    /** App.jsx */
    import React, { useState } from 'react';
    import { UiContext } from './UiContext';

    const UiPanel = () => {
      const { structure, render, validate } = useUiContext();
      return (
        <div>
          <button onClick={render}>渲染 UI</button>
          <button onClick={validate}>驗證 UI</button>
        </div>
      );
    };

    const App = () => {
      const structure = new UiStructure();
      structure.addElement(new ButtonElement("提交"));
      structure.addElement(new InputElement("輸入姓名"));

      const [visitor, setVisitor] = useState(new RenderVisitor());

      const render = () => structure.accept(new RenderVisitor());
      const validate = () => structure.accept(new ValidateVisitor());

      return (
        <UiContext.Provider value={{ structure, render, validate }}>
          <UiPanel />
        </UiContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Hook，動態處理元件結構操作。

<br />

## 應用場景

Visitor 模式適用於以下場景

- 複雜物件結構

    例如：文件結構、樹狀結構或異構物件集合的處理。

- 動態新增操作

    例如：新增報表生成或驗證功能，無需修改元素類別。

- 結構穩定

    例如：物件結構穩定，但操作頻繁變化。

- 分離職責

    例如：將操作功能從結構中分離，提升可維護性。

例如

- 在前端，Visitor 用於處理複雜 UI 元件結構或樹狀資料。

- Java 的 `java.nio.file.FileVisitor` 是 Visitor 模式的典型應用。

<br />

## 優缺點

### 優點

- 符合開閉原則：新增操作無需修改元素類別。

- 分離職責：操作功能與物件結構解耦。

- 靈活性：支援動態新增訪問者，適應不同需求。

- 集中操作：相關操作集中在訪問者類別，便於管理。

### 缺點

- 類別數量增加：每個操作需一個訪問者類別。

- 結構修改困難：新增元素類型需修改所有訪問者。

- 複雜性：對簡單結構，Visitor 模式可能過於複雜。

<br />

## 注意事項

- 結構穩定性：Visitor 適合結構穩定但操作變化的場景。

- 訪問者擴展：確保訪問者介面涵蓋所有元素類型。

- 效能考量：遍歷複雜結構可能影響效能，需優化。

- 狀態管理：若訪問者需維護狀態，需小心處理。

<br />

## 與其他模式的關係

- 與迭代器模式 (Iterator)：Iterator 遍歷結構，Visitor 執行操作。

- 與命令模式 (Command)：Command 封裝單一操作，Visitor 處理結構操作。

- 與組合模式 (Composite)：Visitor 常與 Composite 結合，處理樹狀結構。

<br />

## 總結

Visitor 模式是一種強大的行為型設計模式，透過將操作封裝到訪問者類別，實現結構與行為的分離，特別適合處理複雜物件結構或動態新增操作的場景，例如：文件報表生成或樹狀資料處理。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據專案需求選擇最適合的工具。需注意結構穩定性與程式碼複雜度，確保高效實現。對於追求靈活操作與可維護性設計的開發人員而言，Visitor 模式是一個核心工具，能顯著提升系統的擴展性與清晰度。
