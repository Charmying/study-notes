# OSI 七層模型

在電腦網路的世界中，資料從一台電腦傳送到另一台電腦，過程中會經過多種不同的處理和傳輸機制。為了方便理解與標準化網路設計，國際標準組織 (ISO) 於1977年提出、1984年標準化 (ISO 7498-1) 的 OSI (Open Systems Interconnection) 七層模型，將網路通訊過程分為七個層次，每層有特定功能，並只與上下相鄰層互動。相較於 TCP/IP 四層模型 (實務主流)，OSI 更細緻但較為理論化，廣泛用於教育與標準化互通。

<br />

## 七層模型概覽

OSI 模型由下到上分為七層

1. 實體層 (Physical Layer)

2. 資料鏈路層 (Data Link Layer)

3. 網路層 (Network Layer)

4. 傳輸層 (Transport Layer)

5. 會話層 (Session Layer)

6. 表示層 (Presentation Layer)

7. 應用層 (Application Layer)

這七層從最底層的「實體傳輸」到最上層的「應用服務」逐步抽象化，使網路通訊更有條理，也方便不同廠商的設備互通。

資料傳送時，發送端從上層往下層進行封裝 (Encapsulation)，接收端則從下層往上進行解封裝 (Decapsulation)，各層移除頭部 (Header) 並驗證。

以下為各層的協議資料單元 (PDU)

| 層級 | PDU 名稱 | 範例協議/功能 |
| - | - | - |
| 應用層 | Data | HTTP，FTP |
| 表示層 | Data | JPEG，SSL/TLS |
| 會話層 | Data | NetBIOS，RPC|
| 傳輸層 | Segment/Datagram | TCP，UDP |
| 網路層 | Packet | IP，ICMP|
| 資料鏈路層 | Frame| Ethernet，PPP |
| 實體層 | Bit | RJ-45，光纖 |

<br />

## 各層功能詳細解釋

### 1. 實體層 (Physical Layer)

- 主要功能：負責 Bit (0 和 1) 的實體傳輸。

- 內容：電纜、光纖、網路卡、集線器、無線電波 (例如：Wi-Fi，802.11)、RS-232。

- 安全機制：物理鎖、電磁屏蔽。

- 舉例：家中用網線連接路由器，或使用 Wi-Fi 無線網路。

- 補充：關注訊號的電壓、波形、頻率、速率，不關心資料內容。

- 重點：提供硬體層的訊號傳輸基礎。

### 2. 資料鏈路層 (Data Link Layer)

- 主要功能：負責點對點的資料傳輸，以及錯誤偵測與修正。

- 內容：MAC 位址、以太網框架 (Ethernet Frame，802.3)、交換器 (Switch)、ARP，分為 LLC (邏輯鏈路控制) 與 MAC (媒體存取控制) 子層。

- 安全機制：802.1X 認證。

- 舉例：資料在同一個區域網路 (LAN) 中傳送，確保框架正確送達。

- 補充：支援像是 PPP、HDLC 等協議，常用於 LAN 或點對點鏈路。

- 重點：確保單一網路段中的可靠傳輸。

### 3. 網路層 (Network Layer)

- 主要功能：負責資料從來源到目的的路由選擇。

- 內容：IP 位址 (IPv4/IPv6)、路由器 (Router)、封包 (Packet)、ICMP、OSPF/BGP。

- 安全機制：IPsec。

- 舉例：從台灣寄電子郵件到美國，網路層決定資料經過哪些路由器。

- 補充：處理分段 (Fragmentation) 與重組 (Reassembly)，支援 QoS (服務品質) 與 ICMP 錯誤報告。

- 重點：跨網段傳輸與路由控制。

### 4. 傳輸層 (Transport Layer)

- 主要功能：提供端到端通訊，確保資料可靠送達。

- 內容：TCP (可靠傳輸)、UDP (快速但不可靠)、SCTP、埠號 (Port Number)。

- 安全機制：TLS。

- 舉例：瀏覽網頁時，TCP 確保資料完整；視訊串流使用 UDP。

- 補充：TCP 使用三次握手 (Three-way Handshake) 建立連線，四次揮手 (Four-way Handshake) 結束連線；UDP 適用於低延遲場景，例如：遊戲。

- 重點：錯誤重傳、順序控制、流量控制。

### 5. 會話層 (Session Layer)

- 主要功能：管理應用程式之間的會話，包括建立、維護與結束連線。

- 內容：會話建立與同步 (例如：SIP、RPC)、控制對話權限。

- 安全機制：會話認證 (例如：Kerberos)。

- 舉例：線上會議軟體登入後建立會話，持續傳送訊息。

- 補充：在 TCP/IP 模型中，會話層功能常併入應用層 (例如：WebSocket、HTTP/2 的會話管理)。

- 重點：維護不同應用之間的資料交流狀態。

### 6. 表示層 (Presentation Layer)

- 主要功能：資料格式轉換、編碼、壓縮與加密。

- 內容：壓縮與解壓縮 (JPEG、ZIP)、編碼格式轉換 (ASCII、UTF-8、MIME)、加密傳輸 (SSL/TLS)、XDR。

- 安全機制：加密協議 (例如：AES)。

- 舉例：使用 HTTPS 瀏覽網頁時，表示層負責加密傳送。

- 補充：在 TCP/IP 模型中，部分功能被應用層直接處理。

- 重點：確保不同系統之間的資料能被正確理解。

### 7. 應用層 (Application Layer)

- 主要功能：提供最接近使用者的網路服務。

- 內容：HTTP/HTTPS、FTP/SFTP、SMTP/IMAP/POP3、DNS、SNMP、現代REST API、GraphQL、HTTP/3。

- 安全機制：應用層防火牆、OAuth。

- 舉例：使用瀏覽器打開網站、手機 App 查詢訊息。

- 補充：現代 Web API (例如：REST/GraphQL) 常跨層整合表示與會話功能。

- 重點：直接提供應用程式使用者所需的網路功能。

<br />

## 常見協議與應用對應表

| 層級 | 常見協議/技術 | 範例應用 |
| - | - | - |
| 實體層 | RS-232，Wi-Fi (802.11) | 網線連接 |
| 資料鏈路 | Ethernet (802.3)，ARP，PPP | LAN交換 |
| 網路層 | IPv4/IPv6，OSPF，BGP，ICMP| 網際網路路由 |
| 傳輸層 | TCP，UDP，SCTP | 網頁載入、視訊串流 |
| 會話層 | SIP，RPC，NetBIOS | 視訊會議登入 |
| 表示層 | ASCII，UTF-8，MIME，XDR | 資料加密/壓縮 |
| 應用層 | HTTP/3，DNS，SNMP，REST | 瀏覽器、郵件 |

<br />

## 總結

OSI 七層模型就像一棟高樓，每層有明確職責，從底層的物理傳輸到上層的應用服務，各層協同合作完成資料傳輸。理解這七層不僅是學術知識，也能幫助網路設計、故障排除與安全防護時快速定位問題。相較於 TCP/IP 模型，OSI 更理論化但促進標準化互通，實務中兩者常對照使用。
