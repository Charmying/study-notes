# Flyweight (享元模式)

Flyweight (享元模式) 是一種結構型設計模式，透過共享物件減少記憶體使用，適合大量相似物件的場景。

這種模式將物件狀態分為內部狀態 (共享) 與外部狀態 (非共享)，提升系統效能。

<br />

## 動機

軟體開發中，常需處理大量相似物件，例如

- 文字編輯器中每個字元需儲存字型與樣式，若獨立儲存耗費記憶體。

- 遊戲中重複渲染相似角色或圖形，例如：樹木或敵人。

- 前端中大量重複 UI 元件，例如：按鈕或圖標。

為每個物件創建獨立實例會導致記憶體浪費。

Flyweight 模式透過共享內部狀態，解決此問題。

<br />

## 結構

Flyweight 模式的結構包含以下元素

- 享元介面 (Flyweight Interface)：定義共享物件的操作。

- 具體享元 (Concrete Flyweight)：實作享元介面，儲存內部狀態。

- 享元工廠 (Flyweight Factory)：管理共享物件池，提供享元實例。

- 客戶端 (Client)：維護外部狀態，透過享元工廠獲取享元。

以下是 Flyweight 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuiclrqzRc9xkxNyvT11BWvShCAqajIajCJbLmowaiJyrCpoXHgERbKb3GLiWlI2rABCdCpzD8hIWfoimhpamEBaaiITNavQhbvO8P-RHr-ylLKo06GunCpaaiBbPmpizBBaejIKKpLbS1Q2EIOQHO1R7awVQbJtSlGBOAReLROd99Vb4bpAOqc7YnWfM2Rs81nAxqr1Au1WrKnsW2rS7bKAn-ENtEa_rD44iHFhAfqTF3z2YI2fY3ydLrxP1DTaZDIm562m00" width="100%" />

<br />

## 實現方式

- 基本實現

    假設管理文字編輯器的字元樣式。

    ```java
    /** 享元介面 */
    public interface CharacterFlyweight {
        void render(String extrinsicState);
    }

    /** 具體享元 */
    public class Character implements CharacterFlyweight {
        private String font; // 內部狀態

        public Character(String font) {
            this.font = font;
        }

        @Override
        public void render(String extrinsicState) {
            System.out.println("Character with font " + font + " at position " + extrinsicState);
        }
    }

    /** 享元工廠 */
    public class CharacterFactory {
        private java.util.Map<String, CharacterFlyweight> flyweights = new java.util.HashMap<>();

        public CharacterFlyweight getCharacter(String font) {
            CharacterFlyweight flyweight = flyweights.get(font);
            if (flyweight == null) {
                flyweight = new Character(font);
                flyweights.put(font, flyweight);
            }
            return flyweight;
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            CharacterFactory factory = new CharacterFactory();
            CharacterFlyweight char1 = factory.getCharacter("Arial");
            char1.render("1"); // Character with font Arial at position 1

            CharacterFlyweight char2 = factory.getCharacter("Arial");
            char2.render("2"); // Character with font Arial at position 2

            System.out.println(char1 == char2); // true (共享同一實例)
        }
    }
    ```

    特點：共享字型內部狀態，減少記憶體使用。

- JavaScript 實現 Flyweight

    管理 UI 圖標。

    ```javascript
    /** 享元介面 */
    class IconFlyweight {
      constructor(name) {
        this.name = name; // 內部狀態
      }

      render(position) {
        throw new Error("Method 'render()' must be implemented.");
      }
    }

    /** 具體享元 */
    class Icon extends IconFlyweight {
      render(position) {
        return `<i class="${this.name}" style="position: ${position}"></i>`;
      }
    }

    /** 享元工廠 */
    class IconFactory {
      constructor() {
        this.icons = {};
      }

      getIcon(name) {
        if (!this.icons[name]) {
          this.icons[name] = new Icon(name);
        }
        return this.icons[name];
      }
    }



    /** 使用範例 */
    const factory = new IconFactory();
    const icon1 = factory.getIcon('star');
    console.log(icon1.render('top: 10px')); // <i class="star" style="position: top: 10px"></i>

    const icon2 = factory.getIcon('star');
    console.log(icon2.render('top: 20px')); // <i class="star" style="position: top: 20px"></i>
    console.log(icon1 === icon2);           // true
    ```

    特點：共享圖標內部狀態，減少 DOM 物件數量。

- TypeScript 實現 Flyweight

    管理遊戲角色圖形。

    ```typescript
    /** 享元介面 */
    interface SpriteFlyweight {
      render(extrinsicState: string): string;
    }

    /** 具體享元 */
    class Sprite implements SpriteFlyweight {
      private spriteType: string; // 內部狀態

      constructor(spriteType: string) {
        this.spriteType = spriteType;
      }

      render(extrinsicState: string): string {
        return `<img src="${this.spriteType}.png" style="${extrinsicState}" />`;
      }
    }

    /** 享元工廠 */
    class SpriteFactory {
      private sprites: { [key: string]: SpriteFlyweight } = {};

      getSprite(spriteType: string): SpriteFlyweight {
        if (!this.sprites[spriteType]) {
          this.sprites[spriteType] = new Sprite(spriteType);
        }
        return this.sprites[spriteType];
      }
    }



    /** 使用範例 */
    const factory = new SpriteFactory();
    const sprite1 = factory.getSprite('enemy');
    console.log(sprite1.render('left: 10px')); // <img src="enemy.png" style="left: 10px" />

    const sprite2 = factory.getSprite('enemy');
    console.log(sprite2.render('left: 20px')); // <img src="enemy.png" style="left: 20px" />
    console.log(sprite1 === sprite2);          // true
    ```

    特點：TypeScript 確保型別安全，共享角色圖形。

- Angular 實現 Flyweight

    管理大量按鈕樣式。

    ```typescript
    /** button.service.ts */
    import { Injectable } from '@angular/core';

    export interface ButtonFlyweight {
      render(style: string): string;
    }

    @Injectable()
    export class Button implements ButtonFlyweight {
      constructor(private type: string) {} // 內部狀態

      render(style: string): string {
        return `<button class="${this.type}" style="${style}">Button</button>`;
      }
    }

    @Injectable()
    export class ButtonFactory {
      private buttons: { [key: string]: ButtonFlyweight } = {};

      getButton(type: string): ButtonFlyweight {
        if (!this.buttons[type]) {
          this.buttons[type] = new Button(type);
        }
        return this.buttons[type];
      }
    }



    /** app.module.ts */
    import { NgModule } from '@angular/core';
    import { BrowserModule } from '@angular/platform-browser';
    import { AppComponent } from './app.component';
    import { ButtonFactory } from './button.service';

    @NgModule({
      declarations: [AppComponent],
      imports: [BrowserModule],
      providers: [ButtonFactory],
      bootstrap: [AppComponent]
    })
    export class AppModule { }



    /** app.component.ts */
    import { Component } from '@angular/core';
    import { ButtonFactory } from './button.service';

    @Component({
      selector: 'app-root',
      template: `<button (click)="renderButtons()">渲染按鈕</button>`
    })
    export class AppComponent {
      constructor(private factory: ButtonFactory) {}

      renderButtons() {
        const button1 = this.factory.getButton('primary');
        console.log(button1.render('margin: 10px')); // <button class="primary" style="margin: 10px">Button</button>

        const button2 = this.factory.getButton('primary');
        console.log(button2.render('margin: 20px')); // <button class="primary" style="margin: 20px">Button</button>
        console.log(button1 === button2);            // true
      }
    }
    ```

    特點：Angular 服務管理按鈕樣式，減少記憶體使用。

- React 實現 Flyweight

    管理大量圖標。

    ```javascript
    /** IconFlyweight.js */
    class Icon {
      constructor(type) {
        this.type = type; // 內部狀態
      }

      render(style) {
        return <i className={this.type} style={{ ...style }} />;
      }
    }

    class IconFactory {
      constructor() {
        this.icons = {};
      }

      getIcon(type) {
        if (!this.icons[type]) {
          this.icons[type] = new Icon(type);
        }
        return this.icons[type];
      }
    }



    /** App.jsx */
    import React from 'react';

    const App = () => {
      const factory = new IconFactory();
      const icon1 = factory.getIcon('star');
      const icon2 = factory.getIcon('star');

      return (
        <div>
          {icon1.render({ margin: '10px' })}
          {icon2.render({ margin: '20px' })}
        </div>
      );
    };

    export default App;
    ```

    特點：共享圖標實例，優化 React 渲染效能。

<br />

## 應用場景

Flyweight 模式適用於以下場景

- 處理大量相似物件，例如：字元、圖標或角色。

- 記憶體資源有限，需共享內部狀態。

- 前端中優化大量重複 UI 元件或資源。

例如：Java 的 `String` 類別使用 Flyweight 共享字串常量。

<br />

## 優缺點

### 優點

- 節省記憶體：共享內部狀態減少實例數量。

- 提高效能：降低物件創建與管理成本。

- 靈活性：外部狀態允許動態變化。

- 符合單一職責原則：分離內部與外部狀態。

### 缺點

- 程式碼複雜度：需額外管理享元工廠。

- 狀態管理：內外部狀態分離增加設計難度。

- 執行效能：查詢享元池可能略增開銷。

<br />

## 注意事項

- 內外部狀態：明確區分共享與非共享狀態。

- 享元池管理：確保工廠高效查詢與創建。

- 深拷貝 vs 淺拷貝：Clone 享元時選擇合適拷貝方式。

- 避免濫用：少量物件可直接創建。

<br />

## 與其他模式的關係

- 與 Composite：Flyweight 可與 Composite 結合管理大量葉子。

- 與 Factory：Flyweight 常與工廠模式結合管理共享物件。

- 與 Singleton：享元工廠可實現為單例。

- 與 Strategy：Flyweight 可搭配策略模式處理外部狀態。

<br />

## 總結

Flyweight 模式透過共享內部狀態優化記憶體使用，適合大量相似物件場景。

在前端中，此模式適用於圖標或 UI 元件優化。

理解 Flyweight 有助於設計高效系統，提升程式碼效能與可維護性。
