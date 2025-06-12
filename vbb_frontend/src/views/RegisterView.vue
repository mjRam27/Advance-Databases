import { registerUser } from '../api/auth'

const handleRegister = async () => {
  try {
    await registerUser(user_id.value, password.value)
    router.push('/login')
  } catch (err) {
    errorMsg.value = 'Registration failed'
  }
}
<template>
    <div class="auth-container">
        <h2>📝 Register</h2>
        <input v-model="user_id" placeholder="User ID" />
        <input v-model="password" placeholder="Password" type="password" />
        <button @click="register">[ ➕ Register ]</button>
        <p>Already registered? <router-link to="/login">Go to login</router-link></p>
        <p v-if="message" class="error">⚠️ {{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const user_id = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const register = async () => {
    try {
        const res = await axios.post('http://localhost:8000/user/register', null, {
            params: { user_id: user_id.value, password: password.value }
        })
        if (res.data.status === 'registered') {
            router.push('/login')
        } else {
            message.value = 'User already exists'
        }
    } catch {
        message.value = 'Registration failed'
    }
}
</script>

<style scoped>
.auth-container {
    padding: 2rem;
    border: 2px dashed #ddd;
    width: 300px;
    margin: auto;
}

input {
    display: block;
    margin: 0.5rem 0;
    width: 100%;
}

button {
    margin: 1rem 0;
}

.error {
    color: red;
}
</style>