# Layered Architecture (分層架構)

Layered Architecture (分層架構) 是最常見且廣泛使用的軟體架構模式之一，將應用程式組織成水平分層的結構，每一層都有特定的職責和角色。

這種架構強調關注點分離，通過將不同的功能分配到不同的層次中，使系統更容易理解、開發和維護。

<br />

## 動機

在軟體開發中，常見的問題包括

- 程式碼混亂，業務規則與技術實現交織在一起

- 缺乏明確的職責分工，導致程式碼難以維護

- 修改一個功能時影響到其他不相關的部分

- 團隊成員難以並行開發，容易產生衝突

Layered Architecture 通過分層設計，解決這些問題，讓系統具備

- 清晰性：每一層都有明確的職責和界限

- 可維護性：修改某一層不會影響其他層

- 可重用性：各層可以獨立重用

- 可測試性：每一層都可以獨立測試

<br />

## 結構

Layered Architecture 通常採用三層或四層結構，從上到下分為

### 三層架構

#### 1. Presentation Layer (展示層)

負責處理使用者介面和使用者互動。

- 接收使用者輸入

- 顯示資料給使用者

- 處理 UI 相關的業務

#### 2. Business Layer (業務層)

包含核心業務規則和應用程式功能。

- 實現業務規則

- 協調資料存取

- 處理業務流程

#### 3. Data Access Layer (資料存取層)

負責與資料儲存系統互動。

- 資料庫操作

- 檔案系統存取

- 外部服務呼叫

### 四層架構

#### 1. Presentation Layer (展示層)

與三層架構相同，負責使用者介面。

#### 2. Business Layer (業務層)

與三層架構相同，包含業務規則。

#### 3. Persistence Layer (持久層)

專門負責資料持久化操作。

- ORM 映射

- 資料庫連接管理

- 快取處理

#### 4. Database Layer (資料庫層)

實際的資料儲存系統。

- 關聯式資料庫

- NoSQL 資料庫

- 檔案系統

以下是 Layered Architecture 的層次圖

```text
┌────────────────────────────────────────┐
│          Presentation Layer            │
│       (Controllers, Views, UI)         │
├────────────────────────────────────────┤
│            Business Layer              │
│       (Services, Domain Logic)         │
├────────────────────────────────────────┤
│           Data Access Layer            │
│      (Repositories, DAOs, APIs)        │
├────────────────────────────────────────┤
│            Database Layer              │
│         (MySQL, MongoDB, Files)        │
└────────────────────────────────────────┘
```

<br />

## 核心原則

### 單向依賴 (Unidirectional Dependency)

上層可以依賴下層，但下層不能依賴上層。

### 關注點分離 (Separation of Concerns)

每一層都有明確且單一的職責。

### 抽象化 (Abstraction)

上層通過介面與下層互動，不直接依賴具體實現。

<br />

## 實現方式

### Java Spring Boot 實現範例

以電商系統的商品管理為例

- Presentation Layer (展示層)

    ```java
    /** REST Controller */
    @RestController
    @RequestMapping("/api/products")
    public class ProductController {
        private final ProductService productService;

        public ProductController(ProductService productService) {
            this.productService = productService;
        }

        @GetMapping
        public ResponseEntity<List<ProductDto>> getAllProducts() {
            List<ProductDto> products = productService.getAllProducts();
            return ResponseEntity.ok(products);
        }

        @PostMapping
        public ResponseEntity<ProductDto> createProduct(@RequestBody CreateProductRequest request) {
            ProductDto product = productService.createProduct(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(product);
        }

        @GetMapping("/{id}")
        public ResponseEntity<ProductDto> getProduct(@PathVariable Long id) {
            ProductDto product = productService.getProductById(id);
            return ResponseEntity.ok(product);
        }
    }
    ```

- Business Layer (業務層)

    ```java
    /** Service Interface */
    public interface ProductService {
        List<ProductDto> getAllProducts();
        ProductDto getProductById(Long id);
        ProductDto createProduct(CreateProductRequest request);
        ProductDto updateProduct(Long id, UpdateProductRequest request);
        void deleteProduct(Long id);
    }

    /** Service Implementation */
    @Service
    @Transactional
    public class ProductServiceImpl implements ProductService {
        private final ProductRepository productRepository;
        private final ProductMapper productMapper;

        public ProductServiceImpl(ProductRepository productRepository, ProductMapper productMapper) {
            this.productRepository = productRepository;
            this.productMapper = productMapper;
        }

        @Override
        public List<ProductDto> getAllProducts() {
            List<Product> products = productRepository.findAll();
            return products.stream()
                .map(productMapper::toDto)
                .collect(Collectors.toList());
        }

        @Override
        public ProductDto createProduct(CreateProductRequest request) {
            /** 業務驗證 */
            validateProductData(request);

            /** 建立產品 */
            Product product = Product.builder()
                .name(request.getName())
                .description(request.getDescription())
                .price(request.getPrice())
                .category(request.getCategory())
                .build();

            /** 儲存產品 */
            Product savedProduct = productRepository.save(product);
            return productMapper.toDto(savedProduct);
        }

        private void validateProductData(CreateProductRequest request) {
            if (request.getPrice().compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("商品價格必須大於零");
            }
            if (productRepository.existsByName(request.getName())) {
                throw new IllegalArgumentException("商品名稱已存在");
            }
        }
    }
    ```

- Data Access Layer (資料存取層)

    ```java
    /** Repository Interface */
    public interface ProductRepository extends JpaRepository<Product, Long> {
        List<Product> findByCategory(String category);
        boolean existsByName(String name);
        List<Product> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
    }

    /** Entity */
    @Entity
    @Table(name = "products")
    public class Product {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(nullable = false, unique = true)
        private String name;

        @Column(length = 1000)
        private String description;

        @Column(nullable = false, precision = 10, scale = 2)
        private BigDecimal price;

        @Column(nullable = false)
        private String category;

        @CreationTimestamp
        private LocalDateTime createdAt;

        @UpdateTimestamp
        private LocalDateTime updatedAt;

        /** Constructors, getters, setters */
    }
    ```

### Node.js Express 實現範例

- Presentation Layer (展示層)

    ```typescript
    /** Controller */
    export class UserController {
      constructor(private readonly userService: UserService) {}

      async getUsers(req: Request, res: Response): Promise<void> {
        try {
          const users = await this.userService.getAllUsers();
          res.json(users);
        } catch (error) {
          res.status(500).json({ error: error.message });
        }
      }

      async createUser(req: Request, res: Response): Promise<void> {
        try {
          const userData = req.body;
          const user = await this.userService.createUser(userData);
          res.status(201).json(user);
        } catch (error) {
          res.status(400).json({ error: error.message });
        }
      }

      async getUserById(req: Request, res: Response): Promise<void> {
        try {
          const { id } = req.params;
          const user = await this.userService.getUserById(id);
          res.json(user);
        } catch (error) {
          res.status(404).json({ error: error.message });
        }
      }
    }

    /** Routes */
    const router = express.Router();
    const userController = new UserController(userService);

    router.get('/users', userController.getUsers.bind(userController));
    router.post('/users', userController.createUser.bind(userController));
    router.get('/users/:id', userController.getUserById.bind(userController));
    ```

- Business Layer (業務層)

    ```typescript
    /** Service Interface */
    export interface UserService {
      getAllUsers(): Promise<UserDto[]>;
      getUserById(id: string): Promise<UserDto>;
      createUser(userData: CreateUserDto): Promise<UserDto>;
      updateUser(id: string, userData: UpdateUserDto): Promise<UserDto>;
      deleteUser(id: string): Promise<void>;
    }

    /** Service Implementation */
    export class UserServiceImpl implements UserService {
      constructor(
        private readonly userRepository: UserRepository,
        private readonly emailService: EmailService
      ) {}

      async getAllUsers(): Promise<UserDto[]> {
        const users = await this.userRepository.findAll();
        return users.map(this.mapToDto);
      }

      async createUser(userData: CreateUserDto): Promise<UserDto> {
        /** 業務驗證 */
        await this.validateUserData(userData);

        /** 建立使用者 */
        const user: User = {
          id: generateId(),
          email: userData.email,
          name: userData.name,
          createdAt: new Date(),
          isActive: true
        };

        /** 儲存使用者 */
        const savedUser = await this.userRepository.save(user);

        /** 發送歡迎郵件 */
        await this.emailService.sendWelcomeEmail(savedUser.email, savedUser.name);

        return this.mapToDto(savedUser);
      }

      private async validateUserData(userData: CreateUserDto): Promise<void> {
        if (!this.isValidEmail(userData.email)) {
          throw new Error('無效的電子郵件格式');
        }

        const existingUser = await this.userRepository.findByEmail(userData.email);
        if (existingUser) {
          throw new Error('電子郵件已被使用');
        }
      }

      private isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      }

      private mapToDto(user: User): UserDto {
        return {
          id: user.id,
          email: user.email,
          name: user.name,
          isActive: user.isActive,
          createdAt: user.createdAt
        };
      }
    }
    ```

- Data Access Layer (資料存取層)

    ```typescript
    /** Repository Interface */
    export interface UserRepository {
      findAll(): Promise<User[]>;
      findById(id: string): Promise<User | null>;
      findByEmail(email: string): Promise<User | null>;
      save(user: User): Promise<User>;
      update(id: string, user: Partial<User>): Promise<User>;
      delete(id: string): Promise<void>;
    }

    /** MongoDB Repository Implementation */
    export class MongoUserRepository implements UserRepository {
      constructor(private readonly userModel: Model<UserDocument>) {}

      async findAll(): Promise<User[]> {
        const users = await this.userModel.find({ isActive: true }).exec();
        return users.map(this.mapToUser);
      }

      async findById(id: string): Promise<User | null> {
        const user = await this.userModel.findById(id).exec();
        return user ? this.mapToUser(user) : null;
      }

      async findByEmail(email: string): Promise<User | null> {
        const user = await this.userModel.findOne({ email }).exec();
        return user ? this.mapToUser(user) : null;
      }

      async save(user: User): Promise<User> {
        const userDoc = new this.userModel(user);
        const savedUser = await userDoc.save();
        return this.mapToUser(savedUser);
      }

      private mapToUser(doc: UserDocument): User {
        return {
          id: doc._id.toString(),
          email: doc.email,
          name: doc.name,
          isActive: doc.isActive,
          createdAt: doc.createdAt
        };
      }
    }

    /** User Model */
    export interface User {
      id: string;
      email: string;
      name: string;
      isActive: boolean;
      createdAt: Date;
    }
    ```

### React 前端實現範例

- Presentation Layer (展示層)

    ```typescript
    /** React Component */
    export const ProductList: React.FC = () => {
      const [products, setProducts] = useState<Product[]>([]);
      const [loading, setLoading] = useState(true);
      const [error, setError] = useState<string | null>(null);
      const productService = useProductService();

      useEffect(() => {
        loadProducts();
      }, []);

      const loadProducts = async () => {
        try {
          setLoading(true);
          const productList = await productService.getAllProducts();
          setProducts(productList);
        } catch (err) {
          setError('載入商品失敗');
        } finally {
          setLoading(false);
        }
      };

      const handleDeleteProduct = async (id: string) => {
        try {
          await productService.deleteProduct(id);
          setProducts(products.filter(p => p.id !== id));
        } catch (err) {
          setError('刪除商品失敗');
        }
      };

      if (loading) return <div>載入中...</div>;
      if (error) return <div>錯誤: {error}</div>;

      return (
        <div className="product-list">
          <h2>商品列表</h2>
          <div className="products">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onDelete={handleDeleteProduct}
              />
            ))}
          </div>
        </div>
      );
    };
    ```

- Business Layer (業務層)

    ```typescript
    /** Service Interface */
    export interface ProductService {
      getAllProducts(): Promise<Product[]>;
      getProductById(id: string): Promise<Product>;
      createProduct(product: CreateProductDto): Promise<Product>;
      updateProduct(id: string, product: UpdateProductDto): Promise<Product>;
      deleteProduct(id: string): Promise<void>;
    }

    /** Service Implementation */
    export class ProductServiceImpl implements ProductService {
      constructor(private readonly productRepository: ProductRepository) {}

      async getAllProducts(): Promise<Product[]> {
        return await this.productRepository.findAll();
      }

      async createProduct(productData: CreateProductDto): Promise<Product> {
        /** 業務驗證 */
        this.validateProductData(productData);

        /** 建立商品 */
        const product: Product = {
          id: generateId(),
          name: productData.name,
          description: productData.description,
          price: productData.price,
          category: productData.category,
          createdAt: new Date(),
          isActive: true
        };

        return await this.productRepository.save(product);
      }

      private validateProductData(productData: CreateProductDto): void {
        if (!productData.name || productData.name.trim().length === 0) {
          throw new Error('商品名稱不能為空');
        }

        if (productData.price <= 0) {
          throw new Error('商品價格必須大於零');
        }

        if (!productData.category) {
          throw new Error('必須選擇商品類別');
        }
      }
    }
    ```

- Data Access Layer (資料存取層)

    ```typescript
    /** Repository Interface */
    export interface ProductRepository {
      findAll(): Promise<Product[]>;
      findById(id: string): Promise<Product | null>;
      findByCategory(category: string): Promise<Product[]>;
      save(product: Product): Promise<Product>;
      update(id: string, product: Partial<Product>): Promise<Product>;
      delete(id: string): Promise<void>;
    }

    /** API Repository Implementation */
    export class ApiProductRepository implements ProductRepository {
      constructor(private readonly httpClient: HttpClient) {}

      async findAll(): Promise<Product[]> {
        const response = await this.httpClient.get<Product[]>('/api/products');
        return response.data;
      }

      async findById(id: string): Promise<Product | null> {
        try {
          const response = await this.httpClient.get<Product>(`/api/products/${id}`);
          return response.data;
        } catch (error) {
          if (error.status === 404) {
            return null;
          }
          throw error;
        }
      }

      async save(product: Product): Promise<Product> {
        const response = await this.httpClient.post<Product>('/api/products', product);
        return response.data;
      }

      async delete(id: string): Promise<void> {
        await this.httpClient.delete(`/api/products/${id}`);
      }
    }

    /** Local Storage Repository Implementation */
    export class LocalStorageProductRepository implements ProductRepository {
      private readonly storageKey = 'products';

      async findAll(): Promise<Product[]> {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : [];
      }

      async save(product: Product): Promise<Product> {
        const products = await this.findAll();
        const existingIndex = products.findIndex(p => p.id === product.id);

        if (existingIndex >= 0) {
          products[existingIndex] = product;
        } else {
          products.push(product);
        }

        localStorage.setItem(this.storageKey, JSON.stringify(products));
        return product;
      }
    }
    ```

<br />

## 優點

### 簡單易懂

分層結構直觀，容易理解和學習。

### 關注點分離

每一層都有明確的職責，便於維護和修改。

### 可重用性

各層可以獨立重用，特別是業務層和資料存取層。

### 團隊協作

不同團隊可以並行開發不同的層次。

### 可測試性

每一層都可以獨立進行單元測試。

### 技術獨立性

可以獨立更換某一層的技術實現。

<br />

## 缺點

### 性能開銷

層與層之間的呼叫會產生額外的性能開銷。

### 過度設計

對於簡單的應用程式可能會造成過度設計。

### 緊密耦合風險

若設計不當，層與層之間可能會產生緊密耦合。

### 資料傳遞複雜

資料需要在多個層之間傳遞，可能會變得複雜。

### 變更影響

底層的變更可能會影響到上層的實現。

<br />

## 適用場景

### 適合使用

- 企業級應用：需要清晰的架構和職責分工

- 團隊開發：多人協作的大型專案

- 長期維護：需要長期維護和擴展的系統

- 複雜業務：有複雜業務規則的應用程式

- 多平台支援：需要支援多種前端或介面

### 不適合使用

- 簡單應用：功能簡單的小型應用程式

- 高性能要求：對性能要求極高的系統

- 快速原型：需要快速開發的原型專案

- 微服務架構：已經採用微服務的分散式系統

<br />

## 變體模式

### 開放分層架構 (Open Layered Architecture)

允許跨層呼叫，上層可以直接呼叫任何下層。

### 封閉分層架構 (Closed Layered Architecture)

嚴格限制只能呼叫相鄰的下一層。

### 鬆散分層架構 (Relaxed Layered Architecture)

允許某些特定情況下的跨層呼叫。

<br />

## 實施建議

### 明確定義層次

清楚定義每一層的職責和邊界。

### 使用介面

通過介面來定義層與層之間的契約。

### 避免循環依賴

確保依賴關係是單向的，避免循環依賴。

### 適當的抽象

在適當的層次進行抽象，不要過度抽象。

### 統一的錯誤處理

建立統一的錯誤處理機制。

### 效能監控

監控層與層之間的呼叫效能。

<br />

## 與其他架構模式的比較

### vs Clean Architecture

- Layered Architecture 依賴方向是單向向下

- Clean Architecture 使用依賴反轉，內層不依賴外層

### vs MVC

- Layered Architecture 是水平分層

- MVC 是垂直分離關注點

### vs Microservices

- Layered Architecture 是單體應用的內部結構

- Microservices 是分散式系統的服務劃分

<br />

## 總結

Layered Architecture 是一個經典且實用的架構模式，特別適合傳統的企業級應用開發。雖然在某些現代架構趨勢下可能顯得保守，但其簡單明瞭的結構和清晰的職責分工，使其在許多場景下仍然是很好的選擇。

關鍵在於根據專案的複雜度、團隊規模和長期維護需求來決定是否採用分層架構。對於需要清晰結構和團隊協作的專案，分層架構能夠提供穩定可靠的基礎；但對於追求高性能或快速迭代的專案，可能需要考慮其他更靈活的架構模式。
