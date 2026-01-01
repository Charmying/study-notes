# 物件導向 (OOP)

物件導向程式設計 (Object-Oriented Programming，簡稱 OOP) 是一種以物件為核心的程式設計典範。OOP 將資料與操作資料的方法封裝在一起，形成一個獨立的單元，並透過這些物件之間的互動來解決問題。

物件導向的四大核心特性包括

- 封裝 (Encapsulation)

- 繼承 (Inheritance)

- 多型 (Polymorphism)

- 抽象 (Abstraction)

<br />

## 類別 (Class)

類別用於定義物件的結構與行為，包含了屬性 (Attributes) 與方法 (Methods)

- 屬性 (Attributes)：描述物件的特徵或狀態，例如：汽車物件的屬性可能包括顏色、品牌、速度等。

- 方法 (Methods)：定義物件可以執行的行為，例如：汽車的方法可能包括加速、剎車、轉向等。

### 建構函式 (Constructor)

建構函式是一種特殊的方法，在物件建立時自動執行，常用來初始化屬性值。

TypeScript 範例

```typescript
class Car {
  /** 屬性 (Attributes) */
  brand: string;
  model: string;
  year: number;

  /** 建構函式 (Constructor) */
  constructor(brand: string, model: string, year: number) {
    this.brand = brand;
    this.model = model;
    this.year = year;
  }

  /** 方法 (Methods) */
  public startEngine(): void {
    console.log(`${this.brand} ${this.model}`);
  }
}
```

Python 範例

```python
class Car:
    # 建構函式 (Constructor)
    def __init__(self, brand, model, year):
    	# 屬性 (Attributes)
    	self.brand = brand
    	self.model = model
    	self.year = year

    # 方法 (Methods)
    def start_engine(self):
        print(f"{self.brand} {self.model}")
```

<br />

## 物件 (Object)

物件是類別的實例 (Instance)，是根據類別創建的具體實體。每個物件擁有類別中定義的屬性與方法，但各自的屬性值可以不同。

TypeScript 範例

```typescript
/** 創建物件 */
const myCar = new Car("Bugatti", "La Voiture Noire", 2019);
const yourCar = new Car("Pagani", "Zonda HP Barchetta", 2017);

/** 使用物件的方法 */
myCar.startEngine();   // Bugatti La Voiture Noire
yourCar.startEngine(); // Pagani Zonda HP Barchetta
```

Python 範例

```python
# 創建物件
my_car = Car("Bugatti", "La Voiture Noire", 2020)
your_car = Car("Pagani", "Zonda HP Barchetta", 2018)

# 使用物件的方法
my_car.start_engine()   # Bugatti La Voiture Noire
your_car.start_engine() # Pagani Zonda HP Barchetta
```

### 類別與物件的差異

- 類別是抽象的，只定義了物件的結構和行為，但本身並不佔用記憶體。

- 物件是具體的，是根據類別創建的實例，佔用記憶體並擁有實際的資料。

舉例來說

- 類別就像「汽車設計圖」，描述品牌、型號、年份與功能。

- 物件就像依設計圖製造的「真實汽車」，每輛汽車的屬性值可以不同。

<br />

## 封裝 (Encapsulation)

封裝是將資料與操作資料的方法包裝在一個物件中，並限制外部直接存取內部資料，以保護資料的完整性、減少耦合並提升可維護性。

TypeScript 範例

```typescript
class BankAccount {
  private balance: number;

  constructor(initialBalance: number) {
    this.balance = initialBalance;
  }

  public deposit(amount: number): void {
    if (amount > 0) {
      this.balance += amount;
    }
  }

  public withdraw(amount: number): void {
    if (amount > 0 && amount <= this.balance) {
      this.balance -= amount;
    }
  }

  public getBalance(): number {
    return this.balance;
  }
}

const account = new BankAccount(1000);
account.deposit(500);
account.withdraw(200);
console.log(account.getBalance()); // 1300
```

Python 範例

```python
class BankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance # 使用雙底線表示私有變數

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance()) # 1300
```

<br />

## 繼承 (Inheritance)

繼承允許一個類別繼承另一個類別的屬性與方法，達到程式碼重用的目的。子類別可擴充或覆寫父類別的功能。

TypeScript 範例

```typescript
class Animal {
  protected name: string;

  constructor(name: string) {
    this.name = name;
  }

  public makeSound(): void {
    console.log("動物發出聲音");
  }
}

class Dog extends Animal {
  public makeSound(): void {
    console.log(`${this.name} 汪汪叫`);
  }
}

const myDog = new Dog("小黑");
myDog.makeSound(); // 小黑 汪汪叫
```

Python 範例

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("動物發出聲音")

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} 汪汪叫")

my_dog = Dog("小黑")
my_dog.make_sound() # 小黑 汪汪叫
```

<br />

## 多型 (Polymorphism)

多型是指不同的類別可以對相同的方法名稱有不同的實現方式，使得程式可以更靈活處理不同類型的物件。

TypeScript 範例

```typescript
class Animal {
    constructor(public name: string) {}
    makeSound(): void {}
}

class Dog extends Animal {
    makeSound(): void {
        console.log(`${this.name} 汪汪叫`);
    }
}

class Cat extends Animal {
    makeSound(): void {
        console.log(`${this.name} 喵喵叫`);
    }
}

const animals: Animal[] = [new Dog("小黑"), new Cat("小白")];
animals.forEach(animal => animal.makeSound());

```

執行結果：

```console
小黑 汪汪叫
小白 喵喵叫
```

Python 範例

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        pass # 基底類別只定義介面，不實作


class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} 汪汪叫")


class Cat(Animal):
    def make_sound(self):
        print(f"{self.name} 喵喵叫")


# 使用範例
animals = [Dog("小黑"), Cat("小白")]
for animal in animals:
    animal.make_sound()
```

執行結果：

```console
小黑 汪汪叫
小白 喵喵叫
```

<br />

## 抽象 (Abstraction)

抽象是將複雜的功能隱藏，只暴露必要的功能，讓使用者能專注在核心操作。

在 OOP 中，抽象可透過抽象類別 (Abstract Class) 或介面 (Interface) 實現。

TypeScript 範例 (抽象類別)

```typescript
abstract class Shape {
  abstract getArea(): number;
}

class Circle extends Shape {
  private radius: number;

  constructor(radius: number) {
    super();
    this.radius = radius;
  }

  public getArea(): number {
    return Math.PI * this.radius * this.radius;
  }
}

const myCircle = new Circle(5);
console.log(myCircle.getArea()); // 78.53981633974483
```

Python 範例 (抽象類別)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def get_area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return 3.14159 * self.radius * self.radius

my_circle = Circle(5)
print(my_circle.get_area()) # 78.53975
```

<br />

## 介面 (Interface) (TypeScript 專屬補充)

介面定義了一組規範，類別可以實作 `implements` 該介面以保證行為一致，但不包含實作細節。

TypeScript 範例

```typescript
interface Flyable {
  fly(): void;
}

class Bird implements Flyable {
  public fly(): void {
    console.log("Bird is flying");
  }
}
```

<br />

## 總結

物件導向程式設計 (OOP) 透過封裝、繼承、多型與抽象等特性，讓程式碼更具結構性、可重用性與可維護性，進而提升開發效率與系統可擴充性，是現代軟體設計的重要基礎。
