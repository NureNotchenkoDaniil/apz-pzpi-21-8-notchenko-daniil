<template>
    <div>
      <h2>{{ $t('managePetTypes') }}</h2>
      
      <div>
        <h3>{{ $t('createNewPetType') }}</h3>
        <form @submit.prevent="createPetType">
          <label :for="$t('typeNameLabel')">{{ $t('typeName') }}:</label>
          <input type="text" :id="$t('typeNameId')" v-model="newPetTypeName" required>
          <button type="submit">{{ $t('create') }}</button>
        </form>
      </div>
  
      <div>
        <h3>{{ $t('deletePetType') }}</h3>
        <form @submit.prevent="deletePetType">
          <label :for="$t('petTypeIdLabel')">{{ $t('petTypeId') }}:</label>
          <input type="number" :id="$t('petTypeIdId')" v-model.number="petTypeId" required>
          <button type="submit">{{ $t('delete') }}</button>
        </form>
      </div>
  
      <div>
        <h3>{{ $t('createDatabaseBackup') }}</h3>
        <button @click="createBackup">{{ $t('createBackup') }}</button>
      </div>
      
      <div>
      <h3>{{ $t('userlist') }}</h3>
      <div class="user-list">
        <form v-for="user in users" :key="user.id" class="user-form">
          <div>
            <label>{{ $t('username') }}</label>
            <input type="text" :value="user.username" disabled>
          </div>
          <div>
            <label>Email:</label>
            <input type="email" :value="user.email" disabled>
          </div>
          <div>
            <label>{{ $t('ban') }}</label>
            <input type="checkbox" :checked="user.is_verified" disabled>
          </div>
          <button type="button" @click="updateUserVerification(user.id, !user.is_verified)">
            {{ user.is_verified ? 'UnBun' : 'Bun' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
  
  <script>
import axios from 'axios';

export default {
  name: 'PetTypeManagement',
  data() {
    return {
      newPetTypeName: '',
      petTypeId: null,
      users: []
    };
  },
  methods: {
    async createPetType() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/admin/pet_type', {
          type_name: this.newPetTypeName
        });
        console.log('Новый тип питомца создан успешно:', response.data);
      } catch (error) {
        console.error('Ошибка при создании нового типа питомца:', error);
      }
    },
    async deletePetType() {
      try {
        const response = await axios.delete(`http://127.0.0.1:8000/admin/pet_type/${this.petTypeId}`);
        console.log('Тип питомца удален успешно:', response.data);
      } catch (error) {
        console.error('Ошибка при удалении типа питомца:', error);
      }
    },
    async createBackup() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/admin/backup');
        console.log('Резервная копия базы данных создана успешно:', response.data.message);
      } catch (error) {
        console.error('Ошибка при создании резервной копии базы данных:', error);
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users');
        this.users = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке списка пользователей:', error);
      }
    },
    async updateUserVerification(userId, isVerified) {
      try {
        const response = await axios.put(`http://127.0.0.1:8000/admin/users/${userId}/verify`, {
          is_verified: isVerified
        });
        console.log('Статус верификации пользователя обновлен успешно:', response.data);
        // Update user list
        this.fetchUsers();
      } catch (error) {
        console.error('Ошибка при обновлении статуса верификации пользователя:', error);
      }
    }
  },
  created() {
    this.fetchUsers();
  }
};
</script>
  
  <style scoped>
  .user-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.user-form {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.user-form div {
  margin-bottom: 10px;
}

.user-form label {
  font-weight: bold;
}

.user-form input[type="text"],
.user-form input[type="email"] {
  width: calc(100% - 10px);
}

.user-form input[type="checkbox"] {
  transform: scale(1.5);
}

.user-form button {
  background-color: #2196F3;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  width: 100%;
}

.user-form button:hover {
  background-color: #0b7dda;
}
  </style>
  
  
  