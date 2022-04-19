<script lang="ts">
  import type { Unsubscribe } from '@firebase/util';
  import { onDestroy, createEventDispatcher } from 'svelte';
  import { goto } from '$app/navigation';
  import { activeClub } from '$lib/stores';
  import { Beer, beerView, beersToCsv } from '$lib/models';
  import { getSessionId, getMemberId, watchBeers } from '$lib/firebase';

  const dispatch = createEventDispatcher();

  // Component props
  export let filterKey: string = null;
  export let filterValue: string | number = null;
  export let ascending: boolean = true;
  export let sortKey: string = 'brewery';
  export let searchable: boolean = false;
  export let clickToEdit: boolean = false;
  export let hasBeers: boolean = false;

  let beers: any[] = [];
  let beerList: Beer[] = [];
  let searchTerm: string = '';
  let unsubscribe: Unsubscribe = () => undefined;

  $: {
    unsubscribe();
    // Get beers from the database and watch for updates
    unsubscribe = watchBeers($activeClub.id, (update) => {
      beers = update;
    });
    onDestroy(unsubscribe);
  }

  async function onClickBeer(beer: Beer, key: string) {
    // A bit hacky but change click behavior for displaying beers on different pages
    if (clickToEdit) {
      // Dispatch click events to parent to handle more complex actions (ie. editing)
      dispatch('beerClick', beer);
    } else if (key == 'session') {
      // Goto a specific session page
      const id = await getSessionId($activeClub.id, beer.session);
      goto(`/session/${id}`);
    } else if (key == 'user') {
      try {
        // Goto a specific member page
        const id = await getMemberId(beer.user);
        goto(`/member/${id}`);
      } catch (error) {
        console.log(error.message);
      }
    }
  }

  const isLink = (type: string) => {
    // Used to make the cursor a pointer when the cell is clickable
    return clickToEdit || type == 'session' || type == 'user';
  }

  // Handle user inputs to re-sort, triggers the reactive block below
  function onClickColumn(key: string) {
    if (key == sortKey) {
      ascending = !ascending;
    } else {
      sortKey = key;
    }
  }

  // Reactive block which re-runs when the search term or sort type changes
  $: {
    const searchTermLower = searchTerm.toLowerCase();

    // Update the search function
    function search(beer: Beer): boolean {
      if (filterKey && beer[filterKey] != filterValue) {
        // Exclude beers by filter keys for session or member page
        return false;
      }
      if (!searchable || !searchTerm) {
        return true;
      } else {
        return (
          // The search box only considers these fields
          (beer.name ? beer.name.toLowerCase().includes(searchTermLower) : false) ||
          (beer.brewery ? beer.brewery.toLowerCase().includes(searchTermLower) : false) ||
          (beer.type ? beer.type.toLowerCase().includes(searchTermLower) : false) ||
          (beer.user ? beer.user.toLowerCase().includes(searchTermLower) : false)
        );
      }
    }

    // Update the sorting function
    function compare(a: Beer, b: Beer) {
      if (a[sortKey] > b[sortKey]) {
        return ascending ? 1 : -1;
      } else if (a[sortKey] < b[sortKey]) {
        return ascending ? -1 : 1;
      } else {
        return 0;
      }
    }

    // Filter and sort the list for rendering
    beerList = beers.filter(search).sort(compare);
    hasBeers = !!beerList.length;
  }
</script>

{#if searchable}
  <div class="w-auto mx-2">
    <input
      type="search"
      class="form-control has-clear"
      style="max-width: 768px"
      placeholder="Search"
      bind:value={searchTerm}
    />
    <div class="form-text text-end" style="max-width: 768px">Edit beers from the session page</div>
  </div>
{/if}

<div class="table-div">
  <table class="table table-striped table-hover">
    <thead>
      <tr>
        {#each beerView.filter((field) => field.key != filterKey) as field}
          <th width={field.width} on:click={() => onClickColumn(field.key)}>
            {field.text}
            {#if field.key == sortKey}
              <span class="arrow">
                {#if ascending}
                  &#x25B2;
                {:else}
                  &#x25BC;
                {/if}
              </span>
            {/if}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each beerList as beer}
        <tr>
          {#each beerView.filter((field) => field.key != filterKey) as field}
            <td on:click={() => onClickBeer(beer, field.key)} class:is-link={isLink(field.key)}>
              {field.show(beer)}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
{#if searchable}
  <button type="button" class="btn btn-light mx-2" on:click={() => beersToCsv(beers)}
    >Download as CSV</button
  >
{/if}

<style>
  .arrow {
    color: #116466;
  }
  .table-div {
    overflow: auto;
  }
  table {
    width: 100%;
    overflow: auto;
    table-layout: fixed;
  }
  th {
    text-align: left;
  }
  .is-link {
    cursor: pointer;
  }
</style>
