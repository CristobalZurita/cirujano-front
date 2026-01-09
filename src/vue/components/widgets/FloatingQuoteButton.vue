<template>
  <div v-if="floatingButtonVisible && !loaderActive && showScrollTop" class="floating-quote-button">
    <!-- Botón redondeado: flecha blanca sobre fondo naranja -->
    <button @click="scrollToTop" 
            class="scroll-to-top-btn"
            aria-label="Subir al inicio"
            title="Ir arriba">
      <i class="fas fa-arrow-up"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'

const floatingButtonVisible = inject("floatingButtonVisible", ref(true))
const loaderActive = inject("loaderActive", ref(true))

const showScrollTop = ref(false)

// Calcula 1/3 de la altura total del documento
const calculateOneThirdScroll = () => {
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  return docHeight / 3
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleScroll = () => {
  const oneThirdScroll = calculateOneThirdScroll()
  showScrollTop.value = window.scrollY > oneThirdScroll
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
@import '/src/scss/_variables.scss';

.floating-quote-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 999;

  @media (max-width: 768px) {
    bottom: 1rem;
    right: 1rem;
  }
}

.scroll-to-top-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ff8c00; // Naranja
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 140, 0, 0.4);

  i {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &:hover {
    background-color: #ff6600;
    transform: translateY(-4px);
  }

  &:active {
    transform: translateY(-2px);
  }

  @media (max-width: 768px) {
    width: 45px;
    height: 45px;
    font-size: 1.1rem;
  }
}
</style>
