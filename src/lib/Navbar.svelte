<script lang="ts">
  import type { Member } from '$lib/models';
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, clubs, activeClub } from '$lib/stores';
  import { logout, watchAuthState } from '$lib/firebase';
  import GoogleSignIn from '$lib/GoogleSignIn.svelte';

  // Need this object accessible to open the modal box programatically
  let navbarElement: Element;
  let navbarCollapse: any;
  onMount(async () => {
    const Collapse = (await import('bootstrap/js/dist/collapse.js')).default;
    await import('bootstrap/js/dist/dropdown.js');
    navbarCollapse = new Collapse(navbarElement, { toggle: false });
  });

  // Watch for login/logout events from the auth library
  const unsubscribe = watchAuthState((updatedUser: Member) => {
    $user = updatedUser;
  });

  onDestroy(unsubscribe);

  function closeNavbar() {
    // Bootstrap navbars don't auto-close, so added that feature
    if (navbarCollapse != undefined) {
      navbarCollapse.hide();
    }
  }

  function onLogout() {
    logout();
    goto('/');
  }
</script>

<svelte:window on:click={closeNavbar} />
<nav class="navbar navbar-expand-md navbar-light container-fluid">
  <a href="/" class="me-3">
    <img src="/img/Flight-Club.svg" alt="flight club logo" style="max-width: 150px" />
  </a>
  <button
    class="navbar-toggler"
    type="button"
    data-bs-toggle="collapse"
    data-bs-target="#navbarNav"
    aria-controls="navbarNav"
    aria-expanded="false"
  >
    <span class="navbar-toggler-icon" />
  </button>
  <div id="navbarNav" class="collapse navbar-collapse mt-2" bind:this={navbarElement}>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link px-2" href="/members">Members</a>
      </li>
      <li class="nav-item">
        <a class="nav-link px-2" href="/sessions">Sessions</a>
      </li>
      <li class="nav-item">
        <a class="nav-link px-2" href="/beers">Beers</a>
      </li>
    </ul>
    <hr class="dropdown-divider" />
    <ul class="navbar-nav ms-auto">
      {#if $user}
        <li class="nav-item dropdown">
          <a
            class="nav-link px-2"
            href={undefined}
            role="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            on:click|stopPropagation
          >
            {$user.full_name}
            <img
              class="rounded-circle align-middle ms-1"
              width="30"
              src={$user.photoURL}
              alt="Profile"
            />
          </a>
          <div class="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
            {#each $clubs as club}
              <button
                class="dropdown-item"
                class:active={club == $activeClub}
                on:click={() => ($activeClub = club.id)}
              >
                {club.name}
              </button>
            {/each}
            <hr class="dropdown-divider" />
            <a class="dropdown-item" href={'/member/' + $user.id}>Profile</a>
            <button class="dropdown-item" on:click={onLogout}>Sign Out</button>
          </div>
        </li>
      {:else}
        <li class="nav-item">
          <GoogleSignIn />
        </li>
      {/if}
    </ul>
  </div>
</nav>

<style lang="scss">
  .navbar {
    background: #ffecbc;
  }
  .navbar-toggler {
    border: 0px;
  }
  .navbar-toggler:focus {
    box-shadow: 0 0 0 0;
  }
  .nav-link {
    font-size: 20px;
    font-family: Roboto, sans-serif;
    border-radius: 3px;
  }
  .nav-link:hover {
    background: #ffda7b;
    cursor: pointer;
  }
  .dropdown-item.active {
    background-color: #ffda7b;
    border-color: #ffda7b;
    color: #222;
  }
</style>
