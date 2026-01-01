# Model–View–ViewModel (MVVM) (模型 - 視圖 - 視圖模型)

Model–View–ViewModel (MVVM) 是一種軟體架構模式，主要用於分離使用者介面的開發與業務或後端程式的開發。MVVM 是 Model-View-Controller (MVC) 模式的變體，特別適合現代的資料繫結技術。

這種架構模式通過引入 ViewModel 層，實現了 View 和 Model 之間的解耦，使得使用者介面的開發更加靈活，同時提高了程式碼的可測試性和可維護性。

<br />

## 動機

在傳統的 UI 開發中，常見的問題包括

- 使用者介面與業務程式緊密耦合，難以獨立測試

- UI 程式碼與資料處理程式混合，導致程式碼難以維護

- 資料變更時需要手動更新 UI，容易出現不一致的狀態

- 複雜的 UI 狀態管理導致程式碼複雜度增加

MVVM 通過分層設計和資料繫結，解決這些問題，讓系統具備

- 分離關注點：UI、業務程式和資料各司其職

- 可測試性：ViewModel 可以獨立於 UI 進行測試

- 可維護性：清晰的分層結構便於維護和擴展

- 資料繫結：自動同步 UI 和資料狀態

<br />

## 結構

MVVM 架構分為三個主要元件

### 1. Model (模型)

負責資料和業務程式。

- 封裝應用程式的資料結構

- 處理資料存取和業務規則

- 不依賴於 View 或 ViewModel

- 提供資料變更通知機制

### 2. View (視圖)

負責使用者介面的呈現。

- 定義 UI 元素的佈局和外觀

- 處理使用者輸入事件

- 通過資料繫結與 ViewModel 互動

- 不包含業務程式

### 3. ViewModel (視圖模型)

連接 View 和 Model 的中介層。

- 暴露 View 所需的資料和命令

- 處理 View 的程式

- 將 Model 的資料轉換為 View 可用的格式

- 實現資料繫結和命令繫結

以下是 MVVM 的架構圖

```text
┌──────────────────┐    Data Binding    ┌─────────────────┐
│       View       │ ◄────────────────► │   ViewModel     │
│ (User Interface) │   Command Binding  │  (View Model)   │
└──────────────────┘                    └─────────────────┘
                                                │
                                                │ Data Access
                                                ▼
                                       ┌─────────────────┐
                                       │     Model       │
                                       │  (Data Model)   │
                                       └─────────────────┘
```

<br />

## 核心原則

### 分離關注點 (Separation of Concerns)

每個元件都有明確的職責，不同關注點分離到不同層次。

### 資料繫結 (Data Binding)

View 和 ViewModel 之間通過資料繫結自動同步狀態。

### 命令模式 (Command Pattern)

使用命令物件封裝使用者操作，實現 View 和 ViewModel 的解耦。

<br />

## 實現方式

### C# & WPF 實現範例

以簡單的使用者管理應用為例

- Model (模型)

    ```csharp
    /** 使用者資料模型 */
    public class User : INotifyPropertyChanged
    {
        private string _name;
        private string _email;
        private bool _isActive;

        public string Name
        {
            get => _name;
            set
            {
                _name = value;
                OnPropertyChanged();
            }
        }

        public string Email
        {
            get => _email;
            set
            {
                _email = value;
                OnPropertyChanged();
            }
        }

        public bool IsActive
        {
            get => _isActive;
            set
            {
                _isActive = value;
                OnPropertyChanged();
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    /** 使用者服務 */
    public interface IUserService
    {
        Task<List<User>> GetUsersAsync();
        Task<User> CreateUserAsync(User user);
        Task UpdateUserAsync(User user);
        Task DeleteUserAsync(int userId);
    }

    public class UserService : IUserService
    {
        public async Task<List<User>> GetUsersAsync()
        {
            /** 模擬 API 呼叫 */
            await Task.Delay(500);
            return new List<User>
            {
                new User { Name = "張三", Email = "zhang@example.com", IsActive = true },
                new User { Name = "李四", Email = "li@example.com", IsActive = false }
            };
        }

        public async Task<User> CreateUserAsync(User user)
        {
            await Task.Delay(300);
            return user;
        }

        public async Task UpdateUserAsync(User user)
        {
            await Task.Delay(300);
        }

        public async Task DeleteUserAsync(int userId)
        {
            await Task.Delay(300);
        }
    }
    ```

- ViewModel (視圖模型)

    ```csharp
    /** 使用者列表 ViewModel */
    public class UserListViewModel : INotifyPropertyChanged
    {
        private readonly IUserService _userService;
        private ObservableCollection<User> _users;
        private User _selectedUser;
        private bool _isLoading;

        public UserListViewModel(IUserService userService)
        {
            _userService = userService;
            Users = new ObservableCollection<User>();
            LoadUsersCommand = new RelayCommand(async () => await LoadUsersAsync());
            CreateUserCommand = new RelayCommand(async () => await CreateUserAsync(), CanCreateUser);
            UpdateUserCommand = new RelayCommand(async () => await UpdateUserAsync(), () => SelectedUser != null);
            DeleteUserCommand = new RelayCommand(async () => await DeleteUserAsync(), () => SelectedUser != null);
        }

        public ObservableCollection<User> Users
        {
            get => _users;
            set
            {
                _users = value;
                OnPropertyChanged();
            }
        }

        public User SelectedUser
        {
            get => _selectedUser;
            set
            {
                _selectedUser = value;
                OnPropertyChanged();
                UpdateUserCommand.RaiseCanExecuteChanged();
                DeleteUserCommand.RaiseCanExecuteChanged();
            }
        }

        public bool IsLoading
        {
            get => _isLoading;
            set
            {
                _isLoading = value;
                OnPropertyChanged();
            }
        }

        public ICommand LoadUsersCommand { get; }
        public ICommand CreateUserCommand { get; }
        public ICommand UpdateUserCommand { get; }
        public ICommand DeleteUserCommand { get; }

        private async Task LoadUsersAsync()
        {
            IsLoading = true;
            try
            {
                var users = await _userService.GetUsersAsync();
                Users.Clear();
                foreach (var user in users)
                {
                    Users.Add(user);
                }
            }
            catch (Exception ex)
            {
                /** 處理錯誤 */
                MessageBox.Show($"載入使用者失敗: {ex.Message}");
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task CreateUserAsync()
        {
            var newUser = new User { Name = "新使用者", Email = "new@example.com", IsActive = true };
            try
            {
                var createdUser = await _userService.CreateUserAsync(newUser);
                Users.Add(createdUser);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"建立使用者失敗: {ex.Message}");
            }
        }

        private bool CanCreateUser()
        {
            return !IsLoading;
        }

        private async Task UpdateUserAsync()
        {
            if (SelectedUser == null) return;

            try
            {
                await _userService.UpdateUserAsync(SelectedUser);
                MessageBox.Show("使用者更新成功");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"更新使用者失敗: {ex.Message}");
            }
        }

        private async Task DeleteUserAsync()
        {
            if (SelectedUser == null) return;

            try
            {
                await _userService.DeleteUserAsync(SelectedUser.Id);
                Users.Remove(SelectedUser);
                SelectedUser = null;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"刪除使用者失敗: {ex.Message}");
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
    ```

- View (視圖)

    ```xml
    <!-- UserListView.xaml -->
    <UserControl x:Class="UserManagement.Views.UserListView"
                 xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                 xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
        <Grid>
            <Grid.RowDefinitions>
                <RowDefinition Height="Auto"/>
                <RowDefinition Height="*"/>
                <RowDefinition Height="Auto"/>
            </Grid.RowDefinitions>

            <!-- 工具列 -->
            <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="10">
                <Button Content="載入使用者" Command="{Binding LoadUsersCommand}" Margin="0,0,10,0"/>
                <Button Content="新增使用者" Command="{Binding CreateUserCommand}" Margin="0,0,10,0"/>
                <Button Content="更新使用者" Command="{Binding UpdateUserCommand}" Margin="0,0,10,0"/>
                <Button Content="刪除使用者" Command="{Binding DeleteUserCommand}"/>
            </StackPanel>

            <!-- 使用者列表 -->
            <DataGrid Grid.Row="1" 
                      ItemsSource="{Binding Users}" 
                      SelectedItem="{Binding SelectedUser}"
                      AutoGenerateColumns="False"
                      Margin="10">
                <DataGrid.Columns>
                    <DataGridTextColumn Header="姓名" Binding="{Binding Name}" Width="*"/>
                    <DataGridTextColumn Header="Email" Binding="{Binding Email}" Width="*"/>
                    <DataGridCheckBoxColumn Header="啟用" Binding="{Binding IsActive}" Width="Auto"/>
                </DataGrid.Columns>
            </DataGrid>

            <!-- 載入指示器 -->
            <ProgressBar Grid.Row="2" 
                         IsIndeterminate="True" 
                         Visibility="{Binding IsLoading, Converter={StaticResource BooleanToVisibilityConverter}}"
                         Height="20" Margin="10"/>
        </Grid>
    </UserControl>
    ```

### Vue.js 實現範例

- Model (模型)

    ```typescript
    /** 使用者資料模型 */
    export interface User {
      id: number;
      name: string;
      email: string;
      isActive: boolean;
    }

    /** 使用者 API 服務 */
    export class UserApiService {
      private baseUrl = '/api/users';

      async getUsers(): Promise<User[]> {
        const response = await fetch(this.baseUrl);
        if (!response.ok) {
          throw new Error('載入使用者失敗');
        }
        return response.json();
      }

      async createUser(user: Omit<User, 'id'>): Promise<User> {
        const response = await fetch(this.baseUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });
        if (!response.ok) {
          throw new Error('建立使用者失敗');
        }
        return response.json();
      }

      async updateUser(user: User): Promise<User> {
        const response = await fetch(`${this.baseUrl}/${user.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });
        if (!response.ok) {
          throw new Error('更新使用者失敗');
        }
        return response.json();
      }

      async deleteUser(id: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) {
          throw new Error('刪除使用者失敗');
        }
      }
    }
    ```

- ViewModel (Composable)

    ```typescript
    /** 使用者管理 Composable (ViewModel) */
    import { ref, computed } from 'vue';
    import type { User } from '../models/User';
    import { UserApiService } from '../services/UserApiService';

    export function useUserManagement() {
      const userService = new UserApiService();

      /** 狀態 */
      const users = ref<User[]>([]);
      const selectedUser = ref<User | null>(null);
      const isLoading = ref(false);
      const error = ref<string | null>(null);

      /** 計算屬性 */
      const hasUsers = computed(() => users.value.length > 0);
      const canDelete = computed(() => selectedUser.value !== null);
      const canUpdate = computed(() => selectedUser.value !== null);

      /** 方法 */
      const loadUsers = async () => {
        isLoading.value = true;
        error.value = null;
        try {
          users.value = await userService.getUsers();
        } catch (err) {
          error.value = err instanceof Error ? err.message : '載入使用者失敗';
        } finally {
          isLoading.value = false;
        }
      };

      const createUser = async (userData: Omit<User, 'id'>) => {
        isLoading.value = true;
        error.value = null;
        try {
          const newUser = await userService.createUser(userData);
          users.value.push(newUser);
        } catch (err) {
          error.value = err instanceof Error ? err.message : '建立使用者失敗';
        } finally {
          isLoading.value = false;
        }
      };

      const updateUser = async (user: User) => {
        isLoading.value = true;
        error.value = null;
        try {
          const updatedUser = await userService.updateUser(user);
          const index = users.value.findIndex(u => u.id === user.id);
          if (index !== -1) {
            users.value[index] = updatedUser;
          }
        } catch (err) {
          error.value = err instanceof Error ? err.message : '更新使用者失敗';
        } finally {
          isLoading.value = false;
        }
      };

      const deleteUser = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
          await userService.deleteUser(id);
          users.value = users.value.filter(u => u.id !== id);
          if (selectedUser.value?.id === id) {
            selectedUser.value = null;
          }
        } catch (err) {
          error.value = err instanceof Error ? err.message : '刪除使用者失敗';
        } finally {
          isLoading.value = false;
        }
      };

      const selectUser = (user: User) => {
        selectedUser.value = user;
      };

      const clearSelection = () => {
        selectedUser.value = null;
      };

      return {
        /** 狀態 */
        users,
        selectedUser,
        isLoading,
        error,
        /** 計算屬性 */
        hasUsers,
        canDelete,
        canUpdate,
        /** 方法 */
        loadUsers,
        createUser,
        updateUser,
        deleteUser,
        selectUser,
        clearSelection
      };
    }
    ```

- View (Vue 元件)

    ```vue
    <!-- UserManagement.vue -->
    <template>
      <div class="user-management">
        <!-- 工具列 -->
        <div class="toolbar">
          <button @click="loadUsers" :disabled="isLoading">
            載入使用者
          </button>
          <button @click="showCreateDialog" :disabled="isLoading">
            新增使用者
          </button>
          <button @click="showUpdateDialog" :disabled="!canUpdate || isLoading">
            更新使用者
          </button>
          <button @click="handleDeleteUser" :disabled="!canDelete || isLoading">
            刪除使用者
          </button>
        </div>

        <!-- 錯誤訊息 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- 載入指示器 -->
        <div v-if="isLoading" class="loading">
          載入中...
        </div>

        <!-- 使用者列表 -->
        <div v-else-if="hasUsers" class="user-list">
          <table>
            <thead>
              <tr>
                <th>姓名</th>
                <th>Email</th>
                <th>狀態</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="user in users" 
                :key="user.id"
                :class="{ selected: selectedUser?.id === user.id }"
                @click="selectUser(user)"
              >
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span :class="user.isActive ? 'active' : 'inactive'">
                    {{ user.isActive ? '啟用' : '停用' }}
                  </span>
                </td>
                <td>
                  <button @click.stop="editUser(user)" class="btn-edit">
                    編輯
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 空狀態 -->
        <div v-else class="empty-state">
          <p>沒有使用者資料</p>
          <button @click="loadUsers">重新載入</button>
        </div>

        <!-- 使用者表單對話框 -->
        <UserFormDialog
          v-if="showDialog"
          :user="editingUser"
          :is-create="isCreateMode"
          @save="handleSaveUser"
          @cancel="closeDialog"
        />
      </div>
    </template>

    <script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import { useUserManagement } from '../composables/useUserManagement';
    import UserFormDialog from './UserFormDialog.vue';
    import type { User } from '../models/User';

    /** 使用 ViewModel */
    const {
      users,
      selectedUser,
      isLoading,
      error,
      hasUsers,
      canDelete,
      canUpdate,
      loadUsers,
      createUser,
      updateUser,
      deleteUser,
      selectUser
    } = useUserManagement();

    /** 對話框狀態 */
    const showDialog = ref(false);
    const isCreateMode = ref(false);
    const editingUser = ref<User | null>(null);

    /** 對話框方法 */
    const showCreateDialog = () => {
      isCreateMode.value = true;
      editingUser.value = null;
      showDialog.value = true;
    };

    const showUpdateDialog = () => {
      if (!selectedUser.value) return;
      isCreateMode.value = false;
      editingUser.value = { ...selectedUser.value };
      showDialog.value = true;
    };

    const closeDialog = () => {
      showDialog.value = false;
      editingUser.value = null;
    };

    const handleSaveUser = async (userData: Omit<User, 'id'> | User) => {
      if (isCreateMode.value) {
        await createUser(userData as Omit<User, 'id'>);
      } else {
        await updateUser(userData as User);
      }
      closeDialog();
    };

    const handleDeleteUser = async () => {
      if (!selectedUser.value) return;
      if (confirm(`確定要刪除使用者 "${selectedUser.value.name}" 嗎？`)) {
        await deleteUser(selectedUser.value.id);
      }
    };

    const editUser = (user: User) => {
      selectUser(user);
      showUpdateDialog();
    };

    /** 初始化 */
    onMounted(() => {
      loadUsers();
    });
    </script>

    <style scoped>
    .user-management {
      padding: 20px;
    }

    .toolbar {
      margin-bottom: 20px;
    }

    .toolbar button {
      margin-right: 10px;
      padding: 8px 16px;
      border: 1px solid #ddd;
      background: #f5f5f5;
      cursor: pointer;
    }

    .toolbar button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .error-message {
      color: #d32f2f;
      background: #ffebee;
      padding: 10px;
      border-radius: 4px;
      margin-bottom: 20px;
    }

    .loading {
      text-align: center;
      padding: 40px;
      color: #666;
    }

    .user-list table {
      width: 100%;
      border-collapse: collapse;
    }

    .user-list th,
    .user-list td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    .user-list tr:hover {
      background-color: #f5f5f5;
    }

    .user-list tr.selected {
      background-color: #e3f2fd;
    }

    .active {
      color: #4caf50;
      font-weight: bold;
    }

    .inactive {
      color: #f44336;
    }

    .btn-edit {
      padding: 4px 8px;
      font-size: 12px;
      border: 1px solid #2196f3;
      background: #2196f3;
      color: white;
      cursor: pointer;
      border-radius: 2px;
    }

    .empty-state {
      text-align: center;
      padding: 40px;
      color: #666;
    }
    </style>
    ```

### React 實現範例

- Model (模型)

    ```typescript
    /** 使用者資料模型 */
    export interface User {
      id: number;
      name: string;
      email: string;
      isActive: boolean;
    }

    /** 使用者 Repository */
    export class UserRepository {
      private baseUrl = '/api/users';

      async getUsers(): Promise<User[]> {
        const response = await fetch(this.baseUrl);
        if (!response.ok) {
          throw new Error('載入使用者失敗');
        }
        return response.json();
      }

      async createUser(user: Omit<User, 'id'>): Promise<User> {
        const response = await fetch(this.baseUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });
        if (!response.ok) {
          throw new Error('建立使用者失敗');
        }
        return response.json();
      }

      async updateUser(user: User): Promise<User> {
        const response = await fetch(`${this.baseUrl}/${user.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });
        if (!response.ok) {
          throw new Error('更新使用者失敗');
        }
        return response.json();
      }

      async deleteUser(id: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) {
          throw new Error('刪除使用者失敗');
        }
      }
    }
    ```

- ViewModel (Custom Hook)

    ```typescript
    /** 使用者管理 Hook (ViewModel) */
    import { useState, useCallback } from 'react';
    import type { User } from '../models/User';
    import { UserRepository } from '../repositories/UserRepository';

    export function useUserManagement() {
      const [users, setUsers] = useState<User[]>([]);
      const [selectedUser, setSelectedUser] = useState<User | null>(null);
      const [isLoading, setIsLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);

      const userRepository = new UserRepository();

      const loadUsers = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
          const userList = await userRepository.getUsers();
          setUsers(userList);
        } catch (err) {
          setError(err instanceof Error ? err.message : '載入使用者失敗');
        } finally {
          setIsLoading(false);
        }
      }, []);

      const createUser = useCallback(async (userData: Omit<User, 'id'>) => {
        setIsLoading(true);
        setError(null);
        try {
          const newUser = await userRepository.createUser(userData);
          setUsers(prev => [...prev, newUser]);
        } catch (err) {
          setError(err instanceof Error ? err.message : '建立使用者失敗');
        } finally {
          setIsLoading(false);
        }
      }, []);

      const updateUser = useCallback(async (user: User) => {
        setIsLoading(true);
        setError(null);
        try {
          const updatedUser = await userRepository.updateUser(user);
          setUsers(prev => prev.map(u => u.id === user.id ? updatedUser : u));
          if (selectedUser?.id === user.id) {
            setSelectedUser(updatedUser);
          }
        } catch (err) {
          setError(err instanceof Error ? err.message : '更新使用者失敗');
        } finally {
          setIsLoading(false);
        }
      }, [selectedUser]);

      const deleteUser = useCallback(async (id: number) => {
        setIsLoading(true);
        setError(null);
        try {
          await userRepository.deleteUser(id);
          setUsers(prev => prev.filter(u => u.id !== id));
          if (selectedUser?.id === id) {
            setSelectedUser(null);
          }
        } catch (err) {
          setError(err instanceof Error ? err.message : '刪除使用者失敗');
        } finally {
          setIsLoading(false);
        }
      }, [selectedUser]);

      const selectUser = useCallback((user: User) => {
        setSelectedUser(user);
      }, []);

      const clearSelection = useCallback(() => {
        setSelectedUser(null);
      }, []);

      const clearError = useCallback(() => {
        setError(null);
      }, []);

      return {
        /** 狀態 */
        users,
        selectedUser,
        isLoading,
        error,
        /** 計算屬性 */
        hasUsers: users.length > 0,
        canDelete: selectedUser !== null,
        canUpdate: selectedUser !== null,
        /** 方法 */
        loadUsers,
        createUser,
        updateUser,
        deleteUser,
        selectUser,
        clearSelection,
        clearError
      };
    }
    ```

- View (React 元件)

    ```tsx
    /** 使用者管理元件 */
    import React, { useEffect, useState } from 'react';
    import { useUserManagement } from '../hooks/useUserManagement';
    import type { User } from '../models/User';
    import './UserManagement.css';

    export const UserManagement: React.FC = () => {
      const {
        users,
        selectedUser,
        isLoading,
        error,
        hasUsers,
        canDelete,
        canUpdate,
        loadUsers,
        createUser,
        updateUser,
        deleteUser,
        selectUser,
        clearError
      } = useUserManagement();

      const [showDialog, setShowDialog] = useState(false);
      const [isCreateMode, setIsCreateMode] = useState(false);
      const [editingUser, setEditingUser] = useState<User | null>(null);

      useEffect(() => {
        loadUsers();
      }, [loadUsers]);

      const handleCreateUser = () => {
        setIsCreateMode(true);
        setEditingUser(null);
        setShowDialog(true);
      };

      const handleUpdateUser = () => {
        if (!selectedUser) return;
        setIsCreateMode(false);
        setEditingUser({ ...selectedUser });
        setShowDialog(true);
      };

      const handleDeleteUser = async () => {
        if (!selectedUser) return;
        if (window.confirm(`確定要刪除使用者 "${selectedUser.name}" 嗎？`)) {
          await deleteUser(selectedUser.id);
        }
      };

      const handleSaveUser = async (userData: Omit<User, 'id'> | User) => {
        if (isCreateMode) {
          await createUser(userData as Omit<User, 'id'>);
        } else {
          await updateUser(userData as User);
        }
        setShowDialog(false);
        setEditingUser(null);
      };

      const handleCloseDialog = () => {
        setShowDialog(false);
        setEditingUser(null);
      };

      const handleEditUser = (user: User) => {
        selectUser(user);
        handleUpdateUser();
      };

      return (
        <div className="user-management">
          {/* 工具列 */}
          <div className="toolbar">
            <button onClick={loadUsers} disabled={isLoading}>
              載入使用者
            </button>
            <button onClick={handleCreateUser} disabled={isLoading}>
              新增使用者
            </button>
            <button onClick={handleUpdateUser} disabled={!canUpdate || isLoading}>
              更新使用者
            </button>
            <button onClick={handleDeleteUser} disabled={!canDelete || isLoading}>
              刪除使用者
            </button>
          </div>

          {/* 錯誤訊息 */}
          {error && (
            <div className="error-message">
              {error}
              <button onClick={clearError} className="close-error">×</button>
            </div>
          )}

          {/* 載入指示器 */}
          {isLoading && (
            <div className="loading">
              載入中...
            </div>
          )}

          {/* 使用者列表 */}
          {!isLoading && hasUsers && (
            <div className="user-list">
              <table>
                <thead>
                  <tr>
                    <th>姓名</th>
                    <th>Email</th>
                    <th>狀態</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr
                      key={user.id}
                      className={selectedUser?.id === user.id ? 'selected' : ''}
                      onClick={() => selectUser(user)}
                    >
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>
                        <span className={user.isActive ? 'active' : 'inactive'}>
                          {user.isActive ? '啟用' : '停用'}
                        </span>
                      </td>
                      <td>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEditUser(user);
                          }}
                          className="btn-edit"
                        >
                          編輯
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* 空狀態 */}
          {!isLoading && !hasUsers && (
            <div className="empty-state">
              <p>沒有使用者資料</p>
              <button onClick={loadUsers}>重新載入</button>
            </div>
          )}

          {/* 使用者表單對話框 */}
          {showDialog && (
            <UserFormDialog
              user={editingUser}
              isCreate={isCreateMode}
              onSave={handleSaveUser}
              onCancel={handleCloseDialog}
            />
          )}
        </div>
      );
    };
    ```

<br />

## 優點

### 分離關注點

清楚分離 UI、業務程式和資料處理，每個元件職責明確。

### 可測試性

ViewModel 可以獨立於 UI 進行單元測試，提高程式碼品質。

### 資料繫結

自動同步 UI 和資料狀態，減少手動 DOM 操作。

### 可重用性

ViewModel 可以在不同的 View 中重複使用。

### 可維護性

清晰的架構使得程式碼更容易理解和維護。

<br />

## 缺點

### 學習曲線

需要理解資料繫結和命令模式等概念。

### 複雜性

對於簡單的 UI 可能過於複雜。

### 記憶體使用

資料繫結可能導致記憶體洩漏，需要適當管理。

### 除錯困難

資料繫結的自動化特性可能使除錯變得困難。

<br />

## 適用場景

### 適合使用

- 複雜的使用者介面：有大量互動和狀態管理需求

- 資料驅動應用：UI 需要頻繁反映資料變化

- 團隊協作：UI 設計師和開發者需要分工合作

- 單元測試：對 UI 程式有高測試覆蓋率要求

- 跨平台開發：需要在多個平台共享 ViewModel

### 不適合使用

- 簡單靜態頁面：沒有複雜互動的展示頁面

- 原型開發：快速驗證概念的專案

- 效能敏感應用：對渲染效能有極高要求

- 小型專案：開發資源有限的簡單應用

<br />

## 實施建議

### 合理設計 ViewModel

避免在 ViewModel 中包含過多職責，保持單一職責原則。

### 適當使用資料繫結

不是所有的 UI 更新都需要資料繫結，簡單的情況可以直接操作。

### 記憶體管理

注意解除事件監聽和資料繫結，避免記憶體洩漏。

### 測試策略

重點測試 ViewModel 的業務程式，View 的測試可以相對簡化。

### 漸進式採用

可以從複雜的 UI 模組開始採用 MVVM，逐步擴展到整個應用。

<br />

## 總結

MVVM 是一個強大的架構模式，特別適合現代的資料驅動應用開發。通過分離關注點和資料繫結，MVVM 能夠顯著提升程式碼的可測試性、可維護性和可重用性。

雖然 MVVM 有一定的學習成本和複雜性，但對於需要複雜 UI 互動和狀態管理的應用來說，這種投資是值得的。關鍵在於根據專案的實際需求來決定採用程度，避免過度設計。
