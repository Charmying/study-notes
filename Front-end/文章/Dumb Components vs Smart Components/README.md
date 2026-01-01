# Dumb Components vs Smart Components

在前端開發中，尤其在使用框架 (例如：Angular、Vue 或 React) 時，Dumb Components 和 Smart Components 是兩種常見的設計模式，兩者的區別不僅在於作用，更在於設計哲學與應用場景。

<br />

## Dumb Components (無狀態元件)

Dumb Components 也可以叫做 Presentational Components，又稱「展示型元件」或「無狀態元件」，主要專注於 UI 的呈現，通常不直接處理業務流程或資料管理，而是通過外部傳入的 props 接收資料並進行渲染。

### 特點

- 純粹性：Dumb Components 是純函數元件，相同的輸入會產生相同的輸出 (UI)。

- 可重用性：由於不依賴特定業務規則，這類元件可以在不同場景中被重複使用。

- 易測試性：由於處理流程簡單，只需測試其渲染結果是否符合預期即可。

- 獨立性：與應用程式的狀態管理 (例如：Redux 或 Vuex) 無直接關聯。

### 範例

- Angular

	```html
	<button (click)="onClick.emit()">{{ label }}</button>
	```

	```typescript
	import { Component, Input, Output, EventEmitter } from '@angular/core';

	@Component({
	  selector: 'app-button',
	})
	export class ButtonComponent {
	  @Input() label: string = '按鈕';
	  @Output() onClick = new EventEmitter<void>();
	}
	```

    - `ButtonComponent` 負責顯示按鈕並觸發點擊事件，具體功能由外部傳入的 `onClick` 處理。

    - 通過 `@Input` 接收按鈕的標籤文字，並通過 `@Output` 發出點擊事件。

- Vue

	```vue
	/** Button.vue */

	<template>
	  <button @click="$emit('click')">{{ label }}</button>
	</template>

	<script>
	export default {
	  props: {
	    label: {
	      type: String,
	      default: '按鈕',
	    },
	  },
	};
	</script>
	```

    - 這個 `Button` 元件只負責顯示按鈕並觸發點擊事件，具體功能由外部傳入的 Click 事件處理。

    - 通過 `props` 接收按鈕的標籤文字。

- React

	```jsx
	/** Button.jsx */

	function Button({ label, onClick }) {
	  return <button onClick={onClick}>{label}</button>;
	}

	export default Button;
    ```

    - 這個 `Button` 元件負責顯示按鈕並觸發點擊事件，具體功能由外部傳入的 `onClick` 處理。

    - 通過 `props` 接收按鈕的標籤文字。

<br />

## Smart Components (智慧元件)

Smart Components 也可以叫做 Container Components， 又稱為「容器型元件」或「有狀態元件」，主要是負責管理資料與業務規則，通常與狀態管理工具 (例如：Redux、MobX 或 Vuex) 一起使用，負責獲取資料、處理事件並將結果傳遞給 Dumb Components。

### 特點

- 複雜性：Smart Components 包含業務處理程式碼，可能涉及 API 呼叫、狀態更新等操作。

- 資料管理：負責從外部來源 (例如：API 或狀態管理庫) 獲取數據，並將其傳遞給子元件。

- 應用核心：通常是應用程式的核心部分，負責協調多個 Dumb Components 的工作。

- 不可重用性：由於與特定功能綁定，所以可重用性較低。

### 範例

- Angular

	```html
	<ul>
	  <li *ngFor="let user of users">{{ user.name }}</li>
	</ul>
    ```

	```typescript
	import { Component, OnInit } from '@angular/core';
	import { UserService } from './user.service';

	@Component({
	  selector: 'app-user-list',
	})
	export class UserListComponent implements OnInit {
	  users: any[] = [];

	  constructor(private userService: UserService) {}

	  ngOnInit() {
	    this.userService.getUsers().subscribe((data) => {
	      this.users = data;
	    });
	  }
	}
	```

    - `UserListComponent` 負責從 `UserService` 獲取用戶資料，並將數據渲染成列表。

    - 這是典型的 Smart Component，因為處理了數據的獲取與管理。

- Vue

	```vue
	/** UserList.vue */

	<template>
	  <ul>
	    <li v-for="user in users" :key="user.id">{{ user.name }}</li>
	  </ul>
	</template>

	<script>
	export default {
	  data() {
	    return {
	      users: [],
	    };
	  },
	  async created() {
	    this.users = await this.fetchUsers();
	  },
	  methods: {
	    async fetchUsers() {
	      const response = await fetch('/api/users');
	      return response.json();
	    },
	  },
	};
	</script>
	```

    - `UserList` 元件負責從 API 獲取用戶數據，並將數據渲染成列表。

    - 這是典型的 Smart Component，因為處理了數據的獲取與管理。

- React

	```jsx
	/** UserList.jsx */

	import React, { useState, useEffect } from 'react';

	function UserList() {
	  const [users, setUsers] = useState([]);

	  useEffect(() => {
	    fetch('/api/users')
	      .then((response) => response.json())
	      .then((data) => setUsers(data));
	  }, []);

	  return (
	    <ul>
	      {users.map((user) => (
	        <li key={user.id}>{user.name}</li>
	      ))}
	    </ul>
	  );
	}

	export default UserList;
	```

    - `UserList` 元件負責從 API 獲取用戶數據，並將數據渲染成列表。

    - 這是典型的 Smart Component，因為處理了數據的獲取與管理。

<br />

## Dumb Components 與 Smart Components 的協作

在實際開發中，Dumb Components 和 Smart Components 通常會協同工作，形成一個清晰的架構

- Smart Components 負責資料管理與業務流程處理，並將結果通過 `props` 傳遞給 Dumb Components。

- Dumb Components 負責 UI 呈現，確保視覺效果與用戶互動的一致性。

這種分工模式有助於提升程式碼的可維護性，因為：

- 業務處理與畫面分離，便於單獨測試與修改。

- 元件職責清晰，降低耦合度。

- 便於團隊合作，不同開發人員可以專注於不同層面的工作。

<br />

## 使用時機與最佳實踐

### 使用 Dumb Components 的時機

- 當元件只需要顯示數據或觸發事件時。

- 當元件需要被多個地方重複使用時。

- 當元件的處理流程簡單，且不涉及狀態管理時。

### 使用 Smart Components 的時機

- 當元件需要處理複雜的業務規則時。

- 當元件需要與 API 或狀態管理工具互動時。

- 當元件需要協調多個子元件的工作時。

### 最佳實踐

- 盡量將元件拆分為 Dumb 和 Smart 兩類，遵循「單一職責原則」。

- 避免在 Dumb Components 中直接操作狀態或呼叫 API。

- 使用狀態管理工具 (例如：Redux 或 Vuex) 來集中管理應用程式的狀態，減少 Smart Components 的複雜度。

<br />

## 總結

Dumb Components 和 Smart Components 是前端開發中兩種重要的設計模式，分別負責 UI 呈現和業務處理。通過合理使用這兩種模式，可以打造出結構清晰、易於維護的程式碼。在實際開發中，建議根據元件的職責進行分類，並遵循最佳實踐，提升程式碼質量與開發效率。
