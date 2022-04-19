<script lang="ts">
  import type { Member } from '$lib/models';
  import { activeClub } from '$lib/stores';
  export let member: Member;
  $: activeData = member.data ? member.data[$activeClub.id] ? member.data[$activeClub.id] : {} : {};
</script>

<div class="row mx-3 mb-3 align-items-center" style="max-width: 600px">
  <div class="col-auto my-auto">
    <img class="rounded-circle" width="60" src={member.photoURL} alt="member" />
  </div>
  <div class="col-auto mb-0">
    <p class="mb-0">
      <strong>{member.full_name}</strong>
      <br />
      <a href={'mailto:' + member.email}>{member.email}</a>
    </p>
  </div>
</div>
<div class="row mx-2" style="max-width: 600px">
  <div class="col-sm">
    <p>
      <strong>Wins:</strong>
      {activeData.wins ? activeData.wins : ''}
    </p>
  </div>
  <div class="col-sm">
    <p>
      <strong>Avg Score:</strong>
      {activeData.avg_score ? activeData.avg_score.toFixed(1) : ''}
    </p>
  </div>
</div>
<div class="row mx-2 mb-2" style="max-width: 600px">
  <div class="col-sm">
    <p>
      <strong>Avg ABV:</strong>
      {activeData.avg_abv ? activeData.avg_abv.toFixed(1) : ''}
    </p>
  </div>
  <div class="col-sm">
    <p>
      <strong>Win Rate:</strong>
      {activeData.win_rate ? activeData.win_rate.toFixed(2) : ''}
    </p>
  </div>
</div>
