# 單一職責原則 (Single Responsibility Principle)

在現代軟體開發中，程式碼的可維護性與可擴充性是衡量系統品質的重要指標。

隨著專案規模增加、功能逐漸複雜，若缺乏良好的設計原則，類別容易承擔過多職責，導致程式結構混亂、維護困難。

為了應對這個問題，物件導向設計提出了單一職責原則 (Single Responsibility Principle，簡稱：SRP)。

<br />

## SRP 的核心理念

### SRP 的定義是：一個類別 (Class) 應該只有一個引起變化的原因。

也就是說，每個類別應該只專注於一件事情。當修改某個類別時，應該能明確指出是哪一種「職責」導致這個類別需要改變。若一個類別同時負責多項不同的功能，那麼當任何一個功能發生變更時，都可能影響到這個類別的其他部分，使得系統變得脆弱而難以維護。

簡單來說，每個類別只負責一項功能，當需要修改某個功能時，只需要修改對應的類別。

<br />

## SRP 的核心概念

- 職責分離：將不同的職責分配給不同的類別

- 高內聚：類別內部的元素應該緊密相關

- 低耦合：類別之間的依賴關係應該最小化

- 易於維護：當需求變更時，只需修改特定的類別

<br />

## SRP 的優缺點

### 優點

- 提高可維護性：每個類別職責單一，修改時影響範圍明確且有限

- 增強可測試性：職責分離使得單元測試更容易編寫和執行

- 提升程式碼重用性：專注的類別更容易在不同場景中重複使用

- 降低耦合度：類別間依賴關係清晰，減少意外的副作用

- 便於團隊協作：不同開發者可以並行開發不同職責的類別

- 符合開放封閉原則：新增功能時不需要修改現有類別

### 缺點

- 增加類別數量：可能導致專案中類別數量大幅增加

- 提高複雜度：需要管理更多的類別和之間的關係

- 過度設計風險：可能導致不必要的抽象和過度工程化

- 學習成本：新團隊成員需要時間理解類別間的協作關係

- 效能考量：過多的物件創建和方法調用可能影響效能

- 判斷困難：如何定義「單一職責」有時並不明確

<br />

## 違反 SRP 的問題

- 修改風險：修改一個功能可能影響其他功能

- 測試困難：需要同時測試多個不相關的功能

- 程式碼複雜：類別變得龐大且難以理解

- 重複使用困難：無法單獨使用某個功能

<br />

## 實作範例

依 TypeScript 為例

### 違反 SRP 的範例

```typescript
/** 違反 SRP：User 類別承擔了多個職責 */
class User {
  private name: string;
  private email: string;

  constructor(name: string, email: string) {
    this.name = name;
    this.email = email;
  }

  /** 職責 1：使用者資料管理 */
  getName(): string {
    return this.name;
  }

  getEmail(): string {
    return this.email;
  }

  /** 職責 2：資料驗證 */
  validateEmail(): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(this.email);
  }

  /** 職責 3：資料持久化 */
  saveToDatabase(): void {
    // 儲存到資料庫的程式碼
    console.log(`Saving user ${this.name} to database`);
  }

  /** 職責 4：通知功能 */
  sendWelcomeEmail(): void {
    // 發送歡迎郵件的程式碼
    console.log(`Sending welcome email to ${this.email}`);
  }
}
```

### 遵循 SRP 的範例

```typescript
/** 職責 1：使用者資料管理 */
class User {
  private name: string;
  private email: string;

  constructor(name: string, email: string) {
    this.name = name;
    this.email = email;
  }

  getName(): string {
    return this.name;
  }

  getEmail(): string {
    return this.email;
  }
}

/** 職責 2：資料驗證 */
class UserValidator {
  validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  validateName(name: string): boolean {
    return name.length > 0 && name.length <= 50;
  }
}

/** 職責 3：資料持久化 */
class UserRepository {
  save(user: User): void {
    // 儲存到資料庫的程式碼
    console.log(`Saving user ${user.getName()} to database`);
  }

  findByEmail(email: string): User | null {
    // 從資料庫查詢使用者的程式碼
    return null;
  }
}

/** 職責 4：通知功能 */
class EmailService {
  sendWelcomeEmail(user: User): void {
    // 發送歡迎郵件的程式碼
    console.log(`Sending welcome email to ${user.getEmail()}`);
  }

  sendPasswordResetEmail(user: User): void {
    // 發送密碼重設郵件的程式碼
    console.log(`Sending password reset email to ${user.getEmail()}`);
  }
}

/** 使用範例 */
class UserService {
  private userValidator: UserValidator;
  private userRepository: UserRepository;
  private emailService: EmailService;

  constructor() {
    this.userValidator = new UserValidator();
    this.userRepository = new UserRepository();
    this.emailService = new EmailService();
  }

  createUser(name: string, email: string): User | null {
    if (!this.userValidator.validateName(name) || !this.userValidator.validateEmail(email)) {
      return null;
    }

    const user = new User(name, email);
    this.userRepository.save(user);
    this.emailService.sendWelcomeEmail(user);

    return user;
  }
}
```

<br />

## 其他語言範例

### Java 範例

```java
public class User {
    private String name;
    private String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }
}

public class UserValidator {
    public boolean validateEmail(String email) {
        return email.matches("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
    }

    public boolean validateName(String name) {
        return name != null && name.length() > 0 && name.length() <= 50;
    }
}

public class UserRepository {
    public void save(User user) {
        System.out.println("Saving user " + user.getName() + " to database");
    }

    public User findByEmail(String email) {
        // 資料庫查詢實作
        return null;
    }
}
```

### Python 範例

```python
class User:
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    def get_name(self) -> str:
        return self._name

    def get_email(self) -> str:
        return self._email

class UserValidator:
    def validate_email(self, email: str) -> bool:
        import re
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(pattern, email))

    def validate_name(self, name: str) -> bool:
        return len(name) > 0 and len(name) <= 50

class UserRepository:
    def save(self, user: User) -> None:
        print(f"Saving user {user.get_name()} to database")

    def find_by_email(self, email: str) -> User:
        # 資料庫查詢實作
        return None
```

<br />

## 實際應用場景

### 電商系統中的訂單處理

```typescript
/** 違反 SRP */
class Order {
  calculateTotal(): number { /* ... */ }
  validateOrder(): boolean { /* ... */ }
  saveToDatabase(): void { /* ... */ }
  sendConfirmationEmail(): void { /* ... */ }
  generateInvoice(): string { /* ... */ }
}

/** 遵循 SRP */
class Order {
  calculateTotal(): number { /* ... */ }
}

class OrderValidator {
  validate(order: Order): boolean { /* ... */ }
}

class OrderRepository {
  save(order: Order): void { /* ... */ }
}

class EmailService {
  sendConfirmation(order: Order): void { /* ... */ }
}

class InvoiceGenerator {
  generate(order: Order): string { /* ... */ }
}
```

### 檔案處理系統

```typescript
/** 遵循 SRP 的檔案處理 */
class FileReader {
  read(filePath: string): string {
    // 讀取檔案內容
    return "file content";
  }
}

class FileWriter {
  write(filePath: string, content: string): void {
    // 寫入檔案內容
  }
}

class FileValidator {
  validatePath(filePath: string): boolean {
    // 驗證檔案路徑
    return true;
  }

  validateSize(fileSize: number): boolean {
    // 驗證檔案大小
    return fileSize <= 1024 * 1024; // 1MB
  }
}

class FileCompressor {
  compress(content: string): string {
    // 壓縮檔案內容
    return content;
  }
}
```

<br />

## 識別職責的方法

### 問題導向法

詢問以下問題來識別職責

- 這個類別為什麼需要改變？

- 有多少個不同的原因會導致這個類別修改？

- 這個類別的方法是否都服務於同一個目標？

### 角色分析法
從不同使用者角色的角度分析

- 哪些角色會使用這個類別？

- 不同角色對這個類別有什麼不同的期望？

### 變化軸分析法

分析可能的變化來源

- 業務規則變化

- 資料格式變化

- 外部系統介面變化

- 效能需求變化

<br />

## 最佳實踐

### 保持類別小而專注
```typescript
/** 好的做法：專注於單一職責 */
class EmailValidator {
  validate(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

/** 避免：承擔過多職責 */
class Validator {
  validateEmail(email: string): boolean { /* ... */ }
  validatePhone(phone: string): boolean { /* ... */ }
  validateAddress(address: string): boolean { /* ... */ }
  validateCreditCard(card: string): boolean { /* ... */ }
}
```

### 使用組合而非繼承
```typescript
class UserService {
  private validator: UserValidator;
  private repository: UserRepository;
  private emailService: EmailService;

  constructor(
    validator: UserValidator,
    repository: UserRepository,
    emailService: EmailService
  ) {
    this.validator = validator;
    this.repository = repository;
    this.emailService = emailService;
  }
}
```

### 明確的介面定義
```typescript
interface UserRepositoryInterface {
  save(user: User): void;
  findById(id: string): User | null;
  findByEmail(email: string): User | null;
}

interface EmailServiceInterface {
  sendWelcomeEmail(user: User): void;
  sendPasswordResetEmail(user: User): void;
}
```

<br />

## 常見誤區

### 過度分割
```typescript
/** 過度分割的例子 */
class UserName {
  constructor(private name: string) {}
  getName(): string { return this.name; }
}

class UserEmail {
  constructor(private email: string) {}
  getEmail(): string { return this.email; }
}

/** 合理的做法 */
class User {
  constructor(private name: string, private email: string) {}
  getName(): string { return this.name; }
  getEmail(): string { return this.email; }
}
```

### 忽略內聚性
```typescript
/** 錯誤：將相關功能分離 */
class UserFirstName {
  validate(firstName: string): boolean { /* ... */ }
}

class UserLastName {
  validate(lastName: string): boolean { /* ... */ }
}

/** 正確：保持相關功能的內聚性 */
class UserNameValidator {
  validateFirstName(firstName: string): boolean { /* ... */ }
  validateLastName(lastName: string): boolean { /* ... */ }
  validateFullName(firstName: string, lastName: string): boolean { /* ... */ }
}
```

<br />

## 與其他 SOLID 原則的關係

- 開放封閉原則 (OCP)：SRP 使得擴展功能時不需要修改現有類別

- 里氏替換原則 (LSP)：SRP 的類別更容易實現正確的繼承關係

- 介面隔離原則 (ISP)：SRP 有助於設計更小、更專注的介面

- 依賴反轉原則 (DIP)：職責分離使得依賴關係更加清晰

<br />

## 總結

SRP 是 SOLID 原則的基礎，遵循 SRP 能夠

- 提高程式碼可讀性：每個類別的目的明確

- 降低維護成本：修改影響範圍有限

- 增強可測試性：每個類別都可以獨立測試

- 提升重複使用性：小而專注的類別更容易重複使用

- 減少耦合度：類別之間的依賴關係更加清晰

### 注意：一個類別 (Class) 應該只有一個改變的理由。

當發現一個類別有多個改變的原因時，就應該考慮將其拆分成多個更小、更專注的類別。
