# Abstract Factory (抽象工廠模式)

Abstract Factory (抽象工廠模式) 是一種創建型設計模式，提供一個介面用於創建一系列相關或相互依賴的物件，而無需指定具體類別。

這種模式允許系統獨立於產品創建、組合和表示，提升靈活性。

<br />

## 動機

軟體系統中常需處理相關產品家族，例如

- 支援多種作業系統的 GUI 框架，需要創建按鈕、視窗等元件，但元件樣式依作業系統而異。

- 遊戲中不同主題的資源

    例如：森林或沙漠主題的樹木、建築。

- 資料庫連接工廠，根據不同資料庫類型創建連接、命令物件。

直接指定具體類別會導致程式碼依賴特定實現，難以切換產品家族。

Abstract Factory 透過抽象介面隔離創建過程，解決此問題。

<br />

## 結構

Abstract Factory 模式的結構包含以下元素

- 抽象工廠 (Abstract Factory)：定義創建產品的介面。

- 具體工廠 (Concrete Factory)：實作抽象工廠，創建具體產品家族。

- 抽象產品 (Abstract Product)：定義產品類型的介面。

- 具體產品 (Concrete Product)：實作抽象產品的具體類別。

以下是 Abstract Factory 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLukdtfqzqBG4nUhioyajIYjCJaL0N7fEAIeiJa4ZSWpY-gLAZcvL9Gq5P8BafDB4aDACfFAKqkSTJGLB22guG9Ob7eX4sX4ozNBIyNBrToJc9niO9pVXvGIqagr3v3F1R2E8OuRO9n3A5MG3pwh6llYuqBdqzPz7HoeuAZWfg24ovFmso0EIA_8BKeiIGpFm_e0B2H43V37O9J7Hx3dJ0qEM4pt0dJS2UuuH1_lPm-vyd-9eXVqADDmQP6JmyZS17gu3wrgT7LHGvP3DSYAm05B2yNHfJfwTaXXOcLWX8aQegLyAjrGbFha9gN0aoV0000" width="100%" />

<br />

## 實現方式

- 基本實現

    假設設計一個 GUI 工廠，支援 Windows 和 macOS 風格的按鈕和視窗。

    ```java
	/** 抽象產品：按鈕 */
	public interface Button {
	  void paint();
	}

	/** 具體產品：Windows 按鈕 */
	public class WindowsButton implements Button {
	  @Override
	  public void paint() {
	    System.out.println("Rendering Windows button.");
	  }
	}

	/** 具體產品：macOS 按鈕 */
	public class MacButton implements Button {
	  @Override
	  public void paint() {
	    System.out.println("Rendering macOS button.");
	  }
	}

	/** 抽象產品：視窗 */
	public interface Window {
	  void draw();
	}

	/** 具體產品：Windows 視窗 */
	public class WindowsWindow implements Window {
	  @Override
	  public void draw() {
	    System.out.println("Drawing Windows window.");
	  }
	}

	/** 具體產品：macOS 視窗 */
	public class MacWindow implements Window {
	  @Override
	  public void draw() {
	    System.out.println("Drawing macOS window.");
	  }
	}

	/** 抽象工廠 */
	public interface GUIFactory {
	  Button createButton();
	  Window createWindow();
	}

	/** 具體工廠：Windows 工廠 */
	public class WindowsFactory implements GUIFactory {
	  @Override
	  public Button createButton() {
	    return new WindowsButton();
	  }

	  @Override
	  public Window createWindow() {
	    return new WindowsWindow();
	  }
	}

	/** 具體工廠：macOS 工廠 */
	public class MacFactory implements GUIFactory {
	  @Override
	  public Button createButton() {
	    return new MacButton();
	  }

	  @Override
	  public Window createWindow() {
	    return new MacWindow();
	  }
	}



	/** 使用範例 */
	public class Client {
	  public static void main(String[] args) {
	    GUIFactory factory = new WindowsFactory();
	    Button button = factory.createButton();
	    Window window = factory.createWindow();
	    button.paint(); // Rendering Windows button.
	    window.draw();  // Drawing Windows window.

	    factory = new MacFactory();
	    button = factory.createButton();
	    window = factory.createWindow();
	    button.paint(); // Rendering macOS button.
	    window.draw();  // Drawing macOS window.
	  }
	}
	```

    特點：客戶端程式碼僅依賴抽象工廠，易於切換產品家族。

- JavaScript 實現 Abstract Factory

    用於創建不同主題的 UI 元件家族 (例如：淺色和深色主題的按鈕和輸入框)。

    ```javascript
	/** 抽象產品：按鈕 */
	class Button {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	/** 具體產品：淺色按鈕 */
	class LightButton extends Button {
	  render() {
	    return `<button style="background: white; color: black;">淺色按鈕</button>`;
	  }
	}

	/** 具體產品：深色按鈕 */
	class DarkButton extends Button {
	  render() {
	    return `<button style="background: black; color: white;">深色按鈕</button>`;
	  }
	}

	/** 抽象產品：輸入框 */
	class Input {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	/** 具體產品：淺色輸入框 */
	class LightInput extends Input {
	  render() {
	    return `<input style="background: white; color: black;" placeholder="淺色輸入" />`;
	  }
	}

	/** 具體產品：深色輸入框 */
	class DarkInput extends Input {
	  render() {
	    return `<input style="background: black; color: white;" placeholder="深色輸入" />`;
	  }
	}

	/** 抽象工廠 */
	class UIFactory {
	  createButton() {
	    throw new Error("Method 'createButton()' must be implemented.");
	  }

	  createInput() {
	    throw new Error("Method 'createInput()' must be implemented.");
	  }
	}

	/** 具體工廠：淺色工廠 */
	class LightUIFactory extends UIFactory {
	  createButton() {
	    return new LightButton();
	  }

	  createInput() {
	    return new LightInput();
	  }
	}

	/** 具體工廠：深色工廠 */
	class DarkUIFactory extends UIFactory {
	  createButton() {
	    return new DarkButton();
	  }

	  createInput() {
	    return new DarkInput();
	  }
	}



	/** 使用範例 */
	const lightFactory = new LightUIFactory();
	console.log(lightFactory.createButton().render()); // <button style="background: white; color: black;">淺色按鈕</button>
	console.log(lightFactory.createInput().render());  // <input style="background: white; color: black;" placeholder="淺色輸入" />

	const darkFactory = new DarkUIFactory();
	console.log(darkFactory.createButton().render()); // <button style="background: black; color: white;">深色按鈕</button>
	console.log(darkFactory.createInput().render());  // <input style="background: black; color: white;" placeholder="深色輸入" />
	```

    特點：適用於前端主題切換，確保元件家族一致。

- TypeScript 實現 Abstract Factory

    用於創建不同環境的 API 客戶端家族 (例如：開發和生產環境的請求和錯誤處理物件)。

	```typescript
	/** 抽象產品：請求客戶端 */
	interface RequestClient {
	  sendRequest(url: string): Promise<any>;
	}

	/** 具體產品：開發請求客戶端 */
	class DevRequestClient implements RequestClient {
	  async sendRequest(url: string) {
	    console.log("Sending dev request to " + url);
	    return { data: "dev data" };
	  }
	}

	/** 具體產品：生產請求客戶端 */
	class ProdRequestClient implements RequestClient {
	  async sendRequest(url: string) {
	    console.log("Sending prod request to " + url);
	    return { data: "prod data" };
	  }
	}

	/** 抽象產品：錯誤處理器 */
	interface ErrorHandler {
	  handleError(error: Error): void;
	}

	/** 具體產品：開發錯誤處理器 */
	class DevErrorHandler implements ErrorHandler {
	  handleError(error: Error) {
	    console.log("Dev error: " + error.message);
	  }
	}

	/** 具體產品：生產錯誤處理器 */
	class ProdErrorHandler implements ErrorHandler {
	  handleError(error: Error) {
	    console.log("Prod error: " + error.message);
	  }
	}

	/** 抽象工廠 */
	interface ApiFactory {
	  createRequestClient(): RequestClient;
	  createErrorHandler(): ErrorHandler;
	}

	/** 具體工廠：開發工廠 */
	class DevApiFactory implements ApiFactory {
	  createRequestClient(): RequestClient {
	    return new DevRequestClient();
	  }

	  createErrorHandler(): ErrorHandler {
	    return new DevErrorHandler();
	  }
	}

	/** 具體工廠：生產工廠 */
	class ProdApiFactory implements ApiFactory {
	  createRequestClient(): RequestClient {
	    return new ProdRequestClient();
	  }

	  createErrorHandler(): ErrorHandler {
	    return new ProdErrorHandler();
	  }
	}



	/** 使用範例 */
	const devFactory = new DevApiFactory();
	const devClient = devFactory.createRequestClient();
	devClient.sendRequest("/api"); // Sending dev request to /api
	const devHandler = devFactory.createErrorHandler();
	devHandler.handleError(new Error("test")); // Dev error: test

	const prodFactory = new ProdApiFactory();
	const prodClient = prodFactory.createRequestClient();
	prodClient.sendRequest("/api"); // Sending prod request to /api
	const prodHandler = prodFactory.createErrorHandler();
	prodHandler.handleError(new Error("test")); // Prod error: test
	```

    特點：TypeScript 的型別系統確保客戶端家族的類型安全，適合環境切換。

- Angular 實現 Abstract Factory

    使用 Angular 服務和依賴注入實現 Abstract Factory，創建不同風格的通知和載入指示器家族。

	```typescript
	// ui-elements.service.ts
	import { Injectable } from '@angular/core';

	export interface Notification {
	  show(message: string): void;
	}

	export interface Loader {
	  showLoading(): void;
	}

	@Injectable()
	export abstract class UIFactory {
	  abstract createNotification(): Notification;
	  abstract createLoader(): Loader;
	}

	@Injectable()
	export class ModernNotification implements Notification {
	  show(message: string) {
	    console.log(`Modern notification: ${message}`);
	  }
	}

	@Injectable()
	export class ModernLoader implements Loader {
	  showLoading() {
	    console.log("Showing modern loader");
	  }
	}

	@Injectable()
	export class ClassicNotification implements Notification {
	  show(message: string) {
	    console.log(`Classic notification: ${message}`);
	  }
	}

	@Injectable()
	export class ClassicLoader implements Loader {
	  showLoading() {
	    console.log("Showing classic loader");
	  }
	}

	@Injectable()
	export class ModernUIFactory extends UIFactory {
	  createNotification(): Notification {
	    return new ModernNotification();
	  }

	  createLoader(): Loader {
	    return new ModernLoader();
	  }
	}

	@Injectable()
	export class ClassicUIFactory extends UIFactory {
	  createNotification(): Notification {
	    return new ClassicNotification();
	  }

	  createLoader(): Loader {
	    return new ClassicLoader();
	  }
	}



	/** app.module.ts */
	import { NgModule } from '@angular/core';
	import { BrowserModule } from '@angular/platform-browser';
	import { AppComponent } from './app.component';
	import { ModernUIFactory, ClassicUIFactory } from './ui-elements.service';

	@NgModule({
	  declarations: [AppComponent],
	  imports: [BrowserModule],
	  providers: [ModernUIFactory, ClassicUIFactory],
	  bootstrap: [AppComponent]
	})
	export class AppModule { }



	/** app.component.ts */
	import { Component } from '@angular/core';
	import { ModernUIFactory, ClassicUIFactory } from './ui-elements.service';

	@Component({
	  selector: 'app-root',
	  template: `
	    <button (click)="useModern()">使用現代 UI</button>
	    <button (click)="useClassic()">使用經典 UI</button>
	  `
	})
	export class AppComponent {
	  constructor(
	    private modernFactory: ModernUIFactory,
	    private classicFactory: ClassicUIFactory
	  ) {}

	  useModern() {
	    const notification = this.modernFactory.createNotification();
	    notification.show('現代訊息');
	    const loader = this.modernFactory.createLoader();
	    loader.showLoading();
	  }

	  useClassic() {
	    const notification = this.classicFactory.createNotification();
	    notification.show('經典訊息');
	    const loader = this.classicFactory.createLoader();
	    loader.showLoading();
	  }
	}
	```

    特點：Angular 的依賴注入系統支援工廠注入，適合 UI 風格切換。

- React 實現 Abstract Factory

    使用 React 元件實現 Abstract Factory，創建不同主題的表單元件家族。

	```javascript
	/** FormElements.js */
	class Button {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	class Input {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	class LightButton extends Button {
	  render() {
	    return <button style={{ background: 'white', color: 'black' }}>淺色按鈕</button>;
	  }
	}

	class LightInput extends Input {
	  render() {
	    return <input style={{ background: 'white', color: 'black' }} placeholder="淺色輸入" />;
	  }
	}

	class DarkButton extends Button {
	  render() {
	    return <button style={{ background: 'black', color: 'white' }}>深色按鈕</button>;
	  }
	}

	class DarkInput extends Input {
	  render() {
	    return <input style={{ background: 'black', color: 'white' }} placeholder="深色輸入" />;
	  }
	}

	class FormFactory {
	  createButton() {
	    throw new Error("Method 'createButton()' must be implemented.");
	  }

	  createInput() {
	    throw new Error("Method 'createInput()' must be implemented.");
	  }
	}

	class LightFormFactory extends FormFactory {
	  createButton() {
	    return new LightButton();
	  }

	  createInput() {
	    return new LightInput();
	  }
	}

	class DarkFormFactory extends FormFactory {
	  createButton() {
	    return new DarkButton();
	  }

	  createInput() {
	    return new DarkInput();
	  }
	}



    /** FormContext.js */
    import { createContext, useContext } from 'react';

    const FormContext = createContext(null);

    export const useFormFactory = () => useContext(FormContext);



	// App.jsx
	import React from 'react';
	import { FormContext, useFormFactory } from './FormContext';

	const App = () => {
	  const lightFactory = new LightFormFactory();
	  const darkFactory = new DarkFormFactory();

	  return (
	    <div>
	      <FormContext.Provider value={lightFactory}>
	        <LightForm />
	      </FormContext.Provider>
	      <FormContext.Provider value={darkFactory}>
	        <DarkForm />
	      </FormContext.Provider>
	    </div>
	  );
	};

	const LightForm = () => {
	  const factory = useFormFactory();
	  return (
	    <div>
	      {factory.createInput().render()}
	      {factory.createButton().render()}
	    </div>
	  );
	};

	const DarkForm = () => {
	  const factory = useFormFactory();
	  return (
	    <div>
	      {factory.createInput().render()}
	      {factory.createButton().render()}
	    </div>
	  );
	};

	export default App;
	```

    特點：結合 React Context，此模式支援主題化表單元件。

<br />

## 應用場景

Abstract Factory 模式適用於以下場景

- 需要創建相關產品家族時，例如： GUI 元件或資料庫物件。

- 系統需獨立於產品創建時，例如：支援多平台。

- 強調產品家族一致性時，例如：遊戲資源主題。

- 前端中切換 UI 主題或 API 環境時。

例如：Java 的 `javax.swing` 使用類似概念支援不同 Look-and-feel。

<br />

## 優缺點

### 優點

- 產品一致性：確保相關產品相容。

- 符合開閉原則：新增產品家族無需修改既有程式碼。

- 解耦：客戶端僅依賴抽象介面。

- 易於切換：簡易更換產品家族。

### 缺點

程式碼複雜度增加：引入多層抽象，可能導致類別數量增加。

難以新增產品：新增產品需修改抽象工廠介面，影響所有具體工廠。

過度設計風險：若產品家族少，可能不必要。

<br />

## 注意事項

- 產品家族定義：確保抽象工廠涵蓋所有相關產品。

- 參數化：可透過參數控制具體工廠選擇。

- 與單例結合：工廠可作為單例使用。

避免濫用：若僅需單一產品，使用 Factory Method 較合適。

九、與其他模式的關係

- 與 Factory Method：Abstract Factory 常使用 Factory Method 實作產品創建。

- 與 Builder：Abstract Factory 聚焦家族，Builder 聚焦複雜物件建構。

- 與 Prototype：可結合原型複製創建產品。

- 與 Singleton：工廠實例可為單例。

## 總結

Abstract Factory 模式提供有效方式創建相關物件家族，維持系統靈活性與一致性。

此模式適合複雜系統需切換產品組態的場合。

在前端開發中，此模式適用於 UI 主題或 API 環境管理。理解 Abstract Factory 有助於設計可擴展架構，搭配其他模式提升軟體品質。
