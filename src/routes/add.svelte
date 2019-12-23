<script>
  import { setClient, mutate } from "svelte-apollo";
  import { client } from "./_apollo";
  import { ADD_TEACHER } from "./_queries";
  import { onMount } from "svelte";
  import Nav from "../components/Nav.svelte";
  import Validator from "fastest-validator";
  import toastr from 'toastr';
toastr.options = {
  "positionClass":"toast-top-full-width"
}

onMount(async () => {
  setClient(client);
});

  // $: idn, validate();

  let errors = [],
    validity = [],
    valid = false;

  let idn, name, position;

  let v = new Validator({
    messages: {
      stringMin: "too short",
      required: "this field is required"
    }
  });
  const schema = {
    idn: { type: "string", min: 3, max: 255 },
    name: { type: "string", min: 3, max: 255 },
    position: { type: "string", min: 3, max: 255 }
  };
  var check = v.compile(schema);
  function validate() {
    let c = check({ idn, name, position });
    errors = Array.isArray(c) ? c : []; // data from check function
    validity = errors.map(e => e.field); // map invalid fields
    valid = validity.length === 0 ? true : false; // true if all fields valid
  }





  async function addTeacher(e) {
    e.preventDefault();
    validate();
    if (valid == true) {
      try {
        // show loading
         toastr.success('added teacher', 'Success!')
        await mutate(client, {
          mutation: ADD_TEACHER,
          variables: { idn, position, name }
        });

        
        //alert("Added successfully");
        valid = false;
        idn = "";
        name = "";
        position = "";
      } catch (error) {
        alert("Bugo");
        console.log(error);
      }
    }
  }
</script>

<style>

  main {
    background-color: rgb(233, 233, 233);
  }
  h1 {
    @apply bg-black text-white;
  }
</style>

<main>

  <section class="hero is-fullheight">

    <div class="columns">

      <Nav />

      <div class="column is-5" style="padding: 3rem 1.5rem;">
        <div class="card" style="padding: 1rem 1.5rem;">
          <h1 style="font-size: 3rem;">Add Teacher</h1>
          <form on:submit={addTeacher}>
            <div class="field">

              <div class="control">
                <input
                  class="input {validity.includes('idn') ? 'is-danger' : ''}"
                  placeholder="ID number"
                  bind:value={idn} />
              </div>
              {#if validity.includes('idn')}
                <p class="help is-danger">
                  {errors.find(e => e['field'] === 'idn').message}
                </p>
              {/if}
            </div>
            <div class="field">
              <div class="control">
                <input
                  class="input {validity.includes('name') ? 'is-danger' : ''}"
                  placeholder="Full name"
                  bind:value={name} />
              </div>
              {#if validity.includes('name')}
                <p class="help is-danger">
                  {errors.find(e => e['field'] === 'name').message}
                </p>
              {/if}
            </div>
            <div class="field">
              <div class="control">
                <input
                  class="input {validity.includes('position') ? 'is-danger' : ''}"
                  placeholder="Position"
                  bind:value={position} />

                {#if validity.includes('position')}
                  <p class="help is-danger">
                    {errors.find(e => e['field'] === 'position').message}
                  </p>
                {/if}
              </div>
            </div>
            
            <button  class="button is-primary {valid ? 'is-loading' : ''}" type="submit" >Add Bio</button>
          </form>
        </div>
      </div>
      <div class="column is-5" style="padding: 3rem 1.5rem;">
        <div class="card" style="padding: 1rem 1.5rem;" />

      </div>
    </div>
  </section>

</main>
