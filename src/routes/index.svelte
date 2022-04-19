<script lang="ts">
  import ClubList from '$lib/ClubList.svelte';
  import JoinClub from '$lib/JoinClub.svelte';
</script>

<svelte:head>
  <title>Flight Club</title>
</svelte:head>

<div>
  <h1>Welcome</h1>
  <ClubList />
  <JoinClub />
</div>

<style>
  div {
    text-align: center;
    max-width: 300px;
    margin: 80px auto;
  }
  h1 {
    margin: 30px;
  }
</style>
