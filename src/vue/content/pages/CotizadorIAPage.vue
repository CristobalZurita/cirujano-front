<template>
	<div class="cotizador-ia-page">
		<h1>Cotizador IA</h1>
		<p class="muted">Herramienta de cotización con IA — interfaz optimizada para escritorio y móvil.</p>

		<div class="cotizador-layout">
			<div class="cotizador-left">
				<!-- Placeholder for the generator / controls -->
				<QuoteGenerator />
			</div>

			<div class="cotizador-right">
				<!-- Reserved for results / images -->
				<div class="cotizador-results">
					<p class="muted">Resultados se muestran aquí</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import QuoteGenerator from "/src/vue/components/ai/QuoteGenerator.vue"
</script>

<style scoped>
.cotizador-ia-page { padding: 1rem }
.cotizador-ia-page .muted { color: #666 }

.cotizador-layout {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 32px;
}

@media (max-width: 768px) {
	.cotizador-layout {
		grid-template-columns: 1fr;
	}
}

.cotizador-results {
	min-height: 220px;
	border: 1px dashed rgba(0,0,0,0.06);
	padding: 1rem;
	border-radius: 8px;
}
</style>
