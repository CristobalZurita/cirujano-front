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
                <!-- Formulario de contacto -->
                <div class="contact-form-wrapper">
                    <ContactForm/>
                </div>

                <!-- Mapa de ubicación (Google Maps embed) - Abajo del formulario -->
                <div class="contact-map-section">
                    <h3>Nuestra ubicación</h3>
                    
                    <div class="contact-map-container">
                        <div class="map-wrapper">
                            <iframe
                                title="Mapa - Eusebio Lillo 362, Valparaíso"
                                src="https://www.google.com/maps?q=Eusebio%20Lillo%20362,%20Valparaiso,%20Chile%2C%20CP%202350454&output=embed"
                                loading="lazy"
                                referrerpolicy="no-referrer-when-downgrade">
                            </iframe>
                        </div>

                        <div class="address-info">
                            <h4>Dirección</h4>
                            <p>Eusebio Lillo 362</p>
                            <p>Valparaíso, Chile</p>
                            <p>CP: 2350454</p>
                        </div>
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

.contact-form-wrapper {
  width: 100%;
  margin-bottom: 3rem;
}

.contact-map-section {
  width: 100%;
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);

  h3 {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
    color: var(--color-primary, #ff7a00);
  }
}

.contact-map-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: stretch;
}

.map-wrapper {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);

  iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
}

/* Address info styling */
.address-info {
  background: rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);

  h4 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--color-primary, #ff7a00);
  }

  p {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #d0d0d0;
    margin: 0.5rem 0;
  }
}

/* TABLET */
@media (max-width: 1024px) {
  .map-wrapper {
    height: 350px;
  }

  .contact-map-section {
    margin-top: 3rem;
  }
}

/* MOBILE */
@media (max-width: 768px) {
  .contact-form-wrapper {
    margin-bottom: 2.5rem;
  }

  .contact-map-section {
    margin-top: 3rem;
    padding-top: 1.5rem;
  }

  .contact-map-section h3 {
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
  }

  .map-wrapper {
    height: 280px;
  }

  .address-info {
    padding: 1.5rem;
  }

  .address-info h4 {
    font-size: 1.1rem;
  }

  .address-info p {
    font-size: 1rem;
  }
}

/* MOBILE PEQUEÑO */
@media (max-width: 480px) {
  .contact-map-container {
    gap: 1.5rem;
  }

  .map-wrapper {
    height: 240px;
  }

  .contact-map-section h3 {
    font-size: 1.2rem;
  }
}
</style>
