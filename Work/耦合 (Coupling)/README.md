# 耦合 (Coupling)

耦合 (Coupling) 在軟體設計與系統架構中是一個很重要概念，影響著系統的可維護性、可擴展性以及模組之間的協作方式。無論是在前端、後端，還是整個系統架構中，開發人員都需要去理解耦合的概念。

耦合指的是系統中的不同模組 (Module) 或元件 (Component) 之間的相依程度。若兩個模組之間的關係緊密，當一個模組改變時，另一個模組也需要跟著修改，那就代表兩者的耦合度高。反之，若模組之間的依賴較少，那耦合度就低。

舉個簡單的例子：

假設有一個「訂單系統」，其中有「訂單模組」和「支付模組」。若這兩個模組高度耦合，代表「支付模組」內部直接調用了「訂單模組」的函式，甚至依賴其內部實作細節，這樣當「訂單模組」變更時，「支付模組」可能也需要同步修改。

在這種情況下，系統變更的成本高，且容易發生連鎖錯誤。

<br />

## 高耦合 vs 低耦合

高耦合 (Tightly Coupled)

- 兩個模組彼此強烈依賴，難以單獨測試或修改。

- 當一個模組變更時，其他相關模組也可能需要修改。

- 加維護成本，降低系統的靈活性和擴展性。

低耦合 (Loosely Coupled)

- 各個模組之間的關係較為獨立，能夠各自變更而不影響其他部分。

- 容易測試與除錯，系統更具彈性與可擴展性。

- 有助於模組的重複使用 (Reusability)，提升開發效率。

高耦合的系統通常難以維護，而低耦合的系統則更靈活，適合長期發展。

<br />

## 耦合的適用範圍

耦合主要是用來描述模組 (module) 之間的依賴程度，在許多程式語言 (特別是現代前端和後端開發) 中，模組的範圍可以不同，因此耦合的概念也可以適用在類別 (class)、函式 (function)、甚至整個服務 (service) 之間的關係。

- 模組層級耦合

    在軟體開發中，模組之間應該降低不必要的依賴，以提升系統的可維護性與可測試性。例如：在 Node.js 中，若 `userService.js` 直接調用 `fileUploadService.js` 的函式來處理檔案上傳，那麼這兩個模組之間就存在較高的耦合。理想的做法是透過介面 (interface) 或依賴注入 (Dependency Injection，簡稱：DI) 來降低直接依賴。

- 類別層級耦合

    在物件導向設計 (OOP) 中，類別之間的耦合應該被適當控制。例如：若 `UserManager` 類別直接操作 `DatabaseConnector` 類別的內部細節 (例如： SQL 查詢字串)，那麼這樣的耦合就會很高，使得 `UserManager` 無法輕易更換資料庫系統。理想的做法是透過抽象層 (例如：Repository Pattern) 來降低耦合，使 `UserManager` 只依賴 `UserRepository` 介面，而不是具體的資料庫實作。

- 函式層級耦合

    函式之間的耦合應該保持在最小程度。例如：若 `processData()` 直接呼叫 `sendEmail()`，而 `sendEmail()` 又依賴 `database.save()`，那麼這些函式之間的耦合度就會過高，使得 `processData()` 不能單獨運作。理想的做法是讓 `processData()` 回傳結果，然後由調用者決定是否要進行 `sendEmail()` 或 `database.save()`，藉此降低函式之間的直接依賴。

- 高耦合的模組範例 (Bad)

    在這個例子中，`userModule.ts` 直接依賴 `paymentModule.ts` 和 `emailModule.ts，`這表示無法獨立運作，且若 `paymentModule.ts` 或 `emailModule.ts` 變更，`userModule.ts` 可能也需要修改。

    ```typescript
    /** 高耦合的模組 */
	/** userModule.ts */
	import { processPayment } from './paymentModule';
	import { sendMarketingEmail } from './emailModule';

	export function createUser() { 
	  /* 建立使用者 */
	  processPayment();     // 直接依賴付款模組
	  sendMarketingEmail(); // 直接依賴郵件模組
	}

	export function deleteUser() { 
	  /* 刪除使用者 */ 
	}

	export function updateUser() { 
	  /* 更新使用者資訊 */ 
	}

	export function getUserDetails() { 
	  /* 取得使用者資訊 */ 
	}
    ```

	```typescript
	/** paymentModule.ts */
	export function processPayment() { /* 處理付款 */ }
	```

    ```typescript
    /** emailModule.ts */
    export function sendMarketingEmail() { /* 發送行銷郵件 */ }
    ```

    問題點 (高耦合的壞處)

    - 模組之間的依賴過高：`userModule.ts` 直接調用 `paymentModule.ts` 和 `emailModule.ts`，導致模組之間的變更影響性變大。

    - 降低模組的可重用性：若 `userModule.ts` 想在沒有付款功能的環境下使用 (例如：免費版系統)，就無法輕易拆分。

    - 難以測試：測試 `createUser()` 時，會連帶影響 `processPayment()` 和 `sendMarketingEmail()`，增加測試難度。

- 低耦合的模組範例 (Good)

    在這個例子中，`userModule.ts` 不直接依賴付款或郵件模組，而是透過依賴注入 (Dependency Injection) 或回呼函式 (Callback Function) 來降低耦合度。

	```typescript
	/** 低耦合的模組 */
	/** userModule.ts */

    /** 透過 callback 而非直接依賴 */
    export function createUser(onUserCreated?: () => void ) { 
      /* 建立使用者 */
      if (onUserCreated) {
        onUserCreated(); // 執行額外的處理 (但 userModule 本身不依賴其他模組)
      }
    }

	export function deleteUser() { 
	  /* 刪除使用者 */ 
	}

	export function updateUser() { 
	  /* 更新使用者資訊 */ 
	}

	export function getUserDetails() { 
	  /* 取得使用者資訊 */ 
	}
	```

	```typescript
	/** main.ts (或其他模組來決定是否要整合付款或郵件功能) */
	import { createUser } from './userModule';
	import { processPayment } from './paymentModule';
	import { sendMarketingEmail } from './emailModule';

	createUser(() => {
	  processPayment();
	  sendMarketingEmail();
	});
    ```

    優點 (低耦合的好處)

    - 降低模組之間的依賴：`userModule.ts` 不再直接呼叫 `paymentModule.ts` 或 `emailModule.ts`，而是透過 Callback Function 或外部控制來決定是否執行相關功能。

    - 提升可重用性：`userModule.ts` 可以在沒有付款或郵件功能的專案中使用，而不需要修改程式碼。

    - 提高測試性：可以單獨測試 `createUser()`，不需要模擬 `processPayment()` 或 `sendMarketingEmail()`。

<br />

## 耦合的類型

耦合可以依據不同的依賴方式分類，以下是幾種常見的耦合類型，從最差 (高耦合) 到最好 (低耦合) 排列如下：

1. 內容耦合 (Content Coupling)

    最高耦合

    當一個模組直接存取或修改另一個模組的內部資料或實作細節時，稱為「內容耦合」。這是最嚴重的耦合類型，因為模組之間的相依性極高，導致修改一個模組時，另一個模組也需要同步更改。

    ### 適用場景與影響

    - 影響可維護性：若某個函式直接修改另一個函式的內部變數，則當函式的內部實作變更時，所有存取這個變數的函式也可能需要修改。

    - 影響可讀性與可測試性：測試時，單元測試無法獨立進行，因為模組之間互相影響。

    ### 程式碼範例

    ```typescript
    function updateUserProfile(user) {
      user.name = "New Name"; // 直接修改物件屬性
    }
    ```

    ### 改善程式碼

    ```typescript
    function updateUserProfile(user, newName) {
      return { ...user, name: newName }; // 傳回新物件，避免直接修改
    }
    ```

2. 共用耦合 (Common Coupling)

    當多個模組共享同一個全域變數 (Global Variable) 時，就會產生「共用耦合」。這種耦合類型可能導致某個模組修改變數時，影響到所有依賴該變數的其他模組。

    ### 適用場景與影響

    - 影響可維護性：當某個模組修改共用變數時，所有依賴該變數的模組都可能受到影響。

    - 影響除錯難度：當發生錯誤時，很難追蹤是哪個模組修改了變數。

    ### 特徵

    - 模組內部執行相似類型的功能，但內部處理方式可能大不相同。

    - 通常會使用 `switch` 或 `if-else` 來決定要執行哪種功能。

    ### 程式碼範例

    ```typescript
    let globalConfig = { theme: "dark" };

	function changeTheme(newTheme) {
	  globalConfig.theme = newTheme; // 所有模組都依賴這個變數
	}
    ```

    ### 改善程式碼

    ```typescript
    function createConfig() {
      let theme = "dark";
      return {
        getTheme: () => theme,
        setTheme: (newTheme) => theme = newTheme
      };
    }

    const config = createConfig();
    ```

    透過閉包 (closure) 封裝變數，避免模組直接存取共用變數。

3. 控制耦合 (Control Coupling)

    當一個模組透過「控制參數」影響另一個模組的內部行為時，稱為「控制耦合」，表示呼叫者需要知道被呼叫者的內部程式碼，才能提供正確的參數。

    ### 適用場景與影響

    - 降低可讀性：函式的行為取決於參數值，增加理解的難度。

    - 影響模組獨立性：若控制參數變更，所有呼叫該函式的地方都可能需要調整。

    ### 程式碼範例

    ```typescript
	function processData(data, mode) {
	  if (mode === "json") {
	    return JSON.stringify(data);
      } else if (mode === "xml") {
	    return convertToXML(data);
	  }
	}
    ```

    ### 改善程式碼

    ```typescript
	function processDataJson(data) {
	  return JSON.stringify(data);
	}

	function processDataXml(data) {
	  return convertToXML(data);
	}
    ```

    將不同的處理拆分為獨立函式，而非透過 `mode` 參數控制。

4. 標誌耦合 (Stamp Coupling)

    當一個函式傳遞「過多的資料結構」給另一個函式，而這些資料結構中的某些部分實際上不會被使用，則稱為「標誌耦合」。這種情況增加了函式間的相依性，也可能影響效能。

    ### 適用場景與影響

    - 影響模組獨立性：函式不應該接受不必要的參數，避免過度相依。

    - 影響效能：若傳遞大型物件，可能導致記憶體浪費或不必要的運算。

    ### 程式碼範例

    ```typescript
	function printUserInfo(user) {
	  console.log(user.name); // 只使用了 `name`，但傳遞了整個 `user`
	}
    ```

    ### 改善程式碼

    ```typescript
	function printUserInfo(userName) {
	  console.log(userName);
	}
    ```

    只傳遞必要的資料，而非整個物件。

5. 資料耦合 (Data Coupling，最低耦合)

    當模組之間僅透過「必要的參數」傳遞資料，而不依賴彼此的內部狀態時，稱為「資料耦合」。這是最理想的耦合方式，因為提供了最佳的模組獨立性。

    ### 適用場景與影響

    - 增加可維護性：函式之間只透過參數交換必要的資訊，不會影響彼此的內部狀態。

    - 降低相依性：模組可以獨立變更，而不會影響其他模組。

    ### 程式碼範例

    ```typescript
	function add(a, b) {
	  return a + b;
	}
    ```

    這個函式只依賴傳入的參數，完全沒有外部相依性，因此是最理想的耦合方式。

<br />

## 耦合的好處

- 促進模組間的協作 (Facilitates Module Interaction)：適當的耦合使不同模組能夠順利溝通，確保系統功能的完整性與穩定性。

- 提高程式的靈活性 (Enhances Flexibility)：適當的耦合允許模組之間適度共享數據或控制流程，使系統在保持獨立性的同時，仍能靈活適應變更需求。

- 降低重複開發 (Reduces Redundant Development)：模組之間透過適當的耦合共享資源，避免重複實作相同功能，提高開發效率。

- 支援模組重用 (Supports Module Reusability)：當模組之間維持適當的耦合關係時，可以更容易將某些模組重複使用於不同的專案或系統。

- 提升系統整合性 (Improves System Integration)：透過適當的耦合，確保系統各個部分能夠有效整合與運作，使整體系統運行順暢。

<br />

## 如何提升內聚性

為了讓系統更靈活、易於維護，應該盡可能降低耦合，以下是幾種常見的方式：

- 使用介面與抽象 (Abstraction)

    使用 `interface` 來定義功能，避免直接依賴具體實作。

    ### 程式碼範例

    ```typescript
    interface PaymentProcessor {
      process(amount: number): void;
    }

    class CreditCardPayment implements PaymentProcessor {
      process(amount: number) {
        console.log(`Processing credit card payment of ${amount}`);
      }
    }

    class PayPalPayment implements PaymentProcessor {
      process(amount: number) {
        console.log(`Processing PayPal payment of ${amount}`);
      }
    }
    ```

    透過 `PaymentProcessor` 介面，可以在不同的支付方式之間自由切換，而不影響 process 的使用者。

- 依賴注入 (Dependency Injection，簡稱：DI)

    依賴注入可以減少模組之間的直接依賴，讓系統更靈活。在 Angular、Spring Boot 等框架中很常見。

- 遵循單一職責原則 (Single Responsibility Principle，簡稱：SRP)

    讓每個模組只負責單一功能，避免過多的相依性。

- 使用事件驅動架構 (Event-Driven Architecture)

    例如：透過 Pub/Sub (發布/訂閱模式) 來降低模組間的耦合。

<br />

## 總結

| 耦合種類 | 耦合程度 | 特徵 | 影響 | 解決方案 |
| - | - | - | - | - |
| 內容耦合 | 🚨🚨🚨🚨 (最高) | 直接修改其他模組的內部狀態 | 極難維護，變更影響廣泛 | 使用參數傳遞資料，避免直接存取 |
| 共用耦合 | 🚨🚨🚨 | 多個模組共享全域變數 | 修改時影響所有依賴模組 | 使用閉包、狀態管理工具 |
| 控制耦合 | 🚨🚨 | 透過控制參數改變行為 | 影響函式可讀性 | 拆分函式，避免多重行為 |
| 標誌耦合 | 🚨 | 傳遞不必要的物件 | 影響效能與模組獨立性 | 只傳遞必要的資料 |
| 資料耦合 | ✅ (最低) | 透過參數交換必要資訊 | 最理想的耦合方式 | 只傳遞函式所需的資料 |

耦合是影響軟體品質的重要因素，應該盡可能降低耦合，讓系統更具彈性和可擴展性。透過適當的設計模式，例如：介面 (Interface)、依賴注入、事件驅動架構等，可以有效降低耦合，提高軟體的可維護性與重複使用性。
