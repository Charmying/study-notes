# WebView

WebView 就是一個「嵌入在 App 裡的瀏覽器元件」，手機裝置本身就已經具備，能在手機 App 裡顯示網頁內容 (HTML、CSS 和 JavaScript)。

簡單來說，WebView 可以理解成就是把瀏覽器「縮小到 App 裡」，沒有網址列、沒有瀏覽器按鈕，只專門顯示網頁內容。

在混合式應用程式 (Hybrid App) 或需要部分網頁顯示的原生 App 裡非常常見，例如

- 顯示服務條款/隱私政策頁面

- 內嵌 H5 活動頁 (行銷活動、商品頁)

- 使用網頁作為主 UI，但外層仍是原生殼 (例如：React Native、Flutter、Cordova 等框架會大量依賴 WebView)

<br />

## Android 的 WebView

### 元件說明

- Android 提供 `android.webkit.WebView` 類別。

- 本質上是基於 Chromium 引擎 的一個嵌入式瀏覽器。

- 自 Android 5.0 (Lollipop) 起，WebView 被拆分成獨立應用程式，可以透過 Google Play 商店更新，不需要更新整個系統。

### 常見用法

```java
WebView myWebView = findViewById(R.id.webview);
myWebView.getSettings().setJavaScriptEnabled(true);// 開啟 JS
myWebView.loadUrl("https://example.com");
```

### 特點

- 可客製化程度高：可透過 `WebViewClient` 攔截連結點擊、`WebChromeClient` 控制 JavaScript alert、進度條等。

- 支援 JavaScript 與原生互動：可以透過 `addJavascriptInterface` 與網頁雙向傳遞資料。

- 效能依賴 WebView 版本：新系統支援度較好，舊裝置可能受限。

<br />

## iOS 的 WebView

### 元件說明

iOS 主要有兩種 WebView 方案

- UIWebView (已過時，從 iOS 12 開始被棄用)

- WKWebView (推薦使用，基於 Safari WebKit 引擎)

### WKWebView 範例

```swift
import WebKit

let webView = WKWebView(frame: self.view.bounds)
self.view.addSubview(webView)
let url = URL(string: "https://example.com")!
webView.load(URLRequest(url: url))
```

### 特點

- 效能佳：WKWebView 與 Safari 共用渲染引擎，速度快且安全性更高。

- 支援多進程架構：避免網頁崩潰導致整個 App crash。

- 可與 JavaScript 溝通：透過 `WKScriptMessageHandler` 與網頁互動。

- 安全限制更嚴格：比 Android 更注重 sandbox 和隱私保護。

### 補充

- iOS 8 (2014) → WKWebView 首次引入，但當時 UIWebView 還能用。

- iOS 12 (2018) → UIWebView 被正式標記為棄用 (deprecated)。

- 2019 年底 → 若 App 仍含有 UIWebView，Apple 開始在 App Store Connect 發出警告。

- 2020 年 4 月 → App Store 禁止上架含 UIWebView 的新 App。

- 2020 年 12 月 → App Store 禁止更新含 UIWebView 的舊 App。

也就是說

- 技術層面上，UIWebView 在 iOS 12 被棄用。

- 實務層面上，UIWebView 在 2020 年被徹底禁止使用，之後只能用 WKWebView。

<br />

## Android 與 iOS WebView 差異比較

| 項目 | Android WebView | iOS WKWebView |
| - | - | - |
| 核心引擎 | Chromium | WebKit (Safari) |
| 更新方式 | Play 商店獨立更新 | 跟隨 iOS 系統更新 |
| 過去版本 | 早期綁定系統版本，更新受限 | UIWebView 已棄用，WKWebView 取代 |
| JS 與原生溝通 | `addJavascriptInterface` | `WKScriptMessageHandler` |
| 穩定性/安全性 | 舊版可能受限，需依賴裝置與 WebView 版本 | 更穩定，安全限制較多 |
| 多進程支持 | 有，但依版本而定 | 原生支援 (避免網頁掛掉拖累 App) |

<br />

## 應用場景

- 快速上線：App 需要臨時展示活動頁，WebView 最方便。

- 跨平台框架依賴：React Native、Ionic、Cordova、Flutter (部分情境)等，都依賴 WebView 展示網頁內容。

- 混合式 App：部分頁面用原生實作 (例如：支付、拍照)，部分頁面用 Web 技術 (例如：商品頁、文章內容)。

<br />

## Cordova App 實務影響

| 影響項目 | Android WebView | WKWebView (iOS) |
| - | - | - |
| 性能 | 新版快，舊版可能慢 | 快、穩定 |
| 版本差異 | 不同 Android 版本 WebView 差異大，需要測試 | iOS 8+ 都用 WKWebView |
| plugin 支援 | 大部分 plugin 支援，但某些舊版 Android 需額外處理 | 現代 Cordova plugin 支援良好 |
| 安全性 | 新版安全，舊版注意漏洞 | Apple 官方推薦 |

<br />

## 總結

WebView 就是「App 裡的小型瀏覽器」，Android 用 WebView (Chromium)，iOS 用 WKWebView (WebKit)。

WebView 的好處是能快速整合網頁內容到 App，但缺點是效能通常比不上完全原生的 UI，並且在安全性、相容性上要多加注意。
