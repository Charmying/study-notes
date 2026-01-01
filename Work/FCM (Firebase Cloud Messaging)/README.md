# FCM (Firebase Cloud Messaging)

即時推播通知 (Push Notification) 是行動應用服務中非常重要的功能之一，無論是提醒使用者有新訊息、行銷活動，或是系統狀態更新，推播功能都能有效提升互動率與使用體驗。

FCM (Firebase Cloud Messaging) 正是 Google 所提供的一項免費雲端推播服務，讓開發人員能夠輕鬆從伺服器端向 Android、iOS 或 Web 應用程式傳送通知或資料訊息。

<br />

## FCM 簡介

Firebase Cloud Messaging (FCM)  是 Google Firebase 平台中的一項服務，主要功能是提供可靠且高效的訊息傳遞機制。

FCM 讓開發人員能夠

- 向使用者裝置傳送通知 (Notification Message)

- 向應用程式傳遞資料 (Data Message)

- 支援單一裝置、裝置群組或主題 (Topic) 推播

- 兼容 Android、iOS、Web 三大平台

簡單來說，FCM 是應用程式與雲端之間的即時溝通橋樑，可同時支援行銷、系統提示及資料同步等用途。

<br />

## FCM 的運作原理

FCM 的傳遞過程可分為四個主要階段

1. 註冊階段 (Registration)

    當應用程式第一次啟動時，會向 FCM 伺服器註冊，並取得一組唯一的 Token (裝置識別碼)。

    這個 Token 代表該裝置在 FCM 網路中的身分。

2. 伺服器端發送訊息 (Send Message)

    開發人員的應用伺服器 (Application Server) 可透過 FCM API 或 Firebase 主控台，將推播訊息傳送到指定的 Token、主題或條件。

    開發人員可使用 Firebase 主控台進行簡易的行銷或公告推播；若需自動化或條件式推播，則需透過 FCM API 由後端程式控制。

3. FCM 雲端轉送 (Cloud Delivery)

    FCM 伺服器會接收並處理這些推播請求，根據目標條件找到對應的裝置，然後透過加密通道傳遞訊息。

4. 客戶端接收 (Receive Message)

    使用者的應用程式在前景 (Foreground) 或背景 (Background) 狀態下，都能接收到 FCM 訊息。

    前景時可自行處理顯示條件；背景時則由系統自動顯示通知。

FCM 傳輸過程中採用 HTTPS 與加密通道確保資料安全，但訊息內容仍需由開發人員自行避免傳送敏感資訊 (例如：密碼或個資)。

<br />

## FCM 的訊息種類

FCM 的訊息可分為兩大類型

- 通知訊息 (Notification Message)

    這類訊息通常由 FCM 自動處理，用於顯示在系統通知列。

    常見用途例如

    - 新聞或活動推播

    - 聊天訊息提醒

    - 系統公告

    Android 和 iOS 系統會自動處理通知顯示，不需要額外的程式碼控制。

- 資料訊息 (Data Message)

    資料訊息由開發人員自訂內容與處理方式，應用程式在收到後可以自行決定如何呈現或觸發動作。

    常見用途例如

    - 即時同步資料 (例如：訂單狀態更新)

    - 靜默推播 (Silent Push)

    - 觸發後端行為或背景下載

也可以同時混合兩者，稱為「混合訊息 (Notification + Data Message)」。

| 類型 | 處理方式 | 常見用途 | 控制權 |
| - | - | - | - |
| Notification Message | 系統自動顯示 | 新聞、行銷通知 | 系統處理  |
| Data Message | 需自行處理 | 即時資料同步、靜默推播 | 開發人員控制 |
| 混合訊息 | 同時含通知與資料 | 客製通知互動 | 部分控制 |


<br />

## FCM 的主要功能特色

- 免費使用

    FCM 是 Firebase 平台提供的免費服務，無需額外費用即可傳送大量推播。

- 跨平台支援

    可同時支援 Android、iOS 與 Web 應用程式，實現多裝置同步推播。

- 主題訂閱 (Topic Messaging)

    開發人員可讓使用者訂閱特定主題，例如：「最新活動」、「系統更新」，再透過主題名稱進行群組推播。

- 條件式推播 (Condition Messaging)

    可使用條件語法 (例如：topicA && !topicB) 篩選推播對象。

- 可靠傳遞與排程機制

    FCM 具備重送與排程機制，即使裝置暫時離線，也能在連線後自動補送。

- 與 Firebase 生態整合

    可搭配 Firebase Analytics、Crashlytics、Remote Config 等工具，分析推播成效與使用者行為。

<br />

## FCM 的實際應用流程範例

以行動 App 為例，整體流程如下

1. 使用者首次啟動 App

    App 向 FCM 伺服器註冊，取得裝置 Token

2. App 將 Token 傳回應用伺服器 (儲存於資料庫)

3. 當有新事件 (例如：新訂單、訊息或促銷活動)

    應用伺服器呼叫 FCM API

4. FCM 將推播訊息轉送至目標裝置

5. App 收到後顯示通知或更新畫面內容

<br />

## FCM 簡易範例 (以 Node.js 為例)

```javascript
import admin from "firebase-admin";

admin.initializeApp({
  credential: admin.credential.cert("serviceAccountKey.json")
});

const message = {
  token: "使用者的裝置Token",
  notification: {
    title: "新通知",
    body: "您有一筆新的訂單！"
  },
  data: {
    orderId: "12345"
  }
};

admin.messaging().send(message)
  .then((response) => {
    console.log("推播成功:", response);
  })
  .catch((error) => {
    console.error("推播失敗:", error);
  });
```

雖然 FCM 無法自訂雲端功能，但開發人員可透過 Node.js 自建應用伺服器，進行推播條件、排程或資料整合的處理，再由伺服器端呼叫 FCM API 發送通知。

<br />

## FCM 常見應用場景

- 電商 App：推送訂單狀態更新或優惠通知

- 通訊軟體：傳送即時訊息提醒

- 內容媒體：發布最新文章或影片推播

- 金融服務：通知交易明細、安全警示

- 教育平台：提醒課程更新、作業截止時間

<br />

## FCM 的優缺點

整體而言，FCM 提供高穩定性與整合性，特別適合需要跨平台推播的中小型應用。

### 優點

- 免費且穩定

    FCM 是 Google Firebase 平台的一部分，完全免費使用，即使大量傳送通知也不收費。

    Google 的雲端基礎架構也保證了高可用性與可靠性，適合中小型團隊或新創專案快速導入。

- 跨平台支援完善

    FCM 同時支援

    - Android

    - iOS

    - Web 推播 (Progressive Web App，簡稱：PWA)

    讓開發人員能使用相同的後端程式碼與 API，統一管理多平台的推播功能，大幅減少開發與維護成本。

- 整合 Firebase 生態系

    FCM 可與其他 Firebase 工具無縫整合，例如

    - Firebase Analytics：追蹤推播開啟率與使用者行為

    - Firebase Remote Config：根據使用者分群動態調整內容

    - Firebase Authentication：與使用者身分綁定推播目標

    這種整合性讓 FCM 不僅是推播系統，更能形成完整的使用者互動分析架構。

- 多樣的推播方式

    FCM 提供彈性的訊息傳遞機制

    - 單一裝置推播 (Single Device)

    - 主題推播 (Topic Messaging)

    - 群組推播 (Device Group)

    - 條件推播 (Condition Messaging)

    這讓開發人員能針對不同族群、條件或行銷活動，精準推送訊息。

- 資料訊息 (Data Message) 可自訂

    除了顯示通知外，FCM 也支援純資料傳送。

    開發人員可透過資料訊息進行

    - 背景同步 (例如：訂單更新)

    - 靜默推播 (Silent Push)

    - 自行決定顯示方式與觸發條件

    大幅提升控制彈性。

- 有內建傳遞重試與離線補送機制

    若使用者的裝置暫時離線，FCM 會自動暫存訊息，在裝置重新上線後再行送達，確保訊息可靠性。

不過，FCM 作為雲端托管服務，仍有部分彈性與控制權的限制。

### 缺點

- 無法完全掌控伺服器端行為

    FCM 屬於 雲端托管服務，開發人員無法控制 Google 的內部傳遞機制。

    若 Google 端發生延遲或服務異常，開發人員僅能等待官方修復，無法自行介入。

- 對 iOS 功能有限制

    雖然 FCM 支援 iOS，但

    - 仍需透過 Apple Push Notification Service (APNs) 間接傳遞

    - 某些背景推播 (尤其靜默推播) 可能因 iOS 系統限制而無法正常運作

    - iOS 系統可能延後顯示或不顯示特定推播 (取決於使用者設定與省電策略)

    因此在 iOS 上的推播表現，通常比 Android 更受限。

- 依賴 Google 服務 (特別是 Android)

    在 Android 系統中，FCM 依賴 Google Play Services。

    若裝置沒有 Google 服務 (例如：中國市場或無 GMS 的手機)，推播將無法運作，需要改用其他替代方案 (例如：自建 MQTT 或第三方推播)。

- 無法保證「即時」傳遞

    雖然 FCM 傳遞速度通常很快，但

    - 若裝置進入省電模式、休眠狀態或網路品質不佳

    - FCM 伺服器流量高峰期

        訊息可能延遲數秒到數分鐘，因此不適合用於即時通訊的關鍵場景 (例如：金融交易或警報系統)。

- 設計彈性有限 (無法自訂後端)

    FCM 提供的 API 雖然簡單，但不支援複雜排程、訊息排隊、優先權處理。

    - 若需要進階功能 (例如：根據時區自動推播、批次控流、個人化排程) 仍需自行在伺服器端建立中介層處理。

- 訊息大小與頻率限制

    FCM 對推播訊息有一定限制

    - 單則訊息最大 4KB (Data Message)

    - 通知內容與圖片等需額外壓縮

    - 若推播過於頻繁可能導致被系統抑制或使用者關閉通知

    因此不適合用於大量資料傳輸。

| 分類 | 優點 | 缺點 |
| - | - | - |
| 成本 | 免費使用 | 無法控制伺服器端穩定度 |
| 平台支援 | 跨 Android/iOS/Web | iOS 功能受限 |
| 整合性 | 可搭配 Firebase 工具 | 無法客製後端 |
| 彈性 | 支援主題、條件、群組推播 | 無法支援無 GMS 的裝置 |
| 傳遞機制 | 具重送與離線補送機制 | 無法保證即時性 |
| 控制性 | 支援自訂 Data Message | 訊息大小有限制 |

簡單來說，FCM 是中小型專案與一般應用的首選推播解決方案。

FCM 擁有免費、易整合、跨平台與穩定的優點，非常適合用於

- 行銷通知

- 一般系統公告

- 訂單、狀態更新

若應用程式需要

- 極低延遲 (即時通訊)

- 對後端完全掌控 (自訂佇列或流量控管)

- 在無 Google 服務環境運作 (例如：中國市場)

此時可考慮採用自建推播服務 (例如：使用 MQTT、WebSocket 或第三方推播平台)。

<br />

## 總結

Firebase Cloud Messaging (FCM) 是一個穩定、彈性且跨平台的推播解決方案。

透過簡單的 API 及與 Firebase 生態系的整合，開發人員不僅能節省建置通知系統的成本，更能快速擴充應用服務的互動性。無論是行動應用程式、網頁或桌面平台，FCM 都能作為即時溝通與行銷推播的核心工具。

對多數開發人員而言，FCM 不僅是推播解決方案，更是串接使用者互動與雲端服務的重要基礎建設。
