# CQRS (Command Query Responsibility Segregation) (命令查詢責任分離架構)

CQRS (Command Query Responsibility Segregation) 是一種架構模式，將系統的讀取操作 (Query) 和寫入操作 (Command) 分離到不同的模型中。這種分離允許針對不同的需求優化讀寫操作，提升系統的效能、可擴展性和維護性。

CQRS 基於 CQS (Command Query Separation) 原則，但將分離的概念從方法層級提升到架構層級，使讀寫操作可以使用完全不同的資料模型和儲存機制。

<br />

## 動機

在傳統的 CRUD 應用程式中，常見的問題包括

- 讀寫操作使用相同的資料模型，導致複雜的查詢和更新操作

- 讀取需求和寫入需求的效能特性不同，難以同時優化

- 複雜的業務規則與查詢需求混合在同一個模型中

- 高併發情況下讀寫操作相互影響效能

CQRS 通過分離讀寫模型，解決這些問題，讓系統具備

- 獨立優化：讀寫操作可以獨立優化和擴展

- 簡化複雜性：複雜的查詢不會影響寫入模型的設計

- 效能提升：可以針對不同需求選擇最適合的儲存技術

- 可擴展性：讀寫操作可以獨立擴展

<br />

## 結構

CQRS 將系統分為兩個主要部分：Command Side (命令端) 和 Query Side (查詢端)。

### Command Side (命令端)

負責處理所有的寫入操作和業務規則。

- 接收和處理 Commands

- 執行業務規則驗證

- 更新寫入模型

- 發布領域事件

### Query Side (查詢端)

負責處理所有的讀取操作和資料查詢。

- 接收和處理 Queries

- 從讀取模型獲取資料

- 提供優化的查詢介面

- 處理資料投影和轉換

以下是 CQRS 的架構圖

```text
┌─────────────────────────────────────────────────────────────┐
│                           Client                            │
└─────────────┬────────────────────────────────┬──────────────┘
              │                                │
              ▼                                ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│        Command Side         │ │         Query Side          │
│                             │ │                             │
│  ┌─────────────────────┐    │ │    ┌─────────────────────┐  │
│  │   Command Handler   │    │ │    │   Query Handler     │  │
│  └─────────────────────┘    │ │    └─────────────────────┘  │
│              │              │ │              │              │
│              ▼              │ │              ▼              │
│  ┌─────────────────────┐    │ │    ┌─────────────────────┐  │
│  │    Write Model      │    │ │    │     Read Model      │  │
│  └─────────────────────┘    │ │    └─────────────────────┘  │
│              │              │ │              ▲              │
│              ▼              │ │              │              │
│  ┌─────────────────────┐    │ │              │              │
│  │   Write Database    │    │ │              │              │
│  └─────────────────────┘    │ │              │              │
│              │              │ │              │              │
│              ▼              │ │              │              │
│            Events ──────────┼─┼──────────────┘              │
│                             │ │                             │
└─────────────────────────────┘ └─────────────────────────────┘
```

<br />

## 核心概念

### Commands (命令)

表示系統中的寫入操作，包含執行特定業務操作所需的資料。

- 具有明確的意圖和業務含義

- 包含執行操作所需的所有資料

- 通常以動詞命名 (例如：CreateOrder, UpdateProduct)

### Queries (查詢)

表示系統中的讀取操作，用於獲取特定的資料。

- 不會改變系統狀態

- 可以包含過濾、排序、分頁等參數

- 返回針對特定用途優化的資料結構

### Event Sourcing (事件溯源)

CQRS 常與 Event Sourcing 結合使用，通過事件來同步讀寫模型。

### Eventual Consistency (最終一致性)

讀寫模型之間可能存在短暫的不一致，但最終會達到一致狀態。

<br />

## 實現方式

### Java 實現範例

以電商系統的產品管理為例

- Commands 和 Command Handlers

    ```java
    /** 建立產品命令 */
    public class CreateProductCommand {
        private final String name;
        private final String description;
        private final BigDecimal price;
        private final String categoryId;

        public CreateProductCommand(String name, String description, BigDecimal price, String categoryId) {
            this.name = name;
            this.description = description;
            this.price = price;
            this.categoryId = categoryId;
        }

        // getters...
    }

    /** 命令處理器 */
    @Component
    public class CreateProductCommandHandler {
        private final ProductRepository productRepository;
        private final EventPublisher eventPublisher;

        public CreateProductCommandHandler(ProductRepository productRepository, EventPublisher eventPublisher) {
            this.productRepository = productRepository;
            this.eventPublisher = eventPublisher;
        }

        public void handle(CreateProductCommand command) {
            /** 驗證業務規則 */
            validateProductData(command);

            /** 建立產品實體 */
            Product product = new Product(
                UUID.randomUUID().toString(),
                command.getName(),
                command.getDescription(),
                command.getPrice(),
                command.getCategoryId()
            );

            /** 儲存到寫入模型 */
            productRepository.save(product);

            /** 發布事件 */
            eventPublisher.publish(new ProductCreatedEvent(
                product.getId(),
                product.getName(),
                product.getPrice(),
                product.getCategoryId()
            ));
        }

        private void validateProductData(CreateProductCommand command) {
            if (command.getName() == null || command.getName().trim().isEmpty()) {
                throw new IllegalArgumentException("產品名稱不能為空");
            }
            if (command.getPrice().compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("產品價格必須大於零");
            }
        }
    }
    ```

- Queries 和 Query Handlers

    ```java
    /** 產品查詢 */
    public class GetProductsQuery {
        private final String categoryId;
        private final String searchTerm;
        private final int page;
        private final int size;
        private final String sortBy;

        public GetProductsQuery(String categoryId, String searchTerm, int page, int size, String sortBy) {
            this.categoryId = categoryId;
            this.searchTerm = searchTerm;
            this.page = page;
            this.size = size;
            this.sortBy = sortBy;
        }

        // getters...
    }

    /** 查詢處理器 */
    @Component
    public class GetProductsQueryHandler {
        private final ProductReadModelRepository readModelRepository;

        public GetProductsQueryHandler(ProductReadModelRepository readModelRepository) {
            this.readModelRepository = readModelRepository;
        }

        public ProductListResponse handle(GetProductsQuery query) {
            /** 從讀取模型查詢資料 */
            List<ProductReadModel> products = readModelRepository.findProducts(
                query.getCategoryId(),
                query.getSearchTerm(),
                query.getPage(),
                query.getSize(),
                query.getSortBy()
            );

            /** 轉換為回應格式 */
            List<ProductDto> productDtos = products.stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());

            return new ProductListResponse(productDtos, products.size());
        }

        private ProductDto mapToDto(ProductReadModel product) {
            return new ProductDto(
                product.getId(),
                product.getName(),
                product.getDescription(),
                product.getPrice(),
                product.getCategoryName(),
                product.getAverageRating(),
                product.getReviewCount()
            );
        }
    }
    ```

- Event Handlers (事件處理器)

    ```java
    /** 事件處理器更新讀取模型 */
    @Component
    public class ProductEventHandler {
        private final ProductReadModelRepository readModelRepository;

        public ProductEventHandler(ProductReadModelRepository readModelRepository) {
            this.readModelRepository = readModelRepository;
        }

        @EventHandler
        public void handle(ProductCreatedEvent event) {
            /** 建立讀取模型 */
            ProductReadModel readModel = new ProductReadModel(
                event.getProductId(),
                event.getName(),
                event.getDescription(),
                event.getPrice(),
                event.getCategoryId(),
                getCategoryName(event.getCategoryId()),
                BigDecimal.ZERO, // 初始評分
                0 // 初始評論數
            );

            readModelRepository.save(readModel);
        }

        @EventHandler
        public void handle(ProductPriceUpdatedEvent event) {
            /** 更新讀取模型中的價格 */
            ProductReadModel readModel = readModelRepository.findById(event.getProductId());
            if (readModel != null) {
                readModel.updatePrice(event.getNewPrice());
                readModelRepository.save(readModel);
            }
        }

        private String getCategoryName(String categoryId) {
            // 從分類服務獲取分類名稱
            return "分類名稱";
        }
    }
    ```

### TypeScript 與 Node.js 實現範例

- Commands 和 Command Handlers

    ```typescript
    /** 建立使用者命令 */
    export interface CreateUserCommand {
      email: string;
      name: string;
      password: string;
    }

    /** 命令處理器 */
    export class CreateUserCommandHandler {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly eventBus: EventBus,
        private readonly passwordHasher: PasswordHasher
      ) {}

      async handle(command: CreateUserCommand): Promise<void> {
        /** 驗證業務規則 */
        await this.validateCommand(command);

        /** 建立使用者實體 */
        const hashedPassword = await this.passwordHasher.hash(command.password);
        const user = new User(
          generateId(),
          command.email,
          command.name,
          hashedPassword
        );

        /** 儲存到寫入模型 */
        await this.userRepository.save(user);

        /** 發布事件 */
        await this.eventBus.publish(new UserCreatedEvent(
          user.getId(),
          user.getEmail(),
          user.getName()
        ));
      }

      private async validateCommand(command: CreateUserCommand): Promise<void> {
        if (!command.email || !isValidEmail(command.email)) {
          throw new Error('無效的電子郵件格式');
        }

        const existingUser = await this.userRepository.findByEmail(command.email);
        if (existingUser) {
          throw new Error('電子郵件已被使用');
        }

        if (!command.password || command.password.length < 8) {
          throw new Error('密碼長度至少需要 8 個字元');
        }
      }
    }
    ```

- Queries 和 Query Handlers

    ```typescript
    /** 使用者查詢 */
    export interface GetUsersQuery {
      search?: string;
      isActive?: boolean;
      page: number;
      limit: number;
      sortBy?: 'name' | 'email' | 'createdAt';
      sortOrder?: 'asc' | 'desc';
    }

    /** 查詢處理器 */
    export class GetUsersQueryHandler {
      constructor(
        private readonly userReadModelRepository: UserReadModelRepository
      ) {}

      async handle(query: GetUsersQuery): Promise<UserListResponse> {
        /** 從讀取模型查詢資料 */
        const users = await this.userReadModelRepository.findUsers({
          search: query.search,
          isActive: query.isActive,
          page: query.page,
          limit: query.limit,
          sortBy: query.sortBy || 'createdAt',
          sortOrder: query.sortOrder || 'desc'
        });

        const totalCount = await this.userReadModelRepository.countUsers({
          search: query.search,
          isActive: query.isActive
        });

        /** 轉換為回應格式 */
        const userDtos = users.map(user => ({
          id: user.id,
          email: user.email,
          name: user.name,
          isActive: user.isActive,
          createdAt: user.createdAt,
          lastLoginAt: user.lastLoginAt,
          profileCompleteness: user.profileCompleteness
        }));

        return {
          users: userDtos,
          totalCount,
          page: query.page,
          limit: query.limit,
          totalPages: Math.ceil(totalCount / query.limit)
        };
      }
    }
    ```

- Event Handlers (事件處理器)

    ```typescript
    /** 事件處理器 */
    export class UserEventHandler {
      constructor(
        private readonly userReadModelRepository: UserReadModelRepository,
        private readonly emailService: EmailService
      ) {}

      async handleUserCreated(event: UserCreatedEvent): Promise<void> {
        /** 建立讀取模型 */
        const readModel: UserReadModel = {
          id: event.userId,
          email: event.email,
          name: event.name,
          isActive: true,
          createdAt: new Date(),
          lastLoginAt: null,
          profileCompleteness: this.calculateProfileCompleteness(event)
        };

        await this.userReadModelRepository.save(readModel);

        /** 發送歡迎郵件 */
        await this.emailService.sendWelcomeEmail(event.email, event.name);
      }

      async handleUserProfileUpdated(event: UserProfileUpdatedEvent): Promise<void> {
        /** 更新讀取模型 */
        const readModel = await this.userReadModelRepository.findById(event.userId);
        if (readModel) {
          readModel.name = event.name;
          readModel.profileCompleteness = this.calculateProfileCompleteness(event);
          await this.userReadModelRepository.save(readModel);
        }
      }

      private calculateProfileCompleteness(data: any): number {
        let completeness = 0;
        if (data.name) completeness += 25;
        if (data.email) completeness += 25;
        if (data.avatar) completeness += 25;
        if (data.bio) completeness += 25;
        return completeness;
      }
    }
    ```

### React 前端實現範例

- Command 處理

    ```typescript
    /** 命令服務 */
    export class UserCommandService {
      constructor(private readonly httpClient: HttpClient) {}

      async createUser(command: CreateUserCommand): Promise<void> {
        await this.httpClient.post('/api/commands/users', command);
      }

      async updateUserProfile(userId: string, command: UpdateUserProfileCommand): Promise<void> {
        await this.httpClient.put(`/api/commands/users/${userId}/profile`, command);
      }

      async deactivateUser(userId: string): Promise<void> {
        await this.httpClient.post(`/api/commands/users/${userId}/deactivate`);
      }
    }

    /** React Hook */
    export const useUserCommands = () => {
      const commandService = useUserCommandService();
      const [isLoading, setIsLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);

      const createUser = async (userData: CreateUserCommand) => {
        setIsLoading(true);
        setError(null);
        try {
          await commandService.createUser(userData);
        } catch (err) {
          setError(err instanceof Error ? err.message : '建立使用者失敗');
          throw err;
        } finally {
          setIsLoading(false);
        }
      };

      return { createUser, isLoading, error };
    };
    ```

- Query 處理

    ```typescript
    /** 查詢服務 */
    export class UserQueryService {
      constructor(private readonly httpClient: HttpClient) {}

      async getUsers(query: GetUsersQuery): Promise<UserListResponse> {
        const response = await this.httpClient.get('/api/queries/users', {
          params: query
        });
        return response.data;
      }

      async getUserById(userId: string): Promise<UserDetailResponse> {
        const response = await this.httpClient.get(`/api/queries/users/${userId}`);
        return response.data;
      }

      async getUserStatistics(): Promise<UserStatisticsResponse> {
        const response = await this.httpClient.get('/api/queries/users/statistics');
        return response.data;
      }
    }

    /** React Hook */
    export const useUserQuery = (query: GetUsersQuery) => {
      const queryService = useUserQueryService();
      const [data, setData] = useState<UserListResponse | null>(null);
      const [isLoading, setIsLoading] = useState(true);
      const [error, setError] = useState<string | null>(null);

      useEffect(() => {
        const fetchUsers = async () => {
          setIsLoading(true);
          setError(null);
          try {
            const result = await queryService.getUsers(query);
            setData(result);
          } catch (err) {
            setError(err instanceof Error ? err.message : '查詢使用者失敗');
          } finally {
            setIsLoading(false);
          }
        };

        fetchUsers();
      }, [query]);

      return { data, isLoading, error, refetch: () => fetchUsers() };
    };
    ```

- React 元件

    ```typescript
    /** 使用者管理元件 */
    export const UserManagement: React.FC = () => {
      const [query, setQuery] = useState<GetUsersQuery>({
        page: 1,
        limit: 10,
        sortBy: 'createdAt',
        sortOrder: 'desc'
      });

      const { data: users, isLoading, error, refetch } = useUserQuery(query);
      const { createUser, isLoading: isCreating } = useUserCommands();
      const [showCreateForm, setShowCreateForm] = useState(false);

      const handleCreateUser = async (userData: CreateUserCommand) => {
        try {
          await createUser(userData);
          setShowCreateForm(false);
          /** 重新整理使用者列表 */
          setTimeout(() => refetch(), 1000); // 等待事件處理完成
        } catch (error) {
          console.error('建立使用者失敗:', error);
        }
      };

      const handleSearch = (searchTerm: string) => {
        setQuery(prev => ({ ...prev, search: searchTerm, page: 1 }));
      };

      const handlePageChange = (page: number) => {
        setQuery(prev => ({ ...prev, page }));
      };

      if (isLoading) return <div>載入中...</div>;
      if (error) return <div>錯誤: {error}</div>;

      return (
        <div className="user-management">
          <div className="header">
            <h1>使用者管理</h1>
            <button onClick={() => setShowCreateForm(true)}>新增使用者</button>
          </div>

          <SearchBar onSearch={handleSearch} />

          <UserTable 
            users={users?.users || []} 
            onSort={(sortBy, sortOrder) => 
              setQuery(prev => ({ ...prev, sortBy, sortOrder }))
            }
          />

          <Pagination
            currentPage={users?.page || 1}
            totalPages={users?.totalPages || 1}
            onPageChange={handlePageChange}
          />

          {showCreateForm && (
            <CreateUserModal
              onSubmit={handleCreateUser}
              onClose={() => setShowCreateForm(false)}
              isLoading={isCreating}
            />
          )}
        </div>
      );
    };
    ```

<br />

## 優點

### 效能優化

讀寫操作可以獨立優化，使用最適合的資料結構和儲存技術。

### 可擴展性

- 讀寫操作可以獨立擴展

- 可以針對不同需求選擇不同的資料庫技術

- 支援水平擴展

### 簡化複雜性

- 複雜的查詢需求不會影響寫入模型的設計

- 業務規則與查詢需求分離

- 每個模型都有明確的職責

### 靈活性

- 可以為不同的查詢需求建立多個讀取模型

- 支援不同的資料格式和結構

- 容易添加新的查詢功能

<br />

## 缺點

### 複雜性增加

需要維護兩套不同的模型和資料同步機制。

### 最終一致性

讀寫模型之間可能存在資料不一致的情況。

### 開發成本

需要更多的程式碼和基礎設施來支援分離的模型。

### 資料同步挑戰

需要確保讀寫模型之間的資料同步正確性。

<br />

## 適用場景

### 適合使用

- 高讀寫比例：讀取操作遠多於寫入操作

- 複雜查詢需求：需要複雜的報表和分析功能

- 效能要求高：對讀寫效能都有高要求

- 不同團隊負責：讀寫功能由不同團隊開發維護

- 多種查詢介面：需要支援多種不同的查詢需求

### 不適合使用

- 簡單 CRUD 應用：只有基本的增刪改查需求

- 強一致性要求：需要即時的資料一致性

- 小型應用：系統規模小，複雜度低

- 資源有限：開發和維護資源不足

<br />

## 實施建議

### 從簡單開始

可以先在單一應用程式中實現 CQRS，不一定需要分離到不同的服務。

### 選擇合適的同步機制

- 同步更新：適合強一致性需求

- 非同步事件：適合最終一致性需求

- 定期同步：適合對即時性要求不高的場景

### 監控和告警

建立完善的監控機制，及時發現資料同步問題。

### 錯誤處理

設計完善的錯誤處理和重試機制，確保資料同步的可靠性。

### 測試策略

建立完整的測試套件，特別是資料同步和一致性的測試。

<br />

## 與其他模式的結合

### Event Sourcing

CQRS 常與 Event Sourcing 結合，使用事件作為資料同步的機制。

### Domain-Driven Design (DDD)

CQRS 可以很好配合 DDD 的聚合和限界上下文概念。

### Microservices

在微服務架構中，每個服務可以獨立實現 CQRS 模式。

<br />

## 總結

CQRS 是一個強大的架構模式，特別適合需要處理複雜查詢需求和高效能要求的系統。通過分離讀寫操作，系統可以獲得更好的效能、可擴展性和維護性。

但是，CQRS 也帶來了額外的複雜性和開發成本。在決定是否採用 CQRS 時，需要仔細評估系統的實際需求，確保收益大於成本。對於簡單的應用程式，傳統的 CRUD 模式可能更加合適；但對於複雜的企業級應用，CQRS 能夠帶來顯著的價值。
