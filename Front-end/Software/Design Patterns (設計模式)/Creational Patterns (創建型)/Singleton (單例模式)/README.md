# Singleton (單例模式)

Singleton (單例模式) 是一種創建型設計模式，確保某個類別在應用程式執行期間只有一個實例 (Instance)，並提供一個全域存取點，讓系統中的任何部分都能存取這個唯一實例。

這種模式特別適合用於管理共享資源，例如：資料庫連線、執行緒池、全域設定管理器或日誌系統。

<br />

## 動機

在軟體系統中，有些物件只需要一個實例，例如

- 全域設定：應用程式的配置檔案只需要一個實例來管理全域設定。

- 資源管理：像是資料庫連線池或檔案系統存取，多次創建實例可能導致資源浪費或競爭條件。

- 日誌系統：日誌記錄器需要統一管理，以確保日誌的順序性和一致性。

若不加以控制，多次創建這些物件的實例可能導致系統資源浪費、效能下降或資料不一致。

Singleton 模式通過限制實例的創建，解決這些問題。

<br />

## 結構

Singleton 模式的結構相對簡單，主要包含以下元素

- 單例類別 (Singleton Class)：定義一個類別，該類別負責創建並管理自己的唯一實例。

- 私有建構函數：防止外部程式碼直接通過 `new` 關鍵字創建實例。

- 靜態實例變數：儲存該類別的唯一實例，通常為靜態變數。

- 公開的靜態存取方法：提供全域存取點，通常是一個靜態方法 (例如：`getInstance()`)，用於返回唯一實例。

以下是 Singleton 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULApaaiBbO8pinBpqajoSzJgERbKb3GLSZC0oh9IqwrGaX19E1S3KsGWBP2Ucg99rInXYQAybfUBeVKl1IWDG00" width="100%" />

<br />

## 實現方式

- 延遲初始化 (Lazy Initialization)

    這種方式在第一次呼叫 `getInstance()` 時才創建實例，適合單執行緒環境。

	```java
	public class Singleton {
	    private static Singleton instance;

	    /** 私有建構函數，防止外部實例化 */
	    private Singleton() {}

	    /** 提供全域存取點 */
	    public static Singleton getInstance() {
	        if (instance == null) {
	            instance = new Singleton();
	        }
	        return instance;
	    }
	}
	```

    缺點：在多執行緒環境中，存在競爭條件，可能導致多個實例被創建。

- 執行緒安全的延遲初始化

    為了解決多執行緒問題，可以在 `getInstance()` 方法上加 `synchronized` 鎖。

	```java
	public class Singleton {
	    private static Singleton instance;

	    private Singleton() {}

	    public static synchronized Singleton getInstance() {
	        if (instance == null) {
	            instance = new Singleton();
	        }
	        return instance;
	    }
	}
	```

    缺點：每次呼叫 `getInstance()` 都需要獲取鎖，影響效能。

- 雙重檢查鎖定 (Double-checked Locking)

    這種方式減少了鎖的開銷，只有在實例尚未創建時才加鎖。

	```java
	public class Singleton {
	    private static volatile Singleton instance;

	    private Singleton() {}

	    public static Singleton getInstance() {
	        if (instance == null) {
	            synchronized (Singleton.class) {
	                if (instance == null) {
	                    instance = new Singleton();
	                }
	            }
	        }
	        return instance;
	    }
	}
	```

    注意：使用 `volatile` 關鍵字避免指令重排序，確保實例初始化的正確性。

- 立即初始化 (Eager Initialization)

    在類別載入時就創建實例，適用於實例創建開銷較小的場景。

	```java
	public class Singleton {
	    private static final Singleton instance = new Singleton();

	    private Singleton() {}

	    public static Singleton getInstance() {
	        return instance;
	    }
	}
	```

    優點：簡單且執行緒安全。

    缺點：若實例創建成本高或應用程式不一定使用該實例，可能導致資源浪費。

- 初始化塊 (Initialization-on-Demand Holder Idiom)

    這種方式結合了延遲初始化和執行緒安全的優點，利用 Java 類別載入機制實現延遲載入。

	```java
	public class Singleton {
	    private Singleton() {}

	    private static class SingletonHolder {
	        private static final Singleton INSTANCE = new Singleton();
	    }

	    public static Singleton getInstance() {
	        return SingletonHolder.INSTANCE;
	    }
	}
	```

    優點：執行緒安全且實現延遲載入，效能較高。

- JavaScript 閉包實現 Singleton

    利用閉包實現 Singleton，適用於前端管理全域 API 客戶端。

	```javascript
	const ApiClient = (function () {
	  let instance;

	  function createInstance() {
	    return {
	      baseUrl: 'https://api.example.com',
	      headers: { 'Content-Type': 'application/json' },
	      async fetchData(endpoint) {
	        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
	          headers: this.headers
	        });
	        return response.json();
	      }
	    };
	  }

	  return {
	    getInstance: function () {
	      if (!instance) {
	        instance = createInstance();
	      }
	      return instance;
	    }
	  };
    })();



	// 使用範例
	const clientA = ApiClient.getInstance();
	const clientB = ApiClient.getInstance();
	clientA.headers.Authorization = 'Bearer token123';
	console.log(clientB.headers.Authorization); // 'Bearer token123'
	console.log(clientA === clientB);           // true
	```

    特點：利用立即執行函數 (IIFE) 封裝實例，適合簡單的前端應用。

- TypeScript 類別實現 Singleton

    使用 TypeScript 實現一個全域通知管理器。

	```typescript
	class NotificationManager {
	  private static instance: NotificationManager | null = null;
	  private notifications: { message: string; type: string }[] = [];

	  private constructor() {}

	  static getInstance(): NotificationManager {
	    if (!NotificationManager.instance) {
	      NotificationManager.instance = new NotificationManager();
	    }
	    return NotificationManager.instance;
	  }

	  addNotification(message: string, type: string = 'info') {
	    this.notifications.push({ message, type });
	    console.log('Notifications:', this.notifications);
	  }

	  getNotifications(): { message: string; type: string }[] {
	    return this.notifications;
	  }
	}



    /** 使用範例 */
	const managerA = NotificationManager.getInstance();
	const managerB = NotificationManager.getInstance();
	managerA.addNotification('操作成功', 'success');
	console.log(managerB.getNotifications()); // [{ message: '操作成功', type: 'success' }]
	console.log(managerA === managerB);       // true
	```

    特點：TypeScript 的型別系統增強程式碼的安全性和可讀性，適合需要型別檢查的前端專案。

- Angular 服務實現 Singleton

    在 Angular 中，服務預設為 Singleton (當在根模組注入時)。

    以下是一個全域設定管理的範例

	```typescript
	/** config.service.ts */
	import { Injectable } from '@angular/core';

	@Injectable({
	  providedIn: 'root' // 確保服務在根模組單例注入
	})
	export class ConfigService {
	  private settings: { [key: string]: string } = {};

	  setSetting(key: string, value: string) {
	    this.settings[key] = value;
	  }

	  getSetting(key: string): string | undefined {
	    return this.settings[key];
	  }
	}



	/** 使用範例 (元件中) */
	import { Component } from '@angular/core';
	import { ConfigService } from './config.service';

	@Component({
	  selector: 'app-root',
	  template: `<button (click)="setConfig()">設定</button>`
	})
	export class AppComponent {
	  constructor(private configService: ConfigService) {}

	  setConfig() {
	    this.configService.setSetting('theme', 'dark');
	    console.log(this.configService.getSetting('theme')); // 'dark'
	  }
	}
	```

    特點：Angular 的依賴注入系統天然支援 Singleton，`providedIn: 'root'` 確保服務實例全域唯一。

- React Context 結合 Singleton

    在 React 中，Singleton 可以與 Context 結合，實現全域通知管理器。

    ```javascript
    /** NotificationManager.js */
    class NotificationManager {
      static #instance = null;
      #notifications = [];

      constructor() {
        if (NotificationManager.#instance) {
          return NotificationManager.#instance;
        }
        NotificationManager.#instance = this;
      }

      static getInstance() {
        if (!NotificationManager.#instance) {
          NotificationManager.#instance = new NotificationManager();
        }
        return NotificationManager.#instance;
      }

      addNotification(message, type = 'info') {
        this.#notifications.push({ message, type });
        this.renderNotifications();
      }

      renderNotifications() {
        console.log('Notifications:', this.#notifications);
      }
    }



    /** NotificationContext.js */
    import { createContext, useContext } from 'react';

    const NotificationContext = createContext(NotificationManager.getInstance());

    export const useNotification = () => useContext(NotificationContext);



    /** App.jsx */
    import React from 'react';
    import { useNotification } from './NotificationContext';

    const App = () => {
      const notificationManager = useNotification();

      const notify = () => {
        notificationManager.addNotification('操作成功！', 'success');
      };

      return (
        <div>
          <button onClick={notify}>顯示通知</button>
        </div>
      );
    };

    export default App;
    ```

    特點：結合 React Context，Singleton 可在元件樹中方便存取，適合管理全域 UI 狀態。

<br />

## 應用場景

Singleton 模式適用於以下場景

- 全域資源管理

    例如：資料庫連線池、執行緒池或快取管理器。

- 設定管理：管理應用程式的全域設定

    例如：讀取設定檔。

- 硬體資源存取

    例如：像是印表機或檔案系統的單一存取點。

- 日誌系統：確保所有日誌記錄都寫入同一個檔案或輸出管道。

例如

- Java 的 `java.lang.Runtime` 類別是 Singleton 模式的典型應用，每個 Java 應用程式只有一個 `Runtime` 實例，用於與底層系統交互。

- 在前端，Singleton 可用於管理 API 客戶端或全域通知系統。

<br />

## 優缺點

### 優點

- 控制實例數量：確保只有一個實例，避免資源浪費。

- 全域存取：提供統一的存取點，方便系統各部分使用。

- 延遲載入 (部分實現)：僅在需要時創建實例，節省資源。

- 簡單易用：實現方式直觀，易於理解和維護。

### 缺點

- 執行緒安全問題：在多執行緒環境中，簡單實現可能導致競爭條件。

- 單元測試困難：由於全域狀態，Singleton 可能導致測試時的依賴問題，難以模擬或重置狀態。

- 濫用風險：過度使用 Singleton 可能導致程式碼耦合度高，違反物件導向的單一職責原則。

- 擴展困難：Singleton 模式難以支援子類別化或動態替換實例。

<br />

## 注意事項

- 執行緒安全：在多執行緒環境中，選擇適當的實現方式 (例如：雙重檢查鎖定或初始化塊) 以確保安全。在前端，需注意非同步操作的初始化順序。

- 防止反射攻擊：外部程式碼可能透過反射繞過私有建構函數，需在建構函數中添加檢查。

	```java
	private Singleton() {
	    if (instance != null) {
	        throw new RuntimeException("Use getInstance() method to get the single instance of this class.");
	    }
	}
	```

- 序列化問題：若 Singleton 類別實現了 `Serializable`，反序列化可能創建新實例，需實現 `readResolve()` 方法。

	```java
	private Object readResolve() {
	    return getInstance();
	}
	```

- 避免濫用：僅在需要全域唯一實例時使用 Singleton，避免將其作為全域變數的替代品。

<br />

## 與其他模式的關係

- 與工廠模式 (Factory Method)：Singleton 可與工廠模式結合，透過工廠方法提供單例實例。

- 與抽象工廠 (Abstract Factory)：抽象工廠可能使用 Singleton 確保工廠本身的唯一性。

- 與狀態模式 (State)：Singleton 可作為全域狀態管理器，與狀態模式搭配使用。

<br />

## 總結

Singleton 模式是一種簡單而強大的創建型設計模式，適用於需要確保唯一實例並提供全域存取的場景。

在前端開發中，Singleton 特別適合管理 API 客戶端、通知系統或全域設定。透過 JavaScript、TypeScript、Angular 和 React 的實現，開發人員可靈活應用 Singleton 於不同場景。

開發人員需根據應用場景選擇合適的實現，並注意執行緒安全、測試性和擴展性等問題。正確使用 Singleton 模式能有效提升系統的資源利用率和一致性，但應避免濫用，以免導致程式碼維護困難。對於希望深入理解物件導向設計的開發人員來說，Singleton 是一個值得學習和掌握的基礎模式。
