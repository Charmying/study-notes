# `constructor()` 建構函式

在程式開發中，`constructor()` 是一個非常重要的概念，特別是在物件導向程式設計 (Object-Oriented Programming，簡稱：OOP) 中，用於初始化一個類別 (Class) 的實例 (Instance)，並在物件創建時執行必要的設定。

<br />

## `constructor()` 簡介

`constructor()` 是物件導向程式設計中用於初始化物件的方法。

當一個類別 (Class) 被實例化 (Instantiated) 時，`constructor()` 會自動執行，用於設定物件的初始狀態或執行必要的初始化操作。

在許多程式語言中，`constructor()` 是類別的預設方法，名稱可能有所不同 (例如：Python 的 `__init__()`)，但功能大致相同。

<br />

## `constructor()` 的語法

```typescript
class MyClass {
  /** 屬性 (Property) */
  private name: string;

  /** 建構函式 (Constructor) */
  constructor(name: string) {
    this.name = name; // 初始化屬性
  }

  /** 方法 (Method) */
  public greet(): void {
    console.log(`Hello, ${this.name}`);
  }
}

/** 創建實例 (Instance) */
const myInstance = new MyClass("Charmy");
myInstance.greet(); // Hello, Charmy
```

語法說明

- `constructor()` 是類別的預設方法，不需要手動呼叫。

- 參數可以在 `constructor()` 中傳遞，用於初始化屬性。

- `this` 用於指向當前實例的屬性和方法。

<br />

## `constructor()` 的用途

- 初始化屬性

    在物件創建時，`constructor()` 可以為物件的屬性賦予初始值。

    ```typescript
    class Person {
      private name: string;
      private age: number;

      constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
      }
    }
    ```

- 依賴注入 (Dependency Injection)

    在 Angular 中，`constructor()` 用於注入服務 (Service) 或其他依賴。

    ```typescript
    import { HttpClient } from '@angular/common/http';

	class MyService {
	  constructor(private http: HttpClient) {}
	}
    ```

- 執行初始化

    `constructor()` 可以執行必要的初始化，例如：分配資源或設定預設值。

    ```typescript
    class Database {
      private connection: any;

      constructor() {
        this.connection = this.connect(); // 初始化資料庫連線
      }

      private connect(): any {
        // 連線
      }
    }
    ```

<br />

## `constructor()` 在不同語言中的應用

`constructor()` 是多種程式語言中的通用概念，以下列舉幾種常見語言的範例

- JavaScript

    JavaScript 中的 `constructor()` 與 TypeScript 相同

    ```javascript
    class Person {
      constructor(name, age) {
        this.name = name;
        this.age = age;
      }
    }

    const person = new Person("Charmy", 28);
    console.log(person.name); // Charmy
    ```

- PHP

    PHP 中的建構函式是 `__construct()` 方法

    ```php
    class Person {
    	private $name;
    	private $age;

        public function __construct($name, $age) {
	    	$this->name = $name;
	    	$this->age = $age;
        }
    }

	$person = new Person("Charmy", 28);
	echo $person->name; // Charmy
    ```

- Java

    Java 中的建構函式語法略有不同

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public static void main(String[] args) {
        Person person = new Person("Charmy", 28);
        System.out.println(person.name); // Charmy
    }
}
```

- Python

    Python 中的建構函式是 `__init__()` 方法：

    ```python
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    person = Person("Charmy", 28)
    print(person.name) # Charmy
    ```

- C#

    C# 中的建構函式語法與 Java 類似：

    ```csharp
    public class Person {
    	private string name;
    	private int age;

        public Person(string name, int age) {
            this.name = name;
            this.age = age;
        }

        public static void Main(string[] args) {
            Person person = new Person("Charmy", 28);
            Console.WriteLine(person.name); // Charmy
        }
    }
    ```

- Ruby

    Ruby 中的建構函式是 `initialize()` 方法：

    ```ruby
    class Person
      def initialize(name, age)
        @name = name
        @age = age
      end
    end

	person = Person.new("Charmy", 28)
	puts person.name # Charmy
    ```

<br />

## `constructor()` 常見錯誤與陷阱

- 在 `constructor()` 中執行複雜程式

    ```typescript
    class MyClass {
      constructor() {
        /** ❌ 複雜程式應移至其他方法 */
        this.loadData();
        this.processData();
        this.renderUI();
      }
    }
    ```

    - 修正：保持 `constructor()` 簡單，僅用於初始化。

- 在 `constructor()` 中訪問尚未初始化的屬性

    ```typescript
    class MyClass {
      private data: any;

      constructor() {
        /** ❌ 錯誤：data 尚未初始化 */
        console.log(this.data);
      }
    }
    ```

    - 修正：確保屬性在 `constructor()` 中正確初始化。

<br />

## constructor() 的最佳實踐

- 保持 `constructor()` 簡單

    僅用於依賴注入和簡單初始化，避免執行複雜程式。

- 避免副作用 (Side Effects)

    `constructor()` 中不應執行可能導致副作用的操作，例如：API 呼叫或 DOM 操作。

- 明確實作初始化

    複雜的初始化應移至其他方法，例如：`ngOnInit()` 或自訂方法。

<br />

## 總結

`constructor()` 是物件導向程式設計中的核心概念，用於初始化物件的屬性和執行必要的設定，在多種程式語言中都有類似的實現，例如：JavaScript、TypeScript、Java、Python 和 C# 等。

在 TypeScript 和 Angular 中，`constructor()` 還承擔了依賴注入 (Dependency Injection) 的重要角色。正確使用 `constructor()` 能讓程式碼更符合物件導向的設計原則，同時避免因執行時機錯誤導致的問題。
