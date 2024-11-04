<script>
	import { IconFile, IconOpenFolder, IconArrowDown, IconBucket } from '$lib/components/icon';
	import { Tree } from './index';

	/**
	 * @typedef {{id: number, name: string, updateTime?: string, type: string, isExpand?: boolean, children?: fileConfig[] }} fileConfig
	 * @type {fileConfig[]}
	 */
	const tree = [
		{
			id: 1,
			name: 'Documents',
			type: 'bucket',
			isExpand: false,
			children: [
				{
					id: 2,
					name: 'Report.docx',
					type: 'file'
				},
				{
					id: 3,
					name: 'Presentation.pptx',
					type: 'file'
				},
				{
					id: 4,
					name: 'Images',
					type: 'folder',
					isExpand: false,
					children: [
						{
							id: 5,
							name: 'Logo.png',
							type: 'file'
						},
						{
							id: 6,
							name: 'Mockup.jpg',
							type: 'file'
						}
					]
				}
			]
		},
		{
			id: 7,
			name: 'Downloads',
			type: 'bucket',
			isExpand: false,
			children: [
				{
					id: 8,
					name: 'File1.pdf',
					type: 'file'
				},
				{
					id: 9,
					name: 'File2.zip',
					type: 'file'
				}
			]
		},
		{
			id: 10,
			name: 'Desktop',
			type: 'bucket',
			isExpand: false,
			children: []
		}
	];

	let { treeData = tree } = $props();

	/**
	 * @param {number} id
	 */
	const handleToggle = (id) => {
		const newTreeData = treeData.map((item) =>
			item.id === id ? { ...item, isExpand: !item.isExpand } : item
		);
		treeData = newTreeData;
	};
</script>

{#each treeData as data}
	{@const { id, isExpand, children, type, name } = data}
	<div>
		<div
			class={`flex items-center gap-2 px-2 py-1 hover:bg-gray-100 dark:hover:bg-gray-800 ${
				type === 'folder' ? 'cursor-pointer' : ''
			}`}
			role="button"
			aria-label="click"
			tabindex={0}
			onkeydown={(eve) => {}}
			onclick={() => ['bucket', 'folder'].includes(type) && handleToggle(id)}
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

			{#if children !== undefined}
				{#if ['bucket', 'folder'].includes(type) && children.length > 0}
					<IconArrowDown class="h-4 w-4 text-gray-500 dark:text-gray-400" />
				{/if}
			{/if}
		</div>
		{#if children}
			{#if isExpand && children.length > 0}
				<div class="pl-6">
					<Tree treeData={children} />
				</div>
			{/if}
		{/if}
	</div>
{/each}
