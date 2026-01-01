# Cordova

在行動應用程式開發領域，開發人員往往需要同時面對 iOS 與 Android 等多個平台。若使用原生開發 (Native Development)，就必須分別使用 Swift/Objective-C (iOS) 與 Java/Kotlin (Android) 撰寫程式碼，不僅增加開發成本，也提高維護難度。

為了降低這些問題，Apache Cordova (簡稱 Cordova) 應運而生，成為跨平台應用程式開發的重要工具之一。

<br />

## Cordova 簡介

Cordova 是由 Apache 基金會維護的開源專案，最早由 Nitobi 公司開發，後來被 Adobe 收購並整合為 PhoneGap，再釋出為 Apache Cordova。

核心理念是：「使用 Web 技術開發行動應用程式」。

Cordova 容許開發人員透過 HTML、CSS 和 JavaScript 來撰寫 App 的畫面與功能，並且利用 Cordova 提供的 WebView 容器將應用程式包裝成原生 App，這樣開發人員就能使用熟悉的前端技術來開發跨平台的行動應用程式。

<br />

## Cordova 的運作原理

Cordova 的核心運作方式可以簡單理解為以下三層

- WebView 容器

    Cordova 會在 iOS 或 Android 上建立一個 WebView，將 HTML/CSS/JavaScript 的內容顯示在其中，讓 App 的介面由網頁技術來呈現。

- plugin (外掛) 層

    由於 Web 技術本身無法直接存取裝置硬體 (例如：相機、GPS、加速度感應器)，Cordova 提供了一套 plugin 系統 (plugin System)。

    plugin 由原生程式碼 (例如：Java/Swift/Objective-C) 撰寫，並透過 JavaScript API 對外提供功能。

    例如：呼叫相機拍照、存取聯絡人、推播通知、讀寫檔案。

- JavaScript 應用層

    開發人員主要使用 JavaScript 來撰寫功能，並透過 Cordova 提供的 API 與 plugin 來呼叫原生功能。

    簡單來說，Cordova 就像一個橋樑，將 Web 技術與行動裝置原生功能連結在一起。

<br />

## Cordova 的主要特點

- 跨平台

    使用一次開發，即可同時輸出 iOS、Android 甚至 Windows App。

- plugin 擴充性強

    內建常見裝置 API plugin (例如：相機、GPS、檔案系統)，同時允許社群開發 plugin，或自行撰寫專屬 plugin。

- 結合前端框架

    Cordova 與常見的前端框架相容，例如：Angular、Vue.js、React。也能搭配 Ionic 等 UI Framework，打造接近原生體驗的介面。

- 開源免費

    由 Apache 基金會維護，開發人員可自由使用並修改。

<br />

## Cordova 的優缺點

### 優點

- 減少多平台開發成本，一套程式碼可支援多個系統。

- 前端開發人員可直接轉型為行動應用開發人員。

- 社群資源豐富，擴充性高。

### 缺點

- 效能通常不如原生應用，特別是需要大量動畫或高效能計算的情境。

- UI 體驗有時難以做到完全的原生感。

- plugin 相依性高，若 plugin 維護不足，可能導致平台更新後出現相容性問題。

<br />

## Cordova 的應用場景

Cordova 特別適合以下情境

- 中小型企業：希望快速推出跨平台應用，但資源有限。

- 資訊系統整合：例如企業內部系統 App，不需要高度原生體驗。

- 原型開發：快速驗證商業模式，之後再決定是否轉為原生開發。

<br />

## Cordova 的現況與發展

隨著行動應用的多樣化，市場上也出現了其他跨平台框架，例如：React Native、Flutter，這些框架的效能與原生體驗通常優於 Cordova，因此近年來 Cordova 的熱度有所下降，但 Cordova 仍然在許多專案中被廣泛使用，特別是對於前端開發人員而言，Cordova 依然是一個入門門檻低且快速上手的解決方案。

<br />

## 總結

Apache Cordova 是一個以 Web 技術為基礎的跨平台行動應用開發框架，透過 WebView 與 plugin 系統，讓開發人員可以用 HTML、CSS、JavaScript 來打造多平台 App。

雖然在效能與原生體驗上略遜於 React Native 或 Flutter，但 Cordova 仍具備快速開發、降低成本、易於維護等優勢，適合用於企業內部應用、原型驗證或中小型專案。

對於熟悉前端技術的開發人員來說，Cordova 依然是一條進入行動應用開發的便捷道路。
