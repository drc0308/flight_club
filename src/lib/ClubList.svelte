<script lang="ts">
  import type { Club } from '$lib/models';
  import { clubs, activeClub } from '$lib/stores';
  import { goto } from '$app/navigation';

  export let goOnClick: boolean = true;

  function onClick(club: Club) {
    if (goOnClick && club == $activeClub) {
      goto('/sessions');
    } else {
      $activeClub = club.id;
    }
  }
</script>

<div class="club-list m-3">
  <div class="list-group">
    {#each $clubs as club}
      <li
        class="list-group-item list-group-item-action"
        class:active={club == $activeClub}
        on:click={() => onClick(club)}
      >
        {club.name}
      </li>
    {/each}
  </div>
  <p class="form-text">Your club(s)</p>
</div>

<style>
  .club-list {
    max-width: 300px;
  }
  p {
    text-align: right;
    padding: 4px;
    margin: 0;
  }
  .list-group-item.active {
    background-color: #ffda7b;
    border-color: #ffda7b;
    color: #222;
  }
</style>
