<script>
	import Directory from './Directory.svelte';
	/**
	 * @type {{ data: any, handleOnClick?: (id?:string) => {}}}
	 */
	let { data, handleOnClick } = $props();
</script>

{#each data as datum}
	<Directory
		id={datum.id}
		type="bucket"
		name={datum.name}
		handleOnClick={() => {
			if (handleOnClick) {
				handleOnClick(datum);
			}
		}}
	/>
{/each}
