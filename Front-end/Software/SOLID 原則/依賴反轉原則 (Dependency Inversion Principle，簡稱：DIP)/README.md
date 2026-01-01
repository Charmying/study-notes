# 依賴反轉原則 (Dependency Inversion Principle)

在軟體開發過程中，模組間的依賴關係往往決定了系統的靈活性與可維護性。

傳統的軟體架構中，高層模組直接依賴於低層模組的具體實作，這種依賴關係使得系統變得僵化且難以擴展。

為了解決這個問題，物件導向設計提出了依賴反轉原則 (Dependency Inversion Principle，簡稱：DIP)。

<br />

## DIP 的核心理念

### DIP 的定義包含兩個重要概念

- 高層模組不應該依賴於低層模組，兩者都應該依賴於抽象

- 抽象不應該依賴於具體實作，具體實作應該依賴於抽象

簡單來說，系統應該依賴於介面或抽象類別，而不是具體的實作類別。這樣可以讓系統更加靈活，當需要更換實作時，只需要提供新的實作類別，而不需要修改使用該功能的程式碼。

<br />

## DIP 的核心概念

- 抽象依賴：依賴於介面或抽象類別，而非具體實作

- 控制反轉：將依賴關係的控制權從使用者轉移到外部

- 依賴注入：透過建構函式、方法或屬性注入依賴

- 鬆散耦合：減少模組間的直接依賴關係

<br />

## DIP 的優缺點

### 優點

- 提高靈活性：可以輕鬆替換不同的實作

- 增強可測試性：可以注入模擬物件進行單元測試

- 降低耦合度：模組間依賴關係更加鬆散

- 提升可維護性：修改實作不會影響使用該功能的程式碼

- 支援多種實作：同一個介面可以有多種不同的實作

- 符合開放封閉原則：對擴展開放，對修改封閉

### 缺點

- 增加複雜度：需要額外的抽象層和依賴注入機制

- 學習成本：需要理解抽象和依賴注入的概念

- 過度設計風險：可能導致不必要的抽象

- 執行時期錯誤：依賴注入錯誤可能在執行時才被發現

- 除錯困難：抽象層可能使除錯變得更加複雜

- 效能影響：額外的抽象層可能帶來輕微的效能損失

<br />

## 違反 DIP 的問題

- 緊密耦合：高層模組直接依賴低層模組的具體實作

- 難以測試：無法輕鬆替換依賴進行單元測試

- 缺乏彈性：更換實作需要修改大量程式碼

- 違反開放封閉原則：新增功能需要修改現有程式碼

<br />

## 實作範例

依 TypeScript 為例

### 違反 DIP 的範例

```typescript
/** 低層模組：具體的資料存取實作 */
class MySQLDatabase {
  save(data: string): void {
    console.log(`Saving data to MySQL: ${data}`);
  }

  find(id: string): string {
    console.log(`Finding data from MySQL with id: ${id}`);
    return "data from MySQL";
  }
}

/** 高層模組：直接依賴具體實作 */
class UserService {
  private database: MySQLDatabase; // 直接依賴具體實作

  constructor() {
    this.database = new MySQLDatabase(); // 緊密耦合
  }

  createUser(userData: string): void {
    // 業務流程處理
    const processedData = `processed: ${userData}`;
    this.database.save(processedData);
  }

  getUser(id: string): string {
    return this.database.find(id);
  }
}
```

### 遵循 DIP 的範例

```typescript
/** 抽象層：定義資料存取介面 */
interface DatabaseInterface {
  save(data: string): void;
  find(id: string): string;
}

/** 低層模組：MySQL 實作 */
class MySQLDatabase implements DatabaseInterface {
  save(data: string): void {
    console.log(`Saving data to MySQL: ${data}`);
  }

  find(id: string): string {
    console.log(`Finding data from MySQL with id: ${id}`);
    return "data from MySQL";
  }
}

/** 低層模組：MongoDB 實作 */
class MongoDatabase implements DatabaseInterface {
  save(data: string): void {
    console.log(`Saving data to MongoDB: ${data}`);
  }

  find(id: string): string {
    console.log(`Finding data from MongoDB with id: ${id}`);
    return "data from MongoDB";
  }
}

/** 高層模組：依賴於抽象 */
class UserService {
  private database: DatabaseInterface; // 依賴於抽象

  constructor(database: DatabaseInterface) { // 依賴注入
    this.database = database;
  }

  createUser(userData: string): void {
    // 業務流程處理
    const processedData = `processed: ${userData}`;
    this.database.save(processedData);
  }

  getUser(id: string): string {
    return this.database.find(id);
  }
}

/** 使用範例 */
class Application {
  static main(): void {
    // 可以輕鬆切換不同的資料庫實作
    const mysqlDb = new MySQLDatabase();
    const mongoDb = new MongoDatabase();

    const userServiceWithMySQL = new UserService(mysqlDb);
    const userServiceWithMongo = new UserService(mongoDb);

    userServiceWithMySQL.createUser("Tina");
    userServiceWithMongo.createUser("Charmy");
  }
}
```

<br />

## 其他語言範例

### Java 範例

```java
// 抽象層
public interface PaymentProcessor {
    void processPayment(double amount);
    boolean validatePayment(double amount);
}

// 具體實作
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing credit card payment: $" + amount);
    }

    @Override
    public boolean validatePayment(double amount) {
        return amount > 0 && amount <= 10000;
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing PayPal payment: $" + amount);
    }

    @Override
    public boolean validatePayment(double amount) {
        return amount > 0;
    }
}

// 高層模組
public class OrderService {
    private PaymentProcessor paymentProcessor;

    public OrderService(PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }

    public void processOrder(double amount) {
        if (paymentProcessor.validatePayment(amount)) {
            paymentProcessor.processPayment(amount);
            System.out.println("Order processed successfully");
        } else {
            System.out.println("Payment validation failed");
        }
    }
}
```

### Python 範例

```python
from abc import ABC, abstractmethod

# 抽象層
class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str, recipient: str) -> None:
        pass

# 具體實作
class EmailNotification(NotificationService):
    def send_notification(self, message: str, recipient: str) -> None:
        print(f"Sending email to {recipient}: {message}")

class SMSNotification(NotificationService):
    def send_notification(self, message: str, recipient: str) -> None:
        print(f"Sending SMS to {recipient}: {message}")

class PushNotification(NotificationService):
    def send_notification(self, message: str, recipient: str) -> None:
        print(f"Sending push notification to {recipient}: {message}")

# 高層模組
class UserNotificationManager:
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    def notify_user(self, user_id: str, message: str) -> None:
        # 業務流程處理
        formatted_message = f"[User {user_id}] {message}"
        self._notification_service.send_notification(formatted_message, user_id)

# 使用範例
def main():
    email_service = EmailNotification()
    sms_service = SMSNotification()

    email_manager = UserNotificationManager(email_service)
    sms_manager = UserNotificationManager(sms_service)

    email_manager.notify_user("user123", "Welcome to our platform!")
    sms_manager.notify_user("user456", "Your order has been shipped!")
```

<br />

## 實際應用場景

### 日誌系統

```typescript
/** 抽象層 */
interface Logger {
  log(level: string, message: string): void;
}

/** 具體實作 */
class FileLogger implements Logger {
  log(level: string, message: string): void {
    console.log(`[FILE] ${level}: ${message}`);
  }
}

class DatabaseLogger implements Logger {
  log(level: string, message: string): void {
    console.log(`[DB] ${level}: ${message}`);
  }
}

class ConsoleLogger implements Logger {
  log(level: string, message: string): void {
    console.log(`[CONSOLE] ${level}: ${message}`);
  }
}

/** 高層模組 */
class ApplicationService {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  performOperation(): void {
    this.logger.log("INFO", "Operation started");
    // 執行業務流程
    this.logger.log("INFO", "Operation completed");
  }
}
```

### 快取系統

```typescript
/** 抽象層 */
interface CacheService {
  get(key: string): string | null;
  set(key: string, value: string, ttl?: number): void;
  delete(key: string): void;
}

/** 具體實作 */
class RedisCache implements CacheService {
  get(key: string): string | null {
    console.log(`Getting from Redis: ${key}`);
    return "cached_value";
  }

  set(key: string, value: string, ttl?: number): void {
    console.log(`Setting to Redis: ${key} = ${value}`);
  }

  delete(key: string): void {
    console.log(`Deleting from Redis: ${key}`);
  }
}

class MemoryCache implements CacheService {
  private cache = new Map<string, string>();

  get(key: string): string | null {
    return this.cache.get(key) || null;
  }

  set(key: string, value: string): void {
    this.cache.set(key, value);
  }

  delete(key: string): void {
    this.cache.delete(key);
  }
}

/** 高層模組 */
class ProductService {
  private cache: CacheService;

  constructor(cache: CacheService) {
    this.cache = cache;
  }

  getProduct(id: string): string {
    const cached = this.cache.get(`product_${id}`);
    if (cached) {
      return cached;
    }

    /** 從資料庫獲取產品資訊 */
    const product = `Product ${id} data`;
    this.cache.set(`product_${id}`, product, 3600);
    return product;
  }
}
```

<br />

## 依賴注入的實作方式

### 建構函式注入

```typescript
class OrderService {
  constructor(
    private paymentService: PaymentService,
    private inventoryService: InventoryService,
    private emailService: EmailService
  ) {}

  processOrder(order: Order): void {
    // 使用注入的服務
  }
}
```

### 方法注入

```typescript
class ReportGenerator {
  generateReport(data: any[], formatter: ReportFormatter): string {
    return formatter.format(data);
  }
}
```

### 屬性注入

```typescript
class UserController {
  userService: UserService;

  setUserService(service: UserService): void {
    this.userService = service;
  }
}
```

### 介面注入

```typescript
interface ServiceInjectable {
  injectService(service: any): void;
}

class UserManager implements ServiceInjectable {
  private userService: UserService;

  injectService(service: UserService): void {
    this.userService = service;
  }
}
```

<br />

## 依賴注入容器

### 簡單的 DI 容器實作

```typescript
class DIContainer {
  private services = new Map<string, any>();
  private factories = new Map<string, () => any>();

  register<T>(name: string, factory: () => T): void {
    this.factories.set(name, factory);
  }

  get<T>(name: string): T {
    if (this.services.has(name)) {
      return this.services.get(name);
    }

    const factory = this.factories.get(name);
    if (!factory) {
      throw new Error(`Service ${name} not found`);
    }

    const instance = factory();
    this.services.set(name, instance);
    return instance;
  }
}

/** 使用範例 */
const container = new DIContainer();

// 註冊服務
container.register('database', () => new MySQLDatabase());
container.register('userService', () => new UserService(container.get('database')));

// 使用服務
const userService = container.get<UserService>('userService');
```

<br />

## 測試中的 DIP 應用

### 模擬物件的使用

```typescript
/** 測試用的模擬實作 */
class MockDatabase implements DatabaseInterface {
  private data = new Map<string, string>();

  save(data: string): void {
    this.data.set('test_key', data);
  }

  find(id: string): string {
    return this.data.get(id) || 'not found';
  }

  /** 測試輔助方法 */
  getSavedData(): string | undefined {
    return this.data.get('test_key');
  }
}

/** 單元測試 */
class UserServiceTest {
  testCreateUser(): void {
    /** 安排 */
    const mockDb = new MockDatabase();
    const userService = new UserService(mockDb);

    /** 執行 */
    userService.createUser('Charmy');

    /** 驗證 */
    const savedData = mockDb.getSavedData();
    console.assert(savedData === 'processed: Charmy');
  }
}
```

<br />

## 最佳實踐

### 定義清晰的介面

```typescript
/** 好的做法：介面職責單一且清晰 */
interface EmailSender {
  sendEmail(to: string, subject: string, body: string): Promise<void>;
}

interface SMSSender {
  sendSMS(phoneNumber: string, message: string): Promise<void>;
}

/** 避免：介面過於龐大 */
interface CommunicationService {
  sendEmail(to: string, subject: string, body: string): Promise<void>;
  sendSMS(phoneNumber: string, message: string): Promise<void>;
  sendPushNotification(deviceId: string, message: string): Promise<void>;
  sendSlackMessage(channel: string, message: string): Promise<void>;
}
```

### 避免服務定位器模式

```typescript
/** 避免：服務定位器模式 */
class BadUserService {
  createUser(userData: string): void {
    const database = ServiceLocator.get('database'); // 隱藏依賴
    database.save(userData);
  }
}

/** 好的做法：明確的依賴注入 */
class GoodUserService {
  constructor(private database: DatabaseInterface) {} // 明確的依賴

  createUser(userData: string): void {
    this.database.save(userData);
  }
}
```

### 使用工廠模式

```typescript
interface DatabaseFactory {
  createDatabase(type: string): DatabaseInterface;
}

class DatabaseFactoryImpl implements DatabaseFactory {
  createDatabase(type: string): DatabaseInterface {
    switch (type) {
      case 'mysql':
        return new MySQLDatabase();
      case 'mongo':
        return new MongoDatabase();
      default:
        throw new Error(`Unknown database type: ${type}`);
    }
  }
}

class UserService {
  private database: DatabaseInterface;

  constructor(databaseFactory: DatabaseFactory, dbType: string) {
    this.database = databaseFactory.createDatabase(dbType);
  }
}
```

<br />

## 常見誤區

### 過度抽象

```typescript
/** 過度抽象的例子 */
interface StringProcessor {
  process(input: string): string;
}

class UpperCaseProcessor implements StringProcessor {
  process(input: string): string {
    return input.toUpperCase();
  }
}

/** 更合理的做法 */
class StringUtils {
  static toUpperCase(input: string): string {
    return input.toUpperCase();
  }
}
```

### 循環依賴

```typescript
/** 避免：循環依賴 */
class UserService {
  constructor(private orderService: OrderService) {}
}

class OrderService {
  constructor(private userService: UserService) {} // 循環依賴
}

/** 解決方案：引入中介者或事件系統 */
interface EventBus {
  publish(event: string, data: any): void;
  subscribe(event: string, handler: (data: any) => void): void;
}

class UserService {
  constructor(private eventBus: EventBus) {}

  /** 建立使用者 */
  createUser(userData: any): void {
    this.eventBus.publish('user.created', userData);
  }
}

class OrderService {
  constructor(private eventBus: EventBus) {
    this.eventBus.subscribe('user.created', this.handleUserCreated.bind(this));
  }

  private handleUserCreated(userData: any): void {
    // 處理使用者建立事件
  }
}
```

<br />

## 與其他 SOLID 原則的關係

- 單一職責原則 (SRP)：DIP 促進職責分離，每個類別專注於自己的職責

- 開放封閉原則 (OCP)：透過抽象，系統對擴展開放，對修改封閉

- 里氏替換原則 (LSP)：DIP 確保抽象的實作可以互相替換

- 介面隔離原則 (ISP)：DIP 鼓勵使用小而專注的介面

<br />

## 總結

DIP 是實現鬆散耦合系統的關鍵原則，遵循 DIP 能夠

- 提高系統靈活性：可以輕鬆替換不同的實作

- 增強可測試性：可以注入模擬物件進行測試

- 降低耦合度：模組間依賴關係更加鬆散

- 提升可維護性：修改實作不會影響使用該功能的程式碼

- 支援擴展性：新增功能不需要修改現有程式碼

- 促進重複使用：抽象介面可以在不同場景中重複使用

### 注意：依賴於抽象，而不是具體實作。

當發現高層模組直接依賴低層模組的具體實作時，就應該考慮引入抽象層，透過依賴注入來實現依賴反轉。
