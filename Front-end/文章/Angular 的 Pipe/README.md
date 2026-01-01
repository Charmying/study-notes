# Angular 的 Pipe

Pipe (管道) 是 Angular 中用來轉換顯示資料的工具之一，可以在模板 (Template) 中改變資料的格式、樣式或進行其他資料處理。

使用 Pipe 可以在不更動原始資料的情況下呈現不同的格式，例如：格式化日期、貨幣、字串大小寫等。

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from "../../Component/header/header.component";
import { SectionComponent } from "../../Component/section/section.component";
import { Observable } from 'rxjs/internal/Observable';
import { delay, of } from 'rxjs';
import { DiscountPipe } from "../../Formate/DiscountPipe";
import { ComplexCalculationPipe } from '../../Formate/ComplexCalculationPipe';

@Component({
  selector: 'app-pipe',
  standalone: true,
  templateUrl: './pipe.component.html',
  styleUrl: './pipe.component.scss',
  imports: [CommonModule, HeaderComponent, SectionComponent, DiscountPipe, ComplexCalculationPipe]
})
export class PipeComponent {
  today: number = Date.now(); // 取得目前時間的 timestamp
  string = 'Hello World';     // 測試字串
  number = 3.14159265359;
  jsonData = {
    name: 'Charmy',
    age: 28,
    interest: ['LOL', 'Apex']
  };
  observableData: Observable<string> = of('Hello from Observable!').pipe(delay(5000));
  products = [
    { name: 'Product 1', price: 1000 },
    { name: 'Product 2', price: 2000 },
    { name: 'Product 3', price: 3000 },
  ];
  tryComplexCalculationArray = [1, 2, 3, 4, 5, 6];
}
```

<br />

## Pipe 的基本用法

在 Template 中使用 Pipe 語法只需在變數或表達式後面加上管道符號 `|`，並指定要使用的 Pipe 名稱即可，也可以一次串接多個 Pipe。

```html
<p>{{ today | date }}</p>   <!-- Aug 26, 2025 -->
```

在這個範例中，`today` 是一個日期物件，透過 `DatePipe`，可以將日期格式化為預設的格式來顯示。

<br />

## 內建的 Pipe

Angular 提供了許多內建的 Pipe 提供使用者直接使用。

- `DatePipe`：將日期對象格式化為使用者可讀的字符串格式

    ```html
    <p>{{ today | date }}</p>                <!-- Aug 26, 2025 -->
    <p>{{ today | date:'short' }}</p>        <!-- 8/26/25, 2:05 PM -->
    <p>{{ today | date:'medium' }}</p>       <!-- Aug 26, 2025, 2:05:09 PM -->
    <p>{{ today | date:'long' }}</p>         <!-- August 26, 2025 at 2:05:09 PM GMT+8 -->
    <p>{{ today | date:'full' }}</p>         <!-- Tuesday, August 26, 2025 at 2:05:09 PM Taipei Standard Time -->
    <p>{{ today | date:'shortDate' }}</p>    <!-- 8/26/25 -->
    <p>{{ today | date:'mediumDate' }}</p>   <!-- Aug 26, 2025 -->
    <p>{{ today | date:'longDate' }}</p>     <!-- August 26, 2025 -->
    <p>{{ today | date:'fullDate' }}</p>     <!-- Tuesday, August 26, 2025 -->
    <p>{{ today | date:'shortTime' }}</p>    <!-- 2:05 PM -->
    <p>{{ today | date:'mediumTime' }}</p>   <!-- 2:05:09 PM -->
    <p>{{ today | date:'longTime' }}</p>     <!-- 2:05:09 PM GMT+8 -->
    <p>{{ today | date:'fullTime' }}</p>     <!-- 2:05:09 PM Taipei Standard Time -->
    ```

- `UpperCasePipe`：將字符串轉換為全部大寫

    ```html
    <p>{{ string | uppercase }}</p>   <!-- HELLO WORLD -->
    ```

- `LowerCasePipe`：將字符串轉換為全部小寫

    ```html
    <p>{{ string | lowercase }}</p>   <!-- hello world -->
    ```

- `CurrencyPipe`：將數字轉換為貨幣格式

    ```html
    <!-- 默認貨幣格式 -->
    <p>{{ number | currency }}</p>                          <!-- $3.14 -->

	  <!-- 使用歐元格式 -->
	  <p>{{ number | currency:'EUR' }}</p>                    <!-- €3.14 -->

	  <!-- 使用日元，顯示小數點後2位 -->
	  <p>{{ number | currency:'JPY':'symbol':'4.2-2' }}</p>   <!-- ¥0,003.14 -->
	  ```

- `DecimalPipe`：將數字格式化為指定的小數格式

	  ```html
	  <!-- 默認格式 -->
	  <p>{{ number | number }}</p>               <!-- 3.142 -->

	  <!-- 小數點後最多 2 位 -->
	  <p>{{ number | number:'1.0-2' }}</p>       <!-- 3.14 -->

	  <!-- 數字最少顯示 3 位，小數點後最多 5 位 -->
	  <p>{{ number | number:'3.1-5' }}</p>       <!-- 003.14159 -->
	  ```

- `PercentPipe`：將數字轉換為百分比格式

	  ```html
	  <!-- 默認百分比格式 -->
	  <p>{{ number | percent }}</p>           <!-- 314% -->

	  <!-- 自定義百分比格式 -->
	  <p>{{ number | percent:'2.0-2' }}</p>   <!-- 314.16% -->
	  ```

- `JsonPipe`：轉換為 JSON 字符串格式，方便調試和顯示

	  ```html
	  <pre class="bg-gray-100 p-2 rounded">{{ jsonData | json }}</pre>
	  ```

    顯示內容：

	  ```console
	  {
	    "name": "Charmy",
	    "age": 28,
	    "interest": [
	      "LOL",
	      "Apex"
	    ]
	  }
	  ```

- `AsyncPipe`：訂閱 `Observable` 或 `Promise` 並自動解開其值，方便在模板中使用非同步數據

	  ```html
	  <!-- 當 observable 發出數據後，自動顯示結果 -->
	  <p>{{ observableData | async }}</p>   <!-- Hello from Observable! -->
	  ```

<br />

## 自訂 Pipe

除了使用內建的 Pipe，Angular 也允許開發人員自訂 Pipe。開發人員可以建立一個新的 Pipe 來滿足特定的需求，例如：格式化自定義的資料格式。

- `DiscountPipe`：自訂價格折扣 Pipe

	  ```typescript
	  import { Pipe, PipeTransform } from '@angular/core';

	  /** 折扣 Pipe */
	  @Pipe({
	    name: 'discount',
	    standalone: true
	  })

	  export class DiscountPipe implements PipeTransform {
	    transform(value: number, discount: number): number {
	      return value - (value * discount / 100);
	    }
	  }
	  ```

	  ```html
	  <ul>
	    <li *ngFor="let product of products">{{ product.name }}: {{ product.price | discount: 20 }}</li>
	  </ul>
	  ```

    顯示內容：

	  ```console
	  Product 1: 800
	  Product 2: 1600
	  Product 3: 2400
	  ```

- `ComplexCalculationPipe`：接受一個數字 Array 並返回其平方根的和，然後除以數組中所有偶數的乘積

	  ```typescript
	  import { Pipe, PipeTransform } from '@angular/core';

	  /** 接受一個數字 Array 並返回其平方根的和，然後除以數組中所有偶數的乘積 */
	  @Pipe({
	    name: 'complexCalculation',
	    standalone: true
	  })

	  export class ComplexCalculationPipe implements PipeTransform {
	    transform(value: number[]): number {
	      if (!Array.isArray(value) || value.length === 0) {
	        return 0;
	      }
	      const sqrtSum = value.reduce((sum, num) => sum + Math.sqrt(num), 0);
	      const evenProduct = value.filter(num => num % 2 === 0).reduce((product, num) => product * num, 1);
	      if (evenProduct === 0) {
	        return 0;
	      }
	      return sqrtSum / evenProduct;
	    }
	  }
	  ```

	  ```html
	  <p>{{ tryComplexCalculationArray | complexCalculation }}</p>   <!-- 0.22566296021301957 -->
	  ```
