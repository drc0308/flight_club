<script lang="ts">
  import type { Session, Beer } from '$lib/models';
  import type { Unsubscribe } from '@firebase/util';
  import { onDestroy } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { user, activeClub } from '$lib/stores';
  import { watchSession, deleteSession, findSession } from '$lib/firebase';
  import SessionInfo from '$lib/SessionInfo.svelte';
  import Recap from '$lib/Recap.svelte';
  import UpdateBeer from '$lib/UpdateBeer.svelte';
  import BeerList from '$lib/BeerList.svelte';
  import UpdateSession from '$lib/UpdateSession.svelte';
  import Photos from '$lib/Photos.svelte';
  import UserNotes from '$lib/UserNotes.svelte';

  let session: Session;
  let clubId: string;
  let hasBeers: boolean;
  let unsubscribeSession: Unsubscribe = () => undefined;

  // Leave the page if active club changes, use subscribe instead of $: for immediate effect
  const unsubscribeClub = activeClub.subscribe((update) => {
    if (session && update.id != clubId) {
      goto('/sessions');
    }
    clubId = update.id;
  });

  $: {
    unsubscribeSession();
    unsubscribeSession = watchSession($page.params.sessionId, (update: any) => {
      session = update;
    });
  }

  onDestroy(() => {
    unsubscribeSession();
    unsubscribeClub();
  });

  function onDelete() {
    if (hasBeers || session.photos.length) {
      alert('Delete all beers and photos before deleting session');
      return;
    }
    if (confirm(`Delete session ${session.number}?`)) {
      deleteSession(session.id);
      goto('/sessions');
    }
  }

  // Link the BeerList and UpdateBeer components for editing existing beers
  let openBeerEditor: (data: Beer) => void;
  function beerClick(event: CustomEvent) {
    if ($user.roles.editor) {
      openBeerEditor(event.detail);
    }
  }

  async function jumpSession(forward: boolean) {
    let result = await findSession($activeClub.id, session.number + (forward ? 1 : -1));
    if (result) {
      goto(`/session/${result}`);
    } else {
      goto('/sessions');
    }
  }
</script>

<svelte:head>
  <title>FC &#183; Session {session ? session.number : ''}</title>
</svelte:head>

<h1>
  Session {session ? session.number : ''}
  <div style:float="right">
    <a name='back' on:click={() => jumpSession(false)} style:cursor='pointer'>&#x276e</a>
    &#160
    <a name='next' on:click={() => jumpSession(true)} style:cursor='pointer'>&#x276f</a>
    &#160
  </div>
</h1>
{#if session}
  <SessionInfo {session} />

  <h3>Recap</h3>
  <Recap bind:session />

  <h3>Beers</h3>
  {#if $user.roles.editor}
    <UpdateBeer bind:openBeerEditor session={session.number} />
    <span class="text-muted">(edit by selecting below)</span>
  {/if}
  <BeerList
    filterKey="session"
    sortKey="order"
    filterValue={session.number}
    clickToEdit={true}
    on:beerClick={beerClick}
    bind:hasBeers
  />

  <h3>Photos</h3>
  <Photos {session} />
  <hr />
  {#if $user.roles.editor}
    <UpdateSession {session} />
    <button class="btn btn-light mx-2" on:click={onDelete}>Delete Session</button>
    <hr />

    <h3>User Notes</h3>
    <UserNotes sessionId={$page.params.sessionId} />
  {/if}
{/if}