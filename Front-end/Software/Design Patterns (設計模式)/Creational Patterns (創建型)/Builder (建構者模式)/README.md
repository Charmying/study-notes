# Builder (建構者模式)

Builder (建構者模式) 是一種創建型設計模式，將複雜物件的建構過程與其表示分離，使相同建構過程可創建不同表示。

這種模式允許逐步建構複雜物件，適合需要多個配置選項的場景。

<br />

## 動機

軟體開發中，常需創建具有多個屬性的複雜物件，例如

- 製作客製化產品設定

    例如：電腦硬體配置 (CPU、記憶體、儲存)。

- 產生複雜 UI 元件

    例如：表單或對話框，需動態調整屬性。

- 組裝 API 請求，根據不同參數生成不同配置。

若直接在建構函數中傳遞大量參數，程式碼會變得冗長且難以維護。

Builder 模式透過分步建構，簡化物件創建並提升可讀性。

<br />

## 結構

Builder 模式的結構包含以下元素

- 產品 (Product)：最終生成的複雜物件。

- 抽象建構者 (Abstract Builder)：定義建構各部分的介面。

- 具體建構者 (Concrete Builder)：實作建構者介面，負責建構產品。

- 導演 (Director)：控制建構過程，與建構者協作。

以下是 Builder 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLuFcNHqycD82OlLt9EOd6nGa1HVaffSeb2DI-NWeAkGW5GlIE2wSJBLSlB1TFzh6llYuqBd-xUzR9XmOk6LeWncNabgKLfYScf2ev9nIL5YSabJgMPEIcfHH0ZjHMIGDm0aBaQccWYJZ2HzDGIg4CqD1MiO8v2iVnfw_QNgwUWMGxnWtD-Nd9HQaagYiL03q2zXcGU5TtphAVzwOO-D9UuP1Qb9fVam_sUd9y731EmCIYQNqwVysH_4qGdB0PizFGmV6Abe0Ja9vQa5YlnSg67hqqDfWvUBhWJT7NjCA84Q5vfCTWmNYw7rBmKOD800000" width="100%" />

<br />

## 實現方式

- 基本實現

    ``` java
    /** 產品 */
    public class Computer {
        private String cpu;
        private String ram;
        private String storage;

        public void setCpu(String cpu) {
            this.cpu = cpu;
        }

        public void setRam(String ram) {
            this.ram = ram;
        }

        public void setStorage(String storage) {
            this.storage = storage;
        }

        @Override
        public String toString() {
            return "Computer [CPU=" + cpu + ", RAM=" + ram + ", Storage=" + storage + "]";
        }
    }

    /** 抽象建構者 */
    public interface ComputerBuilder {
        void buildCpu();
        void buildRam();
        void buildStorage();
        Computer getProduct();
    }

    /** 具體建構者：高階電腦 */
    public class HighEndComputerBuilder implements ComputerBuilder {
        private Computer computer;

        public HighEndComputerBuilder() {
            this.computer = new Computer();
        }

        @Override
        public void buildCpu() {
            computer.setCpu("Intel i9");
        }

        @Override
        public void buildRam() {
            computer.setRam("32GB");
        }

        @Override
        public void buildStorage() {
            computer.setStorage("1TB SSD");
        }

        @Override
        public Computer getProduct() {
            return computer;
        }
    }

    /** 導演 */
    public class ComputerDirector {
        public Computer construct(ComputerBuilder builder) {
            builder.buildCpu();
            builder.buildRam();
            builder.buildStorage();
            return builder.getProduct();
        }
    }



    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            ComputerDirector director = new ComputerDirector();
            ComputerBuilder builder = new HighEndComputerBuilder();
            Computer computer = director.construct(builder);
            System.out.println(computer); // Computer [CPU=Intel i9, RAM=32GB, Storage=1TB SSD]
        }
    }
    ```

    特點：分步建構確保靈活配置電腦屬性。

- JavaScript 實現 Builder

    用於建構表單元件。

    ```javascript
	/** 產品 */
	class Form {
	  constructor() {
	    this.fields = [];
	    this.submitButton = null;
	  }

	  addField(field) {
	    this.fields.push(field);
	  }

	  setSubmitButton(button) {
	    this.submitButton = button;
	  }

	  render() {
	    return `<form>${this.fields.join('')}${this.submitButton}</form>`;
	  }
	}

	/** 抽象建構者 */
	class FormBuilder {
	  buildField() {
	    throw new Error("Method 'buildField()' must be implemented.");
	  }

	  buildSubmitButton() {
	    throw new Error("Method 'buildSubmitButton()' must be implemented.");
	  }

	  getProduct() {
	    throw new Error("Method 'getProduct()' must be implemented.");
	  }
	}

	/** 具體建構者：聯絡表單 */
	class ContactFormBuilder extends FormBuilder {
	  constructor() {
	    super();
	    this.form = new Form();
	  }

	  buildField() {
	    this.form.addField('<input type="text" placeholder="姓名" />');
	    this.form.addField('<input type="email" placeholder="電子郵件" />');
	  }

	  buildSubmitButton() {
	    this.form.setSubmitButton('<button>提交</button>');
	  }

	  getProduct() {
	    return this.form;
	  }
	}

	/** 導演 */
	class FormDirector {
	  construct(builder) {
	    builder.buildField();
	    builder.buildSubmitButton();
	    return builder.getProduct();
	  }
	}



    /** 使用範例 */
	const director = new FormDirector();
	const builder = new ContactFormBuilder();
	const form = director.construct(builder);
	console.log(form.render()); // <form><input type="text" placeholder="姓名" /><input type="email" placeholder="電子郵件" /><button>提交</button></form>
    ```

    特點：逐步建構表單，適用於動態生成 UI。

- TypeScript 實現 Builder

    用於建構 API 請求配置。

    ```typescript
  	/** 產品 */
  	class ApiRequest {
  	  private url: string = '';
  	  private method: string = 'GET';
  	  private headers: { [key: string]: string } = {};

  	  setUrl(url: string) {
  	    this.url = url;
  	  }

  	  setMethod(method: string) {
  	    this.method = method;
  	  }

  	  addHeader(key: string, value: string) {
  	    this.headers[key] = value;
  	  }

  	  execute(): Promise<any> {
  	    return fetch(this.url, { method: this.method, headers: this.headers });
  	  }
  	}

  	/** 抽象建構者 */
  	interface RequestBuilder {
  	  buildUrl(): void;
  	  buildMethod(): void;
  	  buildHeaders(): void;
  	  getProduct(): ApiRequest;
  	}

  	/** 具體建構者：認證請求 */
  	class AuthRequestBuilder implements RequestBuilder {
  	  private request: ApiRequest;

  	  constructor() {
  	    this.request = new ApiRequest();
  	  }

  	  buildUrl() {
  	    this.request.setUrl('https://api.example.com/data');
  	  }

  	  buildMethod() {
  	    this.request.setMethod('POST');
  	  }

  	  buildHeaders() {
  	    this.request.addHeader('Authorization', 'Bearer token123');
  	    this.request.addHeader('Content-Type', 'application/json');
  	  }

  	  getProduct() {
  	    return this.request;
  	  }
  	}

  	/** 導演 */
  	class RequestDirector {
  	  construct(builder: RequestBuilder) {
  	    builder.buildUrl();
  	    builder.buildMethod();
  	    builder.buildHeaders();
  	    return builder.getProduct();
  	  }
  	}



  	/** 使用範例 */
  	const director = new RequestDirector();
  	const builder = new AuthRequestBuilder();
  	const request = director.construct(builder);
  	request.execute().then(res => console.log(res));
    ```

    特點：TypeScript 確保型別安全，適合複雜 API 請求配置。

- Angular 實現 Builder

    使用 Angular 服務建構對話框元件。

    ```typescript
  	/** dialog.service.ts */
  	import { Injectable } from '@angular/core';

  	export interface Dialog {
  	  render(): string;
  	}

  	@Injectable()
  	export class DialogComponent implements Dialog {
  	  private title: string = '';
  	  private content: string = '';
  	  private buttons: string[] = [];

      setTitle(title: string) {
        this.title = title;
      }

      setContent(content: string) {
        this.content = content;
      }

      addButton(button: string) {
        this.buttons.push(button);
      }

      render() {
        return `<dialog><h2>${this.title}</h2><p>${this.content}</p>${this.buttons.join('')}</dialog>`;
      }
    }

  	@Injectable()
  	export abstract class DialogBuilder {
  	  abstract buildTitle(): void;
  	  abstract buildContent(): void;
  	  abstract buildButtons(): void;
  	  abstract getProduct(): Dialog;
  	}

  	@Injectable()
  	export class ConfirmDialogBuilder extends DialogBuilder {
  	  private dialog: DialogComponent;

      constructor() {
        super();
        this.dialog = new DialogComponent();
      }

      buildTitle() {
        this.dialog.setTitle('確認對話框');
      }

      buildContent() {
        this.dialog.setContent('是否確定執行此操作？');
      }

      buildButtons() {
        this.dialog.addButton('<button>確認</button>');
        this.dialog.addButton('<button>取消</button>');
      }

      getProduct() {
        return this.dialog;
      }
    }

  	@Injectable()
  	export class DialogDirector {
  	  construct(builder: DialogBuilder) {
  	    builder.buildTitle();
  	    builder.buildContent();
  	    builder.buildButtons();
  	    return builder.getProduct();
  	  }
  	}



  	/** app.module.ts */
  	import { NgModule } from '@angular/core';
  	import { BrowserModule } from '@angular/platform-browser';
  	import { AppComponent } from './app.component';
  	import { ConfirmDialogBuilder, DialogDirector } from './dialog.service';

  	@NgModule({
  	  declarations: [AppComponent],
  	  imports: [BrowserModule],
  	  providers: [ConfirmDialogBuilder, DialogDirector],
  	  bootstrap: [AppComponent]
  	})
  	export class AppModule { }



  	/** app.component.ts */
  	import { Component } from '@angular/core';
  	import { ConfirmDialogBuilder, DialogDirector } from './dialog.service';

  	@Component({
  	  selector: 'app-root',
  	  template: `<button (click)="buildDialog()">建構對話框</button>`
  	})
  	export class AppComponent {
      constructor(
        private builder: ConfirmDialogBuilder,
        private director: DialogDirector
      ) {}

      buildDialog() {
        const dialog = this.director.construct(this.builder);
        console.log(dialog.render());
      }
    }
    ```

    特點：Angular 服務支援分步建構複雜 UI 元件。

- React 實現 Builder

    使用 React 元件建構表單。

    ```javascript
    /** FormBuilder.js */
  	class Form {
  	  constructor() {
  	    this.fields = [];
  	    this.submitButton = null;
  	  }

      addField(field) {
        this.fields.push(field);
      }

      setSubmitButton(button) {
        this.submitButton = button;
      }

      render() {
        return (
          <form>
            {this.fields}
            {this.submitButton}
          </form>
        );
      }
    }

  	class FormBuilder {
  	  buildField() {
  	    throw new Error("Method 'buildField()' must be implemented.");
  	  }

  	  buildSubmitButton() {
  	    throw new Error("Method 'buildSubmitButton()' must be implemented.");
  	  }

  	  getProduct() {
  	    throw new Error("Method 'getProduct()' must be implemented.");
  	  }
  	}

  	class ContactFormBuilder extends FormBuilder {
  	  constructor() {
  	    super();
  	    this.form = new Form();
  	  }

  	  buildField() {
  	    this.form.addField(<input type="text" placeholder="姓名" />);
  	    this.form.addField(<input type="email" placeholder="電子郵件" />);
  	  }

  	  buildSubmitButton() {
  	    this.form.setSubmitButton(<button>提交</button>);
  	  }

  	  getProduct() {
  	    return this.form;
  	  }
  	}

  	class FormDirector {
  	  construct(builder) {
  	    builder.buildField();
  	    builder.buildSubmitButton();
  	    return builder.getProduct();
  	  }
  	}



  	/** FormContext.js */
  	import { createContext, useContext } from 'react';

    const FormContext = createContext(null);

    export const useFormBuilder = () => useContext(FormContext);



  	/** App.jsx */
  	import React from 'react';
  	import { FormContext, useFormBuilder } from './FormContext';

  	const App = () => {
  	  const builder = new ContactFormBuilder();
  	  const director = new FormDirector();
  	  const form = director.construct(builder);

  	  return (
  	    <FormContext.Provider value={builder}>
  	      <FormComponent />
  	    </FormContext.Provider>
  	  );
  	};

  	const FormComponent = () => {
  	  const builder = useFormBuilder();
  	  return builder.getProduct().render();
  	};

  	export default App;
    ```

    特點：結合 React Context，支援動態表單建構。

<br />

## 應用場景

Builder 模式適用於以下場景

- 建構複雜物件，例如：多屬性配置。

- 需要不同表示的相同建構過程，例如：多種表單。

- 前端中動態生成 UI 元件或 API 請求。

<br />

## 優缺點

### 優點

- 分步建構：簡化複雜物件創建。

- 靈活性：支援多種產品表示。

- 可讀性：程式碼結構清晰。

- 封裝性：隱藏建構細節。

### 缺點

- 程式碼量增加：需定義多個建構者類別。

- 複雜度：簡單物件可能不必要。

- 導演依賴：導演可能限制靈活性。

<br />

## 注意事項

- 建構者設計：確保建構者涵蓋所有必要部分。

- 導演可選：可省略導演，允許客戶端直接控制。

- 參數化：支援動態參數配置。

- 避免濫用：簡單物件可直接建構。

<br />

## 與其他模式的關係

- 與 Abstract Factory：Abstract Factory 聚焦家族，Builder 聚焦單一物件建構。

- 與 Factory Method：Builder 提供分步建構，Factory Method 聚焦單一創建。

- 與 Prototype：可結合原型複製初始化產品。

- 與 Singleton：建構者可為單例。

<br />

## 總結

Builder 模式透過分步建構提供靈活方式創建複雜物件，適合多屬性配置場景。

在前端中，此模式適用於動態 UI 或 API 請求配置。理解 Builder 有助於設計清晰、可擴展的架構，提升程式碼品質。
