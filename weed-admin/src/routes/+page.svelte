<script>
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import { ObjectStorage } from '$lib/components/containers';

	// Create a client
	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				staleTime: 60 * 1000,
				retry: 3
			}
		}
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<QueryClientProvider client={queryClient}>
	<div class="h-screen w-screen overflow-hidden p-4">
		<div class="flex h-full w-full flex-col gap-4">
			<div class="h-2/4 w-full">
				<div class="flex h-full flex-col p-4">
					<ObjectStorage />
				</div>
				<!-- The dataframe or folder/file meta data -->
				<!-- <div class="flex-auto border-2 border-dashed border-gray-100">
				</div> -->
			</div>

			<div class="flex w-full w-full flex-1 border-2 border-dashed border-gray-100"></div>
		</div>
	</div>
</QueryClientProvider>
