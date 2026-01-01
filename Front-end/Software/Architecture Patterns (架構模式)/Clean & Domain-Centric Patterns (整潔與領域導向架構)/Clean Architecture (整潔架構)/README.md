# Clean Architecture (整潔架構)

Clean Architecture (整潔架構) 是由 Robert C. Martin (Uncle Bob) 提出的軟體架構模式，目標在創建可測試、可維護、獨立於框架和外部依賴的系統。

這種架構強調關注點分離，將業務規則與外部細節 (例如：資料庫、UI、框架) 分離，使系統更容易理解、測試和修改。

<br />

## 動機

在軟體開發中，常見的問題包括

- 業務規則與技術實現緊密耦合，難以測試和修改

- 框架變更時需要大幅修改核心業務規則

- 資料庫或外部服務的變更影響整個系統

- 程式碼難以理解和維護，新功能開發困難

Clean Architecture 通過分層設計和依賴反轉，解決這些問題，讓系統具備

- 獨立性：業務規則不依賴於框架、資料庫或 UI

- 可測試性：核心功能可以獨立測試

- 可維護性：變更外部依賴不影響核心業務

- 可理解性：清晰的分層結構便於理解

<br />

## 結構

Clean Architecture 採用同心圓分層結構，從內到外分為四層

### 1. Entities (實體層)

最內層，包含企業級業務規則和核心業務物件。

- 封裝最通用和高層的規則

- 不依賴任何外部層

- 變更機率最低

### 2. Use Cases (用例層)

包含應用程式特定的業務規則。

- 協調實體之間的資料流

- 實現應用程式的用例

- 不依賴外部層的實現細節

### 3. Interface Adapters (介面適配器層)

將資料從用例和實體的格式轉換為外部代理的格式。

- 包含 Controllers、Gateways、Presenters

- 處理資料格式轉換

- 實現依賴反轉

### 4. Frameworks & Drivers (框架和驅動層)

最外層，包含框架和工具。

- Web 框架、資料庫、外部介面

- 具體的技術實現

- 變更機率最高

以下是 Clean Architecture 的層次圖

```text
┌───────────────────────────────────────────────────┐
│               Frameworks & Drivers                │
│  ┌─────────────────────────────────────────────┐  │
│  │             Interface Adapters              │  │
│  │  ┌───────────────────────────────────────┐  │  │
│  │  │               Use Cases               │  │  │
│  │  │  ┌─────────────────────────────────┐  │  │  │
│  │  │  │            Entities             │  │  │  │
│  │  │  └─────────────────────────────────┘  │  │  │
│  │  └───────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 依賴規則 (Dependency Rule)

依賴只能指向內層，外層可以依賴內層，但內層不能依賴外層。

### 依賴反轉原則 (Dependency Inversion Principle)

高層模組不應該依賴低層模組，兩者都應該依賴抽象。

### 關注點分離 (Separation of Concerns)

每一層都有明確的職責，不同關注點分離到不同層次。

<br />

## 實現方式

### Java 實現範例

以電商系統的訂單處理為例

- Entities (實體層)

    ```java
    /** 核心業務實體 */
    public class Order {
        private String id;
        private String customerId;
        private List<OrderItem> items;
        private OrderStatus status;
        private BigDecimal totalAmount;

        public Order(String customerId, List<OrderItem> items) {
            this.id = UUID.randomUUID().toString();
            this.customerId = customerId;
            this.items = items;
            this.status = OrderStatus.PENDING;
            this.totalAmount = calculateTotal();
        }

        public void confirm() {
            if (status != OrderStatus.PENDING) {
                throw new IllegalStateException("只能確認待處理的訂單");
            }
            this.status = OrderStatus.CONFIRMED;
        }

        private BigDecimal calculateTotal() {
            return items.stream()
                .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        }
    }
    ```

- Use Cases (用例層)

    ```java
    /** 用例介面 */
    public interface CreateOrderUseCase {
        OrderResponse createOrder(CreateOrderRequest request);
    }

    /** 用例實現 */
    public class CreateOrderUseCaseImpl implements CreateOrderUseCase {
        private final OrderRepository orderRepository;
        private final CustomerRepository customerRepository;
        private final NotificationService notificationService;

        public CreateOrderUseCaseImpl(
            OrderRepository orderRepository,
            CustomerRepository customerRepository,
            NotificationService notificationService
        ) {
            this.orderRepository = orderRepository;
            this.customerRepository = customerRepository;
            this.notificationService = notificationService;
        }

        @Override
        public OrderResponse createOrder(CreateOrderRequest request) {
            /** 驗證客戶存在 */
            Customer customer = customerRepository.findById(request.getCustomerId())
                .orElseThrow(() -> new CustomerNotFoundException("客戶不存在"));

            /** 驗證客戶存在 */
            Order order = new Order(request.getCustomerId(), request.getItems());

            /** 保存訂單 */
            Order savedOrder = orderRepository.save(order);

            /** 發送通知 */
            notificationService.sendOrderConfirmation(customer.getEmail(), savedOrder);

            return OrderResponse.from(savedOrder);
        }
    }
    ```

- Interface Adapters (介面適配器層)

    ```java
    /** Repository 介面 (在用例層定義) */
    public interface OrderRepository {
        Order save(Order order);
        Optional<Order> findById(String id);
    }

    /** Repository 實現 (在介面適配器層) */
    @Repository
    public class JpaOrderRepository implements OrderRepository {
        private final OrderJpaRepository jpaRepository;
        private final OrderMapper mapper;

        @Override
        public Order save(Order order) {
            OrderEntity entity = mapper.toEntity(order);
            OrderEntity saved = jpaRepository.save(entity);
            return mapper.toDomain(saved);
        }

        @Override
        public Optional<Order> findById(String id) {
            return jpaRepository.findById(id)
                .map(mapper::toDomain);
        }
    }

    /** Controller */
    @RestController
    @RequestMapping("/api/orders")
    public class OrderController {
        private final CreateOrderUseCase createOrderUseCase;

        @PostMapping
        public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
            OrderResponse response = createOrderUseCase.createOrder(request);
            return ResponseEntity.ok(response);
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Entities (實體層)

    ```typescript
    /** 核心業務實體 */
    export class User {
      constructor(
        private readonly id: string,
        private readonly email: string,
        private readonly name: string,
        private isActive: boolean = true
      ) {}

      activate(): void {
        if (this.isActive) {
          throw new Error('用戶已經是活躍狀態');
        }
        this.isActive = true;
      }

      deactivate(): void {
        if (!this.isActive) {
          throw new Error('用戶已經是非活躍狀態');
        }
        this.isActive = false;
      }

      getId(): string { return this.id; }
      getEmail(): string { return this.email; }
      getName(): string { return this.name; }
      getIsActive(): boolean { return this.isActive; }
    }
    ```

- Use Cases (用例層)

    ```typescript
    /** 用例介面 */
    export interface CreateUserUseCase {
      execute(request: CreateUserRequest): Promise<UserResponse>;
    }

    /** 用例實現 */
    export class CreateUserUseCaseImpl implements CreateUserUseCase {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly emailService: EmailService
      ) {}

      async execute(request: CreateUserRequest): Promise<UserResponse> {
        /** 檢查 email 是否已存在 */
        const existingUser = await this.userRepository.findByEmail(request.email);
        if (existingUser) {
          throw new Error('Email 已被使用');
        }

        /** 建立使用者 */
        const user = new User(
          generateId(),
          request.email,
          request.name
        );

        /** 儲存使用者 */
        const savedUser = await this.userRepository.save(user);

        /** 傳送歡迎郵件 */
        await this.emailService.sendWelcomeEmail(user.getEmail(), user.getName());

        return {
          id: savedUser.getId(),
          email: savedUser.getEmail(),
          name: savedUser.getName(),
          isActive: savedUser.getIsActive()
        };
      }
    }
    ```

- Interface Adapters (介面適配器層)

    ```typescript
    /** Repository 介面 */
    export interface UserRepository {
      save(user: User): Promise<User>;
      findById(id: string): Promise<User | null>;
      findByEmail(email: string): Promise<User | null>;
    }

    /** Repository 實作 */
    export class MongoUserRepository implements UserRepository {
      constructor(private readonly userModel: Model<UserDocument>) {}

      async save(user: User): Promise<User> {
        const userDoc = new this.userModel({
          _id: user.getId(),
          email: user.getEmail(),
          name: user.getName(),
          isActive: user.getIsActive()
        });

        await userDoc.save();
        return user;
      }

      async findByEmail(email: string): Promise<User | null> {
        const doc = await this.userModel.findOne({ email });
        return doc ? this.mapToUser(doc) : null;
      }

      private mapToUser(doc: UserDocument): User {
        return new User(doc._id, doc.email, doc.name, doc.isActive);
      }
    }

    /** Controller */
    export class UserController {
      constructor(private readonly createUserUseCase: CreateUserUseCase) {}

      async createUser(req: Request, res: Response): Promise<void> {
        try {
          const response = await this.createUserUseCase.execute(req.body);
          res.status(201).json(response);
        } catch (error) {
          res.status(400).json({ error: error.message });
        }
      }
    }
    ```

### React 前端實現範例

- Entities (實體層)

    ```typescript
    /** 領域實體 */
    export class TodoItem {
      constructor(
        private readonly id: string,
        private title: string,
        private completed: boolean = false,
        private readonly createdAt: Date = new Date()
      ) {}

      complete(): void {
        if (this.completed) {
          throw new Error('待辦事項已完成');
        }
        this.completed = true;
      }

      updateTitle(newTitle: string): void {
        if (!newTitle.trim()) {
          throw new Error('標題不能為空');
        }
        this.title = newTitle.trim();
      }

      getId(): string { return this.id; }
      getTitle(): string { return this.title; }
      isCompleted(): boolean { return this.completed; }
      getCreatedAt(): Date { return this.createdAt; }
    }
    ```

- Use Cases (用例層)

    ```typescript
    /** 用例實作 */
    export class TodoUseCases {
      constructor(private readonly todoRepository: TodoRepository) {}

      async createTodo(title: string): Promise<TodoItem> {
        const todo = new TodoItem(generateId(), title);
        return await this.todoRepository.save(todo);
      }

      async completeTodo(id: string): Promise<void> {
        const todo = await this.todoRepository.findById(id);
        if (!todo) {
          throw new Error('待辦事項不存在');
        }
        todo.complete();
        await this.todoRepository.save(todo);
      }

      async getAllTodos(): Promise<TodoItem[]> {
        return await this.todoRepository.findAll();
      }
    }
    ```

- Interface Adapters (介面適配器層)

    ```typescript
    /** Repository 介面 */
    export interface TodoRepository {
      save(todo: TodoItem): Promise<TodoItem>;
      findById(id: string): Promise<TodoItem | null>;
      findAll(): Promise<TodoItem[]>;
    }

    /** API Repository 實作 */
    export class ApiTodoRepository implements TodoRepository {
      constructor(private readonly httpClient: HttpClient) {}

      async save(todo: TodoItem): Promise<TodoItem> {
        const response = await this.httpClient.post('/api/todos', {
          id: todo.getId(),
          title: todo.getTitle(),
          completed: todo.isCompleted()
        });
        return this.mapToTodoItem(response.data);
      }

      async findAll(): Promise<TodoItem[]> {
        const response = await this.httpClient.get('/api/todos');
        return response.data.map(this.mapToTodoItem);
      }

      private mapToTodoItem(data: any): TodoItem {
        return new TodoItem(data.id, data.title, data.completed, new Date(data.createdAt));
      }
    }
    ```

- Frameworks & Drivers (框架與驅動程式層)

    ```typescript
    /** React 元件 */
    export const TodoList: React.FC = () => {
      const [todos, setTodos] = useState<TodoItem[]>([]);
      const [newTodoTitle, setNewTodoTitle] = useState('');
      const todoUseCases = useTodoUseCases();

      useEffect(() => {
        loadTodos();
      }, []);

      const loadTodos = async () => {
        try {
          const todoList = await todoUseCases.getAllTodos();
          setTodos(todoList);
        } catch (error) {
          console.error('載入待辦事項失敗:', error);
        }
      };

      const handleCreateTodo = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newTodoTitle.trim()) return;

        try {
          await todoUseCases.createTodo(newTodoTitle);
          setNewTodoTitle('');
          await loadTodos();
        } catch (error) {
          console.error('建立待辦事項失敗:', error);
        }
      };

      const handleCompleteTodo = async (id: string) => {
        try {
          await todoUseCases.completeTodo(id);
          await loadTodos();
        } catch (error) {
          console.error('完成待辦事項失敗:', error);
        }
      };

      return (
        <div className="todo-list">
          <form onSubmit={handleCreateTodo}>
            <input
              type="text"
              value={newTodoTitle}
              onChange={(e) => setNewTodoTitle(e.target.value)}
              placeholder="輸入新的待辦事項"
            />
            <button type="submit">新增</button>
          </form>

          <ul>
            {todos.map((todo) => (
              <li key={todo.getId()}>
                <span className={todo.isCompleted() ? 'completed' : ''}>
                  {todo.getTitle()}
                </span>
                {!todo.isCompleted() && (
                  <button onClick={() => handleCompleteTodo(todo.getId())}>完成</button>
                )}
              </li>
            ))}
          </ul>
        </div>
      );
    };
    ```

<br />

## 優點

### 可測試性

每一層都可以獨立測試，特別是業務規則可以在沒有外部依賴的情況下進行測試。

### 獨立性

- 框架獨立：不依賴特定框架

- 資料庫獨立：可以輕鬆切換資料庫

- UI 獨立：可以更換使用者介面

- 外部服務獨立：可以替換外部 API

### 可維護性

清晰的分層結構使得程式碼更容易理解和維護。

### 可擴展性

新功能可以在不影響現有程式碼的情況下添加。

<br />

## 缺點

### 複雜性

對於簡單的應用程式來說可能過於複雜。

### 學習曲線

需要團隊成員理解架構原則和設計模式。

### 初期開發成本

需要更多的前期設計和程式碼結構規劃。

### 過度工程化風險

可能會為簡單問題創造過於複雜的解決方案。

<br />

## 適用場景

### 適合使用

- 大型企業應用：需要長期維護和擴展

- 複雜業務規則：有複雜的業務流程和規則

- 多平台支援：需要支援多種使用者介面

- 團隊協作：多個團隊同時開發

- 高品質要求：對程式碼品質和可測試性要求高

### 不適合使用

- 簡單 CRUD 應用：只有基本的增刪改查功能

- 原型開發：快速驗證想法的專案

- 小型專案：團隊規模小且需求簡單

- 時間緊迫：需要快速交付的專案

<br />

## 實施建議

### 漸進式採用

不需要一開始就完全按照 Clean Architecture 實作，可以從核心業務開始，逐步重構。

### 團隊培訓

確保團隊成員理解架構原則和設計模式。

### 程式碼審查

建立程式碼審查機制，確保架構原則得到遵循。

### 自動化測試

建立完整的測試套件，特別是業務規則的單元測試。

### 文件化

維護清晰的架構文件和設計決策記錄。

<br />

## 總結

Clean Architecture 提供了一個強大的框架來組織程式碼，特別適合需要長期維護和擴展的複雜應用程式。雖然初期投入較高，但長期來看能夠顯著提升程式碼品質、可測試性和可維護性。

關鍵在於根據專案的實際需求來決定是否採用，以及採用的程度。對於簡單的應用程式，可能不需要完整的 Clean Architecture；但對於複雜的企業級應用，這種架構模式能夠帶來巨大的價值。
