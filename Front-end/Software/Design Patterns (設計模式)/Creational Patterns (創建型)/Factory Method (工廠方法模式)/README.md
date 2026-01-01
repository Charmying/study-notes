# Factory Method (工廠方法模式)

Factory Method (工廠方法模式) 是一種創建型設計模式，定義了一個用於創建物件的介面，讓子類別決定要實例化哪個類別，使得一個類別的實例化延遲到其子類別，提供了更大的靈活性。

這種模式特別適合用於當系統需要支援多種產品類型時，而不希望創建程式碼直接依賴於具體產品類別。

<br />

## 動機

在軟體開發中，常會遇到需要創建不同類型物件的場景，例如

- 產品多樣性：一個應用程式可能需要支援多種文件格式 (例如：PDF、Word)，但不希望在客戶端程式碼中寫死具體類型。

- 框架擴展：框架提供抽象類別，讓使用者透過子類別定義具體實現。

- 測試與模擬：在單元測試中，使用 Factory Method 可以輕鬆替換真實物件為模擬物件。

若直接在客戶端使用 `new` 創建具體物件，會導致程式碼高耦合，難以擴展或替換。

Factory Method 透過將創建過程移到子類別，解決這些問題。

<br />

## 結構

Factory Method 模式的結構包含以下元素

- 產品介面 (Product Interface)：定義產品物件的介面。

- 具體產品 (Concrete Product)：實作產品介面的具體類別。

- 創建者類別 (Creator Class)：宣告 Factory Method，返回產品介面類型。通常也提供預設實現。

- 具體創建者 (Concrete Creator)：覆寫 Factory Method，返回具體產品實例。

以下是 Factory Method 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/ZL112i903Bmlv0-XfnPf7r142fv5lx1k8nRQZMJJWwX_TzNkmNgensHcCfDfWbhHSUZ1T5v9JjOH7eJRqIdUm22ka2yaLZlsUG7c0GQCwsq8k6NlX9GMwVOOL6naJ3eXgoo97otZTDsHdhdD2woJ_mSEFD1-8S7_5z_Y57XzBylv5s3IiIzqMaPqPbbLcvyYQipS2wQGWMd8jx7V9m00" width="100%" />

<br />

## 實現方式

- 基本實現

    定義產品介面和創建者，用於文件閱讀器系統。

	```java
	/** 產品介面 */
	public interface Document {
	    void open();
	}

	/** 具體產品：PDF 文件 */
	public class PdfDocument implements Document {
	    @Override
	    public void open() {
	        System.out.println("Opening PDF document.");
	    }
	}

	/** 具體產品：Word 文件 */
	public class WordDocument implements Document {
	    @Override
	    public void open() {
	        System.out.println("Opening Word document.");
	    }
	}

	/** 創建者抽象類別 */
	public abstract class DocumentCreator {
	    /** Factory Method */
	    public abstract Document createDocument();

	    /** 使用 Factory Method 的操作 */
	    public void openDocument() {
	        Document doc = createDocument();
	        doc.open();
	    }
	}

	/** 具體創建者：PDF 創建者 */
	public class PdfCreator extends DocumentCreator {
	    @Override
	    public Document createDocument() {
	        return new PdfDocument();
	    }
	}

	/** 具體創建者：Word 創建者 */
	public class WordCreator extends DocumentCreator {
	    @Override
	    public Document createDocument() {
	        return new WordDocument();
	    }
	}



	/** 使用範例 */
	public class Client {
	    public static void main(String[] args) {
	        DocumentCreator creator = new PdfCreator();
	        creator.openDocument(); // Output: Opening PDF document.

	        creator = new WordCreator();
	        creator.openDocument(); // Output: Opening Word document.
	    }
	}
	```

    特點：客戶端不需知道具體產品類別，只需依賴抽象創建者。

- JavaScript 實現 Factory Method

    用於創建不同類型的 UI 元件 (例如：按鈕)。

	```javascript
	/** 產品介面 */
	class Button {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	/** 具體產品：主要按鈕 */
	class PrimaryButton extends Button {
	  render() {
	    return `<button class="btn btn-primary">主要按鈕</button>`;
	  }
	}

	/** 具體產品：次要按鈕 */
	class SecondaryButton extends Button {
	  render() {
	    return `<button class="btn btn-secondary">次要按鈕</button>`;
	  }
	}

	/** 創建者抽象類別 */
	class ButtonCreator {
	  createButton() {
	    throw new Error("Method 'createButton()' must be implemented.");
	  }

	  renderButton() {
	    const button = this.createButton();
	    return button.render();
	  }
	}

	/** 具體創建者：主要按鈕創建者 */
	class PrimaryButtonCreator extends ButtonCreator {
	  createButton() {
	    return new PrimaryButton();
	  }
	}

	/** 具體創建者：次要按鈕創建者 */
	class SecondaryButtonCreator extends ButtonCreator {
	  createButton() {
	    return new SecondaryButton();
	  }
	}



	/** 使用範例 */
	const primaryCreator = new PrimaryButtonCreator();
	console.log(primaryCreator.renderButton()); // <button class="btn btn-primary">主要按鈕</button>

	const secondaryCreator = new SecondaryButtonCreator();
	console.log(secondaryCreator.renderButton()); // <button class="btn btn-secondary">次要按鈕</button>
    ```

    特點：適用於前端動態創建 UI 元件，客戶端程式碼不需直接依賴具體按鈕類型。

- TypeScript 實現 Factory Method

    用於管理不同類型的 API 客戶端。

	```javascript
	/** 產品介面 */
	interface ApiClient {
	  fetchData(endpoint: string): Promise<any>;
	}

	/** 具體產品：公開 API 客戶端 */
	class PublicApiClient implements ApiClient {
	  async fetchData(endpoint: string) {
	    return fetch(`https://public-api.example.com/${endpoint}`).then(res => res.json());
	  }
	}

	/** 具體產品：認證 API 客戶端 */
	class AuthenticatedApiClient implements ApiClient {
	  private token: string = 'Bearer token123';

	  async fetchData(endpoint: string) {
	    return fetch(`https://api.example.com/${endpoint}`, {
	      headers: { Authorization: this.token }
	    }).then(res => res.json());
	  }
	}

	/** 創建者抽象類別 */
	abstract class ApiClientCreator {
	  abstract createApiClient(): ApiClient;

	  async getData(endpoint: string) {
	    const client = this.createApiClient();
	    return client.fetchData(endpoint);
	  }
	}

	/** 具體創建者：公開 API 創建者 */
	class PublicApiClientCreator extends ApiClientCreator {
	  createApiClient(): ApiClient {
	    return new PublicApiClient();
	  }
	}

	/** 具體創建者：認證 API 創建者 */
	class AuthenticatedApiClientCreator extends ApiClientCreator {
	  createApiClient(): ApiClient {
	    return new AuthenticatedApiClient();
	  }
	}



	/** 使用範例 */
	const publicCreator = new PublicApiClientCreator();
	publicCreator.getData('users').then(data => console.log(data));

	const authCreator = new AuthenticatedApiClientCreator();
	authCreator.getData('users').then(data => console.log(data));
	```

    特點：TypeScript 的型別系統確保 API 客戶端的類型安全，適合前端需要與不同後端交互的場景。

- Angular 實現 Factory Method

    使用 Angular 服務和依賴注入實現 Factory Method，創建不同類型的通知服務。

	```javascript
	/** notification.service.ts */
	import { Injectable } from '@angular/core';

	export interface Notification {
	  show(message: string): void;
	}

	@Injectable()
	export class ToastNotification implements Notification {
	  show(message: string) {
	    console.log(`Toast: ${message}`);
	  }
	}

	@Injectable()
	export class AlertNotification implements Notification {
	  show(message: string) {
	    console.log(`Alert: ${message}`);
	  }
	}

	@Injectable()
	export abstract class NotificationCreator {
	  abstract createNotification(): Notification;

	  displayNotification(message: string) {
	    const notification = this.createNotification();
	    notification.show(message);
	  }
	}

	@Injectable()
	export class ToastNotificationCreator extends NotificationCreator {
	  createNotification(): Notification {
	    return new ToastNotification();
	  }
	}

	@Injectable()
	export class AlertNotificationCreator extends NotificationCreator {
	  createNotification(): Notification {
	    return new AlertNotification();
	  }
	}



	/** app.module.ts */
	import { NgModule } from '@angular/core';
	import { BrowserModule } from '@angular/platform-browser';
	import { AppComponent } from './app.component';
	import { ToastNotificationCreator, AlertNotificationCreator } from './notification.service';

	@NgModule({
	  declarations: [AppComponent],
	  imports: [BrowserModule],
	  providers: [ToastNotificationCreator, AlertNotificationCreator],
	  bootstrap: [AppComponent]
	})
	export class AppModule { }



	/** app.component.ts */
	import { Component } from '@angular/core';
	import { ToastNotificationCreator, AlertNotificationCreator } from './notification.service';

	@Component({
	  selector: 'app-root',
	  template: `
	    <button (click)="showToast()">顯示 Toast</button>
	    <button (click)="showAlert()">顯示 Alert</button>
	  `
	})
	export class AppComponent {
	  constructor(
	    private toastCreator: ToastNotificationCreator,
	    private alertCreator: AlertNotificationCreator
	  ) {}

	  showToast() {
	    this.toastCreator.displayNotification('操作成功');
	  }

	  showAlert() {
	    this.alertCreator.displayNotification('操作成功');
	  }
	}
	```

    特點：Angular 的依賴注入系統簡化了創建者的管理，適合動態選擇通知類型。

- React 實現 Factory Method

    使用 React 元件和 Context 實現 Factory Method，創建不同類型的表單輸入元件。

    ```javascript
    /** Input.js */
	class Input {
	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

	class TextInput extends Input {
	  render() {
	    return <input type="text" placeholder="輸入文字" />;
	  }
	}

	class NumberInput extends Input {
	  render() {
	    return <input type="number" placeholder="輸入數字" />;
	  }
	}

	class InputCreator {
	  createInput() {
	    throw new Error("Method 'createInput()' must be implemented.");
	  }

	  renderInput() {
	    const input = this.createInput();
	    return input.render();
	  }
	}

	class TextInputCreator extends InputCreator {
	  createInput() {
	    return new TextInput();
	  }
	}

	class NumberInputCreator extends InputCreator {
	  createInput() {
	    return new NumberInput();
	  }
	}



    /** InputContext.js */
    import { createContext, useContext } from 'react';

    const InputContext = createContext(null);

    export const useInputCreator = () => useContext(InputContext);



	/** App.jsx */
	import React from 'react';
	import { InputContext, useInputCreator } from './InputContext';

	const App = () => {
	  const textCreator = new TextInputCreator();
	  const numberCreator = new NumberInputCreator();

	  return (
	    <div>
	      <InputContext.Provider value={textCreator}>
	        <TextInputComponent />
	      </InputContext.Provider>
	      <InputContext.Provider value={numberCreator}>
	        <NumberInputComponent />
	      </InputContext.Provider>
	    </div>
	  );
	};

	const TextInputComponent = () => {
	  const creator = useInputCreator();
	  return <div>{creator.renderInput()}</div>;
	};

	const NumberInputComponent = () => {
	  const creator = useInputCreator();
	  return <div>{creator.renderInput()}</div>;
	};

	export default App;
	```

    特點：結合 React Context，Factory Method 可用於動態渲染不同類型的 UI 元件。

<br />

## 應用場景

Factory Method 模式適用於以下場景

- 當類別無法預知要創建的物件類型

    例如：框架中，讓使用者定義具體實現。

- 當系統需要支援多種產品家族：結合抽象工廠模式。

- 解耦客戶端與具體類別：提升可擴展性

    例如：在遊戲中創建不同類型的敵人。

- 單元測試：輕鬆替換為模擬物件。

例如

- Java 的 java.util.Calendar 使用 Factory Method 來獲取實例，允許不同時區的子類別。

- 在前端，Factory Method 可用於動態創建 UI 元件或 API 客戶端。

<br />

## 優缺點

### 優點

- 符合開閉原則：新增產品時，只需新增具體創建者和產品，不修改既有程式碼。

- 解耦：客戶端只依賴抽象介面，降低耦合度。

- 靈活性：子類別可自訂創建方式。

- 易於擴展：支援平行類別層級 (Parallel Class Hierarchies)。

### 缺點

- 程式碼複雜度增加：為每個產品都需要具體創建者，可能導致類別數量增加。

- 抽象層級：引入額外抽象類別，可能過度設計。

- 初始化問題：若產品建構需要參數，Factory Method 需處理這些參數。

<br />

## 注意事項

- 預設實現：創建者可提供預設 Factory Method 實現，避免抽象類別無法實例化。

- 參數傳遞：若產品建構需要參數，可在 Factory Method 中傳遞。

- 與模板方法結合：Factory Method 常作為模板方法模式中的一步。

- 避免濫用：若產品類型固定且少，可考慮簡單工廠而非 Factory Method。

<br />

## 與其他模式的關係

- 與抽象工廠 (Abstract Factory)：Factory Method 聚焦單一產品，抽象工廠處理產品家族。

- 與模板方法 (Template Method)：Factory Method 可作為模板方法中的鉤子 (Hook)。

- 與原型模式 (Prototype)：可結合使用，透過複製原型創建物件。

- 與單例模式 (Singleton)：Factory Method 可返回單例實例。

<br />

## 總結

Factory Method 模式是一種經典的創建型設計模式，透過將物件創建延遲到子類別，提供了高度的靈活性和解耦能力，特別適合用於框架設計和需要擴展的系統中。雖然可能增加一些複雜度，但正確應用能大幅提升程式碼的可維護性和可擴展性。

在前端開發中，Factory Method 適用於動態創建 UI 元件或 API 客戶端。

對於物件導向設計的開發人員來說，理解 Factory Method 有助於處理複雜的創建過程，並與其他模式搭配使用，打造更強健的軟體架構。
