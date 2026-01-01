# Client–Server Architecture (客戶端 - 伺服器架構)

Client–Server Architecture (客戶端 - 伺服器架構) 是一種分散式系統架構模式，將應用程式分為兩個主要部分：客戶端 (Client) 負責使用者介面和使用者互動，伺服器端 (Server) 負責資料處理、業務規則和資源管理。

這種架構模式通過網路連接實現客戶端與伺服器端的通訊，是現代網路應用程式和企業系統的基礎架構之一。

<br />

## 動機

在軟體系統發展過程中，單機應用程式面臨許多挑戰

- 資源共享困難，多個使用者無法同時存取相同資料

- 資料一致性問題，各個客戶端可能擁有不同版本的資料

- 擴展性限制，單機效能無法滿足大量使用者需求

- 維護成本高，每個客戶端都需要單獨更新和維護

Client-Server Architecture 通過分離關注點解決這些問題，提供

- 集中式資料管理：統一的資料存取和管理

- 資源共享：多個客戶端可以共享伺服器資源

- 可擴展性：可以根據需求擴展伺服器容量

- 易於維護：集中式的業務規則和資料管理

<br />

## 結構

Client-Server Architecture 主要由兩個核心元件組成

### 1. Client (客戶端)

負責使用者介面和使用者互動的元件。

- 處理使用者輸入和顯示結果

- 發送請求到伺服器端

- 處理伺服器回應

- 提供使用者體驗

### 2. Server (伺服器端)

負責業務處理和資源管理的元件。

- 處理客戶端請求

- 執行業務規則

- 管理資料存取

- 提供服務和資源

### 3. Network (網路)

連接客戶端和伺服器端的通訊媒介。

- 傳輸請求和回應

- 處理網路協定

- 管理連接狀態

以下是 Client-Server Architecture 的結構圖

```text
┌──────────────────┐    Network   ┌──────────────────┐
│     Client       │ ◄──────────► │     Server       │
│                  │              │                  │
│ • User Interface │              │ • Business Logic │
│ • Presentation   │              │ • Data Access    │
│ • User Input     │              │ • Resource Mgmt  │
│ • Display        │              │ • Services       │
└──────────────────┘              └──────────────────┘
         │                                 │
         ▼                                 ▼
┌───────────────────┐             ┌─────────────────┐
│   Local Storage   │             │    Database     │
│   • Cache         │             │  • Persistent   │
│   • Temp Data     │             │  • Shared Data  │
└───────────────────┘             └─────────────────┘
```

<br />

## 核心原則

### 關注點分離 (Separation of Concerns)

客戶端專注於使用者介面，伺服器端專注於業務處理。

### 集中式管理 (Centralized Management)

資料和業務規則集中在伺服器端管理。

### 無狀態通訊 (Stateless Communication)

每個請求都包含完整的資訊，伺服器不需要記住客戶端狀態。

<br />

## 實現方式

### Web 應用程式實現範例

以電商網站為例，展示前後端分離的實現

- 前端 (React + TypeScript)

    ```typescript
    /** 產品服務 */
    export class ProductService {
      private readonly baseUrl = '/api/products';

      async getProducts(): Promise<Product[]> {
        const response = await fetch(this.baseUrl);
        if (!response.ok) {
          throw new Error('獲取產品列表失敗');
        }
        return response.json();
      }

      async getProduct(id: string): Promise<Product> {
        const response = await fetch(`${this.baseUrl}/${id}`);
        if (!response.ok) {
          throw new Error('獲取產品詳情失敗');
        }
        return response.json();
      }

      async createProduct(product: CreateProductRequest): Promise<Product> {
        const response = await fetch(this.baseUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(product)
        });
        if (!response.ok) {
          throw new Error('建立產品失敗');
        }
        return response.json();
      }
    }

    /** React 元件 */
    export const ProductList: React.FC = () => {
      const [products, setProducts] = useState<Product[]>([]);
      const [loading, setLoading] = useState(true);
      const productService = new ProductService();

      useEffect(() => {
        loadProducts();
      }, []);

      const loadProducts = async () => {
        try {
          setLoading(true);
          const productList = await productService.getProducts();
          setProducts(productList);
        } catch (error) {
          console.error('載入產品失敗:', error);
        } finally {
          setLoading(false);
        }
      };

      if (loading) {
        return <div>載入中...</div>;
      }

      return (
        <div className="product-list">
          <h2>產品列表</h2>
          <div className="products">
            {products.map(product => (
              <div key={product.id} className="product-card">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <span className="price">${product.price}</span>
              </div>
            ))}
          </div>
        </div>
      );
    };
    ```

- 後端 (Node.js Express)

    ```javascript
    /** 產品控制器 */
    class ProductController {
      constructor(productService) {
        this.productService = productService;
      }

      async getProducts(req, res) {
        try {
          const products = await this.productService.getAllProducts();
          res.json(products);
        } catch (error) {
          res.status(500).json({ error: '獲取產品列表失敗' });
        }
      }

      async getProduct(req, res) {
        try {
          const { id } = req.params;
          const product = await this.productService.getProductById(id);
          if (!product) {
            return res.status(404).json({ error: '產品不存在' });
          }
          res.json(product);
        } catch (error) {
          res.status(500).json({ error: '獲取產品詳情失敗' });
        }
      }

      async createProduct(req, res) {
        try {
          const productData = req.body;
          const product = await this.productService.createProduct(productData);
          res.status(201).json(product);
        } catch (error) {
          res.status(400).json({ error: '建立產品失敗' });
        }
      }
    }

    /** 產品服務 */
    class ProductService {
      constructor(productRepository) {
        this.productRepository = productRepository;
      }

      async getAllProducts() {
        return await this.productRepository.findAll();
      }

      async getProductById(id) {
        return await this.productRepository.findById(id);
      }

      async createProduct(productData) {
        const product = {
          id: generateId(),
          name: productData.name,
          description: productData.description,
          price: productData.price,
          createdAt: new Date()
        };
        return await this.productRepository.save(product);
      }
    }

    /** 路由設定 */
    const express = require('express');
    const router = express.Router();

    const productController = new ProductController(productService);

    router.get('/products', (req, res) => productController.getProducts(req, res));
    router.get('/products/:id', (req, res) => productController.getProduct(req, res));
    router.post('/products', (req, res) => productController.createProduct(req, res));

    module.exports = router;
    ```

### 桌面應用程式實現範例

以庫存管理系統為例

- 客戶端 (Java Swing)

    ```java
    /** 庫存管理介面 */
    public class InventoryManagementFrame extends JFrame {
        private final InventoryService inventoryService;
        private JTable inventoryTable;
        private DefaultTableModel tableModel;

        public InventoryManagementFrame() {
            this.inventoryService = new InventoryService();
            initializeComponents();
            loadInventoryData();
        }

        private void initializeComponents() {
            setTitle("庫存管理系統");
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setLayout(new BorderLayout());

            /** 建立表格 */
            String[] columns = {"產品ID", "產品名稱", "庫存數量", "最後更新"};
            tableModel = new DefaultTableModel(columns, 0);
            inventoryTable = new JTable(tableModel);
            add(new JScrollPane(inventoryTable), BorderLayout.CENTER);

            /** 建立按鈕面板 */
            JPanel buttonPanel = new JPanel();
            JButton refreshButton = new JButton("重新整理");
            JButton addButton = new JButton("新增產品");
            JButton updateButton = new JButton("更新庫存");

            refreshButton.addActionListener(e -> loadInventoryData());
            addButton.addActionListener(e -> showAddProductDialog());
            updateButton.addActionListener(e -> showUpdateInventoryDialog());

            buttonPanel.add(refreshButton);
            buttonPanel.add(addButton);
            buttonPanel.add(updateButton);
            add(buttonPanel, BorderLayout.SOUTH);

            pack();
            setLocationRelativeTo(null);
        }

        private void loadInventoryData() {
            SwingUtilities.invokeLater(() -> {
                try {
                    List<InventoryItem> items = inventoryService.getAllInventoryItems();
                    updateTable(items);
                } catch (Exception e) {
                    JOptionPane.showMessageDialog(this, "載入庫存資料失敗: " + e.getMessage());
                }
            });
        }

        private void updateTable(List<InventoryItem> items) {
            tableModel.setRowCount(0);
            for (InventoryItem item : items) {
                Object[] row = {
                    item.getProductId(),
                    item.getProductName(),
                    item.getQuantity(),
                    item.getLastUpdated()
                };
                tableModel.addRow(row);
            }
        }
    }

    /** 庫存服務 */
    public class InventoryService {
        private final String serverUrl = "http://localhost:8080/api";
        private final HttpClient httpClient;

        public InventoryService() {
            this.httpClient = HttpClient.newHttpClient();
        }

        public List<InventoryItem> getAllInventoryItems() throws Exception {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(serverUrl + "/inventory"))
                .GET()
                .build();

            HttpResponse<String> response = httpClient.send(request, 
                HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() != 200) {
                throw new Exception("伺服器回應錯誤: " + response.statusCode());
            }

            return parseInventoryItems(response.body());
        }

        public void updateInventory(String productId, int quantity) throws Exception {
            String requestBody = String.format(
                "{\"productId\":\"%s\",\"quantity\":%d}", 
                productId, quantity
            );

            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(serverUrl + "/inventory/update"))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

            HttpResponse<String> response = httpClient.send(request, 
                HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() != 200) {
                throw new Exception("更新庫存失敗: " + response.statusCode());
            }
        }
    }
    ```

- 伺服器端 (Spring Boot)

    ```java
    /** 庫存控制器 */
    @RestController
    @RequestMapping("/api/inventory")
    public class InventoryController {
        private final InventoryService inventoryService;

        public InventoryController(InventoryService inventoryService) {
            this.inventoryService = inventoryService;
        }

        @GetMapping
        public ResponseEntity<List<InventoryItemDto>> getAllInventory() {
            try {
                List<InventoryItemDto> items = inventoryService.getAllInventoryItems();
                return ResponseEntity.ok(items);
            } catch (Exception e) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            }
        }

        @PutMapping("/update")
        public ResponseEntity<Void> updateInventory(@RequestBody UpdateInventoryRequest request) {
            try {
                inventoryService.updateInventory(request.getProductId(), request.getQuantity());
                return ResponseEntity.ok().build();
            } catch (Exception e) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }
        }

        @PostMapping("/products")
        public ResponseEntity<InventoryItemDto> addProduct(@RequestBody AddProductRequest request) {
            try {
                InventoryItemDto item = inventoryService.addProduct(
                    request.getProductName(), 
                    request.getInitialQuantity()
                );
                return ResponseEntity.status(HttpStatus.CREATED).body(item);
            } catch (Exception e) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }
        }
    }

    /** 庫存服務 */
    @Service
    public class InventoryService {
        private final InventoryRepository inventoryRepository;

        public InventoryService(InventoryRepository inventoryRepository) {
            this.inventoryRepository = inventoryRepository;
        }

        public List<InventoryItemDto> getAllInventoryItems() {
            List<InventoryItem> items = inventoryRepository.findAll();
            return items.stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
        }

        public void updateInventory(String productId, int quantity) {
            InventoryItem item = inventoryRepository.findByProductId(productId)
                .orElseThrow(() -> new IllegalArgumentException("產品不存在"));

            item.setQuantity(quantity);
            item.setLastUpdated(LocalDateTime.now());
            inventoryRepository.save(item);
        }

        public InventoryItemDto addProduct(String productName, int initialQuantity) {
            InventoryItem item = new InventoryItem();
            item.setProductId(UUID.randomUUID().toString());
            item.setProductName(productName);
            item.setQuantity(initialQuantity);
            item.setLastUpdated(LocalDateTime.now());

            InventoryItem savedItem = inventoryRepository.save(item);
            return convertToDto(savedItem);
        }

        private InventoryItemDto convertToDto(InventoryItem item) {
            return new InventoryItemDto(
                item.getProductId(),
                item.getProductName(),
                item.getQuantity(),
                item.getLastUpdated()
            );
        }
    }
    ```

### 行動應用程式實現範例

以新聞閱讀 App 為例

- 客戶端 (React Native)

    ```typescript
    /** 新聞服務 */
    export class NewsService {
      private readonly baseUrl = 'https://api.example.com';

      async getNews(category?: string): Promise<NewsArticle[]> {
        const url = category 
          ? `${this.baseUrl}/news?category=${category}`
          : `${this.baseUrl}/news`;

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('獲取新聞失敗');
        }
        return response.json();
      }

      async getArticle(id: string): Promise<NewsArticle> {
        const response = await fetch(`${this.baseUrl}/news/${id}`);
        if (!response.ok) {
          throw new Error('獲取文章詳情失敗');
        }
        return response.json();
      }
    }

    /** 新聞列表元件 */
    export const NewsListScreen: React.FC = () => {
      const [news, setNews] = useState<NewsArticle[]>([]);
      const [loading, setLoading] = useState(true);
      const [refreshing, setRefreshing] = useState(false);
      const newsService = new NewsService();

      useEffect(() => {
        loadNews();
      }, []);

      const loadNews = async () => {
        try {
          setLoading(true);
          const articles = await newsService.getNews();
          setNews(articles);
        } catch (error) {
          Alert.alert('錯誤', '載入新聞失敗');
        } finally {
          setLoading(false);
        }
      };

      const onRefresh = async () => {
        setRefreshing(true);
        await loadNews();
        setRefreshing(false);
      };

      const renderNewsItem = ({ item }: { item: NewsArticle }) => (
        <TouchableOpacity 
          style={styles.newsItem}
          onPress={() => navigation.navigate('ArticleDetail', { id: item.id })}
        >
          <Image source={{ uri: item.imageUrl }} style={styles.newsImage} />
          <View style={styles.newsContent}>
            <Text style={styles.newsTitle}>{item.title}</Text>
            <Text style={styles.newsSummary}>{item.summary}</Text>
            <Text style={styles.newsDate}>{formatDate(item.publishedAt)}</Text>
          </View>
        </TouchableOpacity>
      );

      if (loading) {
        return (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#0066cc" />
          </View>
        );
      }

      return (
        <FlatList
          data={news}
          renderItem={renderNewsItem}
          keyExtractor={(item) => item.id}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          style={styles.container}
        />
      );
    };
    ```

- 伺服器端 (Python Flask)

    ```python
    from flask import Flask, jsonify, request
    from datetime import datetime
    import uuid

    app = Flask(__name__)

    class NewsService:
        def __init__(self):
            self.articles = []
            self._load_sample_data()

        def _load_sample_data(self):
            """載入範例資料"""
            sample_articles = [
                {
                    'id': str(uuid.uuid4()),
                    'title': '科技新聞標題',
                    'summary': '這是一則科技新聞的摘要...',
                    'content': '完整的新聞內容...',
                    'category': 'technology',
                    'image_url': 'https://example.com/image1.jpg',
                    'published_at': datetime.now().isoformat(),
                    'author': '記者姓名'
                }
            ]
            self.articles.extend(sample_articles)

        def get_all_news(self, category=None):
            """獲取所有新聞"""
            if category:
                return [article for article in self.articles 
                       if article['category'] == category]
            return self.articles

        def get_article_by_id(self, article_id):
            """根據 ID 獲取文章"""
            for article in self.articles:
                if article['id'] == article_id:
                    return article
            return None

        def create_article(self, article_data):
            """建立新文章"""
            article = {
                'id': str(uuid.uuid4()),
                'title': article_data['title'],
                'summary': article_data['summary'],
                'content': article_data['content'],
                'category': article_data['category'],
                'image_url': article_data.get('image_url', ''),
                'published_at': datetime.now().isoformat(),
                'author': article_data['author']
            }
            self.articles.append(article)
            return article

    news_service = NewsService()

    @app.route('/news', methods=['GET'])
    def get_news():
        """獲取新聞列表"""
        try:
            category = request.args.get('category')
            articles = news_service.get_all_news(category)
            return jsonify(articles)
        except Exception as e:
            return jsonify({'error': '獲取新聞失敗'}), 500

    @app.route('/news/<article_id>', methods=['GET'])
    def get_article(article_id):
        """獲取單篇文章"""
        try:
            article = news_service.get_article_by_id(article_id)
            if not article:
                return jsonify({'error': '文章不存在'}), 404
            return jsonify(article)
        except Exception as e:
            return jsonify({'error': '獲取文章失敗'}), 500

    @app.route('/news', methods=['POST'])
    def create_article():
        """建立新文章"""
        try:
            article_data = request.json
            article = news_service.create_article(article_data)
            return jsonify(article), 201
        except Exception as e:
            return jsonify({'error': '建立文章失敗'}), 400

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
    ```

<br />

## 變體架構

### 2-Tier Architecture (兩層架構)

客戶端直接連接資料庫，適合小型應用程式。

```text
┌─────────────────┐    Direct DB     ┌─────────────────┐
│     Client      │ ◄──────────────► │    Database     │
│                 │    Connection    │                 │
│ • UI Logic      │                  │ • Data Storage  │
│ • Business Logic│                  │ • Data Rules    │
└─────────────────┘                  └─────────────────┘
```

### 3-Tier Architecture (三層架構)

增加中間層處理業務規則，提供更好的分離。

```text
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Presentation   │ ◄──► │  Application    │ ◄──► │      Data       │
│     Tier        │      │      Tier       │      │      Tier       │
│                 │      │                 │      │                 │
│ • User Interface│      │ • Business Logic│      │ • Database      │
│ • Input/Output  │      │ • Processing    │      │ • File System  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

### N-Tier Architecture (多層架構)

進一步細分層次，適合複雜的企業應用程式。

```text
┌─────────────────┐
│  Presentation   │
└─────────────────┘
         │
┌─────────────────┐
│   Web Service   │
└─────────────────┘
         │
┌─────────────────┐
│  Business Logic │
└─────────────────┘
         │
┌─────────────────┐
│  Data Access    │
└─────────────────┘
         │
┌─────────────────┐
│    Database     │
└─────────────────┘
```

<br />

## 通訊協定

### HTTP/HTTPS

最常用的 Web 通訊協定，支援 RESTful API。

```typescript
/** RESTful API 範例 */
const apiClient = {
  async get(url: string) {
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
  },

  async post(url: string, data: any) {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  }
};
```

### WebSocket

支援雙向即時通訊，適合聊天應用程式和即時更新。

```typescript
/** WebSocket 客戶端 */
class ChatClient {
  private socket: WebSocket;

  connect(url: string) {
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log('連接已建立');
    };

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.socket.onclose = () => {
      console.log('連接已關閉');
    };
  }

  sendMessage(message: string) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type: 'message', content: message }));
    }
  }

  private handleMessage(message: any) {
    // 處理接收到的訊息
  }
}
```

### gRPC

高效能的 RPC 框架，適合微服務間通訊。

```typescript
/** gRPC 客戶端範例 */
import { UserServiceClient } from './generated/user_grpc_pb';
import { GetUserRequest } from './generated/user_pb';

class UserClient {
  private client: UserServiceClient;

  constructor(serverUrl: string) {
    this.client = new UserServiceClient(serverUrl);
  }

  async getUser(userId: string): Promise<User> {
    const request = new GetUserRequest();
    request.setUserId(userId);

    return new Promise((resolve, reject) => {
      this.client.getUser(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve(response.toObject());
        }
      });
    });
  }
}
```

<br />

## 優點

### 資源共享

多個客戶端可以共享伺服器資源和資料。

### 集中式管理

資料和業務規則集中管理，便於維護和更新。

### 可擴展性

可以根據需求擴展伺服器容量或增加伺服器數量。

### 安全性

敏感資料和業務規則保存在伺服器端，提高安全性。

### 一致性

所有客戶端存取相同的資料來源，確保資料一致性。

<br />

## 缺點

### 網路依賴

客戶端必須連接網路才能正常運作。

### 單點故障

伺服器故障會影響所有客戶端。

### 網路延遲

網路通訊會增加回應時間。

### 伺服器負載

大量客戶端同時存取可能造成伺服器負載過重。

### 複雜性

需要處理網路通訊、錯誤處理和狀態管理。

<br />

## 適用場景

### 適合使用

- Web 應用程式：需要多使用者同時存取

- 企業系統：需要集中式資料管理

- 行動應用程式：需要雲端資料同步

- 多平台應用：需要跨平台資料共享

- 即時協作：需要即時資料更新

### 不適合使用

- 離線應用程式：需要在無網路環境下運作

- 即時遊戲：對延遲要求極高

- 簡單工具：不需要資料共享

- 嵌入式系統：資源受限的環境

<br />

## 實施建議

### 設計原則

- 保持客戶端輕量化，將複雜業務規則放在伺服器端

- 設計清晰的 API 介面，便於客戶端呼叫

- 實現適當的錯誤處理和重試機制

- 考慮離線功能和資料快取

### 效能最佳化

- 使用資料快取減少網路請求

- 實現資料分頁和懶載入

- 壓縮傳輸資料減少頻寬使用

- 使用 CDN 加速靜態資源載入

### 安全考量

- 實現身份驗證和授權機制

- 使用 HTTPS 加密傳輸

- 驗證和清理使用者輸入

- 實現適當的存取控制

### 可靠性設計

- 實現伺服器叢集和負載平衡

- 設計資料備份和災難復原機制

- 監控系統效能和可用性

- 實現優雅的錯誤處理

<br />

## 總結

Client-Server Architecture 是現代軟體系統的基礎架構模式，通過分離客戶端和伺服器端的職責，提供了良好的可擴展性、可維護性和資源共享能力。

這種架構特別適合需要多使用者存取、集中式資料管理和跨平台支援的應用程式。雖然增加了網路通訊的複雜性，但通過適當的設計和實施，可以建構出穩定、高效的分散式系統。

選擇 Client-Server Architecture 時，需要考慮應用程式的具體需求、使用者規模、效能要求和維護成本，以確保架構選擇符合專案目標。
