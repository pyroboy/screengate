<script>
	//import Nav from '../components/Nav.svelte';
	//export let segment;
  import "bulma/css/bulma.css";
  import Tailwindcss from '../Tailwindcss.svelte';
</script>

<!--
<Nav {segment}/>
-->
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <div class="navbar-item">
        <img
          src="https://bulma.io/images/bulma-logo.png"
          alt="Bulma: Free, open source, and modern CSS framework based on
          Flexbox"
          width="112"
          height="28" />
      </div>

    </div>
  </nav>

<main>
<Tailwindcss />
	<slot></slot>
</main>