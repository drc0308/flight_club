<script lang="ts">
  import type { Unsubscribe } from '@firebase/util';
  import { onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { Member, memberView, memberCompare, roleView, membersToCsv } from '$lib/models';
  import { user, activeClub } from '$lib/stores';
  import { watchMembers, updateMember } from '$lib/firebase';

  // Component props
  export let sortKey: string = 'name';
  export let ascending: boolean = true;

  let members: any[] = [];
  let memberList: Member[] = [];
  let unsubscribe: Unsubscribe = () => undefined;

  $: {
    unsubscribe();
    // Get members from the database and watch for changes
    unsubscribe = watchMembers($activeClub, (update: any[]) => {
      members = update;
    });
    onDestroy(unsubscribe);
  }

  function onClickRole(member: Member) {
    if (member.roles.admin) member.roles.editor = true;
    if (member.roles.editor) member.roles.viewer = true;
    updateMember(member);
  }

  // Handle member inputs to re-sort, triggers the reactive block below
  function onClickColumn(key: string) {
    if (key == sortKey) {
      ascending = !ascending;
    } else {
      sortKey = key;
    }
  }

  // Reactive block which re-runs when the sort type changes
  $: {
    function compare(a: Member, b: Member) {
      if (memberCompare[sortKey](a, $activeClub.id) > memberCompare[sortKey](b, $activeClub.id)) {
        return ascending ? 1 : -1;
      } else if (memberCompare[sortKey](a, $activeClub.id) < memberCompare[sortKey](b, $activeClub.id)) {
        return ascending ? -1 : 1;
      } else {
        return 0;
      }
    }
    memberList = members.sort(compare);
  }

  function onClickMember(member: Member) {
    // Goto a specific member page
    goto(`/member/${member.id}`);
  }
</script>

<div class="table-div">
  <table class="table table-striped table-hover">
    <thead>
      <tr>
        {#each memberView as field}
          <th width={field.width} on:click={() => onClickColumn(field.key)} style:cursor='pointer'>
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
        {#if $user.roles.admin}
          {#each roleView as field}
            <th class="text-center" width={field.width}>
              {field.text}
            </th>
          {/each}
        {/if}
      </tr>
    </thead>
    <tbody>
      {#each memberList as member}
        <tr>
          {#each memberView as field}
            <td on:click={() => onClickMember(member)} style:cursor='pointer'>
              {field.show(member, $activeClub.id)}
            </td>
          {/each}
          {#if $user.roles.admin}
            {#each roleView as field}
              <td class="text-center">
                <input
                  class="form-check-input"
                  type="checkbox"
                  bind:checked={member.roles[field.key]}
                  disabled={field.disable(member, $user)}
                  on:change={() => onClickRole(member)}
                  style:cursor='pointer'
                />
              </td>
            {/each}
          {/if}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
<button type="button" class="btn btn-light mx-2" on:click={() => membersToCsv(members)}
  >Download as CSV</button
>

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
</style>
