# Proxy (代理模式)

Proxy (代理模式) 是一種結構型設計模式，透過代理物件控制對另一物件的訪問，提供額外功能，例如：延遲載入、訪問控制或日誌記錄。

這種模式在不修改原始物件的情況下增強行為。

<br />

## 動機

軟體開發中，常需控制物件訪問或添加額外功能，例如

- 延遲載入大型資源，例如：圖片或資料庫查詢。

- 限制對敏感物件的訪問，例如：權限檢查。

- 前端中管理 API 請求，添加快取或日誌功能。

直接修改原始物件可能違反開閉原則或增加複雜性。

Proxy 模式透過代理層提供控制與擴展，解決此問題。

<br />

## 結構

Proxy 模式的結構包含以下元素

主體介面 (Subject Interface)：定義代理與真實物件的共同操作。

真實主體 (Real Subject)：執行核心功能的類別。

代理 (Proxy)：實作主體介面，控制對真實主體的訪問。

客戶端 (Client)：透過主體介面與代理交互。

以下是 Proxy 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuicFtozLJdkpkVZbt4KY0boiphoIrA2qnELKXk3GfApMvHA6Qbqj1GLkXABMmDBMuH4EJbwkMbmjcmFCvyv-kNmOn1c90SavYSR52K6fY3b46FDcz-Fc4DcIj0KNv5PKGJRf0JGXph91DnMVco-bpdknlWfW9qsnJewU7gXz51cmfBnV4RbrTEnGFM2cK5gSMyt8vfEQb00CF0000" width="100%" />

<br />

## 實現方式

- 基本實現

    假設延遲載入大型圖片。

    ```java
    /** 主體介面 */
    public interface Image {
        void display();
    }

    /** 真實主體 */
    public class RealImage implements Image {
        private String filename;

        public RealImage(String filename) {
            this.filename = filename;
            loadImage();
        }

        private void loadImage() {
            System.out.println("Loading image: " + filename);
        }

        @Override
        public void display() {
            System.out.println("Displaying image: " + filename);
        }
    }

    /** 代理 */
    public class ImageProxy implements Image {
        private RealImage realImage;
        private String filename;

        public ImageProxy(String filename) {
            this.filename = filename;
        }

        @Override
        public void display() {
            if (realImage == null) {
                realImage = new RealImage(filename);
            }
            realImage.display();
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Image image = new ImageProxy("test.jpg");
            image.display();
            // Loading image: test.jpg
            // Displaying image: test.jpg
            image.display(); // 僅顯示，不重複載入
            // Displaying image: test.jpg
        }
    }
    ```

    特點：代理實現延遲載入，減少不必要的資源消耗。

- JavaScript 實現 Proxy

    為 API 請求添加快取。

    ```javascript
    /** 主體介面 */
    class DataService {
      fetchData(id) {
        throw new Error("Method 'fetchData()' must be implemented.");
      }
    }

    /** 真實主體 */
    class RealDataService extends DataService {
      fetchData(id) {
        console.log(`Fetching data for id: ${id}`);
        return `Data for ${id}`;
      }
    }

    /** 代理 */
    class CacheProxy extends DataService {
      constructor() {
        super();
        this.realService = new RealDataService();
        this.cache = {};
      }

      fetchData(id) {
        if (this.cache[id]) {
          console.log(`Returning cached data for id: ${id}`);
          return this.cache[id];
        }
        const data = this.realService.fetchData(id);
        this.cache[id] = data;
        return data;
      }
    }

    /** 使用範例 */
    const proxy = new CacheProxy();
    console.log(proxy.fetchData(1)); // Fetching data for id: 1
    // Data for 1
    console.log(proxy.fetchData(1)); // Returning cached data for id: 1
    // Data for 1
    ```

    特點：代理添加快取功能，提升 API 請求效率。

- TypeScript 實現 Proxy

    控制對敏感資源的訪問。

    ```typescript
    /** 主體介面 */
    interface Resource {
      access(): string;
    }

    /** 真實主體 */
    class RealResource implements Resource {
      access(): string {
        return "Sensitive data accessed";
      }
    }

    /** 代理 */
    class AccessProxy implements Resource {
      private realResource: RealResource | null = null;
      private hasAccess: boolean;

      constructor(hasAccess: boolean) {
        this.hasAccess = hasAccess;
      }

      access(): string {
        if (!this.hasAccess) {
          return "Access denied";
        }
        if (!this.realResource) {
          this.realResource = new RealResource();
        }
        return this.realResource.access();
      }
    }



    /** 使用範例 */
    const allowedProxy = new AccessProxy(true);
    console.log(allowedProxy.access()); // Sensitive data accessed

    const deniedProxy = new AccessProxy(false);
    console.log(deniedProxy.access()); // Access denied
    ```

    特點：TypeScript 確保型別安全，實現訪問控制。

- Angular 實現 Proxy

    為資料服務添加日誌功能。

    ```typescript
    /** data.service.ts */
    import { Injectable } from '@angular/core';

    export interface DataService {
      fetch(): string;
    }

    @Injectable()
    export class RealDataService implements DataService {
      fetch(): string {
        return "Data fetched";
      }
    }

    @Injectable()
    export class LoggingProxy implements DataService {
      private realService: RealDataService;

      constructor(realService: RealDataService) {
        this.realService = realService;
      }

      fetch(): string {
        console.log("Logging: Fetching data");
        const result = this.realService.fetch();
        console.log("Logging: Data fetched");
        return result;
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { RealDataService, LoggingProxy } from './data.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [
        RealDataService,
        { provide: LoggingProxy, useClass: LoggingProxy, deps: [RealDataService] }
      ],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { LoggingProxy } from './data.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="fetchData()">獲取資料</button>`
    })
    export class AppComponent {
      constructor(private proxy: LoggingProxy) {}

      fetchData() {
        console.log(this.proxy.fetch());
        // Logging: Fetching data
        // Logging: Data fetched
        // Data fetched
      }
    }
    ```

    特點：Angular 服務透過代理添加日誌功能。

- React 實現 Proxy

    為圖片元件添加延遲載入。

    ```javascript
    /** ImageProxy.js */
    class ImageComponent {
      render(src) {
        console.log(`Loading image: ${src}`);
        return <img src={src} alt="image" />;
      }
    }

    class LazyLoadProxy {
      constructor() {
        this.imageComponent = null;
      }

      render(src) {
        if (!this.imageComponent) {
          this.imageComponent = new ImageComponent();
        }
        return this.imageComponent.render(src);
      }
    }



    /** App.jsx */
    import React from 'react';

    const App = () => {
      const proxy = new LazyLoadProxy();
      return (
        <div>
          {proxy.render('test.jpg')}
        </div>
      );
    };

    export default App;
    ```

    特點：代理實現圖片延遲載入，優化 React 渲染。

<br />

## 應用場景

Proxy 模式適用於以下場景

- 延遲載入大型資源，例如：圖片或資料。

- 控制訪問權限，例如：權限檢查。

- 前端中為 API 請求添加快取或日誌。

例如：Java 的 `java.lang.reflect.Proxy` 支援動態代理。

<br />

## 優缺點

### 優點

- 控制訪問：代理管理對真實物件的訪問。

- 符合開閉原則：無需修改原始類別。

- 靈活性：支援延遲載入、快取等功能。

- 透明性：客戶端無需感知代理存在。

### 缺點

- 程式碼複雜度：增加代理層可能提升維護成本。

- 效能開銷：代理處理可能略增延遲。

- 實現難度：動態代理需語言支援。

<br />

## 注意事項

- 代理類型：選擇虛擬代理、保護代理或智慧代理。

- 狀態管理：確保代理與真實主體同步。

- 深拷貝 vs 淺拷貝：Clone 代理時選擇合適拷貝方式。

- 避免濫用：簡單操作可直接訪問真實主體。

<br />

## 與其他模式的關係

- 與 Adapter：Proxy 提供相同介面，Adapter 轉換介面。

- 與 Decorator：Proxy 聚焦控制訪問，Decorator 增強功能。

- 與 Facade：Proxy 控制單一物件，Facade 簡化子系統。

- 與 Mediator：Proxy 管理單一物件訪問，Mediator 協調多物件。

<br />

## 總結

Proxy 模式透過代理層控制物件訪問，適合延遲載入或權限管理場景。

在前端中，此模式適用於 API 快取或資源載入優化。

理解 Proxy 有助於設計高效且安全的系統，提升程式碼可維護性。
