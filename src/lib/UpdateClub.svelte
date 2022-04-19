<script lang="ts">
  import { onMount } from 'svelte';
  import { updateClub } from '$lib/firebase';
  import { activeClub } from '$lib/stores';

  onMount(async () => {
    await import('bootstrap/js/dist/modal.js');
  })

  $: club = $activeClub;
  $: submitDisabled = !club.name;

  function onSubmit() {
    updateClub(club);
    if (document.activeElement instanceof HTMLElement) { document.activeElement.blur() };
  }
</script>

<button
  type="button"
  class="btn btn-light mx-3"
  data-bs-toggle="modal"
  data-bs-target="#updateClub"
>
  Edit Club
</button>

<div class="modal" tabindex="-1" id="updateClub">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title m-0">Edit Club</h3>
        <button type="button" class="btn-close" data-bs-dismiss="modal" />
      </div>
      <div class="modal-body">
        <form class="edit-form" id="update-club" on:submit|preventDefault={onSubmit}>
          <div class="row mb-3 align-items-center">
            <label for="name" class="col-sm-3 col-form-label"> Name </label>
            <div class="col-sm-9">
              <input id="name" bind:value={club.name} class="form-control" type="string" />
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button
          type="submit"
          form="update-club"
          class="btn btn-light"
          on:click={onSubmit}
          data-bs-dismiss="modal"
          disabled={submitDisabled}>Submit</button
        >
      </div>
    </div>
  </div>
</div>
