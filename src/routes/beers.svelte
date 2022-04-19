<script lang="ts">
  import BeerList from '$lib/BeerList.svelte';
</script>

<svelte:head>
  <title>FC &#183; Beers</title>
</svelte:head>

<h1>Beers!</h1>
<BeerList searchable={true} />
