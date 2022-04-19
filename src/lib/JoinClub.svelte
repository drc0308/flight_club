<script lang="ts">
  import type { Unsubscribe } from '@firebase/util';
  import type { Club } from '$lib/models';
  import { onMount } from 'svelte';
  import { user, activeClub } from '$lib/stores';
  import { watchAllClubs, joinClub } from '$lib/firebase';
  import { goto } from '$app/navigation';

  let joinClubElement: Element = undefined;
  let joinClubModal: any;
  onMount(async () => {
    const Modal = (await import('bootstrap/js/dist/modal.js')).default;
    joinClubModal = new Modal(joinClubElement);
  });
  
  let clubs: Club[] = [];
  let selected: Club = null;
  let unsubscribe: Unsubscribe = () => undefined;
  
  $: submitDisabled = !selected;

  function onJoinClub() {
    unsubscribe = watchAllClubs((update) => {
      clubs = update;
    });

    joinClubModal.show();
  }

  async function onSubmit() {
    await joinClub($user.id, selected);
    unsubscribe();
    $activeClub = selected.id;
    joinClubModal.hide();
    goto('/members');
  }

</script>

<div class="text-center">
  <button type="button" class="btn btn-light mx-3" on:click={() => onJoinClub()}>
    Join a Club!
  </button>
</div>

<div class="modal" tabindex="-1" id="joinClub" bind:this={joinClubElement}>
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title m-0">Join a Club</h3>
        <button type="button" class="btn-close" data-bs-dismiss="modal" />
      </div>
      <div class="modal-body">
        <ul class="list-group">
          {#each clubs as club}
            <li
              class="list-group-item"
              class:active={club == selected}
              on:click={() => (selected = club)}
            >
              {club.name}
            </li>
          {/each}
        </ul>
      </div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-light"
          on:click={onSubmit}
          data-bs-dismiss="modal"
          disabled={submitDisabled}>Join</button
        >
      </div>
    </div>
  </div>
</div>

<style>
  .list-group-item.active {
    background-color: #ffda7b;
    border-color: #ffda7b;
    color: #222;
  }
</style>
