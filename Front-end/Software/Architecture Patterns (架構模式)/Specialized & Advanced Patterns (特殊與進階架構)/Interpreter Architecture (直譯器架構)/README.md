# Interpreter Architecture (直譯器架構)

Interpreter Architecture (直譯器架構) 是一種專門用於解析和執行特定語言或表達式的軟體架構模式。這種架構將語言的語法規則轉換為可執行的程式碼結構，廣泛應用於程式語言實作、配置檔案解析、規則引擎和領域特定語言 (DSL) 的開發。

直譯器架構的核心概念是將複雜的語言結構分解為簡單的元件，每個元件負責處理特定的語法元素，通過組合這些元件來實現完整的語言解析和執行功能。

<br />

## 動機

在軟體開發中，經常需要處理各種語言和表達式，常見的挑戰包括

- 複雜的語法解析需要大量的條件判斷和字串處理

- 語言規則變更時需要修改大量相關程式碼

- 不同語法元素的處理方式混雜在一起，難以維護

- 新增語言功能時需要修改現有的解析程式碼

Interpreter Architecture 通過將語法規則抽象為物件結構，解決這些問題，讓系統具備

- 可擴展性：新增語法規則不影響現有程式碼

- 可維護性：每個語法元素有獨立的處理類別

- 可重用性：語法元件可以在不同情境中重複使用

- 可理解性：程式碼結構直接對應語言的語法結構

<br />

## 結構

Interpreter Architecture 採用組合模式 (Composite Pattern) 的結構，主要包含以下元件

### 1. Abstract Expression (抽象表達式)

定義解釋操作的介面。

- 宣告所有具體表達式都需要實作的解釋方法

- 通常包含一個 interpret() 方法

- 可能包含共用的功能和屬性

### 2. Terminal Expression (終端表達式)

實作語法中終端符號的解釋操作。

- 對應語法規則中的葉子節點

- 不包含其他表達式的引用

- 直接執行具體的解釋動作

### 3. Non-terminal Expression (非終端表達式)

實作語法中非終端符號的解釋操作。

- 對應語法規則中的內部節點

- 包含其他表達式的引用

- 通過組合子表達式來實現解釋功能

### 4. Context (上下文)

包含解釋器的全域資訊。

- 儲存變數值和狀態資訊

- 提供表達式執行所需的環境

- 可能包含輸入字串和解析位置

### 5. Client (客戶端)

建構抽象語法樹並呼叫解釋操作。

- 解析輸入並建立表達式樹

- 建立上下文物件

- 呼叫根表達式的解釋方法

以下是 Interpreter Architecture 的結構圖

```text
┌─────────────────┐
│     Client      │
└─────────────────┘
         │
         ▼
┌─────────────────┐    ┌────────────────┐
│    Context      │◄───│  AbstractExpr  │
└─────────────────┘    │  +interpret()  │
                       └────────────────┘
                               ▲
                    ┌──────────┴──────────┐
                    │                     │
          ┌─────────────────┐   ┌─────────────────┐
          │ TerminalExpr    │   │NonTerminalExpr  │
          │   +interpret()  │   │   +interpret()  │
          └─────────────────┘   └─────────────────┘
                                        │
                                        ▼
                                ┌─────────────────┐
                                │ AbstractExpr    │
                                │   (children)    │
                                └─────────────────┘
```

<br />

## 核心原則

### 語法規則對應

每個語法規則對應一個表達式類別，使程式碼結構與語言結構保持一致。

### 組合模式應用

使用組合模式來處理遞迴的語法結構，支援任意複雜度的表達式。

### 關注點分離

將語法解析、語意分析和執行分離到不同的階段和元件中。

<br />

## 實現方式

### Java 實現範例

以簡單的數學表達式解釋器為例

- Abstract Expression (抽象表達式)

    ```java
    /** 抽象表達式介面 */
    public interface Expression {
        int interpret(Context context);
    }

    /** 上下文類別 */
    public class Context {
        private Map<String, Integer> variables = new HashMap<>();

        public void setVariable(String name, int value) {
            variables.put(name, value);
        }

        public int getVariable(String name) {
            return variables.getOrDefault(name, 0);
        }
    }
    ```

- Terminal Expression (終端表達式)

    ```java
    /** 數字表達式 */
    public class NumberExpression implements Expression {
        private final int number;

        public NumberExpression(int number) {
            this.number = number;
        }

        @Override
        public int interpret(Context context) {
            return number;
        }
    }

    /** 變數表達式 */
    public class VariableExpression implements Expression {
        private final String name;

        public VariableExpression(String name) {
            this.name = name;
        }

        @Override
        public int interpret(Context context) {
            return context.getVariable(name);
        }
    }
    ```

- Non-terminal Expression (非終端表達式)

    ```java
    /** 加法表達式 */
    public class AddExpression implements Expression {
        private final Expression left;
        private final Expression right;

        public AddExpression(Expression left, Expression right) {
            this.left = left;
            this.right = right;
        }

        @Override
        public int interpret(Context context) {
            return left.interpret(context) + right.interpret(context);
        }
    }

    /** 減法表達式 */
    public class SubtractExpression implements Expression {
        private final Expression left;
        private final Expression right;

        public SubtractExpression(Expression left, Expression right) {
            this.left = left;
            this.right = right;
        }

        @Override
        public int interpret(Context context) {
            return left.interpret(context) - right.interpret(context);
        }
    }

    /** 乘法表達式 */
    public class MultiplyExpression implements Expression {
        private final Expression left;
        private final Expression right;

        public MultiplyExpression(Expression left, Expression right) {
            this.left = left;
            this.right = right;
        }

        @Override
        public int interpret(Context context) {
            return left.interpret(context) * right.interpret(context);
        }
    }
    ```

- Client (客戶端)

    ```java
    /** 表達式解析器 */
    public class ExpressionParser {
        public Expression parse(String expression) {
            /** 簡化的解析實作，實際應用中需要更完整的語法分析 */
            String[] tokens = expression.split(" ");
            Stack<Expression> stack = new Stack<>();
            Stack<String> operators = new Stack<>();

            for (String token : tokens) {
                if (isNumber(token)) {
                    stack.push(new NumberExpression(Integer.parseInt(token)));
                } else if (isVariable(token)) {
                    stack.push(new VariableExpression(token));
                } else if (isOperator(token)) {
                    while (!operators.isEmpty() && 
                           precedence(operators.peek()) >= precedence(token)) {
                        processOperator(stack, operators.pop());
                    }
                    operators.push(token);
                }
            }

            while (!operators.isEmpty()) {
                processOperator(stack, operators.pop());
            }

            return stack.pop();
        }

        private void processOperator(Stack<Expression> stack, String operator) {
            Expression right = stack.pop();
            Expression left = stack.pop();

            switch (operator) {
                case "+":
                    stack.push(new AddExpression(left, right));
                    break;
                case "-":
                    stack.push(new SubtractExpression(left, right));
                    break;
                case "*":
                    stack.push(new MultiplyExpression(left, right));
                    break;
            }
        }

        private boolean isNumber(String token) {
            try {
                Integer.parseInt(token);
                return true;
            } catch (NumberFormatException e) {
                return false;
            }
        }

        private boolean isVariable(String token) {
            return token.matches("[a-zA-Z]+");
        }

        private boolean isOperator(String token) {
            return "+".equals(token) || "-".equals(token) || "*".equals(token);
        }

        private int precedence(String operator) {
            switch (operator) {
                case "+":
                case "-":
                    return 1;
                case "*":
                case "/":
                    return 2;
                default:
                    return 0;
            }
        }
    }

    /** 使用範例 */
    public class InterpreterExample {
        public static void main(String[] args) {
            ExpressionParser parser = new ExpressionParser();
            Context context = new Context();

            /** 設定變數 */
            context.setVariable("x", 10);
            context.setVariable("y", 5);

            /** 解析並執行表達式 "x + y * 2" */
            Expression expression = parser.parse("x + y * 2");
            int result = expression.interpret(context);

            System.out.println("結果: " + result); /** 輸出: 結果: 20 */
        }
    }
    ```

### TypeScript 實現範例

以 SQL 查詢解釋器為例

- Abstract Expression (抽象表達式)

    ```typescript
    /** 抽象表達式介面 */
    export interface SqlExpression {
      execute(context: QueryContext): QueryResult;
    }

    /** 查詢上下文 */
    export class QueryContext {
      private tables: Map<string, Table> = new Map();

      addTable(name: string, table: Table): void {
        this.tables.set(name, table);
      }

      getTable(name: string): Table | undefined {
        return this.tables.get(name);
      }
    }

    /** 資料表結構 */
    export interface Table {
      name: string;
      columns: string[];
      rows: Record<string, any>[];
    }

    /** 查詢結果 */
    export interface QueryResult {
      columns: string[];
      rows: Record<string, any>[];
    }
    ```

- Terminal Expression (終端表達式)

    ```typescript
    /** 資料表表達式 */
    export class TableExpression implements SqlExpression {
      constructor(private readonly tableName: string) {}

      execute(context: QueryContext): QueryResult {
        const table = context.getTable(this.tableName);
        if (!table) {
          throw new Error(`資料表 ${this.tableName} 不存在`);
        }

        return {
          columns: table.columns,
          rows: table.rows
        };
      }
    }

    /** 欄位表達式 */
    export class ColumnExpression implements SqlExpression {
      constructor(
        private readonly columnName: string,
        private readonly source: SqlExpression
      ) {}

      execute(context: QueryContext): QueryResult {
        const sourceResult = this.source.execute(context);

        if (!sourceResult.columns.includes(this.columnName)) {
          throw new Error(`欄位 ${this.columnName} 不存在`);
        }

        return {
          columns: [this.columnName],
          rows: sourceResult.rows.map(row => ({
            [this.columnName]: row[this.columnName]
          }))
        };
      }
    }
    ```

- Non-terminal Expression (非終端表達式)

    ```typescript
    /** SELECT 表達式 */
    export class SelectExpression implements SqlExpression {
      constructor(
        private readonly columns: string[],
        private readonly source: SqlExpression
      ) {}

      execute(context: QueryContext): QueryResult {
        const sourceResult = this.source.execute(context);

        /** 檢查所有欄位是否存在 */
        for (const column of this.columns) {
          if (!sourceResult.columns.includes(column)) {
            throw new Error(`欄位 ${column} 不存在`);
          }
        }

        return {
          columns: this.columns,
          rows: sourceResult.rows.map(row => {
            const newRow: Record<string, any> = {};
            for (const column of this.columns) {
              newRow[column] = row[column];
            }
            return newRow;
          })
        };
      }
    }

    /** WHERE 表達式 */
    export class WhereExpression implements SqlExpression {
      constructor(
        private readonly source: SqlExpression,
        private readonly condition: ConditionExpression
      ) {}

      execute(context: QueryContext): QueryResult {
        const sourceResult = this.source.execute(context);

        return {
          columns: sourceResult.columns,
          rows: sourceResult.rows.filter(row => 
            this.condition.evaluate(row)
          )
        };
      }
    }

    /** 條件表達式 */
    export class ConditionExpression {
      constructor(
        private readonly column: string,
        private readonly operator: string,
        private readonly value: any
      ) {}

      evaluate(row: Record<string, any>): boolean {
        const columnValue = row[this.column];

        switch (this.operator) {
          case '=':
            return columnValue === this.value;
          case '>':
            return columnValue > this.value;
          case '<':
            return columnValue < this.value;
          case '>=':
            return columnValue >= this.value;
          case '<=':
            return columnValue <= this.value;
          default:
            throw new Error(`不支援的運算子: ${this.operator}`);
        }
      }
    }
    ```

- Client (客戶端)

    ```typescript
    /** SQL 解析器 */
    export class SqlParser {
      parse(sql: string): SqlExpression {
        /** 簡化的 SQL 解析實作 */
        const tokens = this.tokenize(sql);
        return this.parseSelect(tokens);
      }

      private tokenize(sql: string): string[] {
        return sql.trim().split(/\s+/);
      }

      private parseSelect(tokens: string[]): SqlExpression {
        let index = 0;

        /** 解析 SELECT */
        if (tokens[index].toUpperCase() !== 'SELECT') {
          throw new Error('預期 SELECT 關鍵字');
        }
        index++;

        /** 解析欄位列表 */
        const columns: string[] = [];
        while (index < tokens.length && tokens[index].toUpperCase() !== 'FROM') {
          const column = tokens[index].replace(',', '');
          if (column) {
            columns.push(column);
          }
          index++;
        }

        /** 解析 FROM */
        if (index >= tokens.length || tokens[index].toUpperCase() !== 'FROM') {
          throw new Error('預期 FROM 關鍵字');
        }
        index++;

        /** 解析資料表名稱 */
        if (index >= tokens.length) {
          throw new Error('預期資料表名稱');
        }
        const tableName = tokens[index];
        index++;

        let expression: SqlExpression = new TableExpression(tableName);

        /** 解析 WHERE (可選) */
        if (index < tokens.length && tokens[index].toUpperCase() === 'WHERE') {
          index++;
          const condition = this.parseCondition(tokens, index);
          expression = new WhereExpression(expression, condition);
        }

        /** 套用 SELECT */
        return new SelectExpression(columns, expression);
      }

      private parseCondition(tokens: string[], startIndex: number): ConditionExpression {
        if (startIndex + 2 >= tokens.length) {
          throw new Error('條件表達式不完整');
        }

        const column = tokens[startIndex];
        const operator = tokens[startIndex + 1];
        const value = this.parseValue(tokens[startIndex + 2]);

        return new ConditionExpression(column, operator, value);
      }

      private parseValue(token: string): any {
        /** 嘗試解析為數字 */
        const num = Number(token);
        if (!isNaN(num)) {
          return num;
        }

        /** 移除引號 */
        if (token.startsWith("'") && token.endsWith("'")) {
          return token.slice(1, -1);
        }

        return token;
      }
    }

    /** 使用範例 */
    export class SqlInterpreterExample {
      static run(): void {
        const parser = new SqlParser();
        const context = new QueryContext();

        /** 建立測試資料表 */
        const usersTable: Table = {
          name: 'users',
          columns: ['id', 'name', 'age'],
          rows: [
            { id: 1, name: 'Children', age: 18 },
            { id: 2, name: 'Charmy', age: 28 },
            { id: 3, name: 'Tina', age: 35 }
          ]
        };

        context.addTable('users', usersTable);

        /** 解析並執行 SQL */
        const sql = 'SELECT name age FROM users WHERE age > 25';
        const expression = parser.parse(sql);
        const result = expression.execute(context);

        console.log('查詢結果:', result);
        /** 輸出: { columns: ['name', 'age'], rows: [{ name: 'Charmy', age: 28 }, { name: 'Tina', age: 28 }] } */
      }
    }
    ```

### Python 實現範例

以配置檔案解釋器為例

- Abstract Expression (抽象表達式)

    ```python
    from abc import ABC, abstractmethod
    from typing import Any, Dict

    class ConfigExpression(ABC):
        """抽象配置表達式"""

        @abstractmethod
        def evaluate(self, context: 'ConfigContext') -> Any:
            pass

    class ConfigContext:
        """配置上下文"""

        def __init__(self):
            self.variables: Dict[str, Any] = {}
            self.functions: Dict[str, callable] = {
                'env': self._get_env_var,
                'default': self._get_default_value,
                'concat': self._concat_strings
            }

        def set_variable(self, name: str, value: Any) -> None:
            self.variables[name] = value

        def get_variable(self, name: str) -> Any:
            return self.variables.get(name)

        def call_function(self, name: str, *args) -> Any:
            if name not in self.functions:
                raise ValueError(f"未知函數: {name}")
            return self.functions[name](*args)

        def _get_env_var(self, var_name: str) -> str:
            import os
            return os.environ.get(var_name, '')

        def _get_default_value(self, value: Any, default: Any) -> Any:
            return value if value else default

        def _concat_strings(self, *strings) -> str:
            return ''.join(str(s) for s in strings)
    ```

- Terminal Expression (終端表達式)

    ```python
    class LiteralExpression(ConfigExpression):
        """字面值表達式"""

        def __init__(self, value: Any):
            self.value = value

        def evaluate(self, context: ConfigContext) -> Any:
            return self.value

    class VariableExpression(ConfigExpression):
        """變數表達式"""

        def __init__(self, name: str):
            self.name = name

        def evaluate(self, context: ConfigContext) -> Any:
            value = context.get_variable(self.name)
            if value is None:
                raise ValueError(f"未定義的變數: {self.name}")
            return value

    class EnvironmentExpression(ConfigExpression):
        """環境變數表達式"""

        def __init__(self, var_name: str, default_value: Any = None):
            self.var_name = var_name
            self.default_value = default_value

        def evaluate(self, context: ConfigContext) -> Any:
            import os
            value = os.environ.get(self.var_name)
            return value if value is not None else self.default_value
    ```

- Non-terminal Expression (非終端表達式)

    ```python
    class FunctionExpression(ConfigExpression):
        """函數呼叫表達式"""

        def __init__(self, function_name: str, arguments: list):
            self.function_name = function_name
            self.arguments = arguments

        def evaluate(self, context: ConfigContext) -> Any:
            # 評估所有參數
            evaluated_args = []
            for arg in self.arguments:
                if isinstance(arg, ConfigExpression):
                    evaluated_args.append(arg.evaluate(context))
                else:
                    evaluated_args.append(arg)

            return context.call_function(self.function_name, *evaluated_args)

    class ConditionalExpression(ConfigExpression):
        """條件表達式"""

        def __init__(self, condition: ConfigExpression, 
                     true_expr: ConfigExpression, 
                     false_expr: ConfigExpression):
            self.condition = condition
            self.true_expr = true_expr
            self.false_expr = false_expr

        def evaluate(self, context: ConfigContext) -> Any:
            condition_result = self.condition.evaluate(context)
            if condition_result:
                return self.true_expr.evaluate(context)
            else:
                return self.false_expr.evaluate(context)

    class ObjectExpression(ConfigExpression):
        """物件表達式"""

        def __init__(self, properties: Dict[str, ConfigExpression]):
            self.properties = properties

        def evaluate(self, context: ConfigContext) -> Dict[str, Any]:
            result = {}
            for key, expr in self.properties.items():
                result[key] = expr.evaluate(context)
            return result

    class ArrayExpression(ConfigExpression):
        """陣列表達式"""

        def __init__(self, elements: list):
            self.elements = elements

        def evaluate(self, context: ConfigContext) -> list:
            result = []
            for element in self.elements:
                if isinstance(element, ConfigExpression):
                    result.append(element.evaluate(context))
                else:
                    result.append(element)
            return result
    ```

- Client (客戶端)

    ```python
    import json
    import re
    from typing import Union

    class ConfigParser:
        """配置檔案解析器"""

        def parse(self, config_text: str) -> ConfigExpression:
            """解析配置文字"""
            try:
                config_data = json.loads(config_text)
                return self._parse_value(config_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"無效的 JSON 格式: {e}")

        def _parse_value(self, value: Any) -> ConfigExpression:
            """解析值"""
            if isinstance(value, dict):
                return self._parse_object(value)
            elif isinstance(value, list):
                return self._parse_array(value)
            elif isinstance(value, str):
                return self._parse_string(value)
            else:
                return LiteralExpression(value)

        def _parse_object(self, obj: dict) -> ConfigExpression:
            """解析物件"""
            # 檢查是否為特殊函數呼叫
            if len(obj) == 1:
                key = list(obj.keys())[0]
                if key.startswith('$'):
                    return self._parse_function_call(key[1:], obj[key])

            # 一般物件
            properties = {}
            for key, value in obj.items():
                properties[key] = self._parse_value(value)
            return ObjectExpression(properties)

        def _parse_array(self, arr: list) -> ConfigExpression:
            """解析陣列"""
            elements = [self._parse_value(item) for item in arr]
            return ArrayExpression(elements)

        def _parse_string(self, text: str) -> ConfigExpression:
            """解析字串"""
            # 檢查變數引用 ${variable}
            var_pattern = r'\$\{([^}]+)\}'
            if re.search(var_pattern, text):
                return self._parse_template_string(text)

            return LiteralExpression(text)

        def _parse_template_string(self, template: str) -> ConfigExpression:
            """解析模板字串"""
            # 簡化實作：假設整個字串就是一個變數引用
            var_match = re.match(r'^\$\{([^}]+)\}$', template)
            if var_match:
                var_name = var_match.group(1)
                return VariableExpression(var_name)

            # 複雜模板字串處理 (此處簡化)
            return LiteralExpression(template)

        def _parse_function_call(self, func_name: str, args: Any) -> ConfigExpression:
            """解析函數呼叫"""
            if func_name == 'env':
                if isinstance(args, str):
                    return EnvironmentExpression(args)
                elif isinstance(args, list) and len(args) >= 1:
                    var_name = args[0]
                    default_val = args[1] if len(args) > 1 else None
                    return EnvironmentExpression(var_name, default_val)

            # 一般函數呼叫
            if not isinstance(args, list):
                args = [args]

            parsed_args = [self._parse_value(arg) for arg in args]
            return FunctionExpression(func_name, parsed_args)

    # 使用範例
    def main():
        parser = ConfigParser()
        context = ConfigContext()

        # 設定變數
        context.set_variable('app_name', 'MyApp')
        context.set_variable('version', '1.0.0')

        # 配置檔案內容
        config_json = '''
        {
            "app": {
                "name": "${app_name}",
                "version": "${version}",
                "port": {"$env": ["PORT", 8080]},
                "database": {
                    "host": {"$env": "DB_HOST"},
                    "url": {"$concat": ["mongodb://", {"$env": "DB_HOST"}, ":27017"]}
                }
            }
        }
        '''

        # 解析並評估配置
        expression = parser.parse(config_json)
        result = expression.evaluate(context)

        print("配置結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if __name__ == "__main__":
        main()
    ```

<br />

## 優點

### 可擴展性

新增語法規則只需要建立新的表達式類別，不需要修改現有程式碼。

### 可維護性

每個語法元素都有獨立的類別，職責清楚，容易理解和維護。

### 可重用性

表達式物件可以在不同的上下文中重複使用，支援表達式的組合和嵌套。

### 可測試性

每個表達式類別都可以獨立測試，便於單元測試的編寫。

### 語法對應性

程式碼結構直接對應語言的語法結構，便於理解和維護。

<br />

## 缺點

### 類別數量多

每個語法規則都需要一個類別，可能導致類別數量過多。

### 效能開銷

物件建立和方法呼叫的開銷可能影響執行效能。

### 複雜性

對於簡單的語言或表達式來說可能過於複雜。

### 語法變更成本

語法結構的重大變更可能需要修改多個類別。

<br />

## 適用場景

### 適合使用

- 領域特定語言 (DSL)：需要建立專門的語言來解決特定問題

- 配置檔案解析：複雜的配置檔案需要支援變數、函數等功能

- 規則引擎：業務規則需要動態配置和執行

- 查詢語言：需要支援複雜查詢語法的系統

- 表達式評估：數學表達式、條件表達式等的計算

- 模板引擎：需要支援變數替換、條件判斷等功能

### 不適合使用

- 簡單字串處理：只需要基本的字串操作

- 效能要求極高：需要最佳執行效能的場景

- 語法固定不變：語法規則不會變更的簡單系統

- 一次性解析：只需要解析一次且不需要重複使用

<br />

## 實施建議

### 語法設計

在實作前先設計清楚語言的語法規則，使用 BNF 或 EBNF 來描述語法。

### 分階段實作

先實作核心的語法元素，再逐步新增複雜的功能。

### 錯誤處理

建立完善的錯誤處理機制，提供清楚的錯誤訊息。

### 效能最佳化

對於效能敏感的應用，考慮使用快取、預編譯等最佳化技術。

### 測試覆蓋

為每個表達式類別編寫完整的單元測試，確保語法解析的正確性。

<br />

## 總結

Interpreter Architecture 提供了一個結構化的方法來處理語言解析和執行問題。雖然會增加系統的複雜性，但對於需要處理複雜語法規則的應用來說，這種架構能夠提供良好的可擴展性和可維護性。

關鍵在於根據實際需求來決定是否採用這種架構。對於簡單的字串處理，可能不需要完整的直譯器架構；但對於需要支援複雜語法和動態擴展的系統，Interpreter Architecture 能夠提供強大的解決方案。
