# Domain-Driven Design (DDD) Architecture (領域驅動設計架構)

Domain-Driven Design (領域驅動設計架構) 是由 Eric Evans 提出的軟體開發方法論，專注於複雜業務領域的建模和實現。

這種架構強調深入理解業務領域，通過領域模型驅動軟體設計，將複雜的業務規則和概念轉化為可維護的程式碼結構。

<br />

## 動機

在複雜業務系統開發中，常見的問題包括

- 業務專家與開發團隊之間存在溝通障礙

- 業務規則分散在各處，難以維護和理解

- 程式碼結構與實際業務流程不符

- 領域知識流失，系統演進困難

DDD 通過建立統一語言和領域模型，解決這些問題，讓系統具備

- 業務導向：程式碼直接反映業務概念和規則

- 可理解性：技術人員和業務專家使用相同語言

- 可維護性：領域模型集中管理業務規則

- 可演進性：隨業務變化調整模型結構

<br />

## 核心概念

### Ubiquitous Language (統一語言)

團隊成員 (包括業務專家、開發人員、測試人員) 使用的共同語言。

- 消除溝通歧義

- 程式碼中的類別、方法名稱直接對應業務術語

- 文件和對話使用相同詞彙

### Bounded Context (界限上下文)

明確定義領域模型適用的邊界。

- 每個上下文內部保持模型一致性

- 不同上下文可以有不同的模型表示

- 避免大泥球 (Big Ball of Mud) 問題

### Domain Model (領域模型)

業務領域的抽象表示。

- 封裝業務規則和行為

- 反映真實世界的業務概念

- 獨立於技術實現細節

<br />

## 戰術模式

### Entity (實體)

具有唯一識別的領域物件。

- 擁有生命週期

- 身份識別比屬性更重要

- 封裝業務行為

### Value Object (值物件)

沒有唯一識別的不可變物件。

- 通過屬性值定義相等性

- 不可變性保證資料一致性

- 可以被共享和替換

### Aggregate (聚合)

相關物件的集合，作為資料變更的單位。

- 維護業務不變條件

- 定義事務邊界

- 通過 Aggregate Root 存取

### Repository (儲存庫)

提供類似集合的介面來存取聚合。

- 封裝資料存取細節

- 支援查詢和持久化

- 維護領域模型的純淨性

### Domain Service (領域服務)

不屬於特定實體或值物件的業務操作。

- 處理跨多個聚合的業務流程

- 保持無狀態

- 專注於業務概念

### Domain Event (領域事件)

領域中發生的重要業務事件。

- 解耦不同聚合間的互動

- 支援事件驅動架構

- 記錄業務狀態變化

<br />

## 架構分層

DDD 採用分層架構，從上到下分為四層

### 1. User Interface Layer (使用者介面層)

處理使用者互動和資料展示。

- Web Controllers、REST API

- 資料格式轉換

- 使用者輸入驗證

### 2. Application Layer (應用層)

協調領域物件執行應用程式任務。

- Application Services

- 事務管理

- 安全性控制

### 3. Domain Layer (領域層)

包含業務概念、規則和流程。

- Entities、Value Objects、Aggregates

- Domain Services、Domain Events

- 業務規則和不變條件

### 4. Infrastructure Layer (基礎設施層)

提供技術支援服務。

- 資料庫存取、外部 API 呼叫

- 訊息佇列、快取

- 技術框架和工具

以下是 DDD 的分層架構圖

```text
┌────────────────────────────────────────────┐
│            User Interface Layer            │
├────────────────────────────────────────────┤
│             Application Layer              │
├────────────────────────────────────────────┤
│               Domain Layer                 │
├────────────────────────────────────────────┤
│            Infrastructure Layer            │
└────────────────────────────────────────────┘
```

<br />

## 實現方式

### Java 實現範例

以電商系統的訂單管理為例：

- Entity (實體)

    ```java
    /** 訂單實體 */
    public class Order {
        private OrderId id;
        private CustomerId customerId;
        private List<OrderLine> orderLines;
        private OrderStatus status;
        private Money totalAmount;
        private LocalDateTime createdAt;

        public Order(CustomerId customerId, List<OrderLine> orderLines) {
            this.id = OrderId.generate();
            this.customerId = Objects.requireNonNull(customerId);
            this.orderLines = new ArrayList<>(orderLines);
            this.status = OrderStatus.PENDING;
            this.totalAmount = calculateTotal();
            this.createdAt = LocalDateTime.now();

            validateOrder();
        }

        public void confirm() {
            if (!canBeConfirmed()) {
                throw new IllegalStateException("訂單無法確認");
            }
            this.status = OrderStatus.CONFIRMED;

            /** 發布領域事件 */
            DomainEventPublisher.publish(new OrderConfirmedEvent(this.id));
        }

        public void cancel(String reason) {
            if (!canBeCancelled()) {
                throw new IllegalStateException("訂單無法取消");
            }
            this.status = OrderStatus.CANCELLED;

            DomainEventPublisher.publish(new OrderCancelledEvent(this.id, reason));
        }

        private boolean canBeConfirmed() {
            return status == OrderStatus.PENDING && !orderLines.isEmpty();
        }

        private boolean canBeCancelled() {
            return status == OrderStatus.PENDING || status == OrderStatus.CONFIRMED;
        }

        private Money calculateTotal() {
            return orderLines.stream()
                .map(OrderLine::getSubtotal)
                .reduce(Money.ZERO, Money::add);
        }

        private void validateOrder() {
            if (orderLines.isEmpty()) {
                throw new IllegalArgumentException("訂單必須包含至少一個商品");
            }
        }

        /** Getters */
        public OrderId getId() { return id; }
        public CustomerId getCustomerId() { return customerId; }
        public OrderStatus getStatus() { return status; }
        public Money getTotalAmount() { return totalAmount; }
    }
    ```

- Value Object (值物件)

    ```java
    /** 訂單 ID 值物件 */
    public class OrderId {
        private final String value;

        private OrderId(String value) {
            if (value == null || value.trim().isEmpty()) {
                throw new IllegalArgumentException("訂單 ID 不能為空");
            }
            this.value = value;
        }

        public static OrderId of(String value) {
            return new OrderId(value);
        }

        public static OrderId generate() {
            return new OrderId(UUID.randomUUID().toString());
        }

        public String getValue() {
            return value;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            OrderId orderId = (OrderId) obj;
            return Objects.equals(value, orderId.value);
        }

        @Override
        public int hashCode() {
            return Objects.hash(value);
        }
    }

    /** 金額值物件 */
    public class Money {
        public static final Money ZERO = new Money(BigDecimal.ZERO, Currency.getInstance("TWD"));

        private final BigDecimal amount;
        private final Currency currency;

        public Money(BigDecimal amount, Currency currency) {
            this.amount = Objects.requireNonNull(amount);
            this.currency = Objects.requireNonNull(currency);

            if (amount.compareTo(BigDecimal.ZERO) < 0) {
                throw new IllegalArgumentException("金額不能為負數");
            }
        }

        public Money add(Money other) {
            if (!currency.equals(other.currency)) {
                throw new IllegalArgumentException("無法加總不同幣別的金額");
            }
            return new Money(amount.add(other.amount), currency);
        }

        public Money multiply(int quantity) {
            return new Money(amount.multiply(BigDecimal.valueOf(quantity)), currency);
        }

        // Getters and equals/hashCode methods
    }
    ```

- Aggregate (聚合)

    ```java
    /** 訂單聚合根 */
    public class OrderAggregate {
        private Order order;
        private List<OrderLine> orderLines;
        private Customer customer;

        public OrderAggregate(Order order, List<OrderLine> orderLines, Customer customer) {
            this.order = Objects.requireNonNull(order);
            this.orderLines = new ArrayList<>(orderLines);
            this.customer = Objects.requireNonNull(customer);
        }

        public void addOrderLine(Product product, int quantity) {
            if (order.getStatus() != OrderStatus.PENDING) {
                throw new IllegalStateException("只能修改待處理的訂單");
            }

            OrderLine newLine = new OrderLine(product.getId(), product.getPrice(), quantity);
            orderLines.add(newLine);

            /** 重新計算訂單總額 */
            order.recalculateTotal(orderLines);
        }

        public void removeOrderLine(ProductId productId) {
            if (order.getStatus() != OrderStatus.PENDING) {
                throw new IllegalStateException("只能修改待處理的訂單");
            }

            orderLines.removeIf(line -> line.getProductId().equals(productId));
            order.recalculateTotal(orderLines);
        }

        public void confirmOrder() {
            validateCustomerCanOrder();
            order.confirm();
        }

        private void validateCustomerCanOrder() {
            if (!customer.isActive()) {
                throw new IllegalStateException("客戶帳戶未啟用");
            }
            if (customer.hasOutstandingPayments()) {
                throw new IllegalStateException("客戶有未付款項");
            }
        }

        /** Getters */
        public Order getOrder() { return order; }
        public List<OrderLine> getOrderLines() { return new ArrayList<>(orderLines); }
    }
    ```

- Repository (儲存庫)

    ```java
    /** 訂單儲存庫介面 */
    public interface OrderRepository {
        void save(OrderAggregate orderAggregate);
        Optional<OrderAggregate> findById(OrderId orderId);
        List<OrderAggregate> findByCustomerId(CustomerId customerId);
        List<OrderAggregate> findByStatus(OrderStatus status);
    }

    /** JPA 實現 */
    @Repository
    public class JpaOrderRepository implements OrderRepository {
        private final OrderJpaRepository jpaRepository;
        private final OrderMapper mapper;

        @Override
        public void save(OrderAggregate orderAggregate) {
            OrderEntity entity = mapper.toEntity(orderAggregate);
            jpaRepository.save(entity);
        }

        @Override
        public Optional<OrderAggregate> findById(OrderId orderId) {
            return jpaRepository.findById(orderId.getValue())
                .map(mapper::toDomain);
        }

        @Override
        public List<OrderAggregate> findByCustomerId(CustomerId customerId) {
            return jpaRepository.findByCustomerId(customerId.getValue())
                .stream()
                .map(mapper::toDomain)
                .collect(Collectors.toList());
        }
    }
    ```

- Domain Service (領域服務)

    ```java
    /** 訂單定價服務 */
    @Service
    public class OrderPricingService {
        private final DiscountRepository discountRepository;
        private final TaxCalculationService taxService;

        public Money calculateOrderTotal(List<OrderLine> orderLines, CustomerId customerId) {
            Money subtotal = calculateSubtotal(orderLines);
            Money discount = calculateDiscount(subtotal, customerId);
            Money afterDiscount = subtotal.subtract(discount);
            Money tax = taxService.calculateTax(afterDiscount);

            return afterDiscount.add(tax);
        }

        private Money calculateSubtotal(List<OrderLine> orderLines) {
            return orderLines.stream()
                .map(OrderLine::getSubtotal)
                .reduce(Money.ZERO, Money::add);
        }

        private Money calculateDiscount(Money subtotal, CustomerId customerId) {
            List<Discount> applicableDiscounts = discountRepository
                .findApplicableDiscounts(customerId, subtotal);

            return applicableDiscounts.stream()
                .map(discount -> discount.calculateDiscount(subtotal))
                .reduce(Money.ZERO, Money::add);
        }
    }
    ```

- Application Service (應用服務)

    ```java
    /** 訂單應用服務 */
    @Service
    @Transactional
    public class OrderApplicationService {
        private final OrderRepository orderRepository;
        private final CustomerRepository customerRepository;
        private final ProductRepository productRepository;
        private final OrderPricingService pricingService;
        private final DomainEventPublisher eventPublisher;

        public OrderDto createOrder(CreateOrderCommand command) {
            /** 驗證客戶 */
            Customer customer = customerRepository.findById(command.getCustomerId())
                .orElseThrow(() -> new CustomerNotFoundException("客戶不存在"));

            /** 驗證商品 */
            List<OrderLine> orderLines = command.getOrderItems().stream()
                .map(this::createOrderLine)
                .collect(Collectors.toList());

            /** 建立訂單聚合 */
            Order order = new Order(command.getCustomerId(), orderLines);
            OrderAggregate orderAggregate = new OrderAggregate(order, orderLines, customer);

            /** 儲存訂單 */
            orderRepository.save(orderAggregate);

            /** 發布事件 */
            eventPublisher.publish(new OrderCreatedEvent(order.getId()));

            return OrderDto.from(orderAggregate);
        }

        public void confirmOrder(OrderId orderId) {
            OrderAggregate orderAggregate = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("訂單不存在"));

            orderAggregate.confirmOrder();
            orderRepository.save(orderAggregate);
        }

        private OrderLine createOrderLine(OrderItemDto item) {
            Product product = productRepository.findById(item.getProductId())
                .orElseThrow(() -> new ProductNotFoundException("商品不存在"));

            return new OrderLine(product.getId(), product.getPrice(), item.getQuantity());
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Entity (實體)

    ```typescript
    /** 使用者實體 */
    export class User {
      private constructor(
        private readonly id: UserId,
        private email: Email,
        private name: UserName,
        private status: UserStatus,
        private readonly createdAt: Date
      ) {}

      public static create(email: Email, name: UserName): User {
        return new User(
          UserId.generate(),
          email,
          name,
          UserStatus.ACTIVE,
          new Date()
        );
      }

      public static reconstitute(
        id: UserId,
        email: Email,
        name: UserName,
        status: UserStatus,
        createdAt: Date
      ): User {
        return new User(id, email, name, status, createdAt);
      }

      public changeEmail(newEmail: Email): void {
        if (this.status === UserStatus.SUSPENDED) {
          throw new Error('暫停的使用者無法變更電子郵件');
        }

        this.email = newEmail;
        DomainEventPublisher.publish(new UserEmailChangedEvent(this.id, newEmail));
      }

      public suspend(reason: string): void {
        if (this.status === UserStatus.SUSPENDED) {
          throw new Error('使用者已經暫停');
        }

        this.status = UserStatus.SUSPENDED;
        DomainEventPublisher.publish(new UserSuspendedEvent(this.id, reason));
      }

      public activate(): void {
        if (this.status === UserStatus.ACTIVE) {
          throw new Error('使用者已經啟用');
        }

        this.status = UserStatus.ACTIVE;
        DomainEventPublisher.publish(new UserActivatedEvent(this.id));
      }

      /** Getters */
      public getId(): UserId { return this.id; }
      public getEmail(): Email { return this.email; }
      public getName(): UserName { return this.name; }
      public getStatus(): UserStatus { return this.status; }
      public getCreatedAt(): Date { return this.createdAt; }
    }
    ```

- Value Object (值物件)

    ```typescript
    /** 電子郵件值物件 */
    export class Email {
      private static readonly EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      private constructor(private readonly value: string) {}

      public static of(value: string): Email {
        if (!value || !this.EMAIL_REGEX.test(value)) {
          throw new Error('無效的電子郵件格式');
        }
        return new Email(value.toLowerCase());
      }

      public getValue(): string {
        return this.value;
      }

      public equals(other: Email): boolean {
        return this.value === other.value;
      }

      public toString(): string {
        return this.value;
      }
    }

    /** 使用者名稱值物件 */
    export class UserName {
      private constructor(private readonly value: string) {}

      public static of(value: string): UserName {
        if (!value || value.trim().length < 2) {
          throw new Error('使用者名稱至少需要 2 個字元');
        }
        if (value.length > 50) {
          throw new Error('使用者名稱不能超過 50 個字元');
        }
        return new UserName(value.trim());
      }

      public getValue(): string {
        return this.value;
      }

      public equals(other: UserName): boolean {
        return this.value === other.value;
      }
    }

    /** 使用者 ID 值物件 */
    export class UserId {
      private constructor(private readonly value: string) {}

      public static of(value: string): UserId {
        if (!value || value.trim().length === 0) {
          throw new Error('使用者 ID 不能為空');
        }
        return new UserId(value);
      }

      public static generate(): UserId {
        return new UserId(crypto.randomUUID());
      }

      public getValue(): string {
        return this.value;
      }

      public equals(other: UserId): boolean {
        return this.value === other.value;
      }
    }
    ```

- Repository (儲存庫)

    ```typescript
    /** 使用者儲存庫介面 */
    export interface UserRepository {
      save(user: User): Promise<void>;
      findById(id: UserId): Promise<User | null>;
      findByEmail(email: Email): Promise<User | null>;
      findAll(): Promise<User[]>;
      delete(id: UserId): Promise<void>;
    }

    /** MongoDB 實現 */
    export class MongoUserRepository implements UserRepository {
      constructor(private readonly userModel: Model<UserDocument>) {}

      async save(user: User): Promise<void> {
        const document = {
          _id: user.getId().getValue(),
          email: user.getEmail().getValue(),
          name: user.getName().getValue(),
          status: user.getStatus(),
          createdAt: user.getCreatedAt()
        };

        await this.userModel.findByIdAndUpdate(
          document._id,
          document,
          { upsert: true, new: true }
        );
      }

      async findById(id: UserId): Promise<User | null> {
        const doc = await this.userModel.findById(id.getValue());
        return doc ? this.toDomain(doc) : null;
      }

      async findByEmail(email: Email): Promise<User | null> {
        const doc = await this.userModel.findOne({ email: email.getValue() });
        return doc ? this.toDomain(doc) : null;
      }

      async findAll(): Promise<User[]> {
        const docs = await this.userModel.find();
        return docs.map(doc => this.toDomain(doc));
      }

      async delete(id: UserId): Promise<void> {
        await this.userModel.findByIdAndDelete(id.getValue());
      }

      private toDomain(doc: UserDocument): User {
        return User.reconstitute(
          UserId.of(doc._id),
          Email.of(doc.email),
          UserName.of(doc.name),
          doc.status,
          doc.createdAt
        );
      }
    }
    ```

- Domain Service (領域服務)

    ```typescript
    /** 使用者註冊服務 */
    export class UserRegistrationService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly emailService: EmailService
      ) {}

      async registerUser(email: Email, name: UserName): Promise<User> {
        /** 檢查電子郵件是否已存在 */
        const existingUser = await this.userRepository.findByEmail(email);
        if (existingUser) {
          throw new Error('電子郵件已被使用');
        }

        /** 建立新使用者 */
        const user = User.create(email, name);

        /** 儲存使用者 */
        await this.userRepository.save(user);

        /** 發送歡迎郵件 */
        await this.emailService.sendWelcomeEmail(email, name);

        /** 發布領域事件 */
        DomainEventPublisher.publish(new UserRegisteredEvent(user.getId(), email));

        return user;
      }
    }

    /** 使用者驗證服務 */
    export class UserValidationService {
      constructor(private readonly userRepository: UserRepository) {}

      async validateUserCanPerformAction(userId: UserId, action: string): Promise<void> {
        const user = await this.userRepository.findById(userId);
        if (!user) {
          throw new Error('使用者不存在');
        }

        if (user.getStatus() === UserStatus.SUSPENDED) {
          throw new Error(`暫停的使用者無法執行 ${action}`);
        }

        if (user.getStatus() === UserStatus.INACTIVE) {
          throw new Error(`未啟用的使用者無法執行 ${action}`);
        }
      }
    }
    ```

- Application Service (應用服務)

    ```typescript
    /** 使用者應用服務 */
    export class UserApplicationService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly registrationService: UserRegistrationService,
        private readonly validationService: UserValidationService,
        private readonly eventBus: EventBus
      ) {}

      async registerUser(command: RegisterUserCommand): Promise<UserDto> {
        const email = Email.of(command.email);
        const name = UserName.of(command.name);

        const user = await this.registrationService.registerUser(email, name);

        return this.toDto(user);
      }

      async changeUserEmail(command: ChangeUserEmailCommand): Promise<void> {
        const userId = UserId.of(command.userId);
        const newEmail = Email.of(command.newEmail);

        await this.validationService.validateUserCanPerformAction(userId, '變更電子郵件');

        const user = await this.userRepository.findById(userId);
        if (!user) {
          throw new Error('使用者不存在');
        }

        /** 檢查新電子郵件是否已被使用 */
        const existingUser = await this.userRepository.findByEmail(newEmail);
        if (existingUser && !existingUser.getId().equals(userId)) {
          throw new Error('電子郵件已被其他使用者使用');
        }

        user.changeEmail(newEmail);
        await this.userRepository.save(user);
      }

      async suspendUser(command: SuspendUserCommand): Promise<void> {
        const userId = UserId.of(command.userId);

        const user = await this.userRepository.findById(userId);
        if (!user) {
          throw new Error('使用者不存在');
        }

        user.suspend(command.reason);
        await this.userRepository.save(user);
      }

      async getUserById(query: GetUserByIdQuery): Promise<UserDto | null> {
        const userId = UserId.of(query.userId);
        const user = await this.userRepository.findById(userId);

        return user ? this.toDto(user) : null;
      }

      private toDto(user: User): UserDto {
        return {
          id: user.getId().getValue(),
          email: user.getEmail().getValue(),
          name: user.getName().getValue(),
          status: user.getStatus(),
          createdAt: user.getCreatedAt()
        };
      }
    }
    ```

### React 前端實現範例

- Domain Model (領域模型)

    ```typescript
    /** 待辦事項實體 */
    export class TodoItem {
      private constructor(
        private readonly id: TodoId,
        private title: TodoTitle,
        private completed: boolean,
        private readonly createdAt: Date,
        private completedAt?: Date
      ) {}

      public static create(title: TodoTitle): TodoItem {
        return new TodoItem(
          TodoId.generate(),
          title,
          false,
          new Date()
        );
      }

      public static reconstitute(
        id: TodoId,
        title: TodoTitle,
        completed: boolean,
        createdAt: Date,
        completedAt?: Date
      ): TodoItem {
        return new TodoItem(id, title, completed, createdAt, completedAt);
      }

      public complete(): void {
        if (this.completed) {
          throw new Error('待辦事項已完成');
        }

        this.completed = true;
        this.completedAt = new Date();
      }

      public uncomplete(): void {
        if (!this.completed) {
          throw new Error('待辦事項尚未完成');
        }

        this.completed = false;
        this.completedAt = undefined;
      }

      public changeTitle(newTitle: TodoTitle): void {
        this.title = newTitle;
      }

      /** Getters */
      public getId(): TodoId { return this.id; }
      public getTitle(): TodoTitle { return this.title; }
      public isCompleted(): boolean { return this.completed; }
      public getCreatedAt(): Date { return this.createdAt; }
      public getCompletedAt(): Date | undefined { return this.completedAt; }
    }

    /** 待辦事項標題值物件 */
    export class TodoTitle {
      private constructor(private readonly value: string) {}

      public static of(value: string): TodoTitle {
        if (!value || value.trim().length === 0) {
          throw new Error('待辦事項標題不能為空');
        }
        if (value.length > 200) {
          throw new Error('待辦事項標題不能超過 200 個字元');
        }
        return new TodoTitle(value.trim());
      }

      public getValue(): string {
        return this.value;
      }

      public equals(other: TodoTitle): boolean {
        return this.value === other.value;
      }
    }
    ```

- Repository Implementation (儲存庫實現)

    ```typescript
    /** 本地儲存待辦事項儲存庫 */
    export class LocalStorageTodoRepository implements TodoRepository {
      private readonly storageKey = 'todos';

      async save(todo: TodoItem): Promise<void> {
        const todos = await this.findAll();
        const index = todos.findIndex(t => t.getId().equals(todo.getId()));

        if (index >= 0) {
          todos[index] = todo;
        } else {
          todos.push(todo);
        }

        const serialized = todos.map(t => this.serialize(t));
        localStorage.setItem(this.storageKey, JSON.stringify(serialized));
      }

      async findById(id: TodoId): Promise<TodoItem | null> {
        const todos = await this.findAll();
        return todos.find(todo => todo.getId().equals(id)) || null;
      }

      async findAll(): Promise<TodoItem[]> {
        const data = localStorage.getItem(this.storageKey);
        if (!data) return [];

        const parsed = JSON.parse(data);
        return parsed.map((item: any) => this.deserialize(item));
      }

      async delete(id: TodoId): Promise<void> {
        const todos = await this.findAll();
        const filtered = todos.filter(todo => !todo.getId().equals(id));

        const serialized = filtered.map(t => this.serialize(t));
        localStorage.setItem(this.storageKey, JSON.stringify(serialized));
      }

      private serialize(todo: TodoItem) {
        return {
          id: todo.getId().getValue(),
          title: todo.getTitle().getValue(),
          completed: todo.isCompleted(),
          createdAt: todo.getCreatedAt().toISOString(),
          completedAt: todo.getCompletedAt()?.toISOString()
        };
      }

      private deserialize(data: any): TodoItem {
        return TodoItem.reconstitute(
          TodoId.of(data.id),
          TodoTitle.of(data.title),
          data.completed,
          new Date(data.createdAt),
          data.completedAt ? new Date(data.completedAt) : undefined
        );
      }
    }
    ```

- React Hooks (展示層)

    ```typescript
    /** 待辦事項 Hook */
    export const useTodos = () => {
      const [todos, setTodos] = useState<TodoItem[]>([]);
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);

      const todoService = useMemo(() => 
        new TodoApplicationService(new LocalStorageTodoRepository()), []
      );

      const loadTodos = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
          const allTodos = await todoService.getAllTodos();
          setTodos(allTodos);
        } catch (err) {
          setError(err instanceof Error ? err.message : '載入待辦事項失敗');
        } finally {
          setLoading(false);
        }
      }, [todoService]);

      const createTodo = useCallback(async (title: string) => {
        try {
          const newTodo = await todoService.createTodo({ title });
          setTodos(prev => [...prev, newTodo]);
          return newTodo;
        } catch (err) {
          const errorMessage = err instanceof Error ? err.message : '建立待辦事項失敗';
          setError(errorMessage);
          throw new Error(errorMessage);
        }
      }, [todoService]);

      const completeTodo = useCallback(async (id: string) => {
        try {
          const updatedTodo = await todoService.completeTodo({ todoId: id });
          setTodos(prev => prev.map(todo => 
            todo.getId().getValue() === id ? updatedTodo : todo
          ));
        } catch (err) {
          const errorMessage = err instanceof Error ? err.message : '完成待辦事項失敗';
          setError(errorMessage);
          throw new Error(errorMessage);
        }
      }, [todoService]);

      const deleteTodo = useCallback(async (id: string) => {
        try {
          await todoService.deleteTodo({ todoId: id });
          setTodos(prev => prev.filter(todo => todo.getId().getValue() !== id));
        } catch (err) {
          const errorMessage = err instanceof Error ? err.message : '刪除待辦事項失敗';
          setError(errorMessage);
          throw new Error(errorMessage);
        }
      }, [todoService]);

      useEffect(() => {
        loadTodos();
      }, [loadTodos]);

      return {
        todos,
        loading,
        error,
        createTodo,
        completeTodo,
        deleteTodo,
        refreshTodos: loadTodos
      };
    };

    /** 待辦事項應用服務 */
    class TodoApplicationService {
      constructor(private readonly todoRepository: TodoRepository) {}

      async createTodo(command: CreateTodoCommand): Promise<TodoItem> {
        const title = TodoTitle.of(command.title);
        const todo = TodoItem.create(title);

        await this.todoRepository.save(todo);
        return todo;
      }

      async completeTodo(command: CompleteTodoCommand): Promise<TodoItem> {
        const todoId = TodoId.of(command.todoId);
        const todo = await this.todoRepository.findById(todoId);

        if (!todo) {
          throw new Error('待辦事項不存在');
        }

        todo.complete();
        await this.todoRepository.save(todo);
        return todo;
      }

      async deleteTodo(command: DeleteTodoCommand): Promise<void> {
        const todoId = TodoId.of(command.todoId);
        await this.todoRepository.delete(todoId);
      }

      async getAllTodos(): Promise<TodoItem[]> {
        return await this.todoRepository.findAll();
      }
    }
    ```

<br />

## 應用場景

DDD 適用於以下場景：

- 複雜業務領域

    具有豐富業務規則和複雜業務流程的系統。

- 長期維護專案

    需要長期演進和維護的企業級應用。

- 多團隊協作

    業務專家、分析師、開發人員需要密切合作的專案。

- 領域知識豐富

    業務規則複雜且經常變化的系統。

- 微服務架構

    每個微服務專注於特定的業務領域。

例如

- 金融交易系統

- 電商平台的訂單管理

- 醫療資訊系統

- 保險理賠系統

- 供應鏈管理系統

<br />

## 優點

### 業務導向設計

程式碼結構直接反映業務概念和規則，使系統更貼近實際業務需求。

### 統一語言溝通

技術人員和業務專家使用相同的領域語言，消除溝通障礙和理解偏差。

### 高度可維護性

領域模型集中管理業務規則，變更時只需修改相關領域物件。

### 優秀可測試性

業務規則獨立於技術實現，可以進行純粹的單元測試。

### 知識保存能力

領域知識透過程式碼得到永久保存，避免知識流失。

### 清晰邊界劃分

Bounded Context 提供明確的模型邊界，便於系統擴展和團隊協作。

<br />

## 缺點

### 學習曲線陡峭

需要深入理解 DDD 的戰術和戰略模式，對團隊技能要求較高。

### 複雜性增加

引入大量抽象概念和設計模式，增加程式碼的複雜度。

### 過度工程化風險

對於簡單業務領域可能造成不必要的複雜性和開發成本。

### 前期投入成本高

需要大量時間進行領域分析、建模和設計，延長初期開發週期。

### 團隊協作要求高

需要業務專家、分析師和開發人員密切合作，對團隊組織有較高要求。

### 建模難度大

準確識別聚合邊界、實體和值物件需要豐富的領域知識和建模經驗。

<br />

## 注意事項

- 領域建模：深入理解業務領域，建立準確的領域模型

- 邊界劃分：合理劃分 Bounded Context，避免模型混亂

- 統一語言：確保團隊成員使用一致的術語

- 測試策略：為領域模型編寫充分的單元測試

    ```typescript
    /** 領域模型測試 */
    describe('TodoItem', () => {
      it('應該能夠建立新的待辦事項', () => {
        const title = TodoTitle.of('學習 DDD');
        const todo = TodoItem.create(title);

        expect(todo.getTitle().getValue()).toBe('學習 DDD');
        expect(todo.isCompleted()).toBe(false);
      });

      it('應該能夠完成待辦事項', () => {
        const title = TodoTitle.of('學習 DDD');
        const todo = TodoItem.create(title);

        todo.complete();

        expect(todo.isCompleted()).toBe(true);
        expect(todo.getCompletedAt()).toBeDefined();
      });

      it('不應該重複完成已完成的待辦事項', () => {
        const title = TodoTitle.of('學習 DDD');
        const todo = TodoItem.create(title);
        todo.complete();

        expect(() => todo.complete()).toThrow('待辦事項已完成');
      });
    });

    /** 應用服務測試 */
    describe('TodoApplicationService', () => {
      let service: TodoApplicationService;
      let mockRepository: jest.Mocked<TodoRepository>;

      beforeEach(() => {
        mockRepository = {
          save: jest.fn(),
          findById: jest.fn(),
          findAll: jest.fn(),
          delete: jest.fn()
        };
        service = new TodoApplicationService(mockRepository);
      });

      it('應該能夠建立新的待辦事項', async () => {
        const command = { title: '測試標題' };

        const result = await service.createTodo(command);

        expect(result.getTitle().getValue()).toBe('測試標題');
        expect(mockRepository.save).toHaveBeenCalledWith(result);
      });
    });
    ```

- 效能考量：避免過度細分導致效能問題

- 持續重構：隨著業務理解深入，持續改進領域模型

<br />

## 與其他架構模式的關係

- 與 Clean Architecture：DDD 可以作為 Clean Architecture 的領域層實現

- 與 CQRS：DDD 常與 CQRS 結合，分離命令和查詢模型

- 與 Event Sourcing：領域事件可以用於實現事件溯源

- 與微服務：每個微服務可以對應一個 Bounded Context

- 與 Hexagonal Architecture：六邊形架構為 DDD 提供了技術架構支撐

<br />

## 總結

Domain-Driven Design 是一種專注於複雜業務領域建模的軟體開發方法論，通過統一語言、領域模型和戰術模式，將業務知識轉化為可維護的程式碼結構。

在現代軟體開發中，DDD 特別適合業務規則複雜、需要長期維護的企業級系統。透過 Java、TypeScript 和 React 的實現範例，開發人員可以在不同技術棧中應用 DDD 的核心概念和模式。

開發人員需要根據業務複雜度和團隊能力選擇是否採用 DDD，並注意避免過度設計。
