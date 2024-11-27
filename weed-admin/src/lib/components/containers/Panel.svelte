<script>
	import { createQuery } from '@tanstack/svelte-query';
	import fetchApi from '$lib/fetch/fetch';
	import { storeQueryStatement } from '../../stores';
	import * as Table from '../ui/table';

	/**
	 * @param {any} data
	 */
	const parseSchema = (data) => {
		console.log('data***', data);
	};

	$: queryDuckDBS3Schema = createQuery({
		queryKey: [
			'get_duckdb_s3_schema',
			...Object.values($storeQueryStatement['queryDuckDBS3Schema'])
		],
		queryFn: async () =>
			await fetchApi('GET', 'duckdb', '/s3/schema', $storeQueryStatement['queryDuckDBS3Schema']),
		enabled: Object.values($storeQueryStatement['queryDuckDBS3Schema']).some((ele) => ele)
	});

	$: if ($queryDuckDBS3Schema.isSuccess) {
		parseSchema($queryDuckDBS3Schema.data);
	}
</script>

{#if $queryDuckDBS3Schema.data}
	<!-- {#each $queryDuckDBS3Schema.data as data}
		<div>
			<span>{data.id}</span>
			<span>Data Type: {data.dt_type}</span>
		</div>
	{/each} -->
	<div class="w-full overflow-auto">
		<Table.Root>
			<Table.Caption>The Schema of selected file</Table.Caption>
			<Table.Header>
				<Table.Row>
					<Table.Head class="w-[240px]">Colum Name</Table.Head>
					<Table.Head>Data Type</Table.Head>
				</Table.Row>
			</Table.Header>
			<Table.Body>
				{#each $queryDuckDBS3Schema.data as data, i (i)}
					<Table.Row>
						<Table.Cell class="font-medium">{data.id}</Table.Cell>
						<Table.Cell>{data.dt_type}</Table.Cell>
					</Table.Row>
				{/each}
			</Table.Body>
		</Table.Root>
	</div>
{/if}
