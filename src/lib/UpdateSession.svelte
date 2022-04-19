<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { activeClub } from '$lib/stores';
  import { newSessionId, updateSession } from '$lib/firebase';
  import { sessionDefaults } from '$lib/models';

  onMount(async () => {
    await import('bootstrap/js/dist/modal.js');
  });

  export let session = sessionDefaults;
  $: submitDisabled = session.number == null;

  async function onSubmit() {
    session.id = session.id ? session.id : newSessionId();
    session.club = $activeClub.id;
    await updateSession(session);
    goto(`/session/${session.id}`);
    if (document.activeElement instanceof HTMLElement) { document.activeElement.blur() };
  }
</script>

<button
  type="button"
  class="btn btn-light mx-2"
  data-bs-toggle="modal"
  data-bs-target="#updateSession"
>
  {session.id ? 'Edit' : 'Add'} Session
</button>

<div class="modal" tabindex="-1" id="updateSession">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title m-0">{session.id ? 'Edit' : 'Add'} Session</h3>
        <button type="button" class="btn-close" data-bs-dismiss="modal" />
      </div>
      <div class="modal-body">
        <form id="update-session" class="edit-form" on:submit|preventDefault={onSubmit}>
          <div class="row mb-3 align-items-center">
            <label for="number" class="col-sm-3 col-form-label">Number</label>
            <div class="col-sm-9">
              <input id="number" bind:value={session.number} class="form-control" type="number" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="date" class="col-sm-3 col-form-label">Date</label>
            <div class="col-sm-9">
              <input id="date" bind:value={session.date} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="location" class="col-sm-3 col-form-label">Host / Location</label>
            <div class="col-sm-9">
              <input id="location" bind:value={session.location} class="form-control" type="text" />
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button
          type="submit"
          form="update-session"
          class="btn btn-light"
          on:click={onSubmit}
          data-bs-dismiss="modal"
          disabled={submitDisabled}>Submit</button
        >
      </div>
    </div>
  </div>
</div>
