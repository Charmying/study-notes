# Space-Based Architecture (空間型架構)

Space-Based Architecture (空間型架構) 是一種分散式架構模式，專為處理高併發、高可用性和可擴展性需求而設計。這種架構通過消除中央資料庫瓶頸，將資料和處理功能分散到多個處理單元中。

這種架構模式特別適合需要處理大量並發用戶請求的應用程式，例如：電商平台、線上遊戲、金融交易系統等。

<br />

## 動機

在傳統的分層架構中，常見的問題包括

- 資料庫成為系統瓶頸，限制整體效能

- 單點故障風險，資料庫或應用伺服器故障影響整個系統

- 擴展困難，垂直擴展成本高且有限制

- 高併發情況下回應時間變長

Space-Based Architecture 通過以下方式解決這些問題

- 消除中央資料庫依賴，將資料分散到記憶體中

- 水平擴展，根據負載動態增減處理單元

- 高可用性，單個處理單元故障不影響整體系統

- 近乎線性的效能擴展能力

<br />

## 結構

Space-Based Architecture 由以下核心元件組成

### 1. Processing Unit (處理單元)

包含應用程式碼和記憶體內資料網格的自包含單元。

- 包含業務功能和相關資料

- 可獨立部署和擴展

- 通常是無狀態的

### 2. Virtualized Middleware (虛擬化中介軟體)

管理和協調處理單元的基礎設施。

- 負載平衡和路由

- 處理單元的生命週期管理

- 監控和自動擴展

### 3. Data Pumps (資料幫浦)

負責在記憶體網格和持久化儲存之間同步資料。

- 非同步資料同步

- 資料一致性維護

- 批次處理優化

### 4. Data Writers (資料寫入器)

將記憶體中的資料寫入持久化儲存。

- 批次寫入優化

- 錯誤處理和重試機制

- 資料格式轉換

### 5. Data Readers (資料讀取器)

從持久化儲存讀取資料到記憶體網格。

- 快取預熱

- 資料載入策略

- 效能優化

以下是 Space-Based Architecture 的結構圖

```text
┌───────────────────────────────────────────────────────────┐
│                      Load Balancer                        │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────┐
│                  Virtualized Middleware                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Processing  │  │ Processing  │  │ Processing  │        │
│  │   Unit 1    │  │   Unit 2    │  │   Unit N    │        │
│  │             │  │             │  │             │        │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │   ...  │
│  │ │ Memory  │ │  │ │ Memory  │ │  │ │ Memory  │ │        │
│  │ │  Grid   │ │  │ │  Grid   │ │  │ │  Grid   │ │        │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────┐
│                        Data Pumps                         │
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│     │ Data Reader │  │ Data Writer │  │ Data Sync   │     │
│     └─────────────┘  └─────────────┘  └─────────────┘     │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────┐
│                  Persistent Data Store                    │
└───────────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 記憶體優先 (Memory-First)

所有活躍資料都保存在記憶體中，提供最快的存取速度。

### 分散式處理 (Distributed Processing)

處理功能分散到多個獨立的處理單元中。

### 動態擴展 (Dynamic Scaling)

根據負載自動增減處理單元數量。

### 最終一致性 (Eventual Consistency)

接受短期的資料不一致，換取更好的效能和可用性。

<br />

## 實現方式

### Java 實現範例

以線上購物車系統為例

- Processing Unit (處理單元)

    ```java
    /** 購物車處理單元 */
    @Component
    public class ShoppingCartProcessingUnit {
        private final InMemoryDataGrid dataGrid;
        private final CartService cartService;
        private final EventPublisher eventPublisher;

        public ShoppingCartProcessingUnit(
            InMemoryDataGrid dataGrid,
            CartService cartService,
            EventPublisher eventPublisher
        ) {
            this.dataGrid = dataGrid;
            this.cartService = cartService;
            this.eventPublisher = eventPublisher;
        }

        public CartResponse addItem(String userId, AddItemRequest request) {
            /** 從記憶體網格獲取購物車 */
            Cart cart = dataGrid.get("cart:" + userId, Cart.class)
                .orElse(new Cart(userId));

            /** 添加商品到購物車 */
            cart.addItem(request.getProductId(), request.getQuantity());

            /** 更新記憶體網格 */
            dataGrid.put("cart:" + userId, cart);

            /** 發布事件 */
            eventPublisher.publish(new CartUpdatedEvent(userId, cart));

            return CartResponse.from(cart);
        }

        public CartResponse getCart(String userId) {
            Cart cart = dataGrid.get("cart:" + userId, Cart.class)
                .orElse(new Cart(userId));
            return CartResponse.from(cart);
        }
    }
    ```

- In-Memory Data Grid (記憶體資料網格)

    ```java
    /** 記憶體資料網格介面 */
    public interface InMemoryDataGrid {
        <T> Optional<T> get(String key, Class<T> type);
        <T> void put(String key, T value);
        void remove(String key);
        boolean exists(String key);
    }

    /** Hazelcast 實現 */
    @Service
    public class HazelcastDataGrid implements InMemoryDataGrid {
        private final HazelcastInstance hazelcastInstance;

        public HazelcastDataGrid(HazelcastInstance hazelcastInstance) {
            this.hazelcastInstance = hazelcastInstance;
        }

        @Override
        public <T> Optional<T> get(String key, Class<T> type) {
            IMap<String, T> map = hazelcastInstance.getMap("data-grid");
            T value = map.get(key);
            return Optional.ofNullable(value);
        }

        @Override
        public <T> void put(String key, T value) {
            IMap<String, T> map = hazelcastInstance.getMap("data-grid");
            map.put(key, value);
        }

        @Override
        public void remove(String key) {
            IMap<String, Object> map = hazelcastInstance.getMap("data-grid");
            map.remove(key);
        }
    }
    ```

- Data Pump (資料幫浦)

    ```java
    /** 資料同步服務 */
    @Service
    public class CartDataPump {
        private final InMemoryDataGrid dataGrid;
        private final CartRepository cartRepository;
        private final EventListener eventListener;

        @EventHandler
        public void handleCartUpdated(CartUpdatedEvent event) {
            /** 非同步寫入資料庫 */
            CompletableFuture.runAsync(() -> {
                try {
                    Cart cart = event.getCart();
                    cartRepository.save(cart);
                } catch (Exception e) {
                    /** 錯誤處理和重試 */
                    handleSyncError(event, e);
                }
            });
        }

        @Scheduled(fixedDelay = 30000) /** 每30秒執行一次 */
        public void syncPendingData() {
            /** 批次同步待處理的資料 */
            List<String> pendingKeys = getPendingKeys();

            for (String key : pendingKeys) {
                try {
                    syncDataToDatabase(key);
                } catch (Exception e) {
                    /** 記錄錯誤，稍後重試 */
                    logSyncError(key, e);
                }
            }
        }

        private void syncDataToDatabase(String key) {
            Optional<Cart> cart = dataGrid.get(key, Cart.class);
            if (cart.isPresent()) {
                cartRepository.save(cart.get());
            }
        }
    }
    ```

### Node.js 實現範例

- Processing Unit (處理單元)

    ```typescript
    /** 用戶會話處理單元 */
    export class UserSessionProcessingUnit {
      constructor(
        private readonly dataGrid: InMemoryDataGrid,
        private readonly eventBus: EventBus
      ) {}

      async createSession(userId: string, deviceInfo: DeviceInfo): Promise<SessionResponse> {
        /** 檢查現有會話 */
        const existingSession = await this.dataGrid.get(`session:${userId}`);
        if (existingSession) {
          await this.invalidateSession(userId);
        }

        /** 建立新會話 */
        const session = new UserSession({
          userId,
          sessionId: generateSessionId(),
          deviceInfo,
          createdAt: new Date(),
          lastActivity: new Date()
        });

        /** 儲存到記憶體網格 */
        await this.dataGrid.set(`session:${userId}`, session, { ttl: 3600 });

        /** 發布事件 */
        await this.eventBus.publish('session.created', {
          userId,
          sessionId: session.sessionId,
          timestamp: new Date()
        });

        return {
          sessionId: session.sessionId,
          expiresAt: session.expiresAt
        };
      }

      async updateActivity(userId: string): Promise<void> {
        const session = await this.dataGrid.get(`session:${userId}`);
        if (!session) {
          throw new Error('會話不存在');
        }

        session.lastActivity = new Date();
        await this.dataGrid.set(`session:${userId}`, session, { ttl: 3600 });

        /** 發布活動事件 */
        await this.eventBus.publish('session.activity', {
          userId,
          sessionId: session.sessionId,
          timestamp: new Date()
        });
      }
    }
    ```

- Data Grid (資料網格)

    ```typescript
    /** 記憶體資料網格介面 */
    export interface InMemoryDataGrid {
      get<T>(key: string): Promise<T | null>;
      set<T>(key: string, value: T, options?: { ttl?: number }): Promise<void>;
      delete(key: string): Promise<boolean>;
      exists(key: string): Promise<boolean>;
    }

    /** Redis 實現 */
    export class RedisDataGrid implements InMemoryDataGrid {
      constructor(private readonly redis: Redis) {}

      async get<T>(key: string): Promise<T | null> {
        const value = await this.redis.get(key);
        return value ? JSON.parse(value) : null;
      }

      async set<T>(key: string, value: T, options?: { ttl?: number }): Promise<void> {
        const serialized = JSON.stringify(value);
        if (options?.ttl) {
          await this.redis.setex(key, options.ttl, serialized);
        } else {
          await this.redis.set(key, serialized);
        }
      }

      async delete(key: string): Promise<boolean> {
        const result = await this.redis.del(key);
        return result > 0;
      }

      async exists(key: string): Promise<boolean> {
        const result = await this.redis.exists(key);
        return result === 1;
      }
    }
    ```

- Virtualized Middleware (虛擬化中介軟體)

    ```typescript
    /** 負載平衡器 */
    export class ProcessingUnitLoadBalancer {
      private processingUnits: ProcessingUnitInfo[] = [];
      private currentIndex = 0;

      constructor(
        private readonly healthChecker: HealthChecker,
        private readonly scaler: AutoScaler
      ) {
        this.startHealthChecking();
        this.startAutoScaling();
      }

      async routeRequest(request: Request): Promise<ProcessingUnitInfo> {
        const availableUnits = this.processingUnits.filter(unit => unit.isHealthy);

        if (availableUnits.length === 0) {
          throw new Error('沒有可用的處理單元');
        }

        /** 輪詢負載平衡 */
        const selectedUnit = availableUnits[this.currentIndex % availableUnits.length];
        this.currentIndex++;

        /** 更新負載統計 */
        selectedUnit.requestCount++;
        selectedUnit.lastRequestTime = new Date();

        return selectedUnit;
      }

      private async startHealthChecking(): Promise<void> {
        setInterval(async () => {
          for (const unit of this.processingUnits) {
            unit.isHealthy = await this.healthChecker.check(unit.endpoint);
          }
        }, 10000); /** 每10秒檢查一次 */
      }

      private async startAutoScaling(): Promise<void> {
        setInterval(async () => {
          const metrics = this.calculateMetrics();

          if (metrics.averageLoad > 0.8) {
            /** 負載過高，擴展處理單元 */
            await this.scaler.scaleOut();
          } else if (metrics.averageLoad < 0.3 && this.processingUnits.length > 1) {
            /** 負載過低，縮減處理單元 */
            await this.scaler.scaleIn();
          }
        }, 60000); /** 每分鐘檢查一次 */
      }

      private calculateMetrics(): LoadMetrics {
        const totalRequests = this.processingUnits.reduce(
          (sum, unit) => sum + unit.requestCount, 0
        );
        const averageLoad = totalRequests / this.processingUnits.length;

        return { averageLoad, totalRequests };
      }
    }
    ```

### React 前端實現範例

- Real-time Data Sync (即時資料同步)

    ```typescript
    /** 即時資料同步 Hook */
    export const useRealTimeData = <T>(key: string, initialData?: T) => {
      const [data, setData] = useState<T | undefined>(initialData);
      const [isLoading, setIsLoading] = useState(true);
      const [error, setError] = useState<Error | null>(null);
      const wsRef = useRef<WebSocket | null>(null);

      useEffect(() => {
        /** 建立 WebSocket 連接 */
        const ws = new WebSocket(`ws://localhost:8080/realtime/${key}`);
        wsRef.current = ws;

        ws.onopen = () => {
          console.log(`已連接到 ${key} 的即時資料流`);
          setIsLoading(false);
        };

        ws.onmessage = (event) => {
          try {
            const updatedData = JSON.parse(event.data);
            setData(updatedData);
            setError(null);
          } catch (err) {
            setError(new Error('資料解析錯誤'));
          }
        };

        ws.onerror = (event) => {
          setError(new Error('WebSocket 連接錯誤'));
          setIsLoading(false);
        };

        ws.onclose = () => {
          console.log(`${key} 的即時資料流已斷開`);
          /** 嘗試重新連接 */
          setTimeout(() => {
            if (wsRef.current?.readyState === WebSocket.CLOSED) {
              /** 重新建立連接 */
            }
          }, 5000);
        };

        return () => {
          ws.close();
        };
      }, [key]);

      const updateData = useCallback((newData: Partial<T>) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(JSON.stringify({
            type: 'update',
            key,
            data: newData
          }));
        }
      }, [key]);

      return { data, isLoading, error, updateData };
    };
    ```

- Distributed State Management (分散式狀態管理)

    ```typescript
    /** 分散式購物車元件 */
    export const DistributedShoppingCart: React.FC<{ userId: string }> = ({ userId }) => {
      const { data: cart, updateData } = useRealTimeData<ShoppingCart>(`cart:${userId}`);
      const [isUpdating, setIsUpdating] = useState(false);

      const addItem = async (productId: string, quantity: number) => {
        setIsUpdating(true);
        try {
          /** 樂觀更新 */
          const optimisticCart = {
            ...cart,
            items: [
              ...(cart?.items || []),
              { productId, quantity, addedAt: new Date() }
            ]
          };

          /** 立即更新 UI */
          updateData(optimisticCart);

          /** 發送到處理單元 */
          await fetch('/api/cart/add-item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId, productId, quantity })
          });
        } catch (error) {
          /** 錯誤時回滾 */
          console.error('添加商品失敗:', error);
          /** 這裡可以實現錯誤回滾功能 */
        } finally {
          setIsUpdating(false);
        }
      };

      const removeItem = async (productId: string) => {
        setIsUpdating(true);
        try {
          /** 樂觀更新 */
          const optimisticCart = {
            ...cart,
            items: cart?.items?.filter(item => item.productId !== productId) || []
          };

          updateData(optimisticCart);

          await fetch('/api/cart/remove-item', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId, productId })
          });
        } catch (error) {
          console.error('移除商品失敗:', error);
        } finally {
          setIsUpdating(false);
        }
      };

      if (!cart) {
        return <div>載入購物車中...</div>;
      }

      return (
        <div className="shopping-cart">
          <h2>購物車 ({cart.items?.length || 0} 件商品)</h2>

          {cart.items?.map((item) => (
            <div key={item.productId} className="cart-item">
              <span>商品 ID: {item.productId}</span>
              <span>數量: {item.quantity}</span>
              <button 
                onClick={() => removeItem(item.productId)}
                disabled={isUpdating}
              >
                移除
              </button>
            </div>
          ))}

          <div className="cart-actions">
            <button 
              onClick={() => addItem('sample-product', 1)}
              disabled={isUpdating}
            >
              {isUpdating ? '處理中...' : '添加範例商品'}
            </button>
          </div>
        </div>
      );
    };
    ```

<br />

## 優點

### 高效能

記憶體內處理提供極快的回應時間。

### 高可擴展性

- 水平擴展：可以動態增加處理單元

- 近乎線性的效能提升

- 自動負載平衡

### 高可用性

- 無單點故障

- 處理單元獨立運作

- 自動故障轉移

### 彈性部署

可以根據需求動態調整資源配置。

<br />

## 缺點

### 複雜性

架構複雜，需要專業的分散式系統知識。

### 資料一致性

最終一致性模型可能不適合所有應用場景。

### 記憶體成本

需要大量記憶體來儲存資料，成本較高。

### 資料持久化挑戰

需要複雜的資料同步機制來確保資料不遺失。

### 除錯困難

分散式環境下的問題診斷和除錯較為困難。

<br />

## 適用場景

### 適合使用

- 高併發應用：需要處理大量並發請求

- 即時系統：線上遊戲、即時交易、聊天應用

- 電商平台：購物車、庫存管理、促銷活動

- 金融系統：高頻交易、風險計算

- IoT 應用：大量感測器資料處理

### 不適合使用

- 強一致性需求：需要 ACID 特性的應用

- 簡單應用：CRUD 操作為主的系統

- 資源受限環境：記憶體或網路頻寬有限

- 複雜事務：需要跨多個資源的複雜事務

<br />

## 實施建議

### 技術選型

選擇合適的記憶體網格技術，例如：Hazelcast、Apache Ignite、Redis Cluster。

### 資料分割策略

設計合理的資料分割和分散策略，避免熱點問題。

### 監控和觀測

建立完整的監控系統，追蹤效能指標和系統健康狀況。

### 災難恢復

制定資料備份和災難恢復計畫，確保資料安全。

### 漸進式遷移

從非關鍵功能開始，逐步遷移到 Space-Based Architecture。

<br />

## 與其他架構的比較

### vs 微服務架構

- Space-Based 更注重記憶體內處理和水平擴展

- 微服務更注重業務功能的分離和獨立部署

### vs 事件驅動架構

- Space-Based 主要解決效能和擴展性問題

- 事件驅動主要解決系統解耦和非同步處理

### vs 傳統分層架構

- Space-Based 消除了資料庫瓶頸

- 傳統架構更簡單但擴展性有限

<br />

## 總結

Space-Based Architecture 是一種專為高併發、高效能需求設計的架構模式。通過將資料和處理功能分散到記憶體中，這種架構能夠提供優異的效能和擴展性。

雖然實施複雜度較高，但對於需要處理大量並發請求的應用程式來說，Space-Based Architecture 能夠提供傳統架構無法達到的效能水準。關鍵在於評估應用程式的實際需求，權衡效能收益與實施成本。

在選擇這種架構時，需要考慮團隊的技術能力、資源預算，以及對資料一致性的要求。對於合適的應用場景，Space-Based Architecture 能夠帶來顯著的競爭優勢。
