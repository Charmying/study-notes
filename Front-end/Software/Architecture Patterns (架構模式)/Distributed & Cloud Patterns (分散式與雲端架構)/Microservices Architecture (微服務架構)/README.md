# Microservices Architecture (微服務架構)

Microservices Architecture (微服務架構) 是一種將單一應用程式開發為一組小型服務的方法，每個服務運行在自己的進程中，並通過輕量級機制 (通常是 HTTP API) 進行通訊。

這種架構強調服務的獨立性，每個微服務都可以獨立開發、部署和擴展，使系統更具彈性和可維護性。

<br />

## 動機

在傳統的單體架構中，常見的問題包括

- 單一故障點：一個元件的問題可能影響整個系統

- 技術債務累積：隨著時間推移，程式碼變得難以維護

- 擴展困難：必須擴展整個應用程式，無法針對特定功能擴展

- 部署風險：任何變更都需要重新部署整個應用程式

- 技術棧限制：整個應用程式必須使用相同的技術棧

Microservices Architecture 通過服務分解和獨立部署，解決這些問題，讓系統具備

- 獨立性：每個服務可以獨立開發和部署

- 可擴展性：可以針對特定服務進行擴展

- 技術多樣性：不同服務可以使用不同的技術棧

- 容錯性：單一服務的故障不會影響整個系統

<br />

## 結構

Microservices Architecture 將應用程式分解為多個獨立的服務，每個服務負責特定的業務功能。

### 核心元件

#### 1. 微服務 (Microservices)

獨立的業務服務，具有以下特徵：

- 單一職責：每個服務專注於一個業務領域

- 獨立部署：可以獨立於其他服務進行部署

- 資料獨立：擁有自己的資料庫

- 技術獨立：可以使用不同的程式語言和框架

#### 2. API Gateway (API 閘道)

作為所有客戶端請求的入口點：

- 路由：將請求路由到適當的微服務

- 認證：處理身份驗證和授權

- 限流：控制請求頻率

- 監控：收集請求指標和日誌

#### 3. Service Discovery (服務發現)

管理服務實例的註冊和發現：

- 服務註冊：服務啟動時註冊自己

- 健康檢查：監控服務健康狀態

- 負載均衡：在多個服務實例間分配請求

#### 4. Configuration Management (配置管理)

集中管理所有服務的配置：

- 環境配置：不同環境的配置管理

- 動態更新：運行時更新配置

- 版本控制：配置變更的版本管理

以下是 Microservices Architecture 的架構圖

```text
┌───────────────────────────────────────────────────────────────┐
│                        Client Layer                           │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│   │   Web App   │  │ Mobile App  │  │   Third Party API   │   │
│   └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                              │
┌───────────────────────────────────────────────────────────────┐
│                         API Gateway                           │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│   │   Routing   │  │    Auth     │  │    Rate Limiting    │   │
│   └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
                              │
┌───────────────────────────────────────────────────────────────┐
│                    Microservices Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────────┐  │
│  │     User    │  │    Order    │  │        Payment        │  │
│  │   Service   │  │   Service   │  │        Service        │  │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │  ┌──────────────────┐ │  │
│  │ │   DB    │ │  │ │   DB    │ │  │  │        DB        │ │  │
│  │ └─────────┘ │  │ └─────────┘ │  │  └──────────────────┘ │  │
│  └─────────────┘  └─────────────┘  └───────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
┌───────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                       │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│   │   Service   │  │   Config    │  │     Monitoring      │   │
│   │  Discovery  │  │ Management  │  │    & Logging        │   │
│   └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

<br />

## 核心原則

### 單一職責原則 (Single Responsibility Principle)

每個微服務應該專注於一個業務功能或領域。

### 去中心化治理 (Decentralized Governance)

每個團隊可以選擇最適合的技術棧和開發流程。

### 故障隔離 (Failure Isolation)

一個服務的故障不應該影響其他服務的正常運行。

### 資料獨立性 (Data Independence)

每個服務應該擁有自己的資料庫，避免共享資料庫。

<br />

## 實現方式

### Node.js Express 實現範例

以電商系統為例，包含用戶服務、訂單服務和支付服務

- 用戶服務 (User Service)

    ```javascript
    /** 用戶服務 - app.js */
    const express = require('express');
    const mongoose = require('mongoose');
    const userRoutes = require('./routes/users');
    const { registerService } = require('./utils/serviceRegistry');

    const app = express();
    const PORT = process.env.PORT || 3001;

    app.use(express.json());
    app.use('/api/users', userRoutes);

    /** 健康檢查端點 */
    app.get('/health', (req, res) => {
      res.status(200).json({ status: 'healthy', service: 'user-service' });
    });

    /** 連接資料庫 */
    mongoose.connect(process.env.MONGODB_URI)
      .then(() => {
        console.log('Connected to User Database');

        /** 啟動服務並註冊到服務發現 */
        app.listen(PORT, async () => {
          console.log(`User Service running on port ${PORT}`);
          await registerService('user-service', PORT);
        });
      })
      .catch(err => console.error('Database connection error:', err));
    ```

    ```javascript
    /** 用戶路由 - routes/users.js */
    const express = require('express');
    const User = require('../models/User');
    const router = express.Router();

    /** 建立用戶 */
    router.post('/', async (req, res) => {
      try {
        const { email, name, password } = req.body;

        /** 檢查用戶是否已存在 */
        const existingUser = await User.findOne({ email });
        if (existingUser) {
          return res.status(400).json({ error: 'Email already exists' });
        }

        const user = new User({ email, name, password });
        await user.save();

        res.status(201).json({
          id: user._id,
          email: user.email,
          name: user.name
        });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    /** 取得用戶資訊 */
    router.get('/:id', async (req, res) => {
      try {
        const user = await User.findById(req.params.id).select('-password');
        if (!user) {
          return res.status(404).json({ error: 'User not found' });
        }
        res.json(user);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    module.exports = router;
    ```

- 訂單服務 (Order Service)

    ```javascript
    /** 訂單服務 - app.js */
    const express = require('express');
    const mongoose = require('mongoose');
    const orderRoutes = require('./routes/orders');
    const { registerService } = require('./utils/serviceRegistry');

    const app = express();
    const PORT = process.env.PORT || 3002;

    app.use(express.json());
    app.use('/api/orders', orderRoutes);

    app.get('/health', (req, res) => {
      res.status(200).json({ status: 'healthy', service: 'order-service' });
    });

    mongoose.connect(process.env.MONGODB_URI)
      .then(() => {
        console.log('Connected to Order Database');

        app.listen(PORT, async () => {
          console.log(`Order Service running on port ${PORT}`);
          await registerService('order-service', PORT);
        });
      })
      .catch(err => console.error('Database connection error:', err));
    ```

    ```javascript
    /** 訂單路由 - routes/orders.js */
    const express = require('express');
    const Order = require('../models/Order');
    const { callService } = require('../utils/serviceClient');
    const router = express.Router();

    /** 建立訂單 */
    router.post('/', async (req, res) => {
      try {
        const { userId, items, totalAmount } = req.body;

        /** 驗證用戶存在 */
        const userResponse = await callService('user-service', `/api/users/${userId}`);
        if (!userResponse.success) {
          return res.status(400).json({ error: 'Invalid user' });
        }

        /** 建立訂單 */
        const order = new Order({
          userId,
          items,
          totalAmount,
          status: 'pending'
        });

        await order.save();

        /** 呼叫支付服務 */
        const paymentResponse = await callService('payment-service', '/api/payments', {
          method: 'POST',
          data: {
            orderId: order._id,
            amount: totalAmount,
            userId
          }
        });

        if (paymentResponse.success) {
          order.status = 'paid';
          await order.save();
        }

        res.status(201).json(order);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    /** 取得訂單 */
    router.get('/:id', async (req, res) => {
      try {
        const order = await Order.findById(req.params.id);
        if (!order) {
          return res.status(404).json({ error: 'Order not found' });
        }
        res.json(order);
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    module.exports = router;
    ```

- 支付服務 (Payment Service)

    ```javascript
    /** 支付服務 - app.js */
    const express = require('express');
    const mongoose = require('mongoose');
    const paymentRoutes = require('./routes/payments');
    const { registerService } = require('./utils/serviceRegistry');

    const app = express();
    const PORT = process.env.PORT || 3003;

    app.use(express.json());
    app.use('/api/payments', paymentRoutes);

    app.get('/health', (req, res) => {
      res.status(200).json({ status: 'healthy', service: 'payment-service' });
    });

    mongoose.connect(process.env.MONGODB_URI)
      .then(() => {
        console.log('Connected to Payment Database');

        app.listen(PORT, async () => {
          console.log(`Payment Service running on port ${PORT}`);
          await registerService('payment-service', PORT);
        });
      })
      .catch(err => console.error('Database connection error:', err));
    ```

- API Gateway

    ```javascript
    /** API Gateway - gateway.js */
    const express = require('express');
    const httpProxy = require('http-proxy-middleware');
    const { getServiceUrl } = require('./utils/serviceDiscovery');
    const rateLimit = require('express-rate-limit');

    const app = express();
    const PORT = process.env.PORT || 3000;

    /** 限流中間件 */
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, /** 15 分鐘 */
      max: 100 /** 限制每個 IP 15 分鐘內最多 100 個請求 */
    });

    app.use(limiter);
    app.use(express.json());

    /** 動態代理中間件 */
    const createProxyMiddleware = (serviceName, pathRewrite = {}) => {
      return httpProxy({
        target: () => getServiceUrl(serviceName),
        changeOrigin: true,
        pathRewrite,
        onError: (err, req, res) => {
          console.error(`Proxy error for ${serviceName}:`, err.message);
          res.status(503).json({ error: 'Service temporarily unavailable' });
        }
      });
    };

    /** 路由配置 */
    app.use('/api/users', createProxyMiddleware('user-service'));
    app.use('/api/orders', createProxyMiddleware('order-service'));
    app.use('/api/payments', createProxyMiddleware('payment-service'));

    /** 健康檢查 */
    app.get('/health', (req, res) => {
      res.json({ status: 'healthy', service: 'api-gateway' });
    });

    app.listen(PORT, () => {
      console.log(`API Gateway running on port ${PORT}`);
    });
    ```

- 服務發現工具

    ```javascript
    /** 服務註冊 - utils/serviceRegistry.js */
    const consul = require('consul')();

    const registerService = async (serviceName, port) => {
      try {
        await consul.agent.service.register({
          id: `${serviceName}-${port}`,
          name: serviceName,
          port: port,
          check: {
            http: `http://localhost:${port}/health`,
            interval: '10s'
          }
        });
        console.log(`Service ${serviceName} registered successfully`);
      } catch (error) {
        console.error(`Failed to register service ${serviceName}:`, error);
      }
    };

    module.exports = { registerService };
    ```

    ```javascript
    /** 服務發現 - utils/serviceDiscovery.js */
    const consul = require('consul')();

    const getServiceUrl = async (serviceName) => {
      try {
        const services = await consul.health.service(serviceName);
        const healthyServices = services.filter(service => 
          service.Checks.every(check => check.Status === 'passing')
        );

        if (healthyServices.length === 0) {
          throw new Error(`No healthy instances of ${serviceName} found`);
        }

        /** 簡單的負載均衡 - 隨機選擇 */
        const randomIndex = Math.floor(Math.random() * healthyServices.length);
        const selectedService = healthyServices[randomIndex];

        return `http://${selectedService.Service.Address}:${selectedService.Service.Port}`;
      } catch (error) {
        console.error(`Service discovery error for ${serviceName}:`, error);
        throw error;
      }
    };

    module.exports = { getServiceUrl };
    ```

### Java (Spring Boot) 實現範例

- 用戶服務

    ```java
    /** 用戶服務主類 */
    @SpringBootApplication
    @EnableEurekaClient
    public class UserServiceApplication {
        public static void main(String[] args) {
            SpringApplication.run(UserServiceApplication.class, args);
        }
    }

    /** 用戶控制器 */
    @RestController
    @RequestMapping("/api/users")
    public class UserController {
        private final UserService userService;

        public UserController(UserService userService) {
            this.userService = userService;
        }

        @PostMapping
        public ResponseEntity<UserResponse> createUser(@RequestBody CreateUserRequest request) {
            try {
                UserResponse response = userService.createUser(request);
                return ResponseEntity.status(HttpStatus.CREATED).body(response);
            } catch (UserAlreadyExistsException e) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }
        }

        @GetMapping("/{id}")
        public ResponseEntity<UserResponse> getUser(@PathVariable String id) {
            Optional<UserResponse> user = userService.findById(id);
            return user.map(ResponseEntity::ok)
                      .orElse(ResponseEntity.notFound().build());
        }
    }

    /** 用戶服務實現 */
    @Service
    @Transactional
    public class UserService {
        private final UserRepository userRepository;
        private final PasswordEncoder passwordEncoder;

        public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
            this.userRepository = userRepository;
            this.passwordEncoder = passwordEncoder;
        }

        public UserResponse createUser(CreateUserRequest request) {
            if (userRepository.existsByEmail(request.getEmail())) {
                throw new UserAlreadyExistsException("Email already exists");
            }

            User user = new User(
                request.getEmail(),
                request.getName(),
                passwordEncoder.encode(request.getPassword())
            );

            User savedUser = userRepository.save(user);
            return UserResponse.from(savedUser);
        }

        public Optional<UserResponse> findById(String id) {
            return userRepository.findById(id)
                .map(UserResponse::from);
        }
    }
    ```

- 訂單服務

    ```java
    /** 訂單服務主類 */
    @SpringBootApplication
    @EnableEurekaClient
    @EnableFeignClients
    public class OrderServiceApplication {
        public static void main(String[] args) {
            SpringApplication.run(OrderServiceApplication.class, args);
        }
    }

    /** 訂單控制器 */
    @RestController
    @RequestMapping("/api/orders")
    public class OrderController {
        private final OrderService orderService;

        public OrderController(OrderService orderService) {
            this.orderService = orderService;
        }

        @PostMapping
        public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
            try {
                OrderResponse response = orderService.createOrder(request);
                return ResponseEntity.status(HttpStatus.CREATED).body(response);
            } catch (Exception e) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }
        }

        @GetMapping("/{id}")
        public ResponseEntity<OrderResponse> getOrder(@PathVariable String id) {
            Optional<OrderResponse> order = orderService.findById(id);
            return order.map(ResponseEntity::ok)
                       .orElse(ResponseEntity.notFound().build());
        }
    }

    /** Feign 客戶端 */
    @FeignClient(name = "user-service")
    public interface UserServiceClient {
        @GetMapping("/api/users/{id}")
        UserResponse getUser(@PathVariable String id);
    }

    @FeignClient(name = "payment-service")
    public interface PaymentServiceClient {
        @PostMapping("/api/payments")
        PaymentResponse processPayment(@RequestBody PaymentRequest request);
    }

    /** 訂單服務實現 */
    @Service
    @Transactional
    public class OrderService {
        private final OrderRepository orderRepository;
        private final UserServiceClient userServiceClient;
        private final PaymentServiceClient paymentServiceClient;

        public OrderService(
            OrderRepository orderRepository,
            UserServiceClient userServiceClient,
            PaymentServiceClient paymentServiceClient
        ) {
            this.orderRepository = orderRepository;
            this.userServiceClient = userServiceClient;
            this.paymentServiceClient = paymentServiceClient;
        }

        public OrderResponse createOrder(CreateOrderRequest request) {
            /** 驗證用戶存在 */
            try {
                userServiceClient.getUser(request.getUserId());
            } catch (FeignException.NotFound e) {
                throw new UserNotFoundException("User not found");
            }

            /** 建立訂單 */
            Order order = new Order(
                request.getUserId(),
                request.getItems(),
                request.getTotalAmount()
            );

            Order savedOrder = orderRepository.save(order);

            /** 處理支付 */
            try {
                PaymentRequest paymentRequest = new PaymentRequest(
                    savedOrder.getId(),
                    savedOrder.getTotalAmount(),
                    savedOrder.getUserId()
                );

                PaymentResponse paymentResponse = paymentServiceClient.processPayment(paymentRequest);

                if (paymentResponse.isSuccessful()) {
                    savedOrder.markAsPaid();
                    orderRepository.save(savedOrder);
                }
            } catch (Exception e) {
                /** 支付失敗處理 */
                savedOrder.markAsFailed();
                orderRepository.save(savedOrder);
            }

            return OrderResponse.from(savedOrder);
        }

        public Optional<OrderResponse> findById(String id) {
            return orderRepository.findById(id)
                .map(OrderResponse::from);
        }
    }
    ```

- API Gateway (Spring Cloud Gateway)

    ```java
    /** Gateway 配置 */
    @Configuration
    public class GatewayConfig {

        @Bean
        public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
            return builder.routes()
                .route("user-service", r -> r.path("/api/users/**")
                    .uri("lb://user-service"))
                .route("order-service", r -> r.path("/api/orders/**")
                    .uri("lb://order-service"))
                .route("payment-service", r -> r.path("/api/payments/**")
                    .uri("lb://payment-service"))
                .build();
        }

        @Bean
        public RedisRateLimiter redisRateLimiter() {
            return new RedisRateLimiter(10, 20, 1);
        }

        @Bean
        public KeyResolver userKeyResolver() {
            return exchange -> exchange.getRequest().getRemoteAddress()
                .map(addr -> addr.getAddress().getHostAddress())
                .map(Mono::just)
                .orElse(Mono.just("anonymous"));
        }
    }
    ```

### Docker 容器化部署

- 用戶服務 Dockerfile

    ```dockerfile
    FROM node:16-alpine

    WORKDIR /app

    COPY package*.json ./
    RUN npm ci --only=production

    COPY . .

    EXPOSE 3001

    HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
      CMD curl -f http://localhost:3001/health || exit 1

    CMD ["node", "app.js"]
    ```

- Docker Compose 配置

    ```yaml
    version: '3.8'

    services:
      consul:
        image: consul:1.15
        ports:
          - "8500:8500"
        command: consul agent -dev -client=0.0.0.0

      api-gateway:
        build: ./api-gateway
        ports:
          - "3000:3000"
        environment:
          - CONSUL_HOST=consul
        depends_on:
          - consul
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
          interval: 30s
          timeout: 10s
          retries: 3

      user-service:
        build: ./user-service
        ports:
          - "3001:3001"
        environment:
          - MONGODB_URI=mongodb://user-db:27017/users
          - CONSUL_HOST=consul
        depends_on:
          - user-db
          - consul
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
          interval: 30s
          timeout: 10s
          retries: 3

      order-service:
        build: ./order-service
        ports:
          - "3002:3002"
        environment:
          - MONGODB_URI=mongodb://order-db:27017/orders
          - CONSUL_HOST=consul
        depends_on:
          - order-db
          - consul
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3002/health"]
          interval: 30s
          timeout: 10s
          retries: 3

      payment-service:
        build: ./payment-service
        ports:
          - "3003:3003"
        environment:
          - MONGODB_URI=mongodb://payment-db:27017/payments
          - CONSUL_HOST=consul
        depends_on:
          - payment-db
          - consul
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:3003/health"]
          interval: 30s
          timeout: 10s
          retries: 3

      user-db:
        image: mongo:5.0
        volumes:
          - user-data:/data/db

      order-db:
        image: mongo:5.0
        volumes:
          - order-data:/data/db

      payment-db:
        image: mongo:5.0
        volumes:
          - payment-data:/data/db

    volumes:
      user-data:
      order-data:
      payment-data:
    ```

<br />

## 優點

### 獨立開發和部署

每個服務可以由不同的團隊獨立開發，使用不同的技術棧，並且可以獨立部署和擴展。

### 技術多樣性

不同的服務可以使用最適合的程式語言、框架和資料庫。

### 容錯性

單一服務的故障不會導致整個系統崩潰，其他服務仍可正常運行。

### 可擴展性

可以針對特定的服務進行水平擴展，而不需要擴展整個應用程式。

### 組織對齊

服務邊界可以與組織結構對齊，每個團隊負責特定的業務領域。

<br />

## 缺點

### 複雜性增加

分散式系統帶來額外的複雜性，包括網路通訊、資料一致性、服務發現等問題。

### 運維挑戰

需要管理多個服務的部署、監控、日誌收集和故障排除。

### 網路延遲

服務間的網路通訊會增加延遲，影響系統性能。

### 資料一致性

分散式事務和資料一致性變得更加困難。

### 測試複雜度

整合測試和端到端測試變得更加複雜。

<br />

## 適用場景

### 適合使用

- 大型應用程式：具有複雜業務功能的大型系統

- 多團隊開發：多個開發團隊同時工作

- 高可用性要求：需要高可用性和容錯能力

- 不同擴展需求：不同功能有不同的擴展需求

- 技術多樣性：需要使用不同技術棧的場景

### 不適合使用

- 小型應用程式：功能簡單的小型系統

- 單一團隊：小型開發團隊

- 緊密耦合的功能：業務功能高度相關且難以分離

- 資源有限：缺乏足夠的基礎設施和運維資源

<br />

## 實施建議

### 服務劃分策略

根據業務領域 (Domain-Driven Design) 來劃分服務，確保每個服務有明確的業務邊界。

### 資料管理

每個服務應該擁有自己的資料庫，避免共享資料庫造成的耦合。

### 通訊機制

選擇適當的通訊機制，同步通訊 (HTTP/REST) 用於即時查詢，非同步通訊 (Message Queue) 用於事件處理。

### 監控和日誌

建立完整的監控和日誌系統，包括分散式追蹤、指標收集和集中式日誌管理。

### 自動化部署

建立 CI/CD 流水線，實現自動化測試、建置和部署。

### 容器化

使用 Docker 和 Kubernetes 等容器技術，簡化部署和管理。

<br />

## 總結

Microservices Architecture 提供了一種強大的方法來構建大型、複雜的分散式系統。雖然帶來了額外的複雜性，但對於需要高可擴展性、高可用性和技術多樣性的應用程式來說，這種架構模式能夠帶來巨大的價值。

成功實施微服務架構需要充分的規劃、適當的工具支援和成熟的開發運維流程。關鍵在於根據組織的實際需求和能力來決定是否採用，以及採用的程度和方式。
