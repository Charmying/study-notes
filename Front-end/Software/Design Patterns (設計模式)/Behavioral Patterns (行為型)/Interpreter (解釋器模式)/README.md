# Interpreter (解釋器模式)

Interpreter (解釋器模式) 是一種行為型設計模式，提供語言的語法表示，並定義解釋器來解釋句子。

此模式適合處理簡單語言或表達式，例如：規則引擎或查詢語言。

<br />

## 動機

軟體開發中，常需解析與執行特定語言，例如

- 規則引擎中，解釋業務規則，例如：「若年齡大於 18 則允許」。

- 查詢系統中，解析 SQL-like 表達式。

- 前端中，解析使用者輸入的簡單腳本或過濾條件。

直接 hardcoding 解析規則導致程式碼難以維護與擴展。Interpreter 模式透過樹狀結構表示語法，解決此問題。

<br />

## 結構

Interpreter 模式的結構包含以下元素

- 抽象表達式 (Abstract Expression)：定義解釋方法的介面。

- 終端表達式 (Terminal Expression)：實作抽象表達式，代表語法中的原子元素。

- 非終端表達式 (Nonterminal Expression)：實作抽象表達式，代表語法中的組合規則。

- 上下文 (Context)：包含解釋所需的全局資訊。

- 客戶端 (Client)：建立表達式樹並呼叫解釋方法。

以下是 Interpreter 模式的 UML 圖表示

<img src="https://uml.planttext.com/plantuml/svg/SoWkIImgAStDuULILx2rjLLurhNtnSQ5BnQkUDauvUcUVf0OBrTYKd59KM9oYK9oJc9niO8ZbEjQKL2KMboScP-dKCtBfQ2WhP2PLv9Q11GiqKZE1p8hIZHvkMfvkM26Fz_Qz7prUZJ38MQ6f1RbPkObvf1ivikvy_0OwmVIWjraNOLKk8YXWXKMNw6hCiAfYg0hd-peUhAZ-zcqTcJ7EKDKmfoJabYIYEgrwNEUx6-2wC0IvZOrkhfOmWstMgo1mSk5FOpoTNNjiFhM8JKl1PXW0000" width="100%" />

<br />

## 實現方式

- 基本實現

    假設解析簡單布林表達式，例如："true AND false"。

    ```java
    /** 上下文 */
    public class Context {
        // 無特定資料，僅示範
    }

    /** 抽象表達式 */
    public interface Expression {
        boolean interpret(Context context);
    }

    /** 終端表達式：布林值 */
    public class BooleanExpression implements Expression {
        private boolean value;

        public BooleanExpression(boolean value) {
            this.value = value;
        }

        @Override
        public boolean interpret(Context context) {
            return value;
        }
    }

    /** 非終端表達式：AND 操作 */
    public class AndExpression implements Expression {
        private Expression expr1;
        private Expression expr2;

        public AndExpression(Expression expr1, Expression expr2) {
            this.expr1 = expr1;
            this.expr2 = expr2;
        }

        @Override
        public boolean interpret(Context context) {
            return expr1.interpret(context) && expr2.interpret(context);
        }
    }

    /** 使用範例 */
    public class Client {
        public static void main(String[] args) {
            Context context = new Context();
            Expression trueExpr = new BooleanExpression(true);
            Expression falseExpr = new BooleanExpression(false);
            Expression andExpr = new AndExpression(trueExpr, falseExpr);
            System.out.println(andExpr.interpret(context)); // false
        }
    }
    ```

    特點：樹狀結構解析布林運算，易於擴展運算子。

- JavaScript 實現 Interpreter

    解析簡單數學表達式。

	```javascript
	/** 抽象表達式 */
	class Expression {
	  interpret(context) {
	    throw new Error("Method 'interpret()' must be implemented.");
	  }
	}

	/** 終端表達式：數字 */
	class NumberExpression extends Expression {
	  constructor(value) {
	    super();
	    this.value = parseInt(value);
	  }

	  interpret(context) {
	    return this.value;
	  }
	}

	/** 非終端表達式：加法 */
	class AddExpression extends Expression {
	  constructor(left, right) {
	    super();
	    this.left = left;
	    this.right = right;
	  }

	  interpret(context) {
	    return this.left.interpret(context) + this.right.interpret(context);
	  }
	}



	/** 使用範例 */
	const left = new NumberExpression('5');
	const right = new NumberExpression('3');
	const add = new AddExpression(left, right);
	console.log(add.interpret()); // 8
	```

    特點：解析加法表達式，適合簡單計算器。

- TypeScript 實現 Interpreter

    解析過濾條件。

	```typescript
	/** 抽象表達式 */
	interface FilterExpression {
	  interpret(data: any): boolean;
	}

	/** 終端表達式：等於 */
	class EqualsExpression implements FilterExpression {
	  constructor(private key: string, private value: any) {}

	  interpret(data: any): boolean {
	    return data[this.key] === this.value;
	  }
	}

	/** 非終端表達式：AND */
	class AndFilterExpression implements FilterExpression {
	  constructor(private expr1: FilterExpression, private expr2: FilterExpression) {}

	  interpret(data: any): boolean {
	    return this.expr1.interpret(data) && this.expr2.interpret(data);
	  }
	}



	/** 使用範例 */
	const equalsAge = new EqualsExpression('age', 28);
	const equalsName = new EqualsExpression('name', 'Charmy');
	const andExpr = new AndFilterExpression(equalsAge, equalsName);
	const data = { name: 'Charmy', age: 28 };
	console.log(andExpr.interpret(data)); // true
	```

    特點：TypeScript 確保型別安全，適合資料過濾。

- Angular 實現 Interpreter

    解析規則引擎。

	```typescript
	/** rule.service.ts */
	import { Injectable } from '@angular/core';

	export interface RuleExpression {
	  evaluate(data: any): boolean;
	}

	@Injectable()
	export class ValueRule implements RuleExpression {
	  constructor(private key: string, private value: any) {}

	  evaluate(data: any): boolean {
	    return data[this.key] === this.value;
	  }
	}

	@Injectable()
	export class AndRule implements RuleExpression {
	  constructor(private rules: RuleExpression[]) {}

	  evaluate(data: any): boolean {
	    return this.rules.every(rule => rule.evaluate(data));
	  }
	}

	@Injectable()
	export class RuleEngine {
	  createAndRule(rules: RuleExpression[]) {
	    return new AndRule(rules);
	  }
	}



	/** app.module.ts */
	import { NgModule } from '@angular/core';
	import { BrowserModule } from '@angular/platform-browser';
	import { AppComponent } from './app.component';
	import { ValueRule, AndRule, RuleEngine } from './rule.service';

	@NgModule({
	  declarations: [AppComponent],
	  imports: [BrowserModule],
	  providers: [ValueRule, AndRule, RuleEngine],
	  bootstrap: [AppComponent]
	})
	export class AppModule { }



	/** app.component.ts */
	import { Component } from '@angular/core';
	import { ValueRule, RuleEngine } from './rule.service';

	@Component({
	  selector: 'app-root',
	  template: `<button (click)="evaluateRule()">評估規則</button>`
	})
	export class AppComponent {
	  constructor(private ruleEngine: RuleEngine) {}

	  evaluateRule() {
	    const rule1 = new ValueRule('age', 28);
	    const rule2 = new ValueRule('name', 'Charmy');
	    const andRule = this.ruleEngine.createAndRule([rule1, rule2]);
	    const data = { name: 'Charmy', age: 28 };
	    console.log(andRule.evaluate(data)); // true
	  }
	}
	```

    特點：Angular 服務解析規則，支援業務規則。

- React 實現 Interpreter

    解析簡單腳本。

	```javascript
	/** ScriptInterpreter.js */
	class Expression {
	  interpret(context) {
	    throw new Error("Method 'interpret()' must be implemented.");
	  }
	}

	class VariableExpression extends Expression {
	  constructor(name) {
	    super();
	    this.name = name;
	  }

	  interpret(context) {
	    return context[this.name];
	  }
	}

	class MultiplyExpression extends Expression {
	  constructor(left, right) {
	    super();
	    this.left = left;
	    this.right = right;
	  }

	  interpret(context) {
	    return this.left.interpret(context) * this.right.interpret(context);
	  }
	}



	/** App.jsx */
	import React from 'react';

	const App = () => {
	  const context = { a: 5, b: 3 };
	  const a = new VariableExpression('a');
	  const b = new VariableExpression('b');
	  const multiply = new MultiplyExpression(a, b);
	  console.log(multiply.interpret(context)); // 15

	  return <div>Check console</div>;
	};

	export default App;
	```

    特點：解析乘法表達式，適合 React 腳本執行。

<br />

## 應用場景

Interpreter 模式適用於以下場景

- 解析簡單語言，例如：規則或表達式。

- 實現 DSL (領域特定語言)。

- 前端中解析使用者輸入或查詢條件。

例如：Java 的 `java.util.regex.Pattern` 使用 Interpreter 解析正則表達式。

<br />

## 優缺點

### 優點

- 易於擴展：新增表達式無需修改既有程式碼。

- 靈活性：支援動態解析語言。

- 符合開閉原則：語法規則模組化。

- 解釋重用：表達式樹可多次解釋。

### 缺點

- 程式碼複雜度：複雜語言導致類別爆炸。

- 效能開銷：遞迴解釋可能效率低。

- 調試難度：語法樹結構不易追蹤。

<br />

## 注意事項

- 語法表示：使用樹狀結構表示複雜表達式。

- 上下文管理：確保上下文包含必要資料。

- 深拷貝 vs 淺拷貝：Clone 表達式時選擇合適拷貝方式。

- 避免濫用：複雜語言可使用生成器工具。

<br />

## 與其他模式的關係

- 與 Composite：Interpreter 常與 Composite 結合表達式樹。

- 與 Flyweight：可與 Flyweight 結合共享終端表達式。

- 與 Visitor：Visitor 可代替 Interpreter 遍歷樹。

- 與 Command：Command 可與 Interpreter 結合執行命令。

<br />

## 總結

Interpreter 模式透過語法樹提供語言解釋方式，適合簡單表達式解析。

在前端中，此模式適用於使用者輸入或規則引擎。

理解 Interpreter 有助於設計可擴展解析系統，提升程式碼可維護性。
