<script>
  import { setClient, mutate } from "svelte-apollo";
  import { client } from "./_apollo";
  import { gql } from "apollo-boost";
  import { ADD_TEACHER } from "./_queries";
  import { onMount } from "svelte";
  import Nav from '../components/Nav.svelte';
  let idn = "";
  let name = "";
  let position = "";

  onMount(async () => {
    setClient(client);
  });

  async function addTeacher(e) {
    e.preventDefault();
    try {
      await mutate(client, {
        mutation: ADD_TEACHER,
        variables: { idn, position, name }
      });
      alert("Added successfully");
      // restore , refresh query
    } catch (error) {
      alert("Bugo");
      console.log(error);
    }
  }
</script>

<style>
  main {
    background-color: rgb(233, 233, 233);
  }
</style>

<!--

<form on:submit|preventDefault={addTeacher}>
-->
<main>

  <section class="columns is-fullheight">

  
<Nav />
  

    <div class="column is-5">

      <h1 style="font-size: 3rem;">Add Teacher</h1>
      <form on:submit={addTeacher}>
        <input
          class="input"
          placeholder="ID number"
          bind:value={idn} />
        <br />
        <input
          class="input"
          placeholder="Full name"
          bind:value={name} />
        <br />
        <input
          class="input"
          placeholder="Position"
          bind:value={position} />
        <br />
        <button type="submit">Add Bio</button>
      </form>
    </div>
 <button type="submit">Add Bio</button>
  </section>

</main>
