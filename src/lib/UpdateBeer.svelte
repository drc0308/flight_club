<script lang="ts">
  import { onMount } from 'svelte';
  import type { Beer } from '$lib/models';
  import { activeClub } from '$lib/stores';
  import { beerDefaults } from '$lib/models';
  import { newBeerId, updateBeer, deleteBeer } from '$lib/firebase';


  // Get the bootstrap Modal HTML element to open programatically
  let updateBeerElement: Element = undefined;
  let updateBeerModal: any;
  onMount(async () => {
    const Modal = (await import('bootstrap/js/dist/modal.js')).default;
    updateBeerModal = new Modal(updateBeerElement);
  });

  export let session: number;
  let newBeer = beerDefaults;
  let editBeer = newBeer;
  let addingNewBeer = false;
  $: newBeer.session = session;
  $: submitDisabled = editBeer.session ? false : true;
  
  export function openBeerEditor(data: Beer, newBeer: boolean = false) {
    addingNewBeer = newBeer;
    editBeer = { ...data };
    updateBeerModal.show();
  }

  function onSubmit() {
    if (addingNewBeer) {
      editBeer.id = newBeerId();
      addingNewBeer = false;
    }  
    editBeer.club = $activeClub.id;
    updateBeer(editBeer);
    if (document.activeElement instanceof HTMLElement) { document.activeElement.blur() };
  }  

  function onDelete() {
    if (confirm('Delete this beer?')) {
      deleteBeer(editBeer.id);
    }  
  }  
</script>

<button type="button" class="btn btn-light mx-2" on:click={() => openBeerEditor(newBeer, true)}>
  Add Beer
</button>

<div class="modal" tabindex="-1" id="updateBeer" bind:this={updateBeerElement}>
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title m-0">{addingNewBeer ? 'Add' : 'Edit'} Beer</h3>
        <button type="button" class="btn-close" data-bs-dismiss="modal" />
      </div>
      <div class="modal-body">
        <form id="update-beer" class="edit-form" on:submit|preventDefault={onSubmit}>
          <div class="row mb-3 align-items-center">
            <label for="session" class="col-sm-3 col-form-label">Session</label>
            <div class="col">
              <input
                id="session"
                bind:value={editBeer.session}
                class="form-control"
                type="number"
              />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="order" class="col-sm-3 col-form-label">Order</label>
            <div class="col">
              <input id="order" bind:value={editBeer.order} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="user" class="col-sm-3 col-form-label">Member</label>
            <div class="col">
              <input id="user" bind:value={editBeer.user} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="score" class="col-sm-3 col-form-label">Score</label>
            <div class="col">
              <input
                id="score"
                bind:value={editBeer.score}
                class="form-control"
                type="number"
                inputmode="decimal"
              />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="win" class="col-sm-3 col-form-label">Win</label>
            <div class="col">
              <input
                id="win"
                bind:checked={editBeer.win}
                class="form-check-input"
                type="checkbox"
              />
            </div>
          </div>
          <hr />
          <div class="row mb-3 align-items-center">
            <label for="name" class="col-sm-3 col-form-label">Beer Name</label>
            <div class="col">
              <input id="name" bind:value={editBeer.name} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="brewery" class="col-sm-3 col-form-label">Brewery</label>
            <div class="col">
              <input id="brewery" bind:value={editBeer.brewery} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="type" class="col-sm-3 col-form-label">Beer Type</label>
            <div class="col">
              <input id="type" bind:value={editBeer.type} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="style" class="col-sm-3 col-form-label">Specific Type</label>
            <div class="col">
              <input id="style" bind:value={editBeer.style} class="form-control" type="text" />
            </div>
          </div>
          <div class="row mb-3 align-items-center">
            <label for="abv" class="col-sm-3 col-form-label">ABV</label>
            <div class="col">
              <input
                id="abv"
                bind:value={editBeer.abv}
                class="form-control"
                type="number"
                inputmode="decimal"
              />
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button
          type="button"
          class="btn btn-light"
          on:click={onDelete}
          data-bs-dismiss="modal"
          hidden={addingNewBeer}>Delete</button
        >
        <button
          type="submit"
          form="update-beer"
          class="btn btn-light"
          on:click={onSubmit}
          data-bs-dismiss="modal"
          disabled={submitDisabled}>Submit</button
        >
      </div>
    </div>
  </div>
</div>
