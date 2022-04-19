<script lang="ts">
  import { user } from '$lib/stores';
  import { updateMember } from '$lib/firebase';

  export let sessionId: string;
  let editing: boolean = false;

  async function doneEditing() {
    await updateMember($user);
    editing = false;
  }
</script>

{#if editing}
  <div class="form-group mx-2">
    <textarea
      id="notes"
      bind:value={$user.notes[sessionId]}
      class="form-control"
      rows="7"
      on:focusout={doneEditing}
    />
    <button class="btn btn-light" on:click={doneEditing}>Done</button>
  </div>
{:else}
  <p class="mx-3" style="max-width: 600px; white-space: pre-wrap">{$user.notes[sessionId] ?? ''}</p>
  <button class="btn btn-light mx-2" on:click={() => (editing = true)}>Edit Notes</button>
{/if}
