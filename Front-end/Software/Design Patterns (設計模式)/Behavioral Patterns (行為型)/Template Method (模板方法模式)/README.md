# Template Method (模板方法模式)

Template Method (模板方法模式) 是一種行為型設計模式，定義了一個操作的演算法骨架，將某些步驟的實現延遲到子類別，使子類別能在不改變演算法結構的情況下重新定義特定步驟。此模式確保核心流程一致，同時允許靈活的客製化。

這種模式特別適合用於具有固定流程但部分步驟需客製化的場景，例如：文件處理流程、資料處理管道或遊戲關卡初始化。

<br />

## 動機

在軟體系統中，許多操作遵循固定流程，但部分步驟因情境不同而變化，例如

- 文件處理：不同格式 (例如：PDF、Word) 的文件處理流程相同，但解析方式不同。

- 遊戲關卡：關卡初始化遵循相同步驟，但具體內容因關卡而異。

- 資料驗證：資料處理有固定步驟，但驗證規則因資料類型不同。

若每個子類別重複實現整個流程，會導致程式碼冗餘，難以維護。

Template Method 模式透過將不變的流程定義在抽象類別，僅讓子類別實現可變步驟，解決這些問題，提升程式碼重用性與可維護性。

<br />

## 結構

Template Method 模式的結構包含以下元素

- 抽象類別 (Abstract Class)：定義模板方法 (演算法骨架) 與抽象步驟。

- 具體類別 (Concrete Class)：實現抽象步驟，提供具體行為。

- 鉤子方法 (Hook Method)：可選方法，子類別可選擇覆寫以客製化行為。

以下是 Template Method 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULAJ2ekAKfCBb58paaiBbPmX7ATmRngNYu51Ms5ajJSWfp4abJVr9AC_1GDJP2eiW9CPt19Qe4XDa4ZYA2sGaP-VZP2Roql5oyNn3Rd_BpaejIILB1jZX3hg6-m4sa6Wur13GUR6brTDCSILkB4o-MGcfS236K0" width="100%" />

<br />

## 實現方式

- 基本實現

    使用 Java 實現文件處理流程。

    ```java
    public abstract class DocumentProcessor {
        /** 模板方法，定義處理流程 */
        public final void processDocument() {
            openDocument();
            parseContent();
            if (needValidation()) {
                validateContent();
            }
            saveDocument();
        }

        /** 抽象步驟，由子類別實現 */
        protected abstract void openDocument();
        protected abstract void parseContent();

        /** 鉤子方法，子類別可選擇覆寫 */
        protected boolean needValidation() {
            return true;
        }

        /** 抽象步驟 */
        protected abstract void validateContent();

        /** 預設實現 */
        protected void saveDocument() {
            System.out.println("儲存文件到資料庫");
        }
    }

    public class PdfProcessor extends DocumentProcessor {
        @Override
        protected void openDocument() {
            System.out.println("開啟 PDF 文件");
        }

        @Override
        protected void parseContent() {
            System.out.println("解析 PDF 內容");
        }

        @Override
        protected void validateContent() {
            System.out.println("驗證 PDF 文件格式");
        }
    }

    public class WordProcessor extends DocumentProcessor {
        @Override
        protected void openDocument() {
            System.out.println("開啟 Word 文件");
        }

        @Override
        protected void parseContent() {
            System.out.println("解析 Word 內容");
        }

        @Override
        protected void validateContent() {
            System.out.println("驗證 Word 文件格式");
        }

        @Override
        protected boolean needValidation() {
            return false; // Word 文件不需要驗證
        }
    }



    /** 使用範例 */
    public class Main {
        public static void main(String[] args) {
            DocumentProcessor pdf = new PdfProcessor();
            pdf.processDocument();
            // 開啟 PDF 文件
            // 解析 PDF 內容
            // 驗證 PDF 文件格式
            // 儲存文件到資料庫

            DocumentProcessor word = new WordProcessor();
            word.processDocument();
            // 開啟 Word 文件
            // 解析 Word 內容
            // 儲存文件到資料庫
        }
    }
    ```

    特點：模板方法確保流程一致，子類別僅實現特定步驟。

- JavaScript 實現 Template Method

    用於資料處理管道。

    ```javascript
    class DataPipeline {
      processData(data) {
        this.loadData(data);
        this.transformData();
        if (this.needValidation()) {
          this.validateData();
        }
        this.saveData();
      }

      loadData(data) {
        console.log("載入資料: ", data);
      }

      transformData() {
        throw new Error("Method 'transformData()' must be implemented.");
      }

      needValidation() {
        return true;
      }

      validateData() {
        throw new Error("Method 'validateData()' must be implemented.");
      }

      saveData() {
        console.log("儲存資料到伺服器");
      }
    }

    class JsonPipeline extends DataPipeline {
      transformData() {
        console.log("轉換資料為 JSON 格式");
      }

      validateData() {
        console.log("驗證 JSON 資料格式");
      }
    }

    class XmlPipeline extends DataPipeline {
      transformData() {
        console.log("轉換資料為 XML 格式");
      }

      validateData() {
        console.log("驗證 XML 資料格式");
      }

      needValidation() {
        return false;
      }
    }



    /** 使用範例 */
    const jsonPipeline = new JsonPipeline();
    jsonPipeline.processData({ id: 1 }); // 載入資料: { id: 1 }
    // 轉換資料為 JSON 格式
    // 驗證 JSON 資料格式
    // 儲存資料到伺服器

    const xmlPipeline = new XmlPipeline();
    xmlPipeline.processData({ id: 2 }); // 載入資料: { id: 2 }
    // 轉換資料為 XML 格式
    // 儲存資料到伺服器
    ```

    特點：簡化前端資料處理流程，支援客製化步驟。

- TypeScript 實現 Template Method

    用於遊戲關卡初始化，確保型別安全。

    ```javascript
    abstract class LevelInitializer {
      initializeLevel() {
        this.loadResources();
        this.setupEnvironment();
        if (this.needEnemySetup()) {
          this.setupEnemies();
        }
        this.startLevel();
      }

      protected abstract loadResources(): void;
      protected abstract setupEnvironment(): void;

      protected needEnemySetup(): boolean {
        return true;
      }

      protected abstract setupEnemies(): void;

      protected startLevel() {
        console.log("啟動關卡");
      }
    }

    class EasyLevel extends LevelInitializer {
      protected loadResources() {
        console.log("載入簡單關卡資源");
      }

      protected setupEnvironment() {
        console.log("設置簡單關卡環境");
      }

      protected setupEnemies() {
        console.log("設置簡單關卡敵人");
      }
    }

    class HardLevel extends LevelInitializer {
      protected loadResources() {
        console.log("載入困難關卡資源");
      }

      protected setupEnvironment() {
        console.log("設置困難關卡環境");
      }

      protected setupEnemies() {
        console.log("設置困難關卡敵人");
      }

      protected needEnemySetup(): boolean {
        return false;
      }
    }



    /** 使用範例 */
    const easyLevel = new EasyLevel();
    easyLevel.initializeLevel(); // 載入簡單關卡資源
    // 設置簡單關卡環境
    // 設置簡單關卡敵人
    // 啟動關卡

    const hardLevel = new HardLevel();
    hardLevel.initializeLevel(); // 載入困難關卡資源
    // 設置困難關卡環境
    // 啟動關卡
    ```

    特點：TypeScript 確保抽象方法與鉤子方法的型別一致。

- Angular 實現 Template Method

    使用 Angular 服務實現表單處理流程。

    ```javascript
    /** form-processor.service.ts */
    import { Injectable } from '@angular/core';

    export abstract class FormProcessor {
      processForm(data: any) {
        this.validateInput(data);
        this.transformData(data);
        if (this.needSubmission()) {
          this.submitData(data);
        }
        this.notifyUser();
      }

      protected abstract validateInput(data: any): void;
      protected abstract transformData(data: any): void;

      protected needSubmission(): boolean {
        return true;
      }

      protected abstract submitData(data: any): void;

      protected notifyUser() {
        console.log("通知使用者：表單處理完成");
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class RegistrationFormProcessor extends FormProcessor {
      protected validateInput(data: any) {
        console.log("驗證註冊表單資料", data);
      }

      protected transformData(data: any) {
        console.log("轉換註冊表單資料為 JSON");
      }

      protected submitData(data: any) {
        console.log("提交註冊表單資料到伺服器");
      }
    }

    @Injectable({
      providedIn: 'root'
    })
    export class LoginFormProcessor extends FormProcessor {
      protected validateInput(data: any) {
        console.log("驗證登入表單資料", data);
      }

      protected transformData(data: any) {
        console.log("轉換登入表單資料為加密格式");
      }

      protected submitData(data: any) {
        console.log("提交登入表單資料到伺服器");
      }

      protected needSubmission(): boolean {
        return false;
      }
    }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { RegistrationFormProcessor, LoginFormProcessor } from './form-processor.service';

    @Component({
      selector: 'app-root',
      template: `
        <button (click)="processRegistration()">處理註冊表單</button>
        <button (click)="processLogin()">處理登入表單</button>
      `
    })
    export class AppComponent {
      constructor(
        private registrationProcessor: RegistrationFormProcessor,
        private loginProcessor: LoginFormProcessor
      ) {}

      processRegistration() {
        this.registrationProcessor.processForm({ user: 'test' });
      }

      processLogin() {
        this.loginProcessor.processForm({ user: 'test' });
      }
    }
    ```

    特點：利用 Angular 依賴注入，實現表單處理的統一流程。

- React 實現 Template Method

    使用 React Hook 實現資料匯出流程。

    ```javascript
    /** DataExport.js */
    class DataExport {
      exportData(data) {
        this.prepareData(data);
        this.formatData(data);
        if (this.needCompression()) {
          this.compressData(data);
        }
        this.saveData(data);
      }

      prepareData(data) {
        console.log("準備資料:", data);
      }

      formatData(data) {
        throw new Error("Method 'formatData()' must be implemented.");
      }

      needCompression() {
        return true;
      }

      compressData(data) {
        throw new Error("Method 'compressData()' must be implemented.");
      }

      saveData(data) {
        console.log("儲存資料到檔案");
      }
    }

    class CsvExport extends DataExport {
      formatData(data) {
        console.log("格式化資料為 CSV");
      }

      compressData(data) {
        console.log("壓縮 CSV 資料");
      }
    }

    class JsonExport extends DataExport {
      formatData(data) {
        console.log("格式化資料為 JSON");
      }

      compressData(data) {
        console.log("壓縮 JSON 資料");
      }

      needCompression() {
        return false;
      }
    }



    /** DataExportContext.js */
    import { createContext, useContext, useState } from 'react';

    const DataExportContext = createContext(null);
    export const useDataExport = () => useContext(DataExportContext);



    /** App.jsx */
    import React from 'react';
    import { DataExportContext } from './DataExportContext';

    const Exporter = () => {
      const { exporter, exportData } = useDataExport();
      const data = { id: 1, name: 'test' };

      return <button onClick={() => exportData(data)}>匯出資料</button>;
    };

    const App = () => {
      const [exporter, setExporter] = useState(new CsvExport());

      const exportData = (data) => {
        exporter.exportData(data);
      };

      return (
        <DataExportContext.Provider value={{ exporter, exportData }}>
          <button onClick={() => setExporter(new CsvExport())}>使用 CSV</button>
          <button onClick={() => setExporter(new JsonExport())}>使用 JSON</button>
          <Exporter />
        </DataExportContext.Provider>
      );
    };

    export default App;
    ```

    特點：結合 React Hook，實現資料匯出的統一流程。

<br />

## 應用場景

Template Method 模式適用於以下場景

- 固定流程客製化

    例如：文件處理或資料匯出的標準流程。

- 遊戲關卡初始化

    例如：不同關卡遵循相同初始化步驟。

- 資料處理管道

    例如：資料驗證與轉換的固定流程。

- 框架設計

    例如：框架提供預設流程，允許使用者客製化步驟。

例如

- 在前端，Template Method 用於管理 UI 或資料處理流程。

- Java 的 `AbstractList` 和 `AbstractMap` 使用模板方法定義核心行為。

<br />

## 優缺點

### 優點

- 程式碼重用：共用演算法骨架，減少重複程式碼。

- 符合開閉原則：新增具體類別無需修改抽象類別。

- 流程一致性：確保所有子類別遵循相同流程。

- 靈活性：鉤子方法提供客製化彈性。

### 缺點

- 類別數量增加：每個具體實現需一個子類別。

- 繼承限制：依賴繼承，可能限制靈活性。

- 複雜流程：若流程過於複雜，模板方法可能難以維護。

<br />

## 注意事項

- 模板方法最終性：模板方法應設為 `final`，避免子類別修改流程。

- 鉤子方法設計：提供足夠的鉤子方法，增加客製化彈性。

- 抽象層次：確保抽象類別不過於複雜，保持清晰性。

- 測試性：每個具體類別需獨立測試，確保步驟正確。

<br />

## 與其他模式的關係

- 與策略模式 (Strategy)：Strategy 注重行為替換，Template Method 聚焦流程骨架。

- 與工廠方法 (Factory Method)：Factory Method 可作為模板方法的一步。

- 與狀態模式 (State)：State 處理狀態切換，Template Method 處理固定流程。

<br />

## 總結

Template Method 模式是一種實用的行為型設計模式，透過定義演算法骨架並延遲步驟實現到子類別，實現流程一致性與客製化靈活性。特別適合用於具有固定流程但需要客製化步驟的場景，例如：文件處理、資料管道或遊戲關卡初始化。

透過 Java、JavaScript、TypeScript、Angular 和 React 的實現方式，開發人員可根據應用需求選擇最適合的工具。需注意流程設計的清晰性與程式碼可維護性，確保高效實現。對於追求程式碼重用與一致性設計的開發人員而言，Template Method 模式是一個核心工具，能顯著提升系統的可維護性與擴展性。
