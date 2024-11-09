<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import fetchApi from '$lib/fetch/fetch';
	import { isValidBucektName } from '$lib/utils';

	const errorMsg =
		'Bucket name should be lowercase letters, numbers, periods (.), and hyphens (-) ';

	let dialogOpen = false;
	let bucketName = '';
	let showError = false;

	/**
	 * @param {string} name
	 */
	const handleOnSubmit = async (name) => {
		showError = false;

		if (!isValidBucektName(name)) {
			showError = true;
			return;
		} else {
			await fetchApi('POST', 's3', '/buckets', { bucket_name: name });
			dialogOpen = false;
		}
	};
</script>

<Dialog.Root bind:open={dialogOpen}>
	<Button onclick={() => (dialogOpen = true)} class="h-6 text-base">Add Bucket</Button>
	<Dialog.Content class="sm:max-w-[450px]">
		<Dialog.Header>
			<Dialog.Title>Add Bucket</Dialog.Title>
			<Dialog.Description>Create your bucket with name</Dialog.Description>
		</Dialog.Header>
		<div class="grid gap-4 py-4">
			<div class="grid grid-cols-4 items-center gap-4">
				<Label for="bucekt-name" class="text-right">Bucket Name</Label>
				<Input id="bucekt-name" bind:value={bucketName} class="col-span-3" />
			</div>
			{#if showError}
				<span class="text-sm text-red-600">{errorMsg}</span>
			{/if}
		</div>
		<Dialog.Footer>
			<Button type="submit" onclick={() => handleOnSubmit(bucketName)}>Save changes</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
