<template>
    <!-- Sección de Contacto -->
    <PageSection variant="dark"
                 :id="props.id">
        <!-- Título -->
        <PageSectionHeader title="*Contáctanos*"
                           subtitle="¡No dudes en escribirnos!"
                           :contrast="true"/>

        <!-- Contenido -->
        <PageSectionContent>
            <ArticleCustomContent class="p-0">
                <ContactForm/>

                <!-- Mapa de ubicación (Google Maps embed) -->
                <div class="contact-map" aria-label="Ubicación taller">
                  <div class="map-wrapper">
                    <iframe
                      title="Mapa - Eusebio Lillo 362, Valparaíso"
                      src="https://www.google.com/maps?q=Eusebio%20Lillo%20362,%20Valparaiso,%20Chile%2C%20CP%202350454&output=embed"
                      loading="lazy"
                      referrerpolicy="no-referrer-when-downgrade">
                    </iframe>
                  </div>

                  <div class="address">
                    <strong>Dirección:</strong>
                    <div>Eusebio Lillo 362, Valparaíso</div>
                    <div>CP: 2350454</div>
                    <div>Chile</div>
                  </div>
                </div>

            </ArticleCustomContent>
        </PageSectionContent>
    </PageSection>
</template>

<script setup>
import PageSection from "/src/vue/components/layout/PageSection.vue"
import PageSectionHeader from "/src/vue/components/layout/PageSectionHeader.vue"
import PageSectionContent from "/src/vue/components/layout/PageSectionContent.vue"
import ArticleCustomContent from "/src/vue/components/articles/ArticleCustomContent.vue"
import ContactForm from "/src/vue/components/forms/contact/ContactForm.vue"

const props = defineProps({
    id: String
})
</script>

<style lang="scss" scoped>
@import "@/scss/_theming.scss";

.contact-map {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;

  .map-wrapper {
    width: 100%;
    max-width: 600px;
    height: 450px;
    border: 0;
    border-radius: 8px;
    overflow: hidden;

    iframe {
      width: 100%;
      height: 100%;
      border: 0;
    }
  }

  .address {
    margin-top: 1rem;
    text-align: center;
    color: #666;

    strong {
      font-weight: bold;
      color: var(--color-primary, #0066cc);
    }
  }
}
</style>
