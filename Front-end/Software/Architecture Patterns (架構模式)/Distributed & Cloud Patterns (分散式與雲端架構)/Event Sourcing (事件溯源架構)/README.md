# Event Sourcing (事件溯源架構)

Event Sourcing (事件溯源架構) 是一種資料儲存模式，不直接儲存應用程式的當前狀態，而是儲存導致該狀態的所有事件序列。系統狀態可以通過重播這些事件來重建。

這種架構模式將資料的變更記錄為不可變的事件流，提供完整的審計追蹤，並支援時間旅行查詢和複雜的業務分析。

<br />

## 動機

在傳統的 CRUD 系統中，常見的問題包括

- 資料變更歷史遺失，無法追蹤狀態變化過程

- 併發更新衝突，多個使用者同時修改相同資料

- 業務規則複雜時，狀態管理變得困難

- 審計和合規要求難以滿足

- 資料分析需求與操作需求衝突

Event Sourcing 通過事件驅動的方式，解決這些問題，讓系統具備

- 完整性：保留所有歷史變更記錄

- 可追溯性：可以重建任意時間點的狀態

- 可擴展性：讀寫分離，支援高併發

- 靈活性：可以建立多種不同的檢視模型

<br />

## 結構

Event Sourcing 架構包含以下核心元件

### 1. Event (事件)

記錄系統中發生的業務事件。

- 不可變的資料結構

- 包含事件類型、時間戳記和相關資料

- 按時間順序儲存

### 2. Event Store (事件儲存)

專門儲存事件的資料庫。

- 只支援追加操作

- 提供事件查詢和重播功能

- 確保事件順序和完整性

### 3. Aggregate (聚合)

業務實體，處理命令並產生事件。

- 封裝業務規則

- 維護內部狀態

- 確保業務不變條件

### 4. Projection (投影)

從事件流建立的讀取模型。

- 針對特定查詢需求最佳化

- 可以有多個不同的投影

- 支援最終一致性

以下是 Event Sourcing 的架構圖

```text
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Command   │ --→ │  Aggregate  │ --→ │    Event    │
│   Handler   │     │             │     │    Store    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ↓
                    ┌─────────────┐     ┌─────────────┐
                    │ Projection  │ ←-- │    Event    │
                    │   Handler   │     │  Publisher  │
                    └─────────────┘     └─────────────┘
                           │
                           ↓
                    ┌─────────────┐
                    │    Read     │
                    │    Model    │
                    └─────────────┘
```

<br />

## 核心原則

### 事件不可變性 (Event Immutability)

一旦事件被儲存，就不能被修改或刪除，只能追加新事件。

### 事件順序性 (Event Ordering)

事件必須按照發生的時間順序儲存和處理。

### 最終一致性 (Eventual Consistency)

讀取模型可能暫時與事件流不一致，但最終會達到一致狀態。

<br />

## 實現方式

### Java 實現範例

以銀行帳戶系統為例

- Event (事件)

    ```java
    /** 基礎事件介面 */
    public interface DomainEvent {
        String getAggregateId();
        LocalDateTime getOccurredOn();
        String getEventType();
    }

    /** 帳戶開立事件 */
    public class AccountOpenedEvent implements DomainEvent {
        private final String accountId;
        private final String customerId;
        private final BigDecimal initialBalance;
        private final LocalDateTime occurredOn;

        public AccountOpenedEvent(String accountId, String customerId, BigDecimal initialBalance) {
            this.accountId = accountId;
            this.customerId = customerId;
            this.initialBalance = initialBalance;
            this.occurredOn = LocalDateTime.now();
        }

        @Override
        public String getAggregateId() { return accountId; }

        @Override
        public LocalDateTime getOccurredOn() { return occurredOn; }

        @Override
        public String getEventType() { return "AccountOpened"; }

        public String getCustomerId() { return customerId; }
        public BigDecimal getInitialBalance() { return initialBalance; }
    }

    /** 存款事件 */
    public class MoneyDepositedEvent implements DomainEvent {
        private final String accountId;
        private final BigDecimal amount;
        private final LocalDateTime occurredOn;

        public MoneyDepositedEvent(String accountId, BigDecimal amount) {
            this.accountId = accountId;
            this.amount = amount;
            this.occurredOn = LocalDateTime.now();
        }

        @Override
        public String getAggregateId() { return accountId; }

        @Override
        public LocalDateTime getOccurredOn() { return occurredOn; }

        @Override
        public String getEventType() { return "MoneyDeposited"; }

        public BigDecimal getAmount() { return amount; }
    }
    ```

- Aggregate (聚合)

    ```java
    /** 銀行帳戶聚合 */
    public class BankAccount {
        private String accountId;
        private String customerId;
        private BigDecimal balance;
        private boolean isActive;
        private List<DomainEvent> uncommittedEvents;

        public BankAccount() {
            this.uncommittedEvents = new ArrayList<>();
        }

        /** 從事件重建聚合 */
        public static BankAccount fromEvents(List<DomainEvent> events) {
            BankAccount account = new BankAccount();
            for (DomainEvent event : events) {
                account.apply(event);
            }
            return account;
        }

        /** 開立帳戶 */
        public void openAccount(String accountId, String customerId, BigDecimal initialBalance) {
            if (initialBalance.compareTo(BigDecimal.ZERO) < 0) {
                throw new IllegalArgumentException("初始餘額不能為負數");
            }

            AccountOpenedEvent event = new AccountOpenedEvent(accountId, customerId, initialBalance);
            applyAndRecord(event);
        }

        /** 存款 */
        public void deposit(BigDecimal amount) {
            if (!isActive) {
                throw new IllegalStateException("帳戶未啟用");
            }
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("存款金額必須大於零");
            }

            MoneyDepositedEvent event = new MoneyDepositedEvent(accountId, amount);
            applyAndRecord(event);
        }

        /** 套用事件並記錄 */
        private void applyAndRecord(DomainEvent event) {
            apply(event);
            uncommittedEvents.add(event);
        }

        /** 套用事件到聚合狀態 */
        private void apply(DomainEvent event) {
            if (event instanceof AccountOpenedEvent) {
                AccountOpenedEvent e = (AccountOpenedEvent) event;
                this.accountId = e.getAggregateId();
                this.customerId = e.getCustomerId();
                this.balance = e.getInitialBalance();
                this.isActive = true;
            } else if (event instanceof MoneyDepositedEvent) {
                MoneyDepositedEvent e = (MoneyDepositedEvent) event;
                this.balance = this.balance.add(e.getAmount());
            }
        }

        public List<DomainEvent> getUncommittedEvents() {
            return new ArrayList<>(uncommittedEvents);
        }

        public void markEventsAsCommitted() {
            uncommittedEvents.clear();
        }

        public String getAccountId() { return accountId; }
        public BigDecimal getBalance() { return balance; }
        public boolean isActive() { return isActive; }
    }
    ```

- Event Store (事件儲存)

    ```java
    /** 事件儲存介面 */
    public interface EventStore {
        void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion);
        List<DomainEvent> getEvents(String aggregateId);
        List<DomainEvent> getEvents(String aggregateId, int fromVersion);
    }

    /** 記憶體事件儲存實作 */
    @Component
    public class InMemoryEventStore implements EventStore {
        private final Map<String, List<EventData>> eventStreams = new ConcurrentHashMap<>();
        private final EventSerializer serializer;

        @Override
        public void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion) {
            List<EventData> stream = eventStreams.computeIfAbsent(aggregateId, k -> new ArrayList<>());

            if (stream.size() != expectedVersion) {
                throw new ConcurrencyException("預期版本不符");
            }

            for (DomainEvent event : events) {
                EventData eventData = new EventData(
                    UUID.randomUUID().toString(),
                    event.getEventType(),
                    serializer.serialize(event),
                    event.getOccurredOn()
                );
                stream.add(eventData);
            }
        }

        @Override
        public List<DomainEvent> getEvents(String aggregateId) {
            return getEvents(aggregateId, 0);
        }

        @Override
        public List<DomainEvent> getEvents(String aggregateId, int fromVersion) {
            List<EventData> stream = eventStreams.get(aggregateId);
            if (stream == null) {
                return Collections.emptyList();
            }

            return stream.stream()
                .skip(fromVersion)
                .map(eventData -> serializer.deserialize(eventData.getEventType(), eventData.getData()))
                .collect(Collectors.toList());
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Event (事件)

    ```typescript
    /** 基礎事件介面 */
    export interface DomainEvent {
      aggregateId: string;
      occurredOn: Date;
      eventType: string;
    }

    /** 使用者註冊事件 */
    export class UserRegisteredEvent implements DomainEvent {
      constructor(
        public readonly aggregateId: string,
        public readonly email: string,
        public readonly name: string,
        public readonly occurredOn: Date = new Date()
      ) {}

      get eventType(): string {
        return 'UserRegistered';
      }
    }

    /** 使用者啟用事件 */
    export class UserActivatedEvent implements DomainEvent {
      constructor(
        public readonly aggregateId: string,
        public readonly occurredOn: Date = new Date()
      ) {}

      get eventType(): string {
        return 'UserActivated';
      }
    }
    ```

- Aggregate (聚合)

    ```typescript
    /** 使用者聚合 */
    export class User {
      private id: string;
      private email: string;
      private name: string;
      private isActive: boolean = false;
      private uncommittedEvents: DomainEvent[] = [];

      private constructor() {}

      /** 從事件重建聚合 */
      static fromEvents(events: DomainEvent[]): User {
        const user = new User();
        events.forEach(event => user.apply(event));
        return user;
      }

      /** 註冊使用者 */
      static register(id: string, email: string, name: string): User {
        const user = new User();
        const event = new UserRegisteredEvent(id, email, name);
        user.applyAndRecord(event);
        return user;
      }

      /** 啟用使用者 */
      activate(): void {
        if (this.isActive) {
          throw new Error('使用者已經啟用');
        }

        const event = new UserActivatedEvent(this.id);
        this.applyAndRecord(event);
      }

      /** 套用事件並記錄 */
      private applyAndRecord(event: DomainEvent): void {
        this.apply(event);
        this.uncommittedEvents.push(event);
      }

      /** 套用事件到聚合狀態 */
      private apply(event: DomainEvent): void {
        switch (event.eventType) {
          case 'UserRegistered':
            const registeredEvent = event as UserRegisteredEvent;
            this.id = registeredEvent.aggregateId;
            this.email = registeredEvent.email;
            this.name = registeredEvent.name;
            this.isActive = false;
            break;

          case 'UserActivated':
            this.isActive = true;
            break;

          default:
            throw new Error(`未知的事件類型: ${event.eventType}`);
        }
      }

      getUncommittedEvents(): DomainEvent[] {
        return [...this.uncommittedEvents];
      }

      markEventsAsCommitted(): void {
        this.uncommittedEvents = [];
      }

      getId(): string { return this.id; }
      getEmail(): string { return this.email; }
      getName(): string { return this.name; }
      getIsActive(): boolean { return this.isActive; }
    }
    ```

- Event Store (事件儲存)

    ```typescript
    /** 事件資料 */
    interface EventData {
      id: string;
      aggregateId: string;
      eventType: string;
      data: string;
      occurredOn: Date;
      version: number;
    }

    /** 事件儲存介面 */
    export interface EventStore {
      saveEvents(aggregateId: string, events: DomainEvent[], expectedVersion: number): Promise<void>;
      getEvents(aggregateId: string): Promise<DomainEvent[]>;
      getEvents(aggregateId: string, fromVersion: number): Promise<DomainEvent[]>;
    }

    /** MongoDB 事件儲存實作 */
    export class MongoEventStore implements EventStore {
      constructor(
        private readonly eventCollection: Collection<EventData>,
        private readonly eventSerializer: EventSerializer
      ) {}

      async saveEvents(aggregateId: string, events: DomainEvent[], expectedVersion: number): Promise<void> {
        const session = this.eventCollection.client.startSession();

        try {
          await session.withTransaction(async () => {
            /** 檢查版本衝突 */
            const currentVersion = await this.getCurrentVersion(aggregateId);
            if (currentVersion !== expectedVersion) {
              throw new Error('併發衝突：預期版本不符');
            }

            /** 儲存事件 */
            const eventData: EventData[] = events.map((event, index) => ({
              id: generateId(),
              aggregateId,
              eventType: event.eventType,
              data: this.eventSerializer.serialize(event),
              occurredOn: event.occurredOn,
              version: expectedVersion + index + 1
            }));

            await this.eventCollection.insertMany(eventData, { session });
          });
        } finally {
          await session.endSession();
        }
      }

      async getEvents(aggregateId: string, fromVersion: number = 0): Promise<DomainEvent[]> {
        const eventData = await this.eventCollection
          .find({ 
            aggregateId, 
            version: { $gt: fromVersion } 
          })
          .sort({ version: 1 })
          .toArray();

        return eventData.map(data => 
          this.eventSerializer.deserialize(data.eventType, data.data)
        );
      }

      private async getCurrentVersion(aggregateId: string): Promise<number> {
        const lastEvent = await this.eventCollection
          .findOne(
            { aggregateId },
            { sort: { version: -1 } }
          );

        return lastEvent ? lastEvent.version : 0;
      }
    }
    ```

- Projection (投影)

    ```typescript
    /** 使用者檢視模型 */
    export interface UserView {
      id: string;
      email: string;
      name: string;
      isActive: boolean;
      registeredAt: Date;
      activatedAt?: Date;
    }

    /** 投影處理器 */
    export class UserProjectionHandler {
      constructor(private readonly userViewRepository: UserViewRepository) {}

      async handle(event: DomainEvent): Promise<void> {
        switch (event.eventType) {
          case 'UserRegistered':
            await this.handleUserRegistered(event as UserRegisteredEvent);
            break;

          case 'UserActivated':
            await this.handleUserActivated(event as UserActivatedEvent);
            break;
        }
      }

      private async handleUserRegistered(event: UserRegisteredEvent): Promise<void> {
        const userView: UserView = {
          id: event.aggregateId,
          email: event.email,
          name: event.name,
          isActive: false,
          registeredAt: event.occurredOn
        };

        await this.userViewRepository.save(userView);
      }

      private async handleUserActivated(event: UserActivatedEvent): Promise<void> {
        const userView = await this.userViewRepository.findById(event.aggregateId);
        if (userView) {
          userView.isActive = true;
          userView.activatedAt = event.occurredOn;
          await this.userViewRepository.save(userView);
        }
      }
    }
    ```

### React 前端實現範例

- Event Store Client (事件儲存客戶端)

    ```typescript
    /** 前端事件儲存客戶端 */
    export class EventStoreClient {
      constructor(private readonly httpClient: HttpClient) {}

      async getEvents(aggregateId: string): Promise<DomainEvent[]> {
        const response = await this.httpClient.get(`/api/events/${aggregateId}`);
        return response.data.map(this.deserializeEvent);
      }

      async saveEvents(aggregateId: string, events: DomainEvent[]): Promise<void> {
        const serializedEvents = events.map(this.serializeEvent);
        await this.httpClient.post(`/api/events/${aggregateId}`, {
          events: serializedEvents
        });
      }

      private serializeEvent(event: DomainEvent): any {
        return {
          eventType: event.eventType,
          aggregateId: event.aggregateId,
          occurredOn: event.occurredOn.toISOString(),
          data: event
        };
      }

      private deserializeEvent(data: any): DomainEvent {
        switch (data.eventType) {
          case 'TaskCreated':
            return new TaskCreatedEvent(
              data.data.aggregateId,
              data.data.title,
              data.data.description,
              new Date(data.occurredOn)
            );
          case 'TaskCompleted':
            return new TaskCompletedEvent(
              data.data.aggregateId,
              new Date(data.occurredOn)
            );
          default:
            throw new Error(`未知的事件類型: ${data.eventType}`);
        }
      }
    }
    ```

- Task Management Component (任務管理元件)

    ```typescript
    /** 任務事件 */
    export class TaskCreatedEvent implements DomainEvent {
      constructor(
        public readonly aggregateId: string,
        public readonly title: string,
        public readonly description: string,
        public readonly occurredOn: Date = new Date()
      ) {}

      get eventType(): string { return 'TaskCreated'; }
    }

    export class TaskCompletedEvent implements DomainEvent {
      constructor(
        public readonly aggregateId: string,
        public readonly occurredOn: Date = new Date()
      ) {}

      get eventType(): string { return 'TaskCompleted'; }
    }

    /** 任務聚合 */
    export class Task {
      private id: string;
      private title: string;
      private description: string;
      private isCompleted: boolean = false;
      private uncommittedEvents: DomainEvent[] = [];

      static fromEvents(events: DomainEvent[]): Task {
        const task = new Task();
        events.forEach(event => task.apply(event));
        return task;
      }

      static create(id: string, title: string, description: string): Task {
        const task = new Task();
        const event = new TaskCreatedEvent(id, title, description);
        task.applyAndRecord(event);
        return task;
      }

      complete(): void {
        if (this.isCompleted) {
          throw new Error('任務已完成');
        }

        const event = new TaskCompletedEvent(this.id);
        this.applyAndRecord(event);
      }

      private applyAndRecord(event: DomainEvent): void {
        this.apply(event);
        this.uncommittedEvents.push(event);
      }

      private apply(event: DomainEvent): void {
        switch (event.eventType) {
          case 'TaskCreated':
            const createdEvent = event as TaskCreatedEvent;
            this.id = createdEvent.aggregateId;
            this.title = createdEvent.title;
            this.description = createdEvent.description;
            break;
          case 'TaskCompleted':
            this.isCompleted = true;
            break;
        }
      }

      getUncommittedEvents(): DomainEvent[] { return [...this.uncommittedEvents]; }
      markEventsAsCommitted(): void { this.uncommittedEvents = []; }
      getId(): string { return this.id; }
      getTitle(): string { return this.title; }
      getDescription(): string { return this.description; }
      getIsCompleted(): boolean { return this.isCompleted; }
    }

    /** React 元件 */
    export const TaskManager: React.FC = () => {
      const [tasks, setTasks] = useState<Task[]>([]);
      const [newTaskTitle, setNewTaskTitle] = useState('');
      const [newTaskDescription, setNewTaskDescription] = useState('');
      const eventStoreClient = useEventStoreClient();

      const loadTasks = async () => {
        try {
          /** 載入所有任務的事件並重建狀態 */
          const taskIds = await getTaskIds(); /** 假設有方法取得任務 ID 列表 */
          const loadedTasks: Task[] = [];

          for (const taskId of taskIds) {
            const events = await eventStoreClient.getEvents(taskId);
            if (events.length > 0) {
              const task = Task.fromEvents(events);
              loadedTasks.push(task);
            }
          }

          setTasks(loadedTasks);
        } catch (error) {
          console.error('載入任務失敗:', error);
        }
      };

      const createTask = async () => {
        if (!newTaskTitle.trim()) return;

        try {
          const taskId = generateId();
          const task = Task.create(taskId, newTaskTitle, newTaskDescription);

          await eventStoreClient.saveEvents(taskId, task.getUncommittedEvents());
          task.markEventsAsCommitted();

          setTasks(prev => [...prev, task]);
          setNewTaskTitle('');
          setNewTaskDescription('');
        } catch (error) {
          console.error('建立任務失敗:', error);
        }
      };

      const completeTask = async (taskId: string) => {
        try {
          const task = tasks.find(t => t.getId() === taskId);
          if (!task) return;

          task.complete();
          await eventStoreClient.saveEvents(taskId, task.getUncommittedEvents());
          task.markEventsAsCommitted();

          setTasks(prev => prev.map(t => t.getId() === taskId ? task : t));
        } catch (error) {
          console.error('完成任務失敗:', error);
        }
      };

      useEffect(() => {
        loadTasks();
      }, []);

      return (
        <div className="task-manager">
          <div className="create-task">
            <input
              type="text"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              placeholder="任務標題"
            />
            <textarea
              value={newTaskDescription}
              onChange={(e) => setNewTaskDescription(e.target.value)}
              placeholder="任務描述"
            />
            <button onClick={createTask}>建立任務</button>
          </div>

          <div className="task-list">
            {tasks.map(task => (
              <div key={task.getId()} className="task-item">
                <h3>{task.getTitle()}</h3>
                <p>{task.getDescription()}</p>
                <div className="task-status">
                  {task.getIsCompleted() ? (
                    <span className="completed">已完成</span>
                  ) : (
                    <button onClick={() => completeTask(task.getId())}>完成</button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    };
    ```

<br />

## 優點

### 完整的審計追蹤

所有變更都被記錄為事件，提供完整的歷史記錄。

### 時間旅行查詢

可以重建任意時間點的系統狀態。

### 高效能讀取

- 讀寫分離：查詢不影響寫入效能

- 多重投影：針對不同需求最佳化

- 快取友善：投影可以快取

### 可擴展性

- 事件流可以水平擴展

- 投影可以獨立擴展

- 支援微服務架構

### 業務洞察

事件流提供豐富的業務分析資料。

<br />

## 缺點

### 複雜性

相比傳統 CRUD 系統，架構更加複雜。

### 最終一致性

讀取模型可能暫時不一致。

### 事件版本管理

事件結構變更需要謹慎處理。

### 查詢限制

某些複雜查詢可能需要特殊處理。

### 儲存成本

需要儲存所有歷史事件。

<br />

## 適用場景

### 適合使用

- 金融系統：需要完整的交易記錄

- 審計要求：需要追蹤所有變更

- 複雜業務流程：狀態變化複雜

- 分析需求：需要歷史資料分析

- 高併發系統：讀寫分離需求

- 微服務架構：服務間事件通訊

### 不適合使用

- 簡單 CRUD 應用：業務規則簡單

- 即時一致性要求：不能接受最終一致性

- 資源受限環境：儲存和計算資源有限

- 團隊經驗不足：缺乏相關技術經驗

<br />

## 實施建議

### 事件設計

- 事件應該表達業務意圖，而非技術操作

- 保持事件的不可變性和向後相容性

- 包含足夠的上下文資訊

### 聚合設計

- 保持聚合的小而聚焦

- 確保業務不變條件

- 避免跨聚合的事務

### 投影管理

- 針對查詢需求設計投影

- 實作投影重建機制

- 監控投影的一致性

### 事件儲存

- 選擇適合的事件儲存技術

- 實作事件版本管理

- 考慮事件歸檔策略

### 錯誤處理

- 實作事件重播機制

- 處理毒事件 (poison events)

- 監控事件處理失敗

<br />

## 總結

Event Sourcing 是一種強大的架構模式，特別適合需要完整審計追蹤、複雜業務規則和高效能讀取的系統。雖然增加了系統複雜性，但在適當的場景下能夠提供巨大的價值。

成功實施 Event Sourcing 需要仔細的設計和規劃，包括事件模型、聚合邊界、投影策略和錯誤處理機制。團隊需要具備相關的技術知識和經驗，才能充分發揮這種架構模式的優勢。
