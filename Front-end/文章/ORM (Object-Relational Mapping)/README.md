# ORM (Object-Relational Mapping)

ORM (Object-Relational Mapping，物件關聯對映) 是一種程式設計技術，允許開發人員在物件導向程式設計 (Object-Oriented Programming) 中與關係資料庫進行互動，而無需直接撰寫 SQL 語句。

ORM 的核心思想是將資料庫中的結構與程式中的物件進行對映，資料庫中的表格 (Table) 映射到程式中的類別 (Class)，表格中的資料行 (Column) 映射到類別的屬性 (Property)。透過這種方式，開發人員可以像操作程式中的物件一樣來處理資料庫，而無需深入了解底層的 SQL 操作。

| 程式語言中的物件導向概念 | 資料庫中的關聯概念 |
| - | - |
| 類別 (Class) | 資料表 (Table) |
| 屬性 (Property) | 欄位 (Column) |
| 實例 (Instance/Object) | 資料列 (Row/Record) |

假設有一個名為 `users` 的資料庫表格，包含 `id`、`name` 和 `email` 三個資料行。使用 ORM，可以定義一個 `User` 類別，其中包含對應的 `id`、`name` 和 `email` 屬性。當創建一個 `User` 物件並設置其屬性時，ORM 會自動將這些資料存入資料庫。當需要從資料庫中提取資料時，ORM 會將查詢結果轉換為 `User` 物件，供程式直接使用。

```javascript
class User {
  constructor(id, name, email) {
    this.id = id;
    this.name = name;
    this.email = email;
  }
}
```

對應資料表可能如下

| id | name | email |
| - | - | - |
| 1 | Charmy | charmy@example.com |
| 2 | Tina | tina@test.com |

<br />

## ORM 的運作原理

ORM 的運作基於物件與關係資料庫之間的對映關係。

1. 定義模型

    開發人員定義一個類別，這個類別對應資料庫中的某個表格。例如：一個 `User` 類別對應 `users` 表格，類別中的屬性則對應表格的資料行。

2. 創建物件

    開發人員創建該類別的實例 (物件)，並為其屬性賦值。例如：創建一個 `User` 物件並設置 `name` 為 `Charmy`，email 為 `charmy@example.com`。

3. 保存物件

    ORM 會將物件的屬性值轉換為 SQL 的 `INSERT` 語句，並將資料存入資料庫。開發人員無需手動編寫 SQL。

4. 查詢資料

    開發人員使用 ORM 提供的查詢介面 (API) 來檢索資料庫中的資料。ORM 會執行 SQL `SELECT` 語句，並將結果轉換為物件或物件列表。

5. 更新與刪除

    開發人員可以修改物件的屬性並提交變更，ORM 會生成對應的 SQL `UPDATE` 語句；或者刪除物件，ORM 會執行 SQL `DELETE` 語句。

這種對映關係讓開發人員專注於物件層面，而無需處理底層的資料庫操作細節。

<br />

## ORM 的優缺點

### 優點

- 提高開發效率

    開發人員無需手動撰寫繁瑣的 SQL 語句，只需操作物件即可完成資料庫操作。這樣大幅縮短了開發時間。

- 減少錯誤

    SQL 語法錯誤是開發中的常見問題。ORM 自動生成 SQL 語句，能有效降低人為錯誤的發生機率。

- 增強程式碼可讀性

    使用物件導向的方式管理資料庫操作，讓程式碼更直觀、更符合現代程式設計的習慣，便於維護和理解。

- 跨資料庫兼容性

    大多數 ORM 框架支援多種資料庫系統 (例如：MySQL、PostgreSQL、SQLite 等)。開發人員只需撰寫一次程式碼，即可在不同資料庫間切換，無需針對特定資料庫調整 SQL。

- 提升安全性

    ORM 通常內建防止 SQL 注入 (SQL Injection) 的機制，透過參數化查詢保護應用程式免受安全威脅。

### 缺點

- 性能損失

    ORM 自動生成的 SQL 語句可能不如手動優化的 SQL 高效，尤其在處理複雜查詢或大規模資料時，可能導致性能瓶頸。

- 學習曲線

    對於初次接觸 ORM 的開發人員來說，理解其運作方式和相關框架可能需要一定的學習成本。

- 功能限制

    ORM 可能無法完全支援某些資料庫的高級功能 (例如：特定資料庫的原生函數或複雜聯表查詢)。在這些情況下，開發人員可能仍需直接使用 SQL。

<br />

## 臺灣常見的 ORM 框架範例

- Python

    - SQLAlchemy：這是 Python 最著名且功能強大的 ORM 之一，提供高度的靈活性和控制力，既可以用作全功能的 ORM，也可以作為底層的 SQL 工具包。

    - Django ORM：Django 是 Python Web 框架，其內建的 ORM 深度整合於框架之中，提供快速開發的便利性。

- PHP：

    - Doctrine ORM：在 Symfony 等 PHP 框架中廣泛使用，提供強大的物件映射和資料庫操作功能。

    - Laravel Eloquent ORM：Laravel 是一個極受歡迎的 PHP Web 框架，其 Eloquent ORM 以優雅的語法和簡潔的 API 著稱。

- Java：

    - Hibernate：Java 生態系中最具代表性的 ORM 框架，功能強大且成熟，被許多企業級應用程式所採用。

    - MyBatis：與 Hibernate 不同，MyBatis 是一個半 ORM 框架，更側重於 SQL 映射，允許開發人員自行撰寫 SQL，但仍提供物件與結果集的映射。

- Node.js (JavaScript/TypeScript)：

    - Sequelize： 一個功能豐富的 ORM，支援多種資料庫，提供完善的查詢接口。

    - TypeORM： 專為 TypeScript 設計的 ORM，支援多種資料庫，提供強大的型別安全。

<br />

## 總結

ORM 將資料庫操作從底層的 SQL 語句中抽象出來，讓開發人員能夠以更符合物件導向思維的方式進行開發。透過提高開發效率、改善程式碼可讀性及提供資料庫獨立性等優點，ORM 已經成為許多應用程式不可或缺的一部分。

然而，選擇是否使用 ORM 以及如何使用，仍需權衡其優缺點。對於大多數 CRUD 操作等，ORM 能極大提升開發效率；但對於效能要求極高的複雜查詢，適時回歸手寫 SQL 語句或利用 ORM 提供的原生 SQL 功能，將會是更明智的選擇。理解 ORM 的原理、熟練掌握其使用方法並適應不同場景下的應用，是每位現代開發人員應具備的重要能力。
