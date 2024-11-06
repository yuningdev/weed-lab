<script>
	import { QueryClient, QueryClientProvider } from '@sveltestack/svelte-query';
	import { ObjectStorage } from '$lib/components/containers';

	// Create a client
	const queryClient = new QueryClient();
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<QueryClientProvider client={queryClient}>
	<div class="h-screen w-screen overflow-hidden p-4">
		<div class="flex h-full w-full flex-col gap-4">
			<div class="flex h-2/4 w-full flex-row gap-4">
				<ObjectStorage />
			</div>
			<div class="flex w-full w-full flex-1 border-2 border-dashed border-sky-500">
				<!-- The visualization of selected data -->
			</div>
		</div>
	</div>
</QueryClientProvider>
