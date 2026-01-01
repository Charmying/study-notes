# Hexagonal Architecture (Ports and Adapters) (六邊形架構 & 埠與轉接器架構)

Hexagonal Architecture (六邊形架構)，也稱為 Ports and Adapters (埠與轉接器架構)，是由 Alistair Cockburn 提出的軟體架構模式，目標在創建可測試、可維護、獨立於外部技術的應用程式。

這種架構將應用程式核心與外部世界隔離，通過埠 (Ports) 定義介面，透過轉接器 (Adapters) 實現具體的外部整合，使系統更容易測試、理解和修改。

<br />

## 動機

在軟體開發中，常見的問題包括

- 業務核心與外部技術緊密耦合，難以測試和替換

- 資料庫、外部 API 或 UI 框架的變更影響核心業務

- 測試需要依賴外部系統，導致測試困難且不穩定

- 程式碼難以理解，業務規則與技術細節混雜

Hexagonal Architecture 通過埠與轉接器的設計，解決這些問題，讓系統具備

- 隔離性：核心業務與外部技術完全分離

- 可測試性：可以輕鬆模擬外部依賴進行測試

- 可替換性：可以替換任何外部技術而不影響核心

- 可理解性：清晰的邊界使業務規則更容易理解

<br />

## 結構

Hexagonal Architecture 將應用程式分為三個主要部分

### 1. Application Core (應用程式核心)

位於六邊形的中心，包含純粹的業務規則和領域模型。

- 不依賴任何外部技術或框架

- 包含領域實體、業務服務和用例

- 定義埠介面但不實現

### 2. Ports (埠)

定義應用程式核心與外部世界的介面。

- Primary Ports (主要埠)：驅動應用程式的介面 (例如：API、UI)

- Secondary Ports (次要埠)：應用程式驅動的介面 (例如：資料庫、外部服務)

### 3. Adapters (轉接器)

實現埠介面，處理與外部技術的整合。

- Primary Adapters (主要轉接器)：接收外部請求並呼叫應用程式

- Secondary Adapters (次要轉接器)：實現應用程式需要的外部服務

以下是 Hexagonal Architecture 的結構圖

```text
                            ┌─────────────────────────┐
                            │     Primary Adapters    │
                            │    (Web, CLI, Tests)    │
                            └────────────┬────────────┘
                                         │
                            ┌────────────▼────────────┐
                            │      Primary Ports      │
                            │     (Use Cases API)     │
                            └────────────┬────────────┘
┌─────────────────────────┐              │              ┌────────────────────────┐
│ Secondary               │ ┌────────────▼────────────┐ │ Secondary              │
│ Adapters                │ │   Application Core      │ │ Adapters               │
│ (Database, File System) │◄┤   (Business Logic)      │►│ (Email, External APIs) │ 
└─────────────────────────┘ └────────────▲────────────┘ └────────────────────────┘
                                         │
                            ┌────────────┴────────────┐
                            │     Secondary Ports     │
                            │  (Repository, Gateway)  │
                            └─────────────────────────┘
```

<br />

## 核心原則

### 依賴反轉 (Dependency Inversion)

應用程式核心定義介面，外部轉接器實現這些介面。

### 隔離外部關注點 (Isolate External Concerns)

業務規則與外部技術完全分離，不依賴具體實現。

### 可測試性 (Testability)

通過模擬埠介面，可以獨立測試應用程式核心。

<br />

## 實現方式

### Java 實現範例

以銀行轉帳系統為例

- Application Core (應用程式核心)

    ```java
    /** 領域實體 */
    public class Account {
        private final String accountId;
        private BigDecimal balance;
        private final String ownerId;

        public Account(String accountId, String ownerId, BigDecimal initialBalance) {
            this.accountId = accountId;
            this.ownerId = ownerId;
            this.balance = initialBalance;
        }

        public void withdraw(BigDecimal amount) {
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("提款金額必須大於零");
            }
            if (balance.compareTo(amount) < 0) {
                throw new InsufficientFundsException("餘額不足");
            }
            this.balance = this.balance.subtract(amount);
        }

        public void deposit(BigDecimal amount) {
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("存款金額必須大於零");
            }
            this.balance = this.balance.add(amount);
        }

        public String getAccountId() { return accountId; }
        public BigDecimal getBalance() { return balance; }
        public String getOwnerId() { return ownerId; }
    }

    /** 業務服務 */
    public class TransferService {
        private final AccountRepository accountRepository;
        private final NotificationPort notificationPort;
        private final AuditPort auditPort;

        public TransferService(
            AccountRepository accountRepository,
            NotificationPort notificationPort,
            AuditPort auditPort
        ) {
            this.accountRepository = accountRepository;
            this.notificationPort = notificationPort;
            this.auditPort = auditPort;
        }

        public void transfer(String fromAccountId, String toAccountId, BigDecimal amount) {
            Account fromAccount = accountRepository.findById(fromAccountId)
                .orElseThrow(() -> new AccountNotFoundException("來源帳戶不存在"));

            Account toAccount = accountRepository.findById(toAccountId)
                .orElseThrow(() -> new AccountNotFoundException("目標帳戶不存在"));

            fromAccount.withdraw(amount);
            toAccount.deposit(amount);

            accountRepository.save(fromAccount);
            accountRepository.save(toAccount);

            auditPort.logTransfer(fromAccountId, toAccountId, amount);
            notificationPort.sendTransferNotification(fromAccount.getOwnerId(), amount);
        }
    }
    ```

- Ports (埠)

    ```java
    /** Primary Port - 用例介面 */
    public interface TransferUseCase {
        void transfer(TransferRequest request);
        AccountBalance getAccountBalance(String accountId);
    }

    /** Secondary Ports - 外部服務介面 */
    public interface AccountRepository {
        Optional<Account> findById(String accountId);
        void save(Account account);
    }

    public interface NotificationPort {
        void sendTransferNotification(String userId, BigDecimal amount);
    }

    public interface AuditPort {
        void logTransfer(String fromAccountId, String toAccountId, BigDecimal amount);
    }
    ```

- Primary Adapter (主要轉接器)

    ```java
    /** REST API 轉接器 */
    @RestController
    @RequestMapping("/api/transfers")
    public class TransferController {
        private final TransferUseCase transferUseCase;

        public TransferController(TransferUseCase transferUseCase) {
            this.transferUseCase = transferUseCase;
        }

        @PostMapping
        public ResponseEntity<Void> transfer(@RequestBody TransferRequest request) {
            try {
                transferUseCase.transfer(request);
                return ResponseEntity.ok().build();
            } catch (AccountNotFoundException | InsufficientFundsException e) {
                return ResponseEntity.badRequest().build();
            }
        }

        @GetMapping("/accounts/{accountId}/balance")
        public ResponseEntity<AccountBalance> getBalance(@PathVariable String accountId) {
            AccountBalance balance = transferUseCase.getAccountBalance(accountId);
            return ResponseEntity.ok(balance);
        }
    }

    /** Use Case 實現 */
    @Service
    public class TransferUseCaseImpl implements TransferUseCase {
        private final TransferService transferService;
        private final AccountRepository accountRepository;

        @Override
        public void transfer(TransferRequest request) {
            transferService.transfer(
                request.getFromAccountId(),
                request.getToAccountId(),
                request.getAmount()
            );
        }

        @Override
        public AccountBalance getAccountBalance(String accountId) {
            Account account = accountRepository.findById(accountId)
                .orElseThrow(() -> new AccountNotFoundException("帳戶不存在"));
            return new AccountBalance(account.getAccountId(), account.getBalance());
        }
    }
    ```

- Secondary Adapters (次要轉接器)

    ```java
    /** 資料庫轉接器 */
    @Repository
    public class JpaAccountRepository implements AccountRepository {
        private final AccountJpaRepository jpaRepository;
        private final AccountMapper mapper;

        @Override
        public Optional<Account> findById(String accountId) {
            return jpaRepository.findById(accountId)
                .map(mapper::toDomain);
        }

        @Override
        public void save(Account account) {
            AccountEntity entity = mapper.toEntity(account);
            jpaRepository.save(entity);
        }
    }

    /** 通知轉接器 */
    @Component
    public class EmailNotificationAdapter implements NotificationPort {
        private final EmailService emailService;
        private final UserRepository userRepository;

        @Override
        public void sendTransferNotification(String userId, BigDecimal amount) {
            User user = userRepository.findById(userId)
                .orElseThrow(() -> new UserNotFoundException("使用者不存在"));

            String message = String.format("轉帳成功，金額：%s", amount);
            emailService.sendEmail(user.getEmail(), "轉帳通知", message);
        }
    }

    /** 稽核轉接器 */
    @Component
    public class DatabaseAuditAdapter implements AuditPort {
        private final AuditLogRepository auditRepository;

        @Override
        public void logTransfer(String fromAccountId, String toAccountId, BigDecimal amount) {
            AuditLog log = new AuditLog(
                "TRANSFER",
                String.format("從 %s 轉帳 %s 到 %s", fromAccountId, amount, toAccountId),
                Instant.now()
            );
            auditRepository.save(log);
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Application Core (應用程式核心)

    ```typescript
    /** 領域實體 */
    export class Product {
      constructor(
        private readonly id: string,
        private name: string,
        private price: number,
        private stock: number
      ) {
        if (price < 0) throw new Error('價格不能為負數');
        if (stock < 0) throw new Error('庫存不能為負數');
      }

      updatePrice(newPrice: number): void {
        if (newPrice < 0) throw new Error('價格不能為負數');
        this.price = newPrice;
      }

      reduceStock(quantity: number): void {
        if (quantity <= 0) throw new Error('數量必須大於零');
        if (this.stock < quantity) throw new Error('庫存不足');
        this.stock -= quantity;
      }

      addStock(quantity: number): void {
        if (quantity <= 0) throw new Error('數量必須大於零');
        this.stock += quantity;
      }

      getId(): string { return this.id; }
      getName(): string { return this.name; }
      getPrice(): number { return this.price; }
      getStock(): number { return this.stock; }
    }

    /** 業務服務 */
    export class OrderService {
      constructor(
        private readonly productRepository: ProductRepository,
        private readonly orderRepository: OrderRepository,
        private readonly paymentGateway: PaymentGateway,
        private readonly inventoryService: InventoryService
      ) {}

      async processOrder(customerId: string, items: OrderItem[]): Promise<string> {
        /** 驗證庫存 */
        for (const item of items) {
          const product = await this.productRepository.findById(item.productId);
          if (!product) {
            throw new Error(`商品 ${item.productId} 不存在`);
          }
          if (product.getStock() < item.quantity) {
            throw new Error(`商品 ${product.getName()} 庫存不足`);
          }
        }

        /** 計算總金額 */
        let totalAmount = 0;
        for (const item of items) {
          const product = await this.productRepository.findById(item.productId);
          totalAmount += product!.getPrice() * item.quantity;
        }

        /** 處理付款 */
        const paymentResult = await this.paymentGateway.processPayment(
          customerId,
          totalAmount
        );

        if (!paymentResult.success) {
          throw new Error('付款失敗');
        }

        /** 減少庫存 */
        for (const item of items) {
          await this.inventoryService.reduceStock(item.productId, item.quantity);
        }

        /** 建立訂單 */
        const order = new Order(generateId(), customerId, items, totalAmount);
        await this.orderRepository.save(order);

        return order.getId();
      }
    }
    ```

- Ports (埠)

    ```typescript
    /** Primary Port */
    export interface OrderUseCase {
      processOrder(request: ProcessOrderRequest): Promise<ProcessOrderResponse>;
      getOrderStatus(orderId: string): Promise<OrderStatus>;
    }

    /** Secondary Ports */
    export interface ProductRepository {
      findById(id: string): Promise<Product | null>;
      save(product: Product): Promise<void>;
    }

    export interface OrderRepository {
      save(order: Order): Promise<void>;
      findById(id: string): Promise<Order | null>;
    }

    export interface PaymentGateway {
      processPayment(customerId: string, amount: number): Promise<PaymentResult>;
    }

    export interface InventoryService {
      reduceStock(productId: string, quantity: number): Promise<void>;
      addStock(productId: string, quantity: number): Promise<void>;
    }
    ```

- Primary Adapter (主要轉接器)

    ```typescript
    /** Express.js 轉接器 */
    export class OrderController {
      constructor(private readonly orderUseCase: OrderUseCase) {}

      async processOrder(req: Request, res: Response): Promise<void> {
        try {
          const response = await this.orderUseCase.processOrder(req.body);
          res.status(201).json(response);
        } catch (error) {
          res.status(400).json({ error: error.message });
        }
      }

      async getOrderStatus(req: Request, res: Response): Promise<void> {
        try {
          const status = await this.orderUseCase.getOrderStatus(req.params.orderId);
          res.json(status);
        } catch (error) {
          res.status(404).json({ error: error.message });
        }
      }
    }

    /** Use Case 實現 */
    export class OrderUseCaseImpl implements OrderUseCase {
      constructor(private readonly orderService: OrderService) {}

      async processOrder(request: ProcessOrderRequest): Promise<ProcessOrderResponse> {
        const orderId = await this.orderService.processOrder(
          request.customerId,
          request.items
        );
        return { orderId, status: 'PROCESSING' };
      }

      async getOrderStatus(orderId: string): Promise<OrderStatus> {
        /** 實現訂單狀態查詢 */
        return { orderId, status: 'COMPLETED' };
      }
    }
    ```

- Secondary Adapters (次要轉接器)

    ```typescript
    /** MongoDB 轉接器 */
    export class MongoProductRepository implements ProductRepository {
      constructor(private readonly productModel: Model<ProductDocument>) {}

      async findById(id: string): Promise<Product | null> {
        const doc = await this.productModel.findById(id);
        return doc ? this.mapToProduct(doc) : null;
      }

      async save(product: Product): Promise<void> {
        await this.productModel.findByIdAndUpdate(
          product.getId(),
          {
            name: product.getName(),
            price: product.getPrice(),
            stock: product.getStock()
          },
          { upsert: true }
        );
      }

      private mapToProduct(doc: ProductDocument): Product {
        return new Product(doc._id, doc.name, doc.price, doc.stock);
      }
    }

    /** Stripe 付款轉接器 */
    export class StripePaymentAdapter implements PaymentGateway {
      constructor(private readonly stripeClient: Stripe) {}

      async processPayment(customerId: string, amount: number): Promise<PaymentResult> {
        try {
          const paymentIntent = await this.stripeClient.paymentIntents.create({
            amount: amount * 100, // Stripe 使用分為單位
            currency: 'twd',
            customer: customerId
          });

          return {
            success: paymentIntent.status === 'succeeded',
            transactionId: paymentIntent.id
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    }

    /** Redis 庫存服務轉接器 */
    export class RedisInventoryAdapter implements InventoryService {
      constructor(private readonly redisClient: Redis) {}

      async reduceStock(productId: string, quantity: number): Promise<void> {
        const script = `
          local current = redis.call('GET', KEYS[1])
          if not current then
            return redis.error_reply('Product not found')
          end
          local stock = tonumber(current)
          if stock < tonumber(ARGV[1]) then
            return redis.error_reply('Insufficient stock')
          end
          return redis.call('DECRBY', KEYS[1], ARGV[1])
        `;

        await this.redisClient.eval(script, 1, `stock:${productId}`, quantity);
      }

      async addStock(productId: string, quantity: number): Promise<void> {
        await this.redisClient.incrby(`stock:${productId}`, quantity);
      }
    }
    ```

### React 前端實現範例

- Application Core (應用程式核心)

    ```typescript
    /** 領域實體 */
    export class ShoppingCart {
      private items: Map<string, CartItem> = new Map();

      addItem(productId: string, name: string, price: number, quantity: number = 1): void {
        if (quantity <= 0) throw new Error('數量必須大於零');

        const existingItem = this.items.get(productId);
        if (existingItem) {
          existingItem.increaseQuantity(quantity);
        } else {
          this.items.set(productId, new CartItem(productId, name, price, quantity));
        }
      }

      removeItem(productId: string): void {
        this.items.delete(productId);
      }

      updateQuantity(productId: string, quantity: number): void {
        if (quantity <= 0) {
          this.removeItem(productId);
          return;
        }

        const item = this.items.get(productId);
        if (item) {
          item.setQuantity(quantity);
        }
      }

      getTotalAmount(): number {
        return Array.from(this.items.values())
          .reduce((total, item) => total + item.getTotalPrice(), 0);
      }

      getItems(): CartItem[] {
        return Array.from(this.items.values());
      }

      clear(): void {
        this.items.clear();
      }
    }

    /** 購物車服務 */
    export class CartService {
      constructor(
        private readonly cartRepository: CartRepository,
        private readonly productCatalog: ProductCatalog
      ) {}

      async addToCart(userId: string, productId: string, quantity: number): Promise<void> {
        const product = await this.productCatalog.getProduct(productId);
        if (!product) {
          throw new Error('商品不存在');
        }

        const cart = await this.cartRepository.getCart(userId) || new ShoppingCart();
        cart.addItem(productId, product.name, product.price, quantity);
        await this.cartRepository.saveCart(userId, cart);
      }

      async removeFromCart(userId: string, productId: string): Promise<void> {
        const cart = await this.cartRepository.getCart(userId);
        if (cart) {
          cart.removeItem(productId);
          await this.cartRepository.saveCart(userId, cart);
        }
      }

      async getCart(userId: string): Promise<ShoppingCart | null> {
        return await this.cartRepository.getCart(userId);
      }
    }
    ```

- Ports (埠)

    ```typescript
    /** Primary Port */
    export interface CartUseCase {
      addToCart(userId: string, productId: string, quantity: number): Promise<void>;
      removeFromCart(userId: string, productId: string): Promise<void>;
      getCart(userId: string): Promise<CartData | null>;
      clearCart(userId: string): Promise<void>;
    }

    /** Secondary Ports */
    export interface CartRepository {
      getCart(userId: string): Promise<ShoppingCart | null>;
      saveCart(userId: string, cart: ShoppingCart): Promise<void>;
    }

    export interface ProductCatalog {
      getProduct(productId: string): Promise<ProductInfo | null>;
    }
    ```

- Primary Adapter (主要轉接器)

    ```typescript
    /** React Hook 轉接器 */
    export const useCart = (userId: string) => {
      const [cart, setCart] = useState<CartData | null>(null);
      const [loading, setLoading] = useState(false);
      const cartUseCase = useCartUseCase();

      const loadCart = useCallback(async () => {
        setLoading(true);
        try {
          const cartData = await cartUseCase.getCart(userId);
          setCart(cartData);
        } catch (error) {
          console.error('載入購物車失敗:', error);
        } finally {
          setLoading(false);
        }
      }, [userId, cartUseCase]);

      const addToCart = useCallback(async (productId: string, quantity: number) => {
        try {
          await cartUseCase.addToCart(userId, productId, quantity);
          await loadCart();
        } catch (error) {
          console.error('加入購物車失敗:', error);
          throw error;
        }
      }, [userId, cartUseCase, loadCart]);

      const removeFromCart = useCallback(async (productId: string) => {
        try {
          await cartUseCase.removeFromCart(userId, productId);
          await loadCart();
        } catch (error) {
          console.error('移除商品失敗:', error);
          throw error;
        }
      }, [userId, cartUseCase, loadCart]);

      useEffect(() => {
        loadCart();
      }, [loadCart]);

      return {
        cart,
        loading,
        addToCart,
        removeFromCart,
        refreshCart: loadCart
      };
    };

    /** React 元件 */
    export const ShoppingCartComponent: React.FC<{ userId: string }> = ({ userId }) => {
      const { cart, loading, addToCart, removeFromCart } = useCart(userId);

      if (loading) {
        return <div>載入中...</div>;
      }

      if (!cart || cart.items.length === 0) {
        return <div>購物車是空的</div>;
      }

      return (
        <div className="shopping-cart">
          <h2>購物車</h2>
          {cart.items.map((item) => (
            <div key={item.productId} className="cart-item">
              <span>{item.name}</span>
              <span>NT$ {item.price}</span>
              <span>數量: {item.quantity}</span>
              <span>小計: NT$ {item.totalPrice}</span>
              <button onClick={() => removeFromCart(item.productId)}>
                移除
              </button>
            </div>
          ))}
          <div className="cart-total">
            總計: NT$ {cart.totalAmount}
          </div>
        </div>
      );
    };
    ```

- Secondary Adapters (次要轉接器)

    ```typescript
    /** LocalStorage 轉接器 */
    export class LocalStorageCartRepository implements CartRepository {
      async getCart(userId: string): Promise<ShoppingCart | null> {
        const data = localStorage.getItem(`cart_${userId}`);
        if (!data) return null;

        const cartData = JSON.parse(data);
        const cart = new ShoppingCart();

        cartData.items.forEach((item: any) => {
          cart.addItem(item.productId, item.name, item.price, item.quantity);
        });

        return cart;
      }

      async saveCart(userId: string, cart: ShoppingCart): Promise<void> {
        const cartData = {
          items: cart.getItems().map(item => ({
            productId: item.getProductId(),
            name: item.getName(),
            price: item.getPrice(),
            quantity: item.getQuantity()
          }))
        };

        localStorage.setItem(`cart_${userId}`, JSON.stringify(cartData));
      }
    }

    /** API 商品目錄轉接器 */
    export class ApiProductCatalog implements ProductCatalog {
      constructor(private readonly httpClient: HttpClient) {}

      async getProduct(productId: string): Promise<ProductInfo | null> {
        try {
          const response = await this.httpClient.get(`/api/products/${productId}`);
          return response.data;
        } catch (error) {
          if (error.status === 404) {
            return null;
          }
          throw error;
        }
      }
    }
    ```

<br />

## 優點

### 可測試性

應用程式核心可以完全獨立於外部依賴進行測試，通過模擬埠介面即可進行完整的單元測試。

### 技術獨立性

- 資料庫獨立：可以輕鬆切換不同的資料庫技術
- 框架獨立：不依賴特定的 Web 框架或 UI 技術
- 外部服務獨立：可以替換任何外部 API 或服務

### 可維護性

清晰的邊界和職責分離使得程式碼更容易理解和維護。

### 可擴展性

新的外部整合可以通過添加新的轉接器來實現，不需要修改核心業務。

### 並行開發

不同團隊可以同時開發核心業務和外部轉接器。

<br />

## 缺點

### 複雜性增加

對於簡單的應用程式來說，可能會增加不必要的複雜性。

### 學習曲線

需要團隊理解埠與轉接器的概念和實現方式。

### 初期開發成本

需要更多的前期設計和介面定義工作。

### 過度抽象風險

可能會創造過多的抽象層，影響程式碼的可讀性。

<br />

## 適用場景

### 適合使用

- 複雜業務規則：有複雜的業務流程需要獨立測試
- 多種外部整合：需要整合多個外部系統或服務
- 技術變更頻繁：外部技術可能經常變更
- 高品質要求：對程式碼品質和可測試性要求高
- 長期維護：需要長期維護和擴展的系統

### 不適合使用

- 簡單 CRUD 應用：只有基本的資料操作
- 原型開發：快速驗證概念的專案
- 小型專案：團隊規模小且需求簡單
- 時間緊迫：需要快速交付的專案

<br />

## 與其他架構的比較

### vs Clean Architecture

- 相似點：都強調依賴反轉和關注點分離
- 差異點：Hexagonal Architecture 更專注於埠與轉接器的概念，Clean Architecture 有更明確的分層結構

### vs Layered Architecture

- 相似點：都有分層的概念
- 差異點：Hexagonal Architecture 避免了層與層之間的直接依賴，所有外部依賴都通過埠介面

### vs Microservices

- 相似點：都強調服務的獨立性
- 差異點：Hexagonal Architecture 是單一應用程式內的架構模式，Microservices 是分散式系統架構

<br />

## 實施建議

### 從核心開始

先定義業務核心和埠介面，再實現外部轉接器。

### 測試驅動開發

利用架構的可測試性，採用測試驅動開發方法。

### 漸進式重構

對於現有系統，可以逐步重構為 Hexagonal Architecture。

### 介面設計

仔細設計埠介面，確保其穩定性和可擴展性。

### 文件化

維護清晰的架構文件，說明各個埠和轉接器的職責。

<br />

## 總結

Hexagonal Architecture 提供了一個強大的框架來隔離業務核心與外部技術，特別適合需要高度可測試性和技術獨立性的應用程式。通過埠與轉接器的設計，系統可以輕鬆適應技術變更，同時保持業務規則的穩定性。

關鍵在於正確識別應用程式的核心業務，設計合適的埠介面，並實現相應的轉接器。雖然初期投入較高，但對於複雜的業務系統來說，這種架構能夠帶來長期的維護和擴展優勢。
