<script>
	import { IconFile, IconOpenFolder, IconArrowDown, IconBucket } from '$lib/components/icon';
	/**
	 * @type {{ type: 'folder' | 'bucket' | 'file', onToggleHandle?: (id: string) => void, id: string, name: string}}
	 */
	let { type = 'folder', onToggleHandle, id, name = '--' } = $props();
</script>

<div
	class={`flex items-center gap-2 px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-800`}
	role="button"
	aria-label="click"
	tabindex={0}
	onkeydown={(eve) => {}}
	onclick={() => {
		if (onToggleHandle) onToggleHandle(id);
	}}
>
	{#if type === 'folder'}
		<IconOpenFolder class="h-5 w-5 text-primary" />
	{:else if type === 'bucket'}
		<IconBucket class="h-5 w-5 text-primary" />
	{:else}
		<IconFile class="h-5 w-5 text-gray-500 dark:text-gray-400" />
	{/if}

	<span
		class={`flex-1 text-sm font-medium ${
			type === 'file' ? 'text-gray-900 dark:text-gray-50' : 'text-gray-700 dark:text-gray-300'
		}`}
	>
		{name}
	</span>

	{#if type === 'folder'}
		{#if ['bucket', 'folder'].includes(type)}
			<IconArrowDown class="h-4 w-4 text-gray-500 dark:text-gray-400" />
		{/if}
	{/if}
</div>
