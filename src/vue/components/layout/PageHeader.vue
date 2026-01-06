<template>
    <header :id="id"
            class="foxy-header">
        <BackgroundPromo :faded="false"/>

        <!-- Content -->
        <div class="container-xxl">
            <article class="foxy-hero-header">
                <!-- Logo -->
                <ImageView :src="logoUrl"
                           :spinner-enabled="true"
                           :alt="title"
                           class="foxy-hero-header-logo"/>

                <!-- Texts -->
                <h1 class="heading"
                    v-html="parsedTitle"/>
                <h4 class="subheading"
                    v-html="parsedSubtitle"/>

                <!-- CTA Buttons -->
                <div v-if="showCtaButtons" class="hero-cta-buttons">
                    <button class="btn-hero" @click="$emit('scroll-to-top')">
                        <i class="fa-solid fa-search"></i>
                        <span>Descubre más</span>
                    </button>
                    <a href="#diagnostic-section" class="btn-hero btn-hero-primary">
                        <i class="fa-solid fa-file-circle-check"></i>
                        <span>Cotiza tu instrumento</span>
                    </a>
                </div>

                <!-- Button -->
                <Link v-if="showButton"
                      :url="props.buttonUrl">
                    <XLButton :label="buttonLabel"
                              :icon="buttonIcon"
                              :class="`mt-4`"/>
                </Link>
            </article>
        </div>
    </header>
</template>

<script setup>
import BackgroundPromo from "/src/vue/components/layout/BackgroundPromo.vue"
import ImageView from "/src/vue/components/generic/ImageView.vue"
import {useUtils} from "/src/composables/utils.js"
import {computed} from "vue"
import Link from "/src/vue/components/generic/Link.vue"
import XLButton from "/src/vue/components/widgets/XLButton.vue"

const utils = useUtils()

const props = defineProps({
    id: String,
    title: String,
    subtitle: String,
    logoUrl: String,
    showButton: Boolean,
    showCtaButtons: Boolean,
    buttonLabel: String,
    buttonIcon: String,
    buttonUrl: String
})

const parsedTitle = computed(() => {
    return utils.parseCustomText(props.title)
})

const parsedSubtitle = computed(() => {
    return utils.parseCustomText(props.subtitle)
})
</script>

<style lang="scss" scoped>
@import "/src/scss/_theming.scss";

header.foxy-header {
    --height: clamp(650px, 100vh, 1050px);
    --content-margin-top: 80px;
    --max-logo-proportion:45vw;
    --max-logo-height:50vh;
    @include media-breakpoint-down(xl) {--max-logo-height: 35vh;}
    @include media-breakpoint-down(lg) {--max-logo-height: 30vh; }
    @include media-breakpoint-down(md) {--content-margin-top: 65px;}

    --content-height: calc(var(--height) - var(--content-margin-top));
    --logo-proportion: clamp(190px, 45vw, min(37.5vh, 35vw, 350px));

    position: relative;
    height: var(--height);

    div.container-xxl {
        display: flex;
        align-items: center;
        justify-content: center;

        height: var(--height);
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 2rem;
    }

    article.foxy-hero-header {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding-top:var(--content-margin-top);
        position: relative;
        z-index: 3;
    }

    div.foxy-hero-header-logo {
        height: var(--logo-proportion);
        width: var(--logo-proportion);
    }

    h1.heading {
        color:$white;
        text-transform: uppercase;
        text-align: center;
        font-weight: 700;
        font-size: calc(var(--logo-proportion)/6);
        padding: calc(var(--logo-proportion)/8) 0 calc(var(--logo-proportion)/180);
    }

    h4.subheading {
        font-family: $font-family-base;
        color: $light-5;

        font-size: clamp(16px, calc(var(--logo-proportion)/14), 100px);
        padding: calc(var(--logo-proportion)/20) 0;
        line-height: 24px;
        text-align: center;
    }

    .hero-cta-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin-top: 1rem;

        @include media-breakpoint-down(md) {
            gap: 1rem;
            flex-wrap: wrap;
        }
    }

    .btn-hero {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1.125rem 2.3rem;
        border-radius: 4rem;
        border: 2px solid $orange-pastel;
        background-color: $orange-pastel;
        color: white;
        font-family: $headings-font-family;
        font-weight: 400;
        text-transform: uppercase;
        font-size: 1.125rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;

        i {
            font-size: 1.2rem;
        }

        &:hover {
            background-color: #ff7f1f;
            border-color: #ff7f1f;
            color: white;
            transform: scale(1.05);
        }

        &:active {
            transform: scale(0.98);
        }

        &.btn-hero-primary {
            background-color: $orange-pastel;
            color: white;
            border-color: $orange-pastel;

            &:hover {
                background-color: #ff7f1f;
                border-color: #ff7f1f;
            }
        }
    }
}
</style>