# 里氏替換原則 (Liskov Substitution Principle)

在物件導向程式設計中，繼承是實現程式碼重用和多型的重要機制。

然而，不當的繼承設計往往會導致子類別無法正確替換父類別，破壞程式的穩定性和可靠性。

為了確保繼承關係的正確性，物件導向設計提出了里氏替換原則 (Liskov Substitution Principle，簡稱：LSP)。

<br />

## LSP 的核心理念

### LSP 的定義是：子類別物件應該能夠替換父類別物件，而不會改變程式的正確性。

也就是說，當使用子類別的實例替換父類別的實例時，程式應該能夠正常運作，不會產生意外的行為或錯誤。這個原則確保了繼承關係的語義一致性，讓多型能夠安全使用。

簡單來說，子類別必須能夠完全替代父類別，而不破壞原有的功能。

<br />

## LSP 的核心概念

- 行為一致性：子類別的行為應該與父類別保持一致

- 契約遵守：子類別必須遵守父類別定義的契約

- 前置條件不能加強：子類別不能要求更嚴格的輸入條件

- 後置條件不能削弱：子類別必須提供至少與父類別相同的輸出保證

- 不變條件維持：子類別必須維持父類別的不變條件

<br />

## LSP 的優缺點

### 優點

- 提高程式穩定性：確保多型使用時不會產生意外行為

- 增強可替換性：任何使用父類別的地方都可以安全使用子類別

- 提升程式碼重用性：正確的繼承關係讓程式碼更容易重用

- 降低維護成本：遵循 LSP 的設計更容易理解和維護

- 支援開放封閉原則：可以安全新增新的子類別而不影響現有程式碼

- 提高測試效率：父類別的測試可以直接應用於子類別

### 缺點

- 設計複雜度增加：需要仔細考慮繼承關係的設計

- 限制實作彈性：子類別的實作受到父類別契約的約束

- 學習成本較高：需要深入理解契約設計和行為一致性

- 過度抽象風險：可能導致不必要的抽象層級

- 效能考量：嚴格的契約檢查可能影響執行效率

- 重構困難：修改父類別契約可能影響所有子類別

<br />

## 違反 LSP 的問題

- 執行時錯誤：子類別替換父類別時可能產生異常

- 行為不一致：相同的操作在不同子類別中產生不同結果

- 契約違反：子類別無法滿足父類別的承諾

- 多型失效：無法安全使用多型特性

<br />

## 實作範例

依 TypeScript 為例

### 違反 LSP 的範例

```typescript
/** 違反 LSP：Rectangle 和 Square 的關係不符合替換原則 */
class Rectangle {
  protected width: number;
  protected height: number;

  constructor(width: number, height: number) {
    this.width = width;
    this.height = height;
  }

  setWidth(width: number): void {
    this.width = width;
  }

  setHeight(height: number): void {
    this.height = height;
  }

  getWidth(): number {
    return this.width;
  }

  getHeight(): number {
    return this.height;
  }

  getArea(): number {
    return this.width * this.height;
  }
}

class Square extends Rectangle {
  constructor(side: number) {
    super(side, side);
  }

  /** 違反 LSP：改變了父類別的行為 */
  setWidth(width: number): void {
    this.width = width;
    this.height = width; // 強制保持正方形
  }

  setHeight(height: number): void {
    this.width = height;
    this.height = height; // 強制保持正方形
  }
}

/** 測試函數顯示問題 */
function testRectangle(rectangle: Rectangle): void {
  rectangle.setWidth(5);
  rectangle.setHeight(4);

  // 期望面積是 20，但若傳入 Square 實例，面積會是 16
  console.log(`Expected area: 20, Actual area: ${rectangle.getArea()}`);
}

const rectangle = new Rectangle(3, 3);
const square = new Square(3);

testRectangle(rectangle); // 正常：面積 = 20
testRectangle(square);    // 異常：面積 = 16，違反期望
```

### 遵循 LSP 的範例

```typescript
/** 遵循 LSP：使用抽象基類定義共同契約 */
abstract class Shape {
  abstract getArea(): number;
  abstract getPerimeter(): number;
}

class Rectangle extends Shape {
  private width: number;
  private height: number;

  constructor(width: number, height: number) {
    super();
    this.width = width;
    this.height = height;
  }

  setWidth(width: number): void {
    this.width = width;
  }

  setHeight(height: number): void {
    this.height = height;
  }

  getWidth(): number {
    return this.width;
  }

  getHeight(): number {
    return this.height;
  }

  getArea(): number {
    return this.width * this.height;
  }

  getPerimeter(): number {
    return 2 * (this.width + this.height);
  }
}

class Square extends Shape {
  private side: number;

  constructor(side: number) {
    super();
    this.side = side;
  }

  setSide(side: number): void {
    this.side = side;
  }

  getSide(): number {
    return this.side;
  }

  getArea(): number {
    return this.side * this.side;
  }

  getPerimeter(): number {
    return 4 * this.side;
  }
}

/** 使用範例：所有 Shape 子類別都可以安全替換 */
function calculateTotalArea(shapes: Shape[]): number {
  return shapes.reduce((total, shape) => total + shape.getArea(), 0);
}

const shapes: Shape[] = [
  new Rectangle(5, 4),
  new Square(3),
  new Rectangle(2, 6)
];

console.log(`Total area: ${calculateTotalArea(shapes)}`);
```

### 另一個遵循 LSP 的範例：鳥類繼承

```typescript
/** 遵循 LSP：正確的鳥類繼承設計 */
abstract class Bird {
  abstract makeSound(): string;
  abstract move(): string;
}

class FlyingBird extends Bird {
  makeSound(): string {
    return "chirp";
  }

  move(): string {
    return "flying";
  }

  fly(): string {
    return "soaring through the sky";
  }
}

class FlightlessBird extends Bird {
  makeSound(): string {
    return "squawk";
  }

  move(): string {
    return "walking";
  }

  walk(): string {
    return "walking on the ground";
  }
}

class Sparrow extends FlyingBird {
  makeSound(): string {
    return "tweet";
  }
}

class Penguin extends FlightlessBird {
  makeSound(): string {
    return "honk";
  }

  swim(): string {
    return "swimming in water";
  }
}

/** 使用範例：所有 Bird 子類別都遵循相同契約 */
function describeBird(bird: Bird): string {
  return `This bird says "${bird.makeSound()}" and moves by ${bird.move()}`;
}

const birds: Bird[] = [
  new Sparrow(),
  new Penguin()
];

birds.forEach(bird => {
  console.log(describeBird(bird));
});
```

<br />

## 其他語言範例

### Java 範例

```java
public abstract class Vehicle {
    protected String brand;
    protected int maxSpeed;

    public Vehicle(String brand, int maxSpeed) {
        this.brand = brand;
        this.maxSpeed = maxSpeed;
    }

    public abstract void start();
    public abstract void stop();

    public String getBrand() {
        return brand;
    }

    public int getMaxSpeed() {
        return maxSpeed;
    }
}

public class Car extends Vehicle {
    private boolean engineRunning = false;

    public Car(String brand, int maxSpeed) {
        super(brand, maxSpeed);
    }

    @Override
    public void start() {
        if (!engineRunning) {
            engineRunning = true;
            System.out.println("Car engine started");
        }
    }

    @Override
    public void stop() {
        if (engineRunning) {
            engineRunning = false;
            System.out.println("Car engine stopped");
        }
    }
}

public class Bicycle extends Vehicle {
    private boolean inMotion = false;

    public Bicycle(String brand) {
        super(brand, 30); // 腳踏車最高速度約 30 km/h
    }

    @Override
    public void start() {
        inMotion = true;
        System.out.println("Started pedaling");
    }

    @Override
    public void stop() {
        inMotion = false;
        System.out.println("Stopped pedaling");
    }
}
```

### Python 範例

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

    @abstractmethod
    def get_processing_fee(self, amount: float) -> float:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"Processing credit card payment of ${amount}")
        return True

    def get_processing_fee(self, amount: float) -> float:
        return amount * 0.03 # 3% 手續費

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"Processing PayPal payment of ${amount}")
        return True

    def get_processing_fee(self, amount: float) -> float:
        return amount * 0.025 # 2.5% 手續費

class BankTransferProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"Processing bank transfer of ${amount}")
        return True

    def get_processing_fee(self, amount: float) -> float:
        return 5.0 # 固定手續費 $5

def process_order_payment(processor: PaymentProcessor, amount: float):
    fee = processor.get_processing_fee(amount)
    total = amount + fee

    if processor.process_payment(total):
        print(f"Payment successful. Fee: ${fee}, Total: ${total}")
    else:
        print("Payment failed")
```

<br />

## 實際應用場景

### 檔案處理系統

```typescript
/** 遵循 LSP 的檔案處理器設計 */
abstract class FileProcessor {
  abstract process(content: string): string;
  abstract getSupportedExtensions(): string[];

  canProcess(filename: string): boolean {
    const extension = filename.split('.').pop()?.toLowerCase();
    return this.getSupportedExtensions().includes(extension || '');
  }
}

class TextFileProcessor extends FileProcessor {
  process(content: string): string {
    return content.trim().toUpperCase();
  }

  getSupportedExtensions(): string[] {
    return ['txt', 'md'];
  }
}

class JsonFileProcessor extends FileProcessor {
  process(content: string): string {
    try {
      const parsed = JSON.parse(content);
      return JSON.stringify(parsed, null, 2);
    } catch (error) {
      throw new Error('Invalid JSON format');
    }
  }

  getSupportedExtensions(): string[] {
    return ['json'];
  }
}

class CsvFileProcessor extends FileProcessor {
  process(content: string): string {
    const lines = content.split('\n');
    return lines.map(line => line.split(',').join('|')).join('\n');
  }

  getSupportedExtensions(): string[] {
    return ['csv'];
  }
}

/** 使用範例 */
class FileProcessingService {
  private processors: FileProcessor[];

  constructor() {
    this.processors = [
      new TextFileProcessor(),
      new JsonFileProcessor(),
      new CsvFileProcessor()
    ];
  }

  processFile(filename: string, content: string): string {
    const processor = this.processors.find(p => p.canProcess(filename));

    if (!processor) {
      throw new Error(`No processor found for file: ${filename}`);
    }

    return processor.process(content);
  }
}
```

### 資料庫連接器

```typescript
/** 遵循 LSP 的資料庫連接器 */
interface DatabaseConnection {
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  query(sql: string): Promise<any[]>;
  isConnected(): boolean;
}

class MySQLConnection implements DatabaseConnection {
  private connected = false;

  async connect(): Promise<void> {
    // MySQL 連接實作
    this.connected = true;
    console.log('Connected to MySQL');
  }

  async disconnect(): Promise<void> {
    this.connected = false;
    console.log('Disconnected from MySQL');
  }

  async query(sql: string): Promise<any[]> {
    if (!this.connected) {
      throw new Error('Not connected to database');
    }
    // MySQL 查詢實作
    return [];
  }

  isConnected(): boolean {
    return this.connected;
  }
}

class PostgreSQLConnection implements DatabaseConnection {
  private connected = false;

  async connect(): Promise<void> {
    // PostgreSQL 連接實作
    this.connected = true;
    console.log('Connected to PostgreSQL');
  }

  async disconnect(): Promise<void> {
    this.connected = false;
    console.log('Disconnected from PostgreSQL');
  }

  async query(sql: string): Promise<any[]> {
    if (!this.connected) {
      throw new Error('Not connected to database');
    }
    // PostgreSQL 查詢實作
    return [];
  }

  isConnected(): boolean {
    return this.connected;
  }
}

/** 使用範例 */
class DatabaseService {
  constructor(private connection: DatabaseConnection) {}

  async executeQuery(sql: string): Promise<any[]> {
    if (!this.connection.isConnected()) {
      await this.connection.connect();
    }

    return await this.connection.query(sql);
  }
}
```

<br />

## 識別 LSP 違反的方法

### 契約檢查法

檢查以下契約是否被遵守

- 前置條件：子類別是否要求更嚴格的輸入？

- 後置條件：子類別是否提供較弱的輸出保證？

- 不變條件：子類別是否維持父類別的不變條件？

### 行為測試法

使用父類別的測試案例測試子類別

- 所有父類別的測試是否都能通過？

- 子類別是否產生意外的副作用？

- 異常處理是否一致？

### 替換測試法

在實際使用中測試替換性

- 將子類別實例替換父類別實例

- 觀察程式行為是否改變

- 檢查是否需要特殊處理

<br />

## 最佳實踐

### 設計契約明確的介面
```typescript
/** 好的做法：明確定義契約 */
interface Stack<T> {
  /** 將元素推入堆疊頂部 */
  push(item: T): void;

  /** 移除並返回堆疊頂部元素，若堆疊為空則拋出異常 */
  pop(): T;

  /** 返回堆疊頂部元素但不移除，若堆疊為空則拋出異常 */
  peek(): T;

  /** 返回堆疊是否為空 */
  isEmpty(): boolean;

  /** 返回堆疊中元素數量 */
  size(): number;
}

class ArrayStack<T> implements Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T {
    if (this.isEmpty()) {
      throw new Error('Stack is empty');
    }
    return this.items.pop()!;
  }

  peek(): T {
    if (this.isEmpty()) {
      throw new Error('Stack is empty');
    }
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  size(): number {
    return this.items.length;
  }
}
```

### 使用組合優於繼承
```typescript
/** 使用組合避免 LSP 問題 */
interface Flyable {
  fly(): string;
}

interface Swimmable {
  swim(): string;
}

class Bird {
  constructor(
    private name: string,
    private flyable?: Flyable,
    private swimmable?: Swimmable
  ) {}

  getName(): string {
    return this.name;
  }

  canFly(): boolean {
    return this.flyable !== undefined;
  }

  canSwim(): boolean {
    return this.swimmable !== undefined;
  }

  fly(): string {
    if (!this.flyable) {
      throw new Error(`${this.name} cannot fly`);
    }
    return this.flyable.fly();
  }

  swim(): string {
    if (!this.swimmable) {
      throw new Error(`${this.name} cannot swim`);
    }
    return this.swimmable.swim();
  }
}

class FlyingAbility implements Flyable {
  fly(): string {
    return "soaring through the sky";
  }
}

class SwimmingAbility implements Swimmable {
  swim(): string {
    return "swimming in water";
  }
}

/** 使用範例 */
const sparrow = new Bird("Sparrow", new FlyingAbility());
const penguin = new Bird("Penguin", undefined, new SwimmingAbility());
const duck = new Bird("Duck", new FlyingAbility(), new SwimmingAbility());
```

### 避免強化前置條件
```typescript
/** 錯誤：子類別強化了前置條件 */
class FileReader {
  readFile(filename: string): string {
    // 父類別接受任何檔名
    return "file content";
  }
}

class SecureFileReader extends FileReader {
  readFile(filename: string): string {
    // 錯誤：要求更嚴格的條件
    if (!filename.endsWith('.txt')) {
      throw new Error('Only .txt files are allowed');
    }
    return super.readFile(filename);
  }
}

/** 正確：使用不同的方法或參數 */
class SecureFileReaderCorrect extends FileReader {
  constructor(private allowedExtensions: string[]) {
    super();
  }

  readFile(filename: string): string {
    if (!this.isAllowedFile(filename)) {
      throw new Error(`File type not allowed: ${filename}`);
    }
    return super.readFile(filename);
  }

  private isAllowedFile(filename: string): boolean {
    const extension = filename.split('.').pop()?.toLowerCase();
    return this.allowedExtensions.includes(extension || '');
  }
}
```

<br />

## 常見誤區

### 混淆 IS-A 關係
```typescript
/** 錯誤：正方形不是矩形的特殊情況 (在程式設計中) */
class Rectangle {
  setWidth(width: number): void { /* ... */ }
  setHeight(height: number): void { /* ... */ }
}

class Square extends Rectangle {
  // 違反 LSP：改變了父類別的行為
}

/** 正確：使用共同的抽象 */
abstract class Shape {
  abstract getArea(): number;
}

class Rectangle extends Shape { /* ... */ }
class Square extends Shape { /* ... */ }
```

### 忽略異常處理一致性
```typescript
/** 錯誤：子類別拋出不同類型的異常 */
class DataProcessor {
  process(data: string): string {
    if (!data) {
      throw new Error('Data is required');
    }
    return data.toUpperCase();
  }
}

class JsonProcessor extends DataProcessor {
  process(data: string): string {
    if (!data) {
      // 錯誤：拋出不同類型的異常
      throw new TypeError('Invalid data type');
    }
    return JSON.stringify(JSON.parse(data));
  }
}

/** 正確：保持異常類型一致 */
class JsonProcessorCorrect extends DataProcessor {
  process(data: string): string {
    if (!data) {
      throw new Error('Data is required'); // 相同的異常類型
    }
    try {
      return JSON.stringify(JSON.parse(data));
    } catch (error) {
      throw new Error('Invalid JSON format');
    }
  }
}
```

### 破壞不變條件
```typescript
/** 錯誤：子類別破壞了父類別的不變條件 */
class BankAccount {
  protected balance: number;

  constructor(initialBalance: number) {
    this.balance = initialBalance;
  }

  withdraw(amount: number): void {
    if (amount > this.balance) {
      throw new Error('Insufficient funds');
    }
    this.balance -= amount;
  }

  getBalance(): number {
    return this.balance;
  }
}

class OverdraftAccount extends BankAccount {
  withdraw(amount: number): void {
    // 錯誤：允許負餘額，破壞了父類別的不變條件
    this.balance -= amount;
  }
}

/** 正確：維持不變條件或明確定義新的契約 */
class OverdraftAccountCorrect extends BankAccount {
  private overdraftLimit: number;

  constructor(initialBalance: number, overdraftLimit: number) {
    super(initialBalance);
    this.overdraftLimit = overdraftLimit;
  }

  withdraw(amount: number): void {
    if (amount > this.balance + this.overdraftLimit) {
      throw new Error('Overdraft limit exceeded');
    }
    this.balance -= amount;
  }
}
```

<br />

## 與其他 SOLID 原則的關係

- 單一職責原則 (SRP)：LSP 確保繼承關係中每個類別的職責清晰

- 開放封閉原則 (OCP)：LSP 使得新增子類別時不會破壞現有程式碼

- 介面隔離原則 (ISP)：LSP 有助於設計更精確的介面契約

- 依賴反轉原則 (DIP)：LSP 確保抽象和實作之間的正確關係

<br />

## 總結

LSP 是確保繼承關係正確性的重要原則，遵循 LSP 能夠

- 提高程式穩定性：確保多型使用的安全性

- 增強可維護性：正確的繼承關係更容易理解和修改

- 提升程式碼重用性：子類別可以安全替換父類別

- 支援擴展性：可以安全新增新的子類別

- 降低耦合度：清晰的契約定義減少類別間的依賴

### 注意：子類別必須能夠替換父類別而不改變程式的正確性。

當設計繼承關係時，應該確保子類別完全遵守父類別的契約，包括前置條件、後置條件和不變條件。
