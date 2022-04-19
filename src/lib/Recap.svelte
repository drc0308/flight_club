<script lang="ts">
  import type { Session } from '$lib/models';
  import { user } from '$lib/stores';
  import { updateSession } from '$lib/firebase';

  export let session: Session;
  let editing: boolean = false;

  function doneEditing() {
    updateSession(session);
    editing = false;
  }
</script>

{#if editing}
  <div class="form-group mx-2">
    <textarea
      id="recap"
      bind:value={session.recap}
      class="form-control"
      rows="7"
      on:focusout={doneEditing}
    />
    <button class="btn btn-light" on:click={doneEditing}>Done</button>
  </div>
{:else}
  <p class="mx-3" style="max-width: 600px; white-space: pre-wrap">
    {session.recap ? session.recap : ''}
  </p>
  {#if $user.roles.editor}
    <button class="btn btn-light mx-2" on:click={() => (editing = true)}>Edit Recap</button>
  {/if}
{/if}
