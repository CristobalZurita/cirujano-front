<template>
  <div v-if="floatingButtonVisible && !loaderActive" class="floating-quote-button">
    <button
      class="quote-btn"
      @click="scrollToQuote"
      :class="{ 'pulse': isPulsing }"
      aria-label="Cotiza tu instrumento"
      title="Presiona para cotizar tu instrumento"
    >
      <i class="fas fa-file-circle-check"></i>
      <span class="btn-text">¡COTIZA YA!</span>
    </button>

    <!-- Tooltip -->
    <div class="tooltip-text" v-if="showTooltip">
      Cotiza ahora
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, inject } from 'vue'

const floatingButtonVisible = inject("floatingButtonVisible", ref(true))
const loaderActive = inject("loaderActive", ref(true))

const isPulsing = ref(true)
const showTooltip = ref(false)
let tooltipTimer = null

const scrollToQuote = () => {
  const quoteSection = document.getElementById('diagnostic-section')
  if (quoteSection) {
    quoteSection.scrollIntoView({ behavior: 'smooth' })
  }
}

const handleMouseEnter = () => {
  showTooltip.value = true
  if (tooltipTimer) clearTimeout(tooltipTimer)
}

const handleMouseLeave = () => {
  tooltipTimer = setTimeout(() => {
    showTooltip.value = false
  }, 300)
}

onMounted(() => {
  const btn = document.querySelector('.floating-quote-button .quote-btn')
  if (btn) {
    btn.addEventListener('mouseenter', handleMouseEnter)
    btn.addEventListener('mouseleave', handleMouseLeave)
  }
})

onUnmounted(() => {
  if (tooltipTimer) clearTimeout(tooltipTimer)
})
</script>

<style scoped lang="scss">
@import '/src/scss/_variables.scss';

.floating-quote-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 1rem;

  @media (max-width: 768px) {
    bottom: 1.5rem;
    right: 1.5rem;

    .quote-btn {
      padding: 0.75rem;
      border-radius: 50%;

      .btn-text {
        display: none;
      }

      i {
        margin-right: 0;
      }
    }
  }

  .quote-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.875rem;
    background-color: #f5d4b8;
    color: $primary;
    border: 2px solid #f5d4b8;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 700;
    font-family: $headings-font-family;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba($orange-pastel, 0.2);
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;

    i {
      font-size: 1.1rem;
    }

    &:hover:not(.pulse) {
      transform: scale(1.15);
      background-color: #ff7f1f;
      border-color: #ff7f1f;
      color: white;
      box-shadow: 0 8px 24px rgba(#ff7f1f, 0.5);
    }

    &:active {
      transform: scale(1.08);
    }

    // Pulse animation - very subtle
    &.pulse {
      animation: float-pulse 3s ease-in-out infinite;

      &:hover {
        animation: none;
      }
    }
  }

  .tooltip-text {
    position: absolute;
    right: 6rem;
    bottom: 1rem;
    background-color: $dark;
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    animation: slideInRight 0.2s ease;

    &::after {
      content: '';
      position: absolute;
      right: -6px;
      top: 50%;
      transform: translateY(-50%);
      width: 0;
      height: 0;
      border-left: 6px solid $dark;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
    }
  }
}

// Animations
@keyframes float-pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 12px rgba($orange-pastel, 0.2);
  }
  50% {
    transform: scale(1.08);
    box-shadow: 0 6px 16px rgba($orange-pastel, 0.3);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 4px 12px rgba($orange-pastel, 0.2);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
