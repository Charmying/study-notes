# 依賴注入 (Dependency Injection)

依賴注入 (Dependency Injection，簡稱：DI) 是一種設計模式 (Design Pattern)，用於實現控制反轉 (Inversion of Control，簡稱：IoC) 的原則。核心思想是將物件之間的依賴關係由外部容器來管理，而不是由物件自己來創建或尋找依賴的物件。這種方式可以讓程式碼更加模組化、易於測試和維護。

在 Angular 中，依賴注入是框架的核心機制之一，允許開發人員將服務 (Service)、元件 (Component)、指令 (Directive) 等物件注入到需要的地方，不需要手動創建這些物件。

<br />

## 依賴注入的優點

- 模組化：將物件之間的依賴關係解耦，使程式碼更加模組化。

- 易於測試：可以輕鬆替換依賴物件，例如：在單元測試中使用模擬物件 (Mock Object)。

- 可維護性：集中管理依賴關係，減少重複程式碼，提升可維護性。

- 靈活性：可以動態替換或配置依賴物件，提升應用程式的靈活性。

<br />

## Angular 中的依賴注入機制

- Injector (注入器)

    Injector 是 Angular 中用來創建和管理依賴物件的容器。Injector 負責根據提供的依賴關係，創建並返回所需的物件。Angular 應用程式中有一個根注入器 (Root Injector)，並且每個模組 (Module) 和元件 (Component) 也可以有自己的 Injector。

- Provider (提供者)

    Provider 是用來告訴 Injector 如何創建某個依賴物件。通常是一個物件，包含以下屬性：

    - `provide`：指定要提供的依賴的標識符 (Token)，通常是類別 (Class) 或字串。

    - `useClass`、`useValue`、`useFactory` 等：指定如何創建或提供這個依賴。

    例如：

    ```typescript
    { provide: MyService, useClass: MyService }
    ```

- 依賴注入的層級 (Hierarchy)

    Angular 的依賴注入系統具有層級結構 (Hierarchy)。當某個 Component 或 Service 需要一個依賴時，Injector 會先在當前層級尋找，若找不到，則會向上層級查找，直到找到為止。這種機制允許開發人員在不同的層級提供不同的依賴物件。

<br />

## Angular 中的注入方式

在 Angular 中，依賴注入可以通過以下幾種方式實現：

- 建構函數注入 (Constructor Injection)：在類別的建構函數中聲明依賴，Angular 會自動注入。

    ```typescript
    constructor(private myService: MyService) {}
    ```

- 屬性注入 (Property Injection)：通過 `@Inject` 裝飾器 (Decorator) 將依賴注入到屬性中。

    ```typescript
    @Inject(MyService) private myService: MyService;
    ```

### 實際應用範例

1. 創建 Service

    ```typescript
    import { Injectable } from '@angular/core';

    @Injectable({
      providedIn: 'root'
    })
    export class MyService {
      getData() {
        return 'Hello, Angular!';
      }
    }
    ```

2. 在元件中使用 Service

    ```html
    <h1>{{ message }}</h1>
    ```

    ```typescript
    import { Component } from '@angular/core';
    import { MyService } from './my.service';

    @Component({
      selector: 'app-root',
    })
    export class AppComponent {
      message: string;

      constructor(private myService: MyService) {
        this.message = this.myService.getData();
      }
    }
    ```

    在這個範例中，`MyService` 被注入到 `AppComponent` 中，並在元件初始化時調用 `getData` 方法。

<br />

## 總結

Angular 的依賴注入機制是框架的核心機制之一，通過 Injector 和 Provider 來管理物件之間的依賴關係。這種設計模式不僅提升了程式碼的模組化和可維護性，還使應用程式更加靈活且易於測試。
