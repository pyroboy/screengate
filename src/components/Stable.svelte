<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	export let columns;
	export let rows;
		console.log(rows);
	export let sortBy = "";
	export let sortOrder = 1;
	export let iconAsc = '▲';
	export let iconDesc = '▼';
	let sortFunction = () => "";
	let showFilterHeader = columns.some(c => c.filterOptions !== undefined);
	let filterValues = {};
	let filterSettings = {};
	let columnByKey = {};
	columns.forEach(col => {
	  columnByKey[col.key] = col;
	});

	
	$: c_rows = rows
	  .filter(r =>
	    Object.keys(filterSettings).every(f => {
	      let ret =  (
	        filterSettings[f] === undefined ||
	        filterSettings[f] === columnByKey[f].filterValue(r)
				);
				return ret;
	    })
	  )
	  .map(r => (Object.assign({}, r, {$sortOn: sortFunction(r)} ) ) )
	  .sort((a, b) => {
	    if (a.$sortOn > b.$sortOn) return sortOrder;
	    else if (a.$sortOn < b.$sortOn) return -sortOrder;
	    return 0;
	  });
	const calculateFilterValues = () => {
	  filterValues = {};
	  columns.forEach(c => {
	    if (typeof c.filterOptions === "function") {
	      filterValues[c.key] = c.filterOptions(rows);
	    } else if (Array.isArray(c.filterOptions)) {
	      filterValues[c.key] = [...c.filterOptions];
	    }
	  });
	};
	$: {
		let col = columnByKey[sortBy];
	  if (col !== undefined && col.sortable === true && typeof col.value === "function") {
	    sortFunction = r => col.value(r);
	  }
	};
	const updateSortOrder = (colKey) => {
		if (colKey === sortBy) {
			sortOrder = sortOrder === 1 ? -1 : 1
		} else {
			sortOrder = 1;
		}
	}
	
	const handleClickCol = (col) => {
		updateSortOrder(col.key)
		sortBy = col.key;
		dispatch('clickCol', {key:col.key} );
	}
	
	const handleClickRow = (row) => {
		dispatch('clickRow', {row} );
	}
	const handleClickCell = (row, key) => {
		dispatch('clickCell', {row, key} );
	}
	if (showFilterHeader) {
	  calculateFilterValues();
	}
</script>

<table class="w-full table-auto">
	{#if showFilterHeader}
		<tr class="w-full">
		  {#each columns as col}
		  	<th class="w-full px-4 py-2">
					{#if filterValues[col.key] !== undefined}
						<select class="w-full" bind:value={filterSettings[col.key]}>
							<option value={undefined}></option>
						  {#each filterValues[col.key] as option}
								<option value={option.value}>{option.name}</option>
						  {/each}
						</select>
					{/if}
				</th>
		  {/each}
		</tr>
	{/if}
		<slot name="header" sortOrder={sortOrder} sortBy={sortBy}>
			<tr class="w-full">
			  {#each columns as col}
			  	<th
						on:click={() => handleClickCol(col)}
						class="px-4 py-2 {[(col.sortable ? 'cursor-pointer' : '' ),(col.headerClass !== undefined && col.headerClass)].join(' ')}"
					>
						{col.title}
						{#if sortBy === col.key}
							{ sortOrder === 1 ? iconAsc : iconDesc}
						{/if}
					</th>
			  {/each}
			</tr>
		</slot>
	{#each c_rows as row, n}
		<slot name="row" row={row} n={n} >
			<tr class="w-full" on:click={()=>{handleClickRow(row)}} >
			  {#each columns as col}
			  	<td
						on:click={()=>{handleClickCell(row, col.key)}}
						class="border px-4 py-2 {col.class !== undefined && col.class}"
					>{@html col.renderValue ? col.renderValue(row) : col.value(row)}</td>
			  {/each}
			</tr>
		</slot>
	{/each}
</table>