# Command (命令模式)

Command (命令模式) 是一種行為型設計模式，將請求封裝為物件，允許參數化請求、排隊或記錄請求，並支援可撤銷操作。

這種模式解耦發送者與接收者，適合複雜操作管理。

<br />

## 動機

軟體開發中，常需將操作抽象化，例如

- GUI 系統中，按鈕觸發不同動作，例如：開啟檔案或列印。

- 交易系統中，需記錄與撤銷操作，例如：購買或取消訂單。

- 前端中，管理用戶動作，例如：復原與重做功能。

直接將操作寫死在發送者中導致耦合度高且難以擴展。

Command 模式透過封裝命令物件，解決此問題。

<br />

## 結構

Command 模式的結構包含以下元素

- 命令介面 (Command Interface)：定義執行命令的方法。

- 具體命令 (Concrete Command)：實作命令介面，綁定接收者與動作。

- 調用者 (Invoker)：負責觸發命令，不需知道具體細節。

- 接收者 (Receiver)：執行實際動作的類別。

- 客戶端 (Client)：建立命令並設定調用者。

以下是 Command 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuEd7lazrBdkpkVZbt4KY0boiphoIrA2qnELN1EJytDp4lHQ6Qbqj1GLiXjI8rkRGaLKEJbwkMbmjkGElsbwkdG8o1692SarXS3DISbroKMfAAOeYkGb5gScfcMMgHWfL249I9p_GNg_O_dxBYHKChij6UUMNvsK0Ze4OcGssmWZaOOc1nQWcKhu6XGXF5JfWoLAkVzIrzDcKRcjKmDyF2936v93C_3qtdo-bpdknlWcY3UT-cHayFFKn0igY1fAjhXnGiC7_cWuJXUXnIyrA04GW00" width="100%" />

<br />

## 實現方式

- 基本實現
    假設控制燈的開關。

    ```java
    /** 命令介面 */
    public interface Command {
        void execute();
    }

    /** 接收者 */
    public class Light {
        public void turnOn() {
            System.out.println("Light is on");
        }

        public void turnOff() {
            System.out.println("Light is off");
        }
    }

    /** 具體命令：開燈 */
    public class LightOnCommand implements Command {
        private Light light;

        public LightOnCommand(Light light) {
            this.light = light;
        }

        @Override
        public void execute() {
            light.turnOn();
        }
    }

    /** 調用者 */
    public class RemoteControl {
        private Command command;

        public void setCommand(Command command) {
            this.command = command;
        }

        public void pressButton() {
            command.execute();
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Light light = new Light();
            Command lightOn = new LightOnCommand(light);
            RemoteControl remote = new RemoteControl();
            remote.setCommand(lightOn);
            remote.pressButton(); // Light is on
        }
    }
    ```

    特點：封裝燈開關操作，易於擴展其他命令。

- JavaScript 實現 Command

    管理 UI 按鈕動作。

	```javascript
	/** 命令介面 */
	class Command {
	  execute() {
	    throw new Error("Method 'execute()' must be implemented.");
	  }
	}

	/** 接收者 */
	class Document {
	  save() {
	    console.log("Document saved");
	  }
	}

	/** 具體命令：儲存文件 */
	class SaveCommand extends Command {
	  constructor(document) {
	    super();
	    this.document = document;
	  }

	  execute() {
	    this.document.save();
	  }
	}

	/** 調用者 */
	class Menu {
	  constructor() {
	    this.command = null;
	  }

  	setCommand(command) {
  	  this.command = command;
  	}

	  click() {
	    this.command.execute();
	  }
	}



	/** 使用範例 */
	const document = new Document();
	const saveCommand = new SaveCommand(document);
	const menu = new Menu();
	menu.setCommand(saveCommand);
	menu.click(); // Document saved
	```

    特點：封裝 UI 動作，支援動態綁定。

- TypeScript 實現 Command

    管理復原操作。

	```typescript
	/** 命令介面 */
	interface Command {
	  execute(): void;
	  undo(): void;
	}

	/** 接收者 */
	class TextEditor {
	  private text: string = '';

  	  addText(newText: string) {
  	    this.text += newText;
  	    console.log("Text added: " + this.text);
  	  }

	  removeText() {
	    this.text = this.text.slice(0, -1);
	    console.log("Text removed: " + this.text);
	  }
    }

	/** 具體命令：添加文字 */
	class AddTextCommand implements Command {
	  constructor(private editor: TextEditor, private text: string) {}

  	  execute(): void {
  	    this.editor.addText(this.text);
  	  }

	  undo(): void {
	    for (let i = 0; i < this.text.length; i++) {
	      this.editor.removeText();
	    }
	  }
	}

	/** 調用者 */
	class EditorInvoker {
	  private command: Command | null = null;

  	  setCommand(command: Command) {
  	    this.command = command;
  	  }

	  executeCommand() {
	    if (this.command) {
	      this.command.execute();
	    }
	  }

	  undoCommand() {
	    if (this.command) {
	      this.command.undo();
	    }
	  }
	}



	/** 使用範例 */
	const editor = new TextEditor();
	const addCommand = new AddTextCommand(editor, "Hello");
	const invoker = new EditorInvoker();
	invoker.setCommand(addCommand);
	invoker.executeCommand(); // Text added: Hello
	invoker.undoCommand();    // Text removed: Hell
	                          // Text removed: Hel
	                          // Text removed: He
	                          // Text removed: H
	                          // Text removed: 
	```

    特點：TypeScript 確保型別安全，支援復原功能。

- Angular 實現 Command

    管理服務操作。

	```typescript
	/** command.service.ts */
	import { Injectable } from '@angular/core';

	export interface Command {
	  execute(): void;
	}

	@Injectable()
	export class AlertReceiver {
	  showAlert(message: string) {
	    console.log("Alert: " + message);
	  }
	}

	@Injectable()
	export class AlertCommand implements Command {
	  constructor(private receiver: AlertReceiver, private message: string) {}

	  execute(): void {
	    this.receiver.showAlert(this.message);
	  }
	}

	@Injectable()
	export class CommandInvoker {
	  private command: Command | null = null;

	  setCommand(command: Command) {
	    this.command = command;
	  }

	  executeCommand() {
	    if (this.command) {
	      this.command.execute();
	    }
	  }
	}



	/** app.module.ts */
	import { NgModule } from '@angular/core';
	import { BrowserModule } from '@angular/platform-browser';
	import { AppComponent } from './app.component';
	import { AlertReceiver, AlertCommand, CommandInvoker } from './command.service';

	@NgModule({
	  declarations: [AppComponent],
	  imports: [BrowserModule],
	  providers: [AlertReceiver, AlertCommand, CommandInvoker],
	  bootstrap: [AppComponent]
	})
	export class AppModule { }



	/** app.component.ts */
	import { Component } from '@angular/core';
	import { AlertReceiver, AlertCommand, CommandInvoker } from './command.service';

	@Component({
	  selector: 'app-root',
	  template: `<button (click)="executeAlert()">執行警報</button>`
	})
	export class AppComponent {
	  constructor(private receiver: AlertReceiver, private invoker: CommandInvoker) {
	    const command = new AlertCommand(receiver, "Test alert");
	    invoker.setCommand(command);
	  }

	  executeAlert() {
	    this.invoker.executeCommand(); // Alert: Test alert
	  }
	}
	```

    特點：Angular 服務封裝命令，支援模組化操作。

- React 實現 Command

    管理狀態操作。

	```javascript
	/** CommandPattern.js */
	class Command {
	  execute() {
	    throw new Error("Method 'execute()' must be implemented.");
	  }
	}

	class Counter {
	  constructor() {
	    this.value = 0;
	  }

	  increment() {
	    this.value++;
	    console.log("Value: " + this.value);
	  }
	}

	class IncrementCommand extends Command {
	  constructor(counter) {
	    super();
	    this.counter = counter;
	  }

	  execute() {
	    this.counter.increment();
	  }
	}

	class ButtonInvoker {
	  constructor() {
	    this.command = null;
	  }

	  setCommand(command) {
	    this.command = command;
	  }

	  press() {
	    if (this.command) {
	      this.command.execute();
	    }
	  }
	}



	/** App.jsx */
	import React from 'react';

	const App = () => {
	  const counter = new Counter();
	  const incrementCommand = new IncrementCommand(counter);
	  const button = new ButtonInvoker();
	  button.setCommand(incrementCommand);

	  return (
	    <div>
	      <button onClick={() => button.press()}>遞增</button>
	    </div>
	  );
	};

	export default App;
	```

    特點：封裝 React 狀態操作，支援復原擴展。

<br />

## 應用場景

Command 模式適用於以下場景

- 封裝操作，例如：GUI 動作或交易記錄。

- 支援復原與重做功能。

- 前端中管理用戶動作或事件處理。

例如：Java 的 `javax.swing.Action` 使用 Command 模式處理 GUI 動作。

<br />

## 優缺點

### 優點

- 解耦：發送者與接收者無直接依賴。

- 靈活性：易於新增命令或修改行為。

- 支援復原：記錄命令歷史實現復原。

- 符合單一職責原則：命令專注單一動作。

### 缺點

- 程式碼複雜度：增加命令類別數量。

- 記憶體開銷：大量命令可能耗費記憶體。

- 調試難度：命令鏈可能不易追蹤。

<br />

## 注意事項

- 命令封裝：確保命令包含必要參數。

- 復原支援：設計可撤銷命令。

- 深拷貝 vs 淺拷貝：Clone 命令時選擇合適拷貝方式。

- 避免濫用：簡單操作可直接呼叫。

<br />

## 與其他模式的關係

- 與 Strategy：Command 封裝動作，Strategy 封裝演算法。

- 與 Memento：Command 可與 Memento 結合支援復原。

- 與 Observer：可與 Observer 結合事件通知。

- 與 Composite：Command 可組成宏命令。

<br />

## 總結

Command 模式透過封裝請求提供靈活操作管理，適合動作抽象化場景。

在前端中，此模式適用於 UI 動作或復原功能。

理解 Command 有助於設計可擴展系統，提升程式碼可維護性。
