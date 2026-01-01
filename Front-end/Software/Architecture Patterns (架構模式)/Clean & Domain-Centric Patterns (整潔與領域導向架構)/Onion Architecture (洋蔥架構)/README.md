# Onion Architecture (洋蔥架構)

Onion Architecture (洋蔥架構) 是由 Jeffrey Palermo 在 2008 年提出的軟體架構模式，目標在創建高度可測試、可維護且鬆散耦合的系統。

這種架構採用同心圓分層設計，將業務規則置於核心，外部依賴放在外層，通過依賴反轉原則確保內層不依賴外層，使系統更加穩定和靈活。

<br />

## 動機

在傳統的分層架構中，常見的問題包括

- 業務規則與資料存取層緊密耦合，難以獨立測試

- 基礎設施變更時影響核心業務功能

- 外部服務或框架的依賴滲透到業務核心

- 程式碼難以重用，新需求實現困難

Onion Architecture 通過洋蔥式分層和嚴格的依賴方向，解決這些問題，讓系統具備

- 業務核心獨立：核心業務不依賴外部實現

- 高可測試性：每一層都可以獨立進行單元測試

- 技術無關性：可以輕鬆替換外部技術實現

- 清晰職責：每一層都有明確的責任範圍

<br />

## 結構

Onion Architecture 採用同心圓分層結構，從內到外分為四層

### 1. Domain Model (領域模型層)

最內層，包含核心業務實體和業務規則。

- 封裝企業級業務規則和核心概念

- 完全獨立，不依賴任何外部層

- 包含實體、值物件、領域服務

### 2. Domain Services (領域服務層)

包含領域特定的業務服務和規則。

- 實現跨實體的業務操作

- 協調多個領域物件的互動

- 只依賴領域模型層

### 3. Application Services (應用服務層)

包含應用程式特定的業務流程。

- 協調領域物件完成用例

- 定義應用程式的邊界和介面

- 處理事務和安全性

### 4. Infrastructure (基礎設施層)

最外層，包含所有外部關注點。

- 資料存取、外部 API、UI 框架

- 具體的技術實現

- 實現內層定義的介面

以下是 Onion Architecture 的層次圖

```text
┌─────────────────────────────────────────────────────┐
│                  Infrastructure                     │
│  ┌───────────────────────────────────────────────┐  │
│  │              Application Services             │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │            Domain Services              │  │  │
│  │  │  ┌───────────────────────────────────┐  │  │  │
│  │  │  │          Domain Model             │  │  │  │
│  │  │  └───────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 依賴反轉 (Dependency Inversion)

所有依賴都指向內層，外層實現內層定義的介面。

### 關注點分離 (Separation of Concerns)

每一層都有明確且單一的職責，避免職責混淆。

### 介面隔離 (Interface Segregation)

使用小而專注的介面，避免大而全的介面設計。

<br />

## 實現方式

### C# 實現範例

以銀行轉帳系統為例

- Domain Model (領域模型層)

    ```csharp
    /** 核心領域實體 */
    public class Account
    {
        public string Id { get; private set; }
        public string AccountNumber { get; private set; }
        public decimal Balance { get; private set; }
        public string OwnerId { get; private set; }

        public Account(string accountNumber, string ownerId, decimal initialBalance = 0)
        {
            Id = Guid.NewGuid().ToString();
            AccountNumber = accountNumber;
            OwnerId = ownerId;
            Balance = initialBalance;
        }

        public void Deposit(decimal amount)
        {
            if (amount <= 0)
                throw new ArgumentException("存款金額必須大於零");

            Balance += amount;
        }

        public void Withdraw(decimal amount)
        {
            if (amount <= 0)
                throw new ArgumentException("提款金額必須大於零");

            if (Balance < amount)
                throw new InvalidOperationException("餘額不足");

            Balance -= amount;
        }
    }

    /** 值物件 */
    public class Money
    {
        public decimal Amount { get; }
        public string Currency { get; }

        public Money(decimal amount, string currency)
        {
            if (amount < 0)
                throw new ArgumentException("金額不能為負數");

            Amount = amount;
            Currency = currency ?? throw new ArgumentNullException(nameof(currency));
        }
    }
    ```

- Domain Services (領域服務層)

    ```csharp
    /** 領域服務介面 */
    public interface ITransferService
    {
        Task<TransferResult> TransferAsync(string fromAccountId, string toAccountId, decimal amount);
    }

    /** 領域服務實現 */
    public class TransferService : ITransferService
    {
        private readonly IAccountRepository _accountRepository;
        private readonly ITransferRepository _transferRepository;

        public TransferService(IAccountRepository accountRepository, ITransferRepository transferRepository)
        {
            _accountRepository = accountRepository;
            _transferRepository = transferRepository;
        }

        public async Task<TransferResult> TransferAsync(string fromAccountId, string toAccountId, decimal amount)
        {
            var fromAccount = await _accountRepository.GetByIdAsync(fromAccountId);
            var toAccount = await _accountRepository.GetByIdAsync(toAccountId);

            if (fromAccount == null || toAccount == null)
                throw new ArgumentException("帳戶不存在");

            /** 執行轉帳業務規則 */
            fromAccount.Withdraw(amount);
            toAccount.Deposit(amount);

            /** 記錄轉帳 */
            var transfer = new Transfer(fromAccountId, toAccountId, amount);
            await _transferRepository.SaveAsync(transfer);

            return new TransferResult { Success = true, TransferId = transfer.Id };
        }
    }
    ```

- Application Services (應用服務層)

    ```csharp
    /** 應用服務介面 */
    public interface IAccountApplicationService
    {
        Task<AccountDto> CreateAccountAsync(CreateAccountRequest request);
        Task<TransferDto> TransferMoneyAsync(TransferRequest request);
    }

    /** 應用服務實現 */
    public class AccountApplicationService : IAccountApplicationService
    {
        private readonly IAccountRepository _accountRepository;
        private readonly ITransferService _transferService;
        private readonly IUnitOfWork _unitOfWork;

        public AccountApplicationService(
            IAccountRepository accountRepository,
            ITransferService transferService,
            IUnitOfWork unitOfWork)
        {
            _accountRepository = accountRepository;
            _transferService = transferService;
            _unitOfWork = unitOfWork;
        }

        public async Task<AccountDto> CreateAccountAsync(CreateAccountRequest request)
        {
            var account = new Account(request.AccountNumber, request.OwnerId, request.InitialBalance);

            await _accountRepository.SaveAsync(account);
            await _unitOfWork.CommitAsync();

            return new AccountDto
            {
                Id = account.Id,
                AccountNumber = account.AccountNumber,
                Balance = account.Balance,
                OwnerId = account.OwnerId
            };
        }

        public async Task<TransferDto> TransferMoneyAsync(TransferRequest request)
        {
            var result = await _transferService.TransferAsync(
                request.FromAccountId, 
                request.ToAccountId, 
                request.Amount);

            await _unitOfWork.CommitAsync();

            return new TransferDto
            {
                TransferId = result.TransferId,
                Success = result.Success
            };
        }
    }
    ```

- Infrastructure (基礎設施層)

    ```csharp
    /** Repository 實現 */
    public class SqlAccountRepository : IAccountRepository
    {
        private readonly DbContext _context;

        public SqlAccountRepository(DbContext context)
        {
            _context = context;
        }

        public async Task<Account> GetByIdAsync(string id)
        {
            var entity = await _context.Accounts.FindAsync(id);
            return entity?.ToDomainModel();
        }

        public async Task SaveAsync(Account account)
        {
            var entity = AccountEntity.FromDomainModel(account);
            _context.Accounts.Add(entity);
        }
    }

    /** Web API Controller */
    [ApiController]
    [Route("api/[controller]")]
    public class AccountsController : ControllerBase
    {
        private readonly IAccountApplicationService _accountService;

        public AccountsController(IAccountApplicationService accountService)
        {
            _accountService = accountService;
        }

        [HttpPost]
        public async Task<ActionResult<AccountDto>> CreateAccount([FromBody] CreateAccountRequest request)
        {
            try
            {
                var account = await _accountService.CreateAccountAsync(request);
                return CreatedAtAction(nameof(GetAccount), new { id = account.Id }, account);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }

        [HttpPost("transfer")]
        public async Task<ActionResult<TransferDto>> TransferMoney([FromBody] TransferRequest request)
        {
            try
            {
                var result = await _accountService.TransferMoneyAsync(request);
                return Ok(result);
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
    }
    ```

### Java 和 Spring Boot 實現範例

- Domain Model (領域模型層)

    ```java
    /** 核心領域實體 */
    public class Product {
        private String id;
        private String name;
        private BigDecimal price;
        private int stockQuantity;
        private ProductStatus status;

        public Product(String name, BigDecimal price, int stockQuantity) {
            this.id = UUID.randomUUID().toString();
            this.name = name;
            this.price = price;
            this.stockQuantity = stockQuantity;
            this.status = ProductStatus.ACTIVE;
        }

        public void updatePrice(BigDecimal newPrice) {
            if (newPrice.compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("價格必須大於零");
            }
            this.price = newPrice;
        }

        public void reduceStock(int quantity) {
            if (quantity <= 0) {
                throw new IllegalArgumentException("數量必須大於零");
            }
            if (stockQuantity < quantity) {
                throw new InsufficientStockException("庫存不足");
            }
            this.stockQuantity -= quantity;
        }

        public void addStock(int quantity) {
            if (quantity <= 0) {
                throw new IllegalArgumentException("數量必須大於零");
            }
            this.stockQuantity += quantity;
        }

        /** Getters */
        public String getId() { return id; }
        public String getName() { return name; }
        public BigDecimal getPrice() { return price; }
        public int getStockQuantity() { return stockQuantity; }
        public ProductStatus getStatus() { return status; }
    }
    ```

- Domain Services (領域服務層)

    ```java
    /** 領域服務介面 */
    public interface OrderProcessingService {
        OrderResult processOrder(String customerId, List<OrderItem> items);
    }

    /** 領域服務實現 */
    @Service
    public class OrderProcessingServiceImpl implements OrderProcessingService {
        private final ProductRepository productRepository;
        private final PricingService pricingService;

        public OrderProcessingServiceImpl(ProductRepository productRepository, PricingService pricingService) {
            this.productRepository = productRepository;
            this.pricingService = pricingService;
        }

        @Override
        public OrderResult processOrder(String customerId, List<OrderItem> items) {
            /** 驗證庫存 */
            for (OrderItem item : items) {
                Product product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new ProductNotFoundException("產品不存在"));

                if (product.getStockQuantity() < item.getQuantity()) {
                    throw new InsufficientStockException("產品庫存不足: " + product.getName());
                }
            }

            /** 計算總價 */
            BigDecimal totalAmount = pricingService.calculateTotal(items);

            /** 減少庫存 */
            for (OrderItem item : items) {
                Product product = productRepository.findById(item.getProductId()).get();
                product.reduceStock(item.getQuantity());
                productRepository.save(product);
            }

            return new OrderResult(UUID.randomUUID().toString(), totalAmount, OrderStatus.CONFIRMED);
        }
    }
    ```

- Application Services (應用服務層)

    ```java
    /** 應用服務介面 */
    public interface ProductApplicationService {
        ProductDto createProduct(CreateProductRequest request);
        OrderDto placeOrder(PlaceOrderRequest request);
        List<ProductDto> getAllProducts();
    }

    /** 應用服務實現 */
    @Service
    @Transactional
    public class ProductApplicationServiceImpl implements ProductApplicationService {
        private final ProductRepository productRepository;
        private final OrderRepository orderRepository;
        private final OrderProcessingService orderProcessingService;
        private final NotificationService notificationService;

        public ProductApplicationServiceImpl(
            ProductRepository productRepository,
            OrderRepository orderRepository,
            OrderProcessingService orderProcessingService,
            NotificationService notificationService
        ) {
            this.productRepository = productRepository;
            this.orderRepository = orderRepository;
            this.orderProcessingService = orderProcessingService;
            this.notificationService = notificationService;
        }

        @Override
        public ProductDto createProduct(CreateProductRequest request) {
            Product product = new Product(request.getName(), request.getPrice(), request.getStockQuantity());
            Product savedProduct = productRepository.save(product);

            return ProductDto.fromDomain(savedProduct);
        }

        @Override
        public OrderDto placeOrder(PlaceOrderRequest request) {
            /** 處理訂單 */
            OrderResult result = orderProcessingService.processOrder(request.getCustomerId(), request.getItems());

            /** 建立訂單 */
            Order order = new Order(result.getOrderId(), request.getCustomerId(), request.getItems(), result.getTotalAmount());
            Order savedOrder = orderRepository.save(order);

            /** 發送通知 */
            notificationService.sendOrderConfirmation(request.getCustomerId(), savedOrder);

            return OrderDto.fromDomain(savedOrder);
        }

        @Override
        @Transactional(readOnly = true)
        public List<ProductDto> getAllProducts() {
            return productRepository.findAll().stream()
                .map(ProductDto::fromDomain)
                .collect(Collectors.toList());
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Domain Model (領域模型層)

    ```typescript
    /** 核心領域實體 */
    export class BlogPost {
      constructor(
        private readonly id: string,
        private title: string,
        private content: string,
        private readonly authorId: string,
        private status: PostStatus = PostStatus.DRAFT,
        private readonly createdAt: Date = new Date(),
        private updatedAt: Date = new Date()
      ) {}

      publish(): void {
        if (this.status === PostStatus.PUBLISHED) {
          throw new Error('文章已經發布');
        }
        if (!this.title.trim() || !this.content.trim()) {
          throw new Error('標題和內容不能為空');
        }
        this.status = PostStatus.PUBLISHED;
        this.updatedAt = new Date();
      }

      updateContent(title: string, content: string): void {
        if (!title.trim() || !content.trim()) {
          throw new Error('標題和內容不能為空');
        }
        this.title = title;
        this.content = content;
        this.updatedAt = new Date();
      }

      archive(): void {
        this.status = PostStatus.ARCHIVED;
        this.updatedAt = new Date();
      }

      getId(): string { return this.id; }
      getTitle(): string { return this.title; }
      getContent(): string { return this.content; }
      getAuthorId(): string { return this.authorId; }
      getStatus(): PostStatus { return this.status; }
      getCreatedAt(): Date { return this.createdAt; }
      getUpdatedAt(): Date { return this.updatedAt; }
    }

    export enum PostStatus {
      DRAFT = 'DRAFT',
      PUBLISHED = 'PUBLISHED',
      ARCHIVED = 'ARCHIVED'
    }
    ```

- Domain Services (領域服務層)

    ```typescript
    /** 領域服務介面 */
    export interface BlogService {
      publishPost(postId: string): Promise<void>;
      validatePostContent(title: string, content: string): boolean;
    }

    /** 領域服務實現 */
    export class BlogServiceImpl implements BlogService {
      constructor(
        private readonly postRepository: BlogPostRepository,
        private readonly contentValidator: ContentValidator
      ) {}

      async publishPost(postId: string): Promise<void> {
        const post = await this.postRepository.findById(postId);
        if (!post) {
          throw new Error('文章不存在');
        }

        /** 驗證內容 */
        if (!this.validatePostContent(post.getTitle(), post.getContent())) {
          throw new Error('文章內容不符合發布標準');
        }

        /** 發布文章 */
        post.publish();
        await this.postRepository.save(post);
      }

      validatePostContent(title: string, content: string): boolean {
        return this.contentValidator.validate(title, content);
      }
    }
    ```

- Application Services (應用服務層)

    ```typescript
    /** 應用服務介面 */
    export interface BlogApplicationService {
      createPost(request: CreatePostRequest): Promise<BlogPostDto>;
      publishPost(postId: string): Promise<void>;
      updatePost(postId: string, request: UpdatePostRequest): Promise<BlogPostDto>;
      getPostsByAuthor(authorId: string): Promise<BlogPostDto[]>;
    }

    /** 應用服務實現 */
    export class BlogApplicationServiceImpl implements BlogApplicationService {
      constructor(
        private readonly postRepository: BlogPostRepository,
        private readonly blogService: BlogService,
        private readonly notificationService: NotificationService,
        private readonly unitOfWork: UnitOfWork
      ) {}

      async createPost(request: CreatePostRequest): Promise<BlogPostDto> {
        const post = new BlogPost(
          generateId(),
          request.title,
          request.content,
          request.authorId
        );

        await this.postRepository.save(post);
        await this.unitOfWork.commit();

        return this.mapToDto(post);
      }

      async publishPost(postId: string): Promise<void> {
        await this.blogService.publishPost(postId);

        const post = await this.postRepository.findById(postId);
        if (post) {
          await this.notificationService.notifyPostPublished(post);
        }

        await this.unitOfWork.commit();
      }

      async updatePost(postId: string, request: UpdatePostRequest): Promise<BlogPostDto> {
        const post = await this.postRepository.findById(postId);
        if (!post) {
          throw new Error('文章不存在');
        }

        post.updateContent(request.title, request.content);
        await this.postRepository.save(post);
        await this.unitOfWork.commit();

        return this.mapToDto(post);
      }

      async getPostsByAuthor(authorId: string): Promise<BlogPostDto[]> {
        const posts = await this.postRepository.findByAuthorId(authorId);
        return posts.map(post => this.mapToDto(post));
      }

      private mapToDto(post: BlogPost): BlogPostDto {
        return {
          id: post.getId(),
          title: post.getTitle(),
          content: post.getContent(),
          authorId: post.getAuthorId(),
          status: post.getStatus(),
          createdAt: post.getCreatedAt(),
          updatedAt: post.getUpdatedAt()
        };
      }
    }
    ```

- Infrastructure (基礎設施層)

    ```typescript
    /** Repository 實現 */
    export class MongoBlogPostRepository implements BlogPostRepository {
      constructor(private readonly postModel: Model<BlogPostDocument>) {}

      async save(post: BlogPost): Promise<BlogPost> {
        const doc = await this.postModel.findOneAndUpdate(
          { _id: post.getId() },
          {
            title: post.getTitle(),
            content: post.getContent(),
            authorId: post.getAuthorId(),
            status: post.getStatus(),
            updatedAt: post.getUpdatedAt()
          },
          { upsert: true, new: true }
        );
        return this.mapToDomain(doc);
      }

      async findById(id: string): Promise<BlogPost | null> {
        const doc = await this.postModel.findById(id);
        return doc ? this.mapToDomain(doc) : null;
      }

      async findByAuthorId(authorId: string): Promise<BlogPost[]> {
        const docs = await this.postModel.find({ authorId });
        return docs.map(doc => this.mapToDomain(doc));
      }

      private mapToDomain(doc: BlogPostDocument): BlogPost {
        return new BlogPost(
          doc._id,
          doc.title,
          doc.content,
          doc.authorId,
          doc.status,
          doc.createdAt,
          doc.updatedAt
        );
      }
    }

    /** Express Controller */
    export class BlogController {
      constructor(private readonly blogService: BlogApplicationService) {}

      createPost = async (req: Request, res: Response): Promise<void> => {
        try {
          const post = await this.blogService.createPost(req.body);
          res.status(201).json(post);
        } catch (error) {
          res.status(400).json({ error: error.message });
        }
      };

      publishPost = async (req: Request, res: Response): Promise<void> => {
        try {
          await this.blogService.publishPost(req.params.id);
          res.status(200).json({ message: '文章發布成功' });
        } catch (error) {
          res.status(400).json({ error: error.message });
        }
      };

      getPostsByAuthor = async (req: Request, res: Response): Promise<void> => {
        try {
          const posts = await this.blogService.getPostsByAuthor(req.params.authorId);
          res.json(posts);
        } catch (error) {
          res.status(500).json({ error: error.message });
        }
      };
    }
    ```

<br />

## 優點

### 高度可測試性

每一層都可以獨立測試，特別是核心業務規則可以在沒有外部依賴的情況下進行單元測試。

### 技術無關性

- 框架獨立：核心業務不依賴特定框架

- 資料庫獨立：可以輕鬆切換資料存取技術

- UI 獨立：可以支援多種使用者介面

- 外部服務獨立：可以替換第三方服務

### 清晰的職責分離

每一層都有明確的職責，避免關注點混淆。

### 易於維護和擴展

新功能可以在不影響現有程式碼的情況下添加，變更外部依賴不會影響核心業務。

<br />

## 缺點

### 學習曲線陡峭

需要團隊成員深入理解 DDD 概念和架構原則。

### 初期複雜度高

對於簡單的 CRUD 應用可能過於複雜。

### 開發成本較高

需要更多的介面定義和抽象層設計。

### 過度設計風險

可能會為簡單問題創造過於複雜的解決方案。

<br />

## 與其他架構的比較

### vs Clean Architecture

- 相似點：都採用分層設計和依賴反轉

- 差異點：Onion Architecture 更強調領域驅動設計

### vs Hexagonal Architecture

- 相似點：都將業務規則與外部關注點分離

- 差異點：Onion Architecture 有更明確的內部分層

### vs Traditional Layered Architecture

- 主要差異：依賴方向相反，Onion Architecture 依賴指向內層

<br />

## 適用場景

### 適合使用

- 複雜業務領域：有豐富的業務規則和流程

- 長期維護專案：需要長期演進和維護

- 多技術棧支援：需要支援多種技術實現

- 高品質要求：對程式碼品質和可測試性要求高

- 團隊協作：大型團隊需要清晰的架構邊界

### 不適合使用

- 簡單 CRUD 應用：業務規則簡單的系統

- 快速原型：需要快速驗證概念的專案

- 小型專案：團隊規模小且需求穩定

- 資源受限：時間或人力資源緊張的專案

<br />

## 實施建議

### 從核心開始

先設計領域模型和核心業務規則，再逐步添加外層。

### 介面先行

在實現具體功能前，先定義清晰的介面契約。

### 漸進式重構

對於既有系統，可以逐步重構，不需要一次性改造。

### 自動化測試

建立完整的測試金字塔，特別注重領域模型的單元測試。

### 團隊培訓

確保團隊成員理解 DDD 概念和架構原則。

### 持續重構

隨著業務需求的變化，持續優化架構設計。

<br />

## 總結

Onion Architecture 提供了一個強大且靈活的架構模式，特別適合複雜業務領域的應用程式開發。通過嚴格的分層和依賴管理，能夠創建高度可測試、可維護且技術無關的系統。

雖然初期學習成本較高，但對於需要長期維護和演進的複雜系統來說，這種投資是值得的。關鍵在於根據專案的實際複雜度和團隊能力來決定採用程度，避免過度設計的同時確保架構能夠支撐業務發展需求。
