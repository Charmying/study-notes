# Prototype (原型模式)

Prototype (原型模式) 是一種創建型設計模式，透過 Clone 現有物件來創建新物件，而無需依賴具體類別。

這種模式允許系統獨立於物件創建，提升靈活性，尤其適合複雜物件或創建成本高的場景。

<br />

## 動機

軟體開發中，常需創建相似物件，例如

- 遊戲中生成多個類似敵人或物品，僅屬性稍異。

- 圖形編輯器中 Clone 形狀，例如：圓形或矩形。

- 配置管理中 Clone 設定物件，避免重複初始化。

直接使用建構函數創建會導致重複代碼或高成本運算。

Prototype 模式透過 Clone 原型物件，解決此問題。

<br />

## 結構

Prototype 模式的結構包含以下元素

- 原型介面 (Prototype Interface)：定義 Clone 方法的介面。

- 具體原型 (Concrete Prototype)：實作原型介面，提供 Clone 功能。

- 客戶端 (Client)：使用原型創建新物件。

以下是 Prototype 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLurhNtnSQ5J_lcFvtN3HBWvShCAqajIajCJbK8ACeloI-fB4XLgERbKb3GLaZEoSzBrT1Ki498yNBLydB137lQkltbwYd8XYNd91ONApZdvoKNfPQaacpWo-bpdknlWXY5q6nJewU7QIOlbqDgNWhGQm00" width="100%" />

<br />

## 實現方式

- 基本實現

    假設 Clone 一個形狀物件。

    ```java
    import java.util.HashMap;
    import java.util.Map;

    /** 原型介面 */
    public interface Shape extends Cloneable {
        Shape clone();
        void draw();
    }

    /** 具體原型：圓形 */
    public class Circle implements Shape {
        private int radius;

        public Circle(int radius) {
            this.radius = radius;
        }

        @Override
        public Shape clone() {
            try {
                return (Shape) super.clone();
            } catch (CloneNotSupportedException e) {
                return null;
            }
        }

        @Override
        public void draw() {
            System.out.println("Drawing a circle with radius " + radius);
        }

        public void setRadius(int radius) {
            this.radius = radius;
        }
    }

    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Circle prototype = new Circle(10);
            Circle clone = (Circle) prototype.clone();
            clone.setRadius(20);
            prototype.draw(); // Drawing a circle with radius 10
            clone.draw();     // Drawing a circle with radius 20
        }
    }
    ```

    特點：透過 clone 方法複製物件，允許修改 Clone 版本而不影響原型。

- 深拷貝實現

    處理包含引用類型的物件。

    ```java
    import java.io.*;

    /** 具體原型：包含地圖的物件 */
    public class Config implements Serializable, Cloneable {
        private Map<String, String> settings = new HashMap<>();

        public Config() {
            settings.put("theme", "dark");
        }

        public Config deepClone() {
            try {
                ByteArrayOutputStream bos = new ByteArrayOutputStream();
                ObjectOutputStream oos = new ObjectOutputStream(bos);
                oos.writeObject(this);

                ByteArrayInputStream bis = new ByteArrayInputStream(bos.toByteArray());
                ObjectInputStream ois = new ObjectInputStream(bis);
                return (Config) ois.readObject();
            } catch (Exception e) {
                return null;
            }
        }

        public void setSetting(String key, String value) {
            settings.put(key, value);
        }

        @Override
        public String toString() {
            return settings.toString();
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Config prototype = new Config();
            Config clone = prototype.deepClone();
            clone.setSetting("theme", "light");
            System.out.println(prototype); // {theme=dark}
            System.out.println(clone);     // {theme=light}
        }
    }
    ```

    特點：使用序列化實現深拷貝，確保引用類型獨立。

- JavaScript 實現 Prototype

    用於 Clone UI 配置物件。

    ```javascript
  	/** 原型物件 */
  	class UIConfig {
  	  constructor() {
  	    this.theme = 'dark';
  	    this.fontSize = 14;
  	  }

  	  clone() {
  	    return Object.assign(Object.create(Object.getPrototypeOf(this)), this);
  	  }
  	}



  	// 使用範例
  	const prototype = new UIConfig();
  	const clone = prototype.clone();
  	clone.theme = 'light';
  	console.log(prototype.theme); // dark
  	console.log(clone.theme);     // light
    ```

    特點：使用 `Object.assign` 實現淺拷貝，適合簡單物件。

- TypeScript 實現 Prototype

    用於 Clone 狀態物件。

    ```typescript
  	/** 原型介面 */
  	interface State extends Cloneable {
  	  clone(): State;
  	}

  	/** 具體原型 */
  	class AppState implements State {
  	  public user: string = 'guest';
  	  public cart: string[] = [];

  	  clone(): AppState {
  	    const clone = new AppState();
  	    clone.user = this.user;
  	    clone.cart = [...this.cart]; // 深拷貝陣列
  	    return clone;
  	  }
  	}



  	/** 使用範例 */
  	const prototype = new AppState();
  	prototype.cart.push('item1');
  	const clone = prototype.clone();
  	clone.user = 'admin';
  	clone.cart.push('item2');
  	console.log(prototype); // { user: 'guest', cart: [ 'item1' ] }
  	console.log(clone);     // { user: 'admin', cart: [ 'item1', 'item2' ] }
    ```

    特點：手動複製屬性，確保陣列進行深拷貝。

- Angular 實現 Prototype

    使用服務 Clone 元件設定。

    ```typescript
  	/** shape.service.ts */
  	import { Injectable } from '@angular/core';

  	export interface Shape {
  	  clone(): Shape;
  	  draw(): void;
  	}

  	@Injectable()
  	export class Circle implements Shape {
  	  radius: number = 10;

  	  clone(): Circle {
  	    const clone = new Circle();
  	    clone.radius = this.radius;
  	    return clone;
  	  }

  	  draw() {
  	    console.log(`Drawing circle with radius ${this.radius}`);
  	  }
  	}

  	@Injectable()
  	export class ShapeService {
  	  private prototype: Shape;

  	  constructor(private circle: Circle) {
  	    this.prototype = circle;
  	  }

  	  getClone() {
  	    return this.prototype.clone();
  	  }
  	}



  	/** app.module.ts */
  	import { NgModule } from '@angular/core';
  	import { BrowserModule } from '@angular/platform-browser';
  	import { AppComponent } from './app.component';
  	import { Circle, ShapeService } from './shape.service';

  	@NgModule({
  	  declarations: [AppComponent],
  	  imports: [BrowserModule],
  	  providers: [Circle, ShapeService],
  	  bootstrap: [AppComponent]
  	})
  	export class AppModule { }



  	/** app.component.ts */
  	import { Component } from '@angular/core';
  	import { ShapeService } from './shape.service';

  	@Component({
  	  selector: 'app-root',
  	  template: `<button (click)="cloneShape()">Clone 形狀</button>`
  	})
  	export class AppComponent {
  	  constructor(private shapeService: ShapeService) {}

  	  cloneShape() {
  	    const clone = this.shapeService.getClone();
  	    clone.radius = 20;
  	    clone.draw(); // Drawing circle with radius 20
  	  }
  	}
    ```

    特點：Angular 服務管理原型，支援元件 Clone。

- React 實現 Prototype

    使用物件 Clone 狀態。

    ```javascript
  	/** StatePrototype.js */
  	class AppState {
  	  constructor() {
  	    this.user = 'guest';
  	    this.cart = [];
  	  }

  	  clone() {
  	    const clone = new AppState();
  	    clone.user = this.user;
  	    clone.cart = [...this.cart]; // 深拷貝陣列
  	    return clone;
  	  }
  	}



  	/** App.jsx */
  	import React, { useState } from 'react';

  	const App = () => {
  	  const prototype = new AppState();
  	  const [state, setState] = useState(prototype);

  	  const cloneState = () => {
  	    const clone = state.clone();
  	    clone.user = 'admin';
  	    clone.cart.push('item');
  	    setState(clone);
  	  };

  	  return (
  	    <div>
  	      <button onClick={cloneState}>Clone 狀態</button>
  	      <p>User: {state.user}</p>
  	      <p>Cart: {state.cart.join(', ')}</p>
  	    </div>
  	  );
  	};

  	export default App;
    ```

    特點：結合 React 狀態管理，Clone 應用狀態，確保陣列深拷貝。

<br />

## 應用場景

Prototype 模式適用於以下場景

- 物件創建成本高，例如：資料庫查詢或複雜初始化。

- 需要生成相似物件家族。

- 前端中 Clone UI 設定或狀態物件。

例如：Java 的 java.lang.Object 提供 clone 方法作為基礎。

<br />

## 優缺點

### 優點

- 減少創建成本：避免重複初始化。

- 靈活性：動態生成物件而不依賴類別。

- 簡化程式碼：隱藏創建細節。

- 易於擴展：新增原型無需修改客戶端。

### 缺點

- Clone 複雜：深拷貝需小心處理引用。

- 初始化問題：Clone 可能遺漏狀態。

- 語言依賴：需支援 Clone 機制。

<br />

## 注意事項

- 深拷貝 vs 淺拷貝：根據需求選擇拷貝深度。

- 原型註冊：使用註冊表管理多個原型。

- 序列化：語言 (例如：Java) 使用序列化實現深拷貝。

- 避免濫用：簡單物件可直接創建。

<br />

## 與其他模式的關係

- 與 Abstract Factory：Prototype 可作為替代，透過 Clone 生成產品。

- 與 Builder：Prototype 聚焦 Clone，Builder 聚焦分步建構。

- 與 Factory Method：Prototype 避免子類別爆炸。

- 與 Singleton：可結合確保唯一原型。

<br />

## 總結

Prototype 模式透過 Clone 提供有效方式創建物件，適合高成本或相似物件場景。

在前端中，此模式適用於 UI 設定或狀態複製。

理解 Prototype 有助於優化物件生成，提升系統效能。
