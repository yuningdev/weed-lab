<script>
	import { Tree } from '$lib/components/tree';
	import { AddBucket as DialogAddBucket } from '$lib/components/dialog';
	import { Bucket } from '$lib/components/tree';
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
			id: `bucket_${dt}`,
			name: dt,
			type: 'bucket'
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

<div class="h-8 flex flex-row flex-nowrap justify-between items-center">
	<!-- The title row -->
	<div>
		<span class="text-2xl">Bucket</span>
		<span>--</span>
	</div>

	<DialogAddBucket />
</div>
<div class="flex-auto rounded-lg bg-white p-4 shadow-sm dark:bg-gray-950">
	<Bucket data={buckets} />
</div>
