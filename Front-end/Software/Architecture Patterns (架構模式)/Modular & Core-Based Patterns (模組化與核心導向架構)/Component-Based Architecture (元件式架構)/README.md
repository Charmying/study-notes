# Component-Based Architecture (元件式架構)

Component-Based Architecture (元件式架構) 是一種軟體設計方法，將系統分解為獨立、可重用的元件，每個元件封裝特定的功能和狀態。

這種架構強調模組化設計，通過定義清晰的介面和職責分離，使系統更容易開發、測試、維護和擴展。

<br />

## 動機

在軟體開發中，常見的問題包括

- 程式碼重複，相同功能在多處實現

- 緊密耦合，修改一個部分影響其他部分

- 難以測試，功能混雜在一起無法獨立驗證

- 維護困難，程式碼結構混亂難以理解

Component-Based Architecture 通過元件化設計，解決這些問題，讓系統具備

- 可重用性：元件可以在不同場景中重複使用

- 可維護性：每個元件職責單一，易於理解和修改

- 可測試性：元件可以獨立測試

- 可擴展性：新功能可以通過組合現有元件實現

<br />

## 結構

Component-Based Architecture 將系統組織為層次化的元件結構

### 1. 原子元件 (Atomic Components)

最小的功能單位，不可再分解。

- 單一職責，功能明確

- 無外部依賴

- 高度可重用

### 2. 分子元件 (Molecular Components)

由多個原子元件組合而成。

- 實現特定的業務功能

- 管理內部狀態

- 定義元件間的互動

### 3. 有機體元件 (Organism Components)

複雜的功能模組，包含多個分子元件。

- 實現完整的功能區塊

- 處理複雜的業務規則

- 協調子元件的行為

### 4. 模板元件 (Template Components)

定義頁面或應用程式的整體結構。

- 佈局和導航

- 全域狀態管理

- 元件組合和配置

以下是 Component-Based Architecture 的層次圖

```text
┌─────────────────────────────────────────────────────┐
│                     Templates                       │
│  ┌───────────────────────────────────────────────┐  │
│  │                  Organisms                    │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │               Molecules                 │  │  │
│  │  │  ┌───────────────────────────────────┐  │  │  │
│  │  │  │              Atoms                │  │  │  │
│  │  │  └───────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 單一職責原則 (Single Responsibility Principle)

每個元件只負責一個特定的功能或職責。

### 開放封閉原則 (Open/Closed Principle)

元件對擴展開放，對修改封閉。

### 介面隔離原則 (Interface Segregation Principle)

元件只依賴需要的介面，不依賴不需要的功能。

### 依賴反轉原則 (Dependency Inversion Principle)

高層元件不依賴低層元件，兩者都依賴抽象。

<br />

## 實現方式

### React 實現範例

以電商網站的產品展示為例

- 原子元件 (Atomic Components)

    ```typescript
    /** 按鈕元件 */
    interface ButtonProps {
      children: React.ReactNode;
      variant?: 'primary' | 'secondary' | 'danger';
      size?: 'small' | 'medium' | 'large';
      disabled?: boolean;
      onClick?: () => void;
    }

    export const Button: React.FC<ButtonProps> = ({
      children,
      variant = 'primary',
      size = 'medium',
      disabled = false,
      onClick
    }) => {
      const className = `btn btn--${variant} btn--${size} ${disabled ? 'btn--disabled' : ''}`;

      return (
        <button 
          className={className} 
          disabled={disabled} 
          onClick={onClick}
        >
          {children}
        </button>
      );
    };

    /** 輸入框元件 */
    interface InputProps {
      type?: 'text' | 'email' | 'password' | 'number';
      placeholder?: string;
      value: string;
      onChange: (value: string) => void;
      error?: string;
    }

    export const Input: React.FC<InputProps> = ({
      type = 'text',
      placeholder,
      value,
      onChange,
      error
    }) => {
      return (
        <div className="input-wrapper">
          <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className={`input ${error ? 'input--error' : ''}`}
          />
          {error && <span className="input__error">{error}</span>}
        </div>
      );
    };
    ```

- 分子元件 (Molecular Components)

    ```typescript
    /** 產品卡片元件 */
    interface Product {
      id: string;
      name: string;
      price: number;
      image: string;
      rating: number;
    }

    interface ProductCardProps {
      product: Product;
      onAddToCart: (productId: string) => void;
    }

    export const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
      const handleAddToCart = () => {
        onAddToCart(product.id);
      };

      return (
        <div className="product-card">
          <img src={product.image} alt={product.name} className="product-card__image" />
          <div className="product-card__content">
            <h3 className="product-card__name">{product.name}</h3>
            <div className="product-card__rating">
              <StarRating rating={product.rating} />
            </div>
            <div className="product-card__price">${product.price}</div>
            <Button onClick={handleAddToCart}>加入購物車</Button>
          </div>
        </div>
      );
    };

    /** 搜尋表單元件 */
    interface SearchFormProps {
      onSearch: (query: string) => void;
    }

    export const SearchForm: React.FC<SearchFormProps> = ({ onSearch }) => {
      const [query, setQuery] = useState('');

      const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSearch(query);
      };

      return (
        <form onSubmit={handleSubmit} className="search-form">
          <Input
            placeholder="搜尋產品..."
            value={query}
            onChange={setQuery}
          />
          <Button type="submit">搜尋</Button>
        </form>
      );
    };
    ```

- 有機體元件 (Organism Components)

    ```typescript
    /** 產品列表元件 */
    interface ProductListProps {
      products: Product[];
      loading: boolean;
      onAddToCart: (productId: string) => void;
    }

    export const ProductList: React.FC<ProductListProps> = ({
      products,
      loading,
      onAddToCart
    }) => {
      if (loading) {
        return <div className="product-list__loading">載入中...</div>;
      }

      if (products.length === 0) {
        return <div className="product-list__empty">沒有找到產品</div>;
      }

      return (
        <div className="product-list">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={onAddToCart}
            />
          ))}
        </div>
      );
    };

    /** 購物車元件 */
    interface CartItem {
      product: Product;
      quantity: number;
    }

    interface ShoppingCartProps {
      items: CartItem[];
      onUpdateQuantity: (productId: string, quantity: number) => void;
      onRemoveItem: (productId: string) => void;
    }

    export const ShoppingCart: React.FC<ShoppingCartProps> = ({
      items,
      onUpdateQuantity,
      onRemoveItem
    }) => {
      const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

      return (
        <div className="shopping-cart">
          <h2>購物車</h2>
          {items.length === 0 ? (
            <p>購物車是空的</p>
          ) : (
            <>
              <div className="cart-items">
                {items.map((item) => (
                  <CartItem
                    key={item.product.id}
                    item={item}
                    onUpdateQuantity={onUpdateQuantity}
                    onRemove={onRemoveItem}
                  />
                ))}
              </div>
              <div className="cart-total">
                <strong>總計: ${total}</strong>
              </div>
              <Button size="large">結帳</Button>
            </>
          )}
        </div>
      );
    };
    ```

- 模板元件 (Template Components)

    ```typescript
    /** 電商頁面模板 */
    export const EcommercePage: React.FC = () => {
      const [products, setProducts] = useState<Product[]>([]);
      const [cartItems, setCartItems] = useState<CartItem[]>([]);
      const [loading, setLoading] = useState(false);
      const [searchQuery, setSearchQuery] = useState('');

      const handleSearch = async (query: string) => {
        setLoading(true);
        setSearchQuery(query);
        try {
          const results = await productService.search(query);
          setProducts(results);
        } catch (error) {
          console.error('搜尋失敗:', error);
        } finally {
          setLoading(false);
        }
      };

      const handleAddToCart = (productId: string) => {
        const product = products.find(p => p.id === productId);
        if (!product) return;

        setCartItems(prev => {
          const existingItem = prev.find(item => item.product.id === productId);
          if (existingItem) {
            return prev.map(item =>
              item.product.id === productId
                ? { ...item, quantity: item.quantity + 1 }
                : item
            );
          }
          return [...prev, { product, quantity: 1 }];
        });
      };

      const handleUpdateQuantity = (productId: string, quantity: number) => {
        if (quantity <= 0) {
          handleRemoveItem(productId);
          return;
        }

        setCartItems(prev =>
          prev.map(item =>
            item.product.id === productId
              ? { ...item, quantity }
              : item
          )
        );
      };

      const handleRemoveItem = (productId: string) => {
        setCartItems(prev => prev.filter(item => item.product.id !== productId));
      };

      return (
        <div className="ecommerce-page">
          <header className="page-header">
            <h1>線上商店</h1>
            <SearchForm onSearch={handleSearch} />
          </header>

          <main className="page-content">
            <div className="content-grid">
              <section className="products-section">
                <ProductList
                  products={products}
                  loading={loading}
                  onAddToCart={handleAddToCart}
                />
              </section>

              <aside className="cart-section">
                <ShoppingCart
                  items={cartItems}
                  onUpdateQuantity={handleUpdateQuantity}
                  onRemoveItem={handleRemoveItem}
                />
              </aside>
            </div>
          </main>
        </div>
      );
    };
    ```

### Vue.js 實現範例

- 原子元件

    ```typescript
    <!-- BaseButton.vue -->
    <template>
      <button 
        :class="buttonClasses" 
        :disabled="disabled" 
        @click="handleClick"
      >
        <slot />
      </button>
    </template>

    <script setup lang="ts">
    interface Props {
      variant?: 'primary' | 'secondary' | 'danger';
      size?: 'small' | 'medium' | 'large';
      disabled?: boolean;
    }

    const props = withDefaults(defineProps<Props>(), {
      variant: 'primary',
      size: 'medium',
      disabled: false
    });

    const emit = defineEmits<{
      click: [];
    }>();

    const buttonClasses = computed(() => [
      'btn',
      `btn--${props.variant}`,
      `btn--${props.size}`,
      { 'btn--disabled': props.disabled }
    ]);

    const handleClick = () => {
      if (!props.disabled) {
        emit('click');
      }
    };
    </script>
    ```

- 分子元件

    ```typescript
    <!-- ProductCard.vue -->
    <template>
      <div class="product-card">
        <img :src="product.image" :alt="product.name" class="product-card__image" />
        <div class="product-card__content">
          <h3 class="product-card__name">{{ product.name }}</h3>
          <StarRating :rating="product.rating" />
          <div class="product-card__price">${{ product.price }}</div>
          <BaseButton @click="handleAddToCart">加入購物車</BaseButton>
        </div>
      </div>
    </template>

    <script setup lang="ts">
    import BaseButton from './BaseButton.vue';
    import StarRating from './StarRating.vue';

    interface Product {
      id: string;
      name: string;
      price: number;
      image: string;
      rating: number;
    }

    interface Props {
      product: Product;
    }

    const props = defineProps<Props>();

    const emit = defineEmits<{
      addToCart: [productId: string];
    }>();

    const handleAddToCart = () => {
      emit('addToCart', props.product.id);
    };
    </script>
    ```

### Angular 實現範例

- 原子元件

    ```typescript
    /** button.component.ts */
    import { Component, Input, Output, EventEmitter } from '@angular/core';

    @Component({
      selector: 'app-button',
      template: `
        <button 
          [class]="buttonClasses" 
          [disabled]="disabled" 
          (click)="handleClick()"
        >
          <ng-content></ng-content>
        </button>
      `,
      styleUrls: ['./button.component.scss']
    })
    export class ButtonComponent {
      @Input() variant: 'primary' | 'secondary' | 'danger' = 'primary';
      @Input() size: 'small' | 'medium' | 'large' = 'medium';
      @Input() disabled: boolean = false;
      @Output() clicked = new EventEmitter<void>();

      get buttonClasses(): string {
        return [
          'btn',
          `btn--${this.variant}`,
          `btn--${this.size}`,
          this.disabled ? 'btn--disabled' : ''
        ].join(' ');
      }

      handleClick(): void {
        if (!this.disabled) {
          this.clicked.emit();
        }
      }
    }
    ```

- 分子元件

    ```typescript
    /** product-card.component.ts */
    import { Component, Input, Output, EventEmitter } from '@angular/core';

    interface Product {
      id: string;
      name: string;
      price: number;
      image: string;
      rating: number;
    }

    @Component({
      selector: 'app-product-card',
      template: `
        <div class="product-card">
          <img [src]="product.image" [alt]="product.name" class="product-card__image" />
          <div class="product-card__content">
            <h3 class="product-card__name">{{ product.name }}</h3>
            <app-star-rating [rating]="product.rating"></app-star-rating>
            <div class="product-card__price">\${{ product.price }}</div>
            <app-button (clicked)="handleAddToCart()">加入購物車</app-button>
          </div>
        </div>
      `,
      styleUrls: ['./product-card.component.scss']
    })
    export class ProductCardComponent {
      @Input() product!: Product;
      @Output() addToCart = new EventEmitter<string>();

      handleAddToCart(): void {
        this.addToCart.emit(this.product.id);
      }
    }
    ```

### Java Spring 實現範例

- 服務元件

    ```java
    /** 產品服務元件 */
    @Service
    public class ProductService {
        private final ProductRepository productRepository;
        private final CacheService cacheService;

        public ProductService(ProductRepository productRepository, CacheService cacheService) {
            this.productRepository = productRepository;
            this.cacheService = cacheService;
        }

        public List<Product> searchProducts(String query) {
            String cacheKey = "search:" + query;
            List<Product> cachedResults = cacheService.get(cacheKey, List.class);

            if (cachedResults != null) {
                return cachedResults;
            }

            List<Product> products = productRepository.findByNameContaining(query);
            cacheService.put(cacheKey, products, Duration.ofMinutes(10));

            return products;
        }

        public Product getProductById(String id) {
            return productRepository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException("產品不存在: " + id));
        }
    }

    /** 購物車服務元件 */
    @Service
    public class CartService {
        private final CartRepository cartRepository;
        private final ProductService productService;

        public CartService(CartRepository cartRepository, ProductService productService) {
            this.cartRepository = cartRepository;
            this.productService = productService;
        }

        public Cart addToCart(String userId, String productId, int quantity) {
            Product product = productService.getProductById(productId);
            Cart cart = getOrCreateCart(userId);

            cart.addItem(product, quantity);
            return cartRepository.save(cart);
        }

        private Cart getOrCreateCart(String userId) {
            return cartRepository.findByUserId(userId)
                .orElse(new Cart(userId));
        }
    }
    ```

- 控制器元件

    ```java
    /** 產品控制器元件 */
    @RestController
    @RequestMapping("/api/products")
    public class ProductController {
        private final ProductService productService;

        public ProductController(ProductService productService) {
            this.productService = productService;
        }

        @GetMapping("/search")
        public ResponseEntity<List<ProductDto>> searchProducts(
            @RequestParam String query
        ) {
            List<Product> products = productService.searchProducts(query);
            List<ProductDto> productDtos = products.stream()
                .map(ProductDto::from)
                .collect(Collectors.toList());

            return ResponseEntity.ok(productDtos);
        }

        @GetMapping("/{id}")
        public ResponseEntity<ProductDto> getProduct(@PathVariable String id) {
            Product product = productService.getProductById(id);
            return ResponseEntity.ok(ProductDto.from(product));
        }
    }

    /** 購物車控制器元件 */
    @RestController
    @RequestMapping("/api/cart")
    public class CartController {
        private final CartService cartService;

        public CartController(CartService cartService) {
            this.cartService = cartService;
        }

        @PostMapping("/items")
        public ResponseEntity<CartDto> addToCart(
            @RequestHeader("User-Id") String userId,
            @RequestBody AddToCartRequest request
        ) {
            Cart cart = cartService.addToCart(userId, request.getProductId(), request.getQuantity());
            return ResponseEntity.ok(CartDto.from(cart));
        }
    }
    ```

<br />

## 優點

### 可重用性

元件可以在不同的場景和專案中重複使用，減少重複開發。

### 可維護性

- 職責分離：每個元件職責單一，易於理解

- 獨立修改：修改一個元件不影響其他元件

- 程式碼組織：清晰的結構便於維護

### 可測試性

每個元件可以獨立測試，提高測試覆蓋率和品質。

### 團隊協作

不同團隊成員可以並行開發不同的元件，提高開發效率。

### 可擴展性

新功能可以通過組合現有元件或開發新元件來實現。

<br />

## 缺點

### 初期複雜性

需要前期設計元件架構和介面定義。

### 過度抽象

可能會創造過多的小元件，增加系統複雜性。

### 效能考量

元件間的通訊可能帶來效能開銷。

### 學習成本

團隊需要學習元件設計原則和最佳實務。

<br />

## 適用場景

### 適合使用

- 大型前端應用：需要管理複雜的使用者介面

- 設計系統：需要統一的 UI 元件庫

- 多專案共享：多個專案需要共享相同的元件

- 團隊協作：多個開發者同時開發

- 長期維護：需要長期維護和擴展的專案

### 不適合使用

- 簡單頁面：只有少量靜態內容的頁面

- 原型開發：快速驗證想法的專案

- 一次性專案：不需要重用的短期專案

- 資源限制：開發時間或人力資源有限

<br />

## 實施建議

### 設計原則

建立清晰的元件設計原則和命名規範。

### 元件庫

建立統一的元件庫，提供文件和範例。

### 測試策略

為每個元件建立單元測試和整合測試。

### 版本管理

建立元件版本管理機制，確保向後相容性。

### 文件化

維護完整的元件文件，包括 API 和使用範例。

<br />

## 總結

Component-Based Architecture 提供了一個有效的方法來組織和管理複雜的軟體系統，特別適合需要高度重用性和可維護性的應用程式。

通過將系統分解為獨立的元件，開發團隊可以更有效率協作，同時提高程式碼品質和系統的可擴展性。關鍵在於找到適當的抽象層次，避免過度設計，同時確保元件的職責清晰和介面穩定。
