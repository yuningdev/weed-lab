<script>
	import { Tree } from '$lib/components/tree';
	import { AddBucket as DialogAddBucket } from '$lib/components/dialog';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<!-- <Tree /> -->
<div class="h-screen w-screen overflow-hidden p-4">
	<div class="flex h-full w-full flex-col gap-4">
		<div class="flex h-2/4 w-full flex-row gap-4">
			<div class="flex-auto border-2 border-dashed border-sky-500 p-4">
				<div class="flex flex-row flex-nowrap justify-between">
					<!-- The title row -->
					<div>
						<span class="text-2xl">Bucket</span>
						<span>--</span>
					</div>

					<DialogAddBucket />
				</div>
				<!-- The tree folder -->
				<div class="rounded-lg bg-white p-4 shadow-sm dark:bg-gray-950">
					<Tree />
				</div>
			</div>
			<div class="flex-auto border-2 border-dashed border-sky-500">
				<!-- The dataframe or folder/file meta data -->
			</div>
		</div>

		<div class="flex w-full w-full flex-1 border-2 border-dashed border-sky-500">
			<!-- The visualization of selected data -->
		</div>
	</div>
</div>
