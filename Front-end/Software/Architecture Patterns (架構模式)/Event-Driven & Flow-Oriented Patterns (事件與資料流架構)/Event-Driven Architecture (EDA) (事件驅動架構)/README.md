# Event-Driven Architecture (EDA) (事件驅動架構)

Event-Driven Architecture (事件驅動架構) 是一種軟體架構模式，系統中的元件透過產生、偵測、消費和回應事件來進行通訊。

這種架構強調鬆散耦合，當某個事件發生時，相關的元件會自動回應，而不需要直接呼叫或依賴其他元件。

<br />

## 動機

在傳統的同步架構中，常見的問題包括

- 元件之間緊密耦合，一個元件的變更影響其他元件

- 系統難以擴展，新增功能需要修改現有程式碼

- 處理高併發和大量資料時效能不佳

- 系統容錯性差，一個元件失敗可能導致整個系統停止

Event-Driven Architecture 通過事件機制，解決這些問題，讓系統具備

- 鬆散耦合：元件之間透過事件通訊，不直接依賴

- 可擴展性：可以輕鬆新增事件處理器

- 高效能：支援非同步處理和並行執行

- 容錯性：單一元件失敗不影響其他元件

<br />

## 結構

Event-Driven Architecture 主要包含以下核心元件

### 1. Event (事件)

表示系統中發生的重要狀態變化或動作。

- 包含事件類型、時間戳記和相關資料

- 不可變的資料結構

- 具有明確的業務意義

### 2. Event Producer (事件產生器)

負責產生和發布事件的元件。

- 偵測狀態變化或業務動作

- 建立事件物件

- 將事件發布到事件匯流排

### 3. Event Consumer (事件消費者)

訂閱和處理特定類型事件的元件。

- 監聽感興趣的事件類型

- 執行相應的業務處理

- 可能產生新的事件

### 4. Event Bus (事件匯流排)

負責事件路由和傳遞的中介層。

- 接收來自產生器的事件

- 將事件路由到相關的消費者

- 提供事件持久化和重試機制

以下是 Event-Driven Architecture 的結構圖

```text
┌─────────────────┐    Events    ┌─────────────────┐    Events    ┌─────────────────┐
│  Event Producer │ ──────────►  │   Event Bus     │ ──────────►  │ Event Consumer  │
│                 │              │                 │              │                 │
│ - User Service  │              │ - Message Queue │              │ - Email Service │
│ - Order Service │              │ - Event Store   │              │ - Audit Service │
│ - Payment Svc   │              │ - Event Router  │              │ - Analytics Svc │
└─────────────────┘              └─────────────────┘              └─────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  Event Storage  │
                                 │                 │
                                 │ - Event History │
                                 │ - Event Replay  │
                                 │ - Event Sourcing│
                                 └─────────────────┘
```

<br />

## 核心原則

### 事件優先 (Event-First)

系統設計以事件為中心，所有重要的狀態變化都透過事件表達。

### 鬆散耦合 (Loose Coupling)

事件產生器和消費者之間沒有直接依賴關係。

### 非同步處理 (Asynchronous Processing)

事件處理通常是非同步的，提升系統效能和回應性。

<br />

## 實現方式

### Java 實現範例

以電商系統的訂單處理為例

- Event 定義

    ```java
    /** 基礎事件介面 */
    public interface DomainEvent {
        String getEventId();
        LocalDateTime getOccurredAt();
        String getEventType();
    }

    /** 訂單建立事件 */
    public class OrderCreatedEvent implements DomainEvent {
        private final String eventId;
        private final LocalDateTime occurredAt;
        private final String orderId;
        private final String customerId;
        private final BigDecimal totalAmount;
        private final List<OrderItem> items;

        public OrderCreatedEvent(String orderId, String customerId, 
                               BigDecimal totalAmount, List<OrderItem> items) {
            this.eventId = UUID.randomUUID().toString();
            this.occurredAt = LocalDateTime.now();
            this.orderId = orderId;
            this.customerId = customerId;
            this.totalAmount = totalAmount;
            this.items = items;
        }

        @Override
        public String getEventType() {
            return "OrderCreated";
        }

        // getters...
    }
    ```

- Event Producer (事件產生器)

    ```java
    /** 事件發布器介面 */
    public interface EventPublisher {
        void publish(DomainEvent event);
    }

    /** 訂單服務 */
    @Service
    public class OrderService {
        private final OrderRepository orderRepository;
        private final EventPublisher eventPublisher;

        public OrderService(OrderRepository orderRepository, 
                          EventPublisher eventPublisher) {
            this.orderRepository = orderRepository;
            this.eventPublisher = eventPublisher;
        }

        public Order createOrder(CreateOrderRequest request) {
            /** 建立訂單 */
            Order order = new Order(
                request.getCustomerId(),
                request.getItems()
            );

            /** 儲存訂單 */
            Order savedOrder = orderRepository.save(order);

            /** 發布事件 */
            OrderCreatedEvent event = new OrderCreatedEvent(
                savedOrder.getId(),
                savedOrder.getCustomerId(),
                savedOrder.getTotalAmount(),
                savedOrder.getItems()
            );
            eventPublisher.publish(event);

            return savedOrder;
        }
    }
    ```

- Event Consumer (事件消費者)

    ```java
    /** 郵件服務 */
    @Component
    public class EmailNotificationHandler {
        private final EmailService emailService;
        private final CustomerRepository customerRepository;

        @EventListener
        public void handleOrderCreated(OrderCreatedEvent event) {
            try {
                Customer customer = customerRepository
                    .findById(event.getCustomerId())
                    .orElseThrow(() -> new CustomerNotFoundException());

                emailService.sendOrderConfirmation(
                    customer.getEmail(),
                    event.getOrderId(),
                    event.getTotalAmount()
                );
            } catch (Exception e) {
                /** 記錄錯誤，但不影響其他處理器 */
                log.error("發送訂單確認郵件失敗", e);
            }
        }
    }

    /** 庫存服務 */
    @Component
    public class InventoryHandler {
        private final InventoryService inventoryService;

        @EventListener
        public void handleOrderCreated(OrderCreatedEvent event) {
            try {
                for (OrderItem item : event.getItems()) {
                    inventoryService.reserveStock(
                        item.getProductId(),
                        item.getQuantity()
                    );
                }
            } catch (Exception e) {
                log.error("庫存預留失敗", e);
                /** 可以發布庫存不足事件 */
            }
        }
    }
    ```

- Event Bus 實現

    ```java
    /** Spring 事件發布器實現 */
    @Component
    public class SpringEventPublisher implements EventPublisher {
        private final ApplicationEventPublisher applicationEventPublisher;

        public SpringEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
            this.applicationEventPublisher = applicationEventPublisher;
        }

        @Override
        public void publish(DomainEvent event) {
            applicationEventPublisher.publishEvent(event);
        }
    }

    /** 訊息佇列事件發布器 */
    @Component
    public class MessageQueueEventPublisher implements EventPublisher {
        private final RabbitTemplate rabbitTemplate;

        @Override
        public void publish(DomainEvent event) {
            rabbitTemplate.convertAndSend(
                "events.exchange",
                event.getEventType(),
                event
            );
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Event 定義

    ```typescript
    /** 基礎事件介面 */
    export interface DomainEvent {
      eventId: string;
      eventType: string;
      occurredAt: Date;
      version: number;
    }

    /** 使用者註冊事件 */
    export class UserRegisteredEvent implements DomainEvent {
      public readonly eventId: string;
      public readonly eventType = 'UserRegistered';
      public readonly occurredAt: Date;
      public readonly version = 1;

      constructor(
        public readonly userId: string,
        public readonly email: string,
        public readonly name: string
      ) {
        this.eventId = crypto.randomUUID();
        this.occurredAt = new Date();
      }
    }
    ```

- Event Producer (事件產生器)

    ```typescript
    /** 事件發布器介面 */
    export interface EventPublisher {
      publish(event: DomainEvent): Promise<void>;
    }

    /** 使用者服務 */
    export class UserService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly eventPublisher: EventPublisher
      ) {}

      async registerUser(request: RegisterUserRequest): Promise<User> {
        /** 建立使用者 */
        const user = new User(
          generateId(),
          request.email,
          request.name
        );

        /** 儲存使用者 */
        const savedUser = await this.userRepository.save(user);

        /** 發布事件 */
        const event = new UserRegisteredEvent(
          savedUser.getId(),
          savedUser.getEmail(),
          savedUser.getName()
        );
        await this.eventPublisher.publish(event);

        return savedUser;
      }
    }
    ```

- Event Consumer (事件消費者)

    ```typescript
    /** 事件處理器介面 */
    export interface EventHandler<T extends DomainEvent> {
      handle(event: T): Promise<void>;
      getEventType(): string;
    }

    /** 歡迎郵件處理器 */
    export class WelcomeEmailHandler implements EventHandler<UserRegisteredEvent> {
      constructor(private readonly emailService: EmailService) {}

      getEventType(): string {
        return 'UserRegistered';
      }

      async handle(event: UserRegisteredEvent): Promise<void> {
        try {
          await this.emailService.sendWelcomeEmail(
            event.email,
            event.name
          );
        } catch (error) {
          console.error('發送歡迎郵件失敗:', error);
        }
      }
    }

    /** 使用者統計處理器 */
    export class UserAnalyticsHandler implements EventHandler<UserRegisteredEvent> {
      constructor(private readonly analyticsService: AnalyticsService) {}

      getEventType(): string {
        return 'UserRegistered';
      }

      async handle(event: UserRegisteredEvent): Promise<void> {
        try {
          await this.analyticsService.trackUserRegistration({
            userId: event.userId,
            email: event.email,
            registeredAt: event.occurredAt
          });
        } catch (error) {
          console.error('記錄使用者統計失敗:', error);
        }
      }
    }
    ```

- Event Bus 實現

    ```typescript
    /** 記憶體事件匯流排 */
    export class InMemoryEventBus implements EventPublisher {
      private handlers = new Map<string, EventHandler<any>[]>();

      registerHandler<T extends DomainEvent>(handler: EventHandler<T>): void {
        const eventType = handler.getEventType();
        if (!this.handlers.has(eventType)) {
          this.handlers.set(eventType, []);
        }
        this.handlers.get(eventType)!.push(handler);
      }

      async publish(event: DomainEvent): Promise<void> {
        const handlers = this.handlers.get(event.eventType) || [];

        /** 並行處理所有處理器 */
        const promises = handlers.map(handler => 
          handler.handle(event).catch(error => {
            console.error(`事件處理失敗 ${event.eventType}:`, error);
          })
        );

        await Promise.all(promises);
      }
    }

    /** Redis 事件匯流排 */
    export class RedisEventBus implements EventPublisher {
      constructor(private readonly redisClient: Redis) {}

      async publish(event: DomainEvent): Promise<void> {
        await this.redisClient.publish(
          `events:${event.eventType}`,
          JSON.stringify(event)
        );
      }

      subscribe<T extends DomainEvent>(
        eventType: string,
        handler: EventHandler<T>
      ): void {
        this.redisClient.subscribe(`events:${eventType}`);
        this.redisClient.on('message', async (channel, message) => {
          if (channel === `events:${eventType}`) {
            try {
              const event = JSON.parse(message) as T;
              await handler.handle(event);
            } catch (error) {
              console.error('事件處理失敗:', error);
            }
          }
        });
      }
    }
    ```

### React 前端實現範例

- Event 系統

    ```typescript
    /** 前端事件定義 */
    export interface UIEvent {
      type: string;
      payload: any;
      timestamp: number;
    }

    /** 使用者動作事件 */
    export class UserActionEvent implements UIEvent {
      public readonly timestamp: number;

      constructor(
        public readonly type: string,
        public readonly payload: any
      ) {
        this.timestamp = Date.now();
      }
    }
    ```

- Event Bus Hook

    ```typescript
    /** React 事件匯流排 Hook */
    export const useEventBus = () => {
      const [events, setEvents] = useState<UIEvent[]>([]);
      const handlersRef = useRef<Map<string, Function[]>>(new Map());

      const subscribe = useCallback((eventType: string, handler: Function) => {
        const handlers = handlersRef.current;
        if (!handlers.has(eventType)) {
          handlers.set(eventType, []);
        }
        handlers.get(eventType)!.push(handler);

        /** 回傳取消訂閱函數 */
        return () => {
          const eventHandlers = handlers.get(eventType);
          if (eventHandlers) {
            const index = eventHandlers.indexOf(handler);
            if (index > -1) {
              eventHandlers.splice(index, 1);
            }
          }
        };
      }, []);

      const publish = useCallback((event: UIEvent) => {
        setEvents(prev => [...prev, event]);

        const handlers = handlersRef.current.get(event.type) || [];
        handlers.forEach(handler => {
          try {
            handler(event);
          } catch (error) {
            console.error('事件處理失敗:', error);
          }
        });
      }, []);

      return { subscribe, publish, events };
    };
    ```

- 元件實現

    ```typescript
    /** 購物車元件 */
    export const ShoppingCart: React.FC = () => {
      const [items, setItems] = useState<CartItem[]>([]);
      const { subscribe, publish } = useEventBus();

      useEffect(() => {
        /** 訂閱商品新增事件 */
        const unsubscribe = subscribe('PRODUCT_ADDED_TO_CART', (event: UIEvent) => {
          const { product, quantity } = event.payload;
          setItems(prev => [
            ...prev,
            { id: product.id, name: product.name, quantity, price: product.price }
          ]);
        });

        return unsubscribe;
      }, [subscribe]);

      const handleCheckout = () => {
        /** 發布結帳事件 */
        publish(new UserActionEvent('CHECKOUT_INITIATED', {
          items,
          total: items.reduce((sum, item) => sum + item.price * item.quantity, 0)
        }));
      };

      return (
        <div className="shopping-cart">
          <h2>購物車</h2>
          {items.map(item => (
            <div key={item.id} className="cart-item">
              <span>{item.name}</span>
              <span>數量: {item.quantity}</span>
              <span>價格: ${item.price}</span>
            </div>
          ))}
          <button onClick={handleCheckout}>結帳</button>
        </div>
      );
    };

    /** 商品列表元件 */
    export const ProductList: React.FC = () => {
      const [products] = useState<Product[]>(mockProducts);
      const { publish } = useEventBus();

      const handleAddToCart = (product: Product) => {
        /** 發布商品新增事件 */
        publish(new UserActionEvent('PRODUCT_ADDED_TO_CART', {
          product,
          quantity: 1
        }));
      };

      return (
        <div className="product-list">
          {products.map(product => (
            <div key={product.id} className="product-item">
              <h3>{product.name}</h3>
              <p>價格: ${product.price}</p>
              <button onClick={() => handleAddToCart(product)}>
                加入購物車
              </button>
            </div>
          ))}
        </div>
      );
    };
    ```

<br />

## 優點

### 鬆散耦合

元件之間透過事件通訊，不需要直接依賴，提升系統的靈活性。

### 可擴展性

- 新增功能：可以輕鬆新增事件處理器

- 水平擴展：可以部署多個事件處理器實例

- 垂直擴展：可以針對特定事件類型優化處理

### 高效能

- 非同步處理：不阻塞主要業務流程

- 並行處理：多個處理器可以同時處理事件

- 負載分散：事件可以分散到不同的處理器

### 容錯性

單一事件處理器失敗不會影響其他處理器或主要業務流程。

<br />

## 缺點

### 複雜性

事件流程可能難以追蹤和除錯，特別是在複雜的事件鏈中。

### 一致性挑戰

非同步處理可能導致資料一致性問題。

### 事件順序

難以保證事件的處理順序，可能需要額外的機制。

### 效能開銷

事件的序列化、傳輸和反序列化會帶來額外的效能開銷。

<br />

## 適用場景

### 適合使用

- 微服務架構：服務之間需要鬆散耦合的通訊

- 高併發系統：需要處理大量並發請求

- 複雜業務流程：涉及多個步驟和多個系統

- 即時系統：需要即時回應和處理

- 審計和監控：需要記錄所有重要的業務事件

### 不適合使用

- 簡單 CRUD 應用：業務流程簡單，不需要複雜的事件處理

- 強一致性要求：需要嚴格的資料一致性

- 同步處理需求：業務流程必須同步完成

- 小型單體應用：系統規模小，不需要複雜的架構

<br />

## 實施建議

### 事件設計

- 事件應該表達業務意義，而不是技術實現

- 事件應該包含足夠的資訊，避免處理器需要額外查詢

- 事件應該是不可變的

### 錯誤處理

- 實現重試機制處理暫時性錯誤

- 使用死信佇列處理無法處理的事件

- 記錄詳細的錯誤資訊便於除錯

### 監控和觀測

- 監控事件的產生和處理速度

- 追蹤事件處理的成功率和錯誤率

- 實現分散式追蹤來追蹤事件流程

### 測試策略

- 單元測試：測試個別的事件處理器

- 整合測試：測試事件的端到端流程

- 契約測試：確保事件格式的相容性

<br />

## 總結

Event-Driven Architecture 提供了一個強大的架構模式來建構鬆散耦合、高效能和可擴展的系統。特別適合需要處理複雜業務流程和高併發的應用程式。

雖然實施上有一定的複雜性，但對於需要高度靈活性和可擴展性的系統來說，這種架構模式能夠帶來顯著的價值。關鍵在於正確設計事件、選擇合適的事件匯流排技術，以及建立完善的監控和錯誤處理機制。
