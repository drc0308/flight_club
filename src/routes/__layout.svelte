<script lang="ts">
  import { user, activeClub } from '$lib/stores';
  import Navbar from '$lib/Navbar.svelte';
  import Footer from '$lib/Footer.svelte';
  import Login from '$lib/Login.svelte';
  import NewUser from '$lib/NewUser.svelte';
</script>

<Navbar />
<!-- Require login and active club selected to view pages -->
{#if $user}
  {#if $activeClub}
    <slot />
  {:else}
    <NewUser />
  {/if}
{:else}
  <Login />
{/if}
<div class="padding" style="height:50vh" />
<Footer />

<style global lang="scss">
  @import '../custom';

  body {
    margin: 0;
    width: 100vw;
    overflow-x: hidden;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  h1,
  h2,
  h3,
  h4,
  h5 {
    font-family: 'Alfa Slab One';
    color: #d17101;
    font-weight: 100%;
    line-height: 1;
    margin: 12px;
  }
  @font-face {
    font-family: 'Alfa Slab One';
    src: url('/fonts/alpha_slab_one.woff2') format('woff2');
  }
</style>
