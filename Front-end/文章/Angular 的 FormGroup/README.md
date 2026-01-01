# Angular 的 `FormGroup`

`FormGroup` 是 Angular 中一個關鍵的元件，用來構建和管理表單。

`FormGroup` 提供了一種有效方法來組織和管理多個表單控制項，包括集中處理控制項的驗證、狀態管理和數據提交。

在 Angular 的表單架構中，`FormGroup` 表示一組表單控制項的集合，這些控制項可以是基本的輸入欄位、選擇框，也可以是其他嵌套的 `FormGroup`。

作為 Reactive Forms (反應式表單) 的一部分，`FormGroup` 允許分類表單控制項，並集中管理這些控制項的值和驗證狀態。每個 `FormGroup` 可以包含多個 `FormControl` 或其他 `FormGroup`，從而構建出複雜的表單結構。

<br />

## 如何創建 FormGroup

在 Angular 中，創建 `FormGroup` 通常通過 `FormBuilder` 服務來完成。`FormBuilder` 提供了一些方法來簡化 `FormGroup` 和 `FormControl` 的創建過程。

- 使用 `FormBuilder` 創建 `FormGroup`

    `FormBuilder` 是 Angular 提供的一個服務，幫助快速創建 `FormGroup` 和 `FormControl`。以下是創建 `FormGroup` 的基本步驟：

    ```html    
    <form [formGroup]="simpleForm" (ngSubmit)="onSubmit()">
      <label for="name">Name:</label>
      <input id="name" formControlName="name" />

      <div *ngIf="simpleForm.get('name')?.invalid && simpleForm.get('name')?.touched">Name is required.</div>

      <label for="age">Age:</label>
      <input id="age" formControlName="age" />

      <div *ngIf="simpleForm.get('age')?.invalid && simpleForm.get('age')?.touched">Age must be a number between 1 and 120.</div>

      <button type="submit" [disabled]="simpleForm.invalid">Submit</button>
    </form>
    ```

    ```typescript
    import { CommonModule } from '@angular/common';
    import { Component } from '@angular/core';
    import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

    @Component({
      selector: 'app-simple-form',
      standalone: true,
      templateUrl: './simple-form.component.html',
      styleUrl: './simple-form.component.scss',
      imports: [CommonModule, ReactiveFormsModule]
    })

    export class SimpleFormComponent {
      simpleForm: FormGroup;

      constructor(private fb: FormBuilder) {
        this.simpleForm = this.fb.group({
          name: ['', Validators.required],
          age: ['', [Validators.required, Validators.min(1), Validators.max(120)]]
        });
      }

      onSubmit() {
        if (this.simpleForm.valid) {
          console.log(this.simpleForm.value);
        }
      }
    }
    ```

    在這個範例中，使用 `FormBuilder` 創建了一個名為 `simpleForm` 的 `FormGroup`。`FormGroup` 包含兩個控制項：`name` 和 `age`，並且為這些控制項設置了相應的驗證規則。

- 手動創建 `FormGroup`

    除了使用 `FormBuilder`，也可以手動創建 `FormGroup` 和 `FormControl`。這種方法適用於更複雜的情況，或者在需要更多自定義時。

    ```html
    <form [formGroup]="manualForm" (ngSubmit)="onSubmit()">
      <label for="name">Name:</label>
      <input id="name" formControlName="name" />

      <div *ngIf="manualForm.get('name')?.invalid && manualForm.get('name')?.touched">Name is required.</div>

      <label for="age">Age:</label>
      <input id="age" formControlName="age" />

      <div *ngIf="manualForm.get('age')?.invalid && manualForm.get('age')?.touched">Age must be a number between 1 and 120.</div>

      <button type="submit" [disabled]="manualForm.invalid">Submit</button>
    </form>
    ```

    ```typescript
    import { CommonModule } from '@angular/common';
    import { Component } from '@angular/core';
    import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

    @Component({
      selector: 'app-manual-form',
      standalone: true,
      templateUrl: './manual-form.component.html',
      styleUrl: './manual-form.component.scss',
      imports: [CommonModule, ReactiveFormsModule]
    })

    export class ManualFormComponent {
      manualForm: FormGroup;

      constructor() {
        this.manualForm = new FormGroup({
          name: new FormControl('', Validators.required),
          age: new FormControl('', [Validators.required, Validators.min(1),Validators.max(120)])
        });
      }

      onSubmit() {
        if (this.manualForm.valid) {
          console.log(this.manualForm.value);
        }
      }
    }
    ```

<br />

## 管理 `FormGroup` 的控制項

`FormGroup` 提供了一些方法來管理內部控制項，包括獲取控制項、設置值、重置控制項等。

- 獲取控制項

    可以使用 `get` 方法來獲取 `FormGroup` 中的控制項。這個方法接受控制項的名稱或路徑，並返回對應的 `FormControl` 或 `FormGroup`。

    ```typescript
    const nameControl = this.simpleForm.get('name');
    console.log(nameControl?.value);
    ```

- 設置控制項的值

    `setValue` 和 `patchValue` 方法可以用來設置 `FormGroup` 中控制項的值。`setValue` 要求所有控制項的值都必須符合指定的結構，而 `patchValue` 允許部分控制項的值被設置。

    ```typescript
    this.simpleForm.setValue({
      name: 'Charmy',
      age: 18
    });

    this.simpleForm.patchValue({
      age: 28
    });

    console.log(this.simpleForm.value); // {name: 'Charmy', age: 28}
    ```
- 重置控制項

    `reset` 方法用於重置控制項的值和狀態。通常用於表單提交後重置表單。

    ```typescript
    this.simpleForm.setValue({
      name: 'Charmy',
      age: 28
    });

    this.simpleForm.reset();
    console.log(this.simpleForm.value); // {name: null, age: null}
    ```

<br />

## 驗證控制項的值

`FormGroup` 允許設定驗證規則來確保表單數據的有效性。驗證可以是同步的，也可以是非同步的。

- 同步驗證

    同步驗證是在控制項值變化時立即檢查值是否符合規則。例如：`Validators.required` 驗證控制項值是否為空。

    ```typescript
    this.simpleForm = this.fb.group({
      name: ['', Validators.required],
      age: ['', [Validators.required, Validators.min(1), Validators.max(120)]]
    });
    ```

- 非同步驗證

    非同步驗證通常用於伺服器端檢查，例如：檢查用戶名是否已被使用。非同步驗證返回一個 `Observable` 或 `Promise`，並在驗證完成後發出結果。

    ```typescript
    import { AbstractControl, AsyncValidatorFn } from '@angular/forms';
    import { map } from 'rxjs/operators';
    import { Observable, of } from 'rxjs';



    constructor(private fb: FormBuilder) {
      this.simpleForm = this.fb.group({
        name: ['', Validators.required],
        age: ['', [Validators.required, Validators.min(1), Validators.max(120)]]
      });
    }

    onSubmit() {
      if (this.simpleForm.valid) {
        console.log(this.simpleForm.value);
      }
    }

    function usernameValidator(): AsyncValidatorFn {
      return (control: AbstractControl): Observable<{ [key: string]: any } | null> => {
        // 模擬伺服器端驗證
        return of(control.value === 'admin' ? { 'usernameTaken': true } : null);
      };
    }

    this.simpleForm = this.fb.group({
      username: ['', null, usernameValidator()]
    });
    ```

<br />

## 嵌套 `FormGroup`

`FormGroup` 可以嵌套其他 `FormGroup`，這樣可以構建更複雜的表單結構，適合處理多層次的表單。

- 創建嵌套 `FormGroup`

    嵌套 `FormGroup` 允許將表單拆分為更小的單元，並且每個單元都可以有自己的控制項和驗證規則。

    ```typescript
    this.simpleForm = this.fb.group({
      personalInfo: this.fb.group({
        name: ['', Validators.required],
        age: ['', [Validators.required, Validators.min(1), Validators.max(120)]]
      }),

      address: this.fb.group({
        street: [''],
        city: [''],
        zip: ['']
      })
    });
    ```

    在這個範例中，`simpleForm` 包含 `FormGroup`：`personalInfo` 和 `address`。這樣的結構使表單的組織更具可讀性和維護性。

<br />

## 總結

`FormGroup` 是 Angular 表單處理中關鍵的元件之一，可以有效組織和管理表單控制項。通過 `FormGroup`，可以集中處理控制項的狀態、設置值、進行驗證，並且可以構建出複雜的表單結構。`FormGroup` 不僅能提高開發效率，還能使得表單的處理更加靈活和可維護。
