# Modular Monolith Architecture (模組化單體架構)

Modular Monolith Architecture (模組化單體架構) 是一種將單體應用程式組織成鬆散耦合、高內聚模組的架構模式，結合了單體架構的簡單性與微服務架構的模組化優勢。

這種架構強調模組邊界的清晰定義，每個模組都有明確的職責和介面，使系統更容易理解、測試和維護，同時保持部署的簡單性。

<br />

## 動機

在軟體開發中，傳統單體架構常見的問題包括

- 程式碼耦合度高，修改一個功能可能影響其他功能

- 團隊協作困難，多人同時開發容易產生衝突

- 技術債務累積，程式碼結構逐漸惡化

- 測試困難，單元測試和整合測試複雜

- 擴展性差，難以針對特定功能進行優化

Modular Monolith 通過模組化設計和清晰的邊界定義，解決這些問題，讓系統具備

- 模組化：清晰的模組邊界和職責分離

- 可維護性：每個模組可以獨立開發和測試

- 可擴展性：可以逐步演進為微服務架構

- 簡單性：保持單體架構的部署和運維優勢

<br />

## 結構

Modular Monolith 採用模組化分層結構，通常包含以下層次

### 1. Presentation Layer (展示層)

處理使用者介面和外部請求。

- API Controllers、Web UI、CLI 介面

- 請求驗證和回應格式化

- 路由和中介軟體

### 2. Application Layer (應用層)

協調不同模組之間的互動。

- 應用服務和工作流程

- 跨模組的業務流程

- 事件處理和訊息傳遞

### 3. Domain Modules (領域模組)

核心業務功能的模組化實現。

- 每個模組包含完整的業務功能

- 模組間通過定義良好的介面通訊

- 包含實體、值物件、領域服務

### 4. Infrastructure Layer (基礎設施層)

提供技術實現和外部整合。

- 資料庫存取、外部 API 整合

- 快取、訊息佇列、檔案系統

- 設定管理和監控

以下是 Modular Monolith 的架構圖

```text
┌─────────────────────────────────────────────────────────────────┐
│                       Presentation Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                        Application Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐        │
│  │    Module A   │  │    Module B   │  │    Module C   │   ...  │
│  │               │  │               │  │               │        │
│  │  ┌─────────┐  │  │  ┌─────────┐  │  │  ┌─────────┐  │        │
│  │  │ Domain  │  │  │  │ Domain  │  │  │  │ Domain  │  │        │
│  │  │ Service │  │  │  │ Service │  │  │  │ Service │  │        │
│  │  └─────────┘  │  │  └─────────┘  │  │  └─────────┘  │        │
│  │  ┌──────────┐ │  │  ┌──────────┐ │  │  ┌──────────┐ │        │
│  │  │Repository│ │  │  │Repository│ │  │  │Repository│ │        │
│  │  └──────────┘ │  │  └──────────┘ │  │  └──────────┘ │        │
│  └───────────────┘  └───────────────┘  └───────────────┘        │
├─────────────────────────────────────────────────────────────────┤
│                       Infrastructure Layer                      │
└─────────────────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 模組自治 (Module Autonomy)

每個模組應該能夠獨立開發、測試和部署。

### 明確邊界 (Clear Boundaries)

模組之間的介面應該明確定義，避免直接存取內部實現。

### 鬆散耦合 (Loose Coupling)

模組之間的依賴應該最小化，通過介面和事件進行通訊。

### 高內聚 (High Cohesion)

相關的功能應該組織在同一個模組內。

<br />

## 實現方式

### Java 實現範例

以電商系統為例，包含訂單、產品、使用者三個模組

- 模組結構

    ```text
    src/
    ├── main/
    │   ├── java/
    │   │   ├── com/ecommerce/
    │   │   │   ├── shared/                 共享元件
    │   │   │   │   ├── events/
    │   │   │   │   └── exceptions/
    │   │   │   ├── user/                   使用者模組
    │   │   │   │   ├── domain/
    │   │   │   │   ├── application/
    │   │   │   │   └── infrastructure/
    │   │   │   ├── product                 產品模組
    │   │   │   │   ├── domain/
    │   │   │   │   ├── application/
    │   │   │   │   └── infrastructure/
    │   │   │   └── order/                  訂單模組
    │   │   │       ├── domain/
    │   │   │       ├── application/
    │   │   │       └── infrastructure/
    ```

- 使用者模組實現

    ```java
    /** 使用者領域實體 */
    @Entity
    public class User {
        @Id
        private String id;
        private String email;
        private String name;
        private UserStatus status;

        public User(String email, String name) {
            this.id = UUID.randomUUID().toString();
            this.email = email;
            this.name = name;
            this.status = UserStatus.ACTIVE;
        }

        public void deactivate() {
            if (status == UserStatus.INACTIVE) {
                throw new IllegalStateException("使用者已經是非活躍狀態");
            }
            this.status = UserStatus.INACTIVE;
        }
    }

    /** 使用者應用服務 */
    @Service
    @Transactional
    public class UserApplicationService {
        private final UserRepository userRepository;
        private final ApplicationEventPublisher eventPublisher;

        public UserDto createUser(CreateUserCommand command) {
            /** 檢查 email 是否已存在 */
            if (userRepository.existsByEmail(command.getEmail())) {
                throw new UserAlreadyExistsException("Email 已被使用");
            }

            /** 建立使用者 */
            User user = new User(command.getEmail(), command.getName());
            User savedUser = userRepository.save(user);

            /** 發布事件 */
            eventPublisher.publishEvent(new UserCreatedEvent(savedUser.getId(), savedUser.getEmail()));

            return UserDto.from(savedUser);
        }
    }

    /** 使用者模組介面 */
    public interface UserModuleApi {
        UserDto getUserById(String userId);
        boolean isUserActive(String userId);
        void deactivateUser(String userId);
    }

    /** 使用者模組實現 */
    @Component
    public class UserModuleImpl implements UserModuleApi {
        private final UserRepository userRepository;

        @Override
        public UserDto getUserById(String userId) {
            User user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("使用者不存在"));
            return UserDto.from(user);
        }

        @Override
        public boolean isUserActive(String userId) {
            return userRepository.findById(userId)
                .map(user -> user.getStatus() == UserStatus.ACTIVE)
                .orElse(false);
        }
    }
    ```

- 訂單模組實現

    ```java
    /** 訂單領域實體 */
    @Entity
    public class Order {
        @Id
        private String id;
        private String userId;
        private List<OrderItem> items;
        private OrderStatus status;
        private BigDecimal totalAmount;

        public Order(String userId, List<OrderItem> items) {
            this.id = UUID.randomUUID().toString();
            this.userId = userId;
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
    }

    /** 訂單應用服務 */
    @Service
    @Transactional
    public class OrderApplicationService {
        private final OrderRepository orderRepository;
        private final UserModuleApi userModule;
        private final ProductModuleApi productModule;
        private final ApplicationEventPublisher eventPublisher;

        public OrderDto createOrder(CreateOrderCommand command) {
            /** 驗證使用者 */
            if (!userModule.isUserActive(command.getUserId())) {
                throw new InactiveUserException("使用者未啟用");
            }

            /** 驗證產品 */
            List<OrderItem> items = command.getItems().stream()
                .map(this::validateAndCreateOrderItem)
                .collect(Collectors.toList());

            /** 建立訂單 */
            Order order = new Order(command.getUserId(), items);
            Order savedOrder = orderRepository.save(order);

            /** 發布事件 */
            eventPublisher.publishEvent(new OrderCreatedEvent(savedOrder.getId(), savedOrder.getUserId()));

            return OrderDto.from(savedOrder);
        }

        private OrderItem validateAndCreateOrderItem(CreateOrderItemCommand command) {
            ProductDto product = productModule.getProductById(command.getProductId());
            if (!product.isAvailable()) {
                throw new ProductNotAvailableException("產品不可用");
            }
            return new OrderItem(command.getProductId(), command.getQuantity(), product.getPrice());
        }
    }
    ```

- 模組間通訊 (事件驅動)

    ```java
    /** 共享事件 */
    public class UserCreatedEvent {
        private final String userId;
        private final String email;
        private final Instant timestamp;

        public UserCreatedEvent(String userId, String email) {
            this.userId = userId;
            this.email = email;
            this.timestamp = Instant.now();
        }
    }

    /** 事件處理器 */
    @Component
    public class OrderEventHandler {
        private final EmailService emailService;

        @EventListener
        @Async
        public void handleUserCreated(UserCreatedEvent event) {
            /** 發送歡迎郵件 */
            emailService.sendWelcomeEmail(event.getEmail());
        }

        @EventListener
        @Async
        public void handleOrderCreated(OrderCreatedEvent event) {
            /** 發送訂單確認郵件 */
            emailService.sendOrderConfirmation(event.getOrderId());
        }
    }
    ```

### Node.js 與 TypeScript 實現範例

- 模組結構

    ```text
    src/
    ├── shared/
    │   ├── events/
    │   ├── interfaces/
    │   └── exceptions/
    ├── modules/
    │   ├── user/
    │   │   ├── domain/
    │   │   ├── application/
    │   │   ├── infrastructure/
    │   │   └── index.ts
    │   ├── product/
    │   │   ├── domain/
    │   │   ├── application/
    │   │   ├── infrastructure/
    │   │   └── index.ts
    │   └── order/
    │       ├── domain/
    │       ├── application/
    │       ├── infrastructure/
    │       └── index.ts
    └── app.ts
    ```

- 使用者模組實現

    ```typescript
    /** 使用者領域實體 */
    export class User {
      constructor(
        private readonly id: string,
        private readonly email: string,
        private readonly name: string,
        private status: UserStatus = UserStatus.ACTIVE
      ) {}

      deactivate(): void {
        if (this.status === UserStatus.INACTIVE) {
          throw new Error('使用者已經是非活躍狀態');
        }
        this.status = UserStatus.INACTIVE;
      }

      getId(): string { return this.id; }
      getEmail(): string { return this.email; }
      getName(): string { return this.name; }
      getStatus(): UserStatus { return this.status; }
    }

    /** 使用者應用服務 */
    export class UserApplicationService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly eventBus: EventBus
      ) {}

      async createUser(command: CreateUserCommand): Promise<UserDto> {
        /** 檢查 email 是否已存在 */
        const existingUser = await this.userRepository.findByEmail(command.email);
        if (existingUser) {
          throw new UserAlreadyExistsError('Email 已被使用');
        }

        /** 建立使用者 */
        const user = new User(
          generateId(),
          command.email,
          command.name
        );

        const savedUser = await this.userRepository.save(user);

        /** 發布事件 */
        await this.eventBus.publish(new UserCreatedEvent(savedUser.getId(), savedUser.getEmail()));

        return {
          id: savedUser.getId(),
          email: savedUser.getEmail(),
          name: savedUser.getName(),
          status: savedUser.getStatus()
        };
      }
    }

    /** 使用者模組介面 */
    export interface UserModuleApi {
      getUserById(userId: string): Promise<UserDto | null>;
      isUserActive(userId: string): Promise<boolean>;
      deactivateUser(userId: string): Promise<void>;
    }

    /** 使用者模組實現 */
    export class UserModule implements UserModuleApi {
      constructor(private readonly userRepository: UserRepository) {}

      async getUserById(userId: string): Promise<UserDto | null> {
        const user = await this.userRepository.findById(userId);
        return user ? {
          id: user.getId(),
          email: user.getEmail(),
          name: user.getName(),
          status: user.getStatus()
        } : null;
      }

      async isUserActive(userId: string): Promise<boolean> {
        const user = await this.userRepository.findById(userId);
        return user ? user.getStatus() === UserStatus.ACTIVE : false;
      }
    }
    ```

- 訂單模組實現

    ```typescript
    /** 訂單應用服務 */
    export class OrderApplicationService {
      constructor(
        private readonly orderRepository: OrderRepository,
        private readonly userModule: UserModuleApi,
        private readonly productModule: ProductModuleApi,
        private readonly eventBus: EventBus
      ) {}

      async createOrder(command: CreateOrderCommand): Promise<OrderDto> {
        /** 驗證使用者 */
        const isUserActive = await this.userModule.isUserActive(command.userId);
        if (!isUserActive) {
          throw new InactiveUserError('使用者未啟用');
        }

        /** 驗證產品並建立訂單項目 */
        const items: OrderItem[] = [];
        for (const itemCommand of command.items) {
          const product = await this.productModule.getProductById(itemCommand.productId);
          if (!product || !product.isAvailable) {
            throw new ProductNotAvailableError('產品不可用');
          }
          items.push(new OrderItem(itemCommand.productId, itemCommand.quantity, product.price));
        }

        /** 建立訂單 */
        const order = new Order(generateId(), command.userId, items);
        const savedOrder = await this.orderRepository.save(order);

        /** 發布事件 */
        await this.eventBus.publish(new OrderCreatedEvent(savedOrder.getId(), savedOrder.getUserId()));

        return {
          id: savedOrder.getId(),
          userId: savedOrder.getUserId(),
          items: savedOrder.getItems().map(item => ({
            productId: item.getProductId(),
            quantity: item.getQuantity(),
            price: item.getPrice()
          })),
          status: savedOrder.getStatus(),
          totalAmount: savedOrder.getTotalAmount()
        };
      }
    }
    ```

- 模組註冊和依賴注入

    ```typescript
    /** 依賴注入容器 */
    export class DIContainer {
      private readonly services = new Map<string, any>();

      register<T>(key: string, factory: () => T): void {
        this.services.set(key, factory);
      }

      resolve<T>(key: string): T {
        const factory = this.services.get(key);
        if (!factory) {
          throw new Error(`Service ${key} not found`);
        }
        return factory();
      }
    }

    /** 應用程式啟動 */
    export class Application {
      private readonly container = new DIContainer();

      async start(): Promise<void> {
        /** 註冊基礎設施服務 */
        this.container.register('eventBus', () => new InMemoryEventBus());
        this.container.register('userRepository', () => new MongoUserRepository());
        this.container.register('productRepository', () => new MongoProductRepository());
        this.container.register('orderRepository', () => new MongoOrderRepository());

        /** 註冊模組 */
        this.container.register('userModule', () => new UserModule(
          this.container.resolve('userRepository')
        ));

        this.container.register('productModule', () => new ProductModule(
          this.container.resolve('productRepository')
        ));

        this.container.register('orderModule', () => new OrderModule(
          this.container.resolve('orderRepository'),
          this.container.resolve('userModule'),
          this.container.resolve('productModule')
        ));

        /** 啟動 Web 伺服器 */
        const app = express();
        this.setupRoutes(app);
        app.listen(3000, () => {
          console.log('應用程式已啟動在 port 3000');
        });
      }
    }
    ```

### React 前端實現範例

- 模組結構

    ```text
    src/
    ├── shared/
    │   ├── components/
    │   ├── hooks/
    │   └── types/
    ├── modules/
    │   ├── user/
    │   │   ├── components/
    │   │   ├── hooks/
    │   │   ├── services/
    │   │   └── types/
    │   ├── product/
    │   │   ├── components/
    │   │   ├── hooks/
    │   │   ├── services/
    │   │   └── types/
    │   └── order/
    │       ├── components/
    │       ├── hooks/
    │       ├── services/
    │       └── types/
    └── App.tsx
    ```

- 使用者模組實現

    ```typescript
    /** 使用者服務 */
    export class UserService {
      constructor(private readonly httpClient: HttpClient) {}

      async createUser(userData: CreateUserRequest): Promise<User> {
        const response = await this.httpClient.post('/api/users', userData);
        return response.data;
      }

      async getUserById(userId: string): Promise<User> {
        const response = await this.httpClient.get(`/api/users/${userId}`);
        return response.data;
      }
    }

    /** 使用者 Hook */
    export const useUser = () => {
      const [users, setUsers] = useState<User[]>([]);
      const [loading, setLoading] = useState(false);
      const userService = useUserService();

      const createUser = async (userData: CreateUserRequest) => {
        setLoading(true);
        try {
          const newUser = await userService.createUser(userData);
          setUsers(prev => [...prev, newUser]);
          return newUser;
        } finally {
          setLoading(false);
        }
      };

      return {
        users,
        loading,
        createUser
      };
    };

    /** 使用者元件 */
    export const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {
      const [user, setUser] = useState<User | null>(null);
      const userService = useUserService();

      useEffect(() => {
        userService.getUserById(userId).then(setUser);
      }, [userId]);

      if (!user) return <div>載入中...</div>;

      return (
        <div className="user-profile">
          <h2>{user.name}</h2>
          <p>Email: {user.email}</p>
          <p>狀態: {user.status}</p>
        </div>
      );
    };
    ```

<br />

## 優點

### 模組化優勢

每個模組都有清晰的邊界和職責，便於理解和維護。

### 團隊協作

不同團隊可以並行開發不同模組，減少衝突。

### 漸進式演進

可以逐步將模組拆分為獨立的微服務。

### 部署簡單

保持單體架構的部署優勢，避免分散式系統的複雜性。

### 效能優勢

模組間通訊不需要網路呼叫，效能較微服務架構好。

### 測試便利

可以針對單個模組進行獨立測試，也可以進行整合測試。

<br />

## 缺點

### 模組邊界維護

需要持續維護模組邊界，防止耦合度增加。

### 技術棧限制

所有模組必須使用相同的技術棧和程式語言。

### 擴展限制

無法針對單個模組進行獨立擴展。

### 部署風險

一個模組的問題可能影響整個應用程式。

### 資料庫共享

通常需要共享資料庫，可能產生資料耦合。

<br />

## 適用場景

### 適合使用

- 中大型應用：功能複雜但不需要微服務的完整複雜性

- 團隊協作：多個團隊需要並行開發

- 演進需求：未來可能需要拆分為微服務

- 效能要求：需要較好的效能表現

- 運維能力有限：不具備微服務的運維能力

### 不適合使用

- 簡單應用：功能簡單的小型應用

- 高度分散：需要獨立部署和擴展的場景

- 技術多樣性：需要使用不同技術棧的場景

- 極致效能：對單一功能有極高效能要求

<br />

## 實施建議

### 模組設計原則

根據業務領域劃分模組，確保高內聚、低耦合。

### 介面設計

定義清晰的模組介面，避免直接存取內部實現。

### 事件驅動通訊

使用事件驅動模式實現模組間的鬆散耦合。

### 資料隔離

盡可能實現資料隔離，避免跨模組的直接資料存取。

### 測試策略

建立完整的測試策略，包括單元測試、整合測試和端到端測試。

### 監控和觀測

實施適當的監控和觀測機制，追蹤模組間的互動。

<br />

## 總結

Modular Monolith Architecture 提供了一個平衡的解決方案，結合了單體架構的簡單性和微服務架構的模組化優勢。這種架構特別適合需要模組化但不需要完整微服務複雜性的應用程式。

關鍵在於維護清晰的模組邊界和介面設計，確保系統的可維護性和可擴展性。隨著系統的成長，可以逐步演進為微服務架構，使其成為一個很好的過渡方案。
