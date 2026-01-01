# Adapter (適配器模式)

Adapter (適配器模式) 是一種結構型設計模式，將不相容介面轉換為客戶端期望的介面，使原本無法直接協作的類別得以協同工作。此

這種類似於現實中的電源適配器，橋接不同系統或元件。

<br />

## 動機

軟體開發中，常遇到介面不匹配問題，例如

- 整合舊系統與新系統，介面定義不同。

- 使用第三方庫，但其方法與現有程式碼不符。

- 前端需將不同格式的 API 資料轉換為統一結構。

直接修改既有類別可能違反開閉原則或不可行。

Adapter 模式透過中間層轉換介面，解決相容性問題。

<br />

## 結構

Adapter 模式的結構包含以下元素

目標介面 (Target Interface)：客戶端期望使用的介面。

適配者 (Adaptee)：需要適配的現有類別，擁有不兼容介面。

適配器 (Adapter)：實作目標介面，封裝適配者並轉換其方法。

客戶端 (Client)：使用目標介面與適配器交互。

以下是 Adapter 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuFdlTinKpd-pkVZbt4KY0boiphoIrA2qnELKX9B4eFRL4ePgNIq51Mw4ejR0qjRX4GvENgvQN2wR_PUFAbwszJsUkW6XEpaaiBbPmJ4ai01e2qQcha0ZcfYfOGILIyHduOj5gY9al6benpKo5kQQu83KvCoqpEGYxgwRFURA_2Q8TwWkR6ZqzcCDukM0krDMrWvjifQ1KMfnQhCJBvP2Qbm8C8m00" width="100%" />

<br />

## 實現方式

- 物件適配器實現

    假設將舊版日誌系統適配到新版介面。

    ```java
    /** 目標介面 */
    public interface Logger {
        void log(String message);
    }

    /** 適配者：舊版日誌系統 */
    public class OldLogger {
        public void writeLog(String text) {
            System.out.println("Old Logger: " + text);
        }
    }

    /** 適配器 */
    public class LoggerAdapter implements Logger {
        private OldLogger oldLogger;

        public LoggerAdapter(OldLogger oldLogger) {
            this.oldLogger = oldLogger;
        }

        @Override
        public void log(String message) {
            oldLogger.writeLog(message);
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            OldLogger oldLogger = new OldLogger();
            Logger logger = new LoggerAdapter(oldLogger);
            logger.log("Test message"); // Old Logger: Test message
        }
    }
    ```

    特點：物件適配器透過組合方式實現，靈活且符合開閉原則。

- 類別適配器實現

    使用繼承實現適配器。

    ```java
    /** 目標介面 */
    public interface Logger {
        void log(String message);
    }

    /** 適配者：舊版日誌系統 */
    public class OldLogger {
        public void writeLog(String text) {
            System.out.println("Old Logger: " + text);
        }
    }

    /** 適配器 */
    public class LoggerAdapter extends OldLogger implements Logger {
        @Override
        public void log(String message) {
            writeLog(message);
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Logger logger = new LoggerAdapter();
            logger.log("Test message"); // Old Logger: Test message
        }
    }
    ```

    特點：類別適配器透過繼承實現，適用於單一繼承語言，但靈活性較低。

- JavaScript 實現 Adapter

    將第三方 API 資料格式適配為統一結構。

    ```javascript
    /** 目標介面 (期望格式) */
  	class UserData {
  	  constructor(data) {
  	    this.name = data.name;
  	    this.email = data.email;
  	  }

  	  display() {
  	    return `${this.name} <${this.email}>`;
  	  }
  	}

  	/** 適配者：第三方 API 資料 */
  	class ThirdPartyApi {
  	  fetchUser() {
  	    return { username: "Charmy", emailAddress: "charmy@example.com" };
  	  }
  	}

  	/** 適配器 */
  	class UserDataAdapter {
  	  constructor(api) {
  	    this.api = api;
  	  }

  	  getUserData() {
  	    const rawData = this.api.fetchUser();
  	    return new UserData({
  	      name: rawData.username,
  	      email: rawData.emailAddress
  	    });
  	  }
  	}



  	/** 使用範例 */
  	const api = new ThirdPartyApi();
  	const adapter = new UserDataAdapter(api);
  	const userData = adapter.getUserData();
  	console.log(userData.display()); // Charmy <charmy@example.com>
    ```

    特點：適配器轉換 API 資料格式，統一客戶端使用方式。

- TypeScript 實現 Adapter

    將舊版元件介面適配為新版。

    ``` typescript
  	/** 目標介面 */
  	interface NewComponent {
  	  render(): string;
  	}

  	/** 適配者：舊版元件 */
  	class OldComponent {
  	  draw() {
  	    return "<div>Old Component</div>";
  	  }
  	}

  	/** 適配器 */
  	class ComponentAdapter implements NewComponent {
  	  private oldComponent: OldComponent;

  	  constructor(oldComponent: OldComponent) {
  	    this.oldComponent = oldComponent;
  	  }

  	  render(): string {
  	    return this.oldComponent.draw();
  	  }
  	}



  	/** 使用範例 */
  	const oldComponent = new OldComponent();
  	const adapter = new ComponentAdapter(oldComponent);
  	console.log(adapter.render()); // <div>Old Component</div>
    ```

    特點：TypeScript 確保型別安全，適合整合舊版元件。

- Angular 實現 Adapter

    將第三方圖表庫適配為統一介面。

    ```typescript
	/** chart.service.ts */
	import { Injectable } from '@angular/core';

  	export interface Chart {
  	  renderChart(data: number[]): string;
  	}

  	/** 適配者：第三方圖表庫 */
  	export class ThirdPartyChart {
  	  drawGraph(values: number[]) {
  	    return `<svg>${values.join(',')}</svg>`;
  	  }
  	}

  	@Injectable()
  	export class ChartAdapter implements Chart {
  	  private thirdPartyChart: ThirdPartyChart;

  	  constructor() {
  	    this.thirdPartyChart = new ThirdPartyChart();
  	  }

  	  renderChart(data: number[]): string {
  	    return this.thirdPartyChart.drawGraph(data);
  	  }
  	}



  	/** app.module.ts */
  	import { NgModule } from '@angular/core';
  	import { BrowserModule } from '@angular/platform-browser';
  	import { AppComponent } from './app.component';
  	import { ChartAdapter } from './chart.service';

  	@NgModule({
  	  declarations: [AppComponent],
  	  imports: [BrowserModule],
  	  providers: [ChartAdapter],
  	  bootstrap: [AppComponent]
  	})
  	export class AppModule { }



  	/** app.component.ts */
  	import { Component } from '@angular/core';
  	import { ChartAdapter } from './chart.service';

  	@Component({
  	  selector: 'app-root',
  	  template: `<button (click)="renderChart()">渲染圖表</button>`
  	})
  	export class AppComponent {
  	  constructor(private chart: ChartAdapter) {}

  	  renderChart() {
  	    const data = [1, 2, 3];
  	    console.log(this.chart.renderChart(data)); // <svg>1,2,3</svg>
  	  }
  	}
    ```

    特點：Angular 服務封裝適配器，整合第三方庫。

- React 實現 Adapter

    將舊版按鈕適配為新版介面。

    ``` javascript
  	/** ButtonAdapter.js */
  	class OldButton {
  	  drawButton() {
  	    return <button style={{ background: 'gray' }}>舊按鈕</button>;
  	  }
  	}

  	class ButtonAdapter {
  	  constructor(oldButton) {
  	    this.oldButton = oldButton;
  	  }

  	  render() {
  	    return this.oldButton.drawButton();
  	  }
  	}



  	/** App.jsx */
  	import React from 'react';

  	const App = () => {
  	  const oldButton = new OldButton();
  	  const adapter = new ButtonAdapter(oldButton);

  	  return (
  	    <div>
  	      {adapter.render()}
  	    </div>
  	  );
  	};

    export default App;
    ```

    特點：適配器整合舊版 UI 元件至 React 應用。

<br />

## 應用場景

Adapter 模式適用於以下場景

- 整合舊系統或第三方庫。

- 統一不同 API 資料格式。

- 前端中轉換元件介面或資料結構。

例如：Java 的 java.util.Arrays.asList 將陣列適配為 List 介面。

<br />

## 優缺點

### 優點

- 相容性：使不相容介面協同工作。

- 符合開閉原則：無需修改既有類別。

- 靈活性：支援多種適配方式。

- 重用性：舊系統可重用於新環境。

### 缺點

- 程式碼複雜度：增加額外適配器類別。

- 效能開銷：轉換過程可能增加開銷。

- 維護成本：多個適配器可能難以管理。

<br />

## 注意事項

- 物件 vs 類別適配：物件適配透過組合更靈活，類別適配透過繼承更簡單。

- 雙向適配：可設計雙向適配器支援雙向轉換。

- 介面一致性：確保目標介面清晰。

- 避免濫用：簡單轉換可直接處理。

<br />

## 與其他模式的關係

- 與 Bridge：Adapter 轉換現有介面，Bridge 分離介面與實現。

- 與 Decorator：Adapter 改變介面，Decorator 增強功能。

- 與 Facade：Adapter 聚焦介面轉換，Facade 簡化子系統。

- 與 Proxy：Adapter 提供不同介面，Proxy 提供相同介面。

<br />

## 總結

Adapter 模式透過轉換介面解決相容性問題，適合整合不同系統或庫。

在前端中，此模式適用於 API 資料格式統一或舊元件整合。

理解 Adapter 有助於設計靈活架構，提升程式碼重用性與可維護性。
