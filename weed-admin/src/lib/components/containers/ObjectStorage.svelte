<script>
	import { AddBucket as DialogAddBucket } from '$lib/components/dialog';
	import Directory from '../tree/Directory.svelte';
	import { createQuery } from '@tanstack/svelte-query';
	import fetchApi from '$lib/fetch/fetch';
	import * as Breadcrumb from '../ui/breadcrumb';

	/**
	 * @typedef {{id: string | number, name: string}} dirConfig
	 */

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
	 *
	 * @param {string} prefix
	 * @param {string} name
	 */
	const getPrefixType = (prefix, name) => {
		const splitPrefix = prefix.split('/');
		const lastEle = splitPrefix[splitPrefix.length - 1];
		if (lastEle === name) {
			return 'file';
		} else {
			return 'folder';
		}
	};

	/**
	 * @param {{Id: string, Key: string}[]} data
	 */
	const parseDirs = (data) => {
		dirs = data.map((dt, index) => ({
			id: dt.Id,
			name: dt.Id,
			type: getPrefixType(dt.Key, dt.Id)
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
				s3Path.length > 2 && {
					prefix: s3Path.slice(2).join('/')
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
	 * @param {dirConfig} data
	 */
	const handleOnBucketClick = (data) => {
		s3Path = [...s3Path, data?.name];
	};

	/**
	 * @param {dirConfig} data
	 */
	const handleOnFolderClick = (data) => {
		s3Path = [...s3Path, data?.name];
	};

	/**
	 * @param {dirConfig} data
	 */
	const handleOnFileClick = (data) => {
		console.log("TODO: render file based on it's type");
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
		{#each buckets as _bucket}
			<Directory
				id={_bucket.id}
				type="bucket"
				name={_bucket.name}
				handleOnClick={handleOnBucketClick}
			/>
		{/each}
	{:else}
		<div>
			{#each dirs.filter((d) => d.type === 'folder') as _dir}
				<Directory
					id={_dir.id}
					type={_dir.type}
					name={_dir.name}
					handleOnClick={handleOnFolderClick}
				/>
			{/each}
			{#each dirs.filter((d) => d.type === 'file') as _dir}
				<Directory
					id={_dir.id}
					type={_dir.type}
					name={_dir.name}
					handleOnClick={handleOnFileClick}
				/>
			{/each}
		</div>
	{/if}
</div>

<style lang="scss">
	.pointer-cursor {
		cursor: pointer;
	}
</style>
