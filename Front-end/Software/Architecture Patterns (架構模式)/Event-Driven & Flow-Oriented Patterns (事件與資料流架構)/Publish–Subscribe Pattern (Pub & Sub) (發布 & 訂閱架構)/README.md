# Publish–Subscribe Pattern (Pub & Sub) (發布 & 訂閱架構)

Publish–Subscribe Pattern (發布訂閱模式) 是一種訊息傳遞架構模式，發布者 (Publisher) 產生訊息並發布到特定主題 (Topic)，訂閱者 (Subscriber) 訂閱感興趣的主題並接收相關訊息。

這種架構實現了發布者與訂閱者之間的鬆耦合，發布者不需要知道訂閱者的存在，訂閱者也不需要知道發布者的具體實現。

<br />

## 動機

在分散式系統和事件驅動架構中，常見的問題包括

- 元件之間緊密耦合，難以獨立開發和部署

- 一對多通訊需要維護複雜的依賴關係

- 系統擴展時需要修改現有程式碼

- 異步處理和事件通知機制複雜

Publish–Subscribe Pattern 通過引入訊息中介者，解決這些問題，讓系統具備

- 鬆耦合：發布者與訂閱者互不依賴

- 可擴展性：新增訂閱者不影響現有系統

- 異步處理：支援非同步訊息傳遞

- 靈活性：動態訂閱和取消訂閱

<br />

## 結構

Publish–Subscribe Pattern 包含以下核心元件

### 1. Publisher (發布者)

負責產生和發布訊息到特定主題。

- 不知道訂閱者的存在

- 只關注訊息的發布

- 可以同時發布多個主題

### 2. Subscriber (訂閱者)

訂閱感興趣的主題並處理接收到的訊息。

- 不知道發布者的存在

- 可以訂閱多個主題

- 實現訊息處理功能

### 3. Message Broker (訊息代理)

負責管理主題、路由訊息和維護訂閱關係。

- 接收發布者的訊息

- 將訊息分發給相關訂閱者

- 管理訂閱和取消訂閱

### 4. Topic/Channel (主題/頻道)

訊息的分類標識，用於區分不同類型的訊息。

- 提供訊息分類機制

- 支援訂閱者選擇性接收

- 可以是階層式結構

以下是 Publish–Subscribe Pattern 的結構圖

```text
┌─────────────┐    publish    ┌─────────────────┐    deliver    ┌──────────────┐
│ Publisher A │──────────────>│                 │──────────────>│ Subscriber 1 │
└─────────────┘               │                 │               └──────────────┘
                              │ Message Broker  │
┌─────────────┐    publish    │                 │    deliver    ┌──────────────┐
│ Publisher B │──────────────>│  Topic/Channel  │──────────────>│ Subscriber 2 │
└─────────────┘               │                 │               └──────────────┘
                              │                 │
                              └─────────────────┘    deliver    ┌──────────────┐
                                                └──────────────>│ Subscriber 3 │
                                                                └──────────────┘
```

<br />

## 核心原則

### 鬆耦合 (Loose Coupling)

發布者與訂閱者之間沒有直接依賴關係，通過訊息代理進行通訊。

### 異步通訊 (Asynchronous Communication)

訊息發布和接收是異步進行的，不會阻塞發布者。

### 多對多關係 (Many-to-Many Relationship)

一個發布者可以有多個訂閱者，一個訂閱者可以訂閱多個主題。

<br />

## 實現方式

### Java 實現範例

以電商系統的訂單事件處理為例

- 事件定義

    ```java
    /** 基礎事件介面 */
    public interface Event {
        String getEventId();
        String getEventType();
        LocalDateTime getTimestamp();
    }

    /** 訂單事件 */
    public class OrderCreatedEvent implements Event {
        private final String eventId;
        private final String orderId;
        private final String customerId;
        private final BigDecimal amount;
        private final LocalDateTime timestamp;

        public OrderCreatedEvent(String orderId, String customerId, BigDecimal amount) {
            this.eventId = UUID.randomUUID().toString();
            this.orderId = orderId;
            this.customerId = customerId;
            this.amount = amount;
            this.timestamp = LocalDateTime.now();
        }

        @Override
        public String getEventType() {
            return "ORDER_CREATED";
        }

        // getters...
    }
    ```

- 發布者實現

    ```java
    /** 事件發布者介面 */
    public interface EventPublisher {
        void publish(String topic, Event event);
    }

    /** 訂單服務 (發布者) */
    @Service
    public class OrderService {
        private final EventPublisher eventPublisher;
        private final OrderRepository orderRepository;

        public OrderService(EventPublisher eventPublisher, OrderRepository orderRepository) {
            this.eventPublisher = eventPublisher;
            this.orderRepository = orderRepository;
        }

        public Order createOrder(CreateOrderRequest request) {
            Order order = new Order(request.getCustomerId(), request.getItems());
            Order savedOrder = orderRepository.save(order);

            /** 發布訂單建立事件 */
            OrderCreatedEvent event = new OrderCreatedEvent(
                savedOrder.getId(),
                savedOrder.getCustomerId(),
                savedOrder.getTotalAmount()
            );
            eventPublisher.publish("order.created", event);

            return savedOrder;
        }
    }
    ```

- 訂閱者實現

    ```java
    /** 事件處理器介面 */
    public interface EventHandler<T extends Event> {
        void handle(T event);
        String getEventType();
    }

    /** 庫存服務 (訂閱者) */
    @Component
    public class InventoryEventHandler implements EventHandler<OrderCreatedEvent> {
        private final InventoryService inventoryService;

        @Override
        public void handle(OrderCreatedEvent event) {
            try {
                inventoryService.reserveItems(event.getOrderId());
                System.out.println("庫存已預留: " + event.getOrderId());
            } catch (Exception e) {
                System.err.println("庫存預留失敗: " + e.getMessage());
            }
        }

        @Override
        public String getEventType() {
            return "ORDER_CREATED";
        }
    }

    /** 通知服務 (訂閱者) */
    @Component
    public class NotificationEventHandler implements EventHandler<OrderCreatedEvent> {
        private final EmailService emailService;

        @Override
        public void handle(OrderCreatedEvent event) {
            try {
                emailService.sendOrderConfirmation(event.getCustomerId(), event.getOrderId());
                System.out.println("訂單確認郵件已發送: " + event.getOrderId());
            } catch (Exception e) {
                System.err.println("郵件發送失敗: " + e.getMessage());
            }
        }

        @Override
        public String getEventType() {
            return "ORDER_CREATED";
        }
    }
    ```

- 訊息代理實現

    ```java
    /** 簡單的記憶體訊息代理 */
    @Component
    public class InMemoryEventBus implements EventPublisher {
        private final Map<String, List<EventHandler<? extends Event>>> subscribers = new ConcurrentHashMap<>();
        private final ExecutorService executorService = Executors.newCachedThreadPool();

        public void subscribe(String topic, EventHandler<? extends Event> handler) {
            subscribers.computeIfAbsent(topic, k -> new CopyOnWriteArrayList<>()).add(handler);
        }

        @Override
        public void publish(String topic, Event event) {
            List<EventHandler<? extends Event>> handlers = subscribers.get(topic);
            if (handlers != null) {
                for (EventHandler handler : handlers) {
                    if (handler.getEventType().equals(event.getEventType())) {
                        executorService.submit(() -> {
                            try {
                                handler.handle(event);
                            } catch (Exception e) {
                                System.err.println("事件處理失敗: " + e.getMessage());
                            }
                        });
                    }
                }
            }
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- 事件定義

    ```typescript
    /** 基礎事件介面 */
    export interface Event {
      eventId: string;
      eventType: string;
      timestamp: Date;
    }

    /** 使用者註冊事件 */
    export class UserRegisteredEvent implements Event {
      public readonly eventId: string;
      public readonly eventType = 'USER_REGISTERED';
      public readonly timestamp: Date;

      constructor(
        public readonly userId: string,
        public readonly email: string,
        public readonly name: string
      ) {
        this.eventId = crypto.randomUUID();
        this.timestamp = new Date();
      }
    }
    ```

- 發布者實現

    ```typescript
    /** 事件發布者介面 */
    export interface EventPublisher {
      publish(topic: string, event: Event): Promise<void>;
    }

    /** 使用者服務 (發布者) */
    export class UserService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly eventPublisher: EventPublisher
      ) {}

      async registerUser(userData: CreateUserData): Promise<User> {
        const user = new User(userData.email, userData.name);
        const savedUser = await this.userRepository.save(user);

        /** 發布使用者註冊事件 */
        const event = new UserRegisteredEvent(
          savedUser.getId(),
          savedUser.getEmail(),
          savedUser.getName()
        );
        await this.eventPublisher.publish('user.registered', event);

        return savedUser;
      }
    }
    ```

- 訂閱者實現

    ```typescript
    /** 事件處理器介面 */
    export interface EventHandler<T extends Event> {
      handle(event: T): Promise<void>;
      getEventType(): string;
    }

    /** 郵件服務 (訂閱者) */
    export class EmailEventHandler implements EventHandler<UserRegisteredEvent> {
      constructor(private readonly emailService: EmailService) {}

      async handle(event: UserRegisteredEvent): Promise<void> {
        try {
          await this.emailService.sendWelcomeEmail(event.email, event.name);
          console.log(`歡迎郵件已發送: ${event.email}`);
        } catch (error) {
          console.error('郵件發送失敗:', error);
        }
      }

      getEventType(): string {
        return 'USER_REGISTERED';
      }
    }

    /** 分析服務 (訂閱者) */
    export class AnalyticsEventHandler implements EventHandler<UserRegisteredEvent> {
      constructor(private readonly analyticsService: AnalyticsService) {}

      async handle(event: UserRegisteredEvent): Promise<void> {
        try {
          await this.analyticsService.trackUserRegistration(event.userId);
          console.log(`使用者註冊已記錄: ${event.userId}`);
        } catch (error) {
          console.error('分析記錄失敗:', error);
        }
      }

      getEventType(): string {
        return 'USER_REGISTERED';
      }
    }
    ```

- 訊息代理實現

    ```typescript
    /** Node.js EventEmitter 為基礎的訊息代理 */
    export class NodeEventBus implements EventPublisher {
      private readonly eventEmitter = new EventEmitter();
      private readonly handlers = new Map<string, EventHandler<any>[]>();

      subscribe<T extends Event>(topic: string, handler: EventHandler<T>): void {
        if (!this.handlers.has(topic)) {
          this.handlers.set(topic, []);
        }
        this.handlers.get(topic)!.push(handler);

        this.eventEmitter.on(topic, async (event: T) => {
          if (handler.getEventType() === event.eventType) {
            try {
              await handler.handle(event);
            } catch (error) {
              console.error('事件處理失敗:', error);
            }
          }
        });
      }

      async publish(topic: string, event: Event): Promise<void> {
        this.eventEmitter.emit(topic, event);
      }
    }
    ```

### React 前端實現範例

- 事件系統

    ```typescript
    /** 前端事件介面 */
    export interface UIEvent {
      type: string;
      payload: any;
      timestamp: number;
    }

    /** 購物車事件 */
    export class CartItemAddedEvent implements UIEvent {
      public readonly type = 'CART_ITEM_ADDED';
      public readonly timestamp = Date.now();

      constructor(public readonly payload: { productId: string; quantity: number }) {}
    }
    ```

- React Hook 實現

    ```typescript
    /** 事件匯流排 Hook */
    export const useEventBus = () => {
      const eventBusRef = useRef<EventTarget>(new EventTarget());

      const publish = useCallback((event: UIEvent) => {
        const customEvent = new CustomEvent(event.type, { detail: event });
        eventBusRef.current.dispatchEvent(customEvent);
      }, []);

      const subscribe = useCallback((eventType: string, handler: (event: UIEvent) => void) => {
        const listener = (e: Event) => {
          const customEvent = e as CustomEvent;
          handler(customEvent.detail);
        };

        eventBusRef.current.addEventListener(eventType, listener);

        return () => {
          eventBusRef.current.removeEventListener(eventType, listener);
        };
      }, []);

      return { publish, subscribe };
    };
    ```

- 元件實現

    ```typescript
    /** 產品元件 (發布者) */
    export const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
      const { publish } = useEventBus();

      const handleAddToCart = () => {
        const event = new CartItemAddedEvent({
          productId: product.id,
          quantity: 1
        });
        publish(event);
      };

      return (
        <div className="product-card">
          <h3>{product.name}</h3>
          <p>${product.price}</p>
          <button onClick={handleAddToCart}>加入購物車</button>
        </div>
      );
    };

    /** 購物車元件 (訂閱者) */
    export const CartNotification: React.FC = () => {
      const [notification, setNotification] = useState<string>('');
      const { subscribe } = useEventBus();

      useEffect(() => {
        const unsubscribe = subscribe('CART_ITEM_ADDED', (event: CartItemAddedEvent) => {
          setNotification(`商品已加入購物車: ${event.payload.productId}`);
          setTimeout(() => setNotification(''), 3000);
        });

        return unsubscribe;
      }, [subscribe]);

      return notification ? (
        <div className="cart-notification">
          {notification}
        </div>
      ) : null;
    };

    /** 購物車計數器 (訂閱者) */
    export const CartCounter: React.FC = () => {
      const [itemCount, setItemCount] = useState(0);
      const { subscribe } = useEventBus();

      useEffect(() => {
        const unsubscribe = subscribe('CART_ITEM_ADDED', (event: CartItemAddedEvent) => {
          setItemCount(prev => prev + event.payload.quantity);
        });

        return unsubscribe;
      }, [subscribe]);

      return (
        <div className="cart-counter">
          購物車 ({itemCount})
        </div>
      );
    };
    ```

<br />

## 優點

### 鬆耦合

發布者與訂閱者之間沒有直接依賴，可以獨立開發和部署。

### 可擴展性

- 新增訂閱者不需要修改發布者

- 支援動態訂閱和取消訂閱

- 可以輕鬆添加新的事件類型

### 異步處理

支援非同步訊息處理，提升系統效能和響應性。

### 靈活性

- 支援一對多和多對多通訊模式

- 可以實現複雜的事件處理流程

- 支援事件過濾和路由

<br />

## 缺點

### 複雜性

引入額外的抽象層，增加系統複雜度。

### 除錯困難

異步和間接的通訊方式使得問題追蹤變得困難。

### 訊息順序

無法保證訊息的處理順序，可能導致資料不一致。

### 效能開銷

訊息代理和事件分發會帶來額外的效能開銷。

### 錯誤處理

需要考慮訊息丟失、重複處理等問題。

<br />

## 適用場景

### 適合使用

- 微服務架構：服務間的異步通訊

- 事件驅動系統：需要響應各種事件的系統

- 實時通知：需要即時推送訊息給多個接收者

- 系統整合：整合多個獨立系統

- 工作流程：複雜的業務流程處理

### 不適合使用

- 簡單的同步操作：直接方法呼叫更適合

- 強一致性要求：需要立即確認操作結果

- 小型單體應用：增加不必要的複雜性

- 除錯要求高：需要清晰的呼叫鏈追蹤

<br />

## 實施建議

### 選擇合適的訊息代理

根據需求選擇記憶體、資料庫或專業訊息佇列系統。

### 定義清晰的事件契約

建立標準的事件格式和命名規範。

### 實現錯誤處理機制

考慮重試、死信佇列和錯誤通知機制。

### 監控和記錄

建立完整的事件追蹤和監控系統。

### 測試策略

建立事件驅動系統的測試方法和工具。

<br />

## 總結

Publish–Subscribe Pattern 是構建鬆耦合、可擴展系統的重要架構模式。特別適合事件驅動架構、微服務系統和需要異步處理的場景。

雖然會增加系統複雜度，但帶來的靈活性和可擴展性使其成為現代分散式系統的核心模式。關鍵在於根據具體需求選擇合適的實現方式，並建立完善的監控和錯誤處理機制。
