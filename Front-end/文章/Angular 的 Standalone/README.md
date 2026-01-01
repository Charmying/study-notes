# Angular 的 Standalone

在 Angular 前端框架中，Standalone 元件 (獨立元件) 是為了簡化應用程式模組化設計而引入的重要功能。

獨立元件於 Angular 14 首次引入。在此之前，Angular 仰賴 `@NgModule` (模組) 來組織與管理 Component (元件)、Directive (指令)、Pipe (管道)、Service (服務) 等資源。這種模組化架構雖有效，但在大型專案或複雜場景中會導致配置複雜度增加。

<br />

## 獨立元件的定義與特性

- 定義

    - 獨立元件是指不依賴於 `@NgModule` 的 Angular 元件，屬於一種自包含的單元，無需在模組中宣告即可直接使用。

- 特性

    - 獨立性：無需在 `@NgModule` 中宣告或匯入，可直接在應用程式中使用。

    - 輕量化：減少模組配置，讓應用程式結構更簡潔。

    - 路由整合：可直接用於路由 (Routing) 配置，無需透過模組管理。

    - 模組匯入靈活性：獨立元件可自行匯入所需模組 (例如：`CommonModule` 或 `FormsModule`)，保持功能完整。


<br />

## 獨立元件的優點

- 簡化模組依賴：傳統元件需依賴模組註冊，獨立元件則無此限制，無需為每個元件創建或維護模組。

- 減少設定負擔：以往在 `app.module.ts` 中需集中宣告所有元件、管道與指令，導致程式碼臃腫。獨立元件讓這些設定分散到元件本身，降低維護成本。

- 靈活的路由管理：獨立元件可直接用於路由設定，使路由設置更直觀。

- 提升開發效率：開發人員可專注於元件功能，無需處理模組相關的複雜設定。

- 支援無模組化趨勢：獨立元件符合現代前端開發的輕量化與模組化趨勢，特別適合小型應用或微前端架構

<br />

## 獨立元件的使用範例

創建獨立元件時，只需在 `@Component` 裝飾器中設定 `standalone: true`，並在 `imports` 屬性中匯入所需的模組 (例如：`CommonModule`、`FormsModule`) 或其他獨立元件，這樣元件無需在 `@NgModule` 中宣告或匯入，即可在 Angular 應用程式中使用。

```typescript
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Component1Component } from "../../Component/component1/component1.component";
import { Component2Component } from "../../Component/component2/component2.component";
import { HeaderComponent } from "../../Component/header/header.component";

@Component({
  selector: 'app-origin',
  standalone: true,
  templateUrl: './origin.component.html',
  styleUrl: './origin.component.scss',
  imports: [RouterOutlet, Component1Component, Component2Component, HeaderComponent]
})
export class OriginComponent {
  title = 'Test';
}
```

<br />

## 獨立元件與 Routing 的結合

在 Angular 18+ 中，可以直接在路由設定中使用獨立元件，而不需要 `@NgModule`。

```typescript
import { Routes } from '@angular/router';
import { HelloWorldComponent } from './hello-world.component';

export const routes: Routes = [
  {
    path: '',
    component: HelloWorldComponent // 直接使用獨立元件
  }
];
```

<br />

## 總結

- 獨立元件讓 Angular 架構更靈活、更輕量化。

- 減少了對 `@NgModule` 的依賴

    - 小型應用程式 → 簡單快速

    - 大型應用程式 → 減少模組管理的複雜度

    - 開發人員可以專注於元件本身，而非模組設定。

Standalone 順應了無模組化 (Module-less) 的趨勢，使 Angular 更符合現代前端的開發需求。
