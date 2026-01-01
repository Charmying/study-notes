# Angular FormGroup

FormGroup 是 Angular 中 Reactive Forms (反應式表單) 的一部分，用於管理和組織多個 FormControl (表單控制項或表單元件) 的容器，讓開發人員能夠輕鬆建立、驗證和管理複雜的表單。

FormGroup 通常用於包含多個欄位的表單，例如：註冊或登入表單。

- [FormGroup 的屬性](#formgroup-的屬性)

	- [`controls`：JavaScript 物件，包含了這個 FormGroup 中的所有控制項](#controls)

	- [`value`：返回一個物件，其中包含了所有控制項的當前值](#value)

	- [`valid` & `invalid`：表示整個表單的有效性](#valid--invalid)

	- [`dirty` & `pristine`：表示表單中的任何控制項是否已被修改過](#dirty--pristine)

	- [`touched` & `untouched`：表示表單中的任意一個控制項是否被使用者點擊過](#touched--untouched)

	- [`pending`：表示表單中是否有任何控制項正在進行非同步驗證](#pending)

- [FormGroup 的方法](#formgroup-的方法)

	- [`setValue(value: { [key: string]: any })`：用於設定表單中所有控制項的值](#setvaluevalue--key-string-any-)

	- [`patchValue(value: { [key: string]: any })`：可以只更新部分控制項的值，使其變得更靈活](#patchvaluevalue--key-string-any-)

	- [`reset(value?: any)`：用於重設表單至初始狀態](#resetvalue-any)

	- [`get(path: string | (string | number)[])`：用於透過路徑取得 FormGroup 中的某個控制項](#getpath-string--string--number)

	- [`addControl(name: string, control: AbstractControl)`：用於動態為 FormGroup 添加新的控制項](#addcontrolname-string-control-abstractcontrol)

	- [`removeControl(name: string, control: AbstractControl)`：用於從 FormGroup 中移除一個控制項。](#removecontrolname-string-control-abstractcontrol)

	- [`setControl(name: string, control: AbstractControl)`：允許替換指定名稱的控制項](#setcontrolname-string-control-abstractcontrol)

	- [`contains(name: string)`：用於檢查 FormGroup 是否包含指定名稱的控制項](#containsname-string)

- [綜合範例](#綜合範例)

<br />

## FormGroup 的屬性

### `controls`

`controls` 屬性是一個 JavaScript 物件，包含了 FormGroup 中的所有控制項。

每個控制項都以鍵值對 (Key-Value Pairs) 的形式儲存，鍵是控制項的名稱，值是相應的 FormControl、FormGroup 或 FormArray，這樣可以比較輕鬆的存取、操作和管理各種表單元素。

```typescript
const formGroup = new FormGroup({
  username: new FormControl(''),
  password: new FormControl(''),
});

console.log(formGroup.controls); // {username: FormControl2, password: FormControl2}
```

在這個範例中，建立了一個 FormGroup，其中包含兩個控制項：`username` 和 `password`，透過 `controls` 屬性，可以存取這些控制項並對其進行操作。

### `value`

`value` 屬性返回一個物件，其中包含了所有控制項的當前值，表示了目前表單的狀態。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

console.log(formGroup.value); // {username: 'Charmy', password: '123'}
```

在這個範例中，`formGroup.value` 返回包含 `username` 和 `password` 當前值的物件。

### `valid` & `invalid`

`valid` 屬性是一個 boolean，表示整個表單的有效性。只有當 FormGroup 中的所有控制項都通過了驗證，`valid` 才會是 `true`，這樣可以檢查整個表單是否有效，不需要逐一檢查每個控制項。

`invalid` 屬性與 `valid` 相反，當表單中有任何一個控制項無效時，會返回 `true`，因此 `invaild` 適用於顯示錯誤訊息或防止用戶提交無效表單。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy', Validators.required),
  password: new FormControl('', Validators.required),
});

console.log(formGroup.valid);   // false
console.log(formGroup.invalid); // true
```

在這個範例中，為 `username` 和 `password` 添加 `Validators.required` 驗證器。因為 `password` 欄位是空的，所以 `formGroup.valid` 返回 `false`，而 `formGroup.invalid` 則返回 `true`。

### `dirty` & `pristine`

`dirty` 屬性是一個 Boolean，表示表單中的任何控制項是否已被修改過。若使用者對表單中的任何控制項進行了修改，則 `dirty` 會變為 `true`，所以 `dirty` 很適合用於監測表單是否已被修改以及決定是否需要保存更改。

`pristine` 屬性與 `dirty` 相反，當表單中的所有控制項都還未被修改時，`pristine` 的值為 `true`，一旦控制項被修改，`pristine` 就會變為 `false`。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.controls['username'].setValue('Tina');
formGroup.markAsDirty();
console.log(formGroup.dirty);    // true
console.log(formGroup.pristine); // false
```

在這個範例中，更改 `username` 的值時，`formGroup.dirty` 變為 `true`，表示表單已被修改，而 `formGroup.pristine` 則變為 `false`。

### `touched` & `untouched`

`touched` 屬性是一個 Boolean，當表單中的任意一個控制項被使用者點擊過 (即使未修改)，`touched` 都會變為 `true`。也就是說，`touched` 可以確定使用者是否有操作過表單。

`untouched` 屬性與 `touched` 相反，當所有控制項都還沒有被觸碰時，這個屬性會是 `true`。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.controls['username'].markAsTouched();
console.log(formGroup.touched);   // true
console.log(formGroup.untouched); // false
```

在這個範例中，使用 `markAsTouched()` 方法將 `username` 控制項標記為已觸碰，因此 `formGroup.touched` 變為 `true`，而 `formGroup.untouched` 則變為 `false`。

### `pending`

`pending` 屬性表示當表單中有任何控制項正在進行非同步驗證時，這個屬性會變為 `true`。

`pending` 適合用於處理需要與伺服器進行非同步通訊的驗證，例如：檢查用戶名是否已被使用。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

console.log(formGroup.pending); // false
```

在這個範例中，需要有非同步驗證進行才會顯示 `true`。

<br />

## FormGroup 的方法

### `setValue(value: { [key: string]: any })`

`setValue` 方法用於設定表單中所有控制項的值，並且必須傳入一個包含所有控制項值的完整物件。

若缺少任何控制項的值就會產生報錯，也就是說，`setValue` 確保表單的每個部分都被設置了新的值。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.setValue({
  username: 'Tina',
  password: '321',
});

console.log(formGroup.value); // {username: 'Tina', password: '321'}
```

在這個範例中，使用 `setValue` 設定 `username` 和 `password` 的新值，若物件中缺少任何控制項 (例如：沒有提供 `password` 的值) 就會產生報錯。

### `patchValue(value: { [key: string]: any })`

`patchValue` 與 `setValue` 類似，但是可以只更新部分控制項的值，使其變得更靈活。

當只想更新部分表單而不需要提供所有控制項的值時，可以使用 `patchValue`。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.patchValue({
  username: 'Tina',
});

console.log(formGroup.value); // {username: 'Tina', password: '123'}
```

在這個範例中，只更新了 `username` 的值而沒有提供 `password` 的值，這不會像 `setValue` 產生報錯。

### `reset(value?: any)`

`reset` 方法用於重設表單至初始狀態。

若提供 `value`，會將表單控制項重設為該值，否則將所有控制項重設為空，因此 `reset` 適用於提交表單後想要清除所有資料。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.reset();
console.log(formGroup.value); // {username: null, password: null}
```

在這個範例中，重設了整個表單，將所有控制項恢復到初始狀態。

### `get(path: string | (string | number)[])`

`get` 方法用於透過路徑取得 FormGroup 中的某個控制項。

這個路徑可以是控制項名稱的字串，或者是由字串和數字組成的陣列，特別是當表單中使用巢狀結構或表單陣列時。這個方法可以方便存取特定的控制項，不需要直接操作 `controls` 物件。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

const usernameControl = formGroup.get('username');
console.log(usernameControl?.value); // Charmy
```

在這個範例中，用 `get` 方法來存取 `username` 控制項，並透過 `value` 屬性獲取當前值。這種方式可以輕鬆操作 FormGroup 中的特定控制項，特別是當表單結構複雜時。

### `addControl(name: string, control: AbstractControl)`

`addControl` 方法用於動態為 FormGroup 添加新的控制項，因此 `addControl` 適用於需要根據使用者的操作動態添加表單欄位，例如：根據使用者的選擇動態生成更多的輸入欄位。

```typescript
const formGroup = new FormGroup<{ [key: string]: AbstractControl }>({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.addControl('email', new FormControl('charmy@example.com'));
console.log(formGroup.value); // {username: 'Charmy', password: '123', email: 'charmy@example.com'}
```

在這個範例中，為 `formGroup` 動態添加 `email` 的控制項。這個控制項現在可以與 FormGroup 的其他控制項一樣被管理和驗證。

### `removeControl(name: string, control: AbstractControl)`

`removeControl` 方法用於從 FormGroup 中移除一個控制項，因此 `removeControl` 適用於動態表單，例如：當使用者選擇移除某一欄位時，可以使用這個方法將該欄位從表單中移除。

```typescript
const formGroup = new FormGroup<{ [key: string]: AbstractControl }>({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.removeControl('password');
console.log(formGroup.value); // {username: 'Charmy'}
```

在這個範例中，從 `formGroup` 中移除了 `password` 控制項。

### `setControl(name: string, control: AbstractControl)`

`setControl` 方法允許替換指定名稱的控制項。若 FormGroup 中已經存在具有相同名稱的控制項，則將會被新的控制項替換。`setControl` 適用於需要重設或更新特定控制項的定義。

```typescript
const formGroup = new FormGroup<{ [key: string]: AbstractControl }>({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

formGroup.setControl('username', new FormControl('NewUserName'));
console.log(formGroup.value); // {password: '123', username: 'NewUserName'}
```

在這個範例中，將 `username` 控制項替換為一個新的 FormControl，其初始值為 `'NewUserName'`。這是一種更新特定控制項的簡單方法。

### `contains(name: string)`

`contains` 方法用於檢查 FormGroup 是否包含指定名稱的控制項。`contains` 返回一個 boolean，當 FormGroup 包含該名稱的控制項時，返回 `true`，否則返回 `false`，因此 `contains` 適用於需要檢查某個控制項是否存在於 FormGroup 中。

```typescript
const formGroup = new FormGroup({
  username: new FormControl('Charmy'),
  password: new FormControl('123'),
});

console.log(formGroup.contains('username')); // true
```

在這個範例中，`contains` 檢查 `formGroup` 中是否包含 `username` 控制項，結果為 `true`。這可以在動態表單操作中確保某個控制項是否存在。

<br />

## 綜合範例

```typescript
const formGroup = new FormGroup<{ [key: string]: AbstractControl }>({
  username: new FormControl('Charmy', Validators.required),
  password: new FormControl('', Validators.required),
});

/** 獲取某個控制項的值 */
const usernameControl = formGroup.get('username');
console.log(usernameControl?.value); // Charmy

/** 設定新的值 */
formGroup.patchValue({ password: '123' });

/** 檢查表單是否有效 */
console.log(formGroup.valid); // true

/** 添加新的控制項 */
formGroup.addControl('email', new FormControl('', Validators.email));
console.log(formGroup.contains('email')); // true

/** 更新某個控制項 */
formGroup.setControl('username', new FormControl('NewUserName'));
console.log(formGroup.value); // {password: '123', email: '', username: 'NewUserName'}

/** 移除控制項 */
formGroup.removeControl('password');
console.log(formGroup.value); // {email: '', username: 'NewUserName'}

/** 重設表單 */
formGroup.reset();
console.log(formGroup.value); // {email: null, username: null}

/** 檢查表單狀態 */
console.log(formGroup.pristine); // true
console.log(formGroup.touched);  // false
```
