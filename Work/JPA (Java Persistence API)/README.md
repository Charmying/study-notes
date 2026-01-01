# JPA (Java Persistence API)

JPA (Java Persistence API) 是 Java EE 的一個規範，用於管理 Java 物件與關係資料庫之間的持久化。

JPA 透過 ORM (Object Relational Mapping) 提供高階 API，讓開發人員以物件導向方式操作資料庫。

<br />

## JPA 的核心概念

- 實體 (Entity)

    - 對應資料庫中的表。

    - 使用 `@Entity` 標註，並需有主鍵 (`@Id`)。

    ```java
	@Entity
	public class User {
		@Id
		@GeneratedValue(strategy = GenerationType.IDENTITY)
		private Long id;

		private String name;
		private String email;
	}
    ```

- 持久化上下文 (Persistence Context)

    管理實體生命週期，追蹤狀態 (新建、已管理、已分離、已刪除)。

- 實體管理器 (EntityManager)

    - JPA 的核心接口，負責 CRUD 與交易控制。

    - 由 `EntityManagerFactory` 建立。

    ```java
    EntityManagerFactory emf = Persistence.createEntityManagerFactory("example-unit");
    EntityManager em = emf.createEntityManager();

	em.getTransaction().begin();
	User user = new User();
	user.setName("Charmy");
	em.persist(user);
	em.getTransaction().commit();
    ```

- 查詢語言 (JPQL)

    - 操作的是實體物件，而不是資料庫表。

    - 語法類似 SQL。

    ```java
	List<User> users = em.createQuery(
		"SELECT u FROM User u WHERE u.name = :name", User.class)
		.setParameter("name", "Charmy")
		.getResultList();
    ```

<br />

## JPA 的優勢

- 簡化持久化程式碼：減少 SQL 與連線管理。

- 跨平台性：Java EE 標準，程式碼可移植。

- 支援多種資料庫：透過 Hibernate、EclipseLink 等實現。

- 自動管理實體狀態：降低手動管理成本。

<br />

## 常見的 JPA 實現

- Hibernate：最流行，支援延遲加載、快取等功能。

- EclipseLink：Eclipse 社群提供，JPA 參考實現。

- OpenJPA：Apache 提供，強調擴展性與效能。

<br />

## JPA 的優缺點

### 優點

- 抽象化資料庫操作：程式碼簡潔，平台獨立。

- ORM 支援：以物件操作資料庫，自動映射與同步。

- 交易與持久化上下文：確保一致性，提升效能 (快取、延遲加載)。

- JPQL 查詢：具表達性，支援動態查詢。

- 易於整合：可搭配 Spring、JSF 等技術。

### 缺點

- 學習曲線：規範龐大，新手需時間熟悉。

- 性能開銷：抽象層與延遲加載若管理不當，易出現效能瓶頸 (例如：N+1 問題)。

- 複雜查詢受限：多表聯結或資料庫特有功能仍需原生 SQL。

- 特性限制：部分資料庫功能可能無法透過 JPA 使用。

- 除錯困難：比直接使用 JDBC 更難追蹤問題。

<br />

## 總結

JPA 是 Java 企業級應用中關鍵的持久化技術，讓開發人員能以物件導向方式處理資料庫，提升開發效率、可維護性與擴展性。但需理解其抽象層的限制與效能影響，才能正確運用。
