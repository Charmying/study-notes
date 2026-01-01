# 開放封閉原則 (Open Closed Principle)

在軟體開發過程中，需求變更是不可避免的現實。

隨著業務發展與功能擴展，系統必須能夠適應新的需求，但同時也要保持現有程式碼的穩定性。

為了在擴展性與穩定性之間取得平衡，物件導向設計提出了開放封閉原則 (Open Closed Principle，簡稱：OCP)。

<br />

## OCP 的核心理念

### OCP 的定義是：軟體實體 (類別、模組、函數等) 應該對擴展開放，對修改封閉。

也就是說，當需要新增功能時，應該透過擴展現有程式碼來實現，而不是修改已經存在且運作正常的程式碼。這樣可以確保新功能的加入不會破壞現有的功能，同時讓系統更容易維護和測試。

簡單來說，透過抽象化和多型來實現功能擴展，避免直接修改現有程式碼。

<br />

## OCP 的核心概念

- 對擴展開放：可以透過新增程式碼來擴展功能

- 對修改封閉：不修改現有的、已測試的程式碼

- 抽象化設計：使用介面和抽象類別來定義契約

- 多型應用：透過多型來實現不同的行為

<br />

## OCP 的優缺點

### 優點

- 提高系統穩定性：新功能不會影響現有功能的運作

- 降低維護風險：避免修改已測試且穩定的程式碼

- 增強可擴展性：透過抽象化機制輕鬆新增功能

- 提升程式碼重用性：抽象介面可以在多個場景中重複使用

- 便於並行開發：不同開發者可以同時開發新功能而不互相干擾

- 簡化測試工作：新功能可以獨立測試，不需要重新測試所有相關功能

- 促進良好設計：鼓勵使用抽象化和設計模式

### 缺點

- 增加設計複雜度：需要預先設計抽象介面和架構

- 提高學習成本：開發者需要理解抽象化和多型概念

- 可能過度設計：為了遵循 OCP 可能導致不必要的抽象化

- 效能考量：多型和抽象化可能帶來額外的效能開銷

- 預測困難：很難準確預測未來的擴展需求

- 增加程式碼量：需要更多的介面和抽象類別

- 除錯複雜：抽象化層次增加可能使除錯變得困難

<br />

## 違反 OCP 的問題

- 修改風險：每次新增功能都需要修改現有程式碼

- 測試負擔：需要重新測試所有相關功能

- 程式碼脆弱：修改可能引入新的錯誤

- 維護困難：程式碼變得越來越複雜難懂

<br />

## 實作範例

依 TypeScript 為例

### 違反 OCP 的範例

```typescript
/** 違反 OCP：每次新增形狀都需要修改現有程式碼 */
class AreaCalculator {
  calculateArea(shapes: any[]): number {
    let totalArea = 0;

    for (const shape of shapes) {
      if (shape.type === 'rectangle') {
        totalArea += shape.width * shape.height;
      } else if (shape.type === 'circle') {
        totalArea += Math.PI * shape.radius * shape.radius;
      } else if (shape.type === 'triangle') {
        /** 新增三角形需要修改這個方法 */
        totalArea += 0.5 * shape.base * shape.height;
      }
      // 每次新增形狀都需要在這裡加入新的 if-else
    }

    return totalArea;
  }
}

class Rectangle {
  constructor(public width: number, public height: number, public type = 'rectangle') {}
}

class Circle {
  constructor(public radius: number, public type = 'circle') {}
}
```

### 遵循 OCP 的範例

```typescript
/** 遵循 OCP：透過介面和多型實現擴展 */
interface Shape {
  calculateArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}

  calculateArea(): number {
    return this.width * this.height;
  }
}

class Circle implements Shape {
  constructor(private radius: number) {}

  calculateArea(): number {
    return Math.PI * this.radius * this.radius;
  }
}

/** 新增形狀不需要修改現有程式碼 */
class Triangle implements Shape {
  constructor(private base: number, private height: number) {}

  calculateArea(): number {
    return 0.5 * this.base * this.height;
  }
}

class AreaCalculator {
  calculateArea(shapes: Shape[]): number {
    return shapes.reduce((total, shape) => total + shape.calculateArea(), 0);
  }
}

/** 使用範例 */
const calculator = new AreaCalculator();
const shapes: Shape[] = [
  new Rectangle(5, 10),
  new Circle(3),
  new Triangle(4, 6)
];

console.log(calculator.calculateArea(shapes)); // 計算總面積
```

<br />

## 進階範例：支付系統

### 違反 OCP 的支付處理

```typescript
/** 違反 OCP：每次新增支付方式都需要修改 */
class PaymentProcessor {
  processPayment(amount: number, method: string, details: any): boolean {
    if (method === 'credit_card') {
      return this.processCreditCard(amount, details.cardNumber, details.cvv);
    } else if (method === 'paypal') {
      return this.processPayPal(amount, details.email);
    } else if (method === 'bank_transfer') {
      // 新增銀行轉帳需要修改這個方法
      return this.processBankTransfer(amount, details.accountNumber);
    }
    return false;
  }

  private processCreditCard(amount: number, cardNumber: string, cvv: string): boolean {
    console.log(`Processing credit card payment: $${amount}`);
    return true;
  }

  private processPayPal(amount: number, email: string): boolean {
    console.log(`Processing PayPal payment: $${amount}`);
    return true;
  }

  private processBankTransfer(amount: number, accountNumber: string): boolean {
    console.log(`Processing bank transfer: $${amount}`);
    return true;
  }
}
```

### 遵循 OCP 的支付處理

```typescript
/** 遵循 OCP：透過策略模式實現擴展 */
interface PaymentMethod {
  process(amount: number): boolean;
}

class CreditCardPayment implements PaymentMethod {
  constructor(private cardNumber: string, private cvv: string) {}

  process(amount: number): boolean {
    console.log(`Processing credit card payment: $${amount}`);
    // 信用卡處理流程
    return true;
  }
}

class PayPalPayment implements PaymentMethod {
  constructor(private email: string) {}

  process(amount: number): boolean {
    console.log(`Processing PayPal payment: $${amount}`);
    // PayPal 處理流程
    return true;
  }
}

/** 新增支付方式不需要修改現有程式碼 */
class BankTransferPayment implements PaymentMethod {
  constructor(private accountNumber: string) {}

  process(amount: number): boolean {
    console.log(`Processing bank transfer: $${amount}`);
    // 銀行轉帳處理流程
    return true;
  }
}

class CryptocurrencyPayment implements PaymentMethod {
  constructor(private walletAddress: string) {}

  process(amount: number): boolean {
    console.log(`Processing cryptocurrency payment: $${amount}`);
    // 加密貨幣處理流程
    return true;
  }
}

class PaymentProcessor {
  processPayment(amount: number, paymentMethod: PaymentMethod): boolean {
    return paymentMethod.process(amount);
  }
}

/** 使用範例 */
const processor = new PaymentProcessor();
const creditCard = new CreditCardPayment('1234-5678-9012-3456', '123');
const paypal = new PayPalPayment('user@example.com');
const bankTransfer = new BankTransferPayment('ACC-123456789');

processor.processPayment(100, creditCard);
processor.processPayment(50, paypal);
processor.processPayment(200, bankTransfer);
```

<br />

## 其他語言範例

### Java 範例

```java
public interface Shape {
    double calculateArea();
}

public class Rectangle implements Shape {
    private double width;
    private double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double calculateArea() {
        return width * height;
    }
}

public class Circle implements Shape {
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

public class AreaCalculator {
    public double calculateTotalArea(List<Shape> shapes) {
        return shapes.stream()
                .mapToDouble(Shape::calculateArea)
                .sum();
    }
}
```

### Python 範例

```python
from abc import ABC, abstractmethod
from typing import List

class Shape(ABC):
    @abstractmethod
    def calculate_area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    def calculate_area(self) -> float:
        return self._width * self._height

class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius

    def calculate_area(self) -> float:
        import math
        return math.pi * self._radius ** 2

class AreaCalculator:
    def calculate_total_area(self, shapes: List[Shape]) -> float:
        return sum(shape.calculate_area() for shape in shapes)
```

<br />

## 實際應用場景

### 通知系統

```typescript
/** 遵循 OCP 的通知系統 */
interface NotificationChannel {
  send(message: string, recipient: string): boolean;
}

class EmailNotification implements NotificationChannel {
  send(message: string, recipient: string): boolean {
    console.log(`Sending email to ${recipient}: ${message}`);
    return true;
  }
}

class SMSNotification implements NotificationChannel {
  send(message: string, recipient: string): boolean {
    console.log(`Sending SMS to ${recipient}: ${message}`);
    return true;
  }
}

class PushNotification implements NotificationChannel {
  send(message: string, recipient: string): boolean {
    console.log(`Sending push notification to ${recipient}: ${message}`);
    return true;
  }
}

/** 新增通知方式不需要修改現有程式碼 */
class SlackNotification implements NotificationChannel {
  send(message: string, recipient: string): boolean {
    console.log(`Sending Slack message to ${recipient}: ${message}`);
    return true;
  }
}

class NotificationService {
  private channels: NotificationChannel[] = [];

  addChannel(channel: NotificationChannel): void {
    this.channels.push(channel);
  }

  sendNotification(message: string, recipient: string): void {
    this.channels.forEach(channel => {
      channel.send(message, recipient);
    });
  }
}
```

### 資料驗證系統

```typescript
/** 遵循 OCP 的驗證系統 */
interface Validator {
  validate(data: any): boolean;
}

class EmailValidator implements Validator {
  validate(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

class PasswordValidator implements Validator {
  validate(password: string): boolean {
    return password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password);
  }
}

class PhoneValidator implements Validator {
  validate(phone: string): boolean {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    return phoneRegex.test(phone);
  }
}

class ValidationService {
  private validators: Map<string, Validator> = new Map();

  addValidator(field: string, validator: Validator): void {
    this.validators.set(field, validator);
  }

  validateField(field: string, data: any): boolean {
    const validator = this.validators.get(field);
    return validator ? validator.validate(data) : true;
  }

  validateAll(data: Record<string, any>): boolean {
    return Object.entries(data).every(([field, value]) => 
      this.validateField(field, value)
    );
  }
}
```

<br />

## 設計模式與 OCP

### 策略模式 (Strategy Pattern)

```typescript
interface SortingStrategy {
  sort(data: number[]): number[];
}

class BubbleSort implements SortingStrategy {
  sort(data: number[]): number[] {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }
}

class QuickSort implements SortingStrategy {
  sort(data: number[]): number[] {
    if (data.length <= 1) return data;

    const pivot = data[Math.floor(data.length / 2)];
    const left = data.filter(x => x < pivot);
    const middle = data.filter(x => x === pivot);
    const right = data.filter(x => x > pivot);

    return [...this.sort(left), ...middle, ...this.sort(right)];
  }
}

class SortContext {
  constructor(private strategy: SortingStrategy) {}

  setStrategy(strategy: SortingStrategy): void {
    this.strategy = strategy;
  }

  executeSort(data: number[]): number[] {
    return this.strategy.sort(data);
  }
}
```

### 工廠模式 (Factory Pattern)

```typescript
abstract class Logger {
  abstract log(message: string): void;
}

class FileLogger extends Logger {
  log(message: string): void {
    console.log(`[FILE] ${new Date().toISOString()}: ${message}`);
  }
}

class DatabaseLogger extends Logger {
  log(message: string): void {
    console.log(`[DB] ${new Date().toISOString()}: ${message}`);
  }
}

class ConsoleLogger extends Logger {
  log(message: string): void {
    console.log(`[CONSOLE] ${new Date().toISOString()}: ${message}`);
  }
}

class LoggerFactory {
  private static loggers: Map<string, () => Logger> = new Map([
    ['file', () => new FileLogger()],
    ['database', () => new DatabaseLogger()],
    ['console', () => new ConsoleLogger()]
  ]);

  static createLogger(type: string): Logger {
    const loggerCreator = this.loggers.get(type);
    if (!loggerCreator) {
      throw new Error(`Unknown logger type: ${type}`);
    }
    return loggerCreator();
  }

  /** 新增記錄器類型不需要修改現有程式碼 */
  static registerLogger(type: string, creator: () => Logger): void {
    this.loggers.set(type, creator);
  }
}
```

<br />

## 實現 OCP 的技巧

### 使用抽象化
```typescript
/** 定義抽象介面 */
interface DataProcessor {
  process(data: any): any;
}

/** 具體實作 */
class JSONProcessor implements DataProcessor {
  process(data: string): object {
    return JSON.parse(data);
  }
}

class XMLProcessor implements DataProcessor {
  process(data: string): object {
    // XML 解析實作
    return {};
  }
}

/** 處理器可以擴展而不修改現有程式碼 */
class CSVProcessor implements DataProcessor {
  process(data: string): object[] {
    // CSV 解析實作
    return [];
  }
}
```

### 使用組合模式
```typescript
interface Component {
  render(): string;
}

class Button implements Component {
  constructor(private text: string) {}

  render(): string {
    return `<button>${this.text}</button>`;
  }
}

class Input implements Component {
  constructor(private type: string, private placeholder: string) {}

  render(): string {
    return `<input type="${this.type}" placeholder="${this.placeholder}" />`;
  }
}

class Container implements Component {
  private children: Component[] = [];

  add(component: Component): void {
    this.children.push(component);
  }

  render(): string {
    const childrenHTML = this.children.map(child => child.render()).join('');
    return `<div>${childrenHTML}</div>`;
  }
}
```

### 使用依賴注入
```typescript
interface DatabaseConnection {
  query(sql: string): any[];
}

class MySQLConnection implements DatabaseConnection {
  query(sql: string): any[] {
    console.log(`Executing MySQL query: ${sql}`);
    return [];
  }
}

class PostgreSQLConnection implements DatabaseConnection {
  query(sql: string): any[] {
    console.log(`Executing PostgreSQL query: ${sql}`);
    return [];
  }
}

class UserRepository {
  constructor(private db: DatabaseConnection) {}

  findAll(): any[] {
    return this.db.query('SELECT * FROM users');
  }

  findById(id: number): any {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

/** 使用範例 */
const mysqlRepo = new UserRepository(new MySQLConnection());
const postgresRepo = new UserRepository(new PostgreSQLConnection());
```

<br />

## 常見誤區

### 過度抽象化
```typescript
/** 過度抽象化的例子 */
interface NumberOperation {
  execute(a: number, b: number): number;
}

class Addition implements NumberOperation {
  execute(a: number, b: number): number {
    return a + b;
  }
}

/** 簡單的加法不需要這麼複雜的抽象 */
function add(a: number, b: number): number {
  return a + b;
}
```

### 預測性設計
```typescript
/** 避免：為未來可能的需求過度設計 */
interface UserProcessor {
  processUser(user: User): void;
  processUserWithEmail(user: User): void;
  processUserWithSMS(user: User): void;
  // 過多的預測性方法
}

/** 正確：根據當前需求設計，需要時再擴展 */
interface UserProcessor {
  process(user: User): void;
}
```

### 忽略效能考量
```typescript
/** 注意：過度使用多型可能影響效能 */
class ShapeRenderer {
  render(shapes: Shape[]): void {
    shapes.forEach(shape => {
      // 每次呼叫都有多型的開銷
      const area = shape.calculateArea();
      console.log(`Shape area: ${area}`);
    });
  }
}

/** 在效能敏感的場景中，可能需要權衡 */
class OptimizedShapeRenderer {
  render(rectangles: Rectangle[], circles: Circle[]): void {
    /** 分別處理不同類型，減少多型開銷 */
    rectangles.forEach(rect => console.log(`Rectangle area: ${rect.width * rect.height}`));
    circles.forEach(circle => console.log(`Circle area: ${Math.PI * circle.radius ** 2}`));
  }
}
```

<br />

## 與其他 SOLID 原則的關係

- 單一職責原則 (SRP)：職責分離使得擴展更容易實現

- 里氏替換原則 (LSP)：正確的繼承關係支援 OCP 的實現

- 介面隔離原則 (ISP)：小而專注的介面更容易擴展

- 依賴反轉原則 (DIP)：依賴抽象使得擴展成為可能

<br />

## 總結

OCP 是軟體設計中的重要原則，遵循 OCP 能夠

- 提高系統穩定性：新功能不會破壞現有功能

- 降低維護風險：減少修改現有程式碼的需要

- 增強可擴展性：透過抽象化輕鬆新增功能

- 提升程式碼品質：促進更好的設計和架構

- 簡化測試工作：新功能可以獨立測試

### 注意：軟體實體應該對擴展開放，對修改封閉。

當需要新增功能時，優先考慮透過擴展來實現，而不是修改現有的程式碼。透過抽象化、多型和設計模式來達成這個目標。
