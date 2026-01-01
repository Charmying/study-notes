# Facade (外觀模式)

Facade (外觀模式) 是一種結構型設計模式，提供簡化介面，隱藏複雜子系統細節，使客戶端易於使用。

這種模式將子系統功能整合為統一入口，降低使用複雜度。

<br />

## 動機

軟體開發中，常需與複雜子系統交互，例如：

- 多個 API 模組需協同完成任務，例如：用戶認證與資料查詢。

- 前端需協調多個服務，例如：資料獲取、格式化與渲染。

- 檔案處理系統涉及多個模組，例如：讀取、解析與儲存。

直接操作子系統導致程式碼耦合度高且難以維護。Facade 模式透過單一介面封裝子系統，簡化操作。

<br />

## 結構

Facade 模式的結構包含以下元素

- 外觀 (Facade)：提供簡化介面，封裝子系統交互。

- 子系統 (Subsystem)：包含多個類別，執行具體功能。

- 客戶端 (Client)：透過外觀介面與子系統交互。

以下是 Facade 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLukcJQY-KD82OlLt9EOd6nWbjYSc9Aga8rBvU2WhP2Va5gKM99PdwUXYOlLoql5rpVsWdFD-z-ldKZijRWqgJYokAIr5n73EsEKFre2fqm53fXL-YCeT0PpKKlfyzvihy9uXoe7tHrxP3SX5tO2RkmCo-NGsfU2Z2a0000" width="100%" />

<br />

## 實現方式

- 基本實現 (Java，縮排 4 格)

    假設簡化多媒體播放系統。

    ```java
    /** 子系統：音訊模組 */
    public class AudioSystem {
        public void playAudio(String file) {
            System.out.println("Playing audio: " + file);
        }
    }

    /** 子系統：視訊模組 */
    public class VideoSystem {
        public void renderVideo(String file) {
            System.out.println("Rendering video: " + file);
        }
    }

    /** 子系統：字幕模組 */
    public class SubtitleSystem {
        public void displaySubtitle(String text) {
            System.out.println("Displaying subtitle: " + text);
        }
    }

    /** 外觀 */
    public class MediaPlayerFacade {
        private AudioSystem audioSystem;
        private VideoSystem videoSystem;
        private SubtitleSystem subtitleSystem;

        public MediaPlayerFacade() {
            this.audioSystem = new AudioSystem();
            this.videoSystem = new VideoSystem();
            this.subtitleSystem = new SubtitleSystem();
        }

        public void playMedia(String audioFile, String videoFile, String subtitleText) {
            audioSystem.playAudio(audioFile);
            videoSystem.renderVideo(videoFile);
            subtitleSystem.displaySubtitle(subtitleText);
        }
    }

    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            MediaPlayerFacade facade = new MediaPlayerFacade();
            facade.playMedia("song.mp3", "movie.mp4", "Hello World");
            // Playing audio: song.mp3
            // Rendering video: movie.mp4
            // Displaying subtitle: Hello World
        }
    }
    ```

    特點：外觀整合多媒體模組，提供簡單播放介面。

- JavaScript 實現 Facade

    簡化前端資料處理流程。

    ```javascript
    /** 子系統：資料獲取 */
    class DataFetcher {
      fetchData() {
        return { raw: 'raw data' };
      }
    }

    /** 子系統：資料格式化 */
    class DataFormatter {
      format(data) {
        return `Formatted: ${data.raw}`;
      }
    }

    /** 子系統：資料渲染 */
    class DataRenderer {
      render(formattedData) {
        return `<div>${formattedData}</div>`;
      }
    }

    /** 外觀 */
    class DataProcessingFacade {
      constructor() {
        this.fetcher = new DataFetcher();
        this.formatter = new DataFormatter();
        this.renderer = new DataRenderer();
      }

      processData() {
        const rawData = this.fetcher.fetchData();
        const formattedData = this.formatter.format(rawData);
        return this.renderer.render(formattedData);
      }
    }



    /** 使用範例 */
    const facade = new DataProcessingFacade();
    console.log(facade.processData()); // <div>Formatted: raw data</div>
    ```

    特點：外觀簡化資料獲取、格式化與渲染流程。

- TypeScript 實現 Facade

    簡化 API 請求流程。

    ```typescript
    /** 子系統：認證 */
    class AuthService {
      authenticate() {
        return 'Authenticated';
      }
    }

    /** 子系統：請求 */
    class RequestService {
      sendRequest(authToken: string) {
        return `Request sent with ${authToken}`;
      }
    }

    /** 子系統：回應處理 */
    class ResponseHandler {
      processResponse(response: string) {
        return `Processed: ${response}`;
      }
    }

    /** 外觀 */
    class ApiFacade {
      private authService: AuthService;
      private requestService: RequestService;
      private responseHandler: ResponseHandler;

      constructor() {
        this.authService = new AuthService();
        this.requestService = new RequestService();
        this.responseHandler = new ResponseHandler();
      }

      executeRequest(): string {
        const token = this.authService.authenticate();
        const response = this.requestService.sendRequest(token);
        return this.responseHandler.processResponse(response);
      }
    }



    /** 使用範例 */
    const facade = new ApiFacade();
    console.log(facade.executeRequest()); // Processed: Request sent with Authenticated
    ```

    特點：TypeScript 確保型別安全，簡化 API 請求流程。

- Angular 實現 Facade

    簡化表單處理流程。

    ```typescript
    /** form.service.ts */
    import { Injectable } from '@angular/core';

    export class FormValidator {
      validate(data: string) {
        return `Validated: ${data}`;
      }
    }

    export class FormFormatter {
      format(data: string) {
        return `Formatted: ${data}`;
      }
    }

    export class FormSubmitter {
      submit(formattedData: string) {
        return `Submitted: ${formattedData}`;
      }
    }

    @Injectable()
    export class FormFacade {
      private validator: FormValidator;
      private formatter: FormFormatter;
      private submitter: FormSubmitter;

      constructor() {
        this.validator = new FormValidator();
        this.formatter = new FormFormatter();
        this.submitter = new FormSubmitter();
      }

      processForm(data: string): string {
        const validatedData = this.validator.validate(data);
        const formattedData = this.formatter.format(validatedData);
        return this.submitter.submit(formattedData);
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { FormFacade } from './form.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [FormFacade],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { FormFacade } from './form.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="processForm()">處理表單</button>`
    })
    export class AppComponent {
      constructor(private formFacade: FormFacade) {}

      processForm() {
        console.log(this.formFacade.processForm('input data')); // Submitted: Formatted: Validated: input data
      }
    }
    ```

    特點：Angular 服務封裝表單處理流程，簡化客戶端操作。

- React 實現 Facade

    簡化 UI 渲染流程。

    ```javascript
    /** UIFacade.js */
    class DataService {
      fetch() {
        return 'data';
      }
    }

    class StyleService {
      applyStyle(data) {
        return `<div style="color: blue;">${data}</div>`;
      }
    }

    class RenderService {
      render(styledData) {
        return styledData;
      }
    }

    class UIFacade {
      constructor() {
        this.dataService = new DataService();
        this.styleService = new StyleService();
        this.renderService = new RenderService();
      }

      renderUI() {
        const data = this.dataService.fetch();
        const styledData = this.styleService.applyStyle(data);
        return this.renderService.render(styledData);
      }
    }



    /** App.jsx */
    import React from 'react';

    const App = () => {
      const facade = new UIFacade();
      const ui = facade.renderUI();

      return <div dangerouslySetInnerHTML={{ __html: ui }} />;
    };

    export default App;
    ```

    特點：外觀整合資料獲取、樣式與渲染，提升 React 元件簡潔性。

<br />

## 應用場景

Facade 模式適用於以下場景

- 簡化複雜子系統操作，例如：多模組協作。

- 降低客戶端與子系統耦合度。

- 前端中統一 API 請求或 UI 渲染流程。

例如：Java 的 `javax.faces.context.FacesContext` 封裝 JSF 子系統操作。

<br />

## 優缺點

### 優點

- 簡化介面：隱藏子系統複雜性。

- 降低耦合：客戶端僅依賴外觀。

- 提高可維護性：子系統變更不影響客戶端。

- 符合單一職責原則：外觀專注簡化交互。

### 缺點

- 外觀過載：可能成為過於龐大的介面。

- 隱藏細節過多：可能限制進階使用。

- 維護成本：子系統變化需更新外觀。

<br />

## 注意事項

- 介面簡潔：外觀應提供必要功能，避免過於複雜。

- 子系統獨立：確保子系統可獨立運作。

- 深拷貝 vs 淺拷貝：Clone 外觀或子系統時選擇合適拷貝方式。

- 避免濫用：簡單系統可直接操作子系統。

<br />

## 與其他模式的關係

- 與 Adapter：Facade 簡化子系統，Adapter 轉換介面。

- 與 Mediator：Facade 聚焦介面簡化，Mediator 協調物件交互。

- 與 Abstract Factory：Facade 可與抽象工廠結合創建子系統。

- 與 Singleton：Facade 常作為單例使用。

<br />

## 總結

Facade 模式透過統一介面簡化複雜子系統操作，適合多模組協作場景。

在前端中，此模式適用於 API 請求或 UI 渲染流程整合。

理解 Facade 有助於設計簡潔架構，提升程式碼可維護性。
