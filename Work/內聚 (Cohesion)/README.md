# 內聚 (Cohesion)

內聚 (Cohesion) 在軟體設計與系統架構中是一個很重要概念，用來描述模組 (Module) 內部各程式碼間關聯的緊密程度。當一個模組內的程式碼彼此高度相關，且共同達成單一目標時，就可以說是這個模組的內聚性高，也可以說，若模組內的功能彼此關聯性不高，甚至看起來是許多不相關的功能被硬塞進同一個模組，那麼內聚性就低。

內聚是高品質軟體設計的關鍵指標之一，高內聚的程式碼通常更容易維護、理解與測試，並且在系統變更時帶來較少的影響。

<br />

## 內聚的適用範圍

內聚主要是用來描述模組 (Module) 或元件 (Component) 內部的關聯程度，但在許多程式語言 (特別是現代前端和後端開發) 中，模組的範圍可以不同，因此內聚的概念也可以適用在類別 (Class)、函式 (Function)、甚至整個服務 (Service)。

- 模組層級內聚

    傳統上，內聚是用來評估「模組」內部的關聯性。例如：在 Node.js 中，一個 `userService.js` 檔案作為模組，其所有函式應該與「使用者」有關，不應該混入其他不相關的功能 (例如：處理檔案上傳)。

- 類別層級內聚

    在物件導向設計 (OOP) 中，類別內的屬性與方法應該要高度相關。若一個類別同時處理「使用者登入」和「報表產生」，那這樣內聚性就會很低，應該要拆分成不同類別。

- 函式層級內聚

    函式內的程式碼應該要高度相關，不應該在同一個函式裡混雜不相關的功能。例如：一個函式 `processData()` 不應該同時負責「驗證輸入」+「寫入資料庫」+「發送 Email」。

```typescript
/** userModule.ts (這裡的功能不相關) */
export function createUser() { /* 建立使用者 */ }
export function deleteUser() { /* 刪除使用者 */ }
export function processPayment() { /* 付款處理 */ } // 不該屬於 userModule
export function sendMarketingEmail() { /* 發送行銷郵件 */ } // 不該放這裡
```

```typescript
/** 高內聚的模組 */
/** userModule.ts */
export function createUser() { /* 建立使用者 */ }
export function deleteUser() { /* 刪除使用者 */ }
export function updateUser() { /* 更新使用者資訊 */ }
export function getUserDetails() { /* 取得使用者資訊 */ }
```

<br />

## 內聚的類型

內聚可以依據模組內部成員的關聯程度分為幾種不同等級，從最差 (低內聚) 到最好 (高內聚) 排列如下：

1. 偶然內聚 (Coincidental Cohesion)

    也可以叫做巧合內聚。

    若一個模組內的功能完全沒有關聯，只是都被放在一起，那這個模組的內聚性極低。例如：一個 `randomUtilities` 內部包含了計算稅額、圖片壓縮、字串轉換等毫不相干的功能，這樣的模組就屬於偶然內劇。這樣的程式碼很難理解和維護。

    ### 缺點

    - 可讀性低、維護困難、難以測試。

    ### 特徵

    - 模組內的功能無關聯，只是隨機放在一起。

    - 通常是為了省事，把許多不同的功能寫進一個函式內，導致可讀性差。

    ### 程式碼範例

    ```typescript
	function randomUtilities(input: string) {
	  console.log("Logging input:", input); // 日誌記錄

	  let reversed = input.split("").reverse().join(""); // 反轉字串
	  let timestamp = new Date().getTime();              // 取得當前時間戳
	  return { reversed, timestamp };
	}
    ```

    ### 問題

    - 這個函式同時做日誌記錄、字串反轉、時間戳記，功能完全無關，應該拆分成不同的函式。

    ### 改善程式碼

    ```typescript
	function logInput(input: string) {
	  console.log("Logging input:", input);
	}

	function reverseString(input: string): string {
	  return input.split("").reverse().join("");
	}

	function getCurrentTimestamp(): number {
	  return new Date().getTime();
	}
    ```

2. 邏輯內聚 (Logical Cohesion)

    若一個模組內部的功能屬於同一類型，但執行方式卻不同，那就屬於邏輯內聚。例如：一個 `processFile` 模組負責處理 image、audio 和 text 格式的檔案，但內部的方法彼此之間並沒有直接關聯，而是根據功能類別歸類在一起。這種內聚性仍然不理想，應該進一步拆分成不同的專屬模組，例如：`ImageProcessor`、`AudioProcessor` 和 `TextProcessor`。

    ### 缺點

    - 模組需要理解外部參數，增加了複雜度。

    ### 特徵

    - 模組內部執行相似類型的功能，但內部處理方式可能大不相同。

    - 通常會使用 `switch` 或 `if-else` 來決定要執行哪種功能。

    ### 程式碼範例

    ```typescript
    function processFile(type: string, data: any) {
      switch (type) {
        case "image":
          console.log("Processing image file");
          break;
        case "audio":
          console.log("Processing audio file");
          break;
        case "text":
          console.log("Processing text file");
          break;
        default:
          console.log("Unknown file type");
      }
    }
    ```

    ### 問題

    - 這個函式負責不同類型的文件處理，但內部處理方式不一定相關。

    - 當需要支援新的類型時，必須修改 `processFile`，違反開放封閉原則 (Open/Closed Principle，簡稱：OCP)。

    ### 改善程式碼

    使用策略模式 (Strategy Pattern) 來降低耦合

    ```typescript
    interface FileProcessor {
      process(data: any): void;
    }

	class ImageProcessor implements FileProcessor {
	  process(data: any) {
	    console.log("Processing image file");
	  }
	}

	class AudioProcessor implements FileProcessor {
	  process(data: any) {
	    console.log("Processing audio file");
	  }
	}

	class TextProcessor implements FileProcessor {
	  process(data: any) {
	    console.log("Processing text file");
	  }
	}

	/** 使用時 */
	const processorMap = {
      image: new ImageProcessor(),
      audio: new AudioProcessor(),
      text: new TextProcessor(),
	};

	function processFile(type: string, data: any) {
	  processorMap[type]?.process(data) ?? console.log("Unknown file type");
	}
    ```

3. 時間內聚 (Temporal Cohesion)

    若模組內的功能是在特定時間點執行，但彼此之間沒有直接關聯，那就屬於時間內聚。例如：在程式啟動時會執行「環境變數載入系統設定」、「建立與資料庫的連線」、「 建立快取機制」等不同的功能，這些功能雖然在時間上相關，但功能上並不直接相關。因此，應該將這些功能拆分成不同的模組，使其內聚性更高。

    ### 缺點

    - 若某個功能需要獨立修改，可能會影響其他功能。

    ### 特徵

    - 模組內的功能必須在相同時間點執行，但功能可能無關。

    - 常見於 `init()`、`startup()` 這類函式，將多種初始化工作放在一起。

    ### 程式碼範例

    ```typescript
    function initializeSystem() {
      console.log("Loading configuration...");
      console.log("Initializing database connection...");
      console.log("Starting web server...");
    }
    ```

    ### 問題

    - 雖然這些初始化步驟通常會一起執行，但功能並不完全相關。

    - 若 database connection 的初始化程序改變，就會影響 initializeSystem，不易擴展。

    ### 改善程式碼

    應該拆分成不同的初始化函式，並由統一的 `init()` 呼叫

    ```typescript
    function loadConfig() {
      console.log("Loading configuration...");
    }

    function initDatabase() {
      console.log("Initializing database connection...");
    }

    function startServer() {
      console.log("Starting web server...");
    }

    function initializeSystem() {
      loadConfig();
      initDatabase();
      startServer();
    }
    ```

    這樣可以獨立修改各個函式，而不影響其他部分。

4. 程序內聚 (Procedural Cohesion)

    若模組內的功能是按照固定程序執行，但每個步驟的關聯性不強，那就屬於程序內聚。例如：一個 `processOrder` 模組包含「驗證訂單資訊 → 計算折扣 → 產生發票 → 發送 Email 通知」，這些步驟雖然按照特定順序執行，但並非完全相關。這種情況下，應該將這些功能拆分成更專門的模組，例如：`validateOrder`、`calculateTotal`、`generateInvoice` 和 `sendEmail`，讓內聚性提高。

    ### 缺點

    - 功能之間的關係不夠緊密，可能導致難以重複使用某些部分。

    ### 特徵

    - 模組內的功能必須按固定順序執行，但彼此的關聯性仍然不夠高。

    ### 程式碼範例

    ```typescript
    function processOrder(order: any) {
	  validateOrder(order);
	  calculateTotal(order);
	  generateInvoice(order);
	  sendEmail(order);
    }
    ```

    ### 問題

    - 雖然這些步驟是按順序執行的，但 `calculateTotal()` 和 `generateInvoice() 應該屬於不同模組。

    - 若某個步驟需要變更，可能會影響整個函式。

    ### 改善程式碼

    應該拆分責任，讓 `OrderProcessor` 來管理流程，這樣可以更容易測試與擴展

    ```typescript
    class OrderProcessor {
      validateOrder(order: any) {console.log("Validating order...");}

      calculateTotal(order: any) {
        console.log("Calculating total...");
      }

      generateInvoice(order: any) {
        console.log("Generating invoice...");
      }

      processOrder(order: any) {
        this.validateOrder(order);
        this.calculateTotal(order);
        this.generateInvoice(order);
      }
    }
    ```

5. 通訊內聚 (Communicational Cohesion)

    當模組內的所有成員都使用相同的資料結構或變數，那就屬於通訊內聚。例如：一個 `processUserData` 模組在處理「格式化使用者名稱」、「驗證電子郵件 」、「儲存使用者到資料庫 」，功能雖然不同，但都依賴相同的資料來源，因此內聚性相對較高。不過，這類模組仍有進一步拆分的可能性，讓不同的功能獨立運作。

    ### 優點

    - 較容易維護，但仍可能需要進一步拆分。

    ### 特徵

    - 模組內的功能處理相同的輸入或輸出，彼此有一定關聯。

    ### 程式碼範例

    ```typescript
	function processUserData(user: any) {
	  const formattedName = formatUserName(user.name);
	  const email = validateEmail(user.email);
	  saveUserToDatabase(user, formattedName, email);
	}
    ```

    所有函式都在處理相同的使用者資料，而不是無關的功能。

6. 功能內聚 (Functional Cohesion)

    當模組內的所有成員共同達成單一功能，並且不可拆分，那就屬於功能內聚。例如：一個 `calculateTax` 負責「計算稅金」，這個模組內的所有方法都只和這個主要目標相關，這樣的內聚性非常高，具有良好的可讀性、可維護性和可測試性。這就是最理想的內聚類型。

    ### 優點

    - 高可讀性、高可重用性、易於測試與維護。

    ### 特徵

    - 模組內的功能只做一件事情，且高度相關。

    ### 程式碼範例

    ```typescript
    function calculateTax(income: number): number {
      return income * 0.2;
    }
    ```

    這個函式只負責計算稅金，沒有額外不必要的責任，易於測試與擴展。

<br />

## 內聚的好處

- 提高可讀性 (Readability)：當模組內的功能高度相關時，開發人員更容易理解其用途，降低學習成本。

- 提升可維護性 (Maintainability)：模組內部功能彼此高度相關，變更時不會影響無關功能，降低維護成本。

- 減少耦合 (Reduce Coupling)：高內聚通常伴隨著低耦合，使系統更具彈性，方便重構與擴展。

- 增強可測試性 (Testability)：若模組的功能單一，則撰寫單元測試 (Unit Test) 時會更容易，因為不會牽涉到不相關的功能。

- 降低 Bug 產生機率：當模組只專注於單一功能時，程式的錯誤範圍較小，不會影響不相關的部分，提升系統的穩定性。

<br />

## 如何提升內聚性

- 遵循單一職責原則 (Single Responsibility Principle，簡稱：SRP)

    - 讓每個模組只負責一件事，若模組的功能過於分散，應該考慮拆分。

- 使用合理的模組命名

    - 若一個模組的名稱難以概括其功能，那麼很可能具有低內聚性。例如：`HelperFunctions` 這種模組名稱過於模糊，應該拆分成更具體的模組，例如：`DateHelper`、`StringHelper`。

- 減少跨模組的資料共享

    - 若一個模組頻繁存取另一個模組的變數或函式，表示這兩個模組應該可以合併，或重新調整設計。

- 使用分層架構 (Layered Architecture)

    - 例如：在前端開發時，可以將資料處理放在 Service 層，而非 component 層，這樣可以確保每個層級的內聚性較高，職責清晰。

<br />

## 總結

| 內聚類型 | 優劣 | 特色 |
| - | - | - |
| 偶然內聚 | ❌ 最差 | 完全無關的功能混合在一起 |
| 邏輯內聚 | ❌ | 透過 `switch` 或 `if` 控制，但功能不相關 |
| 時間內聚 | ⚠️ | 依照時間點執行，但功能未必有關 |
| 程序內聚 | ⚠️ | 依照固定順序執行，但關聯性不夠 |
| 通訊內聚 | ✅ | 處理相同的數據或輸出，關聯度較高 |
| 功能內聚 | ✅ 最佳 | 模組內的功能高度相關，只做一件事 |

內聚是衡量軟體品質的重要指標之一，高內聚的程式碼通常具有更好的可讀性、可維護性、可測試性，並且較少出現錯誤。在開發過程中，應該盡量提升內聚性，避免讓模組變得過於雜亂或擁有過多責任。透過遵循單一職責原則、適當拆分模組，以及減少不必要的資料共享。
