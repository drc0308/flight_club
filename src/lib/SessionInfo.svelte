<script lang="ts">
  import type { Session } from '$lib/models';
  export let session: Session;
</script>

<div class="row mx-2" style="max-width: 600px">
  <div class="col-sm">
    <p>
      <strong>Date:</strong>
      {session.date ? session.date : ''}
    </p>
  </div>
  <div class="col-sm">
    <p>
      <strong>Winner:</strong>
      {session.winner ? session.winner : ''}
    </p>
  </div>
</div>
<div class="row mx-2" style="max-width: 600px">
  <div class="col-sm">
    <p>
      <strong>Location:</strong>
      {session.location ? session.location : ''}
    </p>
  </div>
  <div class="col-sm">
    <p>
      <strong>Average ABV:</strong>
      {session.avg_abv ? session.avg_abv.toFixed(1) : ''}
    </p>
  </div>
</div>
