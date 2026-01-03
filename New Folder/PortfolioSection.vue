<template>
    <!-- Sección de Portafolio -->
    <PageSection variant="default"
                 :id="props.id">
        <!-- Título -->
        <PageSectionHeader title="Nuestro *Portafolio*"
                           subtitle="Conoce algunos de nuestros trabajos"/>

        <!-- Contenido -->
        <PageSectionContent>
            <ArticlePortfolio :projects="projects"
                              :categories="categories"
                              :link-label="strings.get('where_to_find')"/>
        </PageSectionContent>
    </PageSection>
</template>

<script setup>
import PageSection from "/src/vue/components/layout/PageSection.vue"
import PageSectionHeader from "/src/vue/components/layout/PageSectionHeader.vue"
import PageSectionContent from "/src/vue/components/layout/PageSectionContent.vue"
import ArticlePortfolio from "/src/vue/components/articles/ArticlePortfolio.vue"
import {useStrings} from "/src/composables/strings.js"

const strings = useStrings()

const props = defineProps({
    id: String
})

const categories = [
    {id: 'synths', label: 'Sintetizadores'},
    {id: 'drums', label: 'Drum Machines'},
    {id: 'keys', label: 'Teclados'},
    {id: 'fx', label: 'Efectos'},
]

const projects = [
    // Aquí puedes agregar tus proyectos
]
</script>

<style lang="scss" scoped>
@import "/src/scss/_theming.scss";
</style>
