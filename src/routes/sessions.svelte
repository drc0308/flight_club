<script lang="ts">
  import UpdateSession from '$lib/UpdateSession.svelte';
  import SessionList from '$lib/SessionList.svelte';
</script>

<svelte:head>
  <title>FC &#183; Sessions</title>
</svelte:head>

<h1>Sessions</h1>
<UpdateSession />
<SessionList />
