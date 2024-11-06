<script>
	import { Tree } from '$lib/components/tree';
	import { AddBucket as DialogAddBucket } from '$lib/components/dialog';
	import { useQuery } from '@sveltestack/svelte-query';
	import fetchApi from '$lib/fetch/fetch';

	/**
	 * @type {fileConfig[]}
	 */
	let buckets = [];

	/**
	 * @param {string[]} data
	 */
	const parseBuckets = (data) => {
		buckets = data.map((dt, index) => ({
			id: index,
			name: dt,
			type: 'bucket',
			isExpand: false
		}));
	};

	const queryS3Buckets = useQuery(
		['get_s3_buckets'],
		async () => await fetchApi('GET', 's3', '/buckets', ''),
		{
			staleTime: 60 * 1000,
			retry: 3
		}
	);

	$: if ($queryS3Buckets.isSuccess) {
		parseBuckets($queryS3Buckets.data);
	}
</script>

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
		<Tree treeData={buckets} />
	</div>
</div>
<div class="flex-auto border-2 border-dashed border-sky-500">
	<!-- The dataframe or folder/file meta data -->
</div>
