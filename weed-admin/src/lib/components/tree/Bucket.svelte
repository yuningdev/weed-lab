<script>
	import Directory from './Directory.svelte';
	import { IconFile, IconOpenFolder, IconArrowDown, IconBucket } from '$lib/components/icon';
	/**
	 * @type {{ data: any}}
	 */
	let { data } = $props();
</script>

{#each data as datum}
	<Directory
		id={datum.id}
		type="bucket"
		name={datum.name}
		onToggleHandle={(id) => console.log('eve', id)}
	/>
{/each}
