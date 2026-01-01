# Saga Pattern (分散式交易補償架構)

Saga Pattern (分散式交易補償架構) 是一種管理分散式系統中長時間運行交易的設計模式，通過將複雜的業務流程分解為一系列本地交易，並為每個交易提供補償操作來確保資料一致性。

這種模式特別適用於微服務架構中需要跨多個服務進行協調的業務流程，當無法使用傳統的 ACID 交易時，Saga 提供了一種實現最終一致性的解決方案。

<br />

## 動機

在分散式系統中，常見的問題包括

- 跨服務的 ACID 交易難以實現且性能低下

- 長時間運行的業務流程容易因為服務故障而中斷

- 分散式鎖機制複雜且容易造成死鎖

- 服務間的強一致性要求影響系統可用性

Saga Pattern 通過分解長交易和提供補償機制，解決這些問題，讓系統具備

- 彈性：單個服務故障不會影響整個流程

- 可擴展性：避免分散式鎖，提升系統吞吐量

- 一致性：通過補償操作確保最終一致性

- 可觀測性：清晰的狀態追蹤和錯誤處理

<br />

## 結構

Saga Pattern 包含兩種主要的實現方式

### 1. Choreography (編舞模式)

每個服務知道何時執行下一步操作，通過事件驅動的方式協調。

- 去中心化的協調方式

- 服務間通過事件通訊

- 沒有中央協調器

- 適合簡單的業務流程

### 2. Orchestration (編排模式)

中央協調器負責管理整個 Saga 的執行流程。

- 中心化的協調方式

- 協調器控制執行順序

- 集中的狀態管理

- 適合複雜的業務流程

以下是 Saga Pattern 的結構圖

```text
┌─────────────────────────────────────────────────────────┐
│                    Saga Orchestrator                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │                 Saga Definition                 │    │
│  │  ┌────────────┐  ┌────────────┐  ┌───────────┐  │    │
│  │  │   Step 1   │→ │   Step 2   │→ │   Step 3  │  │    │
│  │  │ Compensate │  │ Compensate │  │ Compensate│  │    │
│  │  └────────────┘  └────────────┘  └───────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Service A    │  │    Service B    │  │    Service C    │
│                 │  │                 │  │                 │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │ Transaction │ │  │ │ Transaction │ │  │ │ Transaction │ │
│ │ Compensate  │ │  │ │ Compensate  │ │  │ │ Compensate  │ │
│ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

<br />

## 核心原則

### 原子性 (Atomicity)

每個 Saga 步驟都是原子操作，要麼完全成功，要麼完全失敗。

### 補償性 (Compensability)

每個步驟都必須有對應的補償操作來撤銷已執行的變更。

### 冪等性 (Idempotency)

補償操作和重試操作都必須是冪等的，多次執行結果相同。

### 隔離性 (Isolation)

雖然無法保證完全隔離，但需要處理中間狀態的可見性問題。

<br />

## 實現方式

### Java 實現範例 (Orchestration)

以電商訂單處理為例

- Saga 定義

    ```java
    /** Saga 步驟定義 */
    public class OrderSagaDefinition {
        private final PaymentService paymentService;
        private final InventoryService inventoryService;
        private final ShippingService shippingService;
        private final NotificationService notificationService;

        public SagaDefinition<OrderSagaData> define() {
            return SagaDefinition.<OrderSagaData>builder()
                .step("reserveInventory")
                    .invokeParticipant(this::reserveInventory)
                    .withCompensation(this::releaseInventory)
                .step("processPayment")
                    .invokeParticipant(this::processPayment)
                    .withCompensation(this::refundPayment)
                .step("createShipment")
                    .invokeParticipant(this::createShipment)
                    .withCompensation(this::cancelShipment)
                .step("sendConfirmation")
                    .invokeParticipant(this::sendConfirmation)
                .build();
        }

        private CommandWithDestination reserveInventory(OrderSagaData data) {
            return send(new ReserveInventoryCommand(data.getOrderId(), data.getItems()))
                .to("inventory-service");
        }

        private CommandWithDestination releaseInventory(OrderSagaData data) {
            return send(new ReleaseInventoryCommand(data.getOrderId()))
                .to("inventory-service");
        }

        private CommandWithDestination processPayment(OrderSagaData data) {
            return send(new ProcessPaymentCommand(
                data.getOrderId(), 
                data.getCustomerId(), 
                data.getTotalAmount()
            )).to("payment-service");
        }

        private CommandWithDestination refundPayment(OrderSagaData data) {
            return send(new RefundPaymentCommand(data.getPaymentId()))
                .to("payment-service");
        }
    }
    ```

- Saga 資料

    ```java
    /** Saga 執行過程中的資料 */
    public class OrderSagaData {
        private String orderId;
        private String customerId;
        private List<OrderItem> items;
        private BigDecimal totalAmount;
        private String paymentId;
        private String shipmentId;
        private SagaStatus status;

        public OrderSagaData(String orderId, String customerId, 
                           List<OrderItem> items, BigDecimal totalAmount) {
            this.orderId = orderId;
            this.customerId = customerId;
            this.items = items;
            this.totalAmount = totalAmount;
            this.status = SagaStatus.STARTED;
        }

        public void setPaymentId(String paymentId) {
            this.paymentId = paymentId;
        }

        public void setShipmentId(String shipmentId) {
            this.shipmentId = shipmentId;
        }

        public void markCompleted() {
            this.status = SagaStatus.COMPLETED;
        }

        public void markFailed() {
            this.status = SagaStatus.FAILED;
        }
    }
    ```

- Saga 協調器

    ```java
    /** Saga 協調器 */
    @Service
    public class SagaOrchestrator {
        private final SagaManager sagaManager;
        private final OrderSagaDefinition orderSagaDefinition;

        public void startOrderSaga(CreateOrderCommand command) {
            OrderSagaData sagaData = new OrderSagaData(
                command.getOrderId(),
                command.getCustomerId(),
                command.getItems(),
                command.getTotalAmount()
            );

            sagaManager.startSaga(
                "OrderSaga",
                sagaData,
                orderSagaDefinition.define()
            );
        }

        @EventHandler
        public void handle(InventoryReservedEvent event) {
            sagaManager.handleReply(
                event.getSagaId(),
                "reserveInventory",
                event
            );
        }

        @EventHandler
        public void handle(PaymentProcessedEvent event) {
            sagaManager.handleReply(
                event.getSagaId(),
                "processPayment",
                event
            );
        }

        @EventHandler
        public void handle(SagaCompletedEvent event) {
            OrderSagaData data = (OrderSagaData) event.getSagaData();
            data.markCompleted();
            /** 更新訂單狀態為已完成 */
        }

        @EventHandler
        public void handle(SagaFailedEvent event) {
            OrderSagaData data = (OrderSagaData) event.getSagaData();
            data.markFailed();
            /** 更新訂單狀態為失敗 */
        }
    }
    ```

### TypeScript 與 Node.js 實現範例 (Choreography)

- 事件定義

    ```typescript
    /** 基礎事件介面 */
    export interface DomainEvent {
      eventId: string;
      sagaId: string;
      timestamp: Date;
      eventType: string;
    }

    /** 訂單建立事件 */
    export interface OrderCreatedEvent extends DomainEvent {
      eventType: 'OrderCreated';
      orderId: string;
      customerId: string;
      items: OrderItem[];
      totalAmount: number;
    }

    /** 庫存保留事件 */
    export interface InventoryReservedEvent extends DomainEvent {
      eventType: 'InventoryReserved';
      orderId: string;
      reservationId: string;
    }

    /** 付款處理事件 */
    export interface PaymentProcessedEvent extends DomainEvent {
      eventType: 'PaymentProcessed';
      orderId: string;
      paymentId: string;
      amount: number;
    }

    /** 補償事件 */
    export interface InventoryReleasedEvent extends DomainEvent {
      eventType: 'InventoryReleased';
      orderId: string;
      reservationId: string;
    }
    ```

- 服務實現

    ```typescript
    /** 庫存服務 */
    export class InventoryService {
      constructor(
        private readonly eventBus: EventBus,
        private readonly inventoryRepository: InventoryRepository
      ) {
        this.setupEventHandlers();
      }

      private setupEventHandlers(): void {
        this.eventBus.subscribe('OrderCreated', this.handleOrderCreated.bind(this));
        this.eventBus.subscribe('PaymentFailed', this.handlePaymentFailed.bind(this));
      }

      private async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
        try {
          const reservationId = await this.reserveInventory(
            event.orderId,
            event.items
          );

          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'InventoryReserved',
            orderId: event.orderId,
            reservationId
          } as InventoryReservedEvent);
        } catch (error) {
          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'InventoryReservationFailed',
            orderId: event.orderId,
            reason: error.message
          });
        }
      }

      private async handlePaymentFailed(event: PaymentFailedEvent): Promise<void> {
        /** 補償操作：釋放庫存 */
        await this.releaseInventory(event.orderId);

        await this.eventBus.publish({
          eventId: generateId(),
          sagaId: event.sagaId,
          timestamp: new Date(),
          eventType: 'InventoryReleased',
          orderId: event.orderId,
          reservationId: event.reservationId
        } as InventoryReleasedEvent);
      }

      private async reserveInventory(orderId: string, items: OrderItem[]): Promise<string> {
        /** 檢查庫存並保留 */
        for (const item of items) {
          const available = await this.inventoryRepository.getAvailableQuantity(item.productId);
          if (available < item.quantity) {
            throw new Error(`商品 ${item.productId} 庫存不足`);
          }
        }

        const reservationId = generateId();
        await this.inventoryRepository.reserveItems(reservationId, items);
        return reservationId;
      }

      private async releaseInventory(orderId: string): Promise<void> {
        await this.inventoryRepository.releaseReservation(orderId);
      }
    }
    ```

- 付款服務

    ```typescript
    /** 付款服務 */
    export class PaymentService {
      constructor(
        private readonly eventBus: EventBus,
        private readonly paymentGateway: PaymentGateway
      ) {
        this.setupEventHandlers();
      }

      private setupEventHandlers(): void {
        this.eventBus.subscribe('InventoryReserved', this.handleInventoryReserved.bind(this));
        this.eventBus.subscribe('ShipmentFailed', this.handleShipmentFailed.bind(this));
      }

      private async handleInventoryReserved(event: InventoryReservedEvent): Promise<void> {
        try {
          const paymentId = await this.processPayment(
            event.orderId,
            event.sagaId
          );

          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'PaymentProcessed',
            orderId: event.orderId,
            paymentId,
            amount: 0 /** 從訂單資料獲取 */
          } as PaymentProcessedEvent);
        } catch (error) {
          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'PaymentFailed',
            orderId: event.orderId,
            reason: error.message
          });
        }
      }

      private async handleShipmentFailed(event: ShipmentFailedEvent): Promise<void> {
        /** 補償操作：退款 */
        await this.refundPayment(event.paymentId);

        await this.eventBus.publish({
          eventId: generateId(),
          sagaId: event.sagaId,
          timestamp: new Date(),
          eventType: 'PaymentRefunded',
          orderId: event.orderId,
          paymentId: event.paymentId
        });
      }

      private async processPayment(orderId: string, sagaId: string): Promise<string> {
        /** 處理付款 */
        const paymentId = generateId();
        await this.paymentGateway.charge(paymentId, orderId);
        return paymentId;
      }

      private async refundPayment(paymentId: string): Promise<void> {
        await this.paymentGateway.refund(paymentId);
      }
    }
    ```

- Saga 狀態管理

    ```typescript
    /** Saga 狀態管理器 */
    export class SagaStateManager {
      constructor(
        private readonly eventBus: EventBus,
        private readonly stateRepository: SagaStateRepository
      ) {
        this.setupEventHandlers();
      }

      private setupEventHandlers(): void {
        this.eventBus.subscribe('OrderCreated', this.handleSagaEvent.bind(this));
        this.eventBus.subscribe('InventoryReserved', this.handleSagaEvent.bind(this));
        this.eventBus.subscribe('PaymentProcessed', this.handleSagaEvent.bind(this));
        this.eventBus.subscribe('ShipmentCreated', this.handleSagaEvent.bind(this));
        /** 補償事件 */
        this.eventBus.subscribe('InventoryReleased', this.handleSagaEvent.bind(this));
        this.eventBus.subscribe('PaymentRefunded', this.handleSagaEvent.bind(this));
      }

      private async handleSagaEvent(event: DomainEvent): Promise<void> {
        const sagaState = await this.stateRepository.findBySagaId(event.sagaId);
        if (!sagaState) {
          return;
        }

        /** 更新 Saga 狀態 */
        sagaState.addEvent(event);

        /** 檢查 Saga 是否完成 */
        if (this.isSagaCompleted(sagaState)) {
          sagaState.markCompleted();
          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'SagaCompleted',
            orderId: sagaState.orderId
          });
        } else if (this.isSagaFailed(sagaState)) {
          sagaState.markFailed();
          await this.eventBus.publish({
            eventId: generateId(),
            sagaId: event.sagaId,
            timestamp: new Date(),
            eventType: 'SagaFailed',
            orderId: sagaState.orderId
          });
        }

        await this.stateRepository.save(sagaState);
      }

      private isSagaCompleted(sagaState: SagaState): boolean {
        const requiredEvents = ['InventoryReserved', 'PaymentProcessed', 'ShipmentCreated'];
        return requiredEvents.every(eventType => 
          sagaState.hasEvent(eventType)
        );
      }

      private isSagaFailed(sagaState: SagaState): boolean {
        const failureEvents = ['InventoryReservationFailed', 'PaymentFailed', 'ShipmentFailed'];
        return failureEvents.some(eventType => 
          sagaState.hasEvent(eventType)
        );
      }
    }
    ```

### React 前端實現範例

- Saga 狀態追蹤

    ```typescript
    /** Saga 狀態介面 */
    export interface SagaStatus {
      sagaId: string;
      orderId: string;
      currentStep: string;
      status: 'running' | 'completed' | 'failed' | 'compensating';
      steps: SagaStep[];
      error?: string;
    }

    export interface SagaStep {
      name: string;
      status: 'pending' | 'running' | 'completed' | 'failed' | 'compensated';
      startTime?: Date;
      endTime?: Date;
      error?: string;
    }
    ```

- React 元件

    ```typescript
    /** 訂單處理狀態元件 */
    export const OrderProcessingStatus: React.FC<{ orderId: string }> = ({ orderId }) => {
      const [sagaStatus, setSagaStatus] = useState<SagaStatus | null>(null);
      const [loading, setLoading] = useState(true);

      useEffect(() => {
        const fetchSagaStatus = async () => {
          try {
            const status = await sagaApi.getSagaStatusByOrderId(orderId);
            setSagaStatus(status);
          } catch (error) {
            console.error('獲取 Saga 狀態失敗:', error);
          } finally {
            setLoading(false);
          }
        };

        fetchSagaStatus();

        /** 設定輪詢更新狀態 */
        const interval = setInterval(fetchSagaStatus, 2000);
        return () => clearInterval(interval);
      }, [orderId]);

      if (loading) {
        return <div className="loading">載入中...</div>;
      }

      if (!sagaStatus) {
        return <div className="error">無法載入訂單處理狀態</div>;
      }

      const getStepIcon = (step: SagaStep) => {
        switch (step.status) {
          case 'completed':
            return '✅';
          case 'running':
            return '⏳';
          case 'failed':
            return '❌';
          case 'compensated':
            return '↩️';
          default:
            return '⭕';
        }
      };

      const getStatusColor = (status: string) => {
        switch (status) {
          case 'completed':
            return 'text-green-600';
          case 'failed':
            return 'text-red-600';
          case 'compensating':
            return 'text-yellow-600';
          default:
            return 'text-blue-600';
        }
      };

      return (
        <div className="saga-status-container">
          <div className="saga-header">
            <h3>訂單處理狀態</h3>
            <span className={`status ${getStatusColor(sagaStatus.status)}`}>
              {sagaStatus.status.toUpperCase()}
            </span>
          </div>

          <div className="saga-steps">
            {sagaStatus.steps.map((step, index) => (
              <div key={step.name} className="step-item">
                <div className="step-icon">
                  {getStepIcon(step)}
                </div>
                <div className="step-content">
                  <div className="step-name">{step.name}</div>
                  <div className={`step-status ${getStatusColor(step.status)}`}>
                    {step.status}
                  </div>
                  {step.error && (
                    <div className="step-error">
                      錯誤: {step.error}
                    </div>
                  )}
                  {step.startTime && (
                    <div className="step-time">
                      開始時間: {step.startTime.toLocaleString()}
                    </div>
                  )}
                </div>
                {index < sagaStatus.steps.length - 1 && (
                  <div className="step-connector">↓</div>
                )}
              </div>
            ))}
          </div>

          {sagaStatus.error && (
            <div className="saga-error">
              <h4>處理錯誤</h4>
              <p>{sagaStatus.error}</p>
            </div>
          )}
        </div>
      );
    };
    ```

<br />

## 優點

### 彈性和容錯性

單個服務的故障不會導致整個業務流程失敗，系統具備自動恢復能力。

### 可擴展性

- 避免分散式鎖：提升系統吞吐量

- 異步處理：不阻塞其他操作

- 服務解耦：各服務可獨立擴展

### 可觀測性

提供清晰的狀態追蹤和錯誤處理機制，便於監控和除錯。

### 業務靈活性

可以輕鬆添加新的業務步驟或修改現有流程。

<br />

## 缺點

### 複雜性

需要設計和實現補償操作，增加系統複雜度。

### 一致性保證

只能保證最終一致性，無法提供強一致性。

### 除錯困難

分散式的執行流程使得問題追蹤和除錯變得困難。

### 補償操作設計

某些操作難以設計有效的補償機制，例如：發送郵件。

### 狀態管理

需要維護 Saga 的執行狀態，增加存儲和管理成本。

<br />

## 適用場景

### 適合使用

- 微服務架構：跨多個服務的業務流程

- 長時間運行的業務流程：訂單處理、工作流程

- 高可用性要求：需要容錯和自動恢復

- 異步處理：不需要即時一致性的場景

- 複雜業務流程：包含多個步驟和條件分支

### 不適合使用

- 強一致性要求：需要 ACID 特性的場景

- 簡單 CRUD 操作：單一服務內的操作

- 實時性要求：需要即時回應的操作

- 難以補償的操作：無法設計有效補償機制

<br />

## 實施建議

### 設計原則

- 每個步驟都要有對應的補償操作

- 確保操作的冪等性

- 設計清晰的狀態轉換

- 提供完整的監控和告警

### 技術選擇

- 選擇合適的事件總線或訊息佇列

- 實現可靠的狀態存儲

- 建立完整的日誌和追蹤系統

- 考慮使用現有的 Saga 框架

### 測試策略

- 單元測試：測試每個步驟和補償操作

- 整合測試：測試完整的 Saga 流程

- 混沌測試：模擬各種故障場景

- 性能測試：驗證系統在高負載下的表現

### 監控和運維

- 實時狀態監控：追蹤 Saga 執行狀態

- 告警機制：及時發現和處理異常

- 手動干預：提供管理介面處理異常情況

- 資料分析：分析 Saga 執行模式和性能

<br />

## 總結

Saga Pattern 提供了一種在分散式系統中管理長時間運行交易的有效方法，特別適合微服務架構中的複雜業務流程。雖然增加了系統複雜度，但通過合理的設計和實現，能夠顯著提升系統的彈性、可擴展性和可維護性。

關鍵在於根據業務需求選擇合適的實現方式 (Choreography 或 Orchestration)，設計有效的補償機制，並建立完整的監控和運維體系。對於需要跨服務協調的複雜業務流程，Saga Pattern 是一個值得考慮的架構選擇。
