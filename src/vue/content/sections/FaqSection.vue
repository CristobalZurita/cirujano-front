<template>
    <!-- Heading Section -->
    <PageHeader :id="props.id"
                title="*Cirujano de Sintetizadores* "
                subtitle="<strong>MANTENCIÓN</strong> • <strong>RESTAURACIÓN</strong> • <strong>REPARACIÓN</strong>"
                logo-url="images/logo/NUEVO_cirujano.png"
                :show-button="true"
                button-icon="fa-solid fa-search"
                button-label="Descubre más"
                button-url="#about"/>
</template>

<script setup>
import PageHeader from "/src/vue/components/layout/PageHeader.vue"

const props = defineProps({
    id: String
})
</script>

<style lang="scss" scoped>
@import "/src/scss/_theming.scss";
</style>
