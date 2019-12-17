<script>
  import { setClient, mutate } from "svelte-apollo";
  import { client } from "./_apollo";
  setClient(client);
  import { gql } from "apollo-boost";

  
  const ADD_TEACHER = gql`
    mutation($id_number: String!,$name: String!,$position :String!) {
      insert_bio(
        objects: {
          id_number: $id_number
          first_name: $name
          teachers: { data: { position: $position } }
        }
      ) {
        affected_rows
      }
    }
  `;

  let id_number = "";
  let name = "";
  let position = "";

  async function addBook() {
    try {
      await mutate(client, {
        mutation: ADD_BOOK,
        variables: { id_number, name, position }
      });
    } catch (error) {
      console.log(error);
    }
  }
</script>

<form on:submit={addBook}>
  <label for="book-author">ID NUMBER</label>
  <input type="text" id="book-author" bind:value={id_number} />
  <br />
  <label for="book-title">NAME</label>
  <input type="text" id="book-title" bind:value={name} />
  <br />
  <label for="book-title">Poistion</label>
  <input type="text" id="book-title" bind:value={position} />
  <br />
  <button type="submit">Add Bio</button>
</form>
