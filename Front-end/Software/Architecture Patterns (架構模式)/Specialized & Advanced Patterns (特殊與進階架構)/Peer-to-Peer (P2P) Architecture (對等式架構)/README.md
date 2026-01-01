# Peer-to-Peer (P2P) Architecture (對等式架構)

Peer-to-Peer (P2P) Architecture (對等式架構) 是一種分散式網路架構模式，其中每個節點 (peer) 既是客戶端也是伺服器，能夠直接與其他節點通訊和共享資源。

這種架構消除了傳統客戶端-伺服器模式中的中央伺服器依賴，讓每個參與者都能平等參與網路運作，提供更好的可擴展性、容錯性和資源利用率。

<br />

## 動機

在傳統的客戶端-伺服器架構中，常見的問題包括

- 中央伺服器成為單點故障，影響整個系統可用性

- 伺服器資源限制導致擴展性瓶頸

- 頻寬和運算成本集中在少數伺服器上

- 中央控制帶來的審查和隱私問題

P2P Architecture 通過分散式設計，解決這些問題，讓系統具備

- 去中心化：沒有單點故障

- 可擴展性：節點數量增加時性能提升

- 資源共享：充分利用參與者的資源

- 抗審查性：難以被單一實體控制或關閉

<br />

## 結構

P2P Architecture 根據網路拓撲和組織方式，可分為三種主要類型

### 1. Pure P2P (純對等式)

所有節點地位完全平等，沒有任何中央協調機制。

- 完全去中心化

- 節點自主發現和連接

- 最高的容錯性

- 實現複雜度最高

### 2. Hybrid P2P (混合式)

結合 P2P 和客戶端-伺服器模式，使用中央伺服器協助節點發現。

- 中央索引伺服器協助節點發現

- 實際資料傳輸在節點間進行

- 平衡了效率和去中心化

- 仍存在中央伺服器依賴

### 3. Structured P2P (結構化)

使用分散式雜湊表 (DHT) 等演算法組織網路拓撲。

- 基於數學演算法的網路結構

- 高效的資源定位和路由

- 可預測的性能特性

- 適合大規模網路

以下是 P2P 網路的結構圖

```text
           純對等式 P2P

    ┌────────┐    ┌────────┐
    │ Node A │ ←→ │ Node B │
    └────────┘    └────────┘
         ↕            ↕
    ┌────────┐    ┌────────┐
    │ Node C │ ←→ │ Node D │
    └────────┘    └────────┘
         ↕            ↕
    ┌────────┐    ┌────────┐
    │ Node E │ ←→ │ Node F │
    └────────┘    └────────┘



                  混合式 P2P

              ┌────────────────┐
              │ Central Server │
              └────────────────┘
                      ↕
    ┌────────┐    ┌────────┐    ┌────────┐
    │ Node A │ ←→ │ Node B │ ←→ │ Node C │
    └────────┘    └────────┘    └────────┘
         ↕                        ↕
    ┌────────┐    ┌────────┐     ┌────────┐
    │ Node D │ ←→ │ Node E │ ←→ │ Node F │
    └────────┘    └────────┘     └────────┘



             結構化 P2P (DHT Ring)

    ┌────────┐   ┌────────┐   ┌────────┐
    │ Node A │ → │ Node B │ → │ Node C │
    └────────┘   └────────┘   └────────┘
         ↑                      ↓
    ┌────────┐   ┌────────┐   ┌────────┐
    │ Node F │ ← │ Node E │ ← │ Node D │
    └────────┘   └────────┘   └────────┘

```

<br />

## 核心原則

### 對等性 (Equality)

所有節點在網路中具有相同的地位和能力。

### 自主性 (Autonomy)

每個節點可以獨立決定參與程度和行為。

### 分散式控制 (Distributed Control)

沒有中央權威控制整個網路。

### 資源共享 (Resource Sharing)

節點貢獻自身資源並使用其他節點的資源。

<br />

## 實現方式

### Node.js WebRTC 實現範例

以檔案分享系統為例

- 節點基礎結構

    ```javascript
    /** P2P 節點基礎類別 */
    class P2PNode {
      constructor(nodeId) {
        this.nodeId = nodeId;
        this.peers = new Map();
        this.files = new Map();
        this.connections = new Map();
      }

      /** 連接到其他節點 */
      async connectToPeer(peerId, signalData) {
        const peer = new RTCPeerConnection({
          iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
        });

        /** 設定資料通道 */
        const dataChannel = peer.createDataChannel('fileShare', {
          ordered: true
        });

        dataChannel.onopen = () => {
          console.log(`連接到節點 ${peerId}`);
          this.connections.set(peerId, dataChannel);
        };

        dataChannel.onmessage = (event) => {
          this.handleMessage(peerId, JSON.parse(event.data));
        };

        this.peers.set(peerId, peer);
        return peer;
      }

      /** 處理接收到的訊息 */
      handleMessage(fromPeer, message) {
        switch (message.type) {
          case 'FILE_REQUEST':
            this.handleFileRequest(fromPeer, message.fileHash);
            break;
          case 'FILE_RESPONSE':
            this.handleFileResponse(message.fileData);
            break;
          case 'PEER_LIST':
            this.updatePeerList(message.peers);
            break;
        }
      }

      /** 分享檔案 */
      shareFile(fileName, fileData) {
        const fileHash = this.calculateHash(fileData);
        this.files.set(fileHash, {
          name: fileName,
          data: fileData,
          size: fileData.length
        });

        /** 廣播檔案可用性 */
        this.broadcastMessage({
          type: 'FILE_AVAILABLE',
          fileHash,
          fileName,
          fileSize: fileData.length
        });
      }

      /** 請求檔案 */
      async requestFile(fileHash, fromPeer) {
        const connection = this.connections.get(fromPeer);
        if (connection) {
          connection.send(JSON.stringify({
            type: 'FILE_REQUEST',
            fileHash
          }));
        }
      }

      /** 處理檔案請求 */
      handleFileRequest(fromPeer, fileHash) {
        const file = this.files.get(fileHash);
        if (file) {
          const connection = this.connections.get(fromPeer);
          connection.send(JSON.stringify({
            type: 'FILE_RESPONSE',
            fileData: file.data,
            fileName: file.name
          }));
        }
      }

      /** 廣播訊息給所有連接的節點 */
      broadcastMessage(message) {
        this.connections.forEach((connection) => {
          if (connection.readyState === 'open') {
            connection.send(JSON.stringify(message));
          }
        });
      }

      calculateHash(data) {
        return require('crypto')
          .createHash('sha256')
          .update(data)
          .digest('hex');
      }
    }
    ```

- DHT 實現

    ```javascript
    /** 分散式雜湊表實現 */
    class DistributedHashTable {
      constructor(nodeId, keySpace = 160) {
        this.nodeId = nodeId;
        this.keySpace = keySpace;
        this.routingTable = new Map();
        this.storage = new Map();
      }

      /** 計算節點間距離 */
      calculateDistance(nodeId1, nodeId2) {
        const hash1 = this.hash(nodeId1);
        const hash2 = this.hash(nodeId2);
        return hash1 ^ hash2;
      }

      /** 尋找最接近的節點 */
      findClosestNodes(targetId, count = 3) {
        const distances = Array.from(this.routingTable.entries())
          .map(([nodeId, nodeInfo]) => ({
            nodeId,
            nodeInfo,
            distance: this.calculateDistance(targetId, nodeId)
          }))
          .sort((a, b) => a.distance - b.distance)
          .slice(0, count);

        return distances.map(item => item.nodeInfo);
      }

      /** 儲存鍵值對 */
      async store(key, value) {
        const targetNodes = this.findClosestNodes(key);

        /** 在本地儲存 */
        this.storage.set(key, value);

        /** 複製到最接近的節點 */
        const storePromises = targetNodes.map(async (node) => {
          try {
            await this.sendStoreRequest(node, key, value);
          } catch (error) {
            console.error(`儲存到節點 ${node.id} 失敗:`, error);
          }
        });

        await Promise.allSettled(storePromises);
      }

      /** 查找值 */
      async lookup(key) {
        /** 先檢查本地儲存 */
        if (this.storage.has(key)) {
          return this.storage.get(key);
        }

        /** 向最接近的節點查詢 */
        const targetNodes = this.findClosestNodes(key);

        for (const node of targetNodes) {
          try {
            const value = await this.sendLookupRequest(node, key);
            if (value !== null) {
              return value;
            }
          } catch (error) {
            console.error(`從節點 ${node.id} 查詢失敗:`, error);
          }
        }

        return null;
      }

      /** 加入新節點到路由表 */
      addNode(nodeId, nodeInfo) {
        this.routingTable.set(nodeId, nodeInfo);
      }

      /** 移除節點 */
      removeNode(nodeId) {
        this.routingTable.delete(nodeId);
      }

      hash(data) {
        return require('crypto')
          .createHash('sha1')
          .update(data.toString())
          .digest('hex');
      }
    }
    ```

### Python BitTorrent-like 實現範例

- Tracker 伺服器 (混合式 P2P)

    ```python
    """BitTorrent-like Tracker 伺服器"""
    import asyncio
    import json
    from datetime import datetime, timedelta
    from typing import Dict, Set, List

    class Tracker:
        def __init__(self):
            self.torrents: Dict[str, Dict] = {}
            self.peers: Dict[str, Dict] = {}

        async def announce(self, info_hash: str, peer_id: str, 
                          ip: str, port: int, event: str = None) -> Dict:
            """處理節點通告"""

            # 更新節點資訊
            peer_key = f"{ip}:{port}"
            self.peers[peer_key] = {
                'peer_id': peer_id,
                'ip': ip,
                'port': port,
                'last_seen': datetime.now()
            }

            # 初始化種子資訊
            if info_hash not in self.torrents:
                self.torrents[info_hash] = {
                    'peers': set(),
                    'seeders': set(),
                    'leechers': set()
                }

            torrent = self.torrents[info_hash]

            # 處理事件
            if event == 'started':
                torrent['leechers'].add(peer_key)
            elif event == 'completed':
                torrent['leechers'].discard(peer_key)
                torrent['seeders'].add(peer_key)
            elif event == 'stopped':
                torrent['peers'].discard(peer_key)
                torrent['seeders'].discard(peer_key)
                torrent['leechers'].discard(peer_key)

            torrent['peers'].add(peer_key)

            # 清理過期節點
            await self.cleanup_expired_peers()

            # 回傳節點清單
            peer_list = self.get_peer_list(info_hash, peer_key)

            return {
                'interval': 1800, # 30 分鐘
                'peers': peer_list,
                'complete': len(torrent['seeders']),
                'incomplete': len(torrent['leechers'])
            }

        def get_peer_list(self, info_hash: str, requesting_peer: str, 
                         max_peers: int = 50) -> List[Dict]:
            """取得節點清單"""
            if info_hash not in self.torrents:
                return []

            torrent = self.torrents[info_hash]
            available_peers = torrent['peers'] - {requesting_peer}

            # 限制回傳的節點數量
            selected_peers = list(available_peers)[:max_peers]

            peer_list = []
            for peer_key in selected_peers:
                if peer_key in self.peers:
                    peer_info = self.peers[peer_key]
                    peer_list.append({
                        'ip': peer_info['ip'],
                        'port': peer_info['port'],
                        'peer_id': peer_info['peer_id']
                    })

            return peer_list

        async def cleanup_expired_peers(self):
            """清理過期節點"""
            cutoff_time = datetime.now() - timedelta(hours=2)
            expired_peers = []

            for peer_key, peer_info in self.peers.items():
                if peer_info['last_seen'] < cutoff_time:
                    expired_peers.append(peer_key)

            for peer_key in expired_peers:
                del self.peers[peer_key]

                # 從所有種子中移除過期節點
                for torrent in self.torrents.values():
                    torrent['peers'].discard(peer_key)
                    torrent['seeders'].discard(peer_key)
                    torrent['leechers'].discard(peer_key)
    ```

- P2P 客戶端

    ```python
    """P2P 檔案分享客戶端"""
    import asyncio
    import hashlib
    import struct
    from typing import Dict, List, Optional

    class P2PClient:
        def __init__(self, peer_id: str, port: int):
            self.peer_id = peer_id
            self.port = port
            self.connections: Dict[str, asyncio.StreamWriter] = {}
            self.files: Dict[str, bytes] = {}
            self.downloading: Dict[str, Dict] = {}

        async def start_server(self):
            """啟動 P2P 伺服器"""
            server = await asyncio.start_server(
                self.handle_peer_connection, 
                '0.0.0.0', 
                self.port
            )
            print(f"P2P 伺服器啟動於 port {self.port}")
            await server.serve_forever()

        async def handle_peer_connection(self, reader: asyncio.StreamReader, 
                                       writer: asyncio.StreamWriter):
            """處理節點連接"""
            try:
                while True:
                    # 讀取訊息長度
                    length_data = await reader.read(4)
                    if not length_data:
                        break

                    message_length = struct.unpack('>I', length_data)[0]

                    # 讀取訊息內容
                    message_data = await reader.read(message_length)
                    message = json.loads(message_data.decode())

                    await self.handle_message(message, writer)

            except Exception as e:
                print(f"處理節點連接錯誤: {e}")
            finally:
                writer.close()
                await writer.wait_closed()

        async def handle_message(self, message: Dict, writer: asyncio.StreamWriter):
            """處理接收到的訊息"""
            msg_type = message.get('type')

            if msg_type == 'REQUEST_FILE':
                await self.handle_file_request(message, writer)
            elif msg_type == 'FILE_CHUNK':
                await self.handle_file_chunk(message)
            elif msg_type == 'HANDSHAKE':
                await self.handle_handshake(message, writer)

        async def handle_file_request(self, message: Dict, writer: asyncio.StreamWriter):
            """處理檔案請求"""
            file_hash = message.get('file_hash')
            chunk_index = message.get('chunk_index', 0)

            if file_hash in self.files:
                file_data = self.files[file_hash]
                chunk_size = 16384 # 16KB chunks
                start = chunk_index * chunk_size
                end = min(start + chunk_size, len(file_data))
                chunk_data = file_data[start:end]

                response = {
                    'type': 'FILE_CHUNK',
                    'file_hash': file_hash,
                    'chunk_index': chunk_index,
                    'chunk_data': chunk_data.hex(),
                    'total_chunks': (len(file_data) + chunk_size - 1) // chunk_size
                }

                await self.send_message(response, writer)

        async def connect_to_peer(self, ip: str, port: int) -> Optional[asyncio.StreamWriter]:
            """連接到其他節點"""
            try:
                reader, writer = await asyncio.open_connection(ip, port)

                # 發送握手訊息
                handshake = {
                    'type': 'HANDSHAKE',
                    'peer_id': self.peer_id,
                    'port': self.port
                }

                await self.send_message(handshake, writer)
                return writer

            except Exception as e:
                print(f"連接到 {ip}:{port} 失敗: {e}")
                return None

        async def download_file(self, file_hash: str, peers: List[Dict]):
            """從多個節點下載檔案"""
            self.downloading[file_hash] = {
                'chunks': {},
                'total_chunks': None,
                'completed': False
            }

            # 連接到所有可用節點
            connections = []
            for peer in peers:
                writer = await self.connect_to_peer(peer['ip'], peer['port'])
                if writer:
                    connections.append(writer)

            if not connections:
                print("無法連接到任何節點")
                return None

            # 並行下載不同區塊
            chunk_index = 0
            tasks = []

            for writer in connections:
                task = asyncio.create_task(
                    self.download_chunks(file_hash, writer, chunk_index)
                )
                tasks.append(task)
                chunk_index += 1

            # 等待下載完成
            await asyncio.gather(*tasks, return_exceptions=True)

            # 組合檔案
            if self.downloading[file_hash]['completed']:
                return self.assemble_file(file_hash)

            return None

        async def download_chunks(self, file_hash: str, writer: asyncio.StreamWriter, 
                                start_chunk: int):
            """下載檔案區塊"""
            chunk_index = start_chunk

            while not self.downloading[file_hash]['completed']:
                # 檢查是否已有此區塊
                if chunk_index in self.downloading[file_hash]['chunks']:
                    chunk_index += len(self.connections)
                    continue

                # 請求區塊
                request = {
                    'type': 'REQUEST_FILE',
                    'file_hash': file_hash,
                    'chunk_index': chunk_index
                }

                await self.send_message(request, writer)
                chunk_index += len(self.connections)

                await asyncio.sleep(0.1) # 避免過於頻繁的請求

        def assemble_file(self, file_hash: str) -> bytes:
            """組合檔案區塊"""
            download_info = self.downloading[file_hash]
            chunks = download_info['chunks']
            total_chunks = download_info['total_chunks']

            if len(chunks) != total_chunks:
                return None

            # 按順序組合區塊
            file_data = b''
            for i in range(total_chunks):
                if i in chunks:
                    file_data += chunks[i]
                else:
                    return None

            # 儲存完整檔案
            self.files[file_hash] = file_data
            return file_data

        async def send_message(self, message: Dict, writer: asyncio.StreamWriter):
            """發送訊息"""
            message_data = json.dumps(message).encode()
            length_data = struct.pack('>I', len(message_data))

            writer.write(length_data + message_data)
            await writer.drain()

        def add_file(self, file_path: str) -> str:
            """新增檔案到分享清單"""
            with open(file_path, 'rb') as f:
                file_data = f.read()

            file_hash = hashlib.sha256(file_data).hexdigest()
            self.files[file_hash] = file_data

            return file_hash
    ```

### TypeScript WebRTC 實現範例

- 即時通訊系統

    ```typescript
    /** P2P 即時通訊節點 */
    export class P2PChatNode {
      private peers: Map<string, RTCPeerConnection> = new Map();
      private dataChannels: Map<string, RTCDataChannel> = new Map();
      private messageHistory: ChatMessage[] = [];
      private onMessageCallback?: (message: ChatMessage) => void;

      constructor(private nodeId: string) {}

      /** 建立與其他節點的連接 */
      async connectToPeer(peerId: string, isInitiator: boolean = false): Promise<void> {
        const peerConnection = new RTCPeerConnection({
          iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' }
          ]
        });

        this.peers.set(peerId, peerConnection);

        if (isInitiator) {
          const dataChannel = peerConnection.createDataChannel('chat', {
            ordered: true
          });
          this.setupDataChannel(peerId, dataChannel);
        } else {
          peerConnection.ondatachannel = (event) => {
            this.setupDataChannel(peerId, event.channel);
          };
        }

        peerConnection.onicecandidate = (event) => {
          if (event.candidate) {
            this.sendSignalingMessage(peerId, {
              type: 'ice-candidate',
              candidate: event.candidate
            });
          }
        };

        if (isInitiator) {
          const offer = await peerConnection.createOffer();
          await peerConnection.setLocalDescription(offer);

          this.sendSignalingMessage(peerId, {
            type: 'offer',
            offer: offer
          });
        }
      }

      /** 設定資料通道 */
      private setupDataChannel(peerId: string, dataChannel: RTCDataChannel): void {
        this.dataChannels.set(peerId, dataChannel);

        dataChannel.onopen = () => {
          console.log(`與節點 ${peerId} 的連接已建立`);
          this.syncMessageHistory(peerId);
        };

        dataChannel.onmessage = (event) => {
          const message: P2PMessage = JSON.parse(event.data);
          this.handleMessage(peerId, message);
        };

        dataChannel.onclose = () => {
          console.log(`與節點 ${peerId} 的連接已關閉`);
          this.dataChannels.delete(peerId);
        };
      }

      /** 處理接收到的訊息 */
      private handleMessage(fromPeer: string, message: P2PMessage): void {
        switch (message.type) {
          case 'chat':
            this.handleChatMessage(message as ChatMessage);
            break;
          case 'sync-request':
            this.handleSyncRequest(fromPeer);
            break;
          case 'sync-response':
            this.handleSyncResponse(message.messages);
            break;
          case 'peer-list':
            this.handlePeerListUpdate(message.peers);
            break;
        }
      }

      /** 發送聊天訊息 */
      sendChatMessage(content: string): void {
        const message: ChatMessage = {
          type: 'chat',
          id: this.generateMessageId(),
          senderId: this.nodeId,
          content,
          timestamp: Date.now()
        };

        this.messageHistory.push(message);
        this.broadcastMessage(message);

        if (this.onMessageCallback) {
          this.onMessageCallback(message);
        }
      }

      /** 處理聊天訊息 */
      private handleChatMessage(message: ChatMessage): void {
        /** 檢查是否已存在此訊息 */
        const exists = this.messageHistory.some(m => m.id === message.id);
        if (exists) return;

        this.messageHistory.push(message);
        this.messageHistory.sort((a, b) => a.timestamp - b.timestamp);

        /** 轉發給其他節點 */
        this.broadcastMessage(message, message.senderId);

        if (this.onMessageCallback) {
          this.onMessageCallback(message);
        }
      }

      /** 同步訊息歷史 */
      private syncMessageHistory(peerId: string): void {
        const dataChannel = this.dataChannels.get(peerId);
        if (dataChannel && dataChannel.readyState === 'open') {
          dataChannel.send(JSON.stringify({
            type: 'sync-request'
          }));
        }
      }

      /** 處理同步請求 */
      private handleSyncRequest(fromPeer: string): void {
        const dataChannel = this.dataChannels.get(fromPeer);
        if (dataChannel && dataChannel.readyState === 'open') {
          dataChannel.send(JSON.stringify({
            type: 'sync-response',
            messages: this.messageHistory
          }));
        }
      }

      /** 處理同步回應 */
      private handleSyncResponse(messages: ChatMessage[]): void {
        const newMessages = messages.filter(msg => 
          !this.messageHistory.some(existing => existing.id === msg.id)
        );

        this.messageHistory.push(...newMessages);
        this.messageHistory.sort((a, b) => a.timestamp - b.timestamp);

        newMessages.forEach(message => {
          if (this.onMessageCallback) {
            this.onMessageCallback(message);
          }
        });
      }

      /** 廣播訊息給所有連接的節點 */
      private broadcastMessage(message: P2PMessage, excludePeer?: string): void {
        this.dataChannels.forEach((dataChannel, peerId) => {
          if (peerId !== excludePeer && dataChannel.readyState === 'open') {
            dataChannel.send(JSON.stringify(message));
          }
        });
      }

      /** 處理信令訊息 */
      async handleSignalingMessage(fromPeer: string, message: SignalingMessage): Promise<void> {
        const peerConnection = this.peers.get(fromPeer);
        if (!peerConnection) return;

        switch (message.type) {
          case 'offer':
            await peerConnection.setRemoteDescription(message.offer);
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);

            this.sendSignalingMessage(fromPeer, {
              type: 'answer',
              answer: answer
            });
            break;

          case 'answer':
            await peerConnection.setRemoteDescription(message.answer);
            break;

          case 'ice-candidate':
            await peerConnection.addIceCandidate(message.candidate);
            break;
        }
      }

      /** 發送信令訊息 (需要外部信令伺服器) */
      private sendSignalingMessage(toPeer: string, message: SignalingMessage): void {
        /** 這裡需要透過信令伺服器發送 */
        /** 實際實現會依賴 WebSocket 或其他通訊方式 */
        console.log(`發送信令訊息給 ${toPeer}:`, message);
      }

      /** 設定訊息 Callback */
      onMessage(callback: (message: ChatMessage) => void): void {
        this.onMessageCallback = callback;
      }

      /** 取得連接的節點清單 */
      getConnectedPeers(): string[] {
        return Array.from(this.dataChannels.keys()).filter(peerId => 
          this.dataChannels.get(peerId)?.readyState === 'open'
        );
      }

      /** 斷開與特定節點的連接 */
      disconnectFromPeer(peerId: string): void {
        const dataChannel = this.dataChannels.get(peerId);
        const peerConnection = this.peers.get(peerId);

        if (dataChannel) {
          dataChannel.close();
          this.dataChannels.delete(peerId);
        }

        if (peerConnection) {
          peerConnection.close();
          this.peers.delete(peerId);
        }
      }

      private generateMessageId(): string {
        return `${this.nodeId}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      }
    }

    /** 訊息介面定義 */
    interface P2PMessage {
      type: string;
    }

    interface ChatMessage extends P2PMessage {
      type: 'chat';
      id: string;
      senderId: string;
      content: string;
      timestamp: number;
    }

    interface SignalingMessage {
      type: 'offer' | 'answer' | 'ice-candidate';
      offer?: RTCSessionDescriptionInit;
      answer?: RTCSessionDescriptionInit;
      candidate?: RTCIceCandidate;
    }
    ```

<br />

## 優點

### 可擴展性

隨著節點數量增加，整體網路容量和性能也會提升。

### 容錯性

沒有單點故障，部分節點離線不會影響整個網路運作。

### 成本效益

- 無需維護昂貴的中央伺服器基礎設施

- 頻寬和儲存成本分散到所有參與者

- 資源利用率更高

### 抗審查性

難以被單一實體控制或關閉，提供更好的資訊自由度。

### 隱私保護

資料直接在節點間傳輸，減少中間人監控的可能性。

<br />

## 缺點

### 複雜性

實現和維護比傳統客戶端-伺服器架構更複雜。

### 安全挑戰

- 難以驗證節點身份和資料完整性

- 容易受到惡意節點攻擊

- 需要複雜的信任機制

### 性能不穩定

網路性能依賴參與節點的品質和數量。

### 內容管理困難

難以控制和管理網路中的內容品質。

### NAT 穿透問題

家用網路的 NAT 和防火牆可能阻礙直接連接。

<br />

## 適用場景

### 適合使用

- 檔案分享系統：BitTorrent、IPFS

- 即時通訊：去中心化聊天應用

- 內容分發：影片串流、軟體更新

- 區塊鏈網路：加密貨幣、智能合約

- 協作平台：分散式版本控制、文件協作

- 物聯網：設備間直接通訊

### 不適合使用

- 需要強一致性的系統：銀行交易、庫存管理

- 高安全性要求：機密資料處理

- 低延遲需求：即時遊戲、高頻交易

- 內容審核嚴格：企業內部系統

<br />

## 實施建議

### 選擇合適的 P2P 模式

根據應用需求選擇純對等式、混合式或結構化 P2P。

### 實現安全機制

- 使用加密通訊保護資料傳輸

- 實現節點身份驗證機制

- 建立信譽系統防範惡意節點

### 處理 NAT 穿透

- 使用 STUN/TURN 伺服器協助連接建立

- 實現 UPnP 自動端口映射

- 提供中繼伺服器作為備用方案

### 優化網路拓撲

- 實現智能節點發現和選擇

- 維護最佳的連接數量

- 定期清理無效連接

### 監控和診斷

建立網路健康監控和問題診斷機制。

<br />

## 總結

P2P Architecture 提供了一種強大的分散式系統設計方法，特別適合需要高可擴展性、容錯性和去中心化特性的應用。雖然實現複雜度較高，但在適當的場景下能夠提供傳統架構無法達到的優勢。

關鍵在於根據具體需求選擇合適的 P2P 模式，並妥善處理安全性、性能和可用性等挑戰。隨著 WebRTC、區塊鏈等技術的發展，P2P 架構在現代應用中的重要性持續提升。
