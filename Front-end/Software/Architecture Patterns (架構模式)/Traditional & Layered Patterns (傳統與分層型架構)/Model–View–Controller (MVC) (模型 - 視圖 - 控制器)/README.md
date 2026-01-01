# Model–View–Controller (MVC) (模型 - 視圖 - 控制器)

Model–View–Controller (MVC) 是一種經典的軟體架構模式，將應用程式分為三個相互關聯但獨立的元件：Model (模型)、View (視圖) 和 Controller (控制器)。

這種架構模式強調關注點分離，將業務處理、資料呈現和使用者互動分離，使系統更容易理解、測試和維護。

<br />

## 動機

在軟體開發中，常見的問題包括

- 業務處理與使用者介面緊密耦合，難以獨立測試和修改

- 資料呈現與業務處理混合，導致程式碼難以維護

- 使用者互動處理分散在各處，缺乏統一的控制點

- 程式碼重複使用性低，新功能開發困難

MVC 通過三層分離設計，解決這些問題，讓系統具備

- 關注點分離：每個元件都有明確的職責

- 可重用性：Model 和 View 可以獨立重用

- 可測試性：各元件可以獨立進行單元測試

- 可維護性：修改一個元件不會影響其他元件

<br />

## 結構

MVC 將應用程式分為三個核心元件

### 1. Model (模型)

負責管理應用程式的資料和業務處理。

- 封裝資料和相關的業務規則

- 提供資料存取和操作的介面

- 通知 View 資料變更

- 不依賴 View 和 Controller

### 2. View (視圖)

負責資料的呈現和使用者介面。

- 顯示 Model 的資料

- 提供使用者互動介面

- 監聽 Model 的變更並更新顯示

- 不包含業務處理

### 3. Controller (控制器)

負責處理使用者輸入和協調 Model 與 View。

- 接收使用者輸入

- 調用 Model 的方法處理業務

- 選擇適當的 View 進行回應

- 協調 Model 和 View 之間的互動

以下是 MVC 的架構圖

```text
┌─────────────────┐    User Input     ┌─────────────────┐
│                 │  ──────────────►  │                 │
│      View       │    Update View    │   Controller    │
│                 │  ◄──────────────  │                 │
└─────────────────┘                   └─────────────────┘
         │                                     │
         │ Listen for Data Changes             │ Call Business Logic
         │                                     │
         ▼                                     ▼
┌──────────────────────────────────────────────────────┐
│                         Model                        │
└──────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 關注點分離 (Separation of Concerns)

每個元件都有明確且單一的職責，不應該承擔其他元件的責任。

### 鬆散耦合 (Loose Coupling)

元件之間的依賴關係應該最小化，通過介面或事件進行通訊。

### 高內聚 (High Cohesion)

每個元件內部的元素應該緊密相關，共同完成特定的功能。

<br />

## 實現方式

### Java Spring MVC 實現範例

以部落格系統的文章管理為例

- Model (模型)

    ```java
    /** 文章實體 */
    @Entity
    @Table(name = "articles")
    public class Article {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(nullable = false)
        private String title;

        @Column(columnDefinition = "TEXT")
        private String content;

        @Column(name = "author_id")
        private Long authorId;

        @CreationTimestamp
        private LocalDateTime createdAt;

        @UpdateTimestamp
        private LocalDateTime updatedAt;

        /** 建構子、getter、setter */
        public Article() {}

        public Article(String title, String content, Long authorId) {
            this.title = title;
            this.content = content;
            this.authorId = authorId;
        }

        /** getter 和 setter 方法 */
        public Long getId() { return id; }
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
    }

    /** 文章服務 */
    @Service
    public class ArticleService {
        private final ArticleRepository articleRepository;

        public ArticleService(ArticleRepository articleRepository) {
            this.articleRepository = articleRepository;
        }

        public List<Article> getAllArticles() {
            return articleRepository.findAll();
        }

        public Article getArticleById(Long id) {
            return articleRepository.findById(id)
                .orElseThrow(() -> new ArticleNotFoundException("文章不存在"));
        }

        public Article createArticle(Article article) {
            validateArticle(article);
            return articleRepository.save(article);
        }

        public Article updateArticle(Long id, Article updatedArticle) {
            Article existingArticle = getArticleById(id);
            existingArticle.setTitle(updatedArticle.getTitle());
            existingArticle.setContent(updatedArticle.getContent());
            return articleRepository.save(existingArticle);
        }

        public void deleteArticle(Long id) {
            Article article = getArticleById(id);
            articleRepository.delete(article);
        }

        private void validateArticle(Article article) {
            if (article.getTitle() == null || article.getTitle().trim().isEmpty()) {
                throw new IllegalArgumentException("文章標題不能為空");
            }
            if (article.getContent() == null || article.getContent().trim().isEmpty()) {
                throw new IllegalArgumentException("文章內容不能為空");
            }
        }
    }
    ```

- Controller (控制器)

    ```java
    /** 文章控制器 */
    @Controller
    @RequestMapping("/articles")
    public class ArticleController {
        private final ArticleService articleService;

        public ArticleController(ArticleService articleService) {
            this.articleService = articleService;
        }

        @GetMapping
        public String listArticles(Model model) {
            List<Article> articles = articleService.getAllArticles();
            model.addAttribute("articles", articles);
            return "articles/list";
        }

        @GetMapping("/{id}")
        public String showArticle(@PathVariable Long id, Model model) {
            Article article = articleService.getArticleById(id);
            model.addAttribute("article", article);
            return "articles/show";
        }

        @GetMapping("/new")
        public String newArticleForm(Model model) {
            model.addAttribute("article", new Article());
            return "articles/form";
        }

        @PostMapping
        public String createArticle(@ModelAttribute Article article, RedirectAttributes redirectAttributes) {
            try {
                Article savedArticle = articleService.createArticle(article);
                redirectAttributes.addFlashAttribute("message", "文章建立成功");
                return "redirect:/articles/" + savedArticle.getId();
            } catch (IllegalArgumentException e) {
                redirectAttributes.addFlashAttribute("error", e.getMessage());
                return "redirect:/articles/new";
            }
        }

        @GetMapping("/{id}/edit")
        public String editArticleForm(@PathVariable Long id, Model model) {
            Article article = articleService.getArticleById(id);
            model.addAttribute("article", article);
            return "articles/form";
        }

        @PutMapping("/{id}")
        public String updateArticle(@PathVariable Long id, @ModelAttribute Article article, RedirectAttributes redirectAttributes) {
            try {
                articleService.updateArticle(id, article);
                redirectAttributes.addFlashAttribute("message", "文章更新成功");
                return "redirect:/articles/" + id;
            } catch (Exception e) {
                redirectAttributes.addFlashAttribute("error", e.getMessage());
                return "redirect:/articles/" + id + "/edit";
            }
        }

        @DeleteMapping("/{id}")
        public String deleteArticle(@PathVariable Long id, RedirectAttributes redirectAttributes) {
            try {
                articleService.deleteArticle(id);
                redirectAttributes.addFlashAttribute("message", "文章刪除成功");
                return "redirect:/articles";
            } catch (Exception e) {
                redirectAttributes.addFlashAttribute("error", e.getMessage());
                return "redirect:/articles";
            }
        }
    }
    ```
- View (視圖)

    ```html
    <!-- articles/list.html -->
    <!DOCTYPE html>
    <html xmlns:th="http://www.thymeleaf.org">
    <head>
        <title>文章列表</title>
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <div class="container">
            <h1>文章列表</h1>

            <div th:if="${message}" class="alert alert-success" th:text="${message}"></div>
            <div th:if="${error}" class="alert alert-error" th:text="${error}"></div>

            <a href="/articles/new" class="btn btn-primary">新增文章</a>

            <div class="articles-grid">
                <div th:each="article : ${articles}" class="article-card">
                    <h3><a th:href="@{/articles/{id}(id=${article.id})}" th:text="${article.title}"></a></h3>
                    <p class="article-meta">
                        發布時間：<span th:text="${#temporals.format(article.createdAt, 'yyyy-MM-dd HH:mm')}"></span>
                    </p>
                    <p class="article-excerpt" th:text="${#strings.abbreviate(article.content, 100)}"></p>
                    <div class="article-actions">
                        <a th:href="@{/articles/{id}/edit(id=${article.id})}" class="btn btn-secondary">編輯</a>
                        <form th:action="@{/articles/{id}(id=${article.id})}" method="post" style="display: inline;">
                            <input type="hidden" name="_method" value="delete">
                            <button type="submit" class="btn btn-danger" onclick="return confirm('確定要刪除這篇文章嗎？')">刪除</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>

    <!-- articles/show.html -->
    <!DOCTYPE html>
    <html xmlns:th="http://www.thymeleaf.org">
    <head>
        <title th:text="${article.title}">文章標題</title>
        <link rel="stylesheet" href="/css/style.css">
    </head>
    <body>
        <div class="container">
            <article class="article-detail">
                <h1 th:text="${article.title}"></h1>
                <div class="article-meta">
                    <p>發布時間：<span th:text="${#temporals.format(article.createdAt, 'yyyy-MM-dd HH:mm')}"></span></p>
                    <p th:if="${article.updatedAt != article.createdAt}">
                        更新時間：<span th:text="${#temporals.format(article.updatedAt, 'yyyy-MM-dd HH:mm')}"></span>
                    </p>
                </div>
                <div class="article-content" th:utext="${article.content}"></div>
                <div class="article-actions">
                    <a href="/articles" class="btn btn-secondary">返回列表</a>
                    <a th:href="@{/articles/{id}/edit(id=${article.id})}" class="btn btn-primary">編輯文章</a>
                </div>
            </article>
        </div>
    </body>
    </html>
    ```

### Express.js (Node.js) 實現範例

- Model (模型)

    ```javascript
    /** 使用者模型 */
    const mongoose = require('mongoose');

    const userSchema = new mongoose.Schema({
      username: {
        type: String,
        required: true,
        unique: true,
        trim: true
      },
      email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true
      },
      password: {
        type: String,
        required: true,
        minlength: 6
      },
      isActive: {
        type: Boolean,
        default: true
      }
    }, {
      timestamps: true
    });

    /** 模型方法 */
    userSchema.methods.toJSON = function() {
      const user = this.toObject();
      delete user.password;
      return user;
    };

    userSchema.statics.findByCredentials = async function(email, password) {
      const user = await this.findOne({ email, isActive: true });
      if (!user) {
        throw new Error('使用者不存在或已停用');
      }

      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        throw new Error('密碼錯誤');
      }

      return user;
    };

    /** 密碼加密中介軟體 */
    userSchema.pre('save', async function(next) {
      if (this.isModified('password')) {
        this.password = await bcrypt.hash(this.password, 10);
      }
      next();
    });

    const User = mongoose.model('User', userSchema);
    module.exports = User;
    ```

- Controller (控制器)

    ```javascript
    /** 使用者控制器 */
    const User = require('../models/User');
    const jwt = require('jsonwebtoken');

    class UserController {
      /** 註冊使用者 */
      static async register(req, res) {
        try {
          const { username, email, password } = req.body;

          /** 驗證輸入 */
          if (!username || !email || !password) {
            return res.status(400).json({ error: '所有欄位都是必填的' });
          }

          /** 建立使用者 */
          const user = new User({ username, email, password });
          await user.save();

          /** 產生 JWT */
          const token = jwt.sign(
            { userId: user._id },
            process.env.JWT_SECRET,
            { expiresIn: '7d' }
          );

          res.status(201).json({
            message: '註冊成功',
            user: user.toJSON(),
            token
          });
        } catch (error) {
          if (error.code === 11000) {
            return res.status(400).json({ error: '使用者名稱或信箱已存在' });
          }
          res.status(400).json({ error: error.message });
        }
      }

      /** 使用者登入 */
      static async login(req, res) {
        try {
          const { email, password } = req.body;

          /** 驗證使用者 */
          const user = await User.findByCredentials(email, password);

          /** 產生 JWT */
          const token = jwt.sign(
            { userId: user._id },
            process.env.JWT_SECRET,
            { expiresIn: '7d' }
          );

          res.json({
            message: '登入成功',
            user: user.toJSON(),
            token
          });
        } catch (error) {
          res.status(401).json({ error: error.message });
        }
      }

      /** 取得使用者資料 */
      static async getProfile(req, res) {
        try {
          const user = await User.findById(req.userId);
          if (!user) {
            return res.status(404).json({ error: '使用者不存在' });
          }

          res.json({ user: user.toJSON() });
        } catch (error) {
          res.status(500).json({ error: error.message });
        }
      }

      /** 更新使用者資料 */
      static async updateProfile(req, res) {
        try {
          const { username, email } = req.body;
          const user = await User.findById(req.userId);

          if (!user) {
            return res.status(404).json({ error: '使用者不存在' });
          }

          /** 更新欄位 */
          if (username) user.username = username;
          if (email) user.email = email;

          await user.save();

          res.json({
            message: '資料更新成功',
            user: user.toJSON()
          });
        } catch (error) {
          if (error.code === 11000) {
            return res.status(400).json({ error: '使用者名稱或信箱已存在' });
          }
          res.status(400).json({ error: error.message });
        }
      }
    }

    module.exports = UserController;
    ```

- View (路由設定)

    ```javascript
    /** 使用者路由 */
    const express = require('express');
    const UserController = require('../controllers/UserController');
    const auth = require('../middleware/auth');

    const router = express.Router();

    /** 公開路由 */
    router.post('/register', UserController.register);
    router.post('/login', UserController.login);

    /** 需要驗證的路由 */
    router.get('/profile', auth, UserController.getProfile);
    router.put('/profile', auth, UserController.updateProfile);

    module.exports = router;

    /** 驗證中介軟體 */
    const jwt = require('jsonwebtoken');

    const auth = async (req, res, next) => {
      try {
        const token = req.header('Authorization')?.replace('Bearer ', '');

        if (!token) {
          return res.status(401).json({ error: '存取被拒絕，需要驗證' });
        }

        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.userId = decoded.userId;
        next();
      } catch (error) {
        res.status(401).json({ error: '無效的驗證令牌' });
      }
    };

    module.exports = auth;
    ```
### React MVC 實現範例

- Model (資料管理)

    ```typescript
    /** 產品模型 */
    export interface Product {
      id: string;
      name: string;
      price: number;
      description: string;
      category: string;
      inStock: boolean;
    }

    /** 產品服務 */
    export class ProductService {
      private static baseUrl = '/api/products';

      static async getAllProducts(): Promise<Product[]> {
        const response = await fetch(this.baseUrl);
        if (!response.ok) {
          throw new Error('取得產品列表失敗');
        }
        return response.json();
      }

      static async getProductById(id: string): Promise<Product> {
        const response = await fetch(`${this.baseUrl}/${id}`);
        if (!response.ok) {
          throw new Error('取得產品詳情失敗');
        }
        return response.json();
      }

      static async createProduct(product: Omit<Product, 'id'>): Promise<Product> {
        const response = await fetch(this.baseUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(product),
        });

        if (!response.ok) {
          throw new Error('建立產品失敗');
        }
        return response.json();
      }

      static async updateProduct(id: string, product: Partial<Product>): Promise<Product> {
        const response = await fetch(`${this.baseUrl}/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(product),
        });

        if (!response.ok) {
          throw new Error('更新產品失敗');
        }
        return response.json();
      }

      static async deleteProduct(id: string): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${id}`, {
          method: 'DELETE',
        });

        if (!response.ok) {
          throw new Error('刪除產品失敗');
        }
      }
    }
    ```

- Controller (狀態管理)

    ```typescript
    /** 產品控制器 Hook */
    import { useState, useEffect, useCallback } from 'react';
    import { ProductService, Product } from '../services/ProductService';

    export const useProductController = () => {
      const [products, setProducts] = useState<Product[]>([]);
      const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);

      /** 載入所有產品 */
      const loadProducts = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
          const productList = await ProductService.getAllProducts();
          setProducts(productList);
        } catch (err) {
          setError(err instanceof Error ? err.message : '載入產品失敗');
        } finally {
          setLoading(false);
        }
      }, []);

      /** 載入單一產品 */
      const loadProduct = useCallback(async (id: string) => {
        setLoading(true);
        setError(null);
        try {
          const product = await ProductService.getProductById(id);
          setSelectedProduct(product);
        } catch (err) {
          setError(err instanceof Error ? err.message : '載入產品失敗');
        } finally {
          setLoading(false);
        }
      }, []);

      /** 建立產品 */
      const createProduct = useCallback(async (productData: Omit<Product, 'id'>) => {
        setLoading(true);
        setError(null);
        try {
          const newProduct = await ProductService.createProduct(productData);
          setProducts(prev => [...prev, newProduct]);
          return newProduct;
        } catch (err) {
          setError(err instanceof Error ? err.message : '建立產品失敗');
          throw err;
        } finally {
          setLoading(false);
        }
      }, []);

      /** 更新產品 */
      const updateProduct = useCallback(async (id: string, productData: Partial<Product>) => {
        setLoading(true);
        setError(null);
        try {
          const updatedProduct = await ProductService.updateProduct(id, productData);
          setProducts(prev => prev.map(p => p.id === id ? updatedProduct : p));
          if (selectedProduct?.id === id) {
            setSelectedProduct(updatedProduct);
          }
          return updatedProduct;
        } catch (err) {
          setError(err instanceof Error ? err.message : '更新產品失敗');
          throw err;
        } finally {
          setLoading(false);
        }
      }, [selectedProduct]);

      /** 刪除產品 */
      const deleteProduct = useCallback(async (id: string) => {
        setLoading(true);
        setError(null);
        try {
          await ProductService.deleteProduct(id);
          setProducts(prev => prev.filter(p => p.id !== id));
          if (selectedProduct?.id === id) {
            setSelectedProduct(null);
          }
        } catch (err) {
          setError(err instanceof Error ? err.message : '刪除產品失敗');
          throw err;
        } finally {
          setLoading(false);
        }
      }, [selectedProduct]);

      /** 清除錯誤 */
      const clearError = useCallback(() => {
        setError(null);
      }, []);

      return {
        products,
        selectedProduct,
        loading,
        error,
        loadProducts,
        loadProduct,
        createProduct,
        updateProduct,
        deleteProduct,
        clearError
      };
    };
    ```

- View (React 元件)

    ```typescript
    /** 產品列表元件 */
    import React, { useEffect } from 'react';
    import { useProductController } from '../hooks/useProductController';
    import { ProductCard } from './ProductCard';
    import { LoadingSpinner } from './LoadingSpinner';
    import { ErrorMessage } from './ErrorMessage';

    export const ProductList: React.FC = () => {
      const {
        products,
        loading,
        error,
        loadProducts,
        deleteProduct,
        clearError
      } = useProductController();

      useEffect(() => {
        loadProducts();
      }, [loadProducts]);

      const handleDeleteProduct = async (id: string) => {
        if (window.confirm('確定要刪除這個產品嗎？')) {
          try {
            await deleteProduct(id);
          } catch (err) {
            // 錯誤已在 controller 中處理
          }
        }
      };

      if (loading) {
        return <LoadingSpinner />;
      }

      return (
        <div className="product-list">
          <div className="product-list-header">
            <h1>產品列表</h1>
            <button className="btn btn-primary">
              新增產品
            </button>
          </div>

          {error && (
            <ErrorMessage 
              message={error} 
              onClose={clearError}
            />
          )}

          <div className="product-grid">
            {products.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                onDelete={() => handleDeleteProduct(product.id)}
              />
            ))}
          </div>

          {products.length === 0 && !loading && (
            <div className="empty-state">
              <p>目前沒有產品</p>
            </div>
          )}
        </div>
      );
    };

    /** 產品卡片元件 */
    interface ProductCardProps {
      product: Product;
      onDelete: () => void;
    }

    export const ProductCard: React.FC<ProductCardProps> = ({ product, onDelete }) => {
      return (
        <div className="product-card">
          <div className="product-card-header">
            <h3>{product.name}</h3>
            <span className={`status ${product.inStock ? 'in-stock' : 'out-of-stock'}`}>
              {product.inStock ? '有庫存' : '缺貨'}
            </span>
          </div>

          <div className="product-card-body">
            <p className="price">NT$ {product.price.toLocaleString()}</p>
            <p className="category">{product.category}</p>
            <p className="description">{product.description}</p>
          </div>

          <div className="product-card-actions">
            <button className="btn btn-secondary">編輯</button>
            <button className="btn btn-danger" onClick={onDelete}>
              刪除
            </button>
          </div>
        </div>
      );
    };
    ```

<br />

## 優點

### 關注點分離

每個元件都有明確的職責，使程式碼更容易理解和維護。

### 可重用性

- Model 可以被多個 View 使用

- View 可以顯示不同的 Model 資料

- Controller 可以處理多種使用者互動

### 可測試性

各元件可以獨立進行單元測試，提高程式碼品質。

### 並行開發

不同開發者可以同時開發不同的元件，提高開發效率。

### 易於維護

修改一個元件通常不會影響其他元件，降低維護成本。

<br />

## 缺點

### 複雜性增加

對於簡單的應用程式來說可能過於複雜。

### 學習曲線

需要開發者理解 MVC 模式的概念和最佳實踐。

### 過度設計風險

可能會為簡單功能創造過於複雜的結構。

### 元件間通訊

需要設計良好的通訊機制來協調各元件。

### 效能考量

在某些情況下，分層結構可能會影響效能。

<br />

## 適用場景

### 適合使用

- Web 應用程式：需要處理使用者互動和資料呈現

- 桌面應用程式：有複雜的使用者介面

- 企業級應用：需要長期維護和擴展

- 團隊開發：多人協作的專案

- 資料驅動應用：需要頻繁的資料操作

### 不適合使用

- 簡單腳本：只有基本功能的小程式

- 靜態網站：沒有複雜互動的網站

- 原型開發：快速驗證想法的專案

- 即時系統：對效能要求極高的系統

<br />

## MVC 變體

### MVP (Model-View-Presenter)

- Presenter 取代 Controller

- View 更被動，所有處理都通過 Presenter

- 更容易進行單元測試

### MVVM (Model-View-ViewModel)

- ViewModel 提供資料綁定

- View 和 ViewModel 之間有雙向綁定

- 常用於 WPF、Angular 等框架

### Component-Based MVC

- 將 MVC 應用到元件層級

- 每個元件都有自己的 Model、View、Controller

- 常見於現代前端框架

<br />

## 實施建議

### 明確職責分工

確保每個元件都有明確且單一的職責，避免職責重疊。

### 設計良好的介面

定義清晰的介面來協調各元件之間的互動。

### 避免緊密耦合

使用依賴注入或觀察者模式來降低元件間的耦合度。

### 適度使用

根據專案複雜度決定是否需要完整的 MVC 架構。

### 團隊培訓

確保團隊成員理解 MVC 模式的概念和最佳實踐。

<br />

## 總結

MVC 是一個經過時間考驗的架構模式，特別適合需要處理使用者互動和資料呈現的應用程式。雖然會增加一定的複雜性，但帶來的關注點分離、可重用性和可維護性優勢，使其成為許多 Web 框架和應用程式的基礎架構。

關鍵在於根據專案需求適當應用 MVC 模式，避免過度設計，同時確保團隊成員理解其核心概念。隨著前端技術的發展，MVC 也演化出許多變體，開發者應該選擇最適合專案需求的架構模式。
