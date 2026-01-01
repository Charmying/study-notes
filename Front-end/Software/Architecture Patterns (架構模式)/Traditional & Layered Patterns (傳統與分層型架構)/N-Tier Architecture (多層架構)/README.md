# N-Tier Architecture (多層架構)

N-Tier Architecture (多層架構) 是一種將應用程式分為多個層次的軟體架構模式，每個層次負責特定的功能，並且只能與相鄰的層次進行通訊。

這種架構強調關注點分離，將不同的職責分配到不同的層次中，使系統更容易維護、擴展和部署。

<br />

## 動機

在軟體開發中，常見的問題包括

- 程式碼混雜在一起，難以維護和測試

- 業務規則與資料存取緊密耦合

- 使用者介面與業務處理混合

- 系統難以擴展和部署

N-Tier Architecture 通過分層設計，解決這些問題，讓系統具備

- 關注點分離：每層專注於特定職責

- 可維護性：層次間的清楚界限便於維護

- 可擴展性：可以獨立擴展特定層次

- 可重用性：層次可以被其他應用程式重用

<br />

## 結構

N-Tier Architecture 通常分為三到四個主要層次，最常見的是三層架構 (3-Tier)

### 1. Presentation Tier (展示層)

負責使用者介面和使用者互動。

- 處理使用者輸入和顯示輸出

- 包含 Web 頁面、桌面應用程式、行動應用程式

- 不包含業務規則

### 2. Business Logic Tier (業務層)

包含應用程式的核心業務規則和處理。

- 處理業務規則和工作流程

- 協調資料存取和業務處理

- 驗證業務規則

### 3. Data Access Tier (資料存取層)

負責與資料儲存系統的互動。

- 處理資料庫操作

- 管理資料持久化

- 提供資料存取介面

### 4. Database Tier (資料庫層)

實際的資料儲存系統。

- 關聯式資料庫、NoSQL 資料庫

- 檔案系統、雲端儲存

- 外部資料服務

以下是 N-Tier Architecture 的層次圖

```text
┌─────────────────────────────────────────┐
│            Presentation Tier            │
│          (Web UI, Mobile App)           │
└─────────────────┬───────────────────────┘
                  │ HTTP/API Calls
┌─────────────────▼───────────────────────┐
│           Business Logic Tier           │
│          (Application Services)         │
└─────────────────┬───────────────────────┘
                  │ Data Operations
┌─────────────────▼───────────────────────┐
│            Data Access Tier             │
│          (Repositories, DAOs)           │
└─────────────────┬───────────────────────┘
                  │ SQL/NoSQL Queries
┌─────────────────▼───────────────────────┐
│             Database Tier               │
│        (MySQL, PostgreSQL, etc.)        │
└─────────────────────────────────────────┘
```

<br />

## 核心原則

### 分層隔離 (Layer Isolation)

每一層只能與相鄰的層次通訊，不能跨層存取。

### 單向依賴 (Unidirectional Dependencies)

上層可以依賴下層，但下層不能依賴上層。

### 關注點分離 (Separation of Concerns)

每一層都有明確且單一的職責。

<br />

## 實現方式

### Java Spring Boot 實現範例

以電商系統的產品管理為例

- Data Access Tier (資料存取層)

    ```java
    /** 資料實體 */
    @Entity
    @Table(name = "products")
    public class ProductEntity {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(nullable = false)
        private String name;

        @Column(nullable = false)
        private BigDecimal price;

        @Column
        private String description;

        @Column(nullable = false)
        private Integer stock;

        // Constructors, getters, setters
    }

    /** 資料存取物件 */
    @Repository
    public interface ProductRepository extends JpaRepository<ProductEntity, Long> {
        List<ProductEntity> findByNameContaining(String name);
        List<ProductEntity> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
        List<ProductEntity> findByStockGreaterThan(Integer minStock);
    }
    ```

- Business Logic Tier (業務層)

    ```java
    /** 業務模型 */
    public class Product {
        private Long id;
        private String name;
        private BigDecimal price;
        private String description;
        private Integer stock;

        public void updateStock(Integer quantity) {
            if (quantity < 0) {
                throw new IllegalArgumentException("庫存不能為負數");
            }
            this.stock = quantity;
        }

        public boolean isAvailable() {
            return stock > 0;
        }

        // Constructors, getters, setters
    }

    /** 業務服務 */
    @Service
    @Transactional
    public class ProductService {
        private final ProductRepository productRepository;

        public ProductService(ProductRepository productRepository) {
            this.productRepository = productRepository;
        }

        public Product createProduct(String name, BigDecimal price, String description, Integer stock) {
            if (price.compareTo(BigDecimal.ZERO) <= 0) {
                throw new IllegalArgumentException("價格必須大於零");
            }

            ProductEntity entity = new ProductEntity();
            entity.setName(name);
            entity.setPrice(price);
            entity.setDescription(description);
            entity.setStock(stock);

            ProductEntity saved = productRepository.save(entity);
            return mapToProduct(saved);
        }

        public List<Product> searchProducts(String keyword) {
            List<ProductEntity> entities = productRepository.findByNameContaining(keyword);
            return entities.stream()
                .map(this::mapToProduct)
                .collect(Collectors.toList());
        }

        public void updateProductStock(Long productId, Integer newStock) {
            ProductEntity entity = productRepository.findById(productId)
                .orElseThrow(() -> new ProductNotFoundException("產品不存在"));

            entity.setStock(newStock);
            productRepository.save(entity);
        }

        private Product mapToProduct(ProductEntity entity) {
            return new Product(
                entity.getId(),
                entity.getName(),
                entity.getPrice(),
                entity.getDescription(),
                entity.getStock()
            );
        }
    }
    ```

- Presentation Tier (展示層)

    ```java
    /** 請求/回應模型 */
    public class CreateProductRequest {
        private String name;
        private BigDecimal price;
        private String description;
        private Integer stock;

        // Getters, setters
    }

    public class ProductResponse {
        private Long id;
        private String name;
        private BigDecimal price;
        private String description;
        private Integer stock;
        private boolean available;

        public static ProductResponse from(Product product) {
            ProductResponse response = new ProductResponse();
            response.setId(product.getId());
            response.setName(product.getName());
            response.setPrice(product.getPrice());
            response.setDescription(product.getDescription());
            response.setStock(product.getStock());
            response.setAvailable(product.isAvailable());
            return response;
        }

        // Getters, setters
    }

    /** 控制器 */
    @RestController
    @RequestMapping("/api/products")
    public class ProductController {
        private final ProductService productService;

        public ProductController(ProductService productService) {
            this.productService = productService;
        }

        @PostMapping
        public ResponseEntity<ProductResponse> createProduct(@RequestBody CreateProductRequest request) {
            try {
                Product product = productService.createProduct(
                    request.getName(),
                    request.getPrice(),
                    request.getDescription(),
                    request.getStock()
                );
                return ResponseEntity.ok(ProductResponse.from(product));
            } catch (IllegalArgumentException e) {
                return ResponseEntity.badRequest().build();
            }
        }

        @GetMapping("/search")
        public ResponseEntity<List<ProductResponse>> searchProducts(@RequestParam String keyword) {
            List<Product> products = productService.searchProducts(keyword);
            List<ProductResponse> responses = products.stream()
                .map(ProductResponse::from)
                .collect(Collectors.toList());
            return ResponseEntity.ok(responses);
        }

        @PutMapping("/{id}/stock")
        public ResponseEntity<Void> updateStock(@PathVariable Long id, @RequestParam Integer stock) {
            try {
                productService.updateProductStock(id, stock);
                return ResponseEntity.ok().build();
            } catch (ProductNotFoundException e) {
                return ResponseEntity.notFound().build();
            }
        }
    }
    ```

### Node.js Express 實現範例

- Data Access Tier (資料存取層)

    ```typescript
    /** 資料模型 */
    import mongoose, { Schema, Document } from 'mongoose';

    export interface IUser extends Document {
      email: string;
      name: string;
      password: string;
      createdAt: Date;
    }

    const UserSchema: Schema = new Schema({
      email: { type: String, required: true, unique: true },
      name: { type: String, required: true },
      password: { type: String, required: true },
      createdAt: { type: Date, default: Date.now }
    });

    export const UserModel = mongoose.model<IUser>('User', UserSchema);

    /** 資料存取層 */
    export class UserRepository {
      async create(userData: Partial<IUser>): Promise<IUser> {
        const user = new UserModel(userData);
        return await user.save();
      }

      async findByEmail(email: string): Promise<IUser | null> {
        return await UserModel.findOne({ email });
      }

      async findById(id: string): Promise<IUser | null> {
        return await UserModel.findById(id);
      }

      async updateById(id: string, updateData: Partial<IUser>): Promise<IUser | null> {
        return await UserModel.findByIdAndUpdate(id, updateData, { new: true });
      }

      async deleteById(id: string): Promise<boolean> {
        const result = await UserModel.findByIdAndDelete(id);
        return result !== null;
      }
    }
    ```

- Business Logic Tier (業務層)

    ```typescript
    import bcrypt from 'bcrypt';
    import jwt from 'jsonwebtoken';

    /** 業務模型 */
    export class User {
      constructor(
        public id: string,
        public email: string,
        public name: string,
        public createdAt: Date
      ) {}

      static fromDocument(doc: IUser): User {
        return new User(doc._id, doc.email, doc.name, doc.createdAt);
      }
    }

    /** 業務服務 */
    export class UserService {
      constructor(private userRepository: UserRepository) {}

      async registerUser(email: string, name: string, password: string): Promise<User> {
        /** 檢查 email 是否已存在 */
        const existingUser = await this.userRepository.findByEmail(email);
        if (existingUser) {
          throw new Error('Email 已被註冊');
        }

        /** 驗證輸入 */
        if (!this.isValidEmail(email)) {
          throw new Error('Email 格式不正確');
        }

        if (password.length < 6) {
          throw new Error('密碼長度至少 6 個字元');
        }

        /** 加密密碼 */
        const hashedPassword = await bcrypt.hash(password, 10);

        /** 建立使用者 */
        const userDoc = await this.userRepository.create({
          email,
          name,
          password: hashedPassword
        });

        return User.fromDocument(userDoc);
      }

      async authenticateUser(email: string, password: string): Promise<string> {
        const userDoc = await this.userRepository.findByEmail(email);
        if (!userDoc) {
          throw new Error('使用者不存在');
        }

        const isPasswordValid = await bcrypt.compare(password, userDoc.password);
        if (!isPasswordValid) {
          throw new Error('密碼錯誤');
        }

        /** 產生 JWT Token */
        const token = jwt.sign(
          { userId: userDoc._id, email: userDoc.email },
          process.env.JWT_SECRET || 'default-secret',
          { expiresIn: '24h' }
        );

        return token;
      }

      async getUserById(id: string): Promise<User | null> {
        const userDoc = await this.userRepository.findById(id);
        return userDoc ? User.fromDocument(userDoc) : null;
      }

      private isValidEmail(email: string): boolean {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      }
    }
    ```

- Presentation Tier (展示層)

    ```typescript
    import express, { Request, Response } from 'express';

    /** 請求/回應介面 */
    interface RegisterRequest {
      email: string;
      name: string;
      password: string;
    }

    interface LoginRequest {
      email: string;
      password: string;
    }

    interface UserResponse {
      id: string;
      email: string;
      name: string;
      createdAt: Date;
    }

    /** 控制器 */
    export class UserController {
      constructor(private userService: UserService) {}

      async register(req: Request, res: Response): Promise<void> {
        try {
          const { email, name, password }: RegisterRequest = req.body;

          const user = await this.userService.registerUser(email, name, password);

          const response: UserResponse = {
            id: user.id,
            email: user.email,
            name: user.name,
            createdAt: user.createdAt
          };

          res.status(201).json({
            success: true,
            data: response,
            message: '註冊成功'
          });
        } catch (error) {
          res.status(400).json({
            success: false,
            message: error.message
          });
        }
      }

      async login(req: Request, res: Response): Promise<void> {
        try {
          const { email, password }: LoginRequest = req.body;

          const token = await this.userService.authenticateUser(email, password);

          res.json({
            success: true,
            data: { token },
            message: '登入成功'
          });
        } catch (error) {
          res.status(401).json({
            success: false,
            message: error.message
          });
        }
      }

      async getProfile(req: Request, res: Response): Promise<void> {
        try {
          const userId = req.user?.id; /** 從 JWT middleware 取得 */

          const user = await this.userService.getUserById(userId);
          if (!user) {
            res.status(404).json({
              success: false,
              message: '使用者不存在'
            });
            return;
          }

          const response: UserResponse = {
            id: user.id,
            email: user.email,
            name: user.name,
            createdAt: user.createdAt
          };

          res.json({
            success: true,
            data: response
          });
        } catch (error) {
          res.status(500).json({
            success: false,
            message: '伺服器錯誤'
          });
        }
      }
    }

    /** 路由設定 */
    export function createUserRoutes(userController: UserController): express.Router {
      const router = express.Router();

      router.post('/register', (req, res) => userController.register(req, res));
      router.post('/login', (req, res) => userController.login(req, res));
      router.get('/profile', authenticateToken, (req, res) => userController.getProfile(req, res));

      return router;
    }
    ```

### React 前端實現範例

- Presentation Tier (展示層)

    ```typescript
    /** API 服務層 */
    export class ApiService {
      private baseURL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

      async post<T>(endpoint: string, data: any): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || '請求失敗');
        }

        return response.json();
      }

      async get<T>(endpoint: string): Promise<T> {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || '請求失敗');
        }

        return response.json();
      }
    }

    /** 使用者服務 */
    export class UserApiService {
      constructor(private apiService: ApiService) {}

      async register(email: string, name: string, password: string) {
        return this.apiService.post('/users/register', { email, name, password });
      }

      async login(email: string, password: string) {
        return this.apiService.post('/users/login', { email, password });
      }

      async getProfile() {
        return this.apiService.get('/users/profile');
      }
    }
    ```

- UI 元件

    ```typescript
    /** 登入表單元件 */
    export const LoginForm: React.FC = () => {
      const [email, setEmail] = useState('');
      const [password, setPassword] = useState('');
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState('');
      const userApiService = new UserApiService(new ApiService());

      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
          const response = await userApiService.login(email, password);
          localStorage.setItem('token', response.data.token);
          window.location.href = '/dashboard';
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };

      return (
        <form onSubmit={handleSubmit} className="login-form">
          <h2>登入</h2>

          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">密碼:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? '登入中...' : '登入'}
          </button>
        </form>
      );
    };

    /** 使用者資料元件 */
    export const UserProfile: React.FC = () => {
      const [user, setUser] = useState(null);
      const [loading, setLoading] = useState(true);
      const userApiService = new UserApiService(new ApiService());

      useEffect(() => {
        loadUserProfile();
      }, []);

      const loadUserProfile = async () => {
        try {
          const response = await userApiService.getProfile();
          setUser(response.data);
        } catch (error) {
          console.error('載入使用者資料失敗:', error);
        } finally {
          setLoading(false);
        }
      };

      if (loading) {
        return <div>載入中...</div>;
      }

      if (!user) {
        return <div>無法載入使用者資料</div>;
      }

      return (
        <div className="user-profile">
          <h2>使用者資料</h2>
          <div className="profile-info">
            <p><strong>姓名:</strong> {user.name}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>註冊時間:</strong> {new Date(user.createdAt).toLocaleDateString()}</p>
          </div>
        </div>
      );
    };
    ```

<br />

## 優點

### 關注點分離

每一層都有明確的職責，使程式碼更容易理解和維護。

### 可維護性

層次間的清楚界限使得修改某一層不會影響其他層。

### 可擴展性

可以獨立擴展特定層次，例如：增加更多的展示層或資料存取層。

### 可重用性

業務層和資料存取層可以被不同的展示層重用。

### 團隊協作

不同團隊可以專注於不同的層次進行開發。

<br />

## 缺點

### 效能開銷

層次間的通訊會增加系統的延遲和資源消耗。

### 複雜性

對於簡單的應用程式來說可能過於複雜。

### 網路延遲

當層次分佈在不同伺服器時，網路延遲會影響效能。

### 資料傳遞

需要在層次間進行資料轉換和傳遞，增加開發工作量。

<br />

## 適用場景

### 適合使用

- 企業級應用：需要清楚的架構和職責分離

- 大型團隊開發：多個團隊需要並行開發

- 多平台支援：需要支援多種使用者介面

- 長期維護：需要長期維護和擴展的系統

- 複雜業務規則：有複雜的業務處理需求

### 不適合使用

- 簡單應用程式：只有基本功能的小型應用

- 高效能要求：對延遲敏感的即時系統

- 快速原型：需要快速開發和驗證的專案

- 資源受限：硬體資源有限的環境

<br />

## 變體

### 2-Tier Architecture (兩層架構)

- Client-Server 架構

- 客戶端包含展示層和業務層

- 伺服器端包含資料存取層和資料庫層

### 4-Tier Architecture (四層架構)

- 在三層架構基礎上增加 Web 伺服器層

- 更好的負載分散和安全性

- 適合大型 Web 應用程式

### Multi-Tier Architecture (多層架構)

- 超過四層的架構

- 可能包含快取層、訊息佇列層等

- 適合超大型分散式系統

<br />

## 實施建議

### 明確層次職責

確保每一層都有明確且單一的職責，避免職責重疊。

### 定義清楚介面

層次間的介面應該清楚且穩定，減少耦合度。

### 錯誤處理

建立統一的錯誤處理機制，確保錯誤能夠正確傳遞和處理。

### 效能監控

監控層次間的通訊效能，識別和解決效能瓶頸。

### 安全考量

在每一層都實施適當的安全措施，特別是資料傳輸和存取控制。

<br />

## 總結

N-Tier Architecture 提供了一個結構化的方法來組織應用程式，特別適合需要清楚職責分離和團隊協作的專案。雖然會增加一定的複雜性和效能開銷，但對於大型企業應用來說，這種架構模式能夠帶來更好的可維護性、可擴展性和可重用性。

關鍵在於根據專案的規模和需求來選擇合適的層次數量和分佈方式。對於簡單的應用程式，可能兩層或三層就足夠；但對於複雜的企業系統，可能需要更多的層次來處理不同的關注點。
