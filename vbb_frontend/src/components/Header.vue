<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const navItems = [
  { name: 'Dashboard', path: '/' },
  { name: 'Search', path: '/search' }
]
</script>

<template>
  <header class="bg-primary-600 text-white shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo and Title -->
        <div class="flex-shrink-0">
          <h1 
            class="text-2xl font-bold cursor-pointer hover:text-primary-200 transition-colors duration-200"
            @click="router.push('/')"
          >
            Travel Station Dashboard
          </h1>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex space-x-8">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="text-white hover:text-primary-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            :class="{ 'bg-primary-700': $route.path === item.path }"
          >
            {{ item.name }}
          </router-link>
        </nav>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button
            @click="toggleMobileMenu"
            class="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-primary-200 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          >
            <span class="sr-only">Open main menu</span>
            <!-- Menu icon -->
            <svg
              :class="{ 'hidden': isMobileMenuOpen, 'block': !isMobileMenuOpen }"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <!-- Close icon -->
            <svg
              :class="{ 'block': isMobileMenuOpen, 'hidden': !isMobileMenuOpen }"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <div
        :class="{ 'block': isMobileMenuOpen, 'hidden': !isMobileMenuOpen }"
        class="md:hidden"
      >
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="block px-3 py-2 rounded-md text-base font-medium text-white hover:text-primary-200 hover:bg-primary-700 transition-colors duration-200"
            :class="{ 'bg-primary-700': $route.path === item.path }"
            @click="isMobileMenuOpen = false"
          >
            {{ item.name }}
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>