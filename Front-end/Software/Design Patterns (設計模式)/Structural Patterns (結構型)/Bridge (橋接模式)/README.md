# Bridge (橋接模式)

Bridge (橋接模式) 是一種結構型設計模式，將抽象部分與實現部分分離，使二者可獨立變化。

這種模式避免類別爆炸，適合多維變化系統，例如：形狀與顏色組合。

<br />

## 動機

軟體開發中，常遇到多維變化需求，例如

- GUI 系統中形狀 (例如：圓形、矩形) 與顏色 (例如：紅、藍) 組合，若直接繼承會產生大量子類別。

- 裝置驅動程式，需支援多種平台與硬體類型。

- 前端 UI 元件，需支援多種主題與行為。

直接繼承會導致類別數量急劇增加，難以維護。

Bridge 模式透過分離抽象與實現，解決此問題。

<br />

## 結構

Bridge 模式的結構包含以下元素

- 抽象部分 (Abstraction)：定義高層介面，維護實現部分的引用。

- 精煉抽象 (Refined Abstraction)：擴展抽象部分，提供具體操作。

- 實現介面 (Implementor)：定義低層介面。

- 具體實現 (Concrete Implementor)：實作實現介面。

以下是 Bridge 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLurhNtnSQ5BvjNFEre0mdmSYKc5PSK9IQNA2Jd91ONApX2kPdvUGhLl5mA2heAcRa5EQcvgNab-KKALWgU21v8MbiXlo2rA16aNaEJbwkMbmjcrVDD-vwtTa8iX5W5iI4eDIqpBpK5moBS9ZrTl-nv_xudkxjVpbq4CIaphoIrA2qnEHNPEHZ6WEJGZMhT_dBr58Y1o8vopizBBaejIINHk9VJvppPtmGn2Db3DZMwkbWyYgf8LzSEnVbM2agbnQd5IhnSoA8sDNfws9p7o-MGcfS2Z5e0" width="100%" />

<br />

## 實現方式

- 基本實現

    假設分離形狀與顏色。

    ```java
    /** 實現介面：顏色 */
    public interface Color {
        String getColor();
    }

    /** 具體實現：紅色 */
    public class Red implements Color {
        @Override
        public String getColor() {
            return "Red";
        }
    }

    /** 具體實現：藍色 */
    public class Blue implements Color {
        @Override
        public String getColor() {
            return "Blue";
        }
    }

    /** 抽象部分：形狀 */
    public abstract class Shape {
        protected Color color;

        public Shape(Color color) {
            this.color = color;
        }

        public abstract void draw();
    }

    /** 精煉抽象：圓形 */
    public class Circle extends Shape {
        public Circle(Color color) {
            super(color);
        }

        @Override
        public void draw() {
            System.out.println("Drawing a " + color.getColor() + " circle");
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Color red = new Red();
            Shape circle = new Circle(red);
            circle.draw(); // Drawing a Red circle

            Color blue = new Blue();
            circle = new Circle(blue);
            circle.draw(); // Drawing a Blue circle
        }
    }
    ```

    特點：形狀與顏色獨立變化，避免類別爆炸。

- JavaScript 實現 Bridge

    分離 UI 元件與主題。

    ```javascript
    /** 實現介面：主題 */
    class Theme {
      getStyle() {
        throw new Error("Method 'getStyle()' must be implemented.");
      }
    }

    /** 具體實現：淺色主題 */
    class LightTheme extends Theme {
      getStyle() {
        return { background: 'white', color: 'black' };
      }
    }

	/** 具體實現：深色主題 */
	class DarkTheme extends Theme {
	  getStyle() {
	    return { background: 'black', color: 'white' };
	  }
	}

	/** 抽象部分：UI 元件 */
	class UIElement {
	  constructor(theme) {
	    this.theme = theme;
	  }

	  render() {
	    throw new Error("Method 'render()' must be implemented.");
	  }
	}

    /** 精煉抽象：按鈕 */
    class Button extends UIElement {
      render() {
        const style = this.theme.getStyle();
        return `<button style="background: ${style.background}; color: ${style.color};">按鈕</button>`;
      }
    }



    /** 使用範例 */
	const lightTheme = new LightTheme();
	const button = new Button(lightTheme);
	console.log(button.render()); // <button style="background: white; color: black;">按鈕</button>

	const darkTheme = new DarkTheme();
	button.theme = darkTheme;
	console.log(button.render()); // <button style="background: black; color: white;">按鈕</button>
    ```

    特點：主題與元件分離，易於切換樣式。

- TypeScript 實現 Bridge

    分離渲染引擎與圖形。

    ```typescript
	/** 實現介面：渲染引擎 */
	interface Renderer {
	  renderShape(shapeType: string): string;
	}

    /** 具體實現：SVG 渲染 */
    class SVGRenderer implements Renderer {
      renderShape(shapeType: string): string {
        return `<svg>${shapeType}</svg>`;
      }
    }

    /** 具體實現：Canvas 渲染 */
    class CanvasRenderer implements Renderer {
      renderShape(shapeType: string): string {
        return `Canvas: ${shapeType}`;
      }
    }

    /** 抽象部分：圖形 */
    abstract class Graphic {
      protected renderer: Renderer;

	  constructor(renderer: Renderer) {
	    this.renderer = renderer;
	  }

      abstract draw(): string;
    }

    /** 精煉抽象：圓形 */
    class CircleGraphic extends Graphic {
      draw(): string {
        return this.renderer.renderShape("Circle");
      }
    }

    /** 使用範例 */
    const svgRenderer = new SVGRenderer();
    const circle = new CircleGraphic(svgRenderer);
    console.log(circle.draw()); // <svg>Circle</svg>

    const canvasRenderer = new CanvasRenderer();
    circle.renderer = canvasRenderer;
    console.log(circle.draw()); // Canvas: Circle
    ```

    特點：TypeScript 確保型別安全，適合多渲染引擎支援。

- Angular 實現 Bridge

    分離資料來源與顯示元件。

    ```typescript
    /** data.service.ts */
    import { Injectable } from '@angular/core';

    export interface DataSource {
      getData(): string[];
    }

    @Injectable()
    export class LocalDataSource implements DataSource {
      getData(): string[] {
        return ['Local Data 1', 'Local Data 2'];
      }
    }

    @Injectable()
    export class RemoteDataSource implements DataSource {
      getData(): string[] {
        return ['Remote Data 1', 'Remote Data 2'];
      }
    }

    @Injectable()
    export abstract class DisplayComponent {
      protected dataSource: DataSource;

      constructor(dataSource: DataSource) {
        this.dataSource = dataSource;
      }

      abstract display(): string;
    }

    @Injectable()
    export class ListDisplay extends DisplayComponent {
      display(): string {
        const data = this.dataSource.getData();
        return `<ul><li>${data.join('</li><li>')}</li></ul>`;
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { LocalDataSource, RemoteDataSource, ListDisplay } from './data.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [LocalDataSource, RemoteDataSource, ListDisplay],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { LocalDataSource, RemoteDataSource, ListDisplay } from './data.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="displayLocal()">顯示本地</button> <button (click)="displayRemote()">顯示遠端</button>`
    })
    export class AppComponent {
      constructor(private localSource: LocalDataSource, private remoteSource: RemoteDataSource, private listDisplay: ListDisplay) {}

      displayLocal() {
        this.listDisplay.dataSource = this.localSource;
        console.log(this.listDisplay.display()); // <ul><li>Local Data 1</li><li>Local Data 2</li></ul>
      }

      displayRemote() {
        this.listDisplay.dataSource = this.remoteSource;
        console.log(this.listDisplay.display()); // <ul><li>Remote Data 1</li><li>Remote Data 2</li></ul>
      }
    }
    ```

    特點：Angular 服務分離資料來源與顯示，提升模組化。

- React 實現 Bridge

    分離行為與 UI 元件。

    ```javascript
    /** BehaviorBridge.js */
    class Behavior {
      handleClick() {
        throw new Error("Method 'handleClick()' must be implemented.");
      }
    }

    class LogBehavior extends Behavior {
      handleClick() {
        console.log("Clicked!");
      }
    }

    class AlertBehavior extends Behavior {
      handleClick() {
        alert("Clicked!");
      }
    }

    class UIComponent {
      constructor(behavior) {
        this.behavior = behavior;
      }

      render() {
        return <button onClick={() => this.behavior.handleClick()}>按鈕</button>;
      }
    }



    /** App.jsx */
    import React from 'react';

    const App = () => {
      const logBehavior = new LogBehavior();
      const component = new UIComponent(logBehavior);

      return (
        <div>
          {component.render()}
        </div>
      );
    };

    export default App;
    ```

    特點：行為與元件分離，易於切換事件處理。

<br />

## 應用場景

Bridge 模式適用於以下場景

- 多維變化系統，例如：GUI 元件與樣式。

- 需要獨立擴展抽象與實現時。

- 前端中分離 UI 與主題或行為。

例如：Java 的 JDBC 使用 Bridge 分離 API 與驅動實現。

<br />

## 優缺點

### 優點

- 解耦：抽象與實現獨立變化。

- 避免類別爆炸：減少子類別數量。

- 靈活性：易於新增抽象或實現。

- 符合開閉原則：擴展無需修改既有程式碼。

### 缺點

- 程式碼複雜度：引入額外抽象層級。

- 理解難度：初學者可能難以掌握。

- 效能開銷：間接呼叫可能略增開銷。

<br />

## 注意事項

- 分離準則：確保抽象與實現有明確界線。

- 組合優先：偏好物件組合而非繼承。

- 介面設計：實現介面應聚焦低層操作。

- 避免濫用：簡單變化可直接使用繼承。

<br />

## 與其他模式的關係

- 與 Adapter：Bridge 分離抽象與實現，Adapter 轉換現有介面。

- 與 Abstract Factory：Bridge 可與抽象工廠結合創建實現。

- 與 Strategy：Bridge 處理結構變化，Strategy 處理演算法變化。

- 與 Composite：Bridge 可在組合模式中使用。

<br />

## 總結

Bridge 模式透過分離抽象與實現提供靈活架構，適合多維變化系統。

在前端中，此模式適用於 UI 主題或行為分離。

理解 Bridge 有助於設計可擴展系統，提升程式碼可維護性。
