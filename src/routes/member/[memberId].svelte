<script lang="ts">
  import type { Unsubscribe } from '@firebase/util';
  import { afterUpdate, onDestroy } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { user, activeClub } from '$lib/stores';
  import { watchMember } from '$lib/firebase';
  import MemberInfo from '$lib/MemberInfo.svelte';
  import BeerList from '$lib/BeerList.svelte';
  import UpdateProfile from '$lib/UpdateProfile.svelte';
  import ClubList from '$lib/ClubList.svelte';

  let member: any = { name: null };
  let clubId: string;

  $: isCurrentUser = ($page.params.memberId == $user.id);
  
  // Leave the page if active club changes, use subscribe instead of $: for immediate effect
  const unsubscribeClub = activeClub.subscribe((update) => {
    if (
      !isCurrentUser && // For logged in user, all clubs will be valid
      clubId && // Only leave if page is already populated
      update.id != clubId  // Only leave if there is actually a change to the activeClub
    ) { 
      goto('/members');
    }
    clubId = update.id;
  });

  // Get member from the database and watch for changes
  let unsubscribeMember: Unsubscribe;
  $: {
    if (unsubscribeMember) { unsubscribeMember() }
    unsubscribeMember = watchMember($page.params.memberId, (update: any) => {
      member = update;
    });
  }

  onDestroy(() => {
    unsubscribeClub();
    unsubscribeMember();
  });
</script>

<svelte:head>
  <title>FC &#183; {member.full_name ?? 'Member'}</title>
</svelte:head>

<h1>{member.name}</h1>
<MemberInfo {member} />
{#if isCurrentUser}
  <ClubList goOnClick={false} />
{/if}
{#if isCurrentUser || $user.roles.admin}
  <UpdateProfile bind:member />
{/if}
<h1>Beers</h1>
<BeerList filterKey="user" filterValue={member.name} />
