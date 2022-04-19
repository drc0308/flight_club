<script lang="ts">
  import type { Session } from '$lib/models';
  import { user } from '$lib/stores';
  import { uploadPhotos, deletePhotos } from '$lib/firebase';

  export let session: Session;
  let files: FileList;

  function choosePhotos() {
    uploadPhotos(session.id, files);
  }

  function onDelete() {
    if (confirm('Delete all session photos?')) {
      deletePhotos(session.id);
    }
  }
</script>

<div class="photos">
  {#if session.photos}
    {#each session.photos as photo}
      <img class="photo" src={photo} alt="" />
    {/each}
  {/if}
</div>
{#if $user.roles.editor}
  <input id="add-photo" type="file" multiple hidden bind:files on:change={choosePhotos} />
  <label for="add-photo" class="btn btn-light mx-2">Add Photos</label>
  {#if session.photos != undefined && session.photos.length}
    <button class="btn btn-light mx-2" on:click={onDelete}>Delete Photos</button>
  {/if}
{/if}

<style>
  .photos {
    width: auto;
    max-height: 70vh;
    overflow-x: scroll;
    overflow-y: hidden;
    white-space: nowrap;
    margin-bottom: 12px;
  }
  .photo {
    max-height: 60vh;
    max-width: 90vw;
    margin: 4px;
  }
</style>
