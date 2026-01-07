<template>
    <!-- About Section -->
    <PageSection variant="default"
                 :id="props.id">
           <!-- Title -->
        <PageSectionHeader title="*Sobre* el taller"
                           subtitle="Conoce cómo trabajamos y qué podemos hacer por tus sintetizadores."/>

        <!-- Content -->
        <PageSectionContent>
            <!-- About Workshop -->
            <ArticleInfoBlock 
                image="/images/logo/Logo Nuevo.jpg"
                :paragraphs="[
                    `<strong>Cirujano de Sintetizadores</strong> es un taller dedicado a la reparación, mantenimiento y personalización de sintetizadores, drum machines, teclados y otros equipos de audio.`,
                    `Cada instrumento se revisa en detalle: limpieza interna, revisión de fuente de poder, reemplazo de componentes cuando es necesario y calibraciones finas para recuperar estabilidad y buen sonido.`,
                    `El objetivo es devolver a tus equipos su confiabilidad y carácter sonoro, respetando su diseño original o integrando modificaciones creativas cuando el proyecto lo requiere.`
                ]"/>

        </PageSectionContent>
    </PageSection>
</template>

<script setup>
import PageSection from "/src/vue/components/layout/PageSection.vue"
import PageSectionHeader from "/src/vue/components/layout/PageSectionHeader.vue"
import PageSectionContent from "/src/vue/components/layout/PageSectionContent.vue"
import ArticleInfoBlock from "/src/vue/components/articles/ArticleInfoBlock.vue"

const props = defineProps({
    id: String
})
</script>

<style lang="scss" scoped>
@import "/src/scss/_theming.scss";
</style>