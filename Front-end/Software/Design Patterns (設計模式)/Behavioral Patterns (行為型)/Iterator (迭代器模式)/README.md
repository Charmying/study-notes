# Iterator (迭代器模式)

Iterator (迭代器模式) 是一種行為型設計模式，提供順序訪問集合元素的方式，而不暴露集合的內部結構。

這種模式允許統一遍歷不同資料結構，適合多種集合操作場景。

<br />

## 動機

軟體開發中，常需遍歷集合中的元素，例如

- 處理陣列、列表、樹或圖形結構中的資料。

- 提供多種遍歷方式，例如：順序、反序或過濾。

- 前端中遍歷資料陣列或 DOM 元素，例如：渲染動態列表。

直接存取集合內部結構導致程式碼耦合度高，難以維護與擴展。Iterator 模式透過抽象迭代過程，解決此問題。

<br />

## 結構

Iterator 模式的結構包含以下元素：

- 聚合介面 (Aggregate Interface)：定義創建迭代器的介面。

- 具體聚合 (Concrete Aggregate)：實作聚合介面，提供具體迭代器。

- 迭代器介面 (Iterator Interface)：定義遍歷操作，例如：檢查是否還有元素與獲取下一個元素。

- 具體迭代器 (Concrete Iterator)：實作迭代器介面，管理遍歷狀態。

- 客戶端 (Client)：透過迭代器介面遍歷集合。

以下是 Iterator 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuqJZhwOIE9xkxNyvT11BWvShCAqajIajCJbLmJ4ylIarFB4bLgERbKb3GLaWkIWNoF87oYINvHHgQ2bOAC0ulLoql5ypGfwtRNwwU0Z4QOcXoJc9niO9pVXxGY99KiWr-iN_jazsBdyvSWTt1C3qmOpCIY_rIAqh0vYNbv-Ua9kP19F9Welv9MQd99TWS3xC9c_kfOi_BwNEUx6-268y849iQFJtCSEBbmWmwNLqx30VnSi6TXc8GGjuXDIy56Fq0" width="100%" />

<br />

## 實現方式

- 基本實現 (Java，縮排 4 格)

    假設遍歷簡單字串列表。

    ```java
    /** 聚合介面 */
    public interface Aggregate {
        Iterator createIterator();
    }

    /** 具體聚合 */
    public class StringList implements Aggregate {
        private String[] items = {"Apple", "Banana", "Cherry"};

        @Override
        public Iterator createIterator() {
        return new StringIterator(this);
        }

        public int size() {
            return items.length;
        }

        public String get(int index) {
            return items[index];
        }
    }

    /** 迭代器介面 */
    public interface Iterator {
        boolean hasNext();
        String next();
    }

    /** 具體迭代器 */
    public class StringIterator implements Iterator {
        private StringList list;
        private int index = 0;

        public StringIterator(StringList list) {
            this.list = list;
        }

        @Override
        public boolean hasNext() {
            return index < list.size();
        }

        @Override
        public String next() {
            return list.get(index++);
        }
    }

    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Aggregate list = new StringList();
            Iterator iterator = list.createIterator();
            while (iterator.hasNext()) {
                System.out.println(iterator.next());
            }
            // Apple
            // Banana
            // Cherry
        }
    }
    ```

    特點：隱藏列表內部結構，提供統一遍歷方式。

- JavaScript 實現 Iterator

    遍歷資料陣列。

	```javascript
	/** 聚合介面 */
	class Aggregate {
	  createIterator() {
	    throw new Error("Method 'createIterator()' must be implemented.");
	  }
	}

	/** 具體聚合 */
	class DataArray extends Aggregate {
	  constructor(data) {
	    super();
	    this.data = data;
	  }

	  createIterator() {
	    return new DataIterator(this);
	  }

	  getLength() {
	    return this.data.length;
	  }

	  get(index) {
	    return this.data[index];
	  }
	}

	/** 迭代器介面 */
	class Iterator {
	  hasNext() {
	    throw new Error("Method 'hasNext()' must be implemented.");
	  }

	  next() {
	    throw new Error("Method 'next()' must be implemented.");
	  }
	}

	/** 具體迭代器 */
	class DataIterator extends Iterator {
	  constructor(aggregate) {
	    super();
	    this.aggregate = aggregate;
	    this.index = 0;
	  }

	  hasNext() {
	    return this.index < this.aggregate.getLength();
	  }

	  next() {
	    return this.aggregate.get(this.index++);
	  }
	}



	/** 使用範例 */
	const data = new DataArray(['Item 1', 'Item 2', 'Item 3']);
	const iterator = data.createIterator();
	while (iterator.hasNext()) {
	  console.log(iterator.next());
	}
	// Item 1
	// Item 2
	// Item 3
	```

    特點：支援前端陣列遍歷，隱藏內部實現。

- TypeScript 實現 Iterator

    遍歷自訂物件集合。

	```typescript
	/** 聚合介面 */
	interface Aggregate {
	  createIterator(): Iterator;
	}

	/** 具體聚合 */
	class ObjectCollection implements Aggregate {
	  private items: { id: number; name: string }[] = [
	    { id: 1, name: 'Item A' },
	    { id: 2, name: 'Item B' }
	  ];

	  createIterator(): Iterator {
	    return new ObjectIterator(this);
	  }

	  getLength(): number {
	    return this.items.length;
	  }

	  get(index: number): { id: number; name: string } {
	    return this.items[index];
	  }
	}

	/** 迭代器介面 */
	interface Iterator {
	  hasNext(): boolean;
	  next(): { id: number; name: string };
	}

	/** 具體迭代器 */
	class ObjectIterator implements Iterator {
	  private collection: ObjectCollection;
	  private index: number = 0;

	  constructor(collection: ObjectCollection) {
	    this.collection = collection;
	  }

	  hasNext(): boolean {
	    return this.index < this.collection.getLength();
	  }

	  next(): { id: number; name: string } {
	    return this.collection.get(this.index++);
	  }
	}



	/** 使用範例 */
	const collection = new ObjectCollection();
	const iterator = collection.createIterator();
	while (iterator.hasNext()) {
	  console.log(iterator.next().name);
	}
	// Item A
	// Item B
	```

    特點：TypeScript 提供型別安全，適合複雜物件遍歷。

- Angular 實現 Iterator

    遍歷服務中的資料集合。

	```typescript
	/** data.service.ts */
	import { Injectable } from '@angular/core';

	export interface Aggregate {
	  createIterator(): Iterator;
	}

	@Injectable({
	  providedIn: 'root'
	})
	export class DataCollection implements Aggregate {
	  private items: string[] = ['Task 1', 'Task 2', 'Task 3'];

  	  createIterator(): Iterator {
  	    return new DataIterator(this);
  	  }

	  getLength(): number {
	    return this.items.length;
	  }

	  get(index: number): string {
	    return this.items[index];
	  }
	}

	export interface Iterator {
	  hasNext(): boolean;
	  next(): string;
	}

	class DataIterator implements Iterator {
	  private collection: DataCollection;
	  private index: number = 0;

	  constructor(collection: DataCollection) {
	    this.collection = collection;
	  }

	  hasNext(): boolean {
	    return this.index < this.collection.getLength();
	  }

      next(): string {
        return this.collection.get(this.index++);
      }
    }



	/** app.module.ts */
	import { NgModule } from '@angular/core';
	import { BrowserModule } from '@angular/platform-browser';
	import { AppComponent } from './app.component';
	import { DataCollection } from './data.service';

	@NgModule({
	  declarations: [AppComponent],
	  imports: [BrowserModule],
	  providers: [DataCollection],
	  bootstrap: [AppComponent]
	})
	export class AppModule { }



	/** app.component.ts */
	import { Component } from '@angular/core';
	import { DataCollection } from './data.service';

	@Component({
	  selector: 'app-root',
	  template: `<button (click)="iterateData()">遍歷資料</button>`
	})
	export class AppComponent {
	  constructor(private collection: DataCollection) {}

	  iterateData() {
	    const iterator = this.collection.createIterator();
	    while (iterator.hasNext()) {
	      console.log(iterator.next());
	    }
	    // Task 1
	    // Task 2
	    // Task 3
	  }
	}
	```

    特點：Angular 服務實現資料遍歷，支援模組化設計。

- React 實現 Iterator

    遍歷狀態資料。

	```javascript
	/** IteratorPattern.js */
	class Aggregate {
	  createIterator() {
	    throw new Error("Method 'createIterator()' must be implemented.");
	  }
	}

	class StateCollection extends Aggregate {
	  constructor(items) {
	    super();
	    this.items = items;
	  }

	  createIterator() {
	    return new StateIterator(this);
	  }

	  getLength() {
	    return this.items.length;
	  }

	  get(index) {
	    return this.items[index];
	  }
	}

	class Iterator {
	  hasNext() {
	    throw new Error("Method 'hasNext()' must be implemented.");
	  }

	  next() {
	    throw new Error("Method 'next()' must be implemented.");
	  }
	}

	class StateIterator extends Iterator {
	  constructor(collection) {
	    super();
	    this.collection = collection;
	    this.index = 0;
	  }

	  hasNext() {
	    return this.index < this.collection.getLength();
	  }

	  next() {
	    return this.collection.get(this.index++);
	  }
	}



	/** App.jsx */
	import React, { useState } from 'react';

	const App = () => {
	  const [items] = useState(['React', 'Vue', 'Angular']);
	  const collection = new StateCollection(items);
	  const iterator = collection.createIterator();

	  const displayItems = () => {
	    while (iterator.hasNext()) {
	      console.log(iterator.next());
	    }
	  };

	  return (
	    <div>
	      <button onClick={displayItems}>顯示項目</button>
	    </div>
	  );
	};

	export default App;
	```

    特點：結合 React 狀態管理，支援動態列表遍歷。

<br />

## 應用場景

Iterator 模式適用於以下場景

- 統一遍歷不同集合結構，例如：陣列、樹或圖。

- 隱藏集合內部實現，提供安全訪問。

- 前端中處理動態列表渲染或資料遍歷。

例如：Java 的 `java.util.Iterator` 介面廣泛應用於集合框架，像是 `ArrayList` 和 `HashSet`。

<br />

## 優缺點

### 優點

- 解耦：客戶端無需了解集合內部結構。

- 靈活性：支援多種遍歷方式，像是順序或過濾。

- 符合單一職責原則：迭代與集合分離。

- 易於擴展：新增聚合類別無需修改客戶端。

### 缺點

- 程式碼複雜度：需額外定義迭代器類別。

- 效能開銷：動態集合可能需追蹤遍歷狀態。

- 並行修改風險：迭代中修改集合可能導致錯誤。

<br />

## 注意事項

- 迭代安全：避免在遍歷過程中修改集合，否則需使用安全迭代器。

- 多迭代器支援：設計可支援多個同時遍歷的迭代器。

- 深拷貝 vs 淺拷貝：Clone 迭代器時選擇合適拷貝方式。

- 避免濫用：簡單集合可使用語言內建迴圈。

<br />

## 與其他模式的關係

- 與 Composite：Iterator 常與 Composite 結合遍歷樹狀結構。

- 與 Factory Method：可用工廠方法創建迭代器。

- 與 Visitor：Iterator 聚焦遍歷，Visitor 聚焦操作。

- 與 Memento：可結合 Memento 保存迭代狀態。

<br />

## 總結

Iterator 模式透過抽象迭代過程提供統一集合訪問方式，適合多種資料結構處理。

在前端中，此模式適用於動態列表渲染或資料遍歷。

理解 Iterator 有助於設計解耦且可擴展的系統，提升程式碼可維護性與靈活性。
