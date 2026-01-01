# Reactive Architecture (反應式架構)

Reactive Architecture (反應式架構) 是一種基於反應式宣言 (Reactive Manifesto) 的軟體架構模式，專注於建構響應式、彈性、可擴展且訊息驅動的系統。

這種架構強調非同步訊息傳遞、事件驅動設計和資料流處理，使系統能夠優雅處理高負載、故障恢復和動態擴展需求。

<br />

## 動機

在現代分散式系統中，常見的挑戰包括

- 高併發請求導致系統響應緩慢或崩潰

- 系統元件間緊密耦合，故障容易擴散

- 難以動態擴展以應對負載變化

- 阻塞式操作影響整體系統效能

- 複雜的狀態管理和資料同步問題

Reactive Architecture 通過反應式原則，解決這些問題，讓系統具備

- 響應性：快速回應使用者請求

- 彈性：優雅處理故障和異常

- 可擴展性：動態調整資源以應對負載

- 訊息驅動：透過非同步訊息解耦元件

<br />

## 結構

Reactive Architecture 基於四個核心原則構建

### 1. Responsive (響應性)

系統在合理時間內回應請求。

- 快速且一致的回應時間

- 建立使用者信心和可用性

- 問題能夠快速被偵測和處理

### 2. Resilient (彈性)

系統在面對故障時保持響應性。

- 故障隔離和容錯機制

- 複製、圍堵、隔離和委派

- 故障恢復不影響整體系統

### 3. Elastic (可擴展性)

系統在工作負載變化時保持響應性。

- 動態增減資源

- 無爭用點和中央瓶頸

- 預測式和反應式擴展

### 4. Message Driven (訊息驅動)

系統依賴非同步訊息傳遞。

- 元件間鬆散耦合

- 位置透明性

- 背壓處理機制

以下是 Reactive Architecture 的核心結構圖

```text
┌──────────────────────────────────────────────────────┐
│                    User Interface                    │
├──────────────────────────────────────────────────────┤
│                Event Stream Layer                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Event     │  │   Event     │  │   Event     │   │ 
│  │  Producer   │  │  Processor  │  │  Consumer   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├──────────────────────────────────────────────────────┤
│                  Message Bus Layer                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │            Asynchronous Messaging               │ │
│  └─────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────┤
│                    Service Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Reactive   │  │  Reactive   │  │  Reactive   │   │
│  │  Service A  │  │  Service B  │  │  Service C  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
├──────────────────────────────────────────────────────┤
│                 Data Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Reactive   │  │   Event     │  │   Stream    │   │
│  │  Database   │  │   Store     │  │  Storage    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└──────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 非同步訊息傳遞

所有元件間通訊都透過非同步訊息進行，避免阻塞操作。

### 事件驅動設計

系統基於事件和狀態變化進行反應，而非主動輪詢。

### 背壓處理

當下游處理能力不足時，能夠向上游發出信號進行流量控制。

### 故障隔離

故障被限制在特定元件內，不會影響整個系統。

<br />

## 實現方式

### Java 實現範例 (使用 Akka)

以訂單處理系統為例

- Actor 系統設計

    ```java
    /** 訂單處理 Actor */
    public class OrderProcessorActor extends AbstractActor {
        private final ActorRef paymentActor;
        private final ActorRef inventoryActor;
        private final ActorRef notificationActor;

        public OrderProcessorActor(
            ActorRef paymentActor,
            ActorRef inventoryActor,
            ActorRef notificationActor
        ) {
            this.paymentActor = paymentActor;
            this.inventoryActor = inventoryActor;
            this.notificationActor = notificationActor;
        }

        @Override
        public Receive createReceive() {
            return receiveBuilder()
                .match(ProcessOrderCommand.class, this::handleProcessOrder)
                .match(PaymentProcessedEvent.class, this::handlePaymentProcessed)
                .match(InventoryReservedEvent.class, this::handleInventoryReserved)
                .build();
        }

        private void handleProcessOrder(ProcessOrderCommand command) {
            /** 檢查庫存 */
            inventoryActor.tell(
                new ReserveInventoryCommand(command.getOrderId(), command.getItems()),
                getSelf()
            );

            /** 處理付款 */
            paymentActor.tell(
                new ProcessPaymentCommand(command.getOrderId(), command.getAmount()),
                getSelf()
            );
        }

        private void handlePaymentProcessed(PaymentProcessedEvent event) {
            if (event.isSuccessful()) {
                /** 確認訂單 */
                notificationActor.tell(
                    new SendNotificationCommand(event.getOrderId(), "訂單付款成功"),
                    getSelf()
                );
            } else {
                /** 取消庫存預留 */
                inventoryActor.tell(
                    new CancelReservationCommand(event.getOrderId()),
                    getSelf()
                );
            }
        }
    }
    ```

- 反應式流處理

    ```java
    /** 使用 Akka Streams 處理訂單流 */
    public class OrderStreamProcessor {
        private final ActorSystem system;
        private final Materializer materializer;

        public OrderStreamProcessor(ActorSystem system) {
            this.system = system;
            this.materializer = ActorMaterializer.create(system);
        }

        public void processOrderStream() {
            Source<OrderEvent, NotUsed> orderSource = 
                Source.actorRef(1000, OverflowStrategy.dropHead());

            Flow<OrderEvent, ProcessedOrder, NotUsed> processingFlow = 
                Flow.<OrderEvent>create()
                    .mapAsync(4, this::validateOrder)
                    .mapAsync(4, this::enrichOrder)
                    .mapAsync(4, this::persistOrder);

            Sink<ProcessedOrder, CompletionStage<Done>> sink = 
                Sink.foreach(order -> 
                    system.log().info("訂單處理完成: {}", order.getId())
                );

            orderSource
                .via(processingFlow)
                .to(sink)
                .run(materializer);
        }

        private CompletionStage<ValidatedOrder> validateOrder(OrderEvent event) {
            return CompletableFuture.supplyAsync(() -> {
                /** 驗證訂單資料 */
                if (event.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
                    throw new IllegalArgumentException("訂單金額必須大於零");
                }
                return new ValidatedOrder(event);
            });
        }

        private CompletionStage<EnrichedOrder> enrichOrder(ValidatedOrder order) {
            return CompletableFuture.supplyAsync(() -> {
                /** 豐富訂單資訊 */
                return new EnrichedOrder(order, fetchCustomerInfo(order.getCustomerId()));
            });
        }

        private CompletionStage<ProcessedOrder> persistOrder(EnrichedOrder order) {
            return CompletableFuture.supplyAsync(() -> {
                /** 持久化訂單 */
                return orderRepository.save(order);
            });
        }
    }
    ```

### TypeScript 與 Node.js 實現範例 (使用 RxJS)

- 反應式服務設計

    ```typescript
    /** 反應式用戶服務 */
    export class ReactiveUserService {
      private userSubject = new BehaviorSubject<User[]>([]);
      private errorSubject = new Subject<Error>();

      constructor(
        private readonly userRepository: UserRepository,
        private readonly eventBus: EventBus
      ) {
        this.initializeEventHandlers();
      }

      /** 獲取用戶流 */
      getUsers$(): Observable<User[]> {
        return this.userSubject.asObservable();
      }

      /** 獲取錯誤流 */
      getErrors$(): Observable<Error> {
        return this.errorSubject.asObservable();
      }

      /** 創建用戶 */
      createUser$(userData: CreateUserData): Observable<User> {
        return from(this.userRepository.create(userData)).pipe(
          tap(user => {
            /** 發布用戶創建事件 */
            this.eventBus.publish(new UserCreatedEvent(user));

            /** 更新用戶列表 */
            const currentUsers = this.userSubject.value;
            this.userSubject.next([...currentUsers, user]);
          }),
          catchError(error => {
            this.errorSubject.next(error);
            return throwError(error);
          })
        );
      }

      /** 更新用戶 */
      updateUser$(id: string, updateData: UpdateUserData): Observable<User> {
        return from(this.userRepository.update(id, updateData)).pipe(
          tap(updatedUser => {
            /** 發布用戶更新事件 */
            this.eventBus.publish(new UserUpdatedEvent(updatedUser));

            /** 更新用戶列表 */
            const currentUsers = this.userSubject.value;
            const updatedUsers = currentUsers.map(user => 
              user.id === id ? updatedUser : user
            );
            this.userSubject.next(updatedUsers);
          }),
          catchError(error => {
            this.errorSubject.next(error);
            return throwError(error);
          })
        );
      }

      private initializeEventHandlers(): void {
        /** 監聽外部事件 */
        this.eventBus.subscribe(UserDeletedEvent).pipe(
          tap(event => {
            const currentUsers = this.userSubject.value;
            const filteredUsers = currentUsers.filter(user => user.id !== event.userId);
            this.userSubject.next(filteredUsers);
          })
        ).subscribe();
      }
    }
    ```

- 背壓處理實現

    ```typescript
    /** 帶背壓控制的資料處理器 */
    export class BackpressureProcessor {
      private readonly bufferSize = 100;
      private readonly processingConcurrency = 5;

      processDataStream$(source: Observable<DataItem>): Observable<ProcessedData> {
        return source.pipe(
          /** 緩衝控制 */
          bufferCount(this.bufferSize),

          /** 並發處理控制 */
          mergeMap(
            batch => this.processBatch$(batch),
            this.processingConcurrency
          ),

          /** 展平結果 */
          mergeMap(results => from(results)),

          /** 錯誤處理 */
          catchError(error => {
            console.error('資料處理錯誤:', error);
            return EMPTY;
          }),

          /** 背壓處理 */
          share()
        );
      }

      private processBatch$(batch: DataItem[]): Observable<ProcessedData[]> {
        return from(
          Promise.all(
            batch.map(item => this.processItem(item))
          )
        ).pipe(
          timeout(5000), /** 超時控制 */
          retry(3) /** 重試機制 */
        );
      }

      private async processItem(item: DataItem): Promise<ProcessedData> {
        /** 模擬非同步處理 */
        await new Promise(resolve => setTimeout(resolve, 100));

        return {
          id: item.id,
          processedAt: new Date(),
          result: `處理完成: ${item.data}`
        };
      }
    }
    ```

### React 前端實現範例

- 反應式狀態管理

    ```typescript
    /** 反應式商店 */
    export class ReactiveStore<T> {
      private state$ = new BehaviorSubject<T>(this.initialState);
      private actions$ = new Subject<Action>();

      constructor(
        private readonly initialState: T,
        private readonly reducer: (state: T, action: Action) => T
      ) {
        this.setupActionProcessing();
      }

      /** 獲取狀態流 */
      getState$(): Observable<T> {
        return this.state$.asObservable();
      }

      /** 獲取當前狀態 */
      getCurrentState(): T {
        return this.state$.value;
      }

      /** 派發動作 */
      dispatch(action: Action): void {
        this.actions$.next(action);
      }

      private setupActionProcessing(): void {
        this.actions$.pipe(
          scan((state, action) => this.reducer(state, action), this.initialState),
          tap(newState => this.state$.next(newState))
        ).subscribe();
      }
    }

    /** 待辦事項反應式商店 */
    interface TodoState {
      todos: Todo[];
      loading: boolean;
      error: string | null;
    }

    type TodoAction = 
      | { type: 'LOAD_TODOS_START' }
      | { type: 'LOAD_TODOS_SUCCESS'; payload: Todo[] }
      | { type: 'LOAD_TODOS_ERROR'; payload: string }
      | { type: 'ADD_TODO'; payload: Todo }
      | { type: 'TOGGLE_TODO'; payload: string };

    const todoReducer = (state: TodoState, action: TodoAction): TodoState => {
      switch (action.type) {
        case 'LOAD_TODOS_START':
          return { ...state, loading: true, error: null };

        case 'LOAD_TODOS_SUCCESS':
          return { ...state, loading: false, todos: action.payload };

        case 'LOAD_TODOS_ERROR':
          return { ...state, loading: false, error: action.payload };

        case 'ADD_TODO':
          return { ...state, todos: [...state.todos, action.payload] };

        case 'TOGGLE_TODO':
          return {
            ...state,
            todos: state.todos.map(todo =>
              todo.id === action.payload
                ? { ...todo, completed: !todo.completed }
                : todo
            )
          };

        default:
          return state;
      }
    };

    export const todoStore = new ReactiveStore<TodoState>(
      { todos: [], loading: false, error: null },
      todoReducer
    );
    ```

- React Hook 整合

    ```typescript
    /** 反應式 Hook */
    export function useReactiveStore<T>(store: ReactiveStore<T>): T {
      const [state, setState] = useState(store.getCurrentState());

      useEffect(() => {
        const subscription = store.getState$().subscribe(setState);
        return () => subscription.unsubscribe();
      }, [store]);

      return state;
    }

    /** 待辦事項元件 */
    export const TodoApp: React.FC = () => {
      const state = useReactiveStore(todoStore);
      const [newTodoText, setNewTodoText] = useState('');

      useEffect(() => {
        /** 載入待辦事項 */
        todoStore.dispatch({ type: 'LOAD_TODOS_START' });

        /** 模擬 API 呼叫 */
        setTimeout(() => {
          todoStore.dispatch({
            type: 'LOAD_TODOS_SUCCESS',
            payload: [
              { id: '1', text: '學習反應式架構', completed: false },
              { id: '2', text: '實作範例程式', completed: true }
            ]
          });
        }, 1000);
      }, []);

      const handleAddTodo = (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTodoText.trim()) return;

        const newTodo: Todo = {
          id: Date.now().toString(),
          text: newTodoText.trim(),
          completed: false
        };

        todoStore.dispatch({ type: 'ADD_TODO', payload: newTodo });
        setNewTodoText('');
      };

      const handleToggleTodo = (id: string) => {
        todoStore.dispatch({ type: 'TOGGLE_TODO', payload: id });
      };

      if (state.loading) {
        return <div>載入中...</div>;
      }

      if (state.error) {
        return <div>錯誤: {state.error}</div>;
      }

      return (
        <div className="todo-app">
          <form onSubmit={handleAddTodo}>
            <input
              type="text"
              value={newTodoText}
              onChange={(e) => setNewTodoText(e.target.value)}
              placeholder="輸入新的待辦事項"
            />
            <button type="submit">新增</button>
          </form>

          <ul className="todo-list">
            {state.todos.map((todo) => (
              <li key={todo.id} className={todo.completed ? 'completed' : ''}>
                <span onClick={() => handleToggleTodo(todo.id)}>
                  {todo.text}
                </span>
              </li>
            ))}
          </ul>
        </div>
      );
    };
    ```

### 微服務實現範例

- 事件驅動微服務

    ```typescript
    /** 訂單服務 */
    export class OrderService {
      constructor(
        private readonly eventBus: EventBus,
        private readonly orderRepository: OrderRepository
      ) {
        this.setupEventHandlers();
      }

      async createOrder(orderData: CreateOrderData): Promise<Order> {
        const order = new Order(orderData);

        /** 保存訂單 */
        const savedOrder = await this.orderRepository.save(order);

        /** 發布訂單創建事件 */
        await this.eventBus.publish(new OrderCreatedEvent(savedOrder));

        return savedOrder;
      }

      private setupEventHandlers(): void {
        /** 監聽付款完成事件 */
        this.eventBus.subscribe(PaymentCompletedEvent, async (event) => {
          const order = await this.orderRepository.findById(event.orderId);
          if (order) {
            order.markAsPaid();
            await this.orderRepository.save(order);

            /** 發布訂單付款完成事件 */
            await this.eventBus.publish(new OrderPaidEvent(order));
          }
        });

        /** 監聽庫存預留失敗事件 */
        this.eventBus.subscribe(InventoryReservationFailedEvent, async (event) => {
          const order = await this.orderRepository.findById(event.orderId);
          if (order) {
            order.markAsCancelled();
            await this.orderRepository.save(order);

            /** 發布訂單取消事件 */
            await this.eventBus.publish(new OrderCancelledEvent(order));
          }
        });
      }
    }

    /** 庫存服務 */
    export class InventoryService {
      constructor(
        private readonly eventBus: EventBus,
        private readonly inventoryRepository: InventoryRepository
      ) {
        this.setupEventHandlers();
      }

      private setupEventHandlers(): void {
        /** 監聽訂單創建事件 */
        this.eventBus.subscribe(OrderCreatedEvent, async (event) => {
          try {
            /** 預留庫存 */
            await this.reserveInventory(event.order.items);

            /** 發布庫存預留成功事件 */
            await this.eventBus.publish(
              new InventoryReservedEvent(event.order.id, event.order.items)
            );
          } catch (error) {
            /** 發布庫存預留失敗事件 */
            await this.eventBus.publish(
              new InventoryReservationFailedEvent(event.order.id, error.message)
            );
          }
        });
      }

      private async reserveInventory(items: OrderItem[]): Promise<void> {
        for (const item of items) {
          const inventory = await this.inventoryRepository.findByProductId(item.productId);

          if (!inventory || inventory.quantity < item.quantity) {
            throw new Error(`商品 ${item.productId} 庫存不足`);
          }

          inventory.reserve(item.quantity);
          await this.inventoryRepository.save(inventory);
        }
      }
    }
    ```

<br />

## 優點

### 高響應性

非同步處理和事件驅動設計確保系統快速回應。

### 故障隔離

元件間鬆散耦合，故障不會擴散到整個系統。

### 動態擴展

可以根據負載動態調整資源配置。

### 高併發處理

非阻塞操作和背壓機制支援高併發場景。

### 可觀測性

事件流和訊息傳遞提供良好的系統可觀測性。

<br />

## 缺點

### 複雜性增加

非同步程式設計和事件驅動模式增加系統複雜度。

### 除錯困難

分散式事件流使得問題追蹤和除錯變得困難。

### 學習曲線

需要團隊掌握反應式程式設計概念和工具。

### 資源消耗

事件處理和訊息傳遞可能增加記憶體和網路開銷。

### 一致性挑戰

最終一致性模型可能不適合所有業務場景。

<br />

## 適用場景

### 適合使用

- 高併發系統：需要處理大量並發請求

- 即時應用：聊天、遊戲、即時通知系統

- 微服務架構：服務間需要鬆散耦合

- 資料流處理：需要處理連續資料流

- 物聯網系統：大量設備產生事件資料

### 不適合使用

- 簡單 CRUD 應用：基本的資料操作不需要反應式設計

- 強一致性需求：需要 ACID 事務保證的系統

- 小型單體應用：複雜度超過收益

- 團隊經驗不足：缺乏反應式程式設計經驗

<br />

## 實施建議

### 漸進式採用

從系統的特定部分開始，逐步引入反應式模式。

### 工具選擇

選擇合適的反應式框架和函式庫 (例如：RxJS、Akka、Spring WebFlux)。

### 監控和觀測

建立完善的監控系統來追蹤事件流和系統效能。

### 錯誤處理策略

設計完整的錯誤處理和恢復機制。

### 團隊培訓

確保團隊理解反應式程式設計原則和最佳實務。

<br />

## 總結

Reactive Architecture 為現代高併發、分散式系統提供了強大的架構模式。透過非同步訊息傳遞、事件驅動設計和背壓處理，能夠建構出響應式、彈性且可擴展的系統。

雖然增加了系統複雜度和學習成本，但對於需要處理高負載、要求高可用性的現代應用來說，反應式架構能夠帶來顯著的效能和可靠性提升。關鍵在於根據實際需求評估是否採用，以及選擇合適的實施策略和工具。
