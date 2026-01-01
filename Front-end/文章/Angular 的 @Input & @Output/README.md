# `@Input()` & `@Output()`

在 Angular 框架中，`@Input()` 和 `@Output()` 是兩個非常重要的裝飾器 (Decorator)，用於元件 (Component) 之間的資料傳遞與互動。

<br />

## `@Input()`：父元件向子元件傳遞資料

`@Input()` 用於讓父元件將資料傳遞給子元件，是一種單向資料流 (One-Way Data Binding) 的方式，父元件可以通過屬性綁定 (Property Binding) 將資料傳遞給子元件。

### 使用方式

- 在子元件中，使用 `@Input()` 來宣告一個變數，這個變數將接收來自父元件的資料。

- 在父元件的模板 (Template) 中，通過屬性綁定將資料傳遞給子元件。

### 範例

```html
<!-- 子元件 child.component.html -->

<p>{{ message }}</p>
```

```typescript
/** 子元件 child.component.ts */

import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-child',
  standalone: true,
  templateUrl: './child.component.html',
  styleUrl: './child.component.scss',
})
export class ChildComponent {
  @Input() message: string = ''; // 接收來自父元件的資料
}
```

```html
<!-- 父元件 parent.component.html -->

<app-child [message]="parentMessage"></app-child>
```

```typescript
/** 父元件 parent.component.ts */

export class ParentComponent {
  parentMessage = '來自父元件的訊息';
}
```

- 在子元件中，`@Input()` 宣告了 `message` 變數，用於接收父元件傳遞的資料。

- 在父元件的模板中，通過 `[message]="parentMessage"` 將 `parentMessage` 的值綁定到子元件的 `message` 屬性。

<br />

## `@Output()`：子元件向父元件傳遞事件

`@Output` 用於讓子元件向父元件傳遞事件 (Event)，是一種事件驅動 (Event-Driven) 的方式，子元件可以通過事件發射器 (EventEmitter) 觸發事件，並將資料傳遞給父元件。

### 使用方式

- 在子元件中，使用 `@Output()` 裝飾器來宣告一個事件發射器 (EventEmitter)。

- 在父元件的模板中，通過事件綁定 (Event Binding) 來監聽子元件觸發的事件。

### 範例

```html
<!-- 子元件 child.component.html -->

<button (click)="sendMessage()">傳送訊息</button>
```

```typescript
/** 子元件 child.component.ts */

import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child',
  standalone: true,
  templateUrl: './child.component.html',
  styleUrl: './child.component.scss',
})
export class ChildComponent {
  @Output() messageEvent = new EventEmitter<string>(); // 宣告事件發射器

  sendMessage() {
    this.messageEvent.emit('這是來自子元件的訊息'); // 觸發事件並傳遞資料
  }
}
```

```html
<!-- 父元件 parent.component.html -->

<app-child (messageEvent)="receiveMessage($event)"></app-child>
<p>{{ receivedMessage }}</p>
```

```typescript
/** 父元件 parent.component.ts */

export class ParentComponent {
  receivedMessage = '';

  receiveMessage(message: string) {
    this.receivedMessage = message; // 接收子元件傳遞的資料
  }
}
```

- 在子元件中，`@Output()` 宣告了 `messageEvent` 事件發射器，並在 `sendMessage` 方法中觸發事件。

- 在父元件的模板中，通過 `(messageEvent)="receiveMessage($event)"` 監聽子元件觸發的事件，並將接收到的資料顯示在畫面上。

<br />

## `@Input()` 與 `@Output()` 的結合使用

`@Input()` 和 `@Output()` 可以結合使用，實現父子元件之間的雙向互動。例如：父元件可以通過 `@Input()` 傳遞資料給子元件，而子元件可以通過 `@Output()` 將處理後的結果回傳給父元件。

### 範例

```html
<!-- 子元件 child.component.html -->

<p>{{ message }}</p>
<button (click)="sendResponse()">回傳結果</button>
```

```typescript
/** 子元件 child.component.ts */

import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-child',
  standalone: true,
  templateUrl: './child.component.html',
  styleUrl: './child.component.scss',
})
export class ChildComponent {
  @Input() message: string = ''; // 接收來自父元件的資料
  @Output() responseEvent = new EventEmitter<string>(); // 宣告事件發射器

  sendResponse() {
    this.responseEvent.emit('子元件已收到訊息'); // 觸發事件並傳遞資料
  }
}
```

```html
<!-- 父元件 parent.component.html -->

<app-child [message]="parentMessage" (responseEvent)="handleResponse($event)"></app-child>
<p>{{ responseMessage }}</p>
```

```typescript
/** 父元件 parent.component.ts */

export class ParentComponent {
  parentMessage = '這是來自父元件的訊息';
  responseMessage = '';

  handleResponse(message: string) {
    this.responseMessage = message; // 接收子元件回傳的資料
  }
}
```

- 父元件通過 `@Input()` 將 `parentMessage` 傳遞給子元件，子元件顯示該訊息。

- 子元件通過 `@Output()` 觸發 `responseEvent` 事件，將回傳的資料傳遞給父元件，父元件接收並顯示。

<br />

## 總結

- `@Input()` 用於父元件向子元件傳遞資料，是一種單向資料流的方式。

- `@Output()` 用於子元件向父元件傳遞事件，是一種事件驅動的方式。

- 兩者結合使用，可以實現父子元件之間的雙向互動。

這些機制使得 Angular 的元件化開發更加靈活與模組化，提升了程式碼的可維護性與可重用性。
