# WebSocket

在現代的網路應用中，「即時性」已成為使用者體驗中不可或缺的一環。從線上客服、即時股價、多人遊戲、聊天室，到即時通知系統，這些功能都需要網頁與伺服器能夠雙向、即時交換資料，WebSocket 就是能夠實現這項能力的核心技術之一。

<br />

## WebSocket 簡介

WebSocket 是一種在 TCP 之上運作的全雙工 (full-duplex) 通訊協定，可讓瀏覽器與伺服器之間建立一條持續開放的連線，也就是說，雙方都能主動發送資料，而不必像 HTTP 那樣只能由瀏覽器發出請求、伺服器回應。

簡單來說，WebSocket 就是一條持續開放、可雙向傳輸資料的通道。

WebSocket 通訊協定由 IETF 在 2011 年制定為 RFC 6455，而其在瀏覽器端的 API 介面則由 W3C 定義。

<br />

## 為什麼需要 WebSocket

傳統的 HTTP 通訊採「請求－回應 (Request-Response)」模式

1. 使用者動作觸發請求。

2. 伺服器回傳結果。

3. 連線關閉。

若想讓伺服器主動通知使用者 (例如：新訊息提醒)，傳統上可透過以下方式模擬「即時性」

- 輪詢 (Polling)：瀏覽器定期發送請求檢查是否有更新。

    缺點：浪費頻寬與伺服器資源。

- 長輪詢 (Long Polling)：瀏覽器發送請求後，伺服器延遲回應直到有新資料。

    改善即時性，但仍存在延遲與高負載問題。

相較之下，WebSocket 則能

- 建立持久連線 (Persistent Connection)

- 實現即時資料推播 (Real-time Push)

- 減少網路與伺服器負擔

因此，WebSocket 成為現代即時應用的主流解決方案。

<br />

## WebSocket 的運作原理

以下是 WebSocket 連線建立的基本過程

1. 交握階段 (Handshake)

    WebSocket 建立於 TCP 協定之上，因此能保證資料傳輸的可靠性與順序性。

    WebSocket 仍以 HTTP 為基礎發起一次初始請求

    ```http
    GET /chat HTTP/1.1
    Host: example.com
    Upgrade: websocket
    Connection: Upgrade
    Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
    Sec-WebSocket-Version: 13
    ```

    伺服器確認支援後，會回應

    ```http
    HTTP/1.1 101 Switching Protocols
    Upgrade: websocket
    Connection: Upgrade
    Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
    ```

    此時，連線從 HTTP 升級為 WebSocket 通訊，這個升級請求仍然經由 HTTP/1.1 傳送，因此能穿越防火牆與代理伺服器，這也是 WebSocket 被廣泛採用的原因之一。

    交握成功後，HTTP 連線會被『升級』為 WebSocket 通道，後續資料以二進位框架 (Frame) 傳輸，而非 HTTP 封包。這些框架可分為文字訊息與二進位訊息，並透過 Opcode 進行區分。

2. 雙向通訊階段

    連線建立後，雙方可以使用同一條 TCP 通道自由交換訊息，不需再每次建立新請求。

    - 瀏覽器可立即發送資料給伺服器。

    - 伺服器也能主動推播訊息給使用者。

3. 關閉連線 (Close)

    任一方可透過 `close` 訊息結束連線，另一方會回應確認。

<br />

## WebSocket 的主要特點

| 特點 | 說明 |
| - | - |
| 全雙工通訊 | 瀏覽器與伺服器可以同時傳送與接收資料，無需等待 |
| 長連線 | 連線建立後可持續存在，減少重複建立 HTTP 連線的開銷 |
| 低延遲 | 不需要等待伺服器回應輪詢請求，資料能即時傳送 |
| 節省頻寬 | 握手後的資料傳輸不再需要額外的 HTTP 標頭，封包更輕量 |
| 支援雙向事件驅動 | 伺服器可以主動推送資料給客戶端 |
| 自訂協定與資料格式 | WebSocket 傳輸內容可自訂 (例如：JSON、二進位、Protobuf)，讓開發人員能根據需求優化效能 |

<br />

## WebSocket 的應用場景

WebSocket 適合各種需要即時更新的應用，例如

| 應用場景 | 說明 |
| - | - |
| 即時聊天系統 | 雙向傳訊、訊息同步 |
| 線上遊戲 | 玩家狀態與遊戲事件即時傳遞 |
| 股票報價與加密貨幣交易 | 即時顯示市場變化 |
| 協作編輯 (例如：Google Docs) | 文件同步更新 |
| 即時通知系統 | 系統狀態或警示即時推播 |
| IoT 裝置監控 | 透過即時連線接收感測器或設備狀態資料 |

<br />

## WebSocket 的生活化舉例

假設在使用一個線上聊天室

    - 傳統的 HTTP 模式下，瀏覽器每隔幾秒就會問伺服器：「有新訊息嗎？」(這就是輪詢)。

    - 使用 WebSocket 時，只要連線建立，伺服器就能即時推送新訊息，而發送的訊息也會立即傳給其他使用者。

        整體反應速度就像使用 LINE 或 Messenger 一樣流暢，幾乎感受不到延遲，這正是 WebSocket 所帶來的使用者體驗差異。

<br />

## WebSocket 的前後端基本實作範例

- 前端 (JavaScript)

    ```javascript
    const socket = new WebSocket("wss://example.com/socket");

    socket.onopen = () => {
      console.log("已連線");
      socket.send("Hello Server!");
    };

    socket.onmessage = (event) => {
      console.log("伺服器回覆：", event.data);
    };

    socket.onclose = () => {
      console.log("連線關閉");
    };

    socket.onerror = (error) => {
      console.error("連線發生錯誤：", error);
    };
    ```

- 後端 (Node.js + ws 套件)

    ```javascript
    import { WebSocketServer } from "ws";

    const wss = new WebSocketServer({ port: 8080 });

    wss.on("connection", (ws) => {
      console.log("用戶已連線");

      ws.on("message", (msg) => {
        console.log("收到訊息：", msg.toString());
        ws.send("伺服器已收到訊息！");
      });

      ws.on("close", () => console.log("連線已關閉"));
    });
    ```

<br />

## WebSocket 與其他技術的比較

| 技術 | 特性 | 是否雙向 | 即時性 | 資源消耗 |
| - | - | - | - | - |
| HTTP Polling | 定期請求更新 | 否 | 差 | 高 |
| HTTP Long Polling | 等待更新後才回應 | 否 | 中等 | 中等 |
| WebSocket | 單一持久連線 | 是 | 優 | 低 |
| SSE (Server-Sent Events) | 僅支援伺服器 → 客戶端的單向傳輸，若需要雙向互動仍須結合其他機制 | 否 | 優 | 低 |

<br />

## 安全性與加密

WebSocket 同樣支援加密版本

`ws://`：未加密連線 (例如：HTTP)

`wss://`：加密連線 (例如：HTTPS)

由於 WebSocket 通常使用 80 (`ws`) 或 443 (`wss`) 埠口，因此能穿越大部分防火牆與 Proxy，不需額外設定。

在實際應用中，建議一律使用 `wss://`，以確保資料安全與防止竊聽攻擊。

除了加密連線之外，開發人員也應搭配認證與授權機制 (例如：JWT、API Token)，以防止惡意用戶利用持久連線進行未授權操作。WebSocket 同樣受同源政策影響，因此跨網域使用時需設定正確的 CORS 或 Origin 驗證。

<br />

## 限制與注意事項

- 連線數限制：大量使用者同時連線時，伺服器需妥善管理資源 (例如：使用連線池或分散式架構)。

- 中斷重連機制：若使用者網路不穩，需自行實作自動重連功能。

- 瀏覽器與 Proxy 相容性：部分公司內網的代理伺服器可能封鎖 WebSocket，需要特別配置。

- 後端擴充性：在大型系統中，通常需結合訊息中介軟體 (例如：Redis、Kafka) 來分散即時訊息。

- 快取限制：由於 WebSocket 為持續連線協定，無法使用傳統 HTTP 快取機制，因此若需降低負載，應在伺服器端自行實作資料緩存策略。

- 心跳機制 (Ping/Pong)：WebSocket 長時間連線可能因防火牆或網路設備中斷，實務上可透過定時 `ping/pong` 訊息來檢測連線是否仍然存活，並在斷線時自動重連。

<br />

## 總結

WebSocket 的出現讓網頁不再只是被動顯示資料的載體，而能成為即時互動、低延遲的應用平台，無論是聊天系統、即時監控，或是金融交易服務，都能提供穩定且高效的通訊能力。

隨著前端框架與後端技術的成熟，WebSocket 早已成為建構現代互動式網頁應用不可或缺的基礎技術之一，而在 WebSocket 的基礎上，也衍生出更高層的即時通訊框架，例如：Socket.IO、SignalR 等，讓開發人員能更輕鬆打造穩定的即時應用。
