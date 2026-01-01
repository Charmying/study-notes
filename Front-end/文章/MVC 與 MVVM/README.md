# MVC 與 MVVM

在程式開發中，為提升程式的可維護性、可讀性與模組化程度，開發人員常使用架構設計模式，其中，MVC (Model-View-Controller) 與 MVVM (Model-View-ViewModel) 是兩種廣泛應用的模式，特別在前端與全端開發中扮演重要角色。

<br />

## MVC (Model-View-Controller)

### 組成

- M = Model：負責應用程式的數據，包括資料存取 (例如：資料庫操作)、業務規則 (例如：資料驗證、計算)。

- V = 負責用戶界面的顯示，呈現 Model 中的資料，通常不直接與 Model 互動。

- C = Controller：處理用戶輸入，接收請求並調用 Model 更新資料，或將結果傳遞給 View，不應包含業務規則。

### 簡介

MVC 最早於 1978 年提出，目標是在解決程式碼混亂的問題，將程式拆分成資料 (Model)、界面 (View) 和控制 (Controller) 三層。

### 運作方式

- View 透過 Controller 獲取 Model 的資料並呈現給用戶。

- 用戶透過 View 觸發操作，Controller 接收後調用 Model 處理業務規則。

- Model 更新資料後，透過觀察者模式 (Observer Pattern) 通知 View 更新界面。

<img src="https://charmying-blog.onrender.com/img/web-mvc.6cae755e.svg" width="100%" />

```javascript
const M = {}, V = {}, C = {};
/** Model 存放資料 */
M.data = "hello world";
/** View 顯示資料 */
V.render = (M) => { alert(M.data); };
/** Controller 連接 M 和 V */
C.handleOnload = () => { V.render(M); };
/** 頁面載入時觸發 */
window.onload = C.handleOnload;
```

### 優點

- 最知名的架構模式，廣泛應用於軟體開發。

- 模組間可獨立開發與替換 (例如：更換資料庫)。

- 實現關注點分離，程式碼易於維護和測試。

- 適合快速換皮與套版，滿足不同客戶需求。

### 缺點

- 原理複雜，開發前期需花時間規劃。

- 模組界線需要明確定義，對初學者有學習門檻。

- 在大規模應用中，Controller 可能變得過於龐大。

- 若沒有用好，業務規則可能被錯誤放入 Controller。

### 總結

MVC 的主要優點在於提供良好的關注點分離 (Separation of Concerns)，使團隊成員能夠在不互相干擾的情況下並行開發。例如：前端開發人員可以專注於 View 的設計，而後端開發人員則專注於資料與業務規則 (Model)。

然而，隨著應用規模擴大，Controller 容易變得龐大且複雜，尤其是同時處理多種規則時，會影響可維護性與可讀性，進而成為開發瓶頸。

<br />

## MVVM (Model-View-ViewModel)

### 組成

- M = Model：與 MVC 的 Model 類似，處理資料與存取。

- V = View：負責界面顯示，透過資料綁定與 ViewModel 互動。

- VM = ViewModel：作為 View 與 Model 的中介，轉換 Model 資料為 View 可顯示的格式，並處理命令與事件。

### 簡介

MVVM 是 MVC 的演進模式，特別在 Web 前端開發中受歡迎。MVVM 將程式拆分成資料 (Model)、界面 (View) 和轉換資料層 (ViewModel)，更注重用戶端界面管理。

### 運作方式

- View 透過 ViewModel 的資料渲染界面。

- 用戶操作 View 時，事件傳遞至 ViewModel，ViewModel 調用 Model 處理資料。

- Model 更新後通知 ViewModel，ViewModel 資料變更則自動觸發 View 更新。

- 核心特色是資料綁定 (Data Binding)，支援雙向綁定 (Two-Way Binding)，實現 View 與 ViewModel 的自動同步。

<img src="https://charmying-blog.onrender.com/img/MVVMPattern.c86fd32c.webp" width="100%" />

通常多用於與 UI 較相關的前端部分

### 優點

- 降低學習門檻，易於理解與使用。

- 透過資料綁定，View 與 ViewModel 耦合度低，ViewModel 不依賴特定 View，增加重用性。

- 業務規則獨立於 UI，便於單元測試與元件重用。

### 缺點

- 在大型應用中，資料綁定可能導致記憶體消耗過大。

- 自動綁定導致 Debug 難以追蹤問題來源。

- View 因綁定 ViewModel，難以簡單重用。

- 學習曲線較陡峭，特別對不熟悉資料綁定的開發人員。

### 總結

MVVM 的最大優勢是實現了 View 與 Model 之間的完全分離，並進一步簡化了控制。透過引入 ViewModel，開發人員可以在不依賴 View 的情況下，撰寫可測試、可重用的介面，提升了整體開發效率與維護性。

MVVM 在許多現代前端框架中被廣泛應用，例如：Angular 與 Vue。這些框架提供了強大的資料綁定 (Data Binding) 與響應式 (Reactive) 特性，讓開發人員可以更輕鬆管理 UI 狀態與使用者互動，特別適合開發單頁應用 (SPA) 與高互動性的前端系統。

<br />

## 總結

MVC 起源於 Web Application，後廣泛應用於 Web 後端框架 (例如：Ruby on Rails、ASP.NET MVC)，注重全端業務規則與資料庫的分離。隨著前端 UI 複雜性增加，MVVM 應運而生，引入 ViewModel 與資料綁定，實現更好的分離與可維護性，特別適合單頁應用 (SPA)，例如：Angular、Vue。

- MVC

    - 優點：MVC 的核心優勢在於其良好的分離性，將業務規則 (Model)、界面 (View) 和控制 (Controller) 分開，使團隊成員能在不互相干擾的情況下進行開發。特別適合需要明確分層的全端項目。

    - 缺點：在大規模應用中，Controller 可能變得過於龐大且難以維護，因為過多規被集中在 Controller 中，增加了複雜性。

- MVVM

    - 優點：MVVM 通過引入 ViewModel，實現了 View 和 Model 的完全分離，同時大幅減少 Controller 的複雜性。ViewModel 負責處理界面，使其可以獨立於 View 進行測試和維護，並提高程式碼的重用性。此外，MVVM 在現代前端框架 (例如：Angular 和 Vue) 中被廣泛採用，提供強大的數據綁定和響應式特性，讓開發人員能更高效管理界面狀態和用戶交互。

    - 缺點：相對而言，MVVM 的學習曲線可能較陡，且在小型項目中可能顯得過於複雜。

### 選擇建議

- MVC 更適合注重全端業務規則與資料庫分離的項目，例如：傳統的後端驅動應用。

- MVVM 則在前端界面複雜、需要高效管理狀態和交互的場景中表現出色，例如：現代單頁應用 (SPA)。

開發人員在選擇時，應根據項目的規模、團隊的技術熟悉度以及具體需求來決定採用哪種模式。

<br />

## 參考資料

- [前端食堂 - MVC V.S. MVVM 學習筆記](https://front-chef.coderbridge.io/2021/02/27/mvc-mvvm)
