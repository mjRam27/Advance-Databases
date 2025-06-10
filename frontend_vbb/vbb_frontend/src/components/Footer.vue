<script setup lang="ts">
interface FooterLink {
  text: string;
  href: string;
}

const links: FooterLink[] = [
  { text: 'About', href: '/about' },
  { text: 'Privacy Policy', href: '/privacy' },
  { text: 'Terms of Service', href: '/terms' },
  { text: 'Contact', href: '/contact' }
]
</script>

<template>
  <footer class="bg-gray-800 text-white py-8 mt-auto">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Company Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Travel Station</h3>
          <p class="text-gray-400 text-sm">
            Your real-time transportation dashboard for tracking trains, buses, and more across the network.
          </p>
        </div>

        <!-- Quick Links -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Quick Links</h3>
          <ul class="space-y-2">
            <li v-for="link in links" :key="link.text">
              <router-link 
                :to="link.href"
                class="text-gray-400 hover:text-primary-300 transition-colors duration-200 text-sm"
              >
                {{ link.text }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div>
          <h3 class="text-lg font-semibold mb-4">Contact Us</h3>
          <div class="text-gray-400 space-y-2 text-sm">
            <p>Email: info@travelstation.com</p>
            <p>Phone: +1 (555) 123-4567</p>
            <p>Hours: Mon-Fri 9:00 - 18:00</p>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-8 pt-8 border-t border-gray-700">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 text-sm">
            &copy; {{ new Date().getFullYear() }} Travel Station Dashboard. All rights reserved.
          </p>
          <div class="mt-4 md:mt-0">
            <div class="flex space-x-6">
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-primary-300">
                Twitter
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-primary-300">
                LinkedIn
              </a>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-primary-300">
                Facebook
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>