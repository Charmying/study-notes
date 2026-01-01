# RxJS (Reactive Extensions for JavaScript)

RxJS (Reactive Extensions for JavaScript) 是基於觀察者模式 (Observer Pattern) 的函式庫，用來處理非同步資料流 (Asynchronous Data Streams)，能夠用「資料是流動的」的方式去處理事件、HTTP 請求、WebSocket、計時器等情境。

舉例來說：想像水管中有水 (資料) 在流動，可以在水流經過時，裝過濾器 (`filter`)、變壓器 (`map`)、分流器 (`merge`) 等，這些就是 `Operators`，只要負責訂閱 (`subscribe`) 水流 (資料流)，就能即時使用或停止。

<br />

## 為什麼要用 RxJS

在 JavaScript 中常見非同步場景

- 使用者事件 (Click、Scroll、Keyup)

- API 呼叫 (HTTP request)

- 計時器 (`setTimeout`/`setInterval`)

- WebSocket 即時資料

- 多個資料來源合併

- 非同步程式依順序執行

若用 Callback 或 `Promise` 處理，很容易遇到

- Callback Hell

- 複雜的 `Promise` 鏈

- 難以取消任務

- 難以合併不同資料來源

RxJS 的優勢

- 統一介面：事件、`Promise`、陣列都可以轉成 `Observable`。

- 強大運算子：像積木一樣組裝資料處理流程 (`map`、`filter`、`debounceTime` ...)。

- 可取消：透過 `unsubscribe()` 停止資料流。

- 可讀性高：程式宣告式 (Declarative)，清楚易維護。

<br />

## 核心概念與圖解

- 核心流程圖

	```mermaid
	graph TD
	    A["資料來源 (Observable)：資料來源"] --> B["Operators 處理資料 (map、filter、merge...)：資料過濾/轉換"]
	    B --> C["訂閱者 (Observer)：接收資料"]
	    C --> D["Subscription (可取消)：控制訂閱"]
	```

-  `Observable` (可觀察物件)

    - 負責發送資料 (同步或非同步)。

    - 可發送多次資料，也可結束或發生錯誤。

	```typescript
	import { Observable } from 'rxjs';

	const observable = new Observable(subscriber => {
	  subscriber.next('Hello');
	  subscriber.next('RxJS');
	  setTimeout(() => {
	    subscriber.next('Async data');
	    subscriber.complete();
	  }, 1000);
	});
	```

- `Observer` (觀察者)

    - 接收 `Observable` 傳來的資料。

    - 有三種方法

	    `next(value)`：接收資料

	    `error(err)`：接收錯誤

	    `complete()`：資料流結束

	```typescript
	const observer = {
	  next: value => console.log('接收到:', value),
	  error: err => console.error('錯誤:', err),
	  complete: () => console.log('完成')
	};

	observable.subscribe(observer);
	```

- `Subscription` (訂閱)

    - `.subscribe()` 後會回傳 `Subscription`。

    - 用 `.unsubscribe()` 停止資料流，避免資源浪費或記憶體洩漏。

	```typescript
	const sub = observable.subscribe(observer);
	setTimeout(() => {
	  sub.unsubscribe(); // 停止接收
	}, 5000);
	```

- `Operators` (運算子)

    負責轉換、過濾、合併資料。

    常見分類

    - 轉換類：`map`, `switchMap`, `mergeMap`

    - 過濾類：`filter`, `debounceTime`, `distinctUntilChanged`

    - 組合類：`merge`, `combineLatest`, `concat`

    - 建立類：`of`, `from`, `interval`, `fromEvent`

	```typescript
    /** 過濾滑鼠 X 座標大於 100 */

	import { fromEvent } from 'rxjs';
	import { map, filter } from 'rxjs/operators';

	fromEvent(document, 'click')
	  .pipe(
	    map((event: MouseEvent) => event.clientX),
	    filter(x => x > 100)
	  )
	  .subscribe(x => console.log('X > 100:', x));
	```

<br />

## 實用範例

- 處理 HTTP 請求

	```typescript
	import { of } from 'rxjs';
	import { delay } from 'rxjs/operators';

	of('伺服器回應')
	  .pipe(delay(2000))
	  .subscribe(data => console.log(data));
	```

- 監聽輸入框輸入 (防抖 Debounce)

	```typescript
	import { fromEvent } from 'rxjs';
	import { map, debounceTime } from 'rxjs/operators';

	const input = document.getElementById('search') as HTMLInputElement;

	fromEvent(input, 'input')
	  .pipe(
	    map(() => input.value),
	    debounceTime(500) // 0.5 秒內沒有新輸入才觸發
	  )
	  .subscribe(value => console.log('搜尋:', value));
	```

- 合併資料流

	```typescript
	import { interval, merge } from 'rxjs';

	const stream1 = interval(1000);
	const stream2 = interval(1500);

	merge(stream1, stream2)
	  .subscribe(value => console.log('收到:', value));
	```

<br />

## RxJS vs Promise

| 特性 | `Observable` | `Promise` |
| - | - | - |
| 是否可多次傳值 | ✅ 支援 | ❌ 只能傳一次 |
| 是否可取消 | ✅ 可透過 unsubscribe | ❌ 不可取消 |
| 延遲執行 (Lazy) | ✅ 需要訂閱才開始 | ❌ 建立後立即執行 |
| 運算子支援 | ✅ 有 RxJS operators | ❌ 沒有 |
| 資料流型態 | Stream (事件序列) | Single Value (單一值) |

<br />

## 最佳實務建議

- 取消訂閱：在 Angular 的 `ngOnDestroy` 中呼叫 `unsubscribe()`。

- 用運算子處理資料：不要在 `subscribe` 內寫太多。

- 用 `pipe()` 串接運算子：讓程式可讀性更高。

- 避免巢狀 `subscribe()`：改用 `switchMap`、`mergeMap` 等平展 (Flatten) 運算子。

<br />

## 總結

- RxJS 是非同步處理的強大工具。

- 核心概念：`Observable` → `Operators` → `Observer` → `Subscription`。

- 適合處理事件流、HTTP、WebSocket、計時器等。

- 透過運算子讓資料處理流程清晰、可維護。
