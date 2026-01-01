# Model–View–Presenter (MVP) (模型 - 視圖 - 展示器)

Model–View–Presenter (MVP) 是一種軟體架構模式，源自於 Model–View–Controller (MVC) 模式的演進。MVP 將應用程式分為三個主要元件：Model (模型)、View (視圖) 和 Presenter (展示器)，目標在於提高程式碼的可測試性、可維護性和關注點分離。

這種架構模式特別適合需要複雜使用者介面互動的應用程式，通過將業務處理與視圖分離，使得程式碼更容易測試和維護。

<br />

## 動機

在傳統的軟體開發中，常見的問題包括

- 使用者介面與業務處理緊密耦合，難以進行單元測試

- 視圖包含過多業務處理，違反單一職責原則

- 程式碼重複使用性低，不同平台需要重寫業務處理

- 團隊協作困難，前端和後端開發者難以並行工作

MVP 模式通過引入 Presenter 作為中介者，解決這些問題，讓系統具備

- 可測試性：Presenter 可以獨立於視圖進行測試

- 關注點分離：每個元件都有明確的職責

- 可重用性：Presenter 可以在不同視圖間重複使用

- 並行開發：前端和後端可以獨立工作

<br />

## 結構

MVP 模式包含三個核心元件

### 1. Model (模型)

負責資料管理和業務規則。

- 封裝應用程式的資料和狀態

- 實現業務規則和資料驗證

- 提供資料存取介面

- 不依賴於視圖或展示器

### 2. View (視圖)

負責使用者介面的顯示和使用者輸入的接收。

- 顯示資料給使用者

- 接收使用者輸入

- 將使用者操作委託給 Presenter

- 不包含業務處理

### 3. Presenter (展示器)

作為 Model 和 View 之間的中介者。

- 處理使用者輸入的業務處理

- 協調 Model 和 View 之間的互動

- 包含展示處理

- 控制視圖的狀態和行為

以下是 MVP 的結構圖

```text
┌────────────────────┐    ┌──────────────────────────┐    ┌────────────────────────┐
│        View        │◄──►│         Presenter        │◄──►│         Model          │
│                    │    │                          │    │                        │
│ - Display Data     │    │ - Handle Business        │    │ - Manage Data          │
│ - Receive Input    │    │ - Coordinate Interaction │    │ - Apply Business Rules │
│ - Delegate Actions │    │ - Format & Present Data  │    │ - Validate Data        │
└────────────────────┘    └──────────────────────────┘    └────────────────────────┘
```

<br />

## 核心原則

### 關注點分離 (Separation of Concerns)

每個元件都有明確且單一的職責，避免職責重疊。

### 依賴反轉 (Dependency Inversion)

Presenter 依賴於 View 的抽象介面，而不是具體實現。

### 被動視圖 (Passive View)

View 保持被動，不包含任何業務處理，所有處理都由 Presenter 負責。

<br />

## 實現方式

### Java & Android 實現範例

以使用者登入功能為例

- Model (模型)

    ```java
    /** 使用者實體 */
    public class User {
        private String username;
        private String email;
        private boolean isActive;

        public User(String username, String email) {
            this.username = username;
            this.email = email;
            this.isActive = true;
        }

        /** Getters and setters */
        public String getUsername() { return username; }
        public String getEmail() { return email; }
        public boolean isActive() { return isActive; }
    }

    /** 認證服務 */
    public interface AuthService {
        User authenticate(String username, String password);
        boolean isValidCredentials(String username, String password);
    }

    public class AuthServiceImpl implements AuthService {
        @Override
        public User authenticate(String username, String password) {
            if (!isValidCredentials(username, password)) {
                throw new AuthenticationException("認證失敗");
            }
            return new User(username, username + "@example.com");
        }

        @Override
        public boolean isValidCredentials(String username, String password) {
            return username != null && !username.isEmpty() && 
                   password != null && password.length() >= 6;
        }
    }
    ```

- View (視圖)

    ```java
    /** 登入視圖介面 */
    public interface LoginView {
        void showLoading();
        void hideLoading();
        void showLoginSuccess(String username);
        void showLoginError(String message);
        void clearInputs();
        String getUsername();
        String getPassword();
    }

    /** Android Activity 實現 */
    public class LoginActivity extends AppCompatActivity implements LoginView {
        private EditText usernameEditText;
        private EditText passwordEditText;
        private Button loginButton;
        private ProgressBar progressBar;
        private LoginPresenter presenter;

        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_login);

            initViews();
            presenter = new LoginPresenter(this, new AuthServiceImpl());
        }

        private void initViews() {
            usernameEditText = findViewById(R.id.username);
            passwordEditText = findViewById(R.id.password);
            loginButton = findViewById(R.id.login_button);
            progressBar = findViewById(R.id.progress_bar);

            loginButton.setOnClickListener(v -> presenter.login());
        }

        @Override
        public void showLoading() {
            progressBar.setVisibility(View.VISIBLE);
            loginButton.setEnabled(false);
        }

        @Override
        public void hideLoading() {
            progressBar.setVisibility(View.GONE);
            loginButton.setEnabled(true);
        }

        @Override
        public void showLoginSuccess(String username) {
            Toast.makeText(this, "歡迎, " + username, Toast.LENGTH_SHORT).show();
            // 導航到主畫面
        }

        @Override
        public void showLoginError(String message) {
            Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
        }

        @Override
        public String getUsername() {
            return usernameEditText.getText().toString();
        }

        @Override
        public String getPassword() {
            return passwordEditText.getText().toString();
        }
    }
    ```

- Presenter (展示器)

    ```java
    /** 登入展示器 */
    public class LoginPresenter {
        private LoginView view;
        private AuthService authService;

        public LoginPresenter(LoginView view, AuthService authService) {
            this.view = view;
            this.authService = authService;
        }

        public void login() {
            String username = view.getUsername();
            String password = view.getPassword();

            if (!validateInputs(username, password)) {
                return;
            }

            view.showLoading();

            /** 模擬非同步操作 */
            new Thread(() -> {
                try {
                    User user = authService.authenticate(username, password);

                    /** 切換回主執行緒更新 UI */
                    new Handler(Looper.getMainLooper()).post(() -> {
                        view.hideLoading();
                        view.showLoginSuccess(user.getUsername());
                        view.clearInputs();
                    });
                } catch (AuthenticationException e) {
                    new Handler(Looper.getMainLooper()).post(() -> {
                        view.hideLoading();
                        view.showLoginError(e.getMessage());
                    });
                }
            }).start();
        }

        private boolean validateInputs(String username, String password) {
            if (username == null || username.trim().isEmpty()) {
                view.showLoginError("請輸入使用者名稱");
                return false;
            }

            if (password == null || password.length() < 6) {
                view.showLoginError("密碼至少需要 6 個字元");
                return false;
            }

            return true;
        }
    }
    ```

### TypeScript & React 實現範例

- Model (模型)

    ```typescript
    /** 產品實體 */
    export interface Product {
      id: string;
      name: string;
      price: number;
      description: string;
      inStock: boolean;
    }

    /** 產品服務 */
    export interface ProductService {
      getProducts(): Promise<Product[]>;
      getProduct(id: string): Promise<Product | null>;
      searchProducts(query: string): Promise<Product[]>;
    }

    export class ProductServiceImpl implements ProductService {
      private products: Product[] = [
        { id: '1', name: '筆記型電腦', price: 25000, description: '高效能筆電', inStock: true },
        { id: '2', name: '滑鼠', price: 800, description: '無線滑鼠', inStock: true },
        { id: '3', name: '鍵盤', price: 1500, description: '機械式鍵盤', inStock: false }
      ];

      async getProducts(): Promise<Product[]> {
        /** 模擬 API 呼叫 */
        return new Promise(resolve => {
          setTimeout(() => resolve([...this.products]), 500);
        });
      }

      async getProduct(id: string): Promise<Product | null> {
        return new Promise(resolve => {
          setTimeout(() => {
            const product = this.products.find(p => p.id === id) || null;
            resolve(product);
          }, 300);
        });
      }

      async searchProducts(query: string): Promise<Product[]> {
        return new Promise(resolve => {
          setTimeout(() => {
            const filtered = this.products.filter(p => 
              p.name.toLowerCase().includes(query.toLowerCase())
            );
            resolve(filtered);
          }, 400);
        });
      }
    }
    ```

- View (視圖)

    ```typescript
    /** 產品列表視圖介面 */
    export interface ProductListView {
      showLoading(): void;
      hideLoading(): void;
      showProducts(products: Product[]): void;
      showError(message: string): void;
      showEmptyState(): void;
      getSearchQuery(): string;
    }

    /** React 元件實現 */
    export const ProductListComponent: React.FC = () => {
      const [products, setProducts] = useState<Product[]>([]);
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);
      const [searchQuery, setSearchQuery] = useState('');
      const [showEmpty, setShowEmpty] = useState(false);

      const presenterRef = useRef<ProductListPresenter | null>(null);

      /** 實現視圖介面 */
      const view: ProductListView = {
        showLoading: () => setLoading(true),
        hideLoading: () => setLoading(false),
        showProducts: (products: Product[]) => {
          setProducts(products);
          setError(null);
          setShowEmpty(false);
        },
        showError: (message: string) => {
          setError(message);
          setShowEmpty(false);
        },
        showEmptyState: () => {
          setProducts([]);
          setError(null);
          setShowEmpty(true);
        },
        getSearchQuery: () => searchQuery
      };

      useEffect(() => {
        presenterRef.current = new ProductListPresenter(view, new ProductServiceImpl());
        presenterRef.current.loadProducts();
      }, []);

      const handleSearch = () => {
        if (presenterRef.current) {
          presenterRef.current.searchProducts();
        }
      };

      const handleRefresh = () => {
        if (presenterRef.current) {
          presenterRef.current.loadProducts();
        }
      };

      return (
        <div className="product-list">
          <div className="search-section">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜尋產品..."
            />
            <button onClick={handleSearch}>搜尋</button>
            <button onClick={handleRefresh}>重新整理</button>
          </div>

          {loading && <div className="loading">載入中...</div>}

          {error && (
            <div className="error">
              錯誤: {error}
            </div>
          )}

          {showEmpty && (
            <div className="empty-state">
              沒有找到產品
            </div>
          )}

          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-card">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <p className="price">NT$ {product.price}</p>
                <p className={`stock ${product.inStock ? 'in-stock' : 'out-of-stock'}`}>
                  {product.inStock ? '有庫存' : '缺貨'}
                </p>
              </div>
            ))}
          </div>
        </div>
      );
    };
    ```

- Presenter (展示器)

    ```typescript
    /** 產品列表展示器 */
    export class ProductListPresenter {
      constructor(
        private view: ProductListView,
        private productService: ProductService
      ) {}

      async loadProducts(): Promise<void> {
        try {
          this.view.showLoading();
          const products = await this.productService.getProducts();

          if (products.length === 0) {
            this.view.showEmptyState();
          } else {
            this.view.showProducts(products);
          }
        } catch (error) {
          this.view.showError('載入產品失敗');
        } finally {
          this.view.hideLoading();
        }
      }

      async searchProducts(): Promise<void> {
        const query = this.view.getSearchQuery().trim();

        if (!query) {
          await this.loadProducts();
          return;
        }

        try {
          this.view.showLoading();
          const products = await this.productService.searchProducts(query);

          if (products.length === 0) {
            this.view.showEmptyState();
          } else {
            this.view.showProducts(products);
          }
        } catch (error) {
          this.view.showError('搜尋產品失敗');
        } finally {
          this.view.hideLoading();
        }
      }
    }
    ```

### C# & WPF 實現範例

- Model (模型)

    ```csharp
    /** 客戶實體 */
    public class Customer
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        public DateTime CreatedAt { get; set; }
        public bool IsActive { get; set; }

        public Customer(string name, string email)
        {
            Name = name;
            Email = email;
            CreatedAt = DateTime.Now;
            IsActive = true;
        }
    }

    /** 客戶服務 */
    public interface ICustomerService
    {
        Task<List<Customer>> GetCustomersAsync();
        Task<Customer> CreateCustomerAsync(string name, string email);
        Task<bool> DeleteCustomerAsync(int id);
    }

    public class CustomerService : ICustomerService
    {
        private List<Customer> customers = new List<Customer>();
        private int nextId = 1;

        public async Task<List<Customer>> GetCustomersAsync()
        {
            /** 模擬非同步操作 */
            await Task.Delay(500);
            return customers.ToList();
        }

        public async Task<Customer> CreateCustomerAsync(string name, string email)
        {
            await Task.Delay(300);

            var customer = new Customer(name, email) { Id = nextId++ };
            customers.Add(customer);
            return customer;
        }

        public async Task<bool> DeleteCustomerAsync(int id)
        {
            await Task.Delay(200);

            var customer = customers.FirstOrDefault(c => c.Id == id);
            if (customer != null)
            {
                customers.Remove(customer);
                return true;
            }
            return false;
        }
    }
    ```

- View (視圖)

    ```csharp
    /** 客戶管理視圖介面 */
    public interface ICustomerView
    {
        void ShowLoading();
        void HideLoading();
        void ShowCustomers(List<Customer> customers);
        void ShowError(string message);
        void ShowSuccess(string message);
        void ClearInputs();
        string GetCustomerName();
        string GetCustomerEmail();
        event EventHandler LoadCustomers;
        event EventHandler CreateCustomer;
        event EventHandler<int> DeleteCustomer;
    }

    /** WPF 視窗實現 */
    public partial class CustomerWindow : Window, ICustomerView
    {
        private CustomerPresenter presenter;

        public CustomerWindow()
        {
            InitializeComponent();
            presenter = new CustomerPresenter(this, new CustomerService());
        }

        public event EventHandler LoadCustomers;
        public event EventHandler CreateCustomer;
        public event EventHandler<int> DeleteCustomer;

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            LoadCustomers?.Invoke(this, EventArgs.Empty);
        }

        private void CreateButton_Click(object sender, RoutedEventArgs e)
        {
            CreateCustomer?.Invoke(this, EventArgs.Empty);
        }

        private void DeleteButton_Click(object sender, RoutedEventArgs e)
        {
            if (CustomersDataGrid.SelectedItem is Customer customer)
            {
                DeleteCustomer?.Invoke(this, customer.Id);
            }
        }

        public void ShowLoading()
        {
            LoadingProgressBar.Visibility = Visibility.Visible;
            CreateButton.IsEnabled = false;
        }

        public void HideLoading()
        {
            LoadingProgressBar.Visibility = Visibility.Collapsed;
            CreateButton.IsEnabled = true;
        }

        public void ShowCustomers(List<Customer> customers)
        {
            CustomersDataGrid.ItemsSource = customers;
        }

        public void ShowError(string message)
        {
            MessageBox.Show(message, "錯誤", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        public void ShowSuccess(string message)
        {
            MessageBox.Show(message, "成功", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        public void ClearInputs()
        {
            NameTextBox.Clear();
            EmailTextBox.Clear();
        }

        public string GetCustomerName() => NameTextBox.Text;
        public string GetCustomerEmail() => EmailTextBox.Text;
    }
    ```

- Presenter (展示器)

    ```csharp
    /** 客戶展示器 */
    public class CustomerPresenter
    {
        private readonly ICustomerView view;
        private readonly ICustomerService customerService;

        public CustomerPresenter(ICustomerView view, ICustomerService customerService)
        {
            this.view = view;
            this.customerService = customerService;

            /** 訂閱視圖事件 */
            view.LoadCustomers += OnLoadCustomers;
            view.CreateCustomer += OnCreateCustomer;
            view.DeleteCustomer += OnDeleteCustomer;
        }

        private async void OnLoadCustomers(object sender, EventArgs e)
        {
            try
            {
                view.ShowLoading();
                var customers = await customerService.GetCustomersAsync();
                view.ShowCustomers(customers);
            }
            catch (Exception ex)
            {
                view.ShowError($"載入客戶失敗: {ex.Message}");
            }
            finally
            {
                view.HideLoading();
            }
        }

        private async void OnCreateCustomer(object sender, EventArgs e)
        {
            var name = view.GetCustomerName();
            var email = view.GetCustomerEmail();

            if (!ValidateCustomerInput(name, email))
                return;

            try
            {
                view.ShowLoading();
                await customerService.CreateCustomerAsync(name, email);
                view.ShowSuccess("客戶建立成功");
                view.ClearInputs();

                /** 重新載入客戶列表 */
                var customers = await customerService.GetCustomersAsync();
                view.ShowCustomers(customers);
            }
            catch (Exception ex)
            {
                view.ShowError($"建立客戶失敗: {ex.Message}");
            }
            finally
            {
                view.HideLoading();
            }
        }

        private async void OnDeleteCustomer(object sender, int customerId)
        {
            try
            {
                view.ShowLoading();
                var success = await customerService.DeleteCustomerAsync(customerId);

                if (success)
                {
                    view.ShowSuccess("客戶刪除成功");
                    /** 重新載入客戶列表 */
                    var customers = await customerService.GetCustomersAsync();
                    view.ShowCustomers(customers);
                }
                else
                {
                    view.ShowError("找不到指定的客戶");
                }
            }
            catch (Exception ex)
            {
                view.ShowError($"刪除客戶失敗: {ex.Message}");
            }
            finally
            {
                view.HideLoading();
            }
        }

        private bool ValidateCustomerInput(string name, string email)
        {
            if (string.IsNullOrWhiteSpace(name))
            {
                view.ShowError("請輸入客戶姓名");
                return false;
            }

            if (string.IsNullOrWhiteSpace(email) || !IsValidEmail(email))
            {
                view.ShowError("請輸入有效的電子郵件地址");
                return false;
            }

            return true;
        }

        private bool IsValidEmail(string email)
        {
            try
            {
                var addr = new System.Net.Mail.MailAddress(email);
                return addr.Address == email;
            }
            catch
            {
                return false;
            }
        }
    }
    ```

<br />

## 優點

### 可測試性

Presenter 可以獨立於視圖進行單元測試，提高程式碼品質。

### 關注點分離

每個元件都有明確的職責，降低程式碼複雜度。

### 可重用性

Presenter 可以在不同的視圖實現間重複使用。

### 並行開發

前端和後端開發者可以獨立工作，提高開發效率。

### 維護性

清晰的架構使得程式碼更容易理解和維護。

<br />

## 缺點

### 複雜性增加

相比簡單的架構，MVP 增加了程式碼的複雜性。

### 學習成本

開發團隊需要理解 MVP 模式的概念和實作方式。

### 程式碼量增加

需要定義介面和實現多個類別，增加程式碼量。

### 過度設計風險

對於簡單的應用程式可能造成過度設計。

<br />

## 適用場景

### 適合使用

- 複雜的使用者介面：需要複雜互動和狀態管理

- 需要高可測試性：對程式碼品質要求高的專案

- 多平台應用：需要在不同平台間共享業務處理

- 團隊協作：前端和後端需要並行開發

- 長期維護：需要長期維護和擴展的專案

### 不適合使用

- 簡單的 CRUD 介面：只有基本的資料操作

- 原型開發：快速驗證概念的專案

- 小型專案：開發資源有限的專案

- 靜態內容：主要顯示靜態內容的應用

<br />

## 與其他模式的比較

### MVP vs MVC

- MVP：Presenter 處理所有使用者輸入，View 完全被動

- MVC：Controller 處理輸入，但 View 可以直接觀察 Model

### MVP vs MVVM

- MVP：Presenter 明確控制 View 的狀態

- MVVM：ViewModel 通過資料繫結自動同步 View

<br />

## 實施建議

### 定義清晰的介面

為 View 定義清晰的介面，避免 Presenter 直接依賴具體的 View 實現。

### 保持 View 的被動性

確保 View 不包含任何業務處理，所有處理都委託給 Presenter。

### 單元測試

為 Presenter 編寫完整的單元測試，使用 Mock 物件模擬 View 和 Model。

### 避免過度複雜

不要為了使用 MVP 而過度設計，根據實際需求選擇合適的複雜度。

### 程式碼組織

將 Model、View、Presenter 分別組織在不同的套件或資料夾中。

<br />

## 總結

MVP 模式提供了一個有效的方式來組織使用者介面程式碼，特別適合需要高可測試性和複雜互動的應用程式。通過將展示處理從視圖中分離出來，MVP 使得程式碼更容易測試、維護和重複使用。

關鍵在於根據專案的實際需求來決定是否採用 MVP 模式。對於簡單的應用程式，傳統的架構可能更合適；但對於複雜的使用者介面和需要高品質程式碼的專案，MVP 模式能夠帶來顯著的價值。
