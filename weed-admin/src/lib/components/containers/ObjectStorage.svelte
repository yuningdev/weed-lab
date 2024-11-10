<script>
	import { Tree } from '$lib/components/tree';
	import { AddBucket as DialogAddBucket } from '$lib/components/dialog';
	import { Bucket } from '$lib/components/tree';
	import { Folder } from '$lib/components/tree';
	import { createQuery } from '@tanstack/svelte-query';
	import fetchApi from '$lib/fetch/fetch';
	import * as Breadcrumb from '../ui/breadcrumb';

	/**
	 * @type {fileConfig[]}
	 */
	let buckets = [];
	/**
	 * @type {fileConfig[]}
	 */
	let dirs = [];

	/**
	 * @type {string[]}
	 */
	let s3Path = ['Home'];

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

	/**
	 * @param {string[]} data
	 */
	const parseDirs = (data) => {
		dirs = data.map((dt, index) => ({
			id: dt.Id,
			name: dt.Id,
			type: dt.Key.includes('/') ? 'folder' : 'file'
		}));
	};

	$: queryS3Buckets = createQuery({
		queryKey: ['get_s3_buckets'],
		queryFn: async () => await fetchApi('GET', 's3', '/buckets', '')
	});

	$: queryDirs = createQuery({
		queryKey: ['get_s3_directories', s3Path],
		queryFn: async () =>
			await fetchApi(
				'GET',
				's3',
				`/${s3Path[1]}/objects`,
				s3Path[2] && {
					prefix: s3Path[2]
				}
			),
		enabled: s3Path.length > 1
	});

	$: if ($queryS3Buckets.isSuccess) {
		parseBuckets($queryS3Buckets.data);
	}

	$: if ($queryDirs.isSuccess) {
		parseDirs($queryDirs.data);
	}

	/**
	 * @param {string | undefined} id
	 */
	const handleOnBucketClick = (id) => {
		const _bucket = buckets.find((bucket) => bucket.id === id);
		if (_bucket) {
			s3Path = [...s3Path, _bucket?.name];
		}
	};
</script>

<div class="flex grid h-8 grid-cols-12 flex-row flex-nowrap items-center justify-between gap-4">
	<!-- The title row -->
	<div class="col-span-10 flex w-4/5 items-center gap-4">
		<span class="text-2xl">Bucket</span>
		<!-- todo make path dir -->
		<Breadcrumb.Root>
			<Breadcrumb.List>
				{#each s3Path as path, index}
					{@const lastItem = index === s3Path.length - 1}
					<Breadcrumb.Item class={`${!lastItem && 'cursor-pointer'}`}>
						<Breadcrumb.Link
							onclick={(eve) => {
								s3Path = s3Path.slice(0, index + 1);
							}}
						>
							{path}
						</Breadcrumb.Link>
					</Breadcrumb.Item>
					{#if s3Path.length > 1 && !lastItem}
						<Breadcrumb.Separator />
					{/if}
				{/each}
			</Breadcrumb.List>
		</Breadcrumb.Root>
	</div>
	<div class="col-span-2">
		<DialogAddBucket />
	</div>
</div>
<div class="flex-auto rounded-lg bg-white p-4 shadow-sm dark:bg-gray-950">
	{#if s3Path.length === 1}
		<Bucket data={buckets} handleOnClick={handleOnBucketClick} />
	{:else}
		<div>
			<Folder data={dirs} />
			<!-- todo render folders and files -->
		</div>
	{/if}
</div>

<style lang="scss">
	.pointer-cursor {
		cursor: pointer;
	}
</style>
