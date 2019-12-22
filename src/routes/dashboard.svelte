<svelte:head>
	<title>Dashboard</title>
</svelte:head>
<script>
import { onMount } from 'svelte';
import { setClient } from 'svelte-apollo';
import { client } from './_apollo';
  
//onMount(async () => {
  setClient(client);
//});


  import Test from '../components/Test.svelte';

</script>
<h1>About this site</h1>

<p>This is the 'about' page. There's not much here.</p>

<Test />