<template>
    <ActivitySpinner :visible="Boolean(spinnerActive)"
                     :message="String(spinnerMessage)"/>

    <Loader v-if="loaderEnabled"
            :visible="Boolean(loaderActive)"
            :refresh-count="Number(loaderPageRefreshCount)"
            :smooth-transition-enabled="Boolean(loaderSmoothTransitionEnabled)"
            @rendered="_onLoaderRendered"
            @ready="_onLoaderReady"
            @leaving="_onLoaderWillLeave"
            @completed="_onLoaderCompleted"/>

    <slot v-if="isReady"/>
</template>

<script setup>
import {inject, ref} from "vue"
import ActivitySpinner from "/src/vue/components/loaders/ActivitySpinner.vue"
import Loader from "/src/vue/components/loaders/Loader.vue"

const loaderEnabled = inject("loaderEnabled")
const LoaderAnimationStatus = inject("LoaderAnimationStatus")
const loaderActive = inject("loaderActive")
const loaderPageRefreshCount = inject("loaderPageRefreshCount")
const loaderSmoothTransitionEnabled = inject("loaderSmoothTransitionEnabled")
const loaderAnimationStatus = inject("loaderAnimationStatus")
const spinnerActive = inject("spinnerActive")
const spinnerMessage = inject("spinnerMessage")

const isReady = ref(!loaderEnabled)

if (loaderEnabled) {
  loaderAnimationStatus.value = LoaderAnimationStatus.INITIALIZED
}


const _onLoaderRendered = () => {
    loaderAnimationStatus.value = LoaderAnimationStatus.RENDERED
}

const _onLoaderReady = () => {
    isReady.value = true
    loaderAnimationStatus.value = LoaderAnimationStatus.TRACKING_PROGRESS
}

const _onLoaderWillLeave = () => {
    loaderAnimationStatus.value = LoaderAnimationStatus.LEAVING
}

const _onLoaderCompleted = () => {
    loaderActive.value = false
}
</script>

<style lang="scss" scoped>
@import "/src/scss/_theming.scss";
</style>