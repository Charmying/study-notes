# `@ViewChild`

在 Angular 框架中，`@ViewChild` 是一個非常重要的裝飾器 (Decorator)，主要用於在元件 (Component) 中獲取對模板 (Template) 中的子元素或子元件的引用，在需要直接操作 DOM 元素或與子元件進行互動時非常有用。

<br />

## `@ViewChild` 的基本用法

```typescript
@ViewChild(selector, {static: boolean}) propertyName: Type;
```

- `selector`：可以是模板中的一個元件、指令 (Directive) 或 DOM 元素的選擇器 (Selector)。

- `static`：是一個可選的參數，用於指定是否在變更檢測 (Change Detection) 的靜態階段 (Static Phase) 就解析這個查詢。預設值為 `false`，表示在變更檢測的動態階段 (Dynamic Phase) 進行解析。

- `propertyName`：這是在元件中定義的屬性名稱，用來儲存查詢到的引用。

- `Type`：這是查詢到的元素的類型，可以是元件類別、指令類別，或者是原生 DOM 元素的類型。

<br />

## `@ViewChild` 的使用範例

假設有一個簡單的 Angular 元件，並且想要獲取模板中的一個 `input` 元素的引用。

```html
<input #myInput type="text" placeholder="請輸入文字">
<button (click)="focusInput()">focus 輸入框</button>
```

在這個模板中，使用了 `#myInput` 來定義一個模板變數 (Template Reference Variable)，這將作為 `@ViewChild` 的選擇器。

```typescript
import { Component, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild('myInput', { static: true }) myInput: ElementRef;

  focusInput() {
    this.myInput.nativeElement.focus();
  }
}
```

在這個元件中，使用了 `@ViewChild` 來獲取 `myInput` 的引用，並將其儲存在 `myInput` 屬性中。`ElementRef` 是 Angular 提供的一個類別，封裝了對原生 DOM 元素的引用。在 `focusInput` 方法中，使用這個引用來調用原生 DOM 元素的 `focus` 方法，使輸入框獲得焦點。

<br />

## `@ViewChild` 查詢子元件

假設有一個 `ChildComponent` 的子元件，可以在父元件中獲取其引用。

```html
<app-child #childComponent></app-child>
<button (click)="callChildMethod()">調用子元件方法</button>
```

```typescript
import { Component, ViewChild } from '@angular/core';
import { ChildComponent } from './child.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild('childComponent', { static: true }) childComponent: ChildComponent;

  callChildMethod() {
    this.childComponent.someMethod();
  }
}
```

在這個範例中，使用 `@ViewChild` 來獲取 `ChildComponent` 的引用，並在 `callChildMethod` 方法中調用子元件的 `someMethod` 方法。

<br />

## `@ViewChild` 查詢指令

假設有一個名為 `HighlightDirective` 的指令，可以在元件中獲取其引用。

```html
<p appHighlight>被 highlight 的文字</p>
<button (click)="changeHighlightColor()">改變 highlight 顏色</button>
```

```typescript
import { Component, ViewChild } from '@angular/core';
import { HighlightDirective } from './highlight.directive';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild(HighlightDirective, { static: true }) highlightDirective: HighlightDirective;

  changeHighlightColor() {
    this.highlightDirective.changeColor('yellow');
  }
}
```

在這個範例中，使用 `@ViewChild` 來獲取 `HighlightDirective` 的引用，並在 `changeHighlightColor` 方法中調用指令的 `changeColor` 方法來改變 highlight 顏色。

<br />

## `@ViewChild` 靜態與動態查詢

`@ViewChild` 的第二個參數 `static` 用於指定查詢的時機。若 `static` 設為 `true`，則查詢會在變更檢測的靜態階段進行，也就是說，查詢會在元件初始化時就完成。若 `static` 設為 `false`，則查詢會在變更檢測的動態階段進行，也就是說，查詢會在元件視圖 (View) 初始化後才完成。

在大多數情況下，`static` 會設為 `false`，但在某些情況下，例如：當需要查詢的元素在 `*ngIf` 或 `*ngFor` 中時，可能需要將 `static` 設為 `true` 來確保查詢在元件初始化時就完成。

<br />

## `@ViewChild` 靜態與動態查詢

除了 `@ViewChild`，Angular 也提供了 `@ViewChildren` 來查詢多個子元素或子元件。`@ViewChildren` 的用法與 `@ViewChild` 類似，但返回的是一個 `QueryList` 物件，可以遍歷這個列表來操作每個查詢到的元素。

```typescript
import { Component, ViewChildren, QueryList } from '@angular/core';
import { ChildComponent } from './child.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChildren(ChildComponent) children: QueryList<ChildComponent>;

  ngAfterViewInit() {
    this.children.forEach(child => child.someMethod());
  }
}
```

在這個範例中，使用 `@ViewChildren` 來獲取所有 `ChildComponent` 的引用，並在 `*ngAfterViewInit` 中遍歷這些引用，調用每個子元件的 `someMethod` 方法。

<br />

## 總結

`@ViewChild` 是 Angular 中一個非常強大的工具，允許在元件中獲取對模板中的子元素、子元件或指令的引用。通過 `@ViewChild` 可以更靈活操作 DOM 元素和與子元件互動。
