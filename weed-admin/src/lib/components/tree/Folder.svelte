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
		type={datum.type}
		name={datum.name}
		onToggleHandle={(id) => {
			if (handleOnClick) {
				handleOnClick(id);
			}
		}}
	/>
{/each}
